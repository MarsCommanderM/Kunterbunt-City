# PHASE 10 · Content-Wellen (Bereiche 4–11)
**Ziel:** Die restlichen 8 Bereiche, jeder nach **demselben Bereichs-Bauplan**. Jeder Bereich ist eine eigene Unterphase mit eigenem Bericht.

| Unterphase | Bereich | Welt-Doku |
|---|---|---|
| 10a | Schule & Pausenhof | §4 |
| 10b | Gesundheitszentrum | §5 |
| 10c | Freizeitbad | §6 |
| 10d | Rummelplatz | §7 |
| 10e | Sportzentrum | §8 |
| 10f | Eishalle | §9 |
| 10g | Zoo | §10 |
| 10h | Werkstatt | §11 |

## Bereichs-Bauplan (für jede Unterphase gleich)
| Schritt | Aufgabe |
|---|---|
| B-01 | `data/areas/<bereich>.json`: Szenen, Türen, Spawn, Kamera-Grenzen (Welt-Doku-Tabelle) |
| B-02 | Fehlende Größen in `scale_table.json` ergänzen (echte Maße recherchieren) + passende `lt`-Regeln (z. B. *Pinguin < Kleinkind*) |
| B-03 | Item-JSONs (Ziel-Anzahl laut Welt-Doku), zuerst mit Platzhaltern |
| B-04 | Fixtures + Oberflächen + SeatSlots + Container |
| B-05 | NPCs aus Rollen-Vorlagen (neue Rolle nur, wenn keine passt) |
| B-06 | Bereichs-Mechanik (z. B. Wasser im Bad, Eis-Reibung, Fahrgeschäfte, Tor-Erkennung, Fütterung) |
| B-07 | Rezepte/Interaktionen (mind. 10 pro Bereich) |
| B-08 | 👤 Grafik (Blätter + Hintergründe) → Pipeline → Lineup → Blick-Check |
| B-09 | Audio (Musik, Ambiente, Item-Sounds) |
| B-10 | 5–10 Geheimnisse fürs Album |
| B-11 | Performance-Messung + Kindertest-Kurzrunde |
| B-12 | Bereichs-Button auf der Stadtkarte von „Baustelle“ auf aktiv |

## Akzeptanzkriterien (pro Bereich)
- [ ] Szenen vollständig, Item-Ziel erreicht, 0 Maßstab-Fehler
- [ ] NPC-Garantie-Tests grün
- [ ] ≥ 10 Interaktionen/Rezepte getestet
- [ ] Performance im Budget
- [ ] Lineup-Bild + Test-Szene in `docs/tests/`
- [ ] `check.sh` grün

## Startprompt (Beispiel 10c)
> Lies MASTERPROMPT.md, docs/05_WELT_UND_BEREICHE.md §6 und docs/phasen/PHASE_10_CONTENT_WELLEN.md. Baue Unterphase 10c „Freizeitbad“ nach dem Bereichs-Bauplan B-01 bis B-12. Phasenbericht und stoppen.
