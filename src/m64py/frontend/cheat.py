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
import re
from collections import defaultdict

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QListWidgetItem
from PyQt5.QtCore import Qt

from m64py.core.defs import *
from m64py.utils import sl
from m64py.frontend.log import log
from m64py.ui.cheat_ui import Ui_CheatDialog
from m64py.ui.choices_ui import Ui_ChoicesDialog


class Cheat(QDialog, Ui_CheatDialog):
    """Cheats dialog"""

    def __init__(self, parent):
        """Constructor."""
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.cheats = self.read_file()
        if not self.cheats:
            log.info("no cheat codes found for ROM image %s" % (
                self.parent.worker.core.rom_header.Name))
            return
        group = self.group_cheats(self.cheats)
        self.build_tree(group)
        self.parent.actionCheats.setEnabled(False)

    def hideEvent(self, event):
        if self.parent.worker.state == M64EMU_PAUSED:
            self.parent.worker.toggle_pause()

    def build_tree(self, cheats):
        """Builds treeWidget"""
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(1)

        for k1,v1 in sorted(cheats.items()):
            top = QTreeWidgetItem()
            top.setText(0, k1)
            self.treeWidget.addTopLevelItem(top)

            if isinstance(v1, dict):
                for k2,v2 in sorted(v1.items()):
                    child1 = QTreeWidgetItem(top)
                    child1.setText(0, k2)
                    self.treeWidget.addTopLevelItem(child1)

                    if isinstance(v2, dict):
                        for k3,v3 in sorted(v2.items()):
                            child2 = QTreeWidgetItem(child1)
                            child2.setText(0, k3)
                            child2.setCheckState(0, Qt.Unchecked)
                            child2.setData(0, Qt.UserRole, v3)
                            self.treeWidget.addTopLevelItem(child2)
                    else:
                        child1.setCheckState(0, Qt.Unchecked)
                        child1.setData(0, Qt.UserRole, v2)
            else:
                top.setCheckState(0, Qt.Unchecked)
                top.setData(0, Qt.UserRole, v1)

        self.treeWidget.sortItems(0, Qt.AscendingOrder)
        self.treeWidget.itemChanged.connect(self.activate_cheat)
        self.treeWidget.itemClicked.connect(self.on_item_clicked)
        self.treeWidget.itemSelectionChanged.connect(self.on_selection_changed)
        self.pushUnmarkAll.clicked.connect(self.on_unmark_all)

    def on_selection_changed(self):
        """Sets description"""
        items = self.treeWidget.selectedItems()
        for item in items:
            data = item.data(0, Qt.UserRole)
            if data:
                for cheat in data:
                    cd, address, value, choices = cheat
                    desc = cd if cd else ""
                    self.labelDesc.setText(desc)

    def on_item_clicked(self, item, column):
        """Sets description"""
        data = item.data(column, Qt.UserRole)
        if data:
            for cheat in data:
                cd, address, value, choices = cheat
                desc = cd if cd else ""
                self.labelDesc.setText(desc)

    def on_unmark_all(self):
        """Deactivates all cheats"""
        it = QTreeWidgetItemIterator(self.treeWidget)
        while it.value():
            item = it.value()
            state = item.checkState(0)
            if state == Qt.Checked:
                item.setCheckState(0, Qt.Unchecked)
            it += 1

    def activate_cheat(self, item, column):
        """Activates selected cheat"""
        state = item.checkState(column)
        name = item.text(column)
        parent = item.parent()
        if parent:
            name = "%s\\%s" % (parent.text(column), name)
            parent = parent.parent()
            if parent:
                name = "%s\\%s" % (parent.text(column), name)
        data = item.data(column, Qt.UserRole)
        if state == Qt.Checked:
            codes_type = m64p_cheat_code * len(data)
            codes = codes_type()
            for num, cheat in enumerate(data):
                cd, address, value, choices = cheat
                if choices:
                    choices = Choices(self, name, choices)
                    rval = choices.exec_()
                    if rval == QDialog.Accepted:
                        curr_item = choices.listWidget.currentItem()
                        value = curr_item.data(Qt.UserRole)
                    else:
                        #item.setCheckState(0, Qt.Unchecked)
                        return
                codes[num].address = int(address, 16)
                codes[num].value = int(value, 16)
            self.parent.worker.add_cheat(name, codes)
        else:
            self.parent.worker.cheat_enabled(name, False)

    def group_cheats(self, ch):
        cheats = defaultdict(lambda : defaultdict(dict))
        for cheat in ch:
            cn, cd, address, value, choices = cheat
            if '\\' in cn:
                split = cn.split('\\')
                if len(split) == 3:
                    c1, c2, cn = split
                    if not cheats[c1][c2].get(cn):
                        cheats[c1][c2][cn] = []
                    cheats[c1][c2][cn].append((
                        cd, address, value, choices))
                elif len(split) == 2:
                    c1, cn = split
                    if not cheats[c1].get(cn):
                        cheats[c1][cn] = []
                    cheats[c1][cn].append((
                        cd, address, value, choices))
            else:
                if not cheats.get(cn):
                    cheats[cn] = []
                cheats[cn].append((
                    cd, address, value, choices))
        return cheats

    def read_file(self):
        """Parses cheats file"""
        rom_found = False
        cheat_name = None
        cheat_description = None
        cheat_gamename = None
        cheat_codes = []

        cheat_file = os.path.join(
            self.parent.worker.core.config.get_path( "SharedData"), 'mupencheat.txt')
        if not os.path.isfile(cheat_file) or not os.access(cheat_file, os.R_OK):
            log.warn("cheat code database file '%s' not found." % cheat_file)
            return None

        rom_section = "%08X-%08X-C:%X" % (
            sl(self.parent.worker.core.rom_header.CRC1),
            sl(self.parent.worker.core.rom_header.CRC2),
            self.parent.worker.core.rom_header.Country_code & 0xff)
        rom_section = rom_section.upper()

        code_re = re.compile('^([0-9A-F]{8})\s+([?|0-9A-F]{4})\s?(.*)$', re.M)

        try:
            fd = open(cheat_file, 'r')
        except IOError:
            log.warn("couldn't open cheat code database file '%s'." % cheat_file)
            return None
        else:
            lines = [line.strip() for line in fd.readlines()]
            fd.close()

        for line in lines:
            # ignore line if comment
            if line.startswith('#') or line.startswith('//'):
                continue

            # handle beginning of new rom section
            if line.startswith('crc '):
                # if we have already found cheats for the given ROM file
                # then return cheats and exit upon encountering a new ROM section
                if rom_found and (cheat_codes or cheat_gamename is not None):
                    del lines
                    return cheat_codes
                # else see if this section matches
                if line[4:] == rom_section:
                    rom_found = True
                continue

            # if we haven't found the specified section
            # then continue looking
            if not rom_found:
                continue

            # game name
            if line.startswith('gn '):
                cheat_gamename = line[3:]
                continue

            # code name
            if line.startswith('cn '):
                cheat_name = line[3:]
                continue

            # if cheat_name is empty don't do these checks
            if not cheat_name:
                continue

            # code description
            if line.startswith('cd '):
                cheat_description = line[3:]
                continue

            # match cheat codes
            match = code_re.match(line)
            if match:
                c1 = match.group(1)
                c2 = match.group(2)
                if '??' in c2:
                    c3 = [tuple(item.split(':')) for item in match.group(3).split(',')]
                else:
                    c3 = None
                cheat_codes.append(
                        (cheat_name, cheat_description, c1, c2, c3))
                if cheat_description:
                    cheat_description = None
                continue

            if line:
                # otherwise we don't know what this line is
                log.warn("unrecognized line in cheat file: '%s'" % line)
        return None


class Choices(QDialog, Ui_ChoicesDialog):
    """Choices dialog"""

    def __init__(self, parent, cheat_name, choices):
        """Constructor."""
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.choices = choices
        self.labelName.setText(cheat_name)
        self.build_list()

    def build_list(self):
        """Builds listWidget"""
        self.listWidget.clear()
        for choice in sorted(self.choices, key=lambda choice: choice[1]):
            value, name = choice
            item = QListWidgetItem(name.replace('"', ''))
            item.setData(Qt.UserRole, value)
            self.listWidget.addItem(item)
