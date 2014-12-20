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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem

from m64py.utils import version_split
from m64py.core.defs import FRONTEND_VERSION
from m64py.ui.about_ui import Ui_AboutDialog
from m64py.ui.license_ui import Ui_LicenseDialog
from m64py.ui.archive_ui import Ui_ArchiveDialog


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        if parent.worker.core.core_version != "Unknown":
            version = version_split(parent.worker.core.core_version)
        else:
            version = "Unknown"
        text = self.labelAbout.text()
        text = text.replace("FRONTEND_VERSION", FRONTEND_VERSION)
        text = text.replace("CORE_VERSION", version)
        self.labelAbout.setText(text)
        self.show()


class LicenseDialog(QDialog, Ui_LicenseDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.show()


class InfoDialog(QMessageBox):
    def __init__(self, parent=None, text=None):
        QMessageBox.__init__(self, parent)
        self.setText(text)
        self.setWindowTitle("Info")
        self.show()


class ArchiveDialog(QDialog, Ui_ArchiveDialog):
    def __init__(self, parent, files):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.build_list(files)

    def build_list(self, files):
        self.listWidget.clear()
        for fname in files:
            item = QListWidgetItem(fname)
            item.setData(Qt.UserRole, fname)
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(0)
