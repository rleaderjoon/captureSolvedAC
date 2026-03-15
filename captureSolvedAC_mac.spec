# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for captureSolvedAC (macOS)
# Run: pyinstaller captureSolvedAC_mac.spec --clean --noconfirm

import sys
from pathlib import Path

block_cipher = None

# --- Include CustomTkinter assets (themes, images) ---
datas_extra = []
try:
    import customtkinter as _ctk
    ctk_dir = Path(_ctk.__file__).parent
    datas_extra.append((str(ctk_dir), "customtkinter"))
except ImportError:
    pass

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas_extra,
    hiddenimports=[
        "playwright.async_api",
        "playwright.sync_api",
        "playwright._impl._driver",
        "playwright._impl._api_types",
        "customtkinter",
        "PIL._tkinter_finder",
        "PIL.Image",
        "PIL.ImageDraw",
        "PIL.ImageFont",
    ],
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
    [],
    exclude_binaries=True,
    name="captureSolvedAC",
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="captureSolvedAC",
)

app = BUNDLE(
    coll,
    name="captureSolvedAC.app",
    icon=None,
    bundle_identifier="com.captureSolvedAC",
)
