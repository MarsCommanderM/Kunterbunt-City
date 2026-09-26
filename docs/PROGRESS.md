# PROGRESS · Gedächtnis des Agenten
> Wird vom Agenten nach **jeder Task** aktualisiert. Neueste Einträge oben im Log. Nie löschen, nur ergänzen.

## Status
| Feld | Wert |
|---|---|
| Aktuelle Phase | **02 · Item-System & Drag-and-Drop** (wartet auf 👤 OK für Phase 01) |
| Nächste Task | P02-T01 |
| Letzter grüner check.sh | 2026-09-26 (Phase 01) |
| Version | 0.0.2 |

## Phasen
| Phase | Status | Bericht |
|---|---|---|
| 00 Setup | ✅ fertig | Log 2026-09-26 |
| 01 Welt-Maßstab | ✅ fertig (👤 Blick-Check offen) | Log 2026-09-26 |
| 02 Items & Drag | ⏳ | – |
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

## Log
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
