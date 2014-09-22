# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os
import re
import sys
import glob
import ctypes
import ctypes.util

if sys.platform == "win32":
    from _ctypes import FreeLibrary as dlclose
else:
    from _ctypes import dlclose


def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []


class LibraryLoader(object):
    def __init__(self):
        self.other_dirs = []

    def find_library(self, libname):
        paths = self.getpaths(libname)
        for path in paths:
            if os.path.exists(path):
                return os.path.realpath(path)
        return None

    def load_library(self, libname):
        paths = self.getpaths(libname)
        for path in paths:
            if os.path.exists(path):
                return self.load(os.path.realpath(path))
        raise ImportError("%s not found." % libname)

    def unload_library(self, tdll):
        dlclose(tdll._handle)

    def load(self, path):
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError as e:
            raise ImportError(e)

    def getpaths(self, libname):
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path:
                yield path

    def getplatformpaths(self, libname):
        return []

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle",
                    "%s.dylib", "%s.framework", "%s.so", "%s.bundle", "%s"]

    def find_library(self, libname):
        paths = self.getpaths(libname)
        for path in paths:
            if os.path.exists(path):
                if os.path.isdir(path) and path.endswith(".framework"):
                    path = os.path.join(path, libname)
                return os.path.realpath(path)
        return None

    def load_library(self, libname):
        paths = self.getpaths(libname)
        for path in paths:
            if os.path.exists(path):
                if os.path.isdir(path) and path.endswith(".framework"):
                    path = os.path.join(path, libname)
                return self.load(os.path.realpath(path))
        raise ImportError("%s not found." % libname)

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [f % libname for f in self.name_formats]

        for dirname in self.getdirs(libname):
            for name in names:
                yield os.path.join(dirname, name)

    def getdirs(self, libname):
        """Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        """
        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []
        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)

        dirs.append(".")

        dirs.append(os.path.realpath(os.path.join(
            os.path.dirname(sys.executable), '..', 'Frameworks')))

        dirs.append(os.path.realpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', 'Frameworks')))

        dirs.extend(dyld_fallback_library_path)
        return dirs

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH",  # HPUX
                     "LIBPATH",  # OS/2, AIX
                     "LIBRARY_PATH",  # BE/OS
                     ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try:
            directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError:
            pass

        directories.extend(['/lib64', '/lib', '/usr/lib64', '/usr/lib',
                            '/usr/games/lib64', '/usr/games/lib', '/usr/local/lib',
                            '/usr/lib/x86_64-linux-gnu', '/usr/lib/i386-linux-gnu'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        for d in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % d):
                    f = os.path.basename(path)

                    # Index by filename
                    if f not in cache:
                        cache[f] = path

                    # Index by library name
                    match = lib_re.match(f)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result:
            yield result

        path = ctypes.util.find_library(libname)
        if path:
            yield os.path.join("/lib", path)


class _WindowsLibrary(object):
    def __init__(self, path):
        try:
            path = os.path.realpath(path)
            self.cdll = ctypes.cdll.LoadLibrary(path)
            self.windll = ctypes.windll.LoadLibrary(path)
        except WindowsError:
            os.environ['PATH'] = ';'.join(
                [os.path.dirname(path), os.environ['PATH']])
            path = os.path.basename(path)
            self.cdll = ctypes.cdll.LoadLibrary(path)
            self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try:
            return getattr(self.cdll, name)
        except AttributeError:
            try:
                return getattr(self.windll, name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

load = loader.load
load_library = loader.load_library
find_library = loader.find_library
unload_library = loader.unload_library

del loaderclass
