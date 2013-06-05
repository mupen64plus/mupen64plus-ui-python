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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtOpenGL import *

from m64py.core.defs import *
from m64py.frontend.keymap import SDL_KEYMAP

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
        self.connect(self, SIGNAL("toggle_fs()"),
                self.toggle_fs)

    def showEvent(self, event):
        self.qglClearColor(Qt.black)
        self.setFocus(True)

    def resizeEvent(self, event):
        size = event.size()
        self.resize(size.width(), size.height())

    def paintEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        self.toggle_fs()

    def keyPressEvent(self, event):
        if self.worker.state == M64EMU_RUNNING:
            key = event.key()
            modifiers = event.modifiers()
            if modifiers & Qt.AltModifier and \
                    (key == Qt.Key_Enter or key == Qt.Key_Return):
                self.toggle_fs()
            elif key == Qt.Key_F3:
                self.worker.save_title()
            elif key == Qt.Key_F4:
                self.worker.save_snapshot()
            else:
                try:
                    self.worker.send_sdl_keydown(
                            SDL_KEYMAP[key])
                except KeyError:
                    pass

    def keyReleaseEvent(self, event):
        if self.worker.state == M64EMU_RUNNING:
            key = event.key()
            try:
                self.worker.send_sdl_keyup(
                        SDL_KEYMAP[key])
            except KeyError:
                pass

    def toggle_fs(self):
        window = self.window()
        if window.isFullScreen():
            self.parent.menubar.show()
            self.parent.statusbar.show()
            window.setWindowState(Qt.WindowActive)
        else:
            self.parent.menubar.hide()
            self.parent.statusbar.hide()
            window.setWindowState(Qt.WindowFullScreen)
