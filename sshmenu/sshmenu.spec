# -*- mode: python -*-
a = Analysis(['sshmenu.py'],
             pathex=[''],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='sshmenu',
          debug=False,
          strip=None,
          upx=False,
          console=True )
