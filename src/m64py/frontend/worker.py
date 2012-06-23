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
import sys
import shutil

from PyQt4.QtGui import *
from PyQt4.QtCore import *

try:
    from m64py.core.defs import *
    from m64py.utils import log
    from m64py.loader import find_library
    from m64py.core.core import Core
    from m64py.core.vidext import video
    from m64py.archive import Archive
    from m64py.frontend.settings import Settings
except ImportError, err:
    sys.stderr.write("Error: Can't import m64py modules%s%s%s" % (
        os.linesep, str(err), os.linesep))
    sys.exit(1)

class Worker(QThread):
    """Mupen64Plus thread worker"""

    def __init__(self, parent=None):
        """Constructor."""
        QThread.__init__(self, parent)
        self.parent = parent
        self.state = 0
        self.m64p = Core()
        self.video = video
        self.muted = False
        self.settings = Settings(self.parent)
        self.use_vidext = self.settings.qset.value("enable_vidext").toBool()
        self.is_firstrun = self.first_run()
        self.core_load()

    def init(self):
        """Initialize."""
        if self.m64p.get_handle():
            self.plugin_load_try()
            self.settings.m64p = self.m64p
            self.settings.m64p_handle = self.m64p.get_handle()

            if self.is_firstrun:
                self.settings.set_default_general()
                self.settings.qset.setValue("firstrun", False)
                self.parent.emit(SIGNAL("file_open(PyQt_PyObject)"),
                        self.test_rom)
            elif self.parent.args:
                self.parent.emit(SIGNAL("file_open(PyQt_PyObject)"),
                        self.parent.args[0])
        else:
            self.parent.emit(SIGNAL(
                "state_changed(PyQt_PyObject)"),
                (False, False, False, False))
            self.parent.emit(SIGNAL(
                "info_dialog(PyQt_PyObject)"),
                "Mupen64Plus library not found.")

    def first_run(self):
        """Checks if this is first run."""
        firstrun = self.settings.qset.value(
                "firstrun", True).toBool()
        self.test_rom = os.path.realpath(
                os.path.join("test", "mupen64plus.v64"))
        if firstrun and os.path.isfile(self.test_rom) \
                and os.access(self.test_rom, os.R_OK):
            self.use_vidext = True
            return True
        return False

    def set_filepath(self, filepath):
        """Sets rom file path."""
        self.filepath = filepath

    def core_load(self, path=None):
        """Loads core library."""
        if self.m64p.get_handle():
            self.core_shutdown()
        if path is not None:
            path_library = path
        else:
            path_library = self.settings.qset.value(
                    "Paths/Library", find_library(CORE_NAME)).toString()
        self.m64p.core_load(str(path_library), self.use_vidext)

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
                PLUGIN_NAME[plugin_type])).toString()
            plugins[plugin_type] = str(text)
        return plugins

    def plugin_load_try(self, path=None):
        """Loads plugins."""
        if path:
            plugins_path = path
        else:
            plugins_path = self.settings.qset.value(
                    "Paths/Plugins", path).toString()
        self.m64p.plugin_load_try(str(plugins_path))

    def attach_plugins(self):
        """Attaches plugins."""
        self.m64p.attach_plugins(self.get_plugins())

    def rom_open(self):
        """Opens ROM."""
        try:
            self.parent.emit(SIGNAL(
                "file_opening(PyQt_PyObject)"), str(self.filepath))
            archive = Archive(self.filepath)
            romfile = archive.read()
            archive.close()
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

    def core_state_query(self):
        """Query emulator state."""
        self.state = self.m64p.core_state_query()

    def save_screenshot(self):
        """Saves screenshot."""
        self.m64p.take_next_screenshot()

    def get_screenshot(self, screenshots_path):
        """Gets last saved screenshot."""
        rom_name = str(self.m64p.rom_header.Name).replace(
                ' ', '_').lower()
        screenshots = []
        for filename in os.listdir(screenshots_path):
            if filename.startswith(rom_name):
                screenshots.append(os.path.join(
                    screenshots_path, filename))
        if screenshots:
            return sorted(screenshots)[-1]
        return None

    def save_image(self, title=True):
        """Saves snapshot or title image."""
        data_path = self.m64p.config.get_path("UserData")
        if title:
            capture = "title"
            dst_path = os.path.join(data_path, capture)
        else:
            capture = "snapshot"
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
                log.exception("Couldn't save image %s" % image)

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
        self.m64p.config.open_section("CoreEvents")
        keysym = self.m64p.config.get_parameter(
                "Kbd Mapping Reset")
        self.send_sdl_keydown(int(keysym))

    def speed_up(self):
        """Speeds up emulator."""
        self.m64p.config.open_section("CoreEvents")
        keysym = self.m64p.config.get_parameter(
                "Kbd Mapping Speed Up")
        self.send_sdl_keydown(int(keysym))

    def speed_down(self):
        """Speeds down emulator."""
        self.m64p.config.open_section("CoreEvents")
        keysym = self.m64p.config.get_parameter(
                "Kbd Mapping Speed Down")
        self.send_sdl_keydown(int(keysym))

    def add_cheat(self, cheat_name, cheat_code):
        """Adds a cheat"""
        self.m64p.add_cheat(cheat_name, cheat_code)

    def cheat_enabled(self, cheat_name, enabled=True):
        """Toggles cheat state"""
        self.m64p.cheat_enabled(cheat_name, enabled)

    def toggle_fs(self):
        """Toggles fullscreen."""
        self.m64p.config.open_section("CoreEvents")
        keysym = self.m64p.config.get_parameter(
                "Kbd Mapping Fullscreen")
        self.send_sdl_keydown(int(keysym))

    def toggle_pause(self):
        """Toggles pause."""
        if self.state == M64EMU_RUNNING:
            self.m64p.pause()
        elif self.state == M64EMU_PAUSED:
            self.m64p.resume()
        self.toggle_actions()

    def toggle_mute(self):
        """Toggles mute."""
        self.m64p.config.open_section("CoreEvents")
        keysym = self.m64p.config.get_parameter(
                "Kbd Mapping Mute")
        self.send_sdl_keydown(keysym)
        self.muted = not self.muted

    def toggle_actions(self):
        """Toggles actions state."""
        self.core_state_query()
        if self.parent.cheats:
            cheat = bool(self.parent.cheats.cheats)
        else:
            cheat = False
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
