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

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

from sdl2.keyboard import SDL_GetScancodeName

from m64py.frontend.keymap import QT2SDL2

SDL_HAT_UP = 0x01
SDL_HAT_RIGHT = 0x02
SDL_HAT_DOWN = 0x04
SDL_HAT_LEFT = 0x08

class InputButton(QPushButton):

    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.key = None
        self.parent = parent
        self.input = None
        self.joystick = None
        self.setFocusPolicy(Qt.ClickFocus)

    def showEvent(self, event):
        dialog = self.parent.parentWidget().parent()
        if hasattr(dialog, 'joystick'):
            self.input = dialog
            self.joystick = dialog.joystick
        else:
            self.input = dialog.parent()
            self.joystick = dialog.parent().joystick
        self.connect_signals()


    def connect_signals(self):
        self.joystick.axis_value_changed.connect(self.on_axis_value_changed)
        self.joystick.button_value_changed.connect(self.on_button_value_changed)
        self.joystick.hat_value_changed.connect(self.on_hat_value_changed)

    def keyPressEvent(self, event):
        modifier = event.modifiers()
        if modifier == Qt.NoModifier or modifier == Qt.KeypadModifier:
            key = event.key()
        else:
            key = modifier.__int__()

        if key == Qt.Key_Escape:
            text = self.key
            self.setCheckable(False)
        elif key == Qt.Key_Backspace:
            text = self.tr("Select...")
            self.setCheckable(False)
        else:
            text = SDL_GetScancodeName(QT2SDL2[key])
            text = text.decode()

        text = text.replace("Left ", "")
        self.setText(text.title())
        self.clearFocus()

    def focusInEvent(self, event):
        self.key = self.text()
        if self.input.is_joystick:
            self.joystick.init()
            self.joystick.open(self.input.device)
        self.setText(self.tr("Press Key"))
        self.setCheckable(True)
        self.window().statusLabel.setText(
            self.tr("Press <em>Escape</em> to cancel, <em>Backspace</em> to delete."))

    def focusOutEvent(self, event):
        if self.input.is_joystick:
            self.joystick.close()
        self.setCheckable(False)
        self.window().statusLabel.setText("")

    def on_joystick_event(self, event, key, value):
        if self.hasFocus():
            if event == "hat":
                self.setText("hat(%s %s)" % (key, value))
            elif event == "axis":
                self.setText("axis(%s%s)" % (key, value))
            elif event == "button":
                self.setText("button(%s)" % key)
            self.clearFocus()

    def on_axis_value_changed(self, axis, value):
        val = "-" if value < 0 else "+"
        self.on_joystick_event("axis", axis, val)

    def on_button_value_changed(self, button, value):
        if value:
            self.on_joystick_event("button", button, value)

    def on_hat_value_changed(self, hat, value):
        if value == SDL_HAT_UP:
            val = "Up"
        elif value == SDL_HAT_RIGHT:
            val = "Right"
        elif value == SDL_HAT_DOWN:
            val = "Down"
        elif value == SDL_HAT_LEFT:
            val = "Left"
        else:
            return
        self.on_joystick_event("hat", hat, val)
