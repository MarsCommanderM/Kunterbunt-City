# PHASE 07 · Vertical Slice „Zuhause & Garten“
**Ziel:** Ein kompletter Bereich in **finaler Qualität** (Stil C). Er ist der Maßstab für alle weiteren Bereiche.
**Voraussetzung:** Phasen 03, 05, 06.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P07-T01 | `data/areas/home.json`: 11 Szenen (Flur, Wohnzimmer, Küche, Eltern-SZ, 2 Kinderzimmer, Bad, Dachboden, Keller, Garage, Garten), Türen zwischen Räumen, Spawn Flur |
| P07-T02 | Pro Raum: Hintergrund (👤 generiert) eingemessen, Oberflächen, SeatSlots, Container, Fixtures |
| P07-T03 | 190 Items (≈ 65 Vorlagen + Varianten) als Item-JSON. Solange Grafik fehlt: Platzhalter. Jeder Eintrag mit `scale_ref` |
| P07-T04 | Möbel im Zuhause **bewegbar** (Ausnahme laut Welt-Doku). Tapete und Boden wählbar (12 + 12) |
| P07-T05 | Fixtures: Herd (an/aus, Topf blubbert), Ofen, Spüle (Wasser), Kühlschrank (Container), Badewanne (Schaum), Dusche, Toilette (Spülen-Sound), Waschmaschine, Licht-Schalter pro Raum, TV |
| P07-T06 | `RecipeSystem` + 25 Rezepte (Spiegelei, Toast, Smoothie, Pizza, Kuchen, Salat …) datengetrieben |
| P07-T07 | Garten: Pflanzen wachsen in 3 Stufen (Samen + Erde + Wasser), Gemüse ernten, Planschbecken, Baumhaus (SeatSlot oben, Leiter) |
| P07-T08 | Nachbarin am Zaun und Postbote (einfach, echte KI kommt in Phase 08) |
| P07-T09 | Audio: Musik (Tag), Ambiente pro Raum, Item-Sounds nach Material |
| P07-T10 | 6 Geheimnisse (Dachboden-Truhe, Maus im Keller …) → Sammel-Album |
| P07-T11 | Lineup `docs/tests/lineup_home.png` + Test-Szene pro Raum |

## Akzeptanzkriterien
- [x] Alle 11 Szenen begehbar, Wechsel über Türen
- [ ] 190 Items, 0 Maßstab-Fehler, 0 Seitenverhältnis-Warnungen bei echter Grafik
- [x] 25 Rezepte funktionieren (GUT je Rezept) – 26
- [ ] 60 FPS im vollsten Raum mit 250 Items (Desktop), ≥ 30 FPS Web auf Mittelklasse-Laptop
- [ ] 👤 **Kindertest** (2–3 Kinder, 15 Min.): keine Frust-Stellen, Protokoll in `docs/tests/`
- [x] `check.sh` grün

## Startprompt
> Lies MASTERPROMPT.md, docs/05_WELT_UND_BEREICHE.md §1 und docs/phasen/PHASE_07_SLICE_ZUHAUSE.md. Baue den Bereich Zuhause komplett. Fehlende Grafik = Platzhalter, nie Größen raten. Phasenbericht und stoppen.
