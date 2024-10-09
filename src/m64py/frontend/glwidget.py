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

from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtOpenGL import QGLWidget


class GLWidget(QGLWidget):

    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_NativeWindow, True)
        self.setContentsMargins(QMargins())
        self.setFocusPolicy(Qt.StrongFocus)

    def showEvent(self, event):
        self.setFocus(True)

    def resizeEvent(self, event):
        size = event.size()
        self.resize(size.width(), size.height())

    def paintEvent(self, event):
        pass
