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
import ctypes as C

from m64py.core.defs import *
from m64py.frontend.log import log

SECTIONS_FUNC = C.CFUNCTYPE(None, C.c_void_p, C.c_char_p)
PARAMETERS_FUNC = C.CFUNCTYPE(None, C.c_void_p, C.c_char_p, C.c_int)


class Config:
    """Mupen64Plus configuration"""

    def __init__(self, core):
        """Constructor."""
        self.core = core
        self.m64p = core.get_handle()
        self.config_handle = None
        self.section = None
        self.sections = []
        self.parameters = {}
        self.list_sections()

    def list_sections_callback(self, context, section_name):
        """Callback function for enumerating sections."""
        self.sections.append(section_name)

    def list_parameters_callback(self, context, param_name, param_type):
        """Callback function for enumerating parameters."""
        self.parameters[self.section][param_name] = param_type

    def list_sections(self):
        """Enumerates the list of sections in config file."""
        self.m64p.ConfigListSections.argtypes = [C.c_void_p, C.c_void_p]
        rval = self.m64p.ConfigListSections(
            C.c_void_p(), SECTIONS_FUNC(self.list_sections_callback))
        if rval != M64ERR_SUCCESS:
            log.debug("list_sections()")
            log.warn(self.core.error_message(rval))
        return rval

    def open_section(self, section=None):
        """Gives a configuration section handle to the frontend."""
        try:
            self.section = section
            self.parameters[self.section] = {}
        except ValueError as err:
            log.exception(str(err))
            return
        config_ptr = C.c_void_p()
        self.m64p.ConfigOpenSection.argtypes = [C.c_char_p, C.c_void_p]
        rval = self.m64p.ConfigOpenSection(
            C.c_char_p(section.encode()), C.byref(config_ptr))
        if rval != M64ERR_SUCCESS:
            log.debug("open_section()")
            log.warn(self.core.error_message(rval))
            return rval
        self.config_handle = config_ptr.value
        self.list_parameters()

    def list_parameters(self):
        """Enumerates the list of parameters in a section."""
        self.m64p.ConfigListParameters.argtypes = [
            C.c_void_p, C.c_void_p, C.c_void_p]
        rval = self.m64p.ConfigListParameters(
            self.config_handle, C.c_void_p(),
            PARAMETERS_FUNC(self.list_parameters_callback))
        if rval != M64ERR_SUCCESS:
            log.debug("list_parameters()")
            log.warn(self.core.error_message(rval))
        return rval

    def has_unsaved_changes(self, section):
        rval = self.m64p.ConfigHasUnsavedChanges(C.c_char_p(section.encode()))
        if rval == 0:
            return False
        else:
            return True

    def delete_section(self, section):
        """Deletes a section from the config."""
        rval = self.m64p.ConfigDeleteSection(C.c_char_p(section.encode()))
        if rval != M64ERR_SUCCESS:
            log.debug("delete_section()")
            log.warn(self.core.error_message(rval))
        return rval

    def save_file(self):
        """Saves config file to disk."""
        rval = self.m64p.ConfigSaveFile()
        if rval != M64ERR_SUCCESS:
            log.debug("save_file()")
            log.warn(self.core.error_message(rval))
        return rval

    def save_section(self, section):
        """Saves one section of the current configuration to disk,
        while leaving the other sections unmodified."""
        rval = self.m64p.ConfigSaveSection(C.c_char_p(section.encode()))
        if rval != M64ERR_SUCCESS:
            log.debug("save_section()")
            log.warn(self.core.error_message(rval))
        return rval

    def revert_changes(self, section):
        """Reverts changes previously made to one section of the current
        configuration file, so that it will match with the configuration
        at the last time that it was loaded from or saved to disk. """
        rval = self.m64p.ConfigRevertChanges(C.c_char_p(section.encode()))
        if rval != M64ERR_SUCCESS:
            log.debug("revert_changes()")
            log.warn(self.core.error_message(rval))
        return rval

    def set_parameter(self, param_name, param_value):
        """Sets the value of one of the emulator's parameters."""
        try:
            param_type = self.parameters[self.section][param_name.encode()]
            param_ctype = M64_CTYPE[param_type]
        except KeyError:
            return

        if param_ctype != C.c_char_p:
            param_value = C.byref(param_ctype(param_value))
            param_arg_type = C.POINTER(param_ctype)
        else:
            param_value = param_ctype(param_value)
            param_arg_type = param_ctype

        self.m64p.ConfigSetParameter.argtypes = [
            C.c_void_p, C.c_char_p, C.c_int, param_arg_type]
        rval = self.m64p.ConfigSetParameter(
            self.config_handle, C.c_char_p(param_name.encode()),
            C.c_int(param_type), param_value)
        if rval != M64ERR_SUCCESS:
            log.debug("set_parameter()")
            log.warn(self.core.error_message(rval))
        return rval

    def get_parameter(self, param_name):
        """Retrieves the value of one of the emulator's parameters."""
        try:
            param_type = self.parameters[self.section][param_name.encode()]
            param_ctype = M64_CTYPE[param_type]
        except KeyError:
            return
        if param_ctype != C.c_char_p:
            maxsize = C.sizeof(M64_CTYPE[param_type])
            param_value = C.pointer(param_ctype())
        else:
            maxsize = 256
            param_value = C.create_string_buffer(maxsize)

        self.m64p.ConfigGetParameter.argtypes = [
            C.c_void_p, C.c_char_p, C.c_int, C.c_void_p, C.c_int]
        rval = self.m64p.ConfigGetParameter(
            self.config_handle, C.c_char_p(param_name.encode()),
            C.c_int(param_type), param_value, C.c_int(maxsize))
        if rval != M64ERR_SUCCESS:
            log.debug("get_parameter()")
            log.warn(self.core.error_message(rval))
            return rval
        else:
            if param_ctype == C.c_char_p:
                return param_value.value
            else:
                return param_value.contents.value

    def get_parameter_type(self, param_name):
        """Retrieves the type of one of the emulator's parameters."""
        param_type = C.byref(C.c_int())
        self.m64p.ConfigGetParameterHelp.argtypes = [
            C.c_void_p, C.c_char_p, C.POINTER(C.c_int)]
        rval = self.m64p.ConfigGetParameterType(
            self.config_handle, C.c_char_p(param_name.encode()), param_type)
        if rval != M64ERR_SUCCESS:
            log.debug("get_parameter_type()")
            log.warn(self.core.error_message(rval))
            return rval
        return param_type.value

    def get_parameter_help(self, param_name):
        """Retrieves the help info about one of the emulator's parameters."""
        self.m64p.ConfigGetParameterHelp.restype = C.c_char_p
        self.m64p.ConfigGetParameterHelp.argtypes = [C.c_void_p, C.c_char_p]
        rval = self.m64p.ConfigGetParameterHelp(
            self.config_handle, C.c_char_p(param_name.encode()))
        return rval

    def set_default(self, param_type, param_name, param_value, param_help):
        """Sets the value of a configuration parameter
        if it is not already present in the configuration file."""
        param_ctype = M64_CTYPE[param_type]
        if param_type == M64TYPE_INT:
            rval = self.m64p.ConfigSetDefaultInt(
                self.config_handle, C.c_char_p(param_name.encode()),
                param_ctype(param_value), C.c_char_p(param_help.encode()))
        elif param_type == M64TYPE_FLOAT:
            rval = self.m64p.ConfigSetDefaultFloat(
                self.config_handle, C.c_char_p(param_name.encode()),
                param_ctype(param_value), C.c_char_p(param_help.encode()))
        elif param_type == M64TYPE_BOOL:
            rval = self.m64p.ConfigSetDefaultBool(
                self.config_handle, C.c_char_p(param_name.encode()),
                param_ctype(param_value), C.c_char_p(param_help.encode()))
        elif param_type == M64TYPE_STRING:
            rval = self.m64p.ConfigSetDefaultString(
                self.config_handle, C.c_char_p(param_name.encode()),
                param_ctype(param_value), C.c_char_p(param_help.encode()))
        return rval

    def get_path(self, path="UserConfig"):
        """Retrieves a path to the data, cache or config directory."""
        if path == "SharedData":
            self.m64p.ConfigGetSharedDataFilepath.restype = C.c_char_p
            rval = self.m64p.ConfigGetSharedDataFilepath(
                C.c_char_p("mupen64plus.ini".encode()))
        elif path == "UserConfig":
            self.m64p.ConfigGetUserConfigPath.restype = C.c_char_p
            rval = self.m64p.ConfigGetUserConfigPath()
        elif path == "UserData":
            self.m64p.ConfigGetUserDataPath.restype = C.c_char_p
            rval = self.m64p.ConfigGetUserDataPath()
        elif path == "UserCache":
            self.m64p.ConfigGetUserCachePath.restype = C.c_char_p
            rval = self.m64p.ConfigGetUserCachePath()
        if rval:
            return os.path.dirname(rval.decode())
        else:
            return rval
