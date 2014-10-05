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

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QRectF

class ImageView(QGraphicsView):

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setScene(QGraphicsScene())

    def resizeEvent(self, event):
        size = event.size()
        for item in self.scene().items():
            pixmap = item.pixmap()
            pixmap = pixmap.scaled(
                size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            item.setPixmap(pixmap)
            self.ensureVisible(item)
            self.centerOn(item)
            self.set_scene_rect()

    def set_scene_rect(self):
        rect = self.scene().itemsBoundingRect()
        if rect.isNull():
            self.scene().setSceneRect(QRectF(0, 0, 1, 1))
        else:
            self.scene().setSceneRect(rect)
