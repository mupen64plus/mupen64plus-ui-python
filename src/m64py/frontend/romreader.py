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
import ctypes
import fnmatch

from PyQt5.QtCore import QThread

from m64py.utils import sl
from m64py.core.defs import m64p_rom_header
from m64py.frontend.log import log
from m64py.archive import Archive, EXT_FILTER


class ROMReader(QThread):
    """ROM reader thread"""

    def __init__(self, parent):
        """Constructor."""
        QThread.__init__(self, parent)
        self.parent = parent
        self.roms = []
        self.rom_path = None

    def set_path(self, path):
        """Sets ROM directory path."""
        self.rom_path = path

    def get_roms(self):
        """Returns ROM list."""
        return self.roms

    def get_files(self):
        """Returns list of files found in path."""
        files = []
        types = EXT_FILTER.split()
        for filename in os.listdir(self.rom_path):
            for ext in types:
                if fnmatch.fnmatch(filename, ext):
                    files.append(filename)
        return files

    def get_rom_crc(self, archive, fname):
        rom_header = m64p_rom_header()
        ctypes.memmove(
            ctypes.byref(rom_header),
            archive.read(fname, ctypes.sizeof(rom_header)),
            ctypes.sizeof(rom_header))
        crc1_pre = sl(rom_header.CRC1)
        crc2_pre = sl(rom_header.CRC2)

        regs = 0
        regs |= rom_header.init_PI_BSB_DOM1_LAT_REG << 24
        regs |= rom_header.init_PI_BSB_DOM1_PGS_REG << 16
        regs |= rom_header.init_PI_BSB_DOM1_PWD_REG << 8
        regs |= rom_header.init_PI_BSB_DOM1_PGS_REG2

        if regs == 0x80371240:
            # native *.z64
            crc1 = crc1_pre
            crc2 = crc2_pre
        elif regs == 0x37804012:
            # byteswapped [BADC] *.v64
            crc1 = 0
            crc1 |= ((crc1_pre >> 0) & 0xff) << 8
            crc1 |= ((crc1_pre >> 8) & 0xff) << 0
            crc1 |= ((crc1_pre >> 16) & 0xff) << 24
            crc1 |= ((crc1_pre >> 24) & 0xff) << 16
            crc2 = 0
            crc2 |= ((crc2_pre >> 0) & 0xff) << 8
            crc2 |= ((crc2_pre >> 8) & 0xff) << 0
            crc2 |= ((crc2_pre >> 16) & 0xff) << 24
            crc2 |= ((crc2_pre >> 24) & 0xff) << 16
        elif regs == 0x40123780:
            # wordswapped [DCBA] *.n64
            crc1 = 0
            crc1 |= ((crc1_pre >> 0) & 0xff) << 24
            crc1 |= ((crc1_pre >> 8) & 0xff) << 16
            crc1 |= ((crc1_pre >> 16) & 0xff) << 8
            crc1 |= ((crc1_pre >> 24) & 0xff) << 0
            crc2 = 0
            crc2 |= ((crc2_pre >> 0) & 0xff) << 24
            crc2 |= ((crc2_pre >> 8) & 0xff) << 16
            crc2 |= ((crc2_pre >> 16) & 0xff) << 8
            crc2 |= ((crc2_pre >> 24) & 0xff) << 0
        else:
            return None
        return (crc1, crc2)

    def read_files(self):
        """Reads files."""
        self.roms = []
        files = self.get_files()
        num_files = len(files)
        for filenum, filename in enumerate(files):
            fullpath = os.path.join(self.rom_path, filename)
            try:
                archive = Archive(fullpath)
                for fname in archive.namelist:
                    crc_tuple = self.get_rom_crc(archive, fname)
                    if crc_tuple:
                        rom_settings = self.parent.core.get_rom_settings(
                            crc_tuple[0], crc_tuple[1])
                        if rom_settings:
                            crc = "%X%X" % (crc_tuple[0], crc_tuple[1])
                            self.roms.append((crc, rom_settings.goodname, fullpath, fname))
                archive.close()
            except Exception as err:
                log.warn(str(err))
                continue
            percent = float(filenum) / float(num_files) * 100
            self.parent.progressBar.valueChanged.emit(percent)
        self.exit()

    def stop(self):
        """Stops thread."""
        if self.isRunning():
            self.terminate()
            self.wait()

    def run(self):
        """Starts thread."""
        self.read_files()
        self.exec_()
