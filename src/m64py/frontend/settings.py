# -*- coding: utf-8 -*-
# Author: Milan Nikolic <gen2brain@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from m64py.core.defs import *
from m64py.loader import find_library
from m64py.core.vidext import MODES
from m64py.platform import DLL_FILTER
from m64py.frontend.plugin import Plugin
from m64py.frontend.input import Input
from m64py.ui.settings_ui import Ui_Settings

class Settings(QDialog, Ui_Settings):
    """Settings dialog"""

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.m64p = None
        self.m64p_handle = None
        self.plugins = []
        self.qset = QSettings("m64py", "m64py")
        self.input = Input(self.parent)
        self.add_items()
        self.connect_signals()

    def showEvent(self, event):
        self.set_config()

    def closeEvent(self, event):
        self.save_config()

    def add_items(self):
        self.combomap = {
                M64PLUGIN_RSP: (
                    self.comboRSP, self.pushButtonRSP,
                    Plugin(self.parent)),
                M64PLUGIN_GFX: (
                    self.comboVideo, self.pushButtonVideo,
                    Plugin(self.parent)),
                M64PLUGIN_AUDIO: (
                    self.comboAudio, self.pushButtonAudio,
                    Plugin(self.parent)),
                M64PLUGIN_INPUT: (
                    self.comboInput, self.pushButtonInput,
                    self.input)}

        self.emumode = [
                QRadioButton(self.tr("Pure Interpreter")),
                QRadioButton(self.tr("Cached Interpreter")),
                QRadioButton(self.tr("Dynamic Recompiler"))]

        vbox = QVBoxLayout(self.groupEmuMode)
        for widget in self.emumode:
            vbox.addWidget(widget)

    def show_page(self, index=0):
        self.tabWidget.setCurrentIndex(index)
        self.show()

    def save_config(self):
        self.save_paths()
        self.save_plugins()
        if self.m64p_handle:
            self.save_video()
            self.save_core()
            self.m64p.config.save_file()
        self.qset.sync()

    def set_config(self):
        if self.m64p_handle:
            self.set_paths()
            self.set_plugins()
            self.set_video()
            self.set_core()

    def connect_signals(self):
        self.browseLibrary.clicked.connect(lambda: self.browse_dialog(
                (self.pathLibrary, self.groupLibrary, False)))
        self.browsePlugins.clicked.connect(lambda: self.browse_dialog(
                (self.pathPlugins, self.groupPlugins, True)))
        self.browseData.clicked.connect(lambda: self.browse_dialog(
                (self.pathData, self.groupData, True)))
        self.browseROM.clicked.connect(lambda: self.browse_dialog(
                (self.pathROM, self.groupROM, True)))
        for plugin_type in self.combomap:
            self.connect_combo_signals(self.combomap[plugin_type])

    def connect_combo_signals(self, combomap):
        combo,button,settings = combomap
        if settings is not None:
            if combo != self.comboInput:
                combo.activated.connect(
                        lambda: self.set_section(combo,button,settings))
            button.clicked.connect(settings.show_dialog)

    def browse_dialog(self, args):
        widget, groupbox, directory = args
        dialog = QFileDialog()
        if directory:
            dialog.setFileMode(QFileDialog.Directory)
            path = dialog.getExistingDirectory(
                    self, groupbox.title(), "", QFileDialog.ShowDirsOnly)
        else:
            dialog.setFileMode(QFileDialog.ExistingFile)
            path = dialog.getOpenFileName(
                    self, groupbox.title(), "",
                    "%s (*%s);;All files (*)" % (groupbox.title(), DLL_FILTER))

        if not path: return
        widget.setText(path)
        if widget == self.pathLibrary:
            if not self.m64p_handle:
                self.parent.worker.core_load(path)
                if self.parent.worker.m64p.get_handle():
                    self.m64p = self.parent.worker.m64p
                    self.m64p_handle = self.m64p.get_handle()

                    self.set_core()
                    self.set_video()
                    self.set_default_general()
                    size = self.qset.value("size", SIZE_1X)
                    self.parent.window_size_triggered(size)

                    self.parent.emit(SIGNAL(
                        "state_changed(PyQt_PyObject)"),
                        (True, False, False, False))
        elif widget == self.pathPlugins:
            if self.m64p_handle:
                self.m64p.plugins_unload()
                self.parent.worker.plugin_load_try(path)
                self.set_plugins()

    def get_section(self, combo):
        plugin = combo.currentText()
        index = combo.findText(plugin)
        desc = combo.itemData(index)
        name = os.path.splitext(plugin)[0][12:]
        section = "-".join([n.capitalize() for n in name.split("-")])
        return (section, desc)

    def set_section(self, combo, button, settings):
        if settings:
            if combo != self.comboInput:
                section, desc = self.get_section(combo)
                settings.set_section(section, desc)
                self.m64p.config.open_section(section)
                items = self.m64p.config.parameters[
                        self.m64p.config.section].items()
                if items:
                    button.setEnabled(True)
                else:
                    button.setEnabled(False)
            else:
                button.setEnabled(True)
        else:
            button.setEnabled(False)

    def set_default_general(self):
        self.m64p.config.open_section("Video-General")
        self.m64p.config.set_default(M64TYPE_INT, "ScreenWidth", 320,
                "Width of output window or fullscreen width")
        self.m64p.config.set_default(M64TYPE_INT, "ScreenHeight", 240,
                "Height of output window or fullscreen height")
        self.m64p.config.set_default(M64TYPE_INT, "Fullscreen", False,
                "Use fullscreen mode if True, or windowed mode if False")
        self.m64p.config.set_default(M64TYPE_BOOL, "VerticalSync", False,
                "If true, activate the SDL_GL_SWAP_CONTROL attribute")
        self.m64p.config.list_parameters()

    def set_paths(self):
        path_library = self.qset.value("Paths/Library", find_library(CORE_NAME))
        path_data = self.qset.value("Paths/Data",
                self.m64p.config.get_path("SharedData"))
        path_roms = self.qset.value("Paths/ROM")
        try:
            path_plugins = self.qset.value("Paths/Plugins", os.path.realpath(
                os.path.dirname(self.m64p.plugin_files[0])))
        except IndexError:
            path_plugins = ""

        self.pathLibrary.setText(str(path_library))
        self.pathPlugins.setText(str(path_plugins))
        self.pathData.setText(str(path_data))
        self.pathROM.setText(str(path_roms))

    def set_video(self):
        self.comboResolution.clear()
        for mode in MODES:
            width, height = mode
            self.comboResolution.addItem(
                    "%sx%s" % (width, height), (width, height))
        self.comboResolution.setCurrentIndex(0)
        self.comboResolution.setEnabled(not self.parent.worker.use_vidext)

        self.m64p.config.open_section("Video-General")
        width = self.m64p.config.get_parameter("ScreenWidth")
        height = self.m64p.config.get_parameter("ScreenHeight")
        index = self.comboResolution.findText(
                "%sx%s" % (width, height))
        if index == -1: index = 0
        self.comboResolution.setCurrentIndex(index)

        self.checkFullscreen.setChecked(
                bool(self.m64p.config.get_parameter("Fullscreen")))
        self.checkFullscreen.setEnabled(not self.parent.worker.use_vidext)

        if sys.platform == "win32":
            self.checkKeepAspect.setChecked(False)
            self.checkKeepAspect.setEnabled(False)
        else:
            keep_aspect = bool(int(self.qset.value("keep_aspect", 1)))
            self.checkKeepAspect.setChecked(keep_aspect)

        disable_screensaver = bool(int(self.qset.value("disable_screensaver", 1)))
        self.checkDisableScreenSaver.setChecked(disable_screensaver)

        enable_vidext = bool(int(self.qset.value("enable_vidext", 1)))
        self.checkEnableVidExt.setChecked(enable_vidext)

    def set_core(self):
        self.m64p.config.open_section("Core")
        mode = self.m64p.config.get_parameter("R4300Emulator")
        self.emumode[mode].setChecked(True)
        self.checkOSD.setChecked(
                self.m64p.config.get_parameter("OnScreenDisplay"))
        self.checkOSD.setToolTip(
                self.m64p.config.get_parameter_help("OnScreenDisplay"))
        self.checkNoCompiledJump.setChecked(
                self.m64p.config.get_parameter("NoCompiledJump"))
        self.checkNoCompiledJump.setToolTip(
                self.m64p.config.get_parameter_help("NoCompiledJump"))
        self.checkDisableExtraMem.setChecked(
                self.m64p.config.get_parameter("DisableExtraMem"))
        self.checkDisableExtraMem.setToolTip(
                self.m64p.config.get_parameter_help("DisableExtraMem"))
        self.checkDelaySI.setChecked(
                self.m64p.config.get_parameter("DelaySI"))
        self.checkDelaySI.setToolTip(
                self.m64p.config.get_parameter_help("DelaySI"))
        self.spinCountPerOp.setValue(
                self.m64p.config.get_parameter("CountPerOp"))
        self.spinCountPerOp.setToolTip(
                self.m64p.config.get_parameter_help("CountPerOp"))

    def set_plugins(self):
        plugin_map = self.m64p.plugin_map
        for plugin_type in self.combomap:
            combo,button,settings = self.combomap[plugin_type]
            combo.clear()
            for plugin in plugin_map[plugin_type].values():
                (plugin_handle, plugin_path, plugin_name,
                        plugin_desc, plugin_version) = plugin
                name = os.path.basename(plugin_path)
                combo.addItem(name)
                index = combo.findText(str(name))
                combo.setItemData(index, plugin_desc)
                combo.setItemData(index, plugin_desc, Qt.ToolTipRole)
            current = self.qset.value("Plugins/%s" % (
                PLUGIN_NAME[plugin_type]), PLUGIN_DEFAULT[plugin_type])
            index = combo.findText(current)
            if index == -1: index = 0
            combo.setCurrentIndex(index)
            self.set_section(combo, button, settings)

    def save_paths(self):
        self.qset.setValue("Paths/Library",
                self.pathLibrary.text())
        self.qset.setValue("Paths/Plugins",
                self.pathPlugins.text())
        self.qset.setValue("Paths/Data",
                self.pathData.text())
        self.qset.setValue("Paths/ROM",
                self.pathROM.text())

    def save_video(self):
        self.m64p.config.open_section("Video-General")
        if not self.parent.worker.use_vidext:
            width, height = self.comboResolution.currentText().split("x")
            self.m64p.config.set_parameter("ScreenWidth", int(width))
            self.m64p.config.set_parameter("ScreenHeight", int(height))
        self.m64p.config.set_parameter("Fullscreen", self.checkFullscreen.isChecked())

        self.qset.setValue("keep_aspect", int(self.checkKeepAspect.isChecked()))
        self.qset.setValue("disable_screensaver", int(self.checkDisableScreenSaver.isChecked()))
        self.qset.setValue("enable_vidext", int(self.checkEnableVidExt.isChecked()))

    def save_core(self):
        self.m64p.config.open_section("Core")
        emumode = [n for n,m in enumerate(self.emumode) if m.isChecked()][0]
        self.m64p.config.set_parameter("R4300Emulator",
                emumode)
        self.m64p.config.set_parameter("OnScreenDisplay",
                self.checkOSD.isChecked())
        self.m64p.config.set_parameter("NoCompiledJump",
                self.checkNoCompiledJump.isChecked())
        self.m64p.config.set_parameter("DisableExtraMem",
                self.checkDisableExtraMem.isChecked())
        self.m64p.config.set_parameter("DelaySI",
                self.checkDelaySI.isChecked())
        self.m64p.config.set_parameter("CountPerOp",
                self.spinCountPerOp.value())
        self.m64p.config.set_parameter("SharedDataPath",
                self.pathData.text())

    def save_plugins(self):
        for plugin_type in self.combomap:
            combo,button,settings = self.combomap[plugin_type]
            self.qset.setValue("Plugins/%s" %
                    PLUGIN_NAME[plugin_type],
                    combo.currentText())
