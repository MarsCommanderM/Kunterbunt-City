# PHASE 04 · Charakter- & Haustier-Editor
**Ziel:** Beim ersten Start **muss** eine eigene Figur erstellt werden. Danach unbegrenzt Figuren und Haustiere erstellen, bearbeiten und löschen.
**Voraussetzung:** Phase 03.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P04-T01 | Datenformat `data/character_parts/*.json`: Slot (hair_front, hair_back, eyes, mouth, top, bottom, shoes, accessory, aid), Schablone, Farbzonen (bis 3), Sprite-Pfade, Tags |
| P04-T02 | Figur-Datenmodell `CharacterData` (Schablone, Hautton, Teile + Farben, Name, Stimme 1–8) ↔ JSON, Speichern über `SaveSystem` |
| P04-T03 | Editor-UI (`src/ui/character_editor/`): links große Vorschau (reagiert mit Emotionen), rechts Kategorien als **Symbole**, unten Farbpalette. **Kein Lese-Zwang** |
| P04-T04 | Umfärben per Shader (Farbzonen-Maske R/G/B im Teil-Sprite → Farbe aus Palette) |
| P04-T05 | 🎲 Zufallsknopf (würfelt stimmige Kombination), 5 Outfit-Plätze pro Figur |
| P04-T06 | Namens-Auswahl: 200 Namen als Bild-Kacheln + Würfel. Freie Eingabe **nur hinter dem Eltern-Tor**, lokaler Wortfilter |
| P04-T07 | **Pflicht-Ablauf:** erster Start → Editor → „Fertig“-Haken aktiv erst, wenn Schablone + Hautton gewählt sind → danach Startmenü |
| P04-T08 | Figuren-Galerie: unbegrenzt, Ordner (Familie, Freunde …), duplizieren, löschen (mit Sicherheitsabfrage per Symbol) |
| P04-T09 | Haustier-Editor: Tierart (Tabelle `pet_*`), Fell/Farbe, Muster, Halsband, Charakterzug (verspielt/verschlafen/neugierig/verfressen/schüchtern) |
| P04-T10 | Platzhalter-Teile: je Slot 5 Varianten als Platzhalter (echte Stil-C-Teile kommen über die Pipeline in Phase 06/07) |

## Akzeptanzkriterien
- [ ] Ohne eigene Figur ist kein Bereich betretbar (Test)
- [ ] 100 Figuren speichern/laden ohne Ruckeln
- [ ] Umfärben funktioniert pro Teil mit 3 Zonen
- [ ] Größe der Figur hängt nur von der Schablone ab (Kind immer 125 cm)
- [ ] Editor ist ohne Lesen bedienbar (👤 Kindertest mit 1 Kind)
- [ ] `check.sh` grün

## 👤 Mensch
Körper-Schablonen im Stil C generieren (Stil-Guide §3C) → erst in Phase 06 durch die Pipeline.

## Startprompt
> Lies MASTERPROMPT.md und docs/phasen/PHASE_04_EDITOR.md. Setze Phase 04 um. Pflicht-Erstellung beim ersten Start, keine freie Texteingabe im Kinderbereich, Figurengröße nur aus der Schablone. Phasenbericht und stoppen.
