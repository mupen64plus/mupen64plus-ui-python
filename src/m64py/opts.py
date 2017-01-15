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

from optparse import OptionParser

from m64py.core.defs import FRONTEND_VERSION

usage = 'usage: %prog <romfile>'
parser = OptionParser(usage=usage, version="M64Py Version %s" % FRONTEND_VERSION)
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="show verbose output")
opts, args = parser.parse_args()

VERBOSE = opts.verbose
