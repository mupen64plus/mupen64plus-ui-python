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

import ctypes as C

CORE_NAME = "mupen64plus"
API_VERSION = 0x20001
FRONTEND_VERSION = "0.1.0"

SIZE_1X = (320, 240)
SIZE_2X = (640, 480)
SIZE_3X = (960, 720)

M64MSG_ERROR = 1
M64MSG_WARNING = 2
M64MSG_INFO = 3
M64MSG_STATUS = 4
M64MSG_VERBOSE = 5

M64ERR_SUCCESS = 0
M64ERR_NOT_INIT = 1
M64ERR_ALREADY_INIT = 2
M64ERR_INCOMPATIBLE = 3
M64ERR_INPUT_ASSERT = 4
M64ERR_INPUT_INVALID = 5
M64ERR_INPUT_NOT_FOUND = 6
M64ERR_NO_MEMORY = 7
M64ERR_FILES = 8
M64ERR_INTERNAL = 9
M64ERR_INVALID_STATE = 10
M64ERR_PLUGIN_FAIL = 11
M64ERR_SYSTEM_FAIL = 12
M64ERR_UNSUPPORTED = 13
M64ERR_WRONG_TYPE = 14

M64CAPS_DYNAREC = 1
M64CAPS_DEBUGGER = 2
M64CAPS_CORE_COMPARE = 4

M64PLUGIN_NULL = 0
M64PLUGIN_RSP = 1
M64PLUGIN_GFX = 2
M64PLUGIN_AUDIO = 3
M64PLUGIN_INPUT = 4
M64PLUGIN_CORE = 5

M64EMU_STOPPED = 1
M64EMU_RUNNING = 2
M64EMU_PAUSED = 3

M64VIDEO_NONE = 1
M64VIDEO_WINDOWED = 2
M64VIDEO_FULLSCREEN = 3

M64CORE_EMU_STATE = 1
M64CORE_VIDEO_MODE = 2
M64CORE_SAVESTATE_SLOT = 3
M64CORE_SPEED_FACTOR = 4
M64CORE_SPEED_LIMITER = 5

M64CMD_NOP = 0
M64CMD_ROM_OPEN = 1
M64CMD_ROM_CLOSE = 2
M64CMD_ROM_GET_HEADER = 3
M64CMD_ROM_GET_SETTINGS = 4
M64CMD_EXECUTE = 5
M64CMD_STOP = 6
M64CMD_PAUSE = 7
M64CMD_RESUME = 8
M64CMD_CORE_STATE_QUERY = 9
M64CMD_STATE_LOAD = 10
M64CMD_STATE_SAVE = 11
M64CMD_STATE_SET_SLOT = 12
M64CMD_SEND_SDL_KEYDOWN = 13
M64CMD_SEND_SDL_KEYUP = 14
M64CMD_SET_FRAME_CALLBACK = 15
M64CMD_TAKE_NEXT_SCREENSHOT = 16
M64CMD_CORE_STATE_SET = 17

M64P_GL_DOUBLEBUFFER = 1
M64P_GL_BUFFER_SIZE = 2
M64P_GL_DEPTH_SIZE = 3
M64P_GL_RED_SIZE = 4
M64P_GL_GREEN_SIZE = 5
M64P_GL_BLUE_SIZE = 6
M64P_GL_ALPHA_SIZE = 7
M64P_GL_SWAP_CONTROL = 8
M64P_GL_MULTISAMPLEBUFFERS = 9
M64P_GL_MULTISAMPLESAMPLES = 10

M64TYPE_INT = 1
M64TYPE_FLOAT = 2
M64TYPE_BOOL = 3
M64TYPE_STRING = 4

M64_CTYPE = {
        M64TYPE_INT: C.c_int,
        M64TYPE_FLOAT: C.c_float,
        M64TYPE_BOOL: C.c_int,
        M64TYPE_STRING: C.c_char_p
        }

PLUGIN_ORDER = [
        M64PLUGIN_GFX,
        M64PLUGIN_AUDIO,
        M64PLUGIN_INPUT,
        M64PLUGIN_RSP
        ]

PLUGIN_NAME = {
        M64PLUGIN_NULL: "NULL",
        M64PLUGIN_RSP: "RSP",
        M64PLUGIN_GFX: "Video",
        M64PLUGIN_AUDIO: "Audio",
        M64PLUGIN_INPUT: "Input"
        }

class m64p_rom_header(C.Structure):
    _fields_ = [
        ('init_PI_BSB_DOM1_LAT_REG', C.c_ubyte),
        ('init_PI_BSB_DOM1_PGS_REG', C.c_ubyte),
        ('init_PI_BSB_DOM1_PWD_REG', C.c_ubyte),
        ('init_PI_BSB_DOM1_PGS_REG2', C.c_ubyte),
        ('ClockRate', C.c_uint),
        ('PC', C.c_uint),
        ('Release', C.c_uint),
        ('CRC1', C.c_uint),
        ('CRC2', C.c_uint),
        ('Unknown', C.c_uint * 2),
        ('Name', C.c_char * 20),
        ('unknown', C.c_uint),
        ('Manufacturer_ID', C.c_uint),
        ('Cartridge_ID', C.c_ushort),
        ('Country_code', C.c_ushort)
        ]

class m64p_rom_settings(C.Structure):
    _fields_ = [
        ('goodname', C.c_char * 256),
        ('MD5', C.c_char * 33),
        ('savetype', C.c_ubyte),
        ('status', C.c_ubyte),
        ('players', C.c_ubyte),
        ('rumble', C.c_ubyte)
        ]

class m64p_cheat_code(C.Structure):
    _fields_ = [
        ('address', C.c_uint),
        ('value', C.c_int),
        ]
