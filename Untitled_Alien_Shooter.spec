# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Untitled_Alien_Shooter.py'],
    pathex=[],
    binaries=[],
    datas=[('Game_Images', 'Game_Images'), ('Game_Music', 'Game_Music'), ('Saves', 'Saves'), ('Text_Font', 'Text_Font')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Untitled_Alien_Shooter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
