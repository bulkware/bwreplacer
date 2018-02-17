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
COPY /Y "about.png" "build"
COPY /Y "add_files.png" "build"
COPY /Y "add_folder.png" "build"
COPY /Y "clear.png" "build"
COPY /Y "corrections.png" "build"
COPY /Y "delete_row.png" "build"
COPY /Y "fix.png" "build"
COPY /Y "icon.png" "build"
COPY /Y "insert_row.png" "build"
COPY /Y "lists.png" "build"
COPY /Y "log.png" "build"
COPY /Y "new_database.png" "build"
COPY /Y "open_database.png" "build"
COPY /Y "quit.png" "build"
COPY /Y "remove.png" "build"
COPY /Y "settings.png" "build"
COPY /Y "start.png" "build"
COPY /Y "update_row.png" "build"
COPY /Y "url.png" "build"

COPY /Y "english-tv.db" "build"
COPY /Y "finnish-tv.db" "build"

COPY /Y "gpl.txt" "build"
COPY /Y "icons.txt" "build"
COPY /Y "license.txt" "build"
COPY /Y "whats_new.txt" "build"
