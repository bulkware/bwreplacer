@ECHO OFF

ECHO Converting "icons.qrc" into "icons_rc.py"
"C:\Python33\Lib\site-packages\PyQt4\pyrcc4" -py3 "icons.qrc" -o "icons_rc.py"
