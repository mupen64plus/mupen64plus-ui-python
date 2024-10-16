import os
from os.path import join

DIST_DIR = os.environ["DIST_DIR"]
BASE_DIR = os.environ["BASE_DIR"]

a = Analysis(
    [join(BASE_DIR, 'bin', 'm64py')],
    pathex=[join(BASE_DIR, 'src')],
    hiddenimports=['pickle'])

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='m64py',
    debug=False,
    strip=False,
    upx=True,
    target_arch='x86_64',
    console=False)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=join('dist', 'macosx', 'm64py'))

app = BUNDLE(
    coll,
    name=join('dist', 'macosx', 'M64Py.app'))
