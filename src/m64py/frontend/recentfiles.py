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

from PyQt4.QtGui import QAction, QIcon, QPixmap
from PyQt4.QtCore import QFileInfo, QVariant, SIGNAL

class RecentFiles():
    """Keeps track of last opened files."""

    def __init__(self, parent = None):
        """Constructor"""
        self.parent = parent
        self.max_recent = 5
        self.recent_actions = []
        self.recent_files = []
        self.create()
        self.update()

    def create(self):
        """Creates menu actions."""
        for i in range(self.max_recent):
            action = QAction(self.parent)
            action.setIcon(QIcon(QPixmap(":/icons/action_rom.png")))
            self.recent_actions.append(action)
            self.recent_actions[i].setVisible(False)
            self.parent.connect(self.recent_actions[i],
                    SIGNAL("triggered()"), self.parent.file_open)
            self.parent.menuRecent.addAction(self.recent_actions[i])
        self.parent.menuRecent.addSeparator()
        self.actionClearHistory = QAction(self.parent)
        self.actionClearHistory.setText("&Clear history")
        self.actionClearHistory.setEnabled(False)
        self.actionClearHistory.setVisible(True)
        self.actionClearHistory.setIcon(
                QIcon(QPixmap(":/icons/action_clear.png")))
        self.parent.connect(self.actionClearHistory,
                SIGNAL("triggered()"), self.clear)
        self.parent.menuRecent.addAction(self.actionClearHistory)

    def update(self):
        """Updates list of recent files."""
        self.recent_files = self.parent.settings.qset.value(
                "recent_files").toStringList()
        num_files = min(self.recent_files.count(), self.max_recent)
        for i in range(num_files):
            text = QFileInfo(self.recent_files[i]).fileName()
            self.recent_actions[i].setText(text)
            self.recent_actions[i].setData(QVariant(self.recent_files[i]))
            self.recent_actions[i].setVisible(True)
            self.recent_actions[i].setToolTip(QFileInfo(
                self.recent_files[i]).filePath())
        for j in range(num_files, self.max_recent):
            self.recent_actions[j].setVisible(False)
        self.actionClearHistory.setEnabled((num_files > 0))

    def add(self, filepath):
        """Adds file to recent files list."""
        self.recent_files.removeAll(filepath)
        self.recent_files.prepend(filepath)
        while self.recent_files.count() > 5:
            self.recent_files.removeAt(self.recent_files.count() - 1)
        self.parent.settings.qset.setValue(
                "recent_files", QVariant(self.recent_files))
        self.update()

    def clear(self):
        """Clears list of recent files."""
        self.parent.settings.qset.remove("recent_files")
        self.update()
