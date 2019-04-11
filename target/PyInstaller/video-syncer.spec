# -*- mode: python -*-

block_cipher = None


a = Analysis(['/home/dave/External/work/video-syncer/src/main/python/main.py'],
             pathex=['/home/dave/External/work/video-syncer/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/home/dave/External/work/video-syncer/venv/lib/python3.5/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/tmp/tmpd9uz2y4s/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='video-syncer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='video-syncer')
