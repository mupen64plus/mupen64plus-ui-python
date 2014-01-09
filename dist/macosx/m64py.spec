# -*- mode: python -*-
import os
a = Analysis(['/Users/milann/Projects/m64py/m64py'],
             pathex=['/Users/milann/Projects/m64py'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.binaries + [('libQtCLucene.4.dylib', '/usr/local/lib/libQtCLucene.4.dylib', 'BINARY')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='m64py',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'macosx', 'm64py'))
app = BUNDLE(coll,
    name=os.path.join('dist', 'macosx', 'M64Py.app'))
