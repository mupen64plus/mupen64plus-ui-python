# -*- mode: python -*-

a = Analysis(['c:\\m64py\\m64py'],
	pathex=['c:\\m64py\\pyinstaller-2.1', 'c:\\m64py\\src'])

pyz = PYZ(a.pure)

exe = EXE(pyz,
	a.scripts,
	exclude_binaries=1,
	name=os.path.join('build\\pyi.win32\\m64py', 'm64py.exe'),
	debug=False,
	strip=False,
	upx=True,
	console=False,
	icon='c:\\m64py\\dist\\windows\\m64py.ico')

coll = COLLECT(exe,
	a.binaries,
	a.zipfiles,
	a.datas,
	strip=False,
	upx=True,
	name='m64py')
