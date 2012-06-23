# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), '/Users/User/Projects/m64py/m64py'],
             pathex=['/Users/User/Projects/m64py'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/m64py', 'm64py'),
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'm64py'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'M64Py.app'))
