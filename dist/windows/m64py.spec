import os
from os.path import join

DIST_DIR = os.environ["DIST_DIR"]
BASE_DIR = os.environ["BASE_DIR"]

a = Analysis([join(BASE_DIR, 'm64py')], hiddenimports=['pickle', 'PyQt5.Qt'], pathex=[join(BASE_DIR, 'src')], hookspath=[join(DIST_DIR, 'hooks')], runtime_hooks=[join(DIST_DIR, 'hooks', 'libdir.py')])

pyz = PYZ(a.pure)

exe = EXE(pyz,
	a.scripts,
	exclude_binaries=1,
	name=join(DIST_DIR, 'build', 'pyi.win32', 'm64py', 'm64py.exe'),
	debug=False,
	strip=False,
	upx=True,
	console=False,
	icon=join(DIST_DIR, 'm64py.ico'))

coll = COLLECT(exe,
	a.binaries,
	a.zipfiles,
	a.datas,
	strip=False,
	upx=True,
	name='m64py')
