# -*- coding: utf-8 -*-
# Author: Milan Nikolic <gen2brain@gmail.com>
#
# This is a Python port of Qt SDL joystick wrapper by René Reucher
# <http://www.batcom-it.net/?p=59>
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

from PyQt5.QtCore import QObject, pyqtSignal, QTime, QTimer

from sdl2 import SDL_WasInit, SDL_InitSubSystem, SDL_INIT_JOYSTICK
from sdl2 import SDL_JoystickOpen, SDL_JoystickClose, SDL_NumJoysticks, SDL_JoystickNameForIndex
from sdl2 import SDL_JoystickNumAxes, SDL_JoystickNumButtons, SDL_JoystickNumHats, SDL_JoystickNumBalls
from sdl2 import SDL_JoystickGetAxis, SDL_JoystickGetButton, SDL_JoystickGetHat, SDL_JoystickUpdate, SDL_JoystickInstanceID
from sdl2 import SDL_Event, SDL_PollEvent
from sdl2 import SDL_JOYAXISMOTION, SDL_JOYHATMOTION, SDL_JOYBALLMOTION, SDL_JOYBUTTONDOWN, SDL_JOYBUTTONUP

from m64py.frontend.log import log
import ctypes

JOYSTICK_DEADZONE = 0
JOYSTICK_SENSITIVITY = 0

SDL_JOYSTICK_DEFAULT_EVENT_TIMEOUT = 25
SDL_JOYSTICK_DEFAULT_AUTOREPEAT_DELAY = 250


class Joystick(QObject):

    axis_value_changed = pyqtSignal(int, int)
    button_value_changed = pyqtSignal(int, bool)
    hat_value_changed = pyqtSignal(int, int)
    trackball_value_changed = pyqtSignal(int, int, int)

    def __init__(self, do_auto_repeat=True,
                 repeat_delay=SDL_JOYSTICK_DEFAULT_AUTOREPEAT_DELAY,
                 joystick_event_timeout=SDL_JOYSTICK_DEFAULT_EVENT_TIMEOUT,
                 joystick_deadzone=JOYSTICK_DEADZONE,
                 joystick_sensitivity=JOYSTICK_SENSITIVITY):
        QObject.__init__(self)
        self.joystick_timer = QTimer()

        self.deadzones = {}
        self.sensitivities = {}
        self.axis_repeat_timers = {}
        self.button_repeat_timers = {}
        self.hat_repeat_timers = {}
        self.axes = self.buttons = self.hats = {}
        self.num_axes = self.num_buttons = self.num_hats = self.num_trackballs = 0

        self.joystick = None
        self.auto_repeat = do_auto_repeat
        self.auto_repeat_delay = repeat_delay
        self.event_timeout = joystick_event_timeout
        self.joystick_deadzone = joystick_deadzone
        self.joystick_sensitivity = joystick_sensitivity

        self.joystick_names = []
        self.init()

    def init(self):
        if not SDL_WasInit(SDL_INIT_JOYSTICK):
            if SDL_InitSubSystem(SDL_INIT_JOYSTICK) == 0:
                for i in range(SDL_NumJoysticks()):
                    joystick_name = SDL_JoystickNameForIndex(i)
                    if isinstance(joystick_name, bytes):
                        joystick_name = joystick_name.decode()
                    self.joystick_names.append(joystick_name.strip())

                self.joystick_timer.timeout.connect(self.process_events)
            else:
                log.info("couldn't initialize SDL joystick support")

    def clear_events(self):
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            pass

    def open(self, stick=0):
        if self.joystick:
            self.close()

        try:
            self.joystick = SDL_JoystickOpen(stick)
        except Exception as err:
            log.warn(str(err))

        if self.joystick:
            self.num_axes = SDL_JoystickNumAxes(self.joystick)
            self.num_buttons = SDL_JoystickNumButtons(self.joystick)
            self.num_hats = SDL_JoystickNumHats(self.joystick)
            self.num_trackballs = SDL_JoystickNumBalls(self.joystick)

            for i in range(self.num_axes):
                self.axes[i] = SDL_JoystickGetAxis(self.joystick, i)
                self.axis_repeat_timers[i] = QTime()
                self.deadzones[i] = self.joystick_deadzone
                self.sensitivities[i] = self.joystick_sensitivity

            for i in range(self.num_buttons):
                self.buttons[i] = SDL_JoystickGetButton(self.joystick, i)
                self.button_repeat_timers[i] = QTime()

            for i in range(self.num_hats):
                self.hats[i] = SDL_JoystickGetHat(self.joystick, i)
                self.hat_repeat_timers[i] = QTime()

            self.clear_events()
            self.joystick_timer.start(self.event_timeout)
            return True
        else:
            log.warn("couldn't open SDL joystick #%d", stick)
            return False

    def close(self):
        self.joystick_timer.stop()
        if self.joystick:
            SDL_JoystickClose(self.joystick)
        self.joystick = None
        self.num_axes = self.num_buttons = self.num_hats = self.num_trackballs = 0

    def process_events(self):
        if not self.joystick:
            return

        stickid = SDL_JoystickInstanceID(self.joystick)
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_JOYAXISMOTION:
                if stickid != event.jaxis.which:
                    continue
                moved = event.jaxis.value
                i = event.jaxis.axis
                if abs(moved) >= self.deadzones[i]:
                    if moved != self.axes[i]:
                        delta_moved = abs(self.axes[i] - moved)
                        if delta_moved >= self.sensitivities[i]:
                            self.axis_value_changed.emit(i, moved)
                        self.axes[i] = moved
                        self.axis_repeat_timers[i].restart()
                    elif self.auto_repeat and moved != 0:
                        if self.axis_repeat_timers[i].elapsed() >= self.auto_repeat_delay:
                            self.axis_value_changed.emit(i, moved)
                            self.axes[i] = moved
                    else:
                        self.axis_repeat_timers[i].restart()
                else:
                    self.axis_value_changed.emit(i, 0)

            elif event.type == SDL_JOYHATMOTION:
                if stickid != event.jhat.which:
                    continue
                changed = event.jhat.value
                i = event.jhat.hat
                if changed != self.hats[i]:
                    self.hat_value_changed.emit(i, changed)
                    self.hats[i] = changed
                    self.hat_repeat_timers[i].restart()
                elif self.auto_repeat and changed != 0:
                    if self.hat_repeat_timers[i].elapsed() >= self.auto_repeat_delay:
                        self.hat_value_changed.emit(i, changed)
                        self.hats[i] = changed
                else:
                    self.hat_repeat_timers[i].restart()

            elif event.type == SDL_JOYBALLMOTION:
                if stickid != event.jball.which:
                    continue
                dx = event.jball.xrel
                dy = event.jball.yrel
                i = event.jball.ball
                if dx != 0 or dy != 0:
                    self.trackball_value_changed.emit(i, dx, dy)

            elif event.type == SDL_JOYBUTTONDOWN or event.type == SDL_JOYBUTTONUP:
                if stickid != event.jbutton.which:
                    continue
                changed = event.jbutton.state
                i = event.jbutton.button
                if changed != self.buttons[i]:
                    self.button_value_changed.emit(i, changed)
                    self.buttons[i] = changed
                    self.button_repeat_timers[i].restart()
                elif self.auto_repeat and changed != 0:
                    if self.button_repeat_timers[i].elapsed() >= self.auto_repeat_delay:
                        self.button_value_changed.emit(i, changed)
                        self.button[si] = changed
                else:
                    self.button_repeat_timers[i].restart()
