#!/usr/bin/env python

import os
import sys
import glob
import urllib
import shutil
import zipfile
import tempfile
import subprocess
from os.path import join, dirname, basename, realpath
from fnmatch import fnmatch
from distutils.core import setup, Command
from distutils.dep_util import newer
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.dir_util import copy_tree

sys.path.insert(0, realpath("src"))
from m64py.core.defs import FRONTEND_VERSION
BASE_DIR = dirname(realpath(__file__))


class build_qt(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def compile_ui(self, ui_file):
        from PyQt5 import uic
        py_file = os.path.splitext(ui_file)[0] + "_ui.py"
        if not newer(ui_file, py_file):
            return
        fp = open(py_file, "w")
        uic.compileUi(ui_file, fp, from_imports = True)
        fp.close()

    def compile_rc(self, qrc_file):
        import PyQt5
        py_file = os.path.splitext(qrc_file)[0] + "_rc.py"
        if not newer(qrc_file, py_file):
            return
        origpath = os.getenv("PATH")
        path = origpath.split(os.pathsep)
        path.append(dirname(PyQt5.__file__))
        os.putenv("PATH", os.pathsep.join(path))
        if subprocess.call(["pyrcc5", qrc_file, "-o", py_file]) > 0:
            self.warn("Unable to compile resource file %s" % qrc_file)
            if not os.path.exists(py_file):
                sys.exit(1)
        os.putenv('PATH', origpath)

    def run(self):
        basepath = join(dirname(__file__),
                'src', 'm64py', 'ui')
        for dirpath, dirs, filenames in os.walk(basepath):
            for filename in filenames:
                if filename.endswith('.ui'):
                    self.compile_ui(join(dirpath, filename))
                elif filename.endswith('.qrc'):
                    self.compile_rc(join(dirpath, filename))


class build_exe(Command):
    """Needs PyQt5, rarfile, PyLZMA, PyWin32, PyInstaller, Inno Setup 5"""
    user_options = []
    arch = "i686-w64-mingw32"
    url = "https://bitbucket.org/ecsv/mupen64plus-mxe-daily/get/master.zip"
    dist_dir = join(BASE_DIR, "dist", "windows")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def copy_emulator(self):
        tempdir = tempfile.mkdtemp()
        zippath = join(tempdir, basename(self.url))
        urllib.request.urlretrieve(self.url, zippath)
        zf = zipfile.ZipFile(zippath)
        for name in zf.namelist():
            if self.arch in name:
                dirn = basename(dirname(name))
                filen = basename(name)
                if not filen: continue
                dest_path = join(self.dist_dir, "m64py")
                if dirn == self.arch:
                    fullpath = join(dest_path, filen)
                else:
                    fullpath = join(dest_path, dirn, filen)
                    if not os.path.exists(join(dest_path, dirn)):
                        os.makedirs(join(dest_path, dirn))
                unpacked = open(fullpath, "wb")
                unpacked.write(zf.read(name))
                unpacked.close()
        zf.close()
        shutil.rmtree(tempdir)

    def copy_files(self):
        dest_path = join(self.dist_dir, "m64py")
        rar_dir = join(os.environ["ProgramFiles(x86)"], "Unrar")
        if not os.path.isfile(join(rar_dir, "UnRAR.exe")):
            tempdir = tempfile.mkdtemp()
            urllib.request.urlretrieve("http://www.rarlab.com/rar/unrarw32.exe", join(tempdir, "unrar.exe"))
            subprocess.call([join(tempdir, "unrar.exe"), "-s"])
            shutil.rmtree(tempdir)
        shutil.copy(join(rar_dir, "UnRAR.exe"), dest_path)
        shutil.copy(join(rar_dir, "license.txt"), join(dest_path, "doc", "unrar-license.txt"))
        for file_name in ["AUTHORS", "ChangeLog", "COPYING", "LICENSES", "README.md"]:
            shutil.copy(join(BASE_DIR, file_name), dest_path)

        import PyQt5
        qt5_dir = dirname(PyQt5.__file__)
        qwindows = join(qt5_dir, "plugins", "platforms", "qwindows.dll")
        qwindows_dest = join(dest_path, "qt5_plugins", "platforms")
        if not os.path.exists(qwindows_dest):
            os.makedirs(qwindows_dest)
        shutil.copy(qwindows, qwindows_dest)

    def remove_files(self):
        dest_path = join(self.dist_dir, "m64py")
        for dir_name in ["api", "include", "man6", "applications", "apps"]:
            shutil.rmtree(join(dest_path, dir_name))
        for file_name in glob.glob(join(dest_path, "icu*.dll")):
            os.remove(file_name)

    def run_build_installer(self):
        iss_file = ""
        iss_in = join(self.dist_dir, "m64py.iss.in")
        iss_out = join(self.dist_dir, "m64py.iss")
        with open(iss_in, "r") as iss: data = iss.read()
        lines = data.split("\n")
        for line in lines:
            line = line.replace("{ICON}", realpath(join(self.dist_dir, "m64py")))
            line = line.replace("{VERSION}", FRONTEND_VERSION)
            iss_file += line + "\n"
        with open(iss_out, "w") as iss: iss.write(iss_file)
        iscc = join(os.environ["ProgramFiles(x86)"], "Inno Setup 5", "ISCC.exe")
        subprocess.call([iscc, iss_out])

    def run_build(self):
        import PyInstaller.build
        work_path = join(self.dist_dir, "build")
        spec_file = join(self.dist_dir, "m64py.spec")
        os.environ["BASE_DIR"] = BASE_DIR
        os.environ["DIST_DIR"] = self.dist_dir
        opts = {"distpath": self.dist_dir, "workpath": work_path, "clean_build": True, "upx_dir": None, "debug": False}
        PyInstaller.build.main(None, spec_file, True, **opts)

    def run(self):
        self.run_command("build_qt")
        set_sdl2()
        set_rthook()
        self.run_build()
        self.copy_emulator()
        self.copy_files()
        self.remove_files()
        self.run_build_installer()


class build_zip(build_exe):

    def run_build_zip(self):
        os.rename(join(self.dist_dir, "m64py"), join(self.dist_dir, "m64py-%s" % FRONTEND_VERSION))
        shutil.make_archive(join(self.dist_dir, "m64py-%s-portable" % FRONTEND_VERSION),
                            "zip", self.dist_dir, "m64py-%s" % FRONTEND_VERSION, True)

    def set_config_path(self):
        core_file = ""
        core_path = join(BASE_DIR, "src", "m64py", "core", "core.py")
        with open(core_path, "r") as core: data = core.read()
        lines = data.split("\n")
        for line in lines:
            if "C.c_int(CORE_API_VERSION)" in line:
                line = line.replace("None", "C.c_char_p(os.getcwd().encode())")
            core_file += line + "\n"
        with open(core_path, "w") as core: core.write(core_file)

        settings_file = ""
        settings_path = join(BASE_DIR, "src", "m64py", "frontend", "settings.py")
        with open(settings_path, "r") as core: data = core.read()
        lines = data.split("\n")
        for line in lines:
            if "QSettings(" in line:
                line = line.replace('QSettings("m64py", "m64py")',
                                    'QSettings(os.path.join(os.getcwd(), "m64py.ini"), QSettings.IniFormat)')
            settings_file += line + "\n"
        with open(settings_path, "w") as core: core.write(settings_file)

    def run(self):
        self.run_command("build_qt")
        set_sdl2()
        set_rthook()
        self.set_config_path()
        self.run_build()
        self.copy_emulator()
        self.copy_files()
        self.remove_files()
        self.run_build_zip()


class build_dmg(Command):
    user_options = []
    dist_dir = join(BASE_DIR, "dist", "macosx")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def set_plist(self):
        info_plist = join(self.dist_dir, "dmg", "M64Py.app", "Contents", "Info.plist")
        shutil.copy(join(self.dist_dir, "m64py.icns"),
                    join(self.dist_dir, "dmg", "M64Py.app", "Contents", "Resources"))
        shutil.copy(join(self.dist_dir, "m64py.sh"),
                    join(self.dist_dir, "dmg", "M64Py.app", "Contents", "MacOS"))
        with open(info_plist, "r") as opts: data = opts.read()
        plist_file = ""
        lines = data.split("\n")
        for line in lines:
            if "0.0.0" in line:
                line = line.replace("0.0.0", FRONTEND_VERSION)
            elif "icon-windowed.icns" in line:
                line = line.replace("icon-windowed.icns", "m64py.icns")
            elif "MacOS/m64py" in line:
                line = line.replace("MacOS/m64py", "m64py.sh")
            plist_file += line + "\n"
        with open(info_plist, "w") as opts: opts.write(plist_file)

    def copy_emulator(self):
        src_path = join(self.dist_dir, "mupen64plus", "Contents")
        dest_path = join(self.dist_dir, "dmg", "M64Py.app", "Contents")
        copy_tree(src_path, dest_path)

    def copy_files(self):
        dest_path = join(self.dist_dir, "dmg")
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
        shutil.move(join(self.dist_dir, "M64Py.app"), dest_path)
        for file_name in ["AUTHORS", "ChangeLog", "COPYING", "LICENSES", "README.md"]:
            shutil.copy(join(BASE_DIR, file_name), dest_path)
        shutil.copy(join(BASE_DIR, "test", "mupen64plus.v64"), dest_path)

    def remove_files(self):
        dest_path = join(self.dist_dir, "dmg", "M64Py.app", "Contents", "MacOS")
        for dir_name in ["include", "lib"]:
            shutil.rmtree(join(dest_path, dir_name))
        os.remove(join(self.dist_dir, "dmg", "M64Py.app", "Contents", "Resources", "icon-windowed.icns"))

    def run_build_dmg(self):
        src_path = join(self.dist_dir, "dmg")
        dst_path = join(self.dist_dir, "m64py-%s.dmg" % FRONTEND_VERSION)
        subprocess.call(["hdiutil", "create", dst_path, "-srcfolder", src_path])

    def run_build(self):
        import PyInstaller.build
        work_path = join(self.dist_dir, "build")
        spec_file = join(self.dist_dir, "m64py.spec")
        os.environ["BASE_DIR"] = BASE_DIR
        os.environ["DIST_DIR"] = self.dist_dir
        opts = {"distpath": self.dist_dir, "workpath": work_path, "clean_build": True, "upx_dir": None, "debug": False}
        PyInstaller.build.main(None, spec_file, True, **opts)

    def run(self):
        self.run_command("build_qt")
        set_sdl2()
        set_rthook()
        self.run_build()
        self.copy_files()
        self.copy_emulator()
        self.remove_files()
        self.set_plist()
        self.run_build_dmg()


def set_sdl2():
    opts_file = ""
    opts_path = join(BASE_DIR, "src", "m64py", "opts.py")
    with open(opts_path, "r") as opts: data = opts.read()
    lines = data.split("\n")
    for line in lines:
        if "sdl2" in line:
            line = line.replace("default=False", "default=True")
        opts_file += line + "\n"
    with open(opts_path, "w") as opts: opts.write(opts_file)


def set_rthook():
    import PyInstaller
    hook_file = ""
    module_dir = dirname(PyInstaller.__file__)
    rthook = join(module_dir, "loader", "rthooks", "pyi_rth_qt5plugins.py")
    with open(rthook, "r") as hook: data = hook.read()
    if "import sip" not in data:
        lines = data.split("\n")
        for line in lines:
            hook_file += line + "\n"
            if "MEIPASS" in line:
                hook_file += "\nimport sip\n"
        with open(rthook, "w") as hook: hook.write(hook_file)


class clean_local(Command):
    pats = ['*.py[co]', '*_ui.py', '*_rc.py', '__pycache__']
    excludedirs = ['.git', 'build', 'dist']
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for e in self._walkpaths('.'):
            if os.path.isdir(e):
                shutil.rmtree(e)
            else:
                os.remove(e)

    def _walkpaths(self, path):
        for root, dirs, files in os.walk(path):
            if any(root == join(path, e) or root.startswith(
                    join(path, e, '')) for e in self.excludedirs):
                continue
            for d in dirs:
                fpath = join(root, d)
                if any(fnmatch(d, p) for p in self.pats):
                    yield fpath
            for e in files:
                fpath = join(root, e)
                if any(fnmatch(fpath, p) for p in self.pats):
                    yield fpath


class mybuild(build):
    def run(self):
        self.run_command("build_qt")
        build.run(self)


class myclean(clean):
    def run(self):
        self.run_command("clean_local")
        clean.run(self)

cmdclass = {
    'build': mybuild,
    'build_qt': build_qt,
    'build_exe': build_exe,
    'build_zip': build_zip,
    'build_dmg': build_dmg,
    'clean': myclean,
    'clean_local': clean_local
}

setup(
    name = "m64py",
    version = FRONTEND_VERSION,
    description = "M64Py - A frontend for Mupen64Plus",
    long_description = "M64Py is a Qt5 front-end (GUI) for Mupen64Plus 2.0, a cross-platform plugin-based Nintendo 64 emulator.",
    author = "Milan Nikolic",
    author_email = "gen2brain@gmail.com",
    license = "GNU GPLv3",
    url = "http://m64py.sourceforge.net",
    packages = ["m64py", "m64py.core", "m64py.frontend", "m64py.ui", "m64py.SDL", "m64py.SDL2"],
    package_dir = {"": "src"},
    scripts = ["m64py"],
    requires = ["PyQt5"],
    platforms = ["Linux", "Windows", "Darwin"],
    cmdclass = cmdclass,
    data_files = [
        ("share/pixmaps", ["xdg/m64py.png"]),
        ("share/applications", ["xdg/m64py.desktop"]),
    ]
)
