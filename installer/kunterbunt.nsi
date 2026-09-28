; Kunterbunt City – Windows-Installer (NSIS, zlib-Lizenz, 0 €).
; Installiert OHNE Admin-Rechte nach %LOCALAPPDATA%\KunterbuntCity, legt eine Desktop-Verknüpfung und einen
; Startmenü-Eintrag an und startet das Spiel auf Wunsch sofort. Kein Netzwerk, keine Datensammlung (R-02).
; Bauen: makensis -DVERSION=1.0.0 -DSRC=export/windows -DOUT=export/KunterbuntCity-Setup.exe installer/kunterbunt.nsi

Unicode true
!include "MUI2.nsh"

!ifndef VERSION
  !define VERSION "1.0.0"
!endif
!ifndef SRC
  !define SRC "..\export\windows"
!endif
!ifndef OUT
  !define OUT "..\export\KunterbuntCity-Setup.exe"
!endif
!define APP "Kunterbunt City"
!define EXE "KunterbuntCity.exe"
!define UNKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\KunterbuntCity"

Name "${APP}"
OutFile "${OUT}"
InstallDir "$LOCALAPPDATA\KunterbuntCity"
RequestExecutionLevel user
SetCompressor /SOLID lzma
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName" "${APP}"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey "FileDescription" "${APP} – Installation"
VIAddVersionKey "LegalCopyright" "Kostenlos, ohne Werbung, ohne Datensammlung"

!define MUI_ICON "..\assets\app\icon.ico"
!define MUI_UNICON "..\assets\app\icon.ico"
!define MUI_ABORTWARNING
!define MUI_FINISHPAGE_RUN "$INSTDIR\${EXE}"
!define MUI_FINISHPAGE_RUN_TEXT "Kunterbunt City jetzt starten"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "German"
!insertmacro MUI_LANGUAGE "English"

Section "Spiel"
  SetOutPath "$INSTDIR"
  File "${SRC}\${EXE}"
  File "..\assets\app\icon.ico"
  WriteUninstaller "$INSTDIR\Deinstallieren.exe"
  CreateShortcut "$DESKTOP\${APP}.lnk" "$INSTDIR\${EXE}" "" "$INSTDIR\icon.ico" 0
  CreateDirectory "$SMPROGRAMS\${APP}"
  CreateShortcut "$SMPROGRAMS\${APP}\${APP}.lnk" "$INSTDIR\${EXE}" "" "$INSTDIR\icon.ico" 0
  CreateShortcut "$SMPROGRAMS\${APP}\Deinstallieren.lnk" "$INSTDIR\Deinstallieren.exe"
  WriteRegStr HKCU "${UNKEY}" "DisplayName" "${APP}"
  WriteRegStr HKCU "${UNKEY}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "${UNKEY}" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegStr HKCU "${UNKEY}" "UninstallString" '"$INSTDIR\Deinstallieren.exe"'
  WriteRegDWORD HKCU "${UNKEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNKEY}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\${APP}.lnk"
  RMDir /r "$SMPROGRAMS\${APP}"
  Delete "$INSTDIR\${EXE}"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\Deinstallieren.exe"
  RMDir "$INSTDIR"
  DeleteRegKey HKCU "${UNKEY}"
  ; Spielstände (%APPDATA%\Godot\app_userdata\Kunterbunt City) bleiben absichtlich erhalten.
SectionEnd
