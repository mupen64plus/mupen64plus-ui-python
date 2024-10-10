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
from PyQt5.QtGui import QWindow, QOpenGLContext

from m64py.core.defs import *
from m64py.frontend.keymap import QT2SDL2


class GLWidget(QWindow):

    def __init__(self, parent=None):
        self.parent = parent
        QWindow.__init__(self, None)

        self.setSurfaceType(QWindow.OpenGLSurface)
        self.ctx = QOpenGLContext()

    def context(self):
        return self.ctx

    def resizeEvent(self, event):
        size = event.size()
        width, height = int(size.width() * self.devicePixelRatio()), int(size.height() * self.devicePixelRatio())
        self.resize(width, height)

    def mouseDoubleClickEvent(self, event):
        self.parent.toggle_fs.emit()

    def keyPressEvent(self, event):
        if self.parent.worker.state != M64EMU_RUNNING:
            return

        key = event.key()
        modifiers = event.modifiers()

        if modifiers & Qt.AltModifier and (key == Qt.Key_Enter or key == Qt.Key_Return):
            self.parent.toggle_fs.emit()
        elif key == Qt.Key_F3:
            self.parent.worker.save_title()
        elif key == Qt.Key_F4:
            self.parent.worker.save_snapshot()
        else:
            try:
                sdl_key = QT2SDL2[key]
                self.parent.worker.send_sdl_keydown(sdl_key)
            except KeyError:
                pass

    def keyReleaseEvent(self, event):
        if self.parent.worker.state != M64EMU_RUNNING:
            return

        key = event.key()
        try:
            sdl_key = QT2SDL2[key]
            self.parent.worker.send_sdl_keyup(sdl_key)
        except KeyError:
            pass
