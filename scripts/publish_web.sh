#!/usr/bin/env bash
# Kunterbunt City – Web-Build exportieren und auf GitHub Pages veröffentlichen.
#
#   bash scripts/publish_web.sh
#
# Ergebnis: https://marscommanderm.github.io/Kunterbunt-City/ (1–2 min Build).
# Voraussetzungen: scripts/setup_dev_linux.sh lief einmal durch (Godot + Web-Templates),
# Repo öffentlich, Push-Recht auf origin (Branch gh-pages).
set -euo pipefail
cd "$(dirname "$0")/.."

GODOT_BIN="${GODOT:-$(command -v godot || command -v godot4 || true)}"
[ -n "$GODOT_BIN" ] || GODOT_BIN="$HOME/.local/godot/godot"
[ -x "$GODOT_BIN" ] || { echo "❌ Godot nicht gefunden – erst scripts/setup_dev_linux.sh"; exit 1; }

echo "▶ Web-Export …"
"$GODOT_BIN" --headless --export-release "Web" export/web/index.html >/dev/null

REPO="$PWD"
echo "▶ gh-pages aktualisieren …"
git fetch origin gh-pages:refs/heads/gh-pages 2>/dev/null || true
WORK="$(mktemp -d)"
trap 'git worktree remove --force "$WORK" 2>/dev/null || true' EXIT
git worktree add --force "$WORK" gh-pages >/dev/null
(
  cd "$WORK"
  find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  cp "$REPO"/export/web/index.html "$REPO"/export/web/index.js "$REPO"/export/web/index.wasm \
     "$REPO"/export/web/index.pck "$REPO"/export/web/index.png "$REPO"/export/web/index.icon.png \
     "$REPO"/export/web/index.audio.worklet.js "$REPO"/export/web/index.audio.position.worklet.js .
  git add -A
  REV="$(git -C "$REPO" rev-parse --short HEAD)"
  if git diff --cached --quiet; then
    echo "  (kein Unterschied – Build schon live)"
  else
    git -c user.name="MarsCommanderM" \
        -c user.email="258017001+MarsCommanderM@users.noreply.github.com" \
        commit -q -m "Web-Build: $REV"
    git push origin gh-pages
    echo "  ✔ gepusht (Web-Build: $REV) – Seiten-Build dauert ~1 Min."
  fi
)
echo "✅ https://marscommanderm.github.io/Kunterbunt-City/"
