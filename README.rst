::

                  _____ __ __
       ____ ___  / ___// // / ____  __  __
      / __ `__ \/ __ \/ // /_/ __ \/ / / /
     / / / / / / /_/ /__  __/ /_/ / /_/ /
    /_/ /_/ /_/\____/  /_/ / .___/\__, /
                          /_/    /____/
        https://m64py.sourceforge.net
        A frontend for Mupen64Plus


About
=====

M64Py is a Qt6 front-end (GUI) for `Mupen64Plus <https://mupen64plus.org/>`_, a cross-platform
plugin-based Nintendo 64 emulator. Front-end is written in Python and it
provides a user-friendly interface over the Mupen64Plus shared library.

Features
========

* Changeable emulation plugins for audio, core, input, rsp, video
* Selection of emulation core
* Configuration dialogs for core, plugin and input settings
* ROMs list with preview images
* Input bindings configuration
* Cheats support
* Support gzip, bzip2, zip, rar and 7z archives
* Video extension (embedded OpenGL window)

Dependencies
============

* `PyQt6 <https://www.riverbankcomputing.com/software/pyqt>`_ (QtCore, QtGui, QtWidgets)
* `PySDL2 <https://pysdl2.readthedocs.io>`_

Ubuntu
++++++


``sudo apt install libsdl2-dev qttools6-dev-tools pyqt6-dev-tools python3-pyqt6``

PyPi
++++

To install just the Python dependencies:

``python -m pip install -r requirements.txt --user``

.. note::

  This will not install the other system dependencies which are listed above.

  You can also drop the ``--user`` flag and run as root user if you want to
  install system-wide, but this is not recommended, as this will likely
  screw up your distro's package management.

Install
=======

.. code::

  python -m pip install . --user

.. note::

  If you use the ``--user`` flag, make sure ``~/.local/bin`` is in your
  user's path environment variable.

License
=======

M64Py is free/libre software released under the terms of the GNU GPL license.
Please see the ``COPYING`` file for details.
