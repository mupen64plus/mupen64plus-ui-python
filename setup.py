#!/usr/bin/env python

import os
import re
import io
import sys
import glob
import shutil
import fnmatch
import subprocess
import fileinput

import setuptools
from setuptools.command.build import build


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FRONTEND_VERSION = re.search(r'FRONTEND_VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open(os.path.join(BASE_DIR, "src", "m64py", "core", "defs.py")).read()).group(1)


class BuildQt(setuptools.Command):

    description = "Build the Qt user interface"

    boolean_options = []
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def newer(self, source, target):
        return not os.path.exists(target) or (os.path.getmtime(source) > os.path.getmtime(target))

    def compile_rc(self, qrc_file):
        py_file = os.path.splitext(qrc_file)[0] + "_rc.py"
        if not self.newer(qrc_file, py_file):
            return
        rcc_exe = self.find_executable("rcc")
        if rcc_exe is None:
            self.warn("Unable to find Qt Resource Compiler (rcc)")
            sys.exit(1)
        if subprocess.call([rcc_exe, "-g", "python", qrc_file, "-o", py_file]) > 0:
            self.warn("Unable to compile resource file {}".format(qrc_file))
            if not os.path.exists(py_file):
                sys.exit(1)
        for line in fileinput.input(py_file, inplace=True):
            if "PySide6" in line:
                line = line.replace("PySide6", "PyQt6")
            sys.stdout.write(line)

    def compile_ui(self, ui_file):
        py_file = os.path.splitext(ui_file)[0] + "_ui.py"
        if not self.newer(ui_file, py_file):
            return
        uic_exe = self.find_executable("pyuic6")
        if uic_exe is None:
            self.warn("Unable to find Qt User Interface Compiler (pyuic6)")
            sys.exit(1)
        if subprocess.call([uic_exe, "-o", py_file, ui_file]) > 0:
            self.warn("Unable to compile ui file {}".format(ui_file))
            if not os.path.exists(py_file):
                sys.exit(1)

    def compile_ts(self, ts_file):
        qm_file = os.path.splitext(ts_file)[0] + ".qm"
        if not self.newer(ts_file, qm_file):
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
        path = os.getenv("PATH").split(os.pathsep)
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
        for dir_name in ["QtNetwork.framework", "QtPdf.framework", "QtSvg.framework"]:
            shutil.rmtree(os.path.join(dest_path, "Frameworks", "PyQt6", "Qt6", "lib", dir_name), True)
        for file_name in ["QtNetwork", "QtPdf", "QtSvg"]:
            os.remove(os.path.join(dest_path, "Frameworks", file_name))
            os.remove(os.path.join(dest_path, "Resources", file_name))
        for file_name in ["libqpdf.dylib", "libqsvg.dylib", "libqwbmp.dylib", "libqtga.dylib", "libqtiff.dylib", "libqwebp.dylib"]:
            os.remove(os.path.join(dest_path, "Frameworks", "PyQt6", "Qt6", "plugins", "imageformats", file_name))
        for dir_name in ["Frameworks", "Resources"]:
            os.remove(os.path.join(dest_path, dir_name, "libcrypto.3.dylib"))
            os.remove(os.path.join(dest_path, dir_name, "libssl.3.dylib"))
        shutil.rmtree(os.path.join(dest_path, "Resources", "PyQt6", "Qt6", "translations"), True)
        os.remove(os.path.join(dest_path, "Frameworks", "PyQt6", "Qt6", "translations"))
        os.remove(os.path.join(dest_path, "Resources", "icon-windowed.icns"))

    def run_build(self):
        import PyInstaller.building.build_main
        work_path = os.path.join(self.dist_dir, "build")
        spec_file = os.path.join(self.dist_dir, "m64py.spec")
        os.environ["BASE_DIR"] = BASE_DIR
        os.environ["DIST_DIR"] = self.dist_dir
        PyInstaller.building.build_main.main(None, spec_file, noconfirm=True, distpath=self.dist_dir,
                                             workpath=work_path, upx_dir=None, clean_build=True)

    def run_build_dmg(self):
        src_path = os.path.join(self.dist_dir, "dmg")
        dst_path = os.path.join(self.dist_dir, "m64py-{}.dmg".format(FRONTEND_VERSION))
        subprocess.call(["hdiutil", "create", dst_path, "-srcfolder", src_path])

    def set_plist(self):
        info_plist = os.path.join(self.dist_dir, "dmg", "M64Py.app", "Contents", "Info.plist")
        shutil.copy(os.path.join(self.dist_dir, "m64py.icns"),
                    os.path.join(self.dist_dir, "dmg", "M64Py.app", "Contents", "Resources"))
        with open(info_plist, "r") as opts:
            data = opts.read()
        plist_file = ""
        lines = data.split("\n")
        for line in lines:
            if "0.0.0" in line:
                line = line.replace("0.0.0", FRONTEND_VERSION)
            elif "icon-windowed.icns" in line:
                line = line.replace("icon-windowed.icns", "m64py.icns")
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

    wildcards = ['*.py[co]', '*_ui.py', '*_rc.py', '__pycache__', '*.qm', "build", "*.egg-info"]
    excludedirs = ['.git', 'dist']
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


class BuildCustom(build):
    sub_commands = [('build_qt', None)] + build.sub_commands


setuptools.setup(
    name = "m64py",
    version = FRONTEND_VERSION,
    description = "A frontend for Mupen64Plus",
    long_description = "A Qt6 front-end (GUI) for Mupen64Plus, a cross-platform plugin-based Nintendo 64 emulator.",
    author = "Milan Nikolic",
    author_email = "gen2brain@gmail.com",
    license = "GNU GPLv3",
    url = "https://m64py.sourceforge.net",
    package_dir = {"": "src"},
    packages = setuptools.find_namespace_packages(where="src"),
    scripts = ["bin/m64py"],
    requires = ["PyQt6", "PySDL2"],
    cmdclass = {
        'build': BuildCustom,
        'build_qt': BuildQt,
        'build_dmg': BuildDmg,
        'build_exe': BuildExe,
        'build_zip': BuildZip,
        'clean': CleanLocal
    },
    data_files = [
        ("share/icons/hicolor/96x96/apps", ["xdg/net.sourceforge.m64py.M64Py.png"]),
        ("share/applications", ["xdg/net.sourceforge.m64py.M64Py.desktop"]),
    ]
)
