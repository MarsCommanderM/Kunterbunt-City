# PHASE 04b · Figuren-Neubau im Stil „großer Kopf“
**Anlass:** Test im Browser (27.09.2026, 👤): Figuren, Figuren-Editor und Tier-Editor sahen unbrauchbar aus
(weiße Haut, graue Kastenkleidung, graue Platzhalter). Zielbild: Stil-Vorlage „C“ (Familie mit großen Köpfen).
**Entscheidungen des Menschen:** großer Kopf · Grafik als Vektor im Code · 1000+ wählbare Teile (Editor + Welt) ·
Räume starten leer, eingerichtet wird über einen Katalog · alle Icons neu im selben Stil.
**Keine fremden Figuren/Motive kopieren** (R-09) – eigener Stil in derselben Art.

## Aufgaben
| ID | Aufgabe | Status |
|---|---|---|
| P04b-T01 | Vektor-Zeichenkern `tools/chibi/vec.py` (Bézier/Catmull-Rom, Kontur per Abstands-Transformation, Glas, Naht, schnelle Ausschnitte) | ✅ |
| P04b-T02 | Körper, Gesicht (8 Augen, 13 Münder), 16 Frisuren, 14 Oberteile, 8 Unterteile (+ sitzend), 9 Schuhe, 12 Accessoires, 6 Hilfsmittel | ✅ |
| P04b-T03 | `tools/make_chibi_parts.py`: alle Teile × 4 Schablonen (Kleinkind, Kind, **Teen neu**, Erwachsene), Katalog + Aliase für alte IDs | ✅ |
| P04b-T04 | Neue Proportionen in `templates.json`, S-03 + Stil-Guide angepasst | ✅ |
| P04b-T05 | Shader mit Tinte (+ Muster-Vorbereitung), Farben je Ebene (Haut+Wangen, Haar+Glanz, nackte Beine = Haut), Haare hinten hinter dem Körper, Liegen mit ganzem Körper | ✅ |
| P04b-T06 | Editor: echte Vorschaubilder, Farbkreise, Symbole statt Zahlen, Teen wählbar | ⏳ |
| P04b-T07 | Tiere im selben Stil neu | ⏳ |
| P04b-T08 | Alle Icons/Symbole im Stil neu | ⏳ |
| P04b-T09 | Item-Bibliothek (hunderte Items, Farbvarianten) + Katalog in jedem Raum | ✅ |
| P04b-T10 | Zustände (Schränke/Schubladen auf, Geräte an/aus mit Animation), Kochen mit Rezepten, Großgeräte, gekochte Speisen, > 1000 Katalog-Items | ✅ |
| P04b-T11 | Mehr Spiel: Grill, Lagerfeuer, Kasse, Werkstatt-Arbeiten, weitere Rezepte | ⏳ |

## Akzeptanzkriterien
- [x] Alle Größen aus der Tabelle, Körper-Größe unabhängig von Teilen (`test_rig_builds_with_every_variant`)
- [x] Alte Speicherstände laden (alte Varianten-IDs bleiben oder haben Aliase)
- [x] Beweisbilder aus dem echten Spiel: `docs/tests/P04/p04_0{1,2,3}_*.jpg`
- [ ] 👤 Blick-Check gegen Zielbild C
- [ ] `check.sh` grün nach jeder Task
