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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QListWidgetItem, QGraphicsPixmapItem

from m64py.frontend.romreader import ROMReader
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
