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
import signal
import ctypes as C
import subprocess
import binascii

from m64py.core.defs import *
from m64py.core.config import Config
from m64py.loader import load, unload_library
from m64py.frontend.log import log
from m64py.utils import version_split
from m64py.opts import VERBOSE
from m64py.archive import ROM_TYPE
from m64py.core.vidext import vidext

def debug_callback(context, level, message):
    if level <= M64MSG_ERROR:
        sys.stderr.write("%s: %s\n" % (context.decode(), message.decode()))
    elif level == M64MSG_WARNING:
        sys.stderr.write("%s: %s\n" % (context.decode(), message.decode()))
    elif level == M64MSG_INFO or level == M64MSG_STATUS:
        sys.stderr.write("%s: %s\n" % (context.decode(), message.decode()))
    elif level == M64MSG_VERBOSE and VERBOSE:
        sys.stderr.write("%s: %s\n" % (context.decode(), message.decode()))


def state_callback(context, param, value):
    if param == M64CORE_VIDEO_SIZE:
        pass
    elif param == M64CORE_VIDEO_MODE:
        pass

DEBUGFUNC = C.CFUNCTYPE(None, C.c_char_p, C.c_int, C.c_char_p)
STATEFUNC = C.CFUNCTYPE(None, C.c_char_p, C.c_int, C.c_int)

DEBUG_CALLBACK = DEBUGFUNC(debug_callback)
STATE_CALLBACK = STATEFUNC(state_callback)


class Core:
    """Mupen64Plus Core library"""

    plugin_map = {
        M64PLUGIN_RSP: {},
        M64PLUGIN_GFX: {},
        M64PLUGIN_AUDIO: {},
        M64PLUGIN_INPUT: {}
    }

    def __init__(self):
        """Constructor."""
        self.m64p = None
        self.config = None
        self.plugins = {}
        self.rom_type = None
        self.rom_length = None
        self.rom_header = m64p_rom_header()
        self.rom_settings = m64p_rom_settings()
        self.core_path = ""
        self.core_name = "Mupen64Plus Core"
        self.core_version = "Unknown"

    def get_handle(self):
        """Retrieves core library handle."""
        return self.m64p

    def core_load(self, path=None):
        """Loads core library."""
        try:
            if path:
                self.m64p = load(path)
                self.core_path = path
                self.check_version()
            else:
                raise Exception("'%s' library not found." % self.core_name)
        except Exception as err:
            self.m64p = None
            log.exception(str(err))

    def check_version(self):
        """Checks core API version."""
        version = self.plugin_get_version(self.m64p, self.core_path)
        if version:
            plugin_type, plugin_version, plugin_api, plugin_name, plugin_cap = version
            if plugin_type != M64PLUGIN_CORE:
                raise Exception(
                    "library '%s' is invalid, "
                    "this is not the emulator core." % (
                        os.path.basename(self.core_path)))
            elif plugin_version < MINIMUM_CORE_VERSION:
                raise Exception(
                    "library '%s' is incompatible, "
                    "core version %s is below minimum supported %s." % (
                        os.path.basename(self.core_path),
                        version_split(plugin_version),
                        version_split(MINIMUM_CORE_VERSION)))
            elif plugin_api & 0xffff0000 != CORE_API_VERSION & 0xffff0000:
                raise Exception(
                    "library '%s' is incompatible, "
                    "core API major version %s doesn't match application (%s)." % (
                        os.path.basename(self.core_path),
                        version_split(plugin_version),
                        version_split(CORE_API_VERSION)))
            else:
                config_ver, debug_ver, vidext_ver = self.get_api_versions()
                if config_ver & 0xffff0000 != CONFIG_API_VERSION & 0xffff0000:
                    raise Exception(
                        "emulator core '%s' is incompatible, "
                        "config API major version %s doesn't match application: (%s)" % (
                        os.path.basename(self.core_path),
                        version_split(config_ver),
                        version_split(CONFIG_API_VERSION)))

                self.core_name = plugin_name
                self.core_version = plugin_version

                log.info("attached to library '%s' version %s" %
                        (self.core_name, version_split(self.core_version)))
                if plugin_cap & M64CAPS_DYNAREC:
                    log.info("includes support for Dynamic Recompiler.")
                if plugin_cap & M64CAPS_DEBUGGER:
                    log.info("includes support for MIPS r4300 Debugger.")
                if plugin_cap & M64CAPS_CORE_COMPARE:
                    log.info("includes support for r4300 Core Comparison.")

    def error_message(self, return_code):
        """Returns description of the error"""
        self.m64p.CoreErrorMessage.restype = C.c_char_p
        rval = self.m64p.CoreErrorMessage(return_code).decode()
        return rval

    def core_startup(self, path, use_vidext):
        """Initializes libmupen64plus for use by allocating memory,
        creating data structures, and loading the configuration file."""
        rval = self.m64p.CoreStartup(
            C.c_int(CORE_API_VERSION), None, C.c_char_p(os.path.dirname(path).encode()),
            C.c_char_p(b"Core"), DEBUG_CALLBACK, C.c_char_p(b"State"), STATE_CALLBACK)
        if rval == M64ERR_SUCCESS:
            if use_vidext:
                self.override_vidext()
            self.config = Config(self)
        else:
            log.debug("core_startup()")
            log.warn("error starting '%s' library" % self.core_name)

    def core_shutdown(self):
        """Saves the config file, then destroys
        data structures and releases allocated memory."""
        if self.m64p:
            self.m64p.CoreShutdown()
        return M64ERR_SUCCESS

    def plugin_get_version(self, handle, path):
        """Retrieves version information from the plugin."""
        try:
            type_ptr = C.pointer(C.c_int())
            ver_ptr = C.pointer(C.c_int())
            api_ptr = C.pointer(C.c_int())
            name_ptr = C.pointer(C.c_char_p())
            cap_ptr = C.pointer(C.c_int())
            rval = handle.PluginGetVersion(
                type_ptr, ver_ptr, api_ptr, name_ptr, cap_ptr)
        except AttributeError:
            unload_library(handle)
            log.warn("library '%s' is invalid, no PluginGetVersion() function found." % (
                os.path.basename(path)))
        except OSError as err:
            log.debug("plugin_get_version()")
            log.warn(str(err))
        else:
            if rval == M64ERR_SUCCESS:
                return (type_ptr.contents.value, ver_ptr.contents.value, api_ptr.contents.value,
                        name_ptr.contents.value.decode(), cap_ptr.contents.value)
            else:
                log.debug("plugin_get_version()")
                log.warn(self.error_message(rval))
        return None

    def get_api_versions(self):
        """Retrieves API version information from the core library."""
        config_ver_ptr = C.pointer(C.c_int())
        debug_ver_ptr = C.pointer(C.c_int())
        vidext_ver_ptr = C.pointer(C.c_int())
        rval = self.m64p.CoreGetAPIVersions(
            config_ver_ptr, debug_ver_ptr, vidext_ver_ptr, None)
        if rval == M64ERR_SUCCESS:
            return (config_ver_ptr.contents.value, debug_ver_ptr.contents.value,
                    vidext_ver_ptr.contents.value)
        else:
            log.debug("get_api_versions()")
            log.warn(self.error_message(rval))
            return None

    def plugin_load_try(self, plugin_path=None):
        """Loads plugins and maps them by plugin type."""
        try:
            plugin_handle = C.cdll.LoadLibrary(plugin_path)
            version = self.plugin_get_version(plugin_handle, plugin_path)
            if version:
                plugin_type, plugin_version, plugin_api, plugin_desc, plugin_cap = version
                plugin_name = os.path.basename(plugin_path)
                self.plugin_map[plugin_type][plugin_name] = (
                    plugin_handle, plugin_path, PLUGIN_NAME[plugin_type], plugin_desc, plugin_version)
        except OSError as e:
            log.debug("plugin_load_try()")
            plugin_path = plugin_path.encode('ascii').decode('ascii', 'ignore')
            log.error("failed to load plugin %s: %s" % (plugin_path, e))

    def plugin_startup(self, handle, name, desc):
        """This function initializes plugin for use by allocating memory,
        creating data structures, and loading the configuration data."""
        rval = handle.PluginStartup(C.c_void_p(self.m64p._handle),
                                    name, DEBUG_CALLBACK)
        if rval != M64ERR_SUCCESS:
            log.debug("plugin_startup()")
            log.warn(self.error_message(rval))
            log.warn("%s failed to start." % desc)

    def plugin_shutdown(self, handle, desc):
        """This function destroys data structures and releases
        memory allocated by the plugin library. """
        rval = handle.PluginShutdown()
        if rval != M64ERR_SUCCESS:
            log.debug("plugin_shutdown()")
            log.warn(self.error_message(rval))
            log.warn("%s failed to stop." % desc)

    def attach_plugins(self, plugins):
        """Attaches plugins to the emulator core."""
        self.plugins = plugins
        for plugin_type in PLUGIN_ORDER:
            plugin = self.plugins[plugin_type]

            if not plugin:
                plugin_map = list(self.plugin_map[plugin_type].values())[0]
            else:
                try:
                    plugin_map = self.plugin_map[plugin_type][plugin]
                except KeyError:
                    continue

            (plugin_handle, plugin_path, plugin_name,
             plugin_desc, plugin_version) = plugin_map

            rval = self.m64p.CoreAttachPlugin(
                C.c_int(plugin_type), C.c_void_p(plugin_handle._handle))
            if rval != M64ERR_SUCCESS:
                log.debug("attach_plugins()")
                log.warn(self.error_message(rval))
                log.warn("core failed to attach %s plugin." % (
                    plugin_name))
            else:
                log.info("using %s plugin: '%s' v%s" % (
                    plugin_name.decode(), plugin_desc, version_split(plugin_version)))

    def detach_plugins(self):
        """Detaches plugins from the emulator core,
        and re-attaches the 'dummy' plugin functions."""
        for plugin_type in PLUGIN_ORDER:
            plugin = self.plugins[plugin_type]

            if not plugin:
                plugin_map = list(self.plugin_map[plugin_type].values())[0]
            else:
                try:
                    plugin_map = self.plugin_map[plugin_type][plugin]
                except KeyError:
                    continue

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
        self.rom_type = ROM_TYPE[binascii.hexlify(romfile[:4])]
        romlength = C.c_int(self.rom_length)
        rombuffer = C.c_buffer(romfile)
        rval = self.m64p.CoreDoCommand(
            M64CMD_ROM_OPEN, romlength, C.byref(rombuffer))
        if rval != M64ERR_SUCCESS:
            log.debug("rom_open()")
            log.warn(self.error_message(rval))
            log.error("core failed to open ROM file.")
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

    def core_state_query(self, state):
        """Query the emulator core for the
        value of a state parameter."""
        state_ptr = C.pointer(C.c_int())
        rval = self.m64p.CoreDoCommand(
            M64CMD_CORE_STATE_QUERY, C.c_int(state), state_ptr)
        if rval != M64ERR_SUCCESS:
            log.debug("core_state_query()")
            log.warn(self.error_message(rval))
        return state_ptr.contents.value

    def core_state_set(self, state, value):
        """Sets the value of a state
        parameter in the emulator core."""
        value_ptr = C.pointer(C.c_int(value))
        rval = self.m64p.CoreDoCommand(
            M64CMD_CORE_STATE_SET, C.c_int(state), value_ptr)
        if rval != M64ERR_SUCCESS:
            log.debug("core_state_set()")
            log.warn(self.error_message(rval))
        return value_ptr.contents.value

    def state_load(self, state_path=None):
        """Loads a saved state file from the current slot."""
        path = C.c_char_p(state_path.encode()) if state_path else None
        rval = self.m64p.CoreDoCommand(
            M64CMD_STATE_LOAD, C.c_int(1), path)
        if rval != M64ERR_SUCCESS:
            log.debug("state_load()")
            log.warn(self.error_message(rval))
        return rval

    def state_save(self, state_path=None, state_type=1):
        """Saves a state file to the current slot."""
        path = C.c_char_p(state_path.encode()) if state_path else None
        rval = self.m64p.CoreDoCommand(
            M64CMD_STATE_SAVE, C.c_int(state_type), path)
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

    def reset(self, soft=False):
        """Reset the emulated machine."""
        rval = self.m64p.CoreDoCommand(
            M64CMD_RESET, C.c_int(int(soft)))
        if rval != M64ERR_SUCCESS:
            log.debug("reset()")
            log.warn(self.error_message(rval))
        return rval

    def advance_frame(self):
        """Advance one frame. The emulator will run
        until the next frame, then pause."""
        rval = self.m64p.CoreDoCommand(
            M64CMD_ADVANCE_FRAME, C.c_int(), C.c_int())
        if rval != M64ERR_SUCCESS:
            log.debug("advance_frame()")
            log.warn(self.error_message(rval))
        return rval

    def get_rom_settings(self, crc1, crc2):
        """Searches through the data in the ini file for given crc hashes,
        if found, fills in the RomSettings structure with the data."""
        rom_settings = m64p_rom_settings()
        rval = self.m64p.CoreGetRomSettings(
            C.byref(rom_settings),
            C.c_int(C.sizeof(rom_settings)),
            C.c_int(crc1), C.c_int(crc2))
        if rval != M64ERR_SUCCESS:
            return None
        return rom_settings

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
        rval = self.m64p.CoreAddCheat(
            C.c_char_p(cheat_name.encode()), C.pointer(cheat_code),
            C.c_int(C.sizeof(cheat_code)))
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
            C.c_char_p(cheat_name.encode()), C.c_int(enabled))
        if rval != M64ERR_SUCCESS:
            log.debug("cheat_enabled()")
            log.info("CoreCheatEnabled() failed for cheat code '%s'" % cheat_name)
            log.warn(self.error_message(rval))
        else:
            state = 'activated' if enabled else 'deactivated'
            log.info("cheat code '%s' %s" % (cheat_name, state))
        return rval
