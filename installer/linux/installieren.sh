#!/bin/sh
# Kunterbunt City – Installation unter Linux (ohne root): kopiert das Spiel nach ~/.local/share/KunterbuntCity
# und legt ein Symbol im Anwendungsmenü und auf dem Desktop an. Aufruf: ./installieren.sh
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.local/share/KunterbuntCity"
mkdir -p "$DEST" "$HOME/.local/share/applications"
cp "$HERE/KunterbuntCity.x86_64" "$HERE/icon.png" "$DEST/"
chmod +x "$DEST/KunterbuntCity.x86_64"
cat > "$HOME/.local/share/applications/kunterbunt-city.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Kunterbunt City
Comment=Digitales Puppenhaus – kostenlos, ohne Werbung, ohne Datensammlung
Exec="$DEST/KunterbuntCity.x86_64"
Icon=$DEST/icon.png
Terminal=false
Categories=Game;KidsGame;
EOF
DESK="$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")"
if [ -d "$DESK" ]; then
  cp "$HOME/.local/share/applications/kunterbunt-city.desktop" "$DESK/"
  chmod +x "$DESK/kunterbunt-city.desktop"
  gio set "$DESK/kunterbunt-city.desktop" metadata::trusted true 2>/dev/null || true
fi
echo "Fertig! Kunterbunt City liegt jetzt auf dem Desktop und im Anwendungsmenü."
