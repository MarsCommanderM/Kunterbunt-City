# PHASE 02 · Item-System & Drag-and-Drop
**Ziel:** Das **Kern-Gefühl**: Items anfassen, anheben, ziehen, sauber abstellen, stapeln, in Behälter legen, rückgängig machen. Es muss sich *perfekt* anfühlen.
**Voraussetzung:** Phase 01.
**Nicht in dieser Phase:** Figuren (Hand-Slot kommt in Phase 03), echte Grafik.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P02-T01 | `tools/make_placeholders.py`: pro `scale_table`-Eintrag ein PNG (8 px/cm, abgerundet, Kategorie-Farbe, Umriss, Kurzname + „20 cm“) nach `assets/placeholders/` + pytest |
| P02-T02 | `ItemDefinition` (Resource) + Laden aller `data/items/*.json` in `ItemDB`, Validierung (scale_ref, grip bei hold ≠ none, Sprite existiert, sonst Platzhalter) |
| P02-T03 | `ItemNode` (`item_node.tscn`): Sprite in Weltgröße (Maßstab-Bibel §1), Pivot-Offset, **Tippfläche min. 48 dp** (unabhängig von der Grafik), weicher Kontaktschatten |
| P02-T04 | `DragController`: Zustände IDLE/PRESS/LIFT/DRAG/DROP (Tech-Spec §4.1), Anheben mit Hüpf-Effekt, Multitouch bis 3 Items |
| P02-T05 | Drop-Logik: Oberfläche unter dem Item finden → Pivot exakt auf der Oberflächenhöhe; sonst sanft auf die nächste Fläche darunter fallen (≤ 0,4 s) |
| P02-T06 | Platzierungsregeln: `placement` + Größe (≤ 60 cm auf Tischen, S-11); passt ein Item nicht → federt zurück auf den Boden |
| P02-T07 | Stapeln (`stackable`, max. 8) und `Container` (Kühlschrank, Schrank, Tasche: Slots, öffnen/schließen per Tipp, verschachtelt max. 2 Ebenen) |
| P02-T08 | `UndoStack` (30 Schritte pro Raum) + Rückgängig-Button im HUD |
| P02-T09 | Tiefe: Items im Bodenband per y sortiert und skaliert (Faktor aus Phase 01) |
| P02-T10 | Test-Raum mit 60 Platzhalter-Items aus `data/items/home_kitchen_demo.json` + Platzhaltern (Küche) |
| P02-T11 | Sounds-Hooks: `pickup`/`drop` je Material (vorerst Platzhalter-Töne mit jsfxr erzeugt, CC0/eigene) |
| P02-T12 | Performance-Test: 250 Items im Raum, 60 FPS Desktop, Messung in PROGRESS.md |

## Akzeptanzkriterien
- [ ] Pflicht-Tests aus Tech-Spec §6 angelegt und grün: `tests/test_scale.gd` + `tests/test_drag_drop.gd`
- [ ] Apfel auf die Arbeitsplatte ziehen → steht exakt auf 90 cm (GUT ±0,5 cm)
- [ ] Apfel ins Leere loslassen → fällt auf den Boden, nie aus der Welt
- [ ] Ein Ei (6 cm) ist mit dem Finger gut greifbar (Tippfläche ≥ 48 dp)
- [ ] 3 Items gleichzeitig ziehbar (Touch-Emulation)
- [ ] Rückgängig stellt 30 Aktionen wieder her
- [ ] 250 Items → ≥ 60 FPS (Desktop)
- [ ] `check.sh` grün

## 👤 Mensch
Kurz selbst spielen: Fühlt sich Anheben/Abstellen gut an? Feedback in PROGRESS.md.

## Startprompt
> Lies MASTERPROMPT.md, docs/06_TECH_SPEC.md §4.1 und docs/phasen/PHASE_02_ITEMS_DRAGDROP.md. Setze Phase 02 um. Fokus: Das Anfassen muss sich weich und präzise anfühlen. Alle Größen aus der Tabelle, Platzhalter statt echter Grafik. Phasenbericht und stoppen.
