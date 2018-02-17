# !/usr/bin/env python3
# -*- coding: utf-8 -*-

""" cx_Freeze setup script for bwReplacer. """

# Python imports
import sys # System-specific parameters and functions

# cx_Freeze imports
from cx_Freeze import setup, Executable, build_exe

# Build options
buildOptions = dict(
    create_shared_zip = False
)

# Platform specific
if sys.platform == 'win32':
    exe = Executable(
        appendScriptToExe = True,
        appendScriptToLibrary = False,
        base = "Win32GUI",
        icon = "icon.ico",
        script = "main.py",
        targetDir = "build",
        targetName = "bwReplacer.exe"
    )
else:
    exe = Executable(
        script = "main.py",
        targetDir = "build",
        targetName = "bwReplacer"
    )

# Setup
setup(
    author = 'bulkware',
    description = "An application to correct spelling errors from files.",
    name = "bwReplacer",
    version = "1.1.0",
    options = dict(build_exe = buildOptions),
    executables = [exe]
)
