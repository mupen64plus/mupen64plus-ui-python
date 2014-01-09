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
import fnmatch
import ConfigParser

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from m64py.utils import md5sum
from m64py.frontend.log import log
from m64py.archive import Archive, EXT_FILTER
from m64py.ui.romlist_ui import Ui_ROMList

try:
    from m64py.ui import title_rc
    from m64py.ui import snapshot_rc
    bool(title_rc)
    bool(snapshot_rc)
except ImportError:
    pass

class ROMList(QMainWindow, Ui_ROMList):
    """ROM list window"""

    def __init__(self, parent=None):
        """Constructor."""
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.m64p = self.parent.worker.m64p
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.qset = self.parent.settings.qset

        rect = self.frameGeometry()
        rect.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(rect.topLeft())
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

        self.parser = ConfigParser.ConfigParser()
        self.reader = ROMReader(self)
        self.user_data_path = self.m64p.config.get_path("UserData")
        self.shared_data_path = self.m64p.config.get_path("SharedData")

        self.init()
        self.connect_signals()
        self.show()

    def closeEvent(self, event):
        self.reader.stop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def init(self):
        self.read_rom_list()
        self.roms = self.qset.value("rom_list", [])
        if bool(int(self.qset.value("show_available", 0))):
            self.add_available_items(self.roms)
        else:
            self.add_items()

    def connect_signals(self):
        """Connects signals."""
        self.listWidget.currentItemChanged.connect(
                self.on_item_changed)
        self.listWidget.itemDoubleClicked.connect(
                self.on_item_activated)
        self.listWidget.itemActivated.connect(
                self.on_item_activated)
        self.checkAvailable.clicked.connect(
                self.on_available_clicked)
        self.progressBar.valueChanged.connect(
                self.on_progress_bar_changed)
        self.pushRefresh.clicked.connect(
                self.refresh_items)
        self.pushOpen.clicked.connect(
                self.on_item_open)
        self.connect(self.reader, SIGNAL("finished()"),
                self.add_available_items)

    def read_rom_list(self):
        """Reads ROM list from ini file."""
        inifile = os.path.join(self.shared_data_path, "mupen64plus.ini")
        self.parser.read(inifile)
        sections = self.parser.sections()
        self.romlist = {}
        for section in sections:
            items = self.parser.items(section)
            self.romlist[section] = dict(items)

    def add_items(self):
        """Adds ROMs to list"""
        for item in self.romlist.items():
            key, rom = item
            try:
                md5 = rom['refmd5']
            except KeyError:
                md5 = key
            list_item = QListWidgetItem(rom['goodname'])
            list_item.setData(Qt.UserRole, (md5, None, None))
            list_item.setFlags(Qt.ItemIsEnabled)
            self.listWidget.addItem(list_item)
        self.pushOpen.setEnabled(False)
        self.pushRefresh.setEnabled(False)
        self.checkAvailable.setChecked(False)
        self.labelAvailable.setText("")
        self.progressBar.hide()

    def add_available_items(self, roms=None):
        """Adds available ROMs to list"""
        if not roms:
            self.roms = self.reader.get_roms()
            self.qset.setValue("rom_list", self.roms)
            self.qset.sync()
        self.listWidget.clear()
        for md5, path, fname in self.roms:
            if md5 in self.romlist:
                goodname = self.romlist[md5]['goodname']
                list_item = QListWidgetItem(goodname)
                list_item.setData(Qt.UserRole, (md5, path, fname))
                self.listWidget.addItem(list_item)
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.pushOpen.setEnabled(True)
        self.pushRefresh.setEnabled(True)
        self.checkAvailable.setChecked(True)
        self.labelAvailable.setText("%s available ROMs. " % len(self.roms))

    def refresh_items(self):
        """Refreshes available ROMs list"""
        path_roms = str(self.qset.value("Paths/ROM"))
        if not path_roms or path_roms == "None":
            self.parent.emit(SIGNAL(
                "info_dialog(PyQt_PyObject)"),
                self.tr("ROMs directory not found."))
            self.checkAvailable.setChecked(False)
            self.labelAvailable.setText("")
        else:
            self.progressBar.show()
            self.reader.set_path(path_roms)
            self.reader.start()

    def file_open(self, path, fname):
        """Opens ROM file."""
        self.close()
        if self.parent.isMinimized():
            self.parent.activateWindow()
        self.parent.emit(SIGNAL(
            "file_open(PyQt_PyObject, PyQt_PyObject)"), path, fname)

    def on_progress_bar_changed(self, value):
        self.progressBar.setValue(value)

    def on_item_open(self):
        item = self.listWidget.currentItem()
        md5, path, fname = item.data(Qt.UserRole)
        if path:
            self.file_open(path, fname)

    def on_item_activated(self, item):
        md5, path, fname = item.data(Qt.UserRole)
        if path:
            self.file_open(path, fname)

    def on_item_changed(self, current, previous):
        if not current: return
        md5, path, fname = current.data(Qt.UserRole)

        title = QPixmap(os.path.join(
            self.user_data_path, "title", "%s.png") % md5)
        snapshot = QPixmap(os.path.join(
            self.user_data_path, "snapshot", "%s.png") % md5)
        if title.isNull():
            title = QPixmap(":/title/%s.jpg" % md5)
        if snapshot.isNull():
            snapshot = QPixmap(":/snapshot/%s.jpg" % md5)
        if title.isNull():
            title = QPixmap(":/images/default.png")
        if snapshot.isNull():
            snapshot = QPixmap(":/images/default.png")

        if previous is not None:
            self.titleView.scene().removeItem(self.titleItem)
            self.snapshotView.scene().removeItem(self.snapshotItem)

        title_pixmap = title.scaled(self.titleView.size(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        snapshot_pixmap = snapshot.scaled(self.snapshotView.size(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation)

        titleItem = QGraphicsPixmapItem(title_pixmap)
        snapshotItem = QGraphicsPixmapItem(snapshot_pixmap)
        self.titleView.scene().addItem(titleItem)
        self.snapshotView.scene().addItem(snapshotItem)
        self.titleItem = titleItem
        self.snapshotItem = snapshotItem

    def on_available_clicked(self):
        is_checked = self.checkAvailable.isChecked()
        self.qset.setValue("show_available", int(is_checked))
        if is_checked:
            if self.roms:
                self.add_available_items(self.roms)
            else:
                self.refresh_items()
        else:
            self.reader.stop()
            self.add_items()

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

    def read_files(self):
        """Reads files."""
        files = self.get_files()
        num_files = len(files)
        for filenum, filename in enumerate(files):
            fullpath = os.path.join(self.rom_path, filename)
            try:
                archive = Archive(fullpath)
                for fname in archive.namelist:
                    romfile = archive.read(fname)
                    archive.close()
                    rom_md5 = md5sum(filedata=romfile)
                    self.roms.append((rom_md5.upper(), fullpath, fname))
            except Exception, err:
                log.warn(str(err))
                continue
            percent = float(filenum) / float(num_files) * 100
            self.parent.progressBar.emit(
                    SIGNAL("valueChanged(int)"), percent)
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
