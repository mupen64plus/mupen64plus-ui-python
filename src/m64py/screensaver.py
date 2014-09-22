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
import ctypes
import subprocess

from m64py.frontend.log import log


class LinuxScreenSaver:
    cookie = None
    screensaver = None

    def __init__(self):
        try:
            import dbus
            self.screensaver = dbus.SessionBus().get_object(
                "org.freedesktop.ScreenSaver", "/ScreenSaver")
        except Exception as err:
            log.info("ScreenSaver not available: %s" % str(err))

    def disable(self):
        if self.screensaver:
            try:
                self.cookie = self.screensaver.Inhibit(
                    "M64Py", "Emulation started")
                log.info("ScreenSaver disabled")
            except Exception as err:
                log.exception(str(err))

    def enable(self):
        if self.cookie:
            try:
                self.screensaver.UnInhibit(self.cookie)
                log.info("ScreenSaver enabled")
                self.cookie = None
            except Exception as err:
                log.exception(str(err))


class DarwinScreenSaver:
    def __init__(self):
        try:
            self.idle_time = subprocess.check_output(
                "defaults -currentHost read com.apple.screensaver idleTime",
                shell=True).strip()
        except subprocess.CalledProcessError:
            self.idle_time = 0

    def disable(self):
        subprocess.call(
            "defaults -currentHost write com.apple.screensaver idleTime 0",
            shell=True)
        log.info("ScreenSaver disabled")

    def enable(self):
        subprocess.call(
            "defaults -currentHost write com.apple.screensaver idleTime %s" % self.idle_time,
            shell=True)
        log.info("ScreenSaver enabled")


class WindowsScreenSaver:
    sys_param_info = None
    SPI_SETSCREENSAVEACTIVE = 17

    def __init__(self):
        try:
            self.sys_param_info = ctypes.windll.user32.SystemParametersInfoA
        except Exception as err:
            log.info("ScreenSaver not available: %s" % str(err))

    def disable(self):
        self.sys_param_info(self.SPI_SETSCREENSAVEACTIVE, False, None, 0)
        log.info("ScreenSaver disabled")

    def enable(self):
        self.sys_param_info(self.SPI_SETSCREENSAVEACTIVE, True, None, 0)
        log.info("ScreenSaver enabled")

screensaver_class = {
    "darwin":   DarwinScreenSaver,
    "cygwin":   WindowsScreenSaver,
    "win32":    WindowsScreenSaver
}

screensaver = screensaver_class.get(sys.platform, LinuxScreenSaver)()
