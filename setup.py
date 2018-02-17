# !/usr/bin/env python3
# -*- coding: utf-8 -*-

""" cx_Freeze setup script for bwReplacer. """

# cx_Freeze imports
from cx_Freeze import setup, Executable

includes = ["re"]

# Excecutable
eggsacutibull = Executable (
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    base = 'Win32GUI',
    compress = True,
    copyDependentFiles = True,
    icon = "icon.ico",
    initScript = None,
    script = "main.py",
    targetName = "bwReplacer.exe"
)

# Setup
setup (
    author = 'bulkware',
    description = "An application to correct spelling errors from files.",
    name = "bwReplacer",
    version = "1.00",
    executables = [eggsacutibull],
    options = {"build_exe": {"includes":includes}}
)
