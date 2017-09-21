# -*- mode: python -*-

block_cipher = None


a = Analysis(['httpc_lib.py'],
             pathex=['/home/mik-ds/COMP445/lab1/httpc/dist'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='httpc',
          debug=False,
          strip=False,
          upx=True,
          console=True )
