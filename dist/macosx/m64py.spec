import os
from os.path import join

DIST_DIR = os.environ["DIST_DIR"]
BASE_DIR = os.environ["BASE_DIR"]

a = Analysis([join(BASE_DIR, 'm64py')], pathex=[join(BASE_DIR, 'src')],
    hiddenimports=['pickle', 'PyQt5.Qt'],
    hookspath=None,
    runtime_hooks=None)

pyz = PYZ(a.pure)

exe = EXE(pyz,
    a.scripts,
    exclude_binaries=True,
    name='m64py',
    debug=False,
    strip=None,
    upx=True,
    console=False)

coll = COLLECT(exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=None,
    upx=True,
    name=join('dist', 'macosx', 'm64py'))

app = BUNDLE(coll,
    name=join('dist', 'macosx', 'M64Py.app'))
