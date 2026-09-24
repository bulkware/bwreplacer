#!/bin/bash

# Regenerate the Python form after changing the Qt Designer source file.
# The output is intentionally not edited by hand.
pyside6-uic "mainwindow.ui" -o "mainwindow.py"
