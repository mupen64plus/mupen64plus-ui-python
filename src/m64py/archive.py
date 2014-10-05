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
import bz2
import gzip
import zipfile
import shutil
import tempfile
from subprocess import Popen, PIPE
import binascii

from m64py.utils import which

try:
    import rarfile
    HAS_RAR = True
    RAR_CMD = None
except ImportError:
    HAS_RAR = False
    RAR_CMD = which("rar") or which("unrar")

try:
    from py7zlib import Archive7z
    HAS_7Z = True
    LZMA_CMD = None
except ImportError:
    HAS_7Z = False
    LZMA_CMD = which("7z")

ZIP, GZIP, BZIP, RAR, LZMA, ROM = range(6)

EXT_FILTER = "*.*64 *.zip *.gz *.bz2"
if HAS_RAR or RAR_CMD: EXT_FILTER += " *.rar"
if HAS_7Z or LZMA_CMD: EXT_FILTER += " *.7z"

ROM_TYPE = {
    b'80371240': 'z64 (native)',
    b'37804012': 'v64 (byteswapped)',
    b'40123780': 'n64 (wordswapped)'
}


class Archive():
    """Extracts ROM file from archive."""

    def __init__(self, filename):
        """Opens archive."""
        self.file = os.path.realpath(filename)
        if not os.path.isfile(self.file) or not os.access(self.file, os.R_OK):
            raise IOError("Cannot open %s. No such file." % self.file)

        self.filetype = self.get_filetype()

        if self.filetype == ZIP:
            self.fd = zipfile.ZipFile(self.file, "r")
        elif self.filetype == GZIP:
            self.fd = gzip.GzipFile(self.file, "rb")
        elif self.filetype == BZIP:
            self.fd = bz2.BZ2File(self.file, "r")
        elif self.filetype == ROM:
            self.fd = open(self.file, "rb")
        elif self.filetype == RAR:
            if HAS_RAR:
                rarfile.USE_EXTRACT_HACK = 0
                self.fd = rarfile.RarFile(self.file)
            elif RAR_CMD:
                self.fd = RarCmd(self.file)
            else:
                raise IOError("rarfile module or rar/unrar is needed for %s." % self.file)
        elif self.filetype == LZMA:
            if HAS_7Z:
                self.fd = Archive7z(open(self.file, "rb"))
            elif LZMA_CMD:
                self.fd = LzmaCmd(self.file)
            else:
                raise IOError("lzma module or 7z is needed for %s." % self.file)
        else:
            raise IOError("File %s is not a N64 ROM file." % self.file)

        self.namelist = self.get_namelist()

    def read(self, filename=None, size=-1):
        """Reads data."""
        data = None
        fname = self.namelist[0] if not filename else filename
        if self.filetype == ZIP:
            fd = self.fd.open(fname)
            data = fd.read(size)
        elif self.filetype == GZIP:
            data = self.fd.read(size)
        elif self.filetype == BZIP:
            data = self.fd.read(size)
        elif self.filetype == RAR:
            if HAS_RAR:
                fd = self.fd.open(fname)
                data = fd.read(size)
            elif RAR_CMD:
                data = self.fd.read(fname, size)
        elif self.filetype == LZMA:
            if HAS_7Z:
                fd = self.fd.getmember(fname)
                if size != -1:
                    fd.size = size
                data = fd.read()
            elif LZMA_CMD:
                data = self.fd.read(fname, size)
        elif self.filetype == ROM:
            data = self.fd.read(size)
        return data

    def close(self):
        """Closes file descriptor."""
        if self.filetype != LZMA:
            self.fd.close()

    def get_namelist(self):
        """Gets list of files in archive."""
        if self.filetype == ZIP:
            namelist = [name.filename for name in self.fd.infolist()]
        elif self.filetype == GZIP:
            namelist = [os.path.basename(self.file)]
        elif self.filetype == BZIP:
            namelist = [os.path.basename(self.file)]
        elif self.filetype == RAR:
            if HAS_RAR:
                namelist = [name.filename for name in self.fd.infolist()]
            elif RAR_CMD:
                namelist = self.fd.namelist()
        elif self.filetype == LZMA:
            if HAS_7Z:
                namelist = self.fd.getnames()
            elif LZMA_CMD:
                namelist = self.fd.namelist()
        elif self.filetype == ROM:
            namelist = [os.path.basename(self.file)]
        return namelist

    def get_filetype(self):
        """Gets archive type."""
        fd = open(self.file, "rb")
        magic = fd.read(4)
        fd.close()
        if magic == b'PK\03\04':
            return ZIP
        elif magic.startswith(b'\037\213'):
            return GZIP
        elif magic.startswith(b'BZh'):
            return BZIP
        elif magic == b'Rar!':
            return RAR
        elif magic == b'7z\xbc\xaf':
            return LZMA
        elif binascii.hexlify(magic) in ROM_TYPE.keys():
            return ROM
        return None


class RarCmd:
    """Extracts ROM file from RAR archive."""

    def __init__(self, archive):
        """Opens archive."""
        self.fd = None
        self.file = archive
        self.filename = None
        self.tempdir = tempfile.mkdtemp()

    def namelist(self):
        """Returns list of filenames in archive."""
        proc = Popen([RAR_CMD, 'vb', self.file], stdout=PIPE)
        return [name.rstrip(os.linesep) for name in proc.stdout.readlines()]

    def extract(self):
        """Extracts archive to temp dir."""
        cmd = [RAR_CMD, 'x', '-kb', '-p-', '-o-', '-inul', '--',
                self.file, self.filename, self.tempdir]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out = proc.communicate()
        if out[1] != '':
            raise IOError("Error extracting file %s: %s." % (self.file, out[1]))

    def read(self, filename=None, size=-1):
        """Reads data."""
        self.filename = filename if filename else self.namelist()[0]
        self.extract()
        self.fd = open(os.path.join(self.tempdir, self.filename), "rb")
        return self.fd.read(size)

    def close(self):
        """Closes file descriptor and clean resources."""
        if self.fd:
            self.fd.close()
        shutil.rmtree(self.tempdir)


class LzmaCmd:
    """Extracts ROM file from 7z archive."""

    def __init__(self, archive):
        """Opens archive."""
        self.fd = None
        self.file = archive
        self.filename = None
        self.tempdir = tempfile.mkdtemp()

    def namelist(self):
        """Returns list of filenames in archive."""
        proc = Popen([LZMA_CMD, 'l', self.file], stdout=PIPE)
        lines = [name.rstrip(os.linesep) for name in proc.stdout.readlines() if '...A' in name]
        return [name[53:] for name in lines]

    def extract(self):
        """Extracts archive to temp dir."""
        cmd = [LZMA_CMD, 'x', '-o'+self.tempdir, self.file, self.filename]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out = proc.communicate()
        if "Error" in out[0]:
            raise IOError("Error extracting file %s: %s." % (
                self.file, out[0]))

    def read(self, filename=None, size=-1):
        """Reads data."""
        self.filename = filename if filename else self.namelist()[0]
        self.extract()
        self.fd = open(os.path.join(self.tempdir, self.filename), "rb")
        return self.fd.read(size)

    def close(self):
        """Closes file descriptor and clean resources."""
        if self.fd:
            self.fd.close()
        shutil.rmtree(self.tempdir)
