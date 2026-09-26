# PHASE 03 · Figuren & Haustiere (Grundsystem)
**Ziel:** Figuren, die man ziehen, hinsetzen, hinlegen und **Items richtig in die Hand geben** kann. Dazu ein Basis-Haustier.
**Voraussetzung:** Phase 02.
**Nicht in dieser Phase:** Editor-UI (Phase 04), NPC-KI (Phase 08).

## Aufgaben
| ID | Aufgabe |
|---|---|
| P03-T01 | `CharacterRig` aus Ebenen: Körper, Kopf, Haare hinten/vorne, Augen, Mund, Oberteil, Hose, Schuhe, **Arm hinten, Arm vorne, Hand vorne (eigene Ebene)**. Platzhalter-Teile passend zu `char_*`-Größen |
| P03-T02 | 3 Schablonen: `toddler` (90), `kid` (125), `adult` (172). Größe **nur** aus der Tabelle |
| P03-T03 | Posen: `stand`, `hold_one` (Arm vorne), `hold_two` (Arm vorne beidseitig), `sit`, `lie`. Wechsel mit kurzer Tween-Animation |
| P03-T04 | `HandSlot` (rechts/links): Item übergeben → Grip auf HandSlot (±0,5 cm), Rotation `hold_angle`, **Zeichenreihenfolge Arm < Item < Hand** (Tech-Spec §4.2) |
| P03-T05 | `SeatSlot`: Stuhl, Sofa, Bett (Pose `sit`/`lie`), Einrasten im Radius 30 cm, Sitzhöhe aus der Tabelle (Stuhl 45 cm). Items (Teddy) können ebenfalls sitzen |
| P03-T06 | Figur ziehen: am Körper greifen, hängt lustig am Griffpunkt (leichtes Pendeln), Absetzen auf dem Bodenband |
| P03-T07 | Emotionen: 6 Gesichter (fröhlich, lachend, überrascht, traurig, müde, verliebt), Tipp auf den Kopf wechselt; Reaktionen auf Essen (Mampf-Animation) |
| P03-T08 | Tiefen-Faktor gilt für Figuren genauso wie für Items (Test: Figur vorne und Tisch vorne behalten das Verhältnis) |
| P03-T09 | `PetNode` + einfaches Verhalten: sitzen, laufen, folgt der Figur, Tipp → Laut (über `AudioBus`-Limiter). Hund mittel 45 cm |
| P03-T10 | Szene „Küche Maßstab“ nachbauen wie `reference/kueche_stil_c_massstab.png`, mit den **echten Sprites aus `reference/sprites/`** (Figur-Sprite dort nur als Einzelbild) |

## Akzeptanzkriterien
- [ ] Pflicht-Tests aus Tech-Spec §6 angelegt und grün: `tests/test_hand.gd`
- [ ] Karotte in die Hand → Finger liegen über der Karotte, Karotte ≈ 20 cm (neben Kind 125 cm) – Screenshot
- [ ] Teddy auf dem Stuhl sitzt auf 45 cm Sitzhöhe
- [ ] Hund ist in jeder Tiefe kleiner als der Tisch (Test)
- [ ] Figur setzt sich auf Stuhl/Sofa, legt sich ins Bett
- [ ] Nachbau der Referenz-Küche wirkt proportional identisch (👤 Blick-Check)
- [ ] `check.sh` grün

## 👤 Mensch
**Erster Kindertest** (10 Minuten, 1–2 Kinder): Verstehen sie Anfassen, Hinsetzen, In-die-Hand-geben ohne Erklärung? Protokoll nach `docs/tests/P03_kindertest.md`.

## Startprompt
> Lies MASTERPROMPT.md, docs/06_TECH_SPEC.md §4.2–4.4 und docs/phasen/PHASE_03_FIGUREN_TIERE.md. Setze Phase 03 um. Kritisch: Grip-Punkt exakt auf die Hand, Hand-Ebene über dem Item, Größen nur aus der Tabelle. Phasenbericht und stoppen.
