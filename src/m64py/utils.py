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

import re


def version_split(ver):
    return "%d.%d.%d" % (
        ((ver >> 16) & 0xffff),
        ((ver >> 8) & 0xff),
        (ver & 0xff))


def sl(mot):
    return ((mot & 0x000000FF) << 24) |\
           ((mot & 0x0000FF00) << 8) |\
           ((mot & 0x00FF0000) >> 8) |\
           ((mot & 0xFF000000) >> 24)


def format_tooltip(tooltip):
    if len(tooltip) > 80:
        lines = tooltip.split(". ")
        tooltip = ""
        for line in lines:
            tooltip += "%s. " % line.lstrip()
            if len(line) > 40:
                tooltip += "\n"
    return tooltip


def format_label(label):
    label = label.replace("_", " ")
    if label.isupper():
        label = label.capitalize()
    else:
        label = label[0].upper() + label[1:]
    return label


def format_options(param_help):
    opts = {}
    if not param_help:
        return None
    items = re.findall(
        r"(\d+|[\d,-]+)\s?=\s?([\w/ %-]+)", param_help)
    for item in items:
        key, value = item
        if '-' in key[1:] or ',' in key:
            return None
        else:
            opts[int(key)] = value
    if len(opts) > 0:
        return opts
    return None
