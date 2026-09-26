# PHASE 01 · Welt-Maßstab, Raum & Kamera
**Ziel:** Eine Welt in **Zentimetern**, in der jede Größe automatisch stimmt. Dazu ein Test-Raum, in dem man scrollt und zoomt.
**Voraussetzung:** Phase 00 abgeschlossen.
**Nicht in dieser Phase:** Drag & Drop, Figuren-Logik.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P01-T01 | `src/core/units.gd`: Konstanten und Helfer (cm ↔ Einheiten = 1:1, `depth_factor()`, `camera_zoom_for_height()`) + GUT-Tests |
| P01-T02 | `ItemDB` lädt `data/scale_table.json` und stellt `get_scale(ref) -> Dictionary` bereit. Unbekannte Referenz = klarer Fehler |
| P01-T03 | `src/world/room.gd` + `room.tscn`: Maße aus `data/areas/*.json` (Breite/Höhe cm), Kinder-Nodes nach Tech-Spec §3.2/MASTERPROMPT §6 |
| P01-T04 | `src/world/world_camera.gd`: sichtbare Höhe 300 cm (Standard), Pinch-Zoom und Mausrad (Grenzen aus Raumdaten), horizontales Wisch-Scrollen mit Trägheit, Grenzen = Raumränder |
| P01-T05 | `src/world/floor_band.gd`: hintere und vordere Bodenlinie, `depth_factor(y)` max. 1,12, Visualisierung im Debug-Modus |
| P01-T06 | `src/world/surface.gd`: Oberfläche (Typ, x-Bereich, Höhe cm, Tiefe), Debug-Zeichnung |
| P01-T07 | `data/areas/test_kitchen.json` + Test-Raum: Hintergrund `reference/raw_kitchen_bg.png`, **eingemessen** mit Arbeitsplatte 90 cm (px 434 → 600, Maßstab-Bibel §6), Bodenband, Arbeitsplatte als Surface |
| P01-T08 | `tools/asset_pipeline/calibrate_bg.py` (erste Version, Ordner anlegen): liest `calibration` aus der Raum-JSON, skaliert den Hintergrund auf 8 px/cm, schreibt nach `assets/backgrounds/…` |
| P01-T09 | **Maßstab-Testszene** `src/debug/scale_test.tscn`: Platzhalter-Rechtecke für `char_child`, `pet_dog_medium`, `home_table_dining`, `food_apple`, `toy_football` automatisch aus der Tabelle + cm-Lineal |
| P01-T10 | Debug-Overlay (Taste F3 / 3-Finger-Tipp in Debug-Builds): Raster 10 cm, Oberflächen, Bodenband, FPS |

## Akzeptanzkriterien
- [ ] Pflicht-Tests aus Tech-Spec §6 angelegt und grün: `tests/test_depth.gd`
- [ ] In der Testszene: Hund (45) < Tisch (75) < Arbeitsplatte (90) < Kind (125), am Lineal nachmessbar
- [ ] Kamera zeigt 300 cm Höhe bei Standard-Zoom (Test: Sichtbereich ±2 cm)
- [ ] Tiefen-Faktor: hinten 1,00, vorne 1,12, nie größer (GUT-Test)
- [ ] Der eingemessene Hintergrund hat die Arbeitsplatte auf 90 cm ±2 cm
- [ ] Scrollen und Zoomen funktionieren mit Maus **und** Touch-Emulation
- [ ] `check.sh` grün

## Startprompt
> Lies MASTERPROMPT.md, docs/02_MASSSTAB_BIBEL.md, docs/06_TECH_SPEC.md und docs/phasen/PHASE_01_WELT_MASSSTAB.md. Setze Phase 01 um. Keine Größe darf hart codiert sein – alles aus data/scale_table.json. Screenshots der Maßstab-Testszene nach docs/tests/P01/ speichern. Phasenbericht und stoppen.
