# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Summitive.py'],
    pathex=[],
    binaries=[],
    datas=[('American Captain.ttf', '.'), ('img/*', 'img/'), ('sound/*', 'sound/'), ('enemy/*', 'enemy/'), ('bullets/*', 'bullets/'), ('player/*', 'player/'), ('powerups/*', 'powerups/'), ('sprite_module.py', '.')],
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
    [],
    exclude_binaries=True,
    name='Undead Siege',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Undead Siege',
)
