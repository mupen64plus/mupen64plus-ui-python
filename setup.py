#!/usr/bin/env python

import fnmatch
import glob
import os
import shutil
import subprocess
import sys
import fileinput

import setuptools

try:
    from setuptools.modified import newer
except ImportError:
    from distutils.dep_util import newer

# Add the src folder to the path
sys.path.insert(0, os.path.realpath("src"))

from m64py.core.defs import FRONTEND_VERSION

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class BuildQt(setuptools.Command):

    description = "Build the Qt interface"

    boolean_options = []
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def compile_rc(self, qrc_file):
        py_file = os.path.splitext(qrc_file)[0] + "_rc.py"
        if not newer(qrc_file, py_file):
            return
        rcc_exe = self.find_executable("rcc")
        if rcc_exe is None:
            self.warn("Unable to find Qt Resource Compiler (rcc)")
            sys.exit(1)
        if subprocess.call(["rcc", "-g", "python", qrc_file, "-o", py_file]) > 0:
            self.warn("Unable to compile resource file {}".format(qrc_file))
            if not os.path.exists(py_file):
                sys.exit(1)
        for line in fileinput.input(py_file, inplace=True):
            if "PySide6" in line:
                line = line.replace("PySide6", "PyQt6")
            sys.stdout.write(line)

    def compile_ui(self, ui_file):
        from PyQt6 import uic
        py_file = os.path.splitext(ui_file)[0] + "_ui.py"
        if not newer(ui_file, py_file):
            return
        with open(py_file, "w") as a_file:
            uic.compileUi(ui_file, a_file)

    def compile_ts(self, ts_file):
        qm_file = os.path.splitext(ts_file)[0] + ".qm"
        if not newer(ts_file, qm_file):
            return
        lr_exe = self.find_executable("lrelease")
        if lr_exe is None:
            self.warn("Unable to find Qt Linguist (lrelease)")
            sys.exit(1)
        if subprocess.call([lr_exe, ts_file, "-qm", qm_file]) > 0:
            self.warn("Unable to compile translation file {}".format(qm_file))
            if not os.path.exists(qm_file):
                sys.exit(1)

    def find_executable(self, name):
        from PyQt6.QtCore import QLibraryInfo
        path = os.getenv("PATH").split(os.pathsep)

        bin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.BinariesPath)
        path.insert(0, bin_path)
        os.environ["PATH"] = os.pathsep.join(path)
        exe = shutil.which(name)
        if exe:
            return exe

        libexec_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.LibraryExecutablesPath)
        path.insert(0, libexec_path)
        os.environ["PATH"] = os.pathsep.join(path)
        exe = shutil.which(name)
        if exe:
            return exe

        path.extend(["/usr/lib64/qt6/bin", "/usr/lib64/qt6/libexec",
                     "/usr/lib/qt6/bin", "/usr/lib/qt6/libexec",
                     "/usr/lib/x86_64-linux-gnu/qt6/bin", "/usr/lib/x86_64-linux-gnu/qt6/libexec"])
        os.environ["PATH"] = os.pathsep.join(path)
        exe = shutil.which(name)
        if exe:
            return exe

        return None

    def run(self):
        basepath = os.path.join(os.path.dirname(__file__), "src", "m64py", "ui")
        for dirpath, _, filenames in os.walk(basepath):
            for filename in filenames:
                if filename.endswith('.ts'):
                    self.compile_ts(os.path.join(dirpath, filename))
        for dirpath, _, filenames in os.walk(basepath):
            for filename in filenames:
                if filename.endswith('.ui'):
                    self.compile_ui(os.path.join(dirpath, filename))
                elif filename.endswith('.qrc'):
                    self.compile_rc(os.path.join(dirpath, filename))


class BuildDmg(setuptools.Command):

    description = "Generate a .dmg file for distribution"

    user_options = []

    dist_dir = os.path.join(BASE_DIR, "dist", "macosx")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def copy_emulator(self):
        src_path = os.path.join(self.dist_dir, "mupen64plus", "Contents")
        dest_path = os.path.join(self.dist_dir, "dmg", "M64Py.app", "Contents")
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)

    def copy_files(self):
        dest_path = os.path.join(self.dist_dir, "dmg")
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
        shutil.move(os.path.join(self.dist_dir, "M64Py.app"), dest_path)
        for file_name in ["AUTHORS", "CHANGELOG", "COPYING", "LICENSES", "README.rst"]:
            shutil.copy(os.path.join(BASE_DIR, file_name), dest_path)
        shutil.copy(os.path.join(BASE_DIR, "test", "mupen64plus.v64"), dest_path)

    def remove_files(self):
        dest_path = os.path.join(self.dist_dir, "dmg", "M64Py.app", "Contents")
        for dir_name in ["include", "lib"]:
            shutil.rmtree(os.path.join(dest_path, "Resources", dir_name), True)
            os.remove(os.path.join(dest_path, "MacOS", dir_name))
        os.remove(os.path.join(dest_path, "Resources", "icon-windowed.icns"))

    def run_build(self):
        import PyInstaller.building.build_main
        work_path = os.path.join(self.dist_dir, "build")
        spec_file = os.path.join(self.dist_dir, "m64py.spec")
        os.environ["BASE_DIR"] = BASE_DIR
        os.environ["DIST_DIR"] = self.dist_dir
        opts = {"distpath": self.dist_dir,
                "workpath": work_path,
                "clean_build": True,
                "upx_dir": None,
                "debug": False}
        PyInstaller.building.build_main.main(None, spec_file, True, **opts)

    def run_build_dmg(self):
        src_path = os.path.join(self.dist_dir, "dmg")
        dst_path = os.path.join(self.dist_dir, "m64py-{}.dmg".format(FRONTEND_VERSION))
        subprocess.call(["hdiutil", "create", dst_path, "-srcfolder", src_path])

    def set_plist(self):
        info_plist = os.path.join(self.dist_dir, "dmg", "M64Py.app", "Contents", "Info.plist")
        shutil.copy(os.path.join(self.dist_dir, "m64py.icns"),
                    os.path.join(self.dist_dir, "dmg", "M64Py.app", "Contents", "Resources"))
        shutil.copy(os.path.join(self.dist_dir, "m64py.sh"),
                    os.path.join(self.dist_dir, "dmg", "M64Py.app", "Contents", "MacOS"))
        with open(info_plist, "r") as opts:
            data = opts.read()
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
        with open(info_plist, "w") as opts:
            opts.write(plist_file)

    def run(self):
        self.run_command("build_qt")
        self.run_build()
        self.copy_files()
        self.copy_emulator()
        self.remove_files()
        self.set_plist()
        self.run_build_dmg()


class BuildExe(setuptools.Command):
    """
    Requires PyQt6, rarfile, WinRAR, PyLZMA, PyWin32, PyInstaller and Inno Setup 6.
    """

    description = "Generate a .exe file for distribution"

    boolean_options = []
    user_options = []

    dist_dir = os.path.join(BASE_DIR, "dist", "windows")
    dest_path = os.path.join(dist_dir, "m64py")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def copy_emulator(self):
        src_path = os.path.join(self.dist_dir, "mupen64plus")
        shutil.copytree(src_path, self.dest_path, dirs_exist_ok=True)

    def copy_files(self):
        rar_dir = os.path.join(os.environ["ProgramFiles"], "WinRAR")
        shutil.copy(os.path.join(rar_dir, "UnRAR.exe"), self.dest_path)
        shutil.copy(os.path.join(rar_dir, "License.txt"),
                    os.path.join(self.dest_path, "doc", "unrar-license"))
        for file_name in ["AUTHORS", "CHANGELOG", "COPYING", "LICENSES", "README.rst"]:
            shutil.copy(os.path.join(BASE_DIR, file_name), self.dest_path)
        shutil.copy(os.path.join(BASE_DIR, "test", "mupen64plus.v64"), self.dest_path)
        shutil.copy(os.path.join(self.dest_path, "SDL2.dll"), os.path.join(self.dest_path, "_internal"))

    def remove_files(self):
        for dir_name in ["api", "man6", "usr"]:
            shutil.rmtree(os.path.join(self.dest_path, dir_name), True)
        for dir_name in ["translations"]:
            shutil.rmtree(os.path.join(self.dest_path, "_internal", "PyQt6", "Qt6", dir_name), True)
        for file_name in glob.glob(os.path.join(self.dest_path, "_internal", "PyQt6", "Qt6", "bin", "Qt*.dll")):
           if os.path.basename(file_name) not in ["Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll"]:
               os.remove(file_name)
        for file_name in ["qpdf.dll", "qsvg.dll", "qwbmp.dll", "qtga.dll", "qtiff.dll", "qwebp.dll"]:
            os.remove(os.path.join(self.dest_path, "_internal", "PyQt6", "Qt6", "plugins", "imageformats", file_name))
        os.remove(os.path.join(self.dest_path, "_internal", "libcrypto-3.dll"))
        os.remove(os.path.join(self.dest_path, "_internal", "PyQt6", "Qt6", "bin", "opengl32sw.dll"))

    def run_build(self):
        import PyInstaller.building.build_main
        work_path = os.path.join(self.dist_dir, "build")
        spec_file = os.path.join(self.dist_dir, "m64py.spec")
        os.environ["BASE_DIR"] = BASE_DIR
        os.environ["DIST_DIR"] = self.dist_dir
        PyInstaller.building.build_main.main(None, spec_file, noconfirm=True, distpath=self.dist_dir,
                                             workpath=work_path, upx_dir=None, clean_build=True)

    def run_build_installer(self):
        iss_file = ""
        iss_in = os.path.join(self.dist_dir, "m64py.iss.in")
        iss_out = os.path.join(self.dist_dir, "m64py.iss")
        with open(iss_in, "r") as iss:
            data = iss.read()
        lines = data.split("\n")
        for line in lines:
            line = line.replace("{ICON}", os.path.realpath(os.path.join(self.dist_dir, "m64py")))
            line = line.replace("{VERSION}", FRONTEND_VERSION)
            iss_file += line + "\n"
        with open(iss_out, "w") as iss:
            iss.write(iss_file)
        iscc = os.path.join(os.environ["ProgramFiles(x86)"], "Inno Setup 6", "ISCC.exe")
        subprocess.call([iscc, iss_out])

    def run(self):
        self.run_command("build_qt")
        self.run_build()
        self.copy_emulator()
        self.copy_files()
        self.remove_files()
        self.run_build_installer()


class BuildZip(BuildExe):

    description = "Generate a .zip file for distribution"

    def run_build_zip(self):
        os.rename(os.path.join(self.dist_dir, "m64py"),
                  os.path.join(self.dist_dir, "m64py-{}".format(FRONTEND_VERSION)))
        shutil.make_archive(os.path.join(self.dist_dir, "m64py-{}-portable-x86_64".format(FRONTEND_VERSION)),
                            "zip",
                            self.dist_dir, "m64py-{}".format(FRONTEND_VERSION),
                            True)

    @staticmethod
    def set_config_path():
        core_file = ""
        core_path = os.path.join(BASE_DIR, "src", "m64py", "core", "core.py")
        with open(core_path, "r") as core:
            data = core.read()
        lines = data.split("\n")
        for line in lines:
            if "C.c_int(CORE_API_VERSION)" in line:
                line = line.replace("None", "C.c_char_p(os.getcwd().encode())")
            core_file += line + "\n"
        with open(core_path, "w") as core:
            core.write(core_file)

        settings_file = ""
        settings_path = os.path.join(BASE_DIR, "src", "m64py", "frontend", "settings.py")
        with open(settings_path, "r") as core:
            data = core.read()
        lines = data.split("\n")
        for line in lines:
            if "QSettings(" in line:
                line = line.replace("QSettings(config_file, QSettings.Format.IniFormat)",
                                    "QSettings(os.path.join(os.getcwd(), \"m64py.conf\"), QSettings.Format.IniFormat)")
            settings_file += line + "\n"
        with open(settings_path, "w") as core:
            core.write(settings_file)

    def run(self):
        self.run_command("build_qt")
        self.set_config_path()
        self.run_build()
        self.copy_emulator()
        self.copy_files()
        self.remove_files()
        self.run_build_zip()


class CleanLocal(setuptools.Command):

    description = "Clean the local project directory"

    wildcards = ['*.py[co]', '*_ui.py', '*_rc.py', '__pycache__', '*.qm']
    excludedirs = ['.git', 'build', 'dist']
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _walkpaths(self, path):
        for root, dirs, files in os.walk(path):
            for excluded_dir in self.excludedirs:
                abs_excluded_dir = os.path.join(path, excluded_dir)
                if root == abs_excluded_dir or root.startswith(abs_excluded_dir + os.sep):
                    continue
            for a_dir in dirs:
                file_path = os.path.join(root, a_dir)
                if any(fnmatch.fnmatch(a_dir, pattern) for pattern in self.wildcards):
                    yield file_path
            for a_file in files:
                file_path = os.path.join(root, a_file)
                if any(fnmatch.fnmatch(file_path, pattern) for pattern in self.wildcards):
                    yield file_path

    def run(self):
        for a_path in self._walkpaths('.'):
            if os.path.isdir(a_path):
                shutil.rmtree(a_path)
            else:
                os.remove(a_path)


setuptools.setup(
    name="m64py",
    version=FRONTEND_VERSION,
    description="A frontend for Mupen64Plus",
    long_description="A Qt6 front-end (GUI) for Mupen64Plus, a cross-platform plugin-based Nintendo 64 emulator.",
    author="Milan Nikolic",
    author_email="gen2brain@gmail.com",
    license="GNU GPLv3",
    url="https://m64py.sourceforge.net",
    package_dir={'': "src"},
    packages=["m64py", "m64py.core", "m64py.frontend", "m64py.ui"],
    scripts=["bin/m64py"],
    requires=["PyQt6", "PySDL2"],
    platforms=["Linux", "Windows", "Darwin"],
    cmdclass={
        'build': BuildQt,
        'build_dmg': BuildDmg,
        'build_exe': BuildExe,
        'build_qt': BuildQt,
        'build_zip': BuildZip,
        'clean': CleanLocal
    },
    data_files=[
        ("share/pixmaps", ["xdg/m64py.png"]),
        ("share/applications", ["xdg/m64py.desktop"]),
    ]
)
