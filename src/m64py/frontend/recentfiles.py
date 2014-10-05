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

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QFileInfo


class RecentFiles():
    """Keeps track of last opened files."""

    def __init__(self, parent = None):
        """Constructor"""
        self.parent = parent
        self.max_recent = 5
        self.recent_files = []
        self.recent_actions = []
        self.action_clear_history = QAction(self.parent)
        self.create()
        self.update()

    def create(self):
        """Creates menu actions."""
        for i in range(self.max_recent):
            action = QAction(self.parent)
            action.setIcon(QIcon(QPixmap(":/icons/action_rom.png")))
            self.recent_actions.append(action)
            self.recent_actions[i].setVisible(False)
            self.recent_actions[i].triggered.connect(self.parent.on_file_open)
            self.parent.menuRecent.addAction(self.recent_actions[i])
        self.parent.menuRecent.addSeparator()
        self.action_clear_history.setText("&Clear history")
        self.action_clear_history.setEnabled(False)
        self.action_clear_history.setVisible(True)
        self.action_clear_history.setIcon(
            QIcon(QPixmap(":/icons/action_clear.png")))
        self.action_clear_history.triggered.connect(self.clear)
        self.parent.menuRecent.addAction(self.action_clear_history)

    def is_string(self, obj):
        try:
            return isinstance(obj, basestring)
        except NameError:
            return isinstance(obj, str)

    def update(self):
        """Updates list of recent files."""
        self.recent_files = self.parent.settings.qset.value("recent_files", [])
        if not type(self.recent_files) == list:
            self.recent_files = []
        self.recent_files = list(filter(lambda x: self.is_string(x), self.recent_files))
        num_files = min(len(self.recent_files), self.max_recent)
        for i in range(num_files):
            text = QFileInfo(self.recent_files[i]).fileName()
            self.recent_actions[i].setText(text)
            self.recent_actions[i].setData(self.recent_files[i])
            self.recent_actions[i].setVisible(True)
            self.recent_actions[i].setToolTip(QFileInfo(
                self.recent_files[i]).filePath())
        for j in range(num_files, self.max_recent):
            self.recent_actions[j].setVisible(False)
        self.action_clear_history.setEnabled((num_files > 0))

    def add(self, filepath):
        """Adds file to recent files list."""
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        while len(self.recent_files) > 5:
            self.recent_files.pop(len(self.recent_files) - 1)
        self.parent.settings.qset.setValue(
            "recent_files", self.recent_files)
        self.update()

    def clear(self):
        """Clears list of recent files."""
        self.parent.settings.qset.remove("recent_files")
        self.update()
