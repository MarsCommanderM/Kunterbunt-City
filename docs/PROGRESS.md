# PROGRESS · Gedächtnis des Agenten
> Wird vom Agenten nach **jeder Task** aktualisiert. Neueste Einträge oben im Log. Nie löschen, nur ergänzen.

## Status
| Feld | Wert |
|---|---|
| Aktuelle Phase | **03 · Figuren & Tiere** |
| Nächste Task | P03-T01 |
| Letzter grüner check.sh | 2026-09-26 (Phase 02) |
| Version | 0.0.3 |

## Phasen
| Phase | Status | Bericht |
|---|---|---|
| 00 Setup | ✅ fertig | Log 2026-09-26 |
| 01 Welt-Maßstab | ✅ fertig (👤 Blick-Check offen) | Log 2026-09-26 |
| 02 Items & Drag | ✅ fertig (👤 Anfass-Gefühl + GPU-FPS offen) | Log 2026-09-26 |
| 03 Figuren & Tiere | ⏳ | – |
| 04 Editor | ⏳ | – |
| 05 Menü & Speichern | ⏳ | – |
| 06 Asset-Pipeline | ⏳ | – |
| 07 Slice Zuhause | ⏳ | – |
| 08 NPC-/Tier-KI | ⏳ | – |
| 09 MVP v0.1 | ⏳ | – |
| 10a–10h Content | ⏳ | – |
| 11 Politur 1.0 | ⏳ | – |

Legende: ⏳ offen · 🔨 in Arbeit · ✅ fertig · ⛔ blockiert

## Bereits vorhanden (vor Phase 00)
- `data/scale_table.json` (155 Größen), `data/scale_rules.json` (43 Regeln), `tools/validate_scale.py` → grün
- `data/items/home_kitchen_demo.json` (18 Beispiel-Items)
- `reference/`: Stil-C-Referenz, Maßstab-Küche, Lineup, 19 Demo-Sprites, Demo-Pipeline

## Offene Fragen an den Menschen 👤
- (keine)

## Messwerte
| Datum | Phase | Test | Ergebnis |
|---|---|---|---|
| 2026-09-26 | 00 | check.sh | Maßstab ✅ · pytest 5/5 ✅ · GUT 7/7 ✅ |
| 2026-09-26 | 00 | Web-Export (leere Szene) | ✅ 39 MB, index.pck 41 KB |
| 2026-09-26 | 01 | check.sh | Maßstab ✅ · pytest 9/9 ✅ · GUT 47/47 ✅ |
| 2026-09-26 | 01 | Einmessen Test-Küche | Arbeitsplatte 90,0 cm · Regale 153/194 cm · Bodenband 0…73,2 cm · Raum 716×313 cm |
| 2026-09-26 | 01 | Web-Export mit Test-Küche | ✅ index.pck 3,2 MB |
| 2026-09-26 | 02 | check.sh | Maßstab ✅ (155 Einträge, 61 Items) · pytest 15/15 ✅ · GUT 129/129 ✅ (850 Asserts) |
| 2026-09-26 | 02 | Leistung 250 Items + 1 Item im Dauer-Drag (`p02_perf_runner.gd`) | headless (nur Logik): **145 FPS** (6,9 ms/Frame) · llvmpipe-Software-Rendering 2 Kerne: 5,7 FPS @1080p / 11,2 @720p (61 Items: 17,7 @720p → Engpass ist das Software-Rendering, nicht die Items) · 613 Draw-Calls · 1040 Nodes · Greifen 0,7–0,9 ms, Zielsuche 1,1–2,0 ms. **GPU-60-FPS muss 👤 auf echter Hardware bestätigen.** |

## Log
### 2026-09-26 · Phase 02 · Item-System & Drag-and-Drop ✅
- Erledigt: P02-T01…T12.
  - `tools/make_placeholders.py`: 155 Platzhalter, 8 px/cm, randlos, bit-genau reproduzierbar
  - `ItemDefinition` + `ItemDB`-Item-Laden mit Validierung (61 Items: 18 echte Stil-C-Sprites + 43 Platzhalter aus `tools/dev/make_test_items.py`)
  - `ItemNode`: Größe exakt aus der Tabelle, Alpha-Treffertest, Mindest-Tippfläche 48 dp, Kontaktschatten, Anheben 6 cm
  - `DragController` (PRESS/LIFT/DRAG/DROP, 80 ms/8 px, Multitouch 3, Tippen)
  - `Placement`: Flächen, Tische, Stapel, Behälter, S-11, Regal-Abstand, Breite, Ablehnung → Boden
  - `UndoStack` (30) + gezeichneter `UndoButton`
  - `AudioBus.play_sfx/play_item_sfx` (Material je Kategorie) + 11 synthetische CC0-Sounds (`tools/make_sfx.py`)
  - `ItemSpawner`, Test-Küche `src/debug/sandbox_kitchen.tscn` (alle 61 Items, Button im Hauptmenü)
- Tests (neu):
  - GUT: test_drag_drop (Pflicht), test_scale (Pflicht), test_placement, test_container_stack, test_undo, test_item_definition, test_item_db_items, test_item_node, test_audio, test_perf
  - pytest: test_placeholders, test_sfx
- Beweis: `docs/tests/P02/*.jpg`, 9 Bilder. Erzeugt durch `tools/godot/p02_scenario_runner.gd`, das die Küche über dieselbe API wie ein Finger bedient:
  - Anheben, Abstellen auf Tisch und Boden
  - Kühlschrank und Rucksack offen
  - Klotz-Turm (4) und Tellerstapel (5) im Zoom
  - Stuhl auf der Arbeitsplatte → abgelehnt
  - 4× rückgängig
  - Debug-Flächen
- Von den Tests gefundene und behobene Fehler:
  - Greif-Versatz wurde beim Anheben statt beim Antippen berechnet; das Item sprang.
  - Wischen über den Kühlschrank öffnete ihn.
  - Im Tellerstapel war nur der oberste Teller greifbar (48-dp-Flächen überdeckten sich).
  - Ein Behälter im Kühlschrank verlor gegen den Kühlschrank.
  - `"grip": null` im JSON ließ das Laden abstürzen.
  - Behälter-Inhalt stand über die Innenfläche hinaus; jetzt Regal-Layout in echter Größe.
- Entscheidungen:
  - `ItemNode` wird per Code gebaut, nicht als `item_node.tscn`. Das ist schneller beim Massen-Spawnen, und es gibt nur eine Quelle.
  - Sounds werden per NumPy-Synthese erzeugt statt jsfxr: reproduzierbar per Skript, 0 €.
  - Tisch-Oberkante aus dem Sprite gemessen (`surface_frac_y`).
  - Beweisbilder als JPG; `docs/.gdignore`, damit Godot die Doku nicht importiert.
- Werkzeug neu: `tools/godot/run.gd -- <runner.gd> [args]`. Das ist der Starter für Skript-Abläufe, weil `-s`-Skripte vor den Autoloads kompiliert werden.
  - Beweisbilder: `xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- res://tools/godot/p02_scenario_runner.gd docs/tests/P02`
  - Leistung: `… -- res://tools/godot/p02_perf_runner.gd 250`
- 👤 offen:
  - Selbst spielen (Test-Küche im Hauptmenü): Fühlt sich Anheben und Abstellen gut an?
  - 250-Items-FPS auf echter GPU messen, mit demselben Befehl.
- Nächste Task: P03-T01
### 2026-09-26 · Phase 01 · Welt-Maßstab, Raum & Kamera ✅
- Erledigt: P01-T01…T10.
  - `Units` (Tiefen-Faktor hart auf 1,12 begrenzt, Zoom-/Sprite-Formeln)
  - `ItemDB.get_scale/height_cm/width_cm` (unbekannte Referenz = Fehler, scale_mul 0,7–1,3)
  - `Room` + `room.tscn` aus `data/areas/*.json`, `FloorBand`, `Surface`, `WorldCamera` (300 cm, Pinch/Mausrad/Trackpad, Trägheit, Grenzen = Raum ∩ Hintergrund)
  - `tools/asset_pipeline/calibrate_bg.py` (Kacheln ≤ 2048 px, schreibt cm-Werte in die Raum-JSON)
  - Test-Küche eingemessen, Maßstab-Testszene `src/debug/scale_test.tscn` (Platzhalter nur aus der Tabelle + cm-Lineal)
  - Debug-Overlay (F3 / 3-Finger-Tipp): 10-cm-Raster, Oberflächen, Bodenband, FPS, Zeiger in cm
- Tests: check.sh ✅ (neu: test_depth, test_units, test_item_db, test_room, test_camera inkl. simulierter Maus/Touch/Pinch, test_scale_scene; pytest test_calibrate_bg).
- Blick-Check: Screenshots `docs/tests/P01/scale_test.png` + `scale_test_debug.png` (echtes OpenGL-Rendering). Apfel ≪ Fußball < Hund < Tisch < Arbeitsplatte < Kind ✅.
- Entscheidungen:
  - `background` in der Raum-JSON zeigt auf `<raum>.bg.json` (Kacheln + Ursprung), Tech-Spec angepasst.
  - Test-Küche mit 4 px/cm statt 8: Die Quelle hat nur 1,84 px/cm, mehr Hochskalieren bringt nichts. Das Tool warnt ab ×2,2.
  - Welt-Text wird 6-fach gerendert und verkleinert (`WorldText`), damit er beim Zoom scharf bleibt.
- Werkzeug neu: `tools/godot/screenshot.gd`. Aufruf (Linux ohne Display mit xvfb-run): `godot --resolution 1920x1080 -s tools/godot/screenshot.gd -- res://src/debug/scale_test.tscn out.png [debug]`
- Bekannt: Der KI-Hintergrund zeigt 313 cm Wand. Dadurch wirkt der Raum „hoch“, die Größen stimmen aber. Neue Hintergründe laut Stil-Guide mit ~260 cm Raumhöhe generieren.
- Nächste Task: P02-T01 (nach 👤 OK)

### 2026-09-26 · Phase 00 · Setup & Werkzeuge ✅
- Erledigt: P00-T01…T12. Godot 4.7.2 (Compatibility, 1920×1080, canvas_items/expand, Querformat, Touch≠Maus), Ordner nach §4, GUT 9.6.1, 7 Autoload-Gerüste, Einstiegsszene `src/main.tscn`, Export-Presets (Web ohne Threads, Android ohne Internet-Recht, Win/Linux/macOS), `scripts/check.sh` + `check.ps1`, CI-Workflow, requirements.txt, CREDITS.
- Tests: check.sh ✅. Gegenprobe: absichtlich eingebauter Fehltest + `HTTPRequest` in src → check.sh ROT ✅ (Tore greifen).
- Entscheidungen: GUT-Aufruf über `.gutconfig.json`; `reference/`, `tools/`, `tests/`, `docs/`, `addons/gut/` werden nicht exportiert; `data/**/*.json` wird explizit exportiert.
- Hinweis 👤: CI-Workflow braucht beim Pushen einen Token mit Workflow-Recht.
- Nächste Task: P01-T01
<!-- Format:
### JJJJ-MM-TT · P0X-TYY · Titel
- Erledigt: …
- Tests: check.sh ✅/❌ (Details)
- Probleme/Entscheidungen: …
- Nächste Task: …
-->
