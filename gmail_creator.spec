# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for Gmail Creator Pro.
Produces a single-file executable with embedded config_examples.

Usage:
    pyinstaller gmail_creator.spec
"""

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ["auto_gmail_creator.py"],
    pathex=[str(Path(__file__).parent)],
    binaries=[],
    datas=[
        ("config_examples", "config_examples"),
    ],
    hiddenimports=["src.gmail_creator"],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "unittest", "pytest"],
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
    name="gmail-creator-pro",
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
