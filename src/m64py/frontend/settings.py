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

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QDialog, QFileDialog, QRadioButton, QVBoxLayout

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
        self.core = None
        self.plugins = []
        self.emumode = []
        self.combomap = {}

        self.qset = QSettings("m64py", "m64py")
        self.qset.setDefaultFormat(QSettings.IniFormat)

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
                Input(self.parent))
        }

        self.emumode = [
            QRadioButton(self.tr("Pure Interpreter")),
            QRadioButton(self.tr("Cached Interpreter")),
            QRadioButton(self.tr("Dynamic Recompiler"))
        ]

        vbox = QVBoxLayout(self.groupEmuMode)
        for widget in self.emumode:
            vbox.addWidget(widget)

    def show_page(self, index=0):
        self.tabWidget.setCurrentIndex(index)
        self.show()

    def save_config(self):
        self.save_paths()
        self.save_plugins()
        if self.core and self.core.get_handle():
            self.save_video()
            self.save_core()
            self.core.config.save_file()
        self.qset.sync()

    def set_config(self):
        if self.core and self.core.get_handle():
            self.set_paths()
            self.set_plugins()
            self.set_video()
            self.set_core()

    def on_vidext_changed(self, state):
        self.parent.vidext = state
        self.comboResolution.setEnabled(not self.parent.vidext)
        self.checkFullscreen.setEnabled(not self.parent.vidext)
        self.parent.worker.quit()
        self.parent.worker.init()

    def connect_signals(self):
        self.browseLibrary.clicked.connect(lambda: self.browse_dialog(
            (self.pathLibrary, self.groupLibrary, False)))
        self.browsePlugins.clicked.connect(lambda: self.browse_dialog(
            (self.pathPlugins, self.groupPlugins, True)))
        self.browseData.clicked.connect(lambda: self.browse_dialog(
            (self.pathData, self.groupData, True)))
        self.browseROM.clicked.connect(lambda: self.browse_dialog(
            (self.pathROM, self.groupROM, True)))
        self.checkEnableVidExt.clicked.connect(self.on_vidext_changed)
        for plugin_type in self.combomap:
            self.connect_combo_signals(self.combomap[plugin_type])

    def connect_combo_signals(self, combomap):
        combo, button, settings = combomap
        if settings is not None:
            if combo != self.comboInput:
                combo.activated.connect(
                    lambda: self.set_section(combo, button, settings))
            button.clicked.connect(settings.show_dialog)

    def browse_dialog(self, args):
        widget, groupbox, directory = args
        dialog = QFileDialog()
        if directory:
            dialog.setFileMode(QFileDialog.Directory)
            path = dialog.getExistingDirectory(
                self, groupbox.title(), widget.text(), QFileDialog.ShowDirsOnly)
        else:
            dialog.setFileMode(QFileDialog.ExistingFile)
            path, _ = dialog.getOpenFileName(
                self, groupbox.title(), widget.text(),
                "%s (*%s);;All files (*)" % (groupbox.title(), DLL_FILTER))

        if not path:
            return

        widget.setText(path)
        if widget == self.pathLibrary:
            self.parent.worker.quit()
            if not self.parent.worker.core.get_handle():
                self.parent.worker.init(path)
                if self.parent.worker.core.get_handle():
                    self.core = self.parent.worker.core
                    self.set_core()
                    self.set_video()
                    self.parent.window_size_triggered(self.get_size_safe())
                    self.parent.state_changed.emit((True, False, False, False))
        elif widget == self.pathPlugins:
            self.parent.worker.plugins_shutdown()
            self.parent.worker.plugins_unload()
            self.parent.worker.plugins_load(path)
            self.parent.worker.plugins_startup()
            self.set_plugins()

    def get_int_safe(self, key, default):
        try:
            return int(self.qset.value(key, default))
        except ValueError:
            return default

    def get_size_safe(self):
        try:
            size = self.qset.value("size", SIZE_1X)
        except TypeError:
            size = SIZE_1X
        if not type(size) == tuple:
            size = SIZE_1X
        if len(size) != 2:
            size = SIZE_1X
        if type(size[0]) != int or type(size[1]) != int:
            size = SIZE_1X
        if size[0] <= 0 or size[1] <= 0:
            size = SIZE_1X
        return size

    def get_parameter_help_safe(self, parameter):
        help = self.core.config.get_parameter_help("NoCompiledJump")
        if help is not None:
            return help.decode()
        return ""

    def get_section(self, combo):
        plugin = combo.currentText()
        index = combo.findText(plugin)
        desc = combo.itemData(index)
        name = os.path.splitext(plugin)[0][12:]
        section = "-".join([n.capitalize() for n in name.split("-")[0:2]])
        return section, desc

    def set_section(self, combo, button, settings):
        if settings:
            if combo != self.comboInput:
                section, desc = self.get_section(combo)
                settings.set_section(section, desc)
                self.core.config.open_section(section)
                items = self.core.config.parameters[
                    self.core.config.section].items()
                if items:
                    button.setEnabled(True)
                else:
                    button.setEnabled(False)
            else:
                button.setEnabled(True)
        else:
            button.setEnabled(False)

    def set_paths(self):
        path_library = self.qset.value(
            "Paths/Library", find_library(CORE_NAME))
        path_data = self.qset.value(
            "Paths/Data", self.core.config.get_path("SharedData"))
        path_roms = self.qset.value("Paths/ROM")

        try:
            path_plugins = self.qset.value("Paths/Plugins", os.path.realpath(
                os.path.dirname(self.parent.worker.plugin_files[0])))
        except IndexError:
            path_plugins = ""

        try:
            self.pathROM.setText(path_roms)
        except TypeError:
            pass

        self.pathLibrary.setText(path_library)
        self.pathPlugins.setText(path_plugins)
        self.pathData.setText(path_data)

    def set_video(self):
        self.core.config.open_section("Video-General")

        self.set_resolution()

        self.checkEnableVidExt.setChecked(
            bool(self.get_int_safe("enable_vidext", 1)))

        self.checkFullscreen.setChecked(
            bool(self.core.config.get_parameter("Fullscreen")))
        self.checkFullscreen.setEnabled(not self.parent.vidext)

        self.checkVsync.setChecked(
            bool(self.core.config.get_parameter("VerticalSync")))
        self.checkVsync.setToolTip(
            self.get_parameter_help_safe("VerticalSync"))

        if sys.platform == "win32":
            self.checkKeepAspect.setChecked(False)
            self.checkKeepAspect.setEnabled(False)
        else:
            keep_aspect = bool(self.get_int_safe("keep_aspect", 1))
            self.checkKeepAspect.setChecked(keep_aspect)

        disable_screensaver = bool(self.get_int_safe("disable_screensaver", 1))
        self.checkDisableScreenSaver.setChecked(disable_screensaver)

    def set_core(self):
        self.core.config.open_section("Core")
        mode = self.core.config.get_parameter("R4300Emulator")
        self.emumode[mode].setChecked(True)
        self.checkOSD.setChecked(
            self.core.config.get_parameter("OnScreenDisplay"))
        self.checkOSD.setToolTip(
            self.get_parameter_help_safe("OnScreenDisplay"))
        self.checkNoCompiledJump.setChecked(
            self.core.config.get_parameter("NoCompiledJump"))
        self.checkNoCompiledJump.setToolTip(
            self.get_parameter_help_safe("NoCompiledJump"))
        self.checkDisableExtraMem.setChecked(
            self.core.config.get_parameter("DisableExtraMem"))
        self.checkDisableExtraMem.setToolTip(
            self.get_parameter_help_safe("DisableExtraMem"))

        count_per_op = self.core.config.get_parameter("CountPerOp")
        if count_per_op is not None:
            self.comboCountPerOp.setCurrentIndex(count_per_op)
        else:
            self.comboCountPerOp.setEnabled(False)
        self.comboCountPerOp.setToolTip(
            self.get_parameter_help_safe("CountPerOp"))

    def set_plugins(self):
        plugin_map = self.core.plugin_map
        for plugin_type in self.combomap:
            combo, button, settings = self.combomap[plugin_type]
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
            if index == -1:
                index = 0
            combo.setCurrentIndex(index)
            self.set_section(combo, button, settings)

    def set_resolution(self):
        width = self.core.config.get_parameter("ScreenWidth")
        height = self.core.config.get_parameter("ScreenHeight")
        if (width, height) not in MODES:
            MODES.append((width, height))

        self.comboResolution.clear()
        for mode in MODES:
            w, h = mode
            self.comboResolution.addItem(
                "%sx%s" % (w, h), (w, h))

        index = self.comboResolution.findText(
            "%sx%s" % (width, height), Qt.MatchExactly)
        if index == -1: index = 0
        self.comboResolution.setCurrentIndex(index)
        self.comboResolution.setEnabled(not self.parent.vidext)

    def save_paths(self):
        self.qset.setValue("Paths/Library", self.pathLibrary.text())
        self.qset.setValue("Paths/Plugins", self.pathPlugins.text())
        self.qset.setValue("Paths/Data", self.pathData.text())
        self.qset.setValue("Paths/ROM", self.pathROM.text())

    def save_video(self):
        self.core.config.open_section("Video-General")
        if self.parent.vidext:
            width, height = self.get_size_safe()
        else:
            width, height = self.comboResolution.currentText().split("x")
        self.core.config.set_parameter("ScreenWidth", int(width))
        self.core.config.set_parameter("ScreenHeight", int(height))
        self.core.config.set_parameter("Fullscreen", self.checkFullscreen.isChecked())
        self.core.config.set_parameter("VerticalSync", self.checkVsync.isChecked())
        self.qset.setValue("keep_aspect", int(self.checkKeepAspect.isChecked()))
        self.qset.setValue("disable_screensaver", int(self.checkDisableScreenSaver.isChecked()))
        self.qset.setValue("enable_vidext", int(self.checkEnableVidExt.isChecked()))

    def save_core(self):
        self.core.config.open_section("Core")
        emumode = [n for n,m in enumerate(self.emumode) if m.isChecked()][0]
        self.core.config.set_parameter("R4300Emulator", emumode)
        self.core.config.set_parameter("OnScreenDisplay", self.checkOSD.isChecked())
        self.core.config.set_parameter("NoCompiledJump", self.checkNoCompiledJump.isChecked())
        self.core.config.set_parameter("DisableExtraMem", self.checkDisableExtraMem.isChecked())
        self.core.config.set_parameter("CountPerOp", self.comboCountPerOp.currentIndex())
        self.core.config.set_parameter("SharedDataPath", self.pathData.text().encode())

    def save_plugins(self):
        for plugin_type in self.combomap:
            combo, button, settings = self.combomap[plugin_type]
            self.qset.setValue("Plugins/%s" % PLUGIN_NAME[plugin_type], combo.currentText())
