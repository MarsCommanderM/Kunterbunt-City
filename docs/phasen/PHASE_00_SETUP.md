# PHASE 00 · Setup & Werkzeuge
**Ziel:** Ein sauberes, testbares Godot-Projekt, in dem jede spätere Phase sicher gebaut werden kann.
**Voraussetzung:** Godot 4.x (mind. 4.4) und Python 3.11+ installiert, Git eingerichtet (👤).
**Nicht in dieser Phase:** Gameplay, Grafik.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P00-T01 | `project.godot` anlegen: Name „Kunterbunt City“, Renderer **Compatibility**, 1920×1080, Stretch `canvas_items`/`expand`, Querformat |
| P00-T02 | Ordnerstruktur exakt nach MASTERPROMPT §4 anlegen (leere Ordner mit `.gitkeep`) |
| P00-T03 | `.gitignore` (Godot: `.godot/`, `*.import`-Cache nach Godot-Empfehlung, `export/`, Python: `__pycache__/`, `.venv/`) |
| P00-T04 | GUT installieren nach `addons/gut/` (aus dem offiziellen GUT-Repository, MIT, Version passend zu Godot 4), Plugin aktivieren, Beispieltest `tests/test_smoke.gd` |
| P00-T05 | Python: `tools/requirements.txt` (pillow, numpy, scipy, pytest, pyyaml), `tools/tests/test_validate_scale.py` testet `validate_scale.py` (grün mit Originaldaten, rot mit manipulierter Kopie „Hund 90 cm“) |
| P00-T06 | `tests/test_no_network.gd`: durchsucht alle `.gd` in `res://src` nach verbotenen Klassen (siehe Tech-Spec §6) |
| P00-T07 | Autoload-Gerüste anlegen (leer, typisiert, mit Doc-Kommentar): `Log`, `Settings`, `ItemDB`, `SaveSystem`, `Game`, `SceneRouter`, `AudioBus` |
| P00-T08 | Export-Presets: Web (Threads aus), Android (Querformat), Windows/Linux/macOS, `export/` ignoriert |
| P00-T09 | `scripts/check.sh` (+ `check.ps1` für Windows): führt Maßstab-Prüfer, pytest und GUT headless aus, Exit-Code ≠ 0 bei Fehlern |
| P00-T10 | Optional: `.github/workflows/ci.yml` führt `check.sh` headless aus (Godot per frei verfügbarem Docker-Image oder Download) |
| P00-T11 | `CREDITS.md` anlegen (GUT, Godot, Python-Pakete mit Lizenz) |
| P00-T12 | `docs/PROGRESS.md` ausfüllen |

## Akzeptanzkriterien
- [ ] `scripts/check.sh` läuft durch: Maßstab ✅, pytest ✅ (mind. 2 Tests), GUT ✅ (Smoke + No-Network)
- [ ] Projekt öffnet sich in Godot ohne Fehler/Warnungen im Output
- [ ] Web-Export lässt sich erzeugen (leere Szene) und lokal starten (`python3 -m http.server` im Export-Ordner)
- [ ] Ordnerstruktur = MASTERPROMPT §4

## Befehle
```bash
pip install -r tools/requirements.txt
bash scripts/check.sh
godot --headless --export-release "Web" export/web/index.html
```

## 👤 Mensch
Godot und Python installieren, GitHub-Repo anlegen (kostenlos), Web-Export-Templates in Godot herunterladen.

## Startprompt (kopieren)
> Lies MASTERPROMPT.md, docs/PROGRESS.md und docs/phasen/PHASE_00_SETUP.md. Setze Phase 00 Task für Task um. Nach jeder Task check.sh ausführen (sobald vorhanden), PROGRESS.md aktualisieren und committen. Am Ende Phasenbericht nach MASTERPROMPT §11 und stoppen.
