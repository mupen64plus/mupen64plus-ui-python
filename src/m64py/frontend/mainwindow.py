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
from m64py.frontend.dialogs import *
from m64py.archive import EXT_FILTER
from m64py.ui.mainwindow_ui import Ui_MainWindow
from m64py.frontend.worker import Worker
from m64py.frontend.rominfo import RomInfo
from m64py.frontend.romlist import ROMList
from m64py.frontend.recentfiles import RecentFiles
from m64py.frontend.glwidget import GLWidget
from m64py.frontend.cheat import Cheat

class MainWindow(QMainWindow, Ui_MainWindow):
    """Frontend main window"""

    rom_opened = pyqtSignal()
    rom_closed = pyqtSignal()
    file_open = pyqtSignal(str, str)
    file_opening = pyqtSignal(str)
    set_caption = pyqtSignal(str)
    state_changed = pyqtSignal(tuple)
    save_image = pyqtSignal(bool)
    info_dialog = pyqtSignal(str)
    archive_dialog = pyqtSignal(list)

    def __init__(self, optparse):
        """Constructor"""
        QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.opts, self.args = optparse

        self.statusbarLabel = QLabel()
        self.statusbarLabel.setIndent(2)
        self.statusbar.addPermanentWidget(self.statusbarLabel, 1)
        self.update_status("Welcome to M64Py version %s." % FRONTEND_VERSION)

        self.sizes = {
            SIZE_1X: self.action1X,
            SIZE_2X: self.action2X,
            SIZE_3X: self.action3X}

        self.cheats = None
        self.widgets_height = None
        self.worker = Worker(self)
        self.settings = self.worker.settings

        self.create_state_slots()
        self.create_widgets()
        self.recent_files = RecentFiles(self)
        self.connect_signals()
        self.worker.init()

    def closeEvent(self, event):
        self.settings.qset.sync()
        self.worker.core_shutdown()

    def resizeEvent(self, event):
        event.ignore()
        size = event.size()
        width, height = size.width(), size.height()
        if self.widgets_height:
            width, height = size.width(), size.height() - self.widgets_height
            self.window_size_triggered((width, height))
        else:
            width, height = size.width(), size.height()
            self.resize(width, height)

    def showEvent(self, event):
        if not self.widgets_height:
            width, height = self.settings.qset.value("size", SIZE_1X)
            menubar_height = self.menubar.size().height()
            statusbar_height = self.statusbar.size().height()
            self.widgets_height = menubar_height + statusbar_height
            self.resize(width, height + self.widgets_height)
            self.create_size_actions()
            self.center_widget()

    def window_size_triggered(self, size):
        width, height = size
        fullscreen = self.window().isFullScreen()
        if self.worker.use_vidext and self.worker.m64p.get_handle():
            # event.ignore() doesn't work on windows
            if not sys.platform == "win32":
                if not fullscreen and \
                        bool(int(self.settings.qset.value("keep_aspect", 1))):
                    width, height = self.keep_aspect(size)

            self.worker.m64p.config.open_section("Video-General")
            self.worker.m64p.config.set_parameter("ScreenWidth", width)
            self.worker.m64p.config.set_parameter("ScreenHeight", height)

            if not fullscreen:
                video_size = (width << 16) + height
            else:
                video_size = (width << 16) + (height + self.widgets_height)
            if self.worker.state in (M64EMU_RUNNING, M64EMU_PAUSED):
                self.worker.core_state_set(M64CORE_VIDEO_SIZE, video_size)

        self.set_sizes((width, height))
        self.settings.qset.setValue("size", (width, height))
        self.resize(width, height + self.widgets_height)

    def set_sizes(self, size):
        """Sets 'Window Size' radio buttons on resize event."""
        width, height = size
        if size in self.sizes.keys():
            self.sizes[(width, height)].setChecked(True)
        else:
            for action in self.sizes.values():
                action.setChecked(False)

    def keep_aspect(self, size):
        """Keeps 4:3 aspect ratio."""
        width, height = size
        fixed_ratio = 1.3333333333333333
        current_ratio = float(width)/float(height)
        if fixed_ratio > current_ratio:
            w = int(width)
            h = int(width/fixed_ratio)
        else:
            h = int(height)
            w = int(height*fixed_ratio)
        return w, h

    def center_widget(self):
        """Centers widget on desktop."""
        size = self.size()
        desktop = QApplication.desktop()
        width, height = size.width(), size.height()
        dwidth, dheight = desktop.width(), desktop.height()
        cw, ch = (dwidth/2)-(width/2), (dheight/2)-(height/2)
        self.move(cw, ch)

    def connect_signals(self):
        """Connects signals."""
        self.connect(self, SIGNAL("rom_opened()"),
                self.on_rom_opened)
        self.connect(self, SIGNAL("rom_closed()"),
                self.on_rom_closed)
        self.connect(self, SIGNAL("file_open(PyQt_PyObject, PyQt_PyObject)"),
                self.file_open)
        self.connect(self, SIGNAL("file_opening(PyQt_PyObject)"),
                self.on_file_opening)
        self.connect(self, SIGNAL("set_caption(PyQt_PyObject)"),
                self.on_set_caption)
        self.connect(self, SIGNAL("state_changed(PyQt_PyObject)"),
                self.on_state_changed)
        self.connect(self, SIGNAL("save_image(PyQt_PyObject)"),
                self.on_save_image)
        self.connect(self, SIGNAL("info_dialog(PyQt_PyObject)"),
                self.on_info_dialog)
        self.connect(self, SIGNAL("archive_dialog(PyQt_PyObject)"),
                self.on_archive_dialog)

    def create_widgets(self):
        """Creates central widgets."""
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        self.view = View(self)
        self.stack.addWidget(self.view)
        if self.worker.use_vidext:
            self.glwidget = GLWidget(self)
            self.worker.video.set_widget(self)
            self.stack.addWidget(self.glwidget)
        self.stack.setCurrentWidget(self.view)

    def create_state_slots(self):
        """Creates state slot actions."""
        self.slots = {}
        group = QActionGroup(self)
        group.setExclusive(True)
        for slot in range(10):
            self.slots[slot] = QAction(self)
            self.slots[slot].setCheckable(True)
            self.slots[slot].setText("Slot %d" % slot)
            self.slots[slot].setShortcut(QKeySequence(str(slot)))
            self.slots[slot].setActionGroup(group)
            self.menuStateSlot.addAction(self.slots[slot])
        self.slots[0].setChecked(True)
        for slot, action in self.slots.items():
            self.connect(action, SIGNAL("triggered()"),
                    lambda s=slot:self.worker.state_set_slot(s))

    def create_size_actions(self):
        """Creates window size actions."""
        group = QActionGroup(self)
        group.setExclusive(True)
        size = self.settings.qset.value("size", SIZE_1X)
        for num, size in enumerate(
                sorted(self.sizes.keys()), 1):
            width, height = size
            action = self.sizes[size]
            action.setActionGroup(group)
            w, h = width, height+self.widgets_height
            action.setText("%dX" % num)
            action.setToolTip("%sx%s" % (width, height))
            self.connect(action, SIGNAL("triggered()"),
                    lambda w=w,h=h:self.resize(w, h))

    def file_open(self, filepath=None, filename=None):
        """Opens ROM file."""
        if not filepath:
            action = self.sender()
            filepath = action.data()
        self.worker.core_state_query(M64CORE_EMU_STATE)
        if self.worker.state in [M64EMU_RUNNING, M64EMU_PAUSED]:
            self.worker.stop()
        self.worker.set_filepath(filepath, filename)
        self.worker.start()
        self.raise_()

    def update_status(self, status):
        """Updates label in status bar."""
        self.statusbarLabel.setText(status)

    def on_set_caption(self, title):
        """Sets window title."""
        self.setWindowTitle(title)

    def on_file_opening(self, filepath):
        """Updates status on file opening."""
        self.update_status("Loading %s..." % (
            os.path.basename(filepath)))

    def on_save_image(self, title):
        """Saves snapshot or title image."""
        self.worker.save_image(title)

    def on_info_dialog(self, info):
        """Shows info dialog."""
        self.settings.show_page(0)
        self.settings.raise_()
        InfoDialog(self.settings, info)

    def on_archive_dialog(self, files):
        """Shows archive dialog."""
        archive = ArchiveDialog(self, files)
        rval = archive.exec_()
        if rval == QDialog.Accepted:
            curr_item = archive.listWidget.currentItem()
            fname = curr_item.data(Qt.UserRole)
            self.worker.filename = fname

    def on_state_changed(self, states):
        """Toggles actions state."""
        load,pause,action,cheats = states
        self.menuLoad.setEnabled(load)
        self.menuRecent.setEnabled(load)
        self.menuStateSlot.setEnabled(load)
        self.actionLoadState.setEnabled(action)
        self.actionSaveState.setEnabled(action)
        self.actionLoadFrom.setEnabled(action)
        self.actionSaveAs.setEnabled(action)
        self.actionSaveScreenshot.setEnabled(action)
        self.actionShowROMInfo.setEnabled(action)
        self.actionMute.setEnabled(action)
        self.actionStop.setEnabled(action)
        self.actionReset.setEnabled(action)
        self.actionSoftReset.setEnabled(action)
        self.actionLimitFPS.setEnabled(action)
        self.actionSlowDown.setEnabled(action)
        self.actionSpeedUp.setEnabled(action)
        self.actionFullscreen.setEnabled(action)
        self.actionCheats.setEnabled(cheats)
        self.actionPause.setEnabled(pause)
        self.actionPaths.setEnabled(not action)
        self.actionEmulator.setEnabled(not action)
        self.actionGraphics.setEnabled(not action)
        self.actionPlugins.setEnabled(not action)

    def on_rom_opened(self):
        if self.worker.use_vidext:
            self.stack.setCurrentWidget(self.glwidget)
            self.glwidget.setFocus(True)
        if not self.cheats:
            self.cheats = Cheat(self)
        self.update_status(self.worker.m64p.rom_settings.goodname)
        QTimer.singleShot(2000, self.worker.toggle_actions)

    def on_rom_closed(self):
        if self.worker.use_vidext and self.isFullScreen():
            self.glwidget.emit(SIGNAL("toggle_fs()"))
        self.stack.setCurrentWidget(self.view)
        self.actionMute.setChecked(False)
        self.actionPause.setChecked(False)
        self.actionLimitFPS.setChecked(True)
        self.on_set_caption("M64Py")
        self.update_status("ROM closed.")
        del self.cheats
        self.cheats = None

    @pyqtSignature("")
    def on_actionManually_triggered(self):
        """Shows ROM file dialog."""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        last_dir = self.settings.qset.value("last_dir")
        filepath = dialog.getOpenFileName(
                self, "Load ROM Image", last_dir,
                "Nintendo64 ROM (%s);;All files (*)" % EXT_FILTER)
        if filepath:
            self.emit(SIGNAL("file_open(PyQt_PyObject, PyQt_PyObject)"), filepath, None)
            last_dir = QFileInfo(filepath).path()
            self.settings.qset.setValue("last_dir", last_dir)

    @pyqtSignature("")
    def on_actionFromList_triggered(self):
        """Shows ROM list."""
        ROMList(self)

    @pyqtSignature("")
    def on_actionShowROMInfo_triggered(self):
        """Shows ROM information."""
        RomInfo(self)

    @pyqtSignature("")
    def on_actionLoadState_triggered(self):
        """Loads state."""
        self.worker.state_load()

    @pyqtSignature("")
    def on_actionSaveState_triggered(self):
        """Saves state."""
        self.worker.state_save()

    @pyqtSignature("")
    def on_actionLoadFrom_triggered(self):
        """Loads state from file."""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        file_path = dialog.getOpenFileName(
                self, "Load State From File",
                os.path.join(self.worker.m64p.config.get_path("UserData"), "save"),
                "M64P/PJ64 Saves (*.st* *.zip *.pj);;All files (*)")
        if file_path:
            self.worker.state_load(file_path)

    @pyqtSignature("")
    def on_actionSaveAs_triggered(self):
        """Saves state to file."""
        dialog = QFileDialog()
        file_path, file_filter = dialog.getSaveFileNameAndFilter(
                self, "Save State To File",
                os.path.join(self.worker.m64p.config.get_path("UserData"), "save"),
                ";;".join([save_filter for save_filter, save_ext in M64P_SAVES.values()]),
                M64P_SAVES[M64SAV_M64P][0])
        if file_path:
            for save_type, filters in M64P_SAVES.items():
                save_filter, save_ext = filters
                if file_filter == save_filter:
                    if not file_path.endswith(save_ext):
                        file_path = "%s.%s" % (file_path, save_ext)
                    self.worker.state_save(file_path, save_type)


    @pyqtSignature("")
    def on_actionSaveScreenshot_triggered(self):
        """Saves screenshot."""
        self.worker.save_screenshot()

    @pyqtSignature("")
    def on_actionPause_triggered(self):
        """Toggles pause."""
        self.worker.toggle_pause()

    @pyqtSignature("")
    def on_actionMute_triggered(self):
        """Toggles mute."""
        self.worker.toggle_mute()

    @pyqtSignature("")
    def on_actionStop_triggered(self):
        """Stops emulator."""
        self.worker.stop()

    @pyqtSignature("")
    def on_actionReset_triggered(self):
        """Resets emulator."""
        self.worker.reset()

    @pyqtSignature("")
    def on_actionSoftReset_triggered(self):
        """Resets emulator."""
        self.worker.reset(True)

    @pyqtSignature("")
    def on_actionLimitFPS_triggered(self):
        """Toggles speed limit."""
        self.worker.toggle_speed_limit()

    @pyqtSignature("")
    def on_actionSlowDown_triggered(self):
        """Speeds down emulator."""
        self.worker.speed_down()

    @pyqtSignature("")
    def on_actionSpeedUp_triggered(self):
        """Speeds up emulator."""
        self.worker.speed_up()

    @pyqtSignature("")
    def on_actionCheats_triggered(self):
        """Shows cheat dialog."""
        if self.cheats:
            self.cheats.show()

    @pyqtSignature("")
    def on_actionFullscreen_triggered(self):
        """Toggles fullscreen."""
        self.worker.toggle_fs()

    @pyqtSignature("")
    def on_actionPaths_triggered(self):
        """Shows paths settings."""
        self.settings.show_page(0)

    @pyqtSignature("")
    def on_actionEmulator_triggered(self):
        """Shows emulator settings."""
        self.settings.show_page(1)

    @pyqtSignature("")
    def on_actionGraphics_triggered(self):
        """Shows emulator settings."""
        self.settings.show_page(2)

    @pyqtSignature("")
    def on_actionPlugins_triggered(self):
        """Shows plugins settings."""
        self.settings.show_page(3)

    @pyqtSignature("")
    def on_actionAbout_triggered(self):
        """Shows about dialog."""
        AboutDialog(self)

    @pyqtSignature("")
    def on_actionLicense_triggered(self):
        """Shows license dialog."""
        LicenseDialog(self)

class View(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.parent = parent
        self.setContentsMargins(QMargins())
        self.setStyleSheet("QGraphicsView {border:0px solid;margin:0px;}")
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setScene(QGraphicsScene())
        self.scene().addItem(
                QGraphicsPixmapItem(QPixmap(":/images/front.png")))
