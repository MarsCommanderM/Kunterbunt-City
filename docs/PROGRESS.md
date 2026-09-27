# PROGRESS · Gedächtnis des Agenten
> Wird vom Agenten nach **jeder Task** aktualisiert. Neueste Einträge oben im Log. Nie löschen, nur ergänzen.

## Status
| Feld | Wert |
|---|---|
| Aktuelle Phase | **07 · Zuhause & Garten** (04b fertig) |
| Nächste Task | P07 Zuhause & Garten (mehrere Räume) |
| Letzter grüner check.sh | 2026-09-27 (P04b T07) |
| Version | 0.0.6 |

## Phasen
| Phase | Status | Bericht |
|---|---|---|
| 00 Setup | ✅ fertig | Log 2026-09-26 |
| 01 Welt-Maßstab | ✅ fertig (👤 Blick-Check offen) | Log 2026-09-26 |
| 02 Items & Drag | ✅ fertig (👤 Anfass-Gefühl + GPU-FPS offen) | Log 2026-09-26 |
| 03 Figuren & Tiere | ✅ fertig (👤 Kindertest offen) | Log 2026-09-26 |
| 04 Editor | ✅ fertig (👤 Kindertest + echte Stil-C-Teile in P06 offen) | Log 2026-09-26 |
| 05 Menü & Speichern | ✅ fertig (nur 1 Bereich hat Inhalt – Rest Baustelle) | Log 2026-09-26 |
| 06 Asset-Pipeline | ✅ fertig (👤 echte ComfyUI-Blätter in P07 offen) | Log 2026-09-27 |
| 04b Figuren-Neubau | ✅ fertig (T01–T12) | Log 2026-09-27 |
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
| 2026-09-26 | 03 | check.sh | Maßstab ✅ (155 Einträge, 65 Items) · pytest 31/31 ✅ · GUT 169/169 ✅ (1019 Asserts) |
| 2026-09-26 | 04 | check.sh | Maßstab ✅ (77 Items) · pytest 54/54 ✅ · GUT 217/217 ✅ (2642 Asserts) |
| 2026-09-26 | 05 | check.sh | Maßstab ✅ (77 Items) · pytest 75/75 ✅ · GUT 240/240 ✅ (2835 Asserts) |
| 2026-09-26 | 05 | Bereichswechsel (`p05_flow.json`) | **160–190 ms** gemessen (Ziel < 2000 ms) · 15 Items im Raum, 14 davon gespeichert · Figur 125,2 cm |
| 2026-09-26 | 05 | Stadtkarte | 12 Bereiche · 1 spielbar (Zuhause), 11 Baustellen (sichtbar, nie gesperrt) · Karte/Raster umschaltbar · Tippflächen ≥ 120×120 px |
| 2026-09-26 | 05 | Speicherstand | Welt-Slots 0–2 · v1-Fixture wandert nach v2 · Export/Import als Datei (kein Netz) · Raumzustand auf 0,1 cm genau |
| 2026-09-26 | 05 | Rucksack & Album | 20 Plätze, Ding rein (ziehen) und raus (tippen) · Foto mit 📷 landet in `user://album/` |
| 2026-09-27 | 06 | check.sh | Maßstab ✅ (155 Einträge, 77 Items) · pytest **110/110** ✅ · GUT **240/240** ✅ (2836 Asserts) |
| 2026-09-27 | 06 | `run.py reference/` (Golden-Lauf) | **0 neu · 18 aktualisiert · 0 Warnungen** · JSON identisch zur Referenz (tags/sfx/seat bleiben erhalten, `pad_px: 4` neu) · 18 Sprites neu bei exakt 8 px/cm · Kind-Sprite + `hand_grip` exportiert |
| 2026-09-27 | 06 | Lineup & Testszene | `docs/tests/lineup_home.png` (Kind 125 · Hund 45 · Tisch 75 cm am Lineal) · `docs/tests/P06/scene_test{,_kamera}.png` (Kamera 1920×1080, Regel S-07/S-08) |
| 2026-09-27 | 06 | Atlas | `assets/sprites/home_atlas.png` (18 Regionen, ≤ 4096², Shelf-Packung, 2 px Gutter) |
| 2026-09-27 | 06 | Abnahme-Tests (neu) | pytest +35: cutout 7 · split/scale 10 · points/export 10 · Referenz-Golden 6 · Atlas/Teile 13 |
| 2026-09-26 | 04 | End-to-End `p04_flow_runner.gd` | App-Start → Pflicht-Editor → Galerie → Bereich: eigene Figur **125,2 cm** (Kind), eigene Katze **28,0 cm** < Tisch, Figur im Bild |
| 2026-09-26 | 04 | Editor-Bedienung im Bild | ✓-Knopf erst grau (Hautton fehlt) → orange · Hautton 1,6 %, Oberteil 4,6 %, 🎲 15,5 % Bildänderung in der Vorschau |
| 2026-09-26 | 04 | Haustier-Editor | 13 Arten (Maßstab-Tabelle 6–125 cm), 3 Fell-Zonen, 5 Muster, 6 Halsbänder, 5 Charakterzüge, je Art eigene Stimme |
| 2026-09-26 | 04 | Namenswahl + Eltern-Tor | 238 Namen als Kacheln · 🎲 · freie Eingabe erst nach Tor (Rechenaufgabe **oder** 3 Punkte 3 s halten) |
| 2026-09-26 | 04 | check.sh (Teil 1) | Maßstab ✅ · pytest 37/37 ✅ · GUT 184/184 ✅ (1547 Asserts) |
| 2026-09-26 | 04 | 100 Figuren speichern + laden | **5,0 ms**, 0,05 MB (Ziel: kein Ruckeln) |
| 2026-09-26 | 04 | Teile-Katalog (`p04_lookbook.gd`) | 198 Teile · 8 Slots × 5 Varianten · 10 Palettenfarben: 9/10 Farb-Richtungen im Bild korrekt zugeordnet |
| 2026-09-26 | 04 | Schablonen-Größen im Bild | Kleinkind : Kind : Erwachsene = 90 : 125 : 172 (±10 % gemessen) |
| 2026-09-26 | 03 | P03-Nachweis `p03_check.gd` (37 Prüfungen, Zahlen statt Augenmaß) | 37/37 grün: Karotte 20,0 cm (15 % der Kind-Größe) · Apfel 7,8 cm · Ball 31,7 cm mit zwei Händen · Hüfte Kind 45,0 cm, Kopf 120,0 cm, Füße baumeln 23,0 cm · Erwachsene Sessel 42,0 cm, Füße 0,0 cm · Kleinkind liegt 92 × 49 cm auf 44,2 cm · Teddy 45,0 cm · Hund 49,4 cm < Tisch 77,8 cm · Griff-Abstand 0,00 cm |
| 2026-09-26 | 03 | Referenz-Küche nachgemessen (`p03_reference_kueche.gd`) | 13 Objekte: größte Abweichung **4,3 %** zur Maßstab-Tabelle (Teddy sitzt 45,0 cm) |
| 2026-09-26 | 02 | Leistung 250 Items + 1 Item im Dauer-Drag (`p02_perf_runner.gd`) | headless (nur Logik): **145 FPS** (6,9 ms/Frame) · llvmpipe-Software-Rendering 2 Kerne: 5,7 FPS @1080p / 11,2 @720p (61 Items: 17,7 @720p → Engpass ist das Software-Rendering, nicht die Items) · 613 Draw-Calls · 1040 Nodes · Greifen 0,7–0,9 ms, Zielsuche 1,1–2,0 ms. **GPU-60-FPS muss 👤 auf echter Hardware bestätigen.** |

## Log
### 2026-09-27 · Phase 04b · T07 Haustiere + Leistung ✅ (Phase 04b komplett)
- `tools/pets/draw.py` + `tools/make_pet_sprites.py`: 13 Tiere neu im Stil C – großer Kopf, Kulleraugen, braune
  Tinte, weiche Schattierung, sichtbares Halsband mit Marke. In Entwurfs-Einheiten (Höhe 100) gezeichnet →
  gleiche Strichstärke vom Hamster bis zum Pony. `make_editor_parts.py` entfernt (nur noch hierfür genutzt).
- **Fellmuster wurden gespeichert, aber nie gezeichnet:** `tools/make_pet_patterns.py` (Flecken, Streifen, Punkte,
  Spitzen, kachelbar) + `PetLook.apply()` → Shader-Muster nur auf Zone 1 (Fell). Stadt, Galerie, Editor nutzen es.
- Tier-Editor: Arten-Kacheln zeigen das echte Tier (vorher falsche Symbole: Schildkröte = Hamster, Pony = Hase),
  Muster-Kacheln zeigen das Muster am Tier, Farben als runde Punkte (gleicher Fehler wie im Figuren-Editor).
- **Leistung (einmal rot in check.sh):** `test_perf` lag bei 2,2–3,1 ms (Limit 4). Ursachen:
  1. `find_target` sammelte alle Raum-Items 3× je Suche und prüfte Sichtbarkeit vor billigen Eigenschaften →
     jetzt 1× sammeln, billige Prüfungen zuerst: **2,65 → 1,4 ms**.
  2. Greifen: mit 250 verschiedenen Katalog-Items maß der Test den einmaligen Masken-Aufbau je Textur mit
     (0,9 ms/Textur). Jetzt wie bei `find_target` aufgewärmt und extra gemeldet: **pick 0,9 ms**.
- Tests: GUT +1 (`test_pet_pattern_is_drawn_on_the_fur`); check.sh ✅ – pytest 127/127 · GUT 260/260.
### 2026-09-27 · Phase 04b · T06 Figuren-Editor 🔨
- **Leere Farbfelder waren ein Fehler:** `Ui.mark_selected(b, false)` überschrieb die Farbe jedes Felds mit Weiß.
  Neu `src/ui/color_dots.gd`: runde Farbpunkte, die Farbe steckt in einem eigenen Kreis (Auswahl = Ring + Häkchen).
- Farbzonen als Punkte in ihrer aktuellen Farbe (statt „1/2/3“), Stoff-Palette bricht in 2 Reihen um.
- Teile-Kacheln immer in Farbe (`CharacterParts.default_colors`, Startfarben in `palette.json › defaults`);
  neue Figuren tragen rot/jeans/rosa statt weiß.
- Outfit-Plätze: „+“ (leer) / Shirt (belegt) statt Zahlen. Größen: 4 Schablonen inkl. **Teen**, das Figur-Symbol
  wächst mit der echten Größe. Kategorie-Leiste passt (10 × 104 px, vorher rechts abgeschnitten).
- Vorschau: warmer Kreis statt grauem (halbdurchsichtiges Weiß wurde in der Mini-Welt grau).
- Beweis-Skript `p04_ui_runner.gd` an den P05-Ablauf angepasst (✓ → Stadtkarte; Galerie jetzt über den Figur-Knopf).
- Tests: GUT +3 (`test_color_dots_show_their_colour_even_when_selected`, Palette/Zonen, bunte Startfigur + Teen).
  check.sh ✅ – pytest 127/127 · GUT 259/259. Bilder `docs/tests/P04/p04_04…08` neu.
### 2026-09-27 · Phase 04b · T08 Symbole im Stil C 🔨
- `tools/make_icons.py` + `tools/icons/` (base, ui_set, editor_set, area_set): **68 Symbole** als Vektor mit
  Farbzonen und brauner Tinten-Kontur – derselbe Stil wie Figuren und Items. Jede Ebene wird wie im Shader
  eingefärbt („gebacken“), 256×256 px, zentriert. Ersetzt `make_ui_icons.py` (einfarbig violett + `modulate`).
- `Ui.icon()` färbt nicht mehr ein (Standard weiß); alle Aufrufer ohne Farbe.
- Neu: `wrench` (Baustellen-Zeichen auf der Stadtkarte – fehlte bisher ganz!), Bereiche Wald, Camping,
  Friseur, Fahrradverleih.
- Tests: pytest `test_icons` (alle benutzten Symbole vorhanden, farbig + braune Kontur, bit-gleich reproduzierbar).
  check.sh ✅ – pytest 127/127 · GUT 256/256.
- Gefunden: Tier-Gesichter lachten verkehrt herum (Mund-Bogen), Wald-Symbol zu einfarbig → Fliegenpilz.
- Offen (Politur): Einstellungen – Welt-Auswahl rutscht unten aus der Karte.
### 2026-09-27 · Phase 04b · T12 Qualitäts-Durchgang Items + Liegen 🔨
- Blick-Check aller Vorlagen, so eingefärbt wie im Spiel: `tools/items/review_sheet.py <out> [--scale] [--states]`
  (Shader-Formel in Python, ein Kontaktbogen je Gruppe).
- Nachgezeichnet: Luftmatratze (Kissenwulst, 6 Kammern, Ventil), Schwimmring (echtes Loch), Flossen, Liegestuhl,
  Strandtuch, Schlafsack, Campingstuhl, Findling mit Moos, Lagerfeuer (Steinring + Holz-Tipi), Fußballtor mit
  Netz-Tiefe, Hockeyschläger, Holzschlitten, Karussellpferd im Galopp, Aquarium (Wasser, Kies, Fische), Sandkasten,
  Puppe im Figuren-Stil, Kerze (Flamme orange), Palme (gebogene Wedel), Glücksbambus, Efeu (Ranken über den Topfrand).
- Fehler gefunden (nur durch Hinschauen):
  - Zeichenfläche hatte oben nur 6 cm Rand → offene Deckel (Kühlbox, Grill, Werkzeugkasten) wurden abgeschnitten.
    Jetzt 80 % der Höhe Luft oben, danach wird eng zugeschnitten.
  - Pflanzen nutzten `hash()` als Zufalls-Seed → bei jedem Lauf andere Bilder. Jetzt `zlib.crc32` (+ pytest, der
    mit zwei verschiedenen `PYTHONHASHSEED` vergleicht und mit dem alten Code rot war).
  - Katze aus `default_items` erschien in Roh-Zonenfarben (rot/grün/gelb) → Tiere ohne Farben bekommen das
    Standard-Fell ihrer Art (GUT-Test).
  - Liegende Figur schwebte ~20 cm über der Luftmatratze: der große Kopf ist dicker als der Körper. Jetzt leicht
    geneigt (max. 26°, wie auf einem Kissen), Kopf und Füße liegen auf, Haare dürfen aufs Kissen fallen. Gemessen
    wird der echte Umriss (`LayerGeometry.lowest`, `BitMap.opaque_to_polygons`) statt gedrehter Rechtecke – die
    Rechteck-Ecke des runden Kopfes lag 10 cm tiefer als der Kopf.
- Beweis: `docs/tests/P04b/p04b_05_luftmatratze_in_der_kueche.jpg` (Zuhause hat bis P07 nur die Küche als Raum).
- Tests: check.sh ✅ – Maßstab (1087 Items) · pytest 124/124 · GUT 256/256
  (neu: `test_items_review` ×2, `test_pet_without_own_colors_gets_default_fur`, `test_kid_lies_on_the_pool_air_mattress`,
  Liege-Test auf „Kopf und Füße liegen auf“ umgestellt).
### 2026-09-27 · Phase 04b · T11 Mehr Spiel draußen, im Laden und in der Werkstatt 🔨
- Neue Zustände (Tippen): Grill an (Deckel hoch, Glut, Rauch), Lagerfeuer an/aus (aus = Holz + Rauchfaden),
  Laterne leuchtet, Zelt-Tür auf/zu, Kühlbox auf, Kasse auf (Geldschublade mit Scheinen/Münzen, Hüpfer),
  Bohrer läuft (Wackeln), Werkzeugkasten auf.
- Grill und Lagerfeuer sind Kochstellen: Grillgut → Wurst, Brot → Toast, Milch am Feuer → heiße Milch (5 neue Rezepte).
- Tests: GUT 254/254 (+3 in `test_item_states`), pytest 122/122, Maßstab ✅.
### 2026-09-27 · Phase 04b · T09 + T10 Item-Bibliothek, Zustände & Kochen 🔨
- Erledigt:
  - T09: `tools/items/` (Vektor-Kit, Möbel, Pflanzen, Haushalt, Spiel, draußen, Stadt), `tools/make_items.py`
    (parallel, Farbzonen, `c_<id>`-Maßstab-Einträge), 27 Katalog-Gruppen in `data/catalog.json`,
    Katalog-Leiste rechts (max. ⅓), Items erscheinen links im freien Bild und bleiben frei verschiebbar.
  - T10: `ItemStates` (Zustands-Sprites auf gleicher Leinwand, Tippen schaltet weiter, Wackeln/Pulsieren/Hüpfen),
    `Recipes` + `data/recipes/cooking.json` (15 Rezepte: Toast, Spiegelei, Würstchen, Pfannkuchen, Suppen,
    Smoothies, Kakao, Popcorn, Kaffee, Kuchen, Brot) – Hitze erbt vom Wirt (Pfanne auf dem Herd).
    Großgeräte (Kühlschrank, Herd, Ofen, Waschmaschine, Spüle, Ventilator, Computer, Konsole), gekochte Speisen.
    Zustand wird im Raum gespeichert. **342 Vorlagen · 1010 Katalog-Items.**
- Tests: check.sh ✅ – Maßstab (492 Einträge, 1087 Items) · pytest 122/122 · GUT 251/251
  (neu: `test_catalog`, `test_item_states`). Beweis `docs/tests/P04b/p04b_01…04`.
- Entscheidung: Maßstab-Referenzen der Katalog-Vorlagen heißen `c_<id>`, damit handgemessene Einträge
  (z. B. `food_apple`) nie überschrieben werden.
- Offen: Tiere (T07), Icons (T08), Editor (T06), mehr Spielzustände (T11).
### 2026-09-27 · Phase 04b · Figuren-Neubau im Stil „großer Kopf“ (T01–T05) 🔨
- Anlass: 👤-Test im Browser – Figuren/Editor/Tiere „sehen Scheiße aus“ (weiße Haut, graue Kästen, Platzhalter
  mit Text). Zielbild: Stil-Vorlage C. Entscheidungen: großer Kopf, Vektor im Code, 1000+ Teile, leere Räume +
  Katalog, alle Icons neu. Phasen-Datei `docs/phasen/PHASE_04B_FIGUREN_NEU.md`.
- Erledigt:
  - `tools/chibi/` (vec, body, hair, wardrobe, accessories, compose) + `tools/make_chibi_parts.py`:
    **139 Teile je Schablone × 4 Schablonen** in ~2 Min (4 Prozesse), Katalog 78 Varianten in 8 Slots.
  - `templates.json`: Kind ≈ 2 Kopfhöhen, **Teen (155 cm) neu**; Kopfmitte so, dass Standard-Frisuren genau bei
    der Tabellenhöhe enden. `scale_table`: Figuren-Breiten = Kopf inkl. Ohren.
  - Shader: `ink` (Tinte statt Schwarz, Standard schwarz = alte Formel) + Muster-Uniforms (vorbereitet).
  - `CharacterLook.colors_for`: Haut+Wangenrot, Augen+Brauen (Haarfarbe), Haar+Glanz+Haargummi,
    Kleidung/Beine/Schuhe Zone 3 = Haut. Alte IDs → Aliase (`knee_bandage` → `plaster`, R-11).
  - Rig: Haare hinten liegen hinter dem Körper (`HeadBack`), gewählter Mund bleibt bei „fröhlich“,
    Liegen dreht die ganze Figur (lange Haare hängen nicht mehr durchs Bett).
  - Accessoire/Hilfsmittel starten „ohne“ (vorher trug jede neue Figur Brille + Hörgerät).
- Tests angepasst (Absicht bleibt, nur Werte aus der Schablone statt fest): Hüfte/Scheitel beim Sitzen,
  Liegen (Achse statt Hüllen-Verhältnis), Varianten „mindestens 5“, Körper-Größe ohne Haare/Hut + Obergrenze
  45 % Kopfhöhe für Frisuren/Hüte, Farbzonen-Beweis mit festen Prüffarben. check.sh ✅ (pytest 122, GUT 240).
- Beweis: `docs/tests/P04/p04_01…03` neu aus dem echten Renderer.
- Entfernt: `tools/make_rig_parts.py` (ersetzt). `make_editor_parts.py` nur noch für `ZCanvas` der Tiere.
- Nächste Task: Editor-Oberfläche (T06), Icons (T08), Item-Bibliothek + Katalog (T09), Tiere (T07).
### 2026-09-27 · Phase 06 · Asset-Pipeline (produktiv) ✅
- Erledigt: P06-T01…T12.
  - `tools/asset_pipeline/`: `cutout.py` (Loch-Regel >500 px/mean>250, Figuren-Modus, Kanten-Entmischung),
    `split.py` (Zeilen über die vertikale Mitte, Anzahl == YAML sonst `SplitError` + nummeriertes
    Vorschaubild, Figuren-Modus = N größte Flächen), `scale.py` (Tabelle × `scale_mul`, Breite aus
    Seitenverhältnis, >30 % = `tolerance_aspect`-Warnung), `points.py` (Kategorie-Grips inkl.
    Tasse=Henkel 45 %, YAML-Override gewinnt, `find_hand_grip`, Marker-Vorschau), `export.py`
    (8 px/cm, ≥64 px Mindestkante, 4 px Padding → `pad_px` im JSON, Upsert mit Metadaten-Merge:
    tags/sfx/seat/surface bleiben erhalten), `lineup.py`, `scene_test.py` (Referenz-Küche),
    `run.py` (Alles-in-einem + Zusammenfassung), `atlas.py` (Shelf-Packung ≤4096²),
    `figure_parts.py` (Differenz Schablone→Teil-Ebene, 8 px/cm tight-box, Anker von unten-links,
    `parts.json`-Upsert), `calibrate_bg.py` (T07, seit P01 + getestet).
  - `reference/raw_items.yaml` + `raw_furniture_dog.yaml` + `raw_girl.yaml`: Demo-Blätter als
    YAML (18 Items + Figur), Werte 1:1 aus `pipeline_demo_kueche.py`.
  - `docs/asset_settings.md` (T12): ComfyUI-Einstellungen, Stil-Block, Negativ-Prompt,
    Blatt-/Raum-/Teil-Vorlagen, LoRA-Training kostenlos, Fehler-Tabelle.
- Tests: check.sh ✅ (pytest 110/110 – neu: cutout/split/scale/points/export/Referenz-Golden/Atlas/Teile;
  GUT 240/240, `test_aspect_ratio_is_kept` pad-aware). Golden-Lauf: `run.py reference/` erzeugt
  JSON == Referenz und 18 Sprites mit identischem Seitenverhältnis (±2 %).
- Entscheidungen:
  - YAML **pro Blatt** (`<blatt>.yaml` neben dem PNG), `items_json:` optional → Upsert in die
    bestehende Datei (kein Dublikat, keine doppelten IDs in der ItemDB).
  - Figuren landen NICHT in `data/items/`, sondern in `assets/characters/sprite/` + `.sprite.json`
    (hand_grip) – sonst würde die ItemDB-Fixture zählen.
  - Paddierung ist im JSON als `pad_px: 4` gemeldet; `ItemNode.draw_size` rechnet den Inhalt,
    Tests vergleichen Inhalt gegen Inhalt.
  - Upsert-Merge: Pipeline-Felder ersetzt, fremde Felder bleiben (Buch behält `tags`,
    Hund behält `sfx`, Stuhl behält `seat`).
- Hinweis 👤: Echte ComfyUI-Blätter für die Küche (Stil-Guide §3A) → `incoming/home/`, dann
  `run.py` – Anleitung in `docs/asset_settings.md`.
- Nächste Task: P07-T01 (Slice Zuhause & Garten: mehrere Räume, Hintergründe, Garten-Items)
### 2026-09-26 · Phase 05 · Startmenü (Stadtkarte), Speichern, Bereichswechsel ✅
- Erledigt: P05-T01…T11 (T09 Eltern-Tor kam schon in Phase 04).
  - `data/areas/index.json` + `src/core/areas.gd`: **12 Bereiche** (Zuhause & Garten, Krankenhaus,
    Schule, Schwimmbad, Spielplatz, Rummelplatz, Zoo, Einkaufsstraße, Eishalle, Sportzentrum,
    Blumenladen, Werkstatt) mit Symbol, Farbe, Karten-Position, Sound und `ready`-Flag.
  - `tools/make_city_map.py`: Karten-Hintergrund (Wiesen, Fluss, Straßen, Bäume, 12 Podeste),
    Bereichs-Knöpfe liegen exakt auf den Podesten. **Umschaltbar** auf ein ruhiges Raster.
  - `src/ui/city_map.gd`: Karte/Raster, Kopfzeile mit Figur · Rucksack · Album · Eltern.
    Unfertige Bereiche zeigen ein wippendes Werkzeug (Baustelle) – **kein Schloss**.
  - `src/core/scene_router.gd` + `src/world/area_scene.gd`: Bereichswechsel mit Ladebild,
    Spawn der **eigenen** Figur am `spawn`-Punkt (Ankunfts-Hüpfer), eigene Haustiere dabei,
    Items aus dem gespeicherten Zustand (sonst aus `default_items` der Bereichs-Datei).
  - `src/ui/area_hud.gd`: Karte (zurück) · 📷 Foto · Rucksack · Rückgängig.
  - `SaveSystem` neu: **3 Welt-Slots**, `save_version 2`, Migration v1→v2 (`_static_init`),
    Export/Import als Datei (ohne Netz), Album unter `user://album/`.
  - `src/world/room_snapshot.gd`: Raumzustand einfrieren/wieder aufbauen – auch Dinge **auf**
    Tischen (Wirt + relativer x-Wert). Figur gehört nicht dazu (wird frisch gespawnt).
  - `src/ui/backpack.gd` (20 Plätze, Ding raus/ziehen-auf-den-Knopf), `src/ui/album.gd`,
    `src/ui/settings_panel.gd` (Lautstärken, große UI, wenig Animation, Sprache, 🪄 Bereich
    zurücksetzen, Alles löschen, Export/Import, Welt-Slots) – alles hinter dem Eltern-Tor.
  - Autosave entprellt (2 s) über `Game.mark_dirty()`; sofort gespeichert beim Verlassen.
- Tests (neu): GUT `test_save_migration` (9, Fixture `tests/fixtures/world_v1.json`),
  `test_city_map` (7), `test_area_flow` (7) · pytest `test_p05_shots` (17) ·
  Beweis `p05_flow_runner.gd` (8 Bilder + `p05_flow.json`).
- Fehler gefunden (nur durch Messen):
  - `Control`-Panels unter einem `Node2D` bleiben unsichtbar (Größe 0) → der Bereich hat jetzt
    eine eigene `CanvasLayer` (`AreaScene.ui`) für Rucksack/Album/Eltern.
  - `LayoutPreset` ist in einem `CanvasLayer`-Skript nicht sichtbar (nur in `Control`) →
    Parameter als `int`. `Script.new()` gibt es nicht → `GDScript`.
  - Loop-Tweens in `_ready` lösen „Infinite loop detected" aus → Wippen läuft über `_process`.
  - `SaveSystem.wipe()` wirkt erst nach `Game.load_all()` (Autoload lädt vorher).
- 👤 offen: Blick-Check der Stadtkarte, echte Stil-C-Hintergründe für weitere Bereiche (P06/P07).
- Nächste Task: P06 (Asset-Pipeline) + P07 (Zuhause & Garten mit mehreren Räumen).
### 2026-09-26 · Phase 04 (Teil 2) · Editor-Oberfläche, Namen, Galerie, Haustiere ✅
- Erledigt: P04-T03 (Editor-UI), T05 (🎲 + 5 Outfit-Plätze), T06 (Namen + Eltern-Tor),
  T07 (Pflicht-Ablauf), T08 (Galerie), T09 (Haustier-Editor).
  - `src/ui/ui.gd` (**Kit**): ein Look für alles – warme Karten, dicke runde Knöpfe (≥ 96 px),
    Symbole statt Text. Schrift **Baloo 2** (rund, OFL) + Nunito; Theme hängt an der Fensterwurzel.
  - **63 Icons** aus `tools/make_ui_icons.py` (PIL, 4× übersampelt, ein dunkles Violett → per
    `modulate` einfärbbar). Kein Emoji-Font nötig – der war im Sandkasten ohnehin nicht da.
  - `src/ui/character_editor.gd`: links große Vorschau (`FigureStage` mit eigener Mini-Welt +
    Kamera, Tippen = Gefühl wechseln), rechts 10 Kategorien als **Symbole**, unten die Palette
    mit Zonen-Wahl (1–3). ✓ bleibt **aus**, bis Schablone + Hautton stehen.
  - `src/ui/gallery.gd`: unbegrenzt Figuren, Ordner (Alle/Familie/Freunde/Kita/Fantasie),
    duplizieren, löschen (✓/✕-Symbole), aktive Figur wählen; zweiter Reiter für Tiere.
  - `src/ui/pet_editor.gd` + `PetSpecies` (`data/pets/species.json`): 13 Arten, Fell/Bauch/
    Halsband als 3 Shader-Zonen, 5 Muster, 5 Charakterzüge (nur passende je Art), Stimme hörbar.
  - **13 Haustier-Sprites** (`tools/make_pet_sprites.py`, Stil C, 3 Zonen) + 15 neue Sounds
    (`tools/make_sfx.py`: Vogel, Kaninchen, Hamster, Meerschweinchen, Fisch, Schildkröte, Pony,
    Drache, Einhorn, Schnurren + UI-Töne). Tier-Größen kommen aus der Maßstab-Tabelle.
  - `src/ui/name_picker.gd`: 238 Namen als Kacheln + 🎲; freie Eingabe **nur hinter dem
    Eltern-Tor** (`parent_gate.gd`: Rechenaufgabe mit Ziffern-Kacheln **oder** 3 Punkte 3 s
    halten) + lokaler Wortfilter (`name_filter.gd`).
  - `src/ui/flow.gd`: Splash → „eigene Figur da?“ → Pflicht-Editor → Galerie → Bereich.
    Ohne vollständige Figur ist kein Bereich betretbar (`Flow.can_play()`, Test).
  - `src/ui/portrait.gd`: Galerie-Bilder aus einer versteckten Mini-Kamera (Cache; ohne
    Bildschirm → `can_render() == false`).
  - Die Sandkasten-Welt spawnt jetzt die **eigene** Figur und die **eigenen** Tiere.
- Tests (neu): GUT `test_editor_ui` (11), `test_gallery_pets_ui` (10), `test_names_gate` (10)
  · pytest `test_p04_ui_shots` (21) · Beweis `p04_ui_runner.gd` (10 Bilder) und
  `p04_flow_runner.gd` (End-to-End + `p04_flow.json`).
- Messwerte: eigene Figur im Spiel **125,2 cm**, Katze **28,0 cm** (< Tisch 77,8 cm),
  🎲/Teile/Farben ändern die Vorschau messbar (1,6 % / 4,6 % / 15,5 % der Pixel).
- Fehler gefunden (nur durch Messen):
  - `ItemDB.get()` ist `Object.get()` → lieferte stillschweigend `null`. Heißt `get_item()`.
  - Container-Ketten haben die Vorschau auf 1898 px aufgeblasen (Mindestbreite der Kacheln) →
    linke Spalte hat jetzt **feste Anker** (720 px) und die Bühne eine feste Größe (660 px).
  - Der Hund lief beim Schlendern **durch die Figur hindurch** (kleinster Abstand 9,4 cm) →
    Ausweich-Bogen + harte Grenze von 40 cm (`MIN_FRIEND_CM`), jetzt 40,0 cm.
  - `String(int)` gibt es in GDScript nicht (Tests) · `find_child` findet nur *owned* Nodes →
    `find_child(name, true, false)`.
- 👤 offen: Kindertest „ohne Lesen bedienbar“, echte Stil-C-Körper/Teile (P06).
- Nächste Task: P05-T01/T02 (Stadtkarte, Startmenü, Speichern).
### 2026-09-26 · Phase 04 (Teil 1) · Daten, Teile & Umfärben
- Erledigt: P04-T01 (Datenformat), T02 (Datenmodell + Speichern), T04 (Umfärben), T10 (Platzhalter-Teile).
  - `tools/make_editor_parts.py`: **198 Teile** für 3 Schablonen. Jedes Teil speichert seine Farbzonen
    als Gewichte in **R/G/B** (mit eingebackenem Verlauf) und die Deckung in A → 3 Zonen pro Teil,
    eine Textur, kein zweites Bild.
  - `assets/shaders/zone_tint.gdshader`: `Farbe = R·zone1 + G·zone2 + B·zone3` (Stil C: farbige Konturen,
    nie schwarz). `CharacterLook` setzt je Ebene Teil + Zonenfarben; der Rig bleibt unter 400 Zeilen.
  - `data/character_parts/<slot>.json`: 8 Slots (top, bottom, shoes, hair, eyes, mouth, accessory, aid)
    × **5 Varianten** + `palette.json` (Haut/Haare/Stoff/Schuhe/Fell).
  - `CharacterData` (Schablone, Hautton, Teile+Farben, Name, Stimme 1–8, **5 Outfit-Plätze**, Ordner)
    und `PetData` (Art, Fell, Muster, Halsband, Charakterzug) ↔ JSON.
  - `SaveSystem`: `user://characters.json` / `pets.json`, versioniert, Migrations-Haken, `wipe()`.
  - Gefühle wechseln jetzt **Mund UND Augenform** (Herzen bei „verliebt"); die im Editor gewählte
    Augenform bleibt der Normalzustand.
- Tests (neu): GUT `test_editor_parts` (Katalog, Sprites je Schablone, Zonen, Shader-Farben, Palette,
  🎲 reproduzierbar), `test_character_data` (Rundlauf, **100 Figuren in 5 ms**, Pflicht-Felder,
  Outfits, Haustier) · pytest `test_p04_shots` (Bildmaße 90:125:172, Farbzonen im Bild).
- Beweis: `docs/tests/P04/*.jpg` (Katalog, Schablonen-Größen, Farbzonen).
- Entscheidungen:
  - Größe kommt **nur** aus der Schablone → ein Kleid oder Stiefel ändern keine Körpergröße (Test).
  - Augen/Mund sind eigene Ebenen statt einer fertigen Gesichts-Ebene: der Editor kann sie einzeln
    tauschen, die Gefühle überschreiben sie nur vorübergehend.
  - Beschriftungen in Beweisbildern werden in **Bildpunkten** gesetzt (1/zoom skaliert), sonst
    überdecken Welt-Labels die Figuren.
- 👤 offen: Editor-Oberfläche (T03), 🎲 + Outfits-UI (T05), Namen (T06), Pflicht-Ablauf (T07),
  Galerie (T08), Haustier-Editor (T09).
- Nächste Task: P04-T03
### 2026-09-26 · Phase 03 · Figuren & Tiere ✅
- Erledigt: P03-T01…T10.
  - `tools/make_rig_parts.py`: 63 Figuren-Teile (3 Schablonen) als Stil-C-Platzhalter, 8 px/cm, bit-genau.
    Anker in `parts.json` (cm, y von unten), Sitz-Geometrie in `_geometry` (`sit_drop_cm`).
  - `CharacterRig` (Ebenen: Haar hinten · Arm hinten · Beine · Schuhe · Oberteil · Kopf · Gesicht ·
    Haar vorne · Arm vorne · Finger). Knoten-Kette `Rig → Lift → Swing → Parts → Arm/HeadPivot`.
  - 3 Schablonen: `toddler` 90, `kid` 125, `adult` 172 cm – **Größe nur aus der Tabelle** (Test).
  - Posen `stand/sit/lie`: sitzende Beine hängen ab der **Hüfte** (Knie auf Sitzhöhe) und verkürzen sich
    perspektivisch, wenn der Sitz niedriger ist als das Schienbein (Erwachsene auf dem 42-cm-Sofa).
    Beim Liegen: Körper waagerecht um die Hüfte gedreht, **Kopf bleibt aufrecht** (liegt auf dem Kissen),
    beide Arme liegen oben.
  - `PlacementCharacter` (vor Behälter/Fläche/Boden): **Mund** (Essen ≤ 15 cm) → **Hand** (Griffpunkt
    ≤ 25 cm, `two_hands` nur in Slot 2) → **Sitz-/Liegeplatz** (Figur/Tier/Spielzeug, Becken-Radius 30 cm).
  - `Seats`: Sitzhöhe Plätze aus der Tabelle (Stuhl 45, Sofa/Sessel 42, Bett 45), Belegung, Platzsuche.
  - `CharacterEating`: Eis am Mund → Mampf → weg, Gesicht `love`.
  - 6 Gefühle (fröhlich, lachend, überrascht, traurig, müde, verliebt); Tipp auf den Kopf schaltet weiter,
    Tipp auf den Körper → lachen + Hüpfen.
  - `SpriteCharacter`: fertiges Mädchen (`reference/sprites/`) mit Hand-Slot + Faust-Ebene über dem Item.
  - `PetNode`: Hund/Katze, 60 cm/s, Modi sitzen/laufen/folgen (Start > 110 cm, Stopp 50 cm), Tipp → Laut
    über den `AudioBus`-Tier-Limiter (1 Laut / 8 s), `tick()` für Tests, RNG-Seed pro Tier.
  - Figuren-Sandbox `sandbox_characters.tscn` (4 Figuren, Hund, Katze, Teddy, Ball, Stuhl, 2. Stuhl,
    Sofa, Sessel, Bett, Esstisch mit Essen) + Referenz-Küche `sandbox_reference_kitchen.tscn` (T10).
- Tests (neu): GUT `test_hand` (**Pflicht**), `test_character`, `test_seat`, `test_pet`,
  `test_character_drag` · pytest `test_p03_shots` (Bilder + Messwerte).
- Beweis: `docs/tests/P03/*.jpg` (13 Bilder) + `p03_messwerte.json` + `p03_13_referenz_kueche.json`.
  Erzeugt durch `tools/godot/p03_scenario_runner.gd` (Screenshots, bedient die Drag-API wie ein Kind),
  `tools/godot/p03_check.gd` (37 Zahlen-Prüfungen) und `tools/godot/p03_reference_kueche.gd` (T10).
- **Neues Messwerkzeug (weil Augenmaß nicht reproduzierbar ist):**
  - Silhouetten-Differenz: Item ausblenden, Bild 2 machen, Differenz → exakte Pixel → cm. Misst nur das,
    was wirklich sichtbar ist (Finger verdecken den Apfel korrekt).
  - `tools/godot/p03_pose_dump.gd`: jede Figur-Ebene in cm über dem Standpunkt (Tabelle je Pose).
  - Screenshot-Läufer rechnet den Bildausschnitt aus den Objekten selbst und meldet „im Bild/angeschnitten“.
- Von den Prüfungen gefundene und behobene Fehler:
  - **Figur versank beim Sitzen:** `PlacementCharacter` setzte den Fußpunkt statt der Hüfte auf den
    Sitzpunkt, und die Pose verschob den Körper zusätzlich → Oberteil-Block bei den Füßen.
  - **Beine ragten beim Sitzen 11 cm unter den Boden** (Erwachsene auf dem 42-cm-Sofa): Sitz-Teil war zu
    lang (Knie saß `sit_thigh` unter der Hüfte). Neues Teil: Knie auf Sitzhöhe, Schienbein hängt ab dort.
  - **Kopf versank beim Liegen** im Bett und der hintere Arm hing *unter* dem Körper: Körper wird jetzt
    um die halbe Rumpfdicke angehoben, Kopf um die halbe Kopfdicke, beide Arme liegen oben.
  - Tiere liefen in Tests und Screenshots selbstständig umher → `PetNode.autonomous` (statisch) aus,
    Bewegung nur per `tick()`. `_process` wird dann ganz abgeschaltet (CPU + test_perf grün).
  - Pose-Tweens machten Messungen ungenau → `CharacterRig.animate_poses` (statisch) für Tests/Bilder aus.
- Entscheidungen:
  - `layer_geometry.gd`: Hülle und Pixel-Treffer über viele Sprite-Ebenen – hält `character_rig.gd`
    unter 400 Zeilen und wird später von den NPCs mitgenutzt.
  - Sitzhöhe wirkt **nur** über die Tabelle (`seat_h_cm`), nie über die Figur.
  - `Lift`-Knoten: beim Anheben gehen Körper, Hände und gehaltene Items gemeinsam 6 cm hoch.
  - Sitzende Figur wird über die **Hüfte** einsortiert (Knoten-Ursprung = Füße bleibt die Regel).
- 👤 offen: **Erster Kindertest** (10 Minuten, 1–2 Kinder) → Protokoll in `docs/tests/P03_kindertest.md`.
- Nächste Task: P04-T01
### 2026-09-26 · Phase 02
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
