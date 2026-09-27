#!/usr/bin/env bash
set -euo pipefail

# Do not hand-edit the generated form; this command deliberately replaces it.
pyside6-uic mainwindow.ui -o mainwindow.py
