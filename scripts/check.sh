#!/usr/bin/env bash
# Kunterbunt City – ALLE Qualitäts-Tore (MASTERPROMPT §8). Rot = nicht committen.
# Godot-Pfad: Umgebungsvariable GODOT, sonst "godot" / "godot4" im PATH.
set -uo pipefail
cd "$(dirname "$0")/.."

PY="${PYTHON:-python3}"; command -v "$PY" >/dev/null || PY=python
GODOT_BIN="${GODOT:-$(command -v godot || command -v godot4 || true)}"
fail=0
step() { printf '\n\033[1m▶ %s\033[0m\n' "$1"; }

step "1/3 Maßstab"
"$PY" tools/validate_scale.py || fail=1

step "2/3 Tool-Tests (pytest)"
"$PY" -m pytest tools/tests -q || fail=1

step "3/3 Godot-Tests (GUT)"
if [ -z "$GODOT_BIN" ]; then
  echo "❌ Godot nicht gefunden – GODOT=/pfad/zu/godot setzen"; fail=1
else
  "$GODOT_BIN" --headless --import >/dev/null 2>&1 || true   # Klassen/Assets registrieren
  out=$("$GODOT_BIN" --headless -s addons/gut/gut_cmdln.gd -gconfig=res://.gutconfig.json 2>&1); code=$?
  echo "$out" | grep -E "^(Totals|Scripts|Tests|Passing|Failing|Risky|Pending|Asserts|---- )|\[Failed\]|FAILED|SCRIPT ERROR|Parse Error|All tests passed" | sed 's/\x1b\[[0-9;]*m//g'
  if [ $code -ne 0 ] || echo "$out" | grep -qE "SCRIPT ERROR|Parse Error"; then fail=1; fi
fi

echo
if [ $fail -eq 0 ]; then echo "✅ check.sh: alles grün"; else echo "❌ check.sh: ROT – nicht committen"; fi
exit $fail
