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

if sys.platform.startswith("linux"):
    DLL_EXT = ".so"
    DLL_FILTER = ".so.2"
    DEFAULT_DYNLIB = "libmupen64plus.so.2"
    SEARCH_DIRS = [
        "/usr/local/lib/mupen64plus",
        "/usr/lib64/mupen64plus",
        "/usr/lib/mupen64plus",
        "/usr/games/lib64/mupen64plus",
        "/usr/games/lib/mupen64plus",
        "/usr/lib/x86_64-linux-gnu/mupen64plus",
        "/usr/lib/i386-linux-gnu/mupen64plus",
        "."
    ]
elif sys.platform.startswith("openbsd"):
    DLL_EXT = ".so"
    DLL_FILTER = ""
    DEFAULT_DYNLIB = "libmupen64plus.so"
    SEARCH_DIRS = [
        "/usr/local/lib/mupen64plus",
        "."
    ]
elif sys.platform == "darwin":
    DLL_EXT = ".dylib"
    DLL_FILTER = ".dylib"
    DEFAULT_DYNLIB = "libmupen64plus.dylib"
    SEARCH_DIRS = [
        "/usr/local/lib/mupen64plus",
        "/usr/lib/mupen64plus",
        "."
    ]
elif sys.platform == "win32":
    DLL_EXT = ".dll"
    DLL_FILTER = ".dll"
    DEFAULT_DYNLIB = "mupen64plus.dll"
    SEARCH_DIRS = ["."]
