# -*- mode: python -*-
a = Analysis(['../ocsidm.py'],
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
          name='ocsidm',
          debug=False,
          strip=None,
          upx=False,
          console=True )
