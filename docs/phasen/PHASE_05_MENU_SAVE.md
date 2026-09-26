# PHASE 05 · Startmenü (Stadtkarte), Speichern, Bereichswechsel
**Ziel:** Der komplette Spielfluss: App-Start → (Pflicht-Editor) → Stadtkarte mit einem Button pro Bereich → Spawn im Bereich → zurück zur Karte. Alles wird gespeichert.
**Voraussetzung:** Phase 04.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P05-T01 | Splash (max. 3 s, überspringbar) → Prüfung „eigene Figur vorhanden?“ → Editor oder Stadtkarte |
| P05-T02 | **Stadtkarte** (`src/ui/main_menu/`): 11 große Bereichs-Buttons (mind. 120×120 px @1080p) mit Bild, Symbol und eigenem Sound. Bereiche ohne Inhalt: sichtbar, aber mit einer freundlichen „Baustelle“-Animation statt Schloss |
| P05-T03 | Umschaltbar: **Karte** (illustriert) / **Raster** (übersichtlich für Kleine) |
| P05-T04 | Oben: Figuren-Button, Rucksack-Button, Album-Button, Eltern-Button (Eltern-Tor) |
| P05-T05 | `SceneRouter`: Ladebildschirm (< 2 s, mit Mini-Animation), Spawn am `spawn`-Punkt des Bereichs mit Ankunfts-Animation (Tür/Bus), aktive Figur + gewählte Haustiere |
| P05-T06 | In jedem Bereich: Karten-Button oben links (zurück), Rucksack unten rechts, Rückgängig |
| P05-T07 | **SaveSystem** komplett: Raumzustände, Figuren, Haustiere, Rucksack, Album. Autosave bei jeder Änderung (entprellt 2 s) + beim Verlassen. 3 Welt-Slots |
| P05-T08 | `save_version` + Migrationen + Tests mit Beispieldateien in `tests/fixtures/` |
| P05-T09 | **Eltern-Tor:** Rechenaufgabe mit Zahlen-Symbolen oder „3 Finger 3 Sekunden halten“ |
| P05-T10 | Einstellungen (hinter dem Tor): Lautstärken (Musik/Effekte/Tiere), große UI, reduzierte Animation, Sprache, Bereich zurücksetzen (🪄), Speicherstand exportieren/importieren (Datei, **ohne Internet**) |
| P05-T11 | Rucksack (Tech-Spec §4.7): 20 Plätze, Items wandern zwischen Bereichen |

## Akzeptanzkriterien
- [x] Pflicht-Tests angelegt und grün: `tests/test_save_migration.gd` (9) + Fixture `tests/fixtures/world_v1.json`
- [x] Kompletter Ablauf ohne Lesen bedienbar (Symbole + Umschalt-Knöpfe; 👤 End-Check mit Kind offen)
- [x] Bereichswechsel < 2 s (Messung: **160–190 ms**, `docs/tests/P05/p05_flow.json`)
- [x] App schließen und neu starten → alles exakt wie vorher (Positionen ±0,1 cm, Test `test_raumzustand_round_trip`)
- [x] Alte Speicherdatei (v1-Fixture) lädt nach einer Format-Änderung korrekt (Migration v1→v2)
- [ ] Web-Build speichert im Browser (Seite neu laden → Zustand bleibt) – 👤 Browser-Test offen
- [x] `check.sh` grün (Maßstab ✅ · pytest 75/75 · GUT 240/240)

## Startprompt
> Lies MASTERPROMPT.md, docs/06_TECH_SPEC.md §2–3.5 und docs/phasen/PHASE_05_MENU_SAVE.md. Setze Phase 05 um. Speicherstände sind heilig: Version + Migration + Tests. Phasenbericht und stoppen.
