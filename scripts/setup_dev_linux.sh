#!/usr/bin/env bash
# Reproduzierbare Entwicklungsumgebung (Linux x86_64) für Kunterbunt City – alles kostenlos.
# Installiert: Godot (headless-fähig) nach ~/.local/godot, Web-Export-Templates,
# Python-Pakete, optional Xvfb (für Screenshots ohne Bildschirm, braucht sudo).
# Danach:  export GODOT=~/.local/godot/godot && bash scripts/check.sh
set -euo pipefail
cd "$(dirname "$0")/.."
GODOT_VERSION="${GODOT_VERSION:-4.7.2}"
DEST="$HOME/.local/godot"

if [ ! -x "$DEST/godot" ] || ! "$DEST/godot" --headless --version 2>/dev/null | grep -q "^${GODOT_VERSION}"; then
  echo "▶ Godot ${GODOT_VERSION} laden …"
  mkdir -p "$DEST"
  curl -sSL -o /tmp/godot.zip "https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}-stable/Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip"
  unzip -oq /tmp/godot.zip -d /tmp/godot_unz && mv /tmp/godot_unz/Godot_v${GODOT_VERSION}-stable_linux.x86_64 "$DEST/godot" && rm -rf /tmp/godot.zip /tmp/godot_unz
  chmod +x "$DEST/godot"
fi
"$DEST/godot" --headless --version | tail -1

TPL="$HOME/.local/share/godot/export_templates/${GODOT_VERSION}.stable"
if [ ! -f "$TPL/web_nothreads_release.zip" ]; then
  echo "▶ Web-Templates (nur ~20 MB statt 1,3 GB) …"
  python3 tools/dev/fetch_web_templates.py "$GODOT_VERSION" "$TPL"
fi

echo "▶ Python-Pakete …"
python3 -m pip install -q -r tools/requirements.txt 2>&1 | grep -v "notice" || true

if ! command -v xvfb-run >/dev/null; then
  if sudo -n true 2>/dev/null; then
    echo "▶ Xvfb (Screenshots ohne Bildschirm) …"
    sudo apt-get install -y -qq xvfb >/dev/null 2>&1 || (sudo apt-get update -qq >/dev/null && sudo apt-get install -y -qq xvfb >/dev/null)
  else
    echo "ℹ️  Xvfb nicht installiert (kein sudo) – Screenshots nur mit echtem Bildschirm"
  fi
fi

echo "▶ Projekt importieren …"
"$DEST/godot" --headless --import >/dev/null 2>&1 || true
echo "✅ Fertig.  export GODOT=$DEST/godot  &&  bash scripts/check.sh"
