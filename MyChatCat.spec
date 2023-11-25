# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mychatcat.py'],
    pathex=[],
    binaries=[],
    datas=[('assert/setting.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MyChatCat',
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
    icon=['assert/icon.icns'],
)
app = BUNDLE(
    exe,
    name='MyChatCat.app',
    icon='assert/icon.icns',
    bundle_identifier=None,
)
