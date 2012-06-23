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
import bz2
import gzip
import zipfile
import shutil
import tempfile
from subprocess import Popen, PIPE

try:
    from m64py.utils import which
except ImportError, err:
    sys.stderr.write("Error: Can't import m64py modules%s%s%s" % (
        os.linesep, str(err), os.linesep))
    sys.exit(1)

try:
    import UnRAR2
    HAS_RAR = True
    RAR_CMD = None
except:
    HAS_RAR = False
    RAR_CMD = which("rar") or which("unrar")

try:
    from py7zlib import Archive7z
    HAS_7Z = True
    LZMA_CMD = None
except:
    HAS_7Z = False
    LZMA_CMD = which("7z")

ZIP, GZIP, BZIP, RAR, LZMA, ROM = range(6)

EXT_FILTER = "*.*64 *.zip *.gz *.bz2"
if HAS_RAR or RAR_CMD: EXT_FILTER += " *.rar"
if HAS_7Z or LZMA_CMD: EXT_FILTER += " *.7z"

ROM_TYPE = {
    '80371240': 'z64 (native)',
    '37804012': 'v64 (byteswapped)',
    '40123780': 'n64 (wordswapped)'
}

class Archive():
    """Extracts ROM file from archive."""

    def __init__(self, filename):
        """Opens archive."""
        self.file = os.path.realpath(filename)
        if not os.path.isfile(self.file) \
                or not os.access(self.file, os.R_OK):
            raise IOError("Cannot open %s. No such file." % (
                self.file))

        self.filetype = self.get_filetype()
        if self.filetype == ZIP:
            self.fd = zipfile.ZipFile(self.file, 'r')
        elif self.filetype == GZIP:
            self.fd = gzip.GzipFile(self.file, 'rb')
        elif self.filetype == BZIP:
            self.fd = bz2.BZ2File(self.file, 'r')
        elif self.filetype == ROM:
            self.fd = open(self.file, 'rb')
        elif self.filetype == RAR:
            if HAS_RAR:
                self.fd = UnRAR2.RarFile(self.file)
            elif RAR_CMD:
                self.fd = RarCmd(self.file)
            else:
                raise IOError("UnRAR2 module or rar/unrar is needed for %s." % (
                    self.file))
        elif self.filetype == LZMA:
            if HAS_7Z:
                self.fd = Archive7z(open(self.file, 'rb'))
            elif LZMA_CMD:
                self.fd = LzmaCmd(self.file)
            else:
                raise IOError("lzma module or 7z is needed for %s." % (
                    self.file))
        else:
            raise IOError("File %s is not a N64 ROM file." % (
                self.file))

    def read(self):
        """Reads data. If archive has more then one
        file the first one is used."""
        data = None
        if self.filetype == ZIP:
            data = self.fd.read(self.fd.infolist()[0])
        elif self.filetype == GZIP:
            data = self.fd.read()
        elif self.filetype == BZIP:
            data = self.fd.read()
        elif self.filetype == RAR:
            if HAS_RAR:
                data = self.fd.read_files()[0][1]
            elif RAR_CMD:
                data = self.fd.read()
        elif self.filetype == LZMA:
            if HAS_7Z:
                data = self.fd.getmember(
                        self.fd.getnames()[0]).read()
            elif LZMA_CMD:
                data = self.fd.read()
        elif self.filetype == ROM:
            data = self.fd.read()
        return data

    def close(self):
        """Closes file descriptor."""
        if self.filetype in [RAR, LZMA]:
            if RAR_CMD or LZMA_CMD:
                self.fd.close()
        else:
            self.fd.close()

    def get_filetype(self):
        """Gets archive type."""
        fd = open(self.file, 'rb')
        magic = fd.read(4)
        fd.close()
        if magic == 'PK\03\04':
            return ZIP
        elif magic.startswith('\037\213'):
            return GZIP
        elif magic.startswith('BZh'):
            return BZIP
        elif magic == 'Rar!':
            return RAR
        elif magic == '7z\xbc\xaf':
            return LZMA
        elif magic.encode('hex') in ROM_TYPE.keys():
            return ROM
        return None

class RarCmd:
    """Extracts ROM file from RAR archive."""

    def __init__(self, archive):
        """Opens archive."""
        self.file = archive
        self.namelist = self.namelist()
        self.filename = self.namelist[0]
        self.tempdir = tempfile.mkdtemp(self.file)
        self.extract()
        self.fd = open(os.path.join(
            self.tempdir, self.filename), "rb")

    def namelist(self):
        """Returns list of filenames in archive."""
        proc = Popen([RAR_CMD, 'vb', self.file], stdout=PIPE)
        return [name.rstrip(os.linesep) for name in proc.stdout.readlines()]

    def extract(self):
        """Extracts archive to temp dir."""
        proc = Popen([RAR_CMD, 'x', '-kb', '-p-', '-o-', '-inul', '--',
                self.file, self.filename, self.tempdir],
                stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out = proc.communicate()
        if out[1] != '':
            raise IOError("Error extracting file %s: %s." % (
                self.file, out[1]))

    def read(self):
        """Reads data."""
        return self.fd.read()

    def close(self):
        """Closes file descriptor and clean resources."""
        self.fd.close()
        shutil.rmtree(self.tempdir)

class LzmaCmd:
    """Extracts ROM file from 7z archive."""

    def __init__(self, archive):
        """Opens archive."""
        self.file = archive
        self.namelist = self.namelist()
        self.filename = self.namelist[0]
        self.tempdir = tempfile.mkdtemp(self.filename)
        self.extract()
        self.fd = open(os.path.join(
            self.tempdir, self.filename), "rb")

    def namelist(self):
        """Returns list of filenames in archive."""
        proc1 = Popen([LZMA_CMD, 'l', self.file], stdout=PIPE)
        proc2 = Popen(['grep', '-F', '...A'], stdin=proc1.stdout, stdout=PIPE)
        lines = [name.rstrip(os.linesep) for name in proc2.stdout.readlines()]
        return [name[53:] for name in lines]

    def extract(self):
        """Extracts archive to temp dir."""
        proc = Popen([LZMA_CMD, 'x', '-o'+self.tempdir, self.file, self.filename],
                stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out = proc.communicate()
        if "Error" in out[0]:
            raise IOError("Error extracting file %s: %s." % (
                self.file, out[0]))

    def read(self):
        """Reads data."""
        return self.fd.read()

    def close(self):
        """Closes file descriptor and clean resources."""
        self.fd.close()
        shutil.rmtree(self.tempdir)
