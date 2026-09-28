#!/usr/bin/env bash
# Baut alle Release-Downloads nach export/release/ (lokal und in .github/workflows/release.yml gleich).
# Voraussetzung: godot (4.7.2) + Export-Vorlagen (tools/dev/fetch_web_templates.py VERSION --desktop), makensis.
# Aufruf: bash scripts/build_release.sh 1.0.0
set -euo pipefail
cd "$(dirname "$0")/.."
VER="${1:-$(grep -oP 'config/version="\K[^"]+' project.godot)}"
OUT=export/release
rm -rf export/windows export/linux export/macos export/web "$OUT"
mkdir -p export/windows export/linux export/macos export/web "$OUT"
godot --headless --import >/dev/null 2>&1 || true
godot --headless --export-release "Windows" export/windows/KunterbuntCity.exe
godot --headless --export-release "Linux" export/linux/KunterbuntCity.x86_64
godot --headless --export-release "macOS" export/macos/KunterbuntCity.zip
godot --headless --export-release "Web" export/web/index.html
# Windows: Installer (Desktop-Verknüpfung) + ohne Installation
(cd installer && makensis -V2 -DVERSION="$VER" -DSRC=../export/windows "-DOUT=../$OUT/KunterbuntCity-Setup-$VER.exe" kunterbunt.nsi)
(cd export/windows && cp ../../assets/app/icon.ico . && zip -q -9 "../../$OUT/KunterbuntCity-Windows-$VER.zip" KunterbuntCity.exe icon.ico)
# Linux: Programm + Symbol + Installationsskript (legt Desktop-Symbol an)
cp assets/app/icon.png installer/linux/installieren.sh export/linux/
chmod +x export/linux/KunterbuntCity.x86_64 export/linux/installieren.sh
tar -C export -czf "$OUT/KunterbuntCity-Linux-$VER.tar.gz" --transform 's,^linux,KunterbuntCity,' linux
cp export/macos/KunterbuntCity.zip "$OUT/KunterbuntCity-macOS-$VER.zip"
(cd export/web && zip -q -9 -r "../../$OUT/KunterbuntCity-Web-$VER.zip" .)
ls -la "$OUT"
