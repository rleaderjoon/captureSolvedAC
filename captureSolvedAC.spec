# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for captureSolvedAC
# Run: pyinstaller captureSolvedAC.spec --clean --noconfirm

import os
import sys
from pathlib import Path

block_cipher = None

# --- Include Playwright driver binary (for 'playwright install chromium' in frozen app) ---
binaries_extra = []
try:
    import playwright as _pw
    driver_exe = Path(_pw.__file__).parent / "driver" / "playwright.exe"
    if driver_exe.exists():
        binaries_extra.append((str(driver_exe), "playwright/driver"))
        print(f"[spec] Including playwright driver: {driver_exe}")
    else:
        print("[spec] playwright.exe driver not found, skipping")
except ImportError:
    print("[spec] playwright not installed")

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
    binaries=binaries_extra,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="captureSolvedAC",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # No terminal window for end users
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon="assets/icon.ico",  # Uncomment if you add an icon file
)
