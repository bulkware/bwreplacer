@ECHO OFF
CLS

ECHO Removing cache directory...
RMDIR /Q /S "__pycache__"
RMDIR /Q /S "__pycache__"

ECHO Removing build directory...
RMDIR /Q /S "build"
RMDIR /Q /S "build"

ECHO Removing installers directory...
RMDIR /Q /S "installers"
RMDIR /Q /S "installers"

ECHO Creating installers directory...
MD "installers"

ECHO Compiling executable...
setup.py build

ECHO.

ECHO Copying application files...
COPY /Y "english-tv.db" "build\exe.win32-3.3"
COPY /Y "finnish-tv.db" "build\exe.win32-3.3"
COPY /Y "GPL.txt" "build\exe.win32-3.3"
COPY /Y "License.txt" "build\exe.win32-3.3"
COPY /Y "WhatsNew.txt" "build\exe.win32-3.3"
