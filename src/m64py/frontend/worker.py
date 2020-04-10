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

from PyQt5.QtCore import QThread, QTimer
from sdl2 import SDL_EnableScreenSaver, SDL_DisableScreenSaver

from m64py.utils import sl
from m64py.core.defs import *
from m64py.frontend.log import log
from m64py.loader import find_library, unload_library
from m64py.core.core import Core
from m64py.core.vidext import video
from m64py.archive import Archive
from m64py.platform import DLL_EXT, DEFAULT_DYNLIB, SEARCH_DIRS


class Worker(QThread):
    """Mupen64Plus thread worker"""

    def __init__(self, parent=None):
        """Constructor."""
        QThread.__init__(self, parent)
        self.parent = parent
        self.video = video
        self.plugin_files = []
        self.archive = None
        self.filepath = None
        self.filename = None
        self.library_path = None
        self.state = M64EMU_STOPPED
        self.settings = self.parent.settings
        self.core = Core()

    def init(self, path=None):
        """Initialize."""
        self.core_load(path)
        if self.core.get_handle():
            self.core_startup()
            self.plugins_load()
            self.plugins_startup()

            self.parent.settings.core = self.core
            if self.parent.args:
                self.parent.file_open.emit(self.parent.args[0], None)
        else:
            self.parent.state_changed.emit((False, False, False, False))
            self.parent.info_dialog.emit(self.tr("Mupen64Plus library not found."))

    def quit(self):
        if self.state in [M64EMU_RUNNING, M64EMU_PAUSED]:
            self.stop()
        if self.core.get_handle():
            self.plugins_shutdown()
            self.plugins_unload()
            self.core_shutdown()
            self.core_unload()

    def set_filepath(self, filepath, filename=None):
        """Sets rom file path."""
        self.filepath = filepath
        self.filename = filename
        self.archive = Archive(self.filepath)
        if len(self.archive.namelist) > 1 and not self.filename:
            self.parent.archive_dialog.emit(self.archive.namelist)

    def core_load(self, path=None):
        """Loads core library."""
        if self.core.get_handle():
            self.core_shutdown()
        if path is not None:
            self.library_path = path
        else:
            self.library_path = self.settings.qset.value(
                "Paths/Library", find_library(CORE_NAME))
            if not self.library_path:
                self.library_path = find_library(CORE_NAME)
        self.core.core_load(self.library_path)

    def core_unload(self):
        """Unloads core library."""
        if self.core.get_handle():
            unload_library(self.core.get_handle())
            self.core.m64p = None
            self.core.config = None

    def core_startup(self):
        """Startups core library."""
        if self.core.get_handle():
            self.core.core_startup(
                str(self.library_path), self.parent.vidext)


    def core_shutdown(self):
        """Shutdowns core library."""
        if self.core.get_handle():
            self.core.core_shutdown()

    def find_plugins(self, path=None):
        """Searches for plugins in defined directories."""
        self.plugin_files = []
        path = path if path else self.settings.qset.value("Paths/Plugins", path)
        if path: SEARCH_DIRS.insert(0, path)
        for searchdir in SEARCH_DIRS:
            if os.path.isdir(searchdir):
                for filename in os.listdir(searchdir):
                    if filename.startswith("mupen64plus") and \
                            filename.endswith(DLL_EXT) and filename != DEFAULT_DYNLIB:
                        self.plugin_files.append(os.path.join(searchdir, filename))
                break

    def get_plugins(self):
        """Gets chosen plugins from config."""
        plugins = {}
        for plugin_type in PLUGIN_ORDER:
            text = self.settings.qset.value("Plugins/%s" % (
                PLUGIN_NAME[plugin_type]), PLUGIN_DEFAULT[plugin_type])
            plugins[plugin_type] = text
        return plugins

    def plugins_load(self, path=None):
        """Loads and startup plugins."""
        self.find_plugins(path)
        for plugin_path in self.plugin_files:
            self.core.plugin_load_try(plugin_path)

    def plugins_unload(self):
        """Unloads plugins."""
        for plugin_type in self.core.plugin_map.keys():
            for plugin_map in self.core.plugin_map[plugin_type].values():
                (plugin_handle, plugin_path, plugin_name,
                    plugin_desc, plugin_version) = plugin_map
                unload_library(plugin_handle)
                del plugin_handle

    def plugins_startup(self):
        """Startup plugins."""
        for plugin_type in self.core.plugin_map.keys():
            for plugin_map in self.core.plugin_map[plugin_type].values():
                (plugin_handle, plugin_path, plugin_name,
                    plugin_desc, plugin_version) = plugin_map
                self.core.plugin_startup(plugin_handle, plugin_name, plugin_desc)

    def plugins_shutdown(self):
        """Shutdowns plugins."""
        for plugin_type in self.core.plugin_map.keys():
            for plugin_map in self.core.plugin_map[plugin_type].values():
                (plugin_handle, plugin_path, plugin_name,
                    plugin_desc, plugin_version) = plugin_map
                self.core.plugin_shutdown(plugin_handle, plugin_desc)

    def rom_open(self):
        """Opens ROM."""
        try:
            self.parent.file_opening.emit(self.filepath)
            romfile = self.archive.read(self.filename)
            self.archive.close()
        except Exception:
            log.exception("couldn't open ROM file '%s' for reading." % (
                self.filepath))
            return

        rval = self.core.rom_open(romfile)
        if rval == M64ERR_SUCCESS:
            del romfile
            self.core.rom_get_header()
            self.core.rom_get_settings()
            if bool(self.settings.get_int_safe(
                    "disable_screensaver", 1)):
                SDL_DisableScreenSaver()
            self.parent.rom_opened.emit()
            self.parent.recent_files.add(self.filepath)

    def rom_close(self):
        """Closes ROM."""
        self.core.rom_close()
        if bool(self.settings.get_int_safe(
                "disable_screensaver", 1)):
            SDL_EnableScreenSaver()
        self.parent.rom_closed.emit()

    def core_state_query(self, state):
        """Query emulator state."""
        return self.core.core_state_query(state)

    def core_state_set(self, state, value):
        """Sets emulator state."""
        return self.core.core_state_set(state, value)

    def save_screenshot(self):
        """Saves screenshot."""
        self.core.take_next_screenshot()

    def get_screenshot(self, path):
        """Gets last saved screenshot."""
        name = self.core.rom_header.Name.decode()
        rom_name = name.replace(' ', '_').lower()
        screenshots = []
        for filename in os.listdir(path):
            if filename.startswith(rom_name):
                screenshots.append(os.path.join(
                    path, filename))
        if screenshots:
            return sorted(screenshots)[-1]
        return None

    def save_image(self, title=True):
        """Saves snapshot or title image."""
        data_path = self.core.config.get_path("UserData")
        capture = "title" if title else "snapshot"
        dst_path = os.path.join(data_path, capture)
        if not os.path.isdir(dst_path):
            os.makedirs(dst_path)
        screenshot = self.get_screenshot(
            os.path.join(data_path, "screenshot"))
        if screenshot:
            image_name = "%X%X.png" % (
                sl(self.core.rom_header.CRC1), sl(self.core.rom_header.CRC2))
            try:
                shutil.copyfile(screenshot, os.path.join(dst_path, image_name))
                log.info("Captured %s" % capture)
            except IOError:
                log.exception("couldn't save image %s" % image_name)

    def save_title(self):
        """Saves title."""
        self.save_screenshot()
        QTimer.singleShot(1500, self.save_title_image)

    def save_snapshot(self):
        """Saves snapshot."""
        self.save_screenshot()
        QTimer.singleShot(1500, self.save_snapshot_image)

    def save_title_image(self):
        self.parent.save_image.emit(True)

    def save_snapshot_image(self):
        self.parent.save_image.emit(False)

    def state_load(self, state_path=None):
        """Loads state."""
        self.core.state_load(state_path)

    def state_save(self, state_path=None, state_type=1):
        """Saves state."""
        self.core.state_save(state_path, state_type)

    def state_set_slot(self, slot):
        """Sets save slot."""
        self.core.state_set_slot(slot)

    def send_sdl_keydown(self, key):
        """Sends key down event."""
        self.core.send_sdl_keydown(key)

    def send_sdl_keyup(self, key):
        """Sends key up event."""
        self.core.send_sdl_keyup(key)

    def reset(self, soft=False):
        """Resets emulator."""
        self.core.reset(soft)

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
        self.core.add_cheat(cheat_name, cheat_code)

    def cheat_enabled(self, cheat_name, enabled=True):
        """Toggles cheat state"""
        self.core.cheat_enabled(cheat_name, enabled)

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
            self.core.pause()
            if bool(self.settings.get_int_safe("disable_screensaver", 1)):
                SDL_EnableScreenSaver()
        elif self.state == M64EMU_PAUSED:
            self.core.resume()
            if bool(self.settings.get_int_safe("disable_screensaver", 1)):
                SDL_DisableScreenSaver()
        self.toggle_actions()

    def toggle_mute(self):
        """Toggles mute."""
        if self.core_state_query(M64CORE_AUDIO_MUTE):
            self.core_state_set(M64CORE_AUDIO_MUTE, 0)
        else:
            self.core_state_set(M64CORE_AUDIO_MUTE, 1)

    def toggle_speed_limit(self):
        """Toggles speed limiter."""
        if self.core_state_query(M64CORE_SPEED_LIMITER):
            self.core_state_set(M64CORE_SPEED_LIMITER, 0)
            log.info("Speed limiter disabled")
        else:
            self.core_state_set(M64CORE_SPEED_LIMITER, 1)
            log.info("Speed limiter enabled")

    def toggle_actions(self):
        """Toggles actions state."""
        self.state = self.core_state_query(M64CORE_EMU_STATE)
        cheat = bool(self.parent.cheats.cheats) if self.parent.cheats else False
        if self.state == M64EMU_STOPPED:
            (load, pause, action, cheats) = True, False, False, False
        elif self.state == M64EMU_PAUSED:
            (load, pause, action, cheats) = True, True, True, cheat
        elif self.state == M64EMU_RUNNING:
            (load, pause, action, cheats) = True, True, True, cheat
        self.parent.state_changed.emit((load, pause, action, cheats))

    def stop(self):
        """Stops thread."""
        self.core.stop()
        self.wait()

    def run(self):
        """Starts thread."""
        self.rom_open()
        self.core.attach_plugins(
            self.get_plugins())
        # Save the configuration file again, just in case a plugin has altered it.
        # This is the last opportunity to save changes before the relatively
        # long-running game.
        self.core.config.save_file()
        self.core.execute()
        self.core.detach_plugins()
        self.rom_close()
        self.toggle_actions()
