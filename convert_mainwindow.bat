@ECHO OFF

ECHO Converting "mainwindow.ui" into "mainwindow.py"
"C:\Python33\Lib\site-packages\PyQt4\pyuic4" "mainwindow.ui" -o "mainwindow.py"
