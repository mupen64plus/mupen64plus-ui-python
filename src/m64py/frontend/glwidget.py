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

from PyQt5.QtCore import Qt, pyqtSignal, QMargins
from PyQt5.QtOpenGL import QGLWidget

from m64py.core.defs import *
from m64py.frontend.keymap import QT2SDL2


class GLWidget(QGLWidget):

    toggle_fs = pyqtSignal()

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.parent = parent
        self.worker = parent.worker
        self.setAttribute(Qt.WA_NativeWindow, True)
        self.setContentsMargins(QMargins())
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus(True)
        self.toggle_fs.connect(self.toggle_fullscreen)

    def showEvent(self, event):
        self.setFocus(True)

    def resizeEvent(self, event):
        size = event.size()
        self.resize(size.width(), size.height())

    def paintEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        self.toggle_fs.emit()

    def keyPressEvent(self, event):
        if self.worker.state == M64EMU_RUNNING:
            key = event.key()
            modifiers = event.modifiers()
            if modifiers & Qt.AltModifier and \
                    (key == Qt.Key_Enter or key == Qt.Key_Return):
                self.toggle_fs.emit()
            elif key == Qt.Key_F3:
                self.worker.save_title()
            elif key == Qt.Key_F4:
                self.worker.save_snapshot()
            else:
                try:
                    sdl_key = QT2SDL2[key]
                    self.worker.send_sdl_keydown(sdl_key)
                except KeyError:
                    pass

    def keyReleaseEvent(self, event):
        if self.worker.state == M64EMU_RUNNING:
            key = event.key()
            try:
                sdl_key = QT2SDL2[key]
                self.worker.send_sdl_keyup(sdl_key)
            except KeyError:
                pass

    def toggle_fullscreen(self):
        window = self.window()
        if window.isFullScreen():
            self.parent.menubar.show()
            self.parent.statusbar.show()
        else:
            self.parent.menubar.hide()
            self.parent.statusbar.hide()
        window.setWindowState(window.windowState() ^ Qt.WindowFullScreen)
