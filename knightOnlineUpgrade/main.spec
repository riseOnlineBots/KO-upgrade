# -*- mode: python ; coding: utf-8 -*-


block_cipher = pyi_crypto.PyiBlockCipher(key='ffXaqEEEg?b86!6365aADEf.!!')


a = Analysis(
    ['C:\\Users\\undefined\\PycharmProjects\\knightOnlineUpgrade\\main.py'],
    pathex=['C:\\Users\\undefined\\AppData\\Local\\Programs\\Python\\Python39-32\\Lib\\site-packages'],
    binaries=[],
    datas=[('items', 'items'), ('confirmButton1.jpg', '.'), ('confirmButton2.jpg', '.'), ('upgradeScroll.jpg', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='upWork',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
