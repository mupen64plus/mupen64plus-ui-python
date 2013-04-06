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

import os
import shutil

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from m64py.core.defs import *
from m64py.utils import log
from m64py.loader import find_library
from m64py.core.core import Core
from m64py.core.vidext import video
from m64py.archive import Archive
from m64py.frontend.settings import Settings

class Worker(QThread):
    """Mupen64Plus thread worker"""

    def __init__(self, parent=None):
        """Constructor."""
        QThread.__init__(self, parent)
        self.parent = parent
        self.state = M64EMU_STOPPED
        self.m64p = Core()
        self.video = video
        self.settings = Settings(self.parent)
        self.use_vidext = bool(
                self.settings.qset.value("enable_vidext", 1))
        self.core_load()

    def init(self):
        """Initialize."""
        if self.m64p.get_handle():
            self.plugin_load_try()
            self.settings.m64p = self.m64p
            self.settings.m64p_handle = self.m64p.get_handle()

            if self.parent.args:
                self.parent.emit(SIGNAL("file_open(PyQt_PyObject)"),
                        self.parent.args[0])
        else:
            self.parent.emit(SIGNAL("state_changed(PyQt_PyObject)"),
                (False, False, False, False))
            self.parent.emit(SIGNAL("info_dialog(PyQt_PyObject)"),
                "Mupen64Plus library not found.")

    def set_filepath(self, filepath, filename=None):
        """Sets rom file path."""
        self.filepath = filepath
        self.filename = filename
        self.archive = Archive(self.filepath)
        if len(self.archive.namelist) > 1 and not self.filename:
            self.parent.emit(SIGNAL(
                "archive_dialog(PyQt_PyObject)"), self.archive.namelist)

    def core_load(self, path=None):
        """Loads core library."""
        if self.m64p.get_handle():
            self.core_shutdown()
        if path is not None:
            path_library = path
        else:
            path_library = self.settings.qset.value(
                    "Paths/Library", find_library(CORE_NAME))
        self.m64p.core_load(path_library, self.use_vidext)

    def core_shutdown(self):
        """Shutdowns core library."""
        if self.state in [M64EMU_RUNNING, M64EMU_PAUSED]:
            self.stop()
        if self.m64p.get_handle():
            self.m64p.plugins_unload()
            self.m64p.core_shutdown()
        self.wait()
        self.quit()

    def get_plugins(self):
        """Get chosen plugins from config."""
        plugins = {}
        for plugin_type in PLUGIN_ORDER:
            text = self.settings.qset.value("Plugins/%s" % (
                PLUGIN_NAME[plugin_type]))
            plugins[plugin_type] = text
        return plugins

    def plugin_load_try(self, path=None):
        """Loads plugins."""
        if path:
            plugins_path = path
        else:
            plugins_path = self.settings.qset.value(
                    "Paths/Plugins", path)
        self.m64p.plugin_load_try(plugins_path)

    def attach_plugins(self):
        """Attaches plugins."""
        self.m64p.attach_plugins(self.get_plugins())

    def rom_open(self):
        """Opens ROM."""
        try:
            self.parent.emit(SIGNAL(
                "file_opening(PyQt_PyObject)"), self.filepath)
            romfile = self.archive.read(self.filename)
            self.archive.close()
        except Exception:
            log.exception("couldn't open ROM file '%s' for reading." % (
                self.filepath))
            return

        rval = self.m64p.rom_open(romfile)
        if rval == M64ERR_SUCCESS:
            del romfile
            self.m64p.rom_get_header()
            self.m64p.rom_get_settings()
            self.parent.emit(SIGNAL("rom_opened()"))
            self.parent.recent_files.add(self.filepath)

    def rom_close(self):
        """Closes ROM."""
        self.m64p.detach_plugins()
        self.m64p.plugins_shutdown()
        self.m64p.rom_close()
        self.parent.emit(SIGNAL("rom_closed()"))

    def core_state_query(self, state):
        """Query emulator state."""
        return self.m64p.core_state_query(state)

    def core_state_set(self, state, value):
        """Sets emulator state."""
        return self.m64p.core_state_set(state, value)

    def save_screenshot(self):
        """Saves screenshot."""
        self.m64p.take_next_screenshot()

    def get_screenshot(self, path):
        """Gets last saved screenshot."""
        rom_name = str(self.m64p.rom_header.Name).replace(
                ' ', '_').lower()
        screenshots = []
        for filename in os.listdir(path):
            if filename.startswith(rom_name):
                screenshots.append(os.path.join(
                    screenshots_path, filename))
        if screenshots:
            return sorted(screenshots)[-1]
        return None

    def save_image(self, title=True):
        """Saves snapshot or title image."""
        data_path = self.m64p.config.get_path("UserData")
        capture = "title" if title else "snapshot"
        dst_path = os.path.join(data_path, capture)
        if not os.path.isdir(dst_path):
            os.makedirs(dst_path)
        screenshot = self.get_screenshot(
                os.path.join(data_path, "screenshot"))
        if screenshot:
            image_name = "%s.png" % self.m64p.rom_settings.MD5
            try:
                shutil.copyfile(screenshot,
                        os.path.join(dst_path, image_name))
                log.info("Captured %s" % capture)
            except IOError:
                log.exception("couldn't save image %s" % image)

    def save_title(self):
        """Saves title."""
        self.save_screenshot()
        QTimer.singleShot(1500, self.save_title_image)

    def save_snapshot(self):
        """Saves snapshot."""
        self.save_screenshot()
        QTimer.singleShot(1500, self.save_snapshot_image)

    def save_title_image(self):
        self.parent.emit(SIGNAL(
            "save_image(PyQt_PyObject)"), True)

    def save_snapshot_image(self):
        self.parent.emit(SIGNAL(
            "save_image(PyQt_PyObject)"), False)

    def state_load(self):
        """Loads state."""
        self.m64p.state_load()

    def state_save(self):
        """Saves state."""
        self.m64p.state_save()

    def state_set_slot(self, slot):
        """Sets save slot."""
        self.m64p.state_set_slot(slot)

    def send_sdl_keydown(self, key):
        """Sends key down event."""
        self.m64p.send_sdl_keydown(key)

    def send_sdl_keyup(self, key):
        """Sends key up event."""
        self.m64p.send_sdl_keyup(key)

    def reset(self):
        """Resets emulator."""
        self.m64p.reset()

    def speed_up(self):
        """Speeds up emulator."""
        speed = self.core_state_query(M64CORE_SPEED_FACTOR)
        self.core_state_set(M64CORE_SPEED_FACTOR, speed + 5)

    def speed_down(self):
        """Speeds down emulator."""
        speed = self.core_state_query(M64CORE_SPEED_FACTOR)
        self.core_state_set(M64CORE_SPEED_FACTOR, speed - 5)

    def add_cheat(self, cheat_name, cheat_code):
        """Adds a cheat"""
        self.m64p.add_cheat(cheat_name, cheat_code)

    def cheat_enabled(self, cheat_name, enabled=True):
        """Toggles cheat state"""
        self.m64p.cheat_enabled(cheat_name, enabled)

    def toggle_fs(self):
        """Toggles fullscreen."""
        mode = self.core_state_query(M64CORE_VIDEO_MODE)
        if mode == M64VIDEO_WINDOWED:
            self.core_state_set(M64CORE_VIDEO_MODE, M64VIDEO_FULLSCREEN)
        elif mode == M64VIDEO_FULLSCREEN:
            self.core_state_set(M64CORE_VIDEO_MODE, M64VIDEO_WINDOWED)

    def toggle_pause(self):
        """Toggles pause."""
        if self.state == M64EMU_RUNNING:
            self.m64p.pause()
        elif self.state == M64EMU_PAUSED:
            self.m64p.resume()
        self.toggle_actions()

    def toggle_mute(self):
        """Toggles mute."""
        if self.core_state_query(M64CORE_AUDIO_MUTE):
            self.core_state_set(M64CORE_AUDIO_MUTE, 0)
        else:
            self.core_state_set(M64CORE_AUDIO_MUTE, 1)

    def toggle_actions(self):
        """Toggles actions state."""
        self.state = self.core_state_query(M64CORE_EMU_STATE)
        cheat = bool(self.parent.cheats.cheats) if self.parent.cheats else False
        if self.state == M64EMU_STOPPED:
            (load,pause,action,cheats) = True,False,False,False
        elif self.state == M64EMU_PAUSED:
            (load,pause,action,cheats) = True,True,True,cheat
        elif self.state == M64EMU_RUNNING:
            (load,pause,action,cheats) = True,True,True,cheat
        self.parent.emit(SIGNAL(
            "state_changed(PyQt_PyObject)"), (load,pause,action,cheats))

    def stop(self):
        """Stops thread."""
        self.m64p.stop()
        self.wait()

    def run(self):
        """Starts thread."""
        self.rom_open()
        self.attach_plugins()
        self.m64p.execute()
        self.rom_close()
        self.toggle_actions()
