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
import ctypes as C

try:
    from m64py.core.defs import *
    from m64py.core.config import Config
    from m64py.loader import load, unload_library
    from m64py.utils import log, version_split
    from m64py.archive import ROM_TYPE
    from m64py.platform import DLL_EXT, DEFAULT_DYNLIB, SEARCH_DIRS
    from m64py.core.vidext import vidext
except ImportError, err:
    sys.stderr.write("Error: Can't import m64py modules%s%s%s" % (
        os.linesep, str(err), os.linesep))
    sys.exit(1)

def py_debug_callback(context, level, message):
    if level <= 1:
        sys.stderr.write("%s: %s\n" % (context, message))
    elif level == 2:
        sys.stderr.write("%s: %s\n" % (context, message))
    elif level == 3 or level == 4:
        sys.stderr.write("%s: %s\n" % (context, message))
    elif level > 4:
        pass

DEBUGFUNC = C.CFUNCTYPE(None, C.c_char_p, C.c_int, C.c_char_p)
DEBUG_CALLBACK = DEBUGFUNC(py_debug_callback)

class Core:
    """Mupen64Plus Core library"""

    def __init__(self):
        """Constructor."""
        self.m64p = None
        self.config = None
        self.plugins = {}
        self.plugin_map = {}
        self.plugin_files = []
        self.rom_type = None
        self.rom_length = None
        self.rom_header = m64p_rom_header()
        self.rom_settings = m64p_rom_settings()
        self.core_name = "Mupen64Plus Core"
        self.core_version = "Unknown"

    def core_load(self, path=None, vidext=False):
        """Loads core library."""
        try:
            if path is not None:
                self.m64p = load(path)
            else:
                self.m64p = None
                raise IOError("'%s' library not found." % self.core_name)

            rval = self.m64p.CoreStartup(C.c_int(API_VERSION), None,
                    C.c_char_p(os.path.dirname(path)),
                    "Core", DEBUG_CALLBACK, None, None)
            if rval != M64ERR_SUCCESS:
                log.debug("core_load()")
                log.warn("error starting '%s' library" % self.core_name)
                self.core_shutdown()
                unload_library(self.m64p)
                del self.m64p
                sys.exit(1)

            ver_ptr = C.pointer(C.c_int())
            name_ptr = C.pointer(C.c_char_p())
            rval = self.m64p.PluginGetVersion(None, ver_ptr, None, name_ptr, None)
            if rval == M64ERR_SUCCESS:
                self.config = Config(self)
                self.core_name = name_ptr.contents.value
                self.core_version = version_split(ver_ptr.contents.value)
                log.info("attached to library '%s' version %s" %
                        (self.core_name, self.core_version))
                if vidext:
                    self.override_vidext()
            else:
                self.m64p = None
                log.debug("core_load()")
                log.warn(self.error_message(rval))
        except Exception, err:
            self.m64p = None
            log.exception(str(err))

    def get_handle(self):
        """Retrieves core library handle."""
        return self.m64p

    def error_message(self, return_code):
        """Returns description of the error"""
        self.m64p.CoreErrorMessage.restype = C.c_char_p
        rval = self.m64p.CoreErrorMessage(return_code)
        return rval

    def find_plugins(self, path=None):
        """Searches for plugins in defined directories."""
        self.plugin_files = []
        if path: SEARCH_DIRS.insert(0, path)
        for searchdir in SEARCH_DIRS:
            if os.path.isdir(searchdir):
                for filename in os.listdir(searchdir):
                    if filename.startswith("mupen64plus") and \
                            filename.endswith(DLL_EXT) and filename != DEFAULT_DYNLIB:
                        self.plugin_files.append(os.path.join(searchdir, filename))
                break

    def plugin_load_try(self, path=None):
        """Loads plugins and maps them by plugin type."""
        self.find_plugins(path)
        self.plugin_map = {
                M64PLUGIN_RSP: {},
                M64PLUGIN_GFX: {},
                M64PLUGIN_AUDIO: {},
                M64PLUGIN_INPUT: {}
                }
        for plugin_path in self.plugin_files:
            try:
                plugin_handle = C.cdll.LoadLibrary(plugin_path)
                type_ptr = C.pointer(C.c_int())
                ver_ptr = C.pointer(C.c_int())
                api_ptr = C.pointer(C.c_int())
                name_ptr = C.pointer(C.c_char_p())
                rval = plugin_handle.PluginGetVersion(
                        type_ptr, ver_ptr, api_ptr, name_ptr, None)
                if rval != M64ERR_SUCCESS:
                    log.debug("plugin_load_try()")
                    log.warn(self.error_message(rval))
                    continue
            except AttributeError:
                unload_library(plugin_handle)
                continue
            except OSError, err:
                log.debug("plugin_load_try()")
                log.warn(str(err))
                continue
            else:
                plugin_type = type_ptr.contents.value
                plugin_version = version_split(ver_ptr.contents.value)
                plugin_desc = name_ptr.contents.value
                plugin_name = os.path.basename(plugin_path)
                self.plugin_map[plugin_type][plugin_name] = (plugin_handle, plugin_path,
                        PLUGIN_NAME[plugin_type], plugin_desc, plugin_version)

    def core_shutdown(self):
        """Saves the config file, then destroys
        data structures and releases allocated memory."""
        if self.m64p:
            self.m64p.CoreShutdown()
            unload_library(self.m64p)
            del self.m64p
            self.m64p = None
        return M64ERR_SUCCESS

    def plugins_shutdown(self):
        """Destroys data structures and releases allocated memory."""
        for plugin_type in PLUGIN_ORDER:
            plugin = self.plugins[plugin_type]
            if not plugin:
                plugin_map = self.plugin_map[plugin_type].values()[0]
            else:
                plugin_map = self.plugin_map[plugin_type][plugin]
            (plugin_handle, plugin_path, plugin_name,
                    plugin_desc, plugin_version) = plugin_map

            rval = plugin_handle.PluginShutdown()
            if rval != M64ERR_SUCCESS:
                log.debug("plugins_shutdown()")
                log.warn(self.error_message(rval))

    def plugins_unload(self):
        """Unloads plugins from plugin_map."""
        if self.plugin_map:
            for plugin_type in self.plugin_map.keys():
                for plugin_map in self.plugin_map[plugin_type].values():
                    (plugin_handle, plugin_path, plugin_name,
                            plugin_desc, plugin_version) = plugin_map
                    unload_library(plugin_handle)
                    del plugin_handle

    def attach_plugins(self, plugins={}):
        """Attaches plugins to the emulator core."""
        self.plugins = plugins
        for plugin_type in PLUGIN_ORDER:
            plugin = self.plugins[plugin_type]
            if not plugin:
                plugin_map = self.plugin_map[plugin_type].values()[0]
            else:
                plugin_map = self.plugin_map[plugin_type][plugin]
            (plugin_handle, plugin_path, plugin_name,
                    plugin_desc, plugin_version) = plugin_map

            rval = plugin_handle.PluginStartup(
                    C.c_void_p(self.m64p._handle),
                    plugin_name,
                    DEBUG_CALLBACK)
            if rval != M64ERR_SUCCESS:
                log.debug("attach_plugins()")
                log.warn(self.error_message(rval))
                log.warn("%s plugin library '%s' failed to start." % (
                    plugin_name, plugin_path))

            rval = self.m64p.CoreAttachPlugin(
                    C.c_int(plugin_type),
                    C.c_void_p(plugin_handle._handle))
            if rval != M64ERR_SUCCESS:
                log.debug("attach_plugins()")
                log.warn(self.error_message(rval))
                log.warn("core failed to attach %s plugin." % (
                    plugin_name))
            else:
                log.info("using %s plugin: '%s' v%s" % (
                    plugin_name, plugin_desc, plugin_version))

    def detach_plugins(self):
        """Detaches plugins from the emulator core,
        and re-attaches the 'dummy' plugin functions."""
        for plugin_type in PLUGIN_ORDER:
            plugin = self.plugins[plugin_type]
            if not plugin:
                plugin_map = self.plugin_map[plugin_type].values()[0]
            else:
                plugin_map = self.plugin_map[plugin_type][plugin]
            (plugin_handle, plugin_path, plugin_name,
                    plugin_desc, plugin_version) = plugin_map

            rval = self.m64p.CoreDetachPlugin(plugin_type)
            if rval != M64ERR_SUCCESS:
                log.debug("detach_plugins()")
                log.warn(self.error_message(rval))
                log.warn("core failed to dettach %s plugin." % (
                    plugin_name))

    def rom_open(self, romfile):
        """Reads in a binary ROM image"""
        self.rom_length = len(romfile)
        self.rom_type = ROM_TYPE[romfile[:4].encode('hex')]
        romlength = C.c_int(self.rom_length)
        rombuffer = C.c_buffer(romfile)
        rval = self.m64p.CoreDoCommand(
                M64CMD_ROM_OPEN, romlength, C.byref(rombuffer))
        if rval != M64ERR_SUCCESS:
            log.debug("rom_open()")
            log.warn(self.error_message(rval))
            log.error("core failed to open ROM file '%s'." % (
                filename))
        del rombuffer
        return rval

    def rom_close(self):
        """Closes any currently open ROM."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_ROM_CLOSE)
        if rval != M64ERR_SUCCESS:
            log.debug("rom_close()")
            log.warn(self.error_message(rval))
            log.error("core failed to close ROM image file.")
        return rval

    def rom_get_header(self):
        """Retrieves the header data of the currently open ROM."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_ROM_GET_HEADER,
                C.c_int(C.sizeof(self.rom_header)),
                C.pointer(self.rom_header))
        if rval != M64ERR_SUCCESS:
            log.debug("rom_get_header()")
            log.warn("core failed to get ROM header.")
        return rval

    def rom_get_settings(self):
        """Retrieves the settings data of the currently open ROM."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_ROM_GET_SETTINGS,
                C.c_int(C.sizeof(self.rom_settings)),
                C.pointer(self.rom_settings))
        if rval != M64ERR_SUCCESS:
            log.debug("rom_get_settings()")
            log.warn("core failed to get ROM settings.")
        return rval

    def execute(self):
        """Starts the emulator and begin executing the ROM image."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_EXECUTE, 0, None)
        if rval != M64ERR_SUCCESS:
            log.warn(self.error_message(rval))
        return rval

    def stop(self):
        """Stops the emulator, if it is currently running."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_STOP, 0, None)
        if rval != M64ERR_SUCCESS:
            log.debug("stop()")
            log.warn(self.error_message(rval))
        return rval

    def pause(self):
        """Pause the emulator if it is running."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_PAUSE, 0, None)
        if rval != M64ERR_SUCCESS:
            log.debug("pause()")
            log.warn(self.error_message(rval))
        return rval

    def resume(self):
        """Resumes execution of the emulator if it is paused."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_RESUME, 0, None)
        if rval != M64ERR_SUCCESS:
            log.debug("resume()")
            log.warn(self.error_message(rval))
        return rval

    def core_state_query(self):
        """Query the emulator core for the
        value of a state parameter."""
        state_ptr = C.pointer(C.c_int())
        rval = self.m64p.CoreDoCommand(
                M64CMD_CORE_STATE_QUERY,
                C.c_int(M64CORE_EMU_STATE), state_ptr)
        if rval != M64ERR_SUCCESS:
            log.debug("core_state_query()")
            log.warn(self.error_message(rval))
        return state_ptr.contents.value

    def state_load(self):
        """Loads a saved state file from the current slot."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_STATE_LOAD, C.c_int(1), None)
        if rval != M64ERR_SUCCESS:
            log.debug("state_load()")
            log.warn(self.error_message(rval))
        return rval

    def state_save(self):
        """Saves a state file to the current slot."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_STATE_SAVE, C.c_int(1), None)
        if rval != M64ERR_SUCCESS:
            log.debug("state_save()")
            log.warn(self.error_message(rval))
        return rval

    def state_set_slot(self, slot):
        """Sets the currently selected save slot index."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_STATE_SET_SLOT, C.c_int(slot))
        if rval != M64ERR_SUCCESS:
            log.debug("state_set_slot()")
            log.warn(self.error_message(rval))
        return rval

    def send_sdl_keydown(self, key):
        """Injects an SDL_KEYDOWN event into
        the emulator's core event loop."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_SEND_SDL_KEYDOWN, C.c_int(key))
        if rval != M64ERR_SUCCESS:
            log.debug("send_sdl_keydown()")
            log.warn(self.error_message(rval))
        return rval

    def send_sdl_keyup(self, key):
        """Injects an SDL_KEYUP event into
        the emulator's core event loop."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_SEND_SDL_KEYUP, C.c_int(key))
        if rval != M64ERR_SUCCESS:
            log.debug("send_sdl_keyup()")
            log.warn(self.error_message(rval))
        return rval

    def take_next_screenshot(self):
        """Saves a screenshot at the next possible opportunity."""
        rval = self.m64p.CoreDoCommand(
                M64CMD_TAKE_NEXT_SCREENSHOT)
        if rval != M64ERR_SUCCESS:
            log.debug("take_next_screenshot()")
            log.warn(self.error_message(rval))
        return rval

    def override_vidext(self):
        """Overrides the core's internal SDL-based OpenGL functions."""
        rval = self.m64p.CoreOverrideVidExt(C.pointer(vidext))
        if rval != M64ERR_SUCCESS:
            log.debug("override_vidext()")
            log.warn(self.error_message(rval))
        else:
            log.info("video extension enabled")
        return rval

    def add_cheat(self, cheat_name, cheat_code):
        """Adds a Cheat Function to a list of currently active cheats
        which are applied to the open ROM, and set its state to Enabled"""
        rval = self.m64p.CoreAddCheat(C.c_char_p(cheat_name),
                C.pointer(cheat_code), C.c_int(C.sizeof(cheat_code)))
        if rval != M64ERR_SUCCESS:
            log.debug("add_cheat()")
            log.info("CoreAddCheat() failed for cheat code '%s'" % cheat_name)
            log.warn(self.error_message(rval))
        else:
            log.info("cheat code '%s' activated" % cheat_name)
        return rval

    def cheat_enabled(self, cheat_name, enabled=True):
        """Enables or disables a specified Cheat Function"""
        rval = self.m64p.CoreCheatEnabled(
                C.c_char_p(cheat_name), C.c_int(enabled))
        if rval != M64ERR_SUCCESS:
            log.debug("cheat_enabled()")
            log.info("CoreCheatEnabled() failed for cheat code '%s'" % cheat_name)
            log.warn(self.error_message(rval))
        else:
            state = 'activated' if enabled else 'deactivated'
            log.info("cheat code '%s' %s" % (cheat_name, state))
        return rval
