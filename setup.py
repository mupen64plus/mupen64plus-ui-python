#!/usr/bin/env python

import os
import sys
from distutils.core import setup

sys.path.append(os.path.realpath("src"))
from m64py.core.defs import FRONTEND_VERSION

setup(name = "m64py",
        version = FRONTEND_VERSION,
        description = "M64Py - A frontend for Mupen64Plus",
        long_description = "M64Py is a Qt4 front-end (GUI) for Mupen64Plus 2.0, a cross-platform plugin-based Nintendo 64 emulator.",
        author = "Milan Nikolic",
        author_email = "gen2brain@gmail.com",
        license = "GNU GPLv3",
        url = "http://m64py.sourceforge.net",
        packages = ["m64py", "m64py.core", "m64py.frontend", "m64py.ui", "SDL"],
        package_dir = {"": "src"},
        scripts = ["m64py"],
        requires = ["PyQt4"],
        platforms = ["Linux", "Windows", "Darwin"],
        data_files = [
            ("share/pixmaps", ["xdg/m64py.png"]),
            ("share/applications", ["xdg/m64py.desktop"]),
            ("share/mime/packages", ["xdg/application-x-m64py.xml"]),
            ("share/icons/hicolor/96x96/mimetypes/application-x-m64py.png",
                ["xdg/application-x-m64py.xml"])
            ]
        )
