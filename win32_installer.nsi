; The name of the installer
Name "bwReplacer"

; The file to write
OutFile "installers\bwReplacer_101_installer_win32.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\bwReplacer"

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\bwReplacer" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages
Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "bwReplacer (required)"

    SectionIn RO

    ; Set output path to the installation directory.
    SetOutPath $INSTDIR

    ; Put application files there
    File "build\exe.win32-3.3\*.*"

    ; Write the installation path into the registry
    WriteRegStr HKLM "SOFTWARE\bwReplacer" "Install_Dir" "$INSTDIR"

    ; Write the uninstall keys for Windows
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwReplacer" "DisplayName" "bwReplacer"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwReplacer" "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwReplacer" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwReplacer" "NoRepair" 1
    WriteUninstaller "Uninstall.exe"

SectionEnd


; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

    CreateDirectory "$SMPROGRAMS\bwReplacer"
    CreateShortCut "$SMPROGRAMS\bwReplacer\bwReplacer.lnk" "$INSTDIR\bwReplacer.exe" "" "$INSTDIR\bwReplacer.exe" 0
    CreateShortCut "$SMPROGRAMS\bwReplacer\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0

SectionEnd

;--------------------------------

; Uninstaller
Section "Uninstall"

    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwReplacer"
    DeleteRegKey HKLM "SOFTWARE\bwReplacer"

    ; Remove files
    Delete "$INSTDIR\*.*"

    ; Remove shortcuts, if any
    Delete "$SMPROGRAMS\bwReplacer\*.*"

    ; Remove directories used
    RMDir "$SMPROGRAMS\bwReplacer"
    RMDir "$INSTDIR"

SectionEnd
