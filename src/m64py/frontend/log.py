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

import sys
import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QTextCursor

from m64py.ui.logview_ui import Ui_LogView


class Log:
    def __init__(self, out=None, logview=None):
        self.out = out
        self.logview = logview

    def write(self, msg):
        if self.out:
            self.out.write(msg)
        if self.logview:
            self.logview.msg_written.emit(msg)


class LogView(QDialog, Ui_LogView):
    msg_written = pyqtSignal(str)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.textEdit.setReadOnly(True)
        self.msg_written.connect(self.on_msg_written)

    def on_msg_written(self, msg):
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(msg)


class Logger():
    def __init__(self):
        log_format = 'Frontend: %(levelname)s: %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=log_format)
        self.logger = logging.getLogger('frontend')

logview = LogView()
sys.stderr = Log(sys.stderr, logview)
log = Logger().logger
