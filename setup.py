#!/usr/bin/env python

import os
import sys
from fnmatch import fnmatch
from distutils.core import setup, Command
from distutils.dep_util import newer
from distutils.command.build import build
from distutils.command.clean import clean

sys.path.append(os.path.realpath("src"))
from m64py.core.defs import FRONTEND_VERSION

class build_qt(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def compile_ui(self, ui_file):
        try:
            from PyQt4 import uic
            py_file = os.path.splitext(ui_file)[0] + "_ui.py"
            if not newer(ui_file, py_file):
                return
            fp = open(py_file, 'w')
            uic.compileUi(ui_file, fp)
            fp.close()
        except Exception, err:
            self.warn('Unable to compile ui file %s: %s' % (ui_file, err))
            if not os.path.exists(py_file):
                sys.exit(1)
            return

    def compile_rc(self, qrc_file):
        import PyQt4
        py_file = os.path.splitext(qrc_file)[0] + "_rc.py"
        if not newer(qrc_file, py_file):
            return
        origpath = os.getenv('PATH')
        path = origpath.split(os.pathsep)
        pyqtfolder = os.path.dirname(PyQt4.__file__)
        path.append(os.path.join(pyqtfolder, 'bin'))
        os.putenv('PATH', os.pathsep.join(path))
        if os.system('pyrcc4 "%s" -o "%s"' % (qrc_file, py_file)) > 0:
            self.warn("Unable to compile resource file %s" % (qrc_file))
            if not os.path.exists(py_file):
                sys.exit(1)
        os.putenv('PATH', origpath)

    def run(self):
        basepath = os.path.join(os.path.dirname(__file__), 'src', 'm64py', 'ui')
        for dirpath, dirs, filenames in os.walk(basepath):
            for filename in filenames:
                if filename.endswith('.ui'):
                    self.compile_ui(os.path.join(dirpath, filename))
                elif filename.endswith('.qrc'):
                    self.compile_rc(os.path.join(dirpath, filename))

class clean_qt(Command):
    pats = ['*.py[co]', '*_ui.py', '*_rc.py']
    excludedirs = ['.git', 'build', 'dist']
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for e in self._walkpaths('.'):
            os.remove(e)

    def _walkpaths(self, path):
        for root, _dirs, files in os.walk(path):
            if any(root == os.path.join(path, e) or root.startswith(
                os.path.join(path, e, '')) for e in self.excludedirs):
                continue
            for e in files:
                fpath = os.path.join(root, e)
                if any(fnmatch(fpath, p) for p in self.pats):
                    yield fpath

class mybuild(build):
    def run(self):
        self.run_command("build_qt")
        build.run(self)

class myclean(clean):
    def run(self):
        self.run_command("clean_qt")
        clean.run(self)

cmdclass = {
        'build': mybuild,
        'build_qt': build_qt,
        'clean': myclean,
        'clean_qt': clean_qt
    }

setup(name = "m64py",
        version = FRONTEND_VERSION,
        description = "M64Py - A frontend for Mupen64Plus",
        long_description = "M64Py is a Qt4 front-end (GUI) for Mupen64Plus 2.0, a cross-platform plugin-based Nintendo 64 emulator.",
        author = "Milan Nikolic",
        author_email = "gen2brain@gmail.com",
        license = "GNU GPLv3",
        url = "http://m64py.sourceforge.net",
        packages = ["m64py", "m64py.core", "m64py.frontend", "m64py.ui", "m64py.SDL", "m64py.SDL2"],
        package_dir = {"": "src"},
        scripts = ["m64py"],
        requires = ["PyQt4"],
        platforms = ["Linux", "Windows", "Darwin"],
        cmdclass = cmdclass,
        data_files = [
            ("share/pixmaps", ["xdg/m64py.png"]),
            ("share/applications", ["xdg/m64py.desktop"]),
            ("share/mime/packages", ["xdg/application-x-m64py.xml"]),
            ("share/icons/hicolor/96x96/mimetypes/application-x-m64py.png",
                ["xdg/application-x-m64py.xml"])
            ]
        )
