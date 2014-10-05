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
import ctypes
import fnmatch

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from m64py.utils import sl
from m64py.core.defs import m64p_rom_header
from m64py.frontend.log import log
from m64py.archive import Archive, EXT_FILTER
from m64py.ui.romlist_ui import Ui_ROMList

try:
    from m64py.ui import title_rc
    from m64py.ui import snapshot_rc
except ImportError:
    pass


class ROMList(QMainWindow, Ui_ROMList):
    """ROM list window"""

    def __init__(self, parent=None):
        """Constructor."""
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.parent = parent
        self.core = self.parent.worker.core
        self.qset = self.parent.settings.qset

        self.title_item = None
        self.snapshot_item = None

        rect = self.frameGeometry()
        rect.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(rect.topLeft())
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

        self.reader = ROMReader(self)

        try:
            self.rom_list = self.qset.value("rom_list", [])
        except TypeError:
            self.rom_list = []

        self.user_data_path = self.core.config.get_path("UserData")

        if self.rom_list:
            self.add_items()
        else:
            self.read_items()

        self.connect_signals()
        self.show()

    def closeEvent(self, event):
        self.reader.stop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def connect_signals(self):
        """Connects signals."""
        self.listWidget.currentItemChanged.connect(self.on_item_changed)
        self.listWidget.itemDoubleClicked.connect(self.on_item_activated)
        self.listWidget.itemActivated.connect(self.on_item_activated)
        self.progressBar.valueChanged.connect(self.on_progress_bar_changed)
        self.pushRefresh.clicked.connect(self.read_items)
        self.pushOpen.clicked.connect(self.on_item_open)
        self.reader.finished.connect(self.on_finished)

    def add_items(self):
        """Adds available ROMs"""
        self.listWidget.clear()
        for rom in self.rom_list:
            if len(rom) == 4:
                crc, goodname, path, fname = rom
                if isinstance(goodname, bytes):
                    goodname = goodname.decode()
                list_item = QListWidgetItem(goodname)
                list_item.setData(Qt.UserRole, (crc, goodname, path, fname))
                self.listWidget.addItem(list_item)
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.pushOpen.setEnabled(True)
        self.pushRefresh.setEnabled(True)
        self.labelAvailable.setText("%s ROMs. " % len(self.rom_list))

    def read_items(self):
        """Read available ROMs"""
        path_roms = str(self.qset.value("Paths/ROM"))
        if not path_roms or path_roms == "None":
            self.parent.info_dialog.emit(self.tr("ROMs directory not found."))
            self.labelAvailable.setText("")
            self.progressBar.hide()
            self.pushOpen.setEnabled(False)
            self.pushRefresh.setEnabled(True)
        else:
            self.progressBar.show()
            self.reader.set_path(path_roms)
            self.reader.start()

    def file_open(self, path, fname):
        """Opens ROM file."""
        self.close()
        if self.parent.isMinimized():
            self.parent.activateWindow()
        self.parent.file_open.emit(path, fname)

    def on_finished(self):
        self.rom_list = self.reader.get_roms()
        self.qset.setValue("rom_list", self.rom_list)
        self.add_items()
        self.listWidget.setCurrentRow(0)

    def on_progress_bar_changed(self, value):
        self.progressBar.setValue(value)

    def on_item_open(self):
        item = self.listWidget.currentItem()
        crc, goodname, path, fname = item.data(Qt.UserRole)
        if path:
            self.file_open(path, fname)

    def on_item_activated(self, item):
        crc, goodname, path, fname = item.data(Qt.UserRole)
        if path:
            self.file_open(path, fname)

    def on_item_changed(self, current, previous):
        if not current:
            return
        crc, goodname, path, fname = current.data(Qt.UserRole)

        title = QPixmap(os.path.join(
            self.user_data_path, "title", "%s.png") % crc)
        snapshot = QPixmap(os.path.join(
            self.user_data_path, "snapshot", "%s.png") % crc)

        if title.isNull():
            title = QPixmap(":/title/%s.jpg" % crc)
        if snapshot.isNull():
            snapshot = QPixmap(":/snapshot/%s.jpg" % crc)

        if title.isNull():
            title = QPixmap(":/images/default.png")
        if snapshot.isNull():
            snapshot = QPixmap(":/images/default.png")

        if previous is not None:
            self.titleView.scene().removeItem(self.title_item)
            self.snapshotView.scene().removeItem(self.snapshot_item)

        title_pixmap = title.scaled(
            self.titleView.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        snapshot_pixmap = snapshot.scaled(
            self.snapshotView.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        title_item = QGraphicsPixmapItem(title_pixmap)
        snapshot_item = QGraphicsPixmapItem(snapshot_pixmap)
        self.titleView.scene().addItem(title_item)
        self.snapshotView.scene().addItem(snapshot_item)
        self.title_item = title_item
        self.snapshot_item = snapshot_item


class ROMReader(QThread):
    """ROM reader thread"""

    def __init__(self, parent):
        """Constructor."""
        QThread.__init__(self, parent)
        self.parent = parent
        self.roms = []
        self.rom_path = None

    def set_path(self, path):
        """Sets ROM directory path."""
        self.rom_path = path

    def get_roms(self):
        """Returns ROM list."""
        return self.roms

    def get_files(self):
        """Returns list of files found in path."""
        files = []
        types = EXT_FILTER.split()
        for filename in os.listdir(self.rom_path):
            for ext in types:
                if fnmatch.fnmatch(filename, ext):
                    files.append(filename)
        return files

    def get_rom_crc(self, archive, fname):
        rom_header = m64p_rom_header()
        ctypes.memmove(
            ctypes.byref(rom_header),
            archive.read(fname, ctypes.sizeof(rom_header)),
            ctypes.sizeof(rom_header))
        crc1_pre = sl(rom_header.CRC1)
        crc2_pre = sl(rom_header.CRC2)

        regs = 0
        regs |= rom_header.init_PI_BSB_DOM1_LAT_REG << 24
        regs |= rom_header.init_PI_BSB_DOM1_PGS_REG << 16
        regs |= rom_header.init_PI_BSB_DOM1_PWD_REG << 8
        regs |= rom_header.init_PI_BSB_DOM1_PGS_REG2

        if regs == 0x80371240:
            # native *.z64
            crc1 = crc1_pre
            crc2 = crc2_pre
        elif regs == 0x37804012:
            # byteswapped [BADC] *.v64
            crc1 = 0
            crc1 |= ((crc1_pre >> 0) & 0xff) << 8
            crc1 |= ((crc1_pre >> 8) & 0xff) << 0
            crc1 |= ((crc1_pre >> 16) & 0xff) << 24
            crc1 |= ((crc1_pre >> 24) & 0xff) << 16
            crc2 = 0
            crc2 |= ((crc2_pre >> 0) & 0xff) << 8
            crc2 |= ((crc2_pre >> 8) & 0xff) << 0
            crc2 |= ((crc2_pre >> 16) & 0xff) << 24
            crc2 |= ((crc2_pre >> 24) & 0xff) << 16
        elif regs == 0x40123780:
            # wordswapped [DCBA] *.n64
            crc1 = 0
            crc1 |= ((crc1_pre >> 0) & 0xff) << 24
            crc1 |= ((crc1_pre >> 8) & 0xff) << 16
            crc1 |= ((crc1_pre >> 16) & 0xff) << 8
            crc1 |= ((crc1_pre >> 24) & 0xff) << 0
            crc2 = 0
            crc2 |= ((crc2_pre >> 0) & 0xff) << 24
            crc2 |= ((crc2_pre >> 8) & 0xff) << 16
            crc2 |= ((crc2_pre >> 16) & 0xff) << 8
            crc2 |= ((crc2_pre >> 24) & 0xff) << 0
        else:
            return None
        return (crc1, crc2)

    def read_files(self):
        """Reads files."""
        self.roms = []
        files = self.get_files()
        num_files = len(files)
        for filenum, filename in enumerate(files):
            fullpath = os.path.join(self.rom_path, filename)
            try:
                archive = Archive(fullpath)
                for fname in archive.namelist:
                    crc_tuple = self.get_rom_crc(archive, fname)
                    if crc_tuple:
                        rom_settings = self.parent.core.get_rom_settings(
                            crc_tuple[0], crc_tuple[1])
                        if rom_settings:
                            crc = "%X%X" % (crc_tuple[0], crc_tuple[1])
                            self.roms.append((crc, rom_settings.goodname, fullpath, fname))
                archive.close()
            except Exception as err:
                log.warn(str(err))
                continue
            percent = float(filenum) / float(num_files) * 100
            self.parent.progressBar.valueChanged.emit(percent)
        self.exit()

    def stop(self):
        """Stops thread."""
        if self.isRunning():
            self.terminate()
            self.wait()

    def run(self):
        """Starts thread."""
        self.read_files()
        self.exec_()
