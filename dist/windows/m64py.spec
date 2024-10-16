import os
from os.path import join

DIST_DIR = os.environ["DIST_DIR"]
BASE_DIR = os.environ["BASE_DIR"]

a = Analysis(
    [join(BASE_DIR, 'bin', 'm64py')],
    pathex=[join(BASE_DIR, 'src')],
    hiddenimports=['pickle'],
    noarchive=False,
    optimize=0)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=1,
    name=join(DIST_DIR, 'build', 'pyi.win32', 'm64py', 'm64py.exe'),
    debug=False,
    strip=False,
    upx=True,
    console=True,
    hide_console='hide-early',
    icon=join(DIST_DIR, 'm64py.ico'))

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='m64py')
