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

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from m64py.core.defs import *
from m64py.utils import format_label, format_options
from m64py.ui.plugin_ui import Ui_PluginDialog

class Plugin(QDialog, Ui_PluginDialog):
    """Plugin settings dialog"""

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)

    def showEvent(self, event):
        self.set_items()
        self.adjustSize()

    def closeEvent(self, event):
        self.save_items()
        self.config.save_file()
        self.close()

    def show_dialog(self):
        self.config = self.parent.worker.m64p.config
        self.config.open_section(self.section)
        self.rm_items()
        self.add_items()
        self.show()

    def set_section(self, section, desc=None):
        self.section = section
        self.groupBox.setTitle(section)
        title = section if not desc else desc
        self.setWindowTitle(title)

    def rm_items(self):
        self.items = self.config.parameters[self.config.section].items()
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            self.gridLayout.removeWidget(item.widget())
            self.gridLayout.removeItem(item)
            item.widget().hide()
            del item

    def add_items(self):
        self.widgets = {}
        size = QSizePolicy()
        size.setHorizontalStretch(0)
        row1, row2, row3 = 0, 0, 0

        for count, item in enumerate(self.items):
            param_name, param_type = item
            param_help = self.config.get_parameter_help(param_name)
            opts = format_options(param_help)

            if param_type == M64TYPE_STRING:
                row1 += 1
                widget = QLineEdit()
                widget.setToolTip(param_help)
                widget.setSizePolicy(size)
                self.gridLayout.addWidget(
                        QLabel(format_label(param_name)), row1, 1)
                self.gridLayout.addWidget(widget, row1, 2)
                self.widgets[param_name] = (widget, widget.__class__, opts)
            elif param_type == M64TYPE_INT:
                row2 += 1
                if not opts:
                    widget = QSpinBox()
                    widget.setMaximum(65535)
                    if param_help: widget.setToolTip(param_help)
                    widget.setSizePolicy(size)
                else:
                    widget = QComboBox()
                    widget.setToolTip(param_help)
                    for idx, key in enumerate(sorted(opts.keys())):
                        value = opts[key]
                        opts[key] = (idx, value)
                        data = (idx, key, value)
                        widget.addItem(value)
                        widget.setItemData(idx, data)
                self.gridLayout.addWidget(
                        QLabel(format_label(param_name)), row2, 3)
                self.gridLayout.addWidget(widget, row2, 4)
                self.widgets[param_name] = (widget, widget.__class__, opts)
            elif param_type == M64TYPE_BOOL:
                row3 += 1
                widget = QCheckBox()
                widget.setText(format_label(param_name))
                if param_help: widget.setToolTip(param_help)
                self.gridLayout.addWidget(widget, row3, 5)
                self.widgets[param_name] = (widget, widget.__class__, opts)

    def set_items(self):
        for param_name, item in self.widgets.items():
            widget, widget_class, opts = item
            if widget_class == QLineEdit:
                widget.setText(str(self.config.get_parameter(param_name)))
            elif widget_class == QSpinBox:
                param = self.config.get_parameter(param_name)
                if param is not None:
                    widget.setValue(int(self.config.get_parameter(param_name)))
            elif widget_class == QComboBox:
                key = self.config.get_parameter(param_name)
                try:
                    idx, value = opts[key]
                except KeyError:
                    idx = 0
                widget.setCurrentIndex(int(idx))
            elif widget_class == QCheckBox:
                widget.setChecked(bool(self.config.get_parameter(param_name)))

    def save_items(self):
        for param_name, item in self.widgets.items():
            widget, widget_class, opts = item
            if widget_class == QLineEdit:
                param_value = str(widget.text())
            elif widget_class == QSpinBox:
                param_value = int(widget.value())
            elif widget_class == QComboBox:
                data = widget.itemData(widget.currentIndex())
                idx, key, value = data
                param_value = key
            elif widget_class == QCheckBox:
                param_value = bool(widget.isChecked())
            self.config.set_parameter(param_name, param_value)
