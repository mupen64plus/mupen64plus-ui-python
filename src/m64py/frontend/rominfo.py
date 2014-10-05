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

from PyQt5.QtWidgets import QMessageBox

from m64py.utils import sl


class RomInfo():
    """ROM information dialog"""

    def __init__(self, parent=None):
        self.parent = parent
        self.core = self.parent.worker.core
        rom_info = [
            ('GoodName', self.core.rom_settings.goodname.decode()),
            ('Name', self.core.rom_header.Name.decode()),
            ('MD5', self.core.rom_settings.MD5.decode()),
            ('CRC1', '%x' % sl(self.core.rom_header.CRC1)),
            ('CRC2', '%x' % sl(self.core.rom_header.CRC2)),
            ('Type', self.core.rom_type),
            ('Size', self.get_rom_size()),
            ('Country', self.get_country_name()),
            ('Manufacturer', self.get_manufacturer())
        ]
        info = os.linesep.join([k+': '+str(v) for k, v in rom_info if str(v)])
        QMessageBox.information(self.parent, 'ROM Information', info)

    def get_rom_size(self):
        return "%s MB" % (self.core.rom_length/1024/1024)

    def get_manufacturer(self):
        if chr(sl(self.core.rom_header.Manufacturer_ID)) == 'N':
            return 'Nintendo'
        else:
            return '0x%x' % self.core.rom_header.Manufacturer_ID

    def get_country_name(self):
        code = self.core.rom_header.Country_code
        if code == 0:
            name = 'Demo'
        elif code == '7':
            name = 'Beta'
        elif code == int(0x41):
            name = 'Japan/USA'
        elif code == int(0x44):
            name = 'Germany'
        elif code == int(0x45):
            name = 'USA'
        elif code == int(0x46):
            name = 'France'
        elif code == 'I':
            name = 'Italy'
        elif code == int(0x4A):
            name = 'Japan'
        elif code == 'S':
            name = 'Spain'
        elif code in [int(0x55), int(0x59)]:
            name = 'Australia'
        elif code in [int(0x50), int(0x58), int(0x20),
                      int(0x21), int(0x38), int(0x70)]:
            name = 'Europe'
        else:
            name = 'Unknown 0x%x' % code
        return name
