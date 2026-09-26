# PROGRESS · Gedächtnis des Agenten
> Wird vom Agenten nach **jeder Task** aktualisiert. Neueste Einträge oben im Log. Nie löschen, nur ergänzen.

## Status
| Feld | Wert |
|---|---|
| Aktuelle Phase | **04 · Charakter-Editor** |
| Nächste Task | P04-T03 (Editor-Oberfläche) – T01/T02/T04/T10 fertig |
| Letzter grüner check.sh | 2026-09-26 (Phase 04, Teil 1) |
| Version | 0.0.4 |

## Phasen
| Phase | Status | Bericht |
|---|---|---|
| 00 Setup | ✅ fertig | Log 2026-09-26 |
| 01 Welt-Maßstab | ✅ fertig (👤 Blick-Check offen) | Log 2026-09-26 |
| 02 Items & Drag | ✅ fertig (👤 Anfass-Gefühl + GPU-FPS offen) | Log 2026-09-26 |
| 03 Figuren & Tiere | ✅ fertig (👤 Kindertest offen) | Log 2026-09-26 |
| 04 Editor | 🔨 Teil 1: Daten/Teile/Farben (UI folgt) | Log 2026-09-26 |
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
| 2026-09-26 | 02 | check.sh | Maßstab ✅ (155 Einträge, 61 Items) · pytest 15/15 ✅ · GUT 129/129 ✅ (850 Asserts) |
| 2026-09-26 | 03 | check.sh | Maßstab ✅ (155 Einträge, 65 Items) · pytest 31/31 ✅ · GUT 169/169 ✅ (1019 Asserts) |
| 2026-09-26 | 04 | check.sh | Maßstab ✅ · pytest 37/37 ✅ · GUT 184/184 ✅ (1547 Asserts) |
| 2026-09-26 | 04 | 100 Figuren speichern + laden | **5,0 ms**, 0,05 MB (Ziel: kein Ruckeln) |
| 2026-09-26 | 04 | Teile-Katalog (`p04_lookbook.gd`) | 198 Teile · 8 Slots × 5 Varianten · 10 Palettenfarben: 9/10 Farb-Richtungen im Bild korrekt zugeordnet |
| 2026-09-26 | 04 | Schablonen-Größen im Bild | Kleinkind : Kind : Erwachsene = 90 : 125 : 172 (±10 % gemessen) |
| 2026-09-26 | 03 | P03-Nachweis `p03_check.gd` (37 Prüfungen, Zahlen statt Augenmaß) | 37/37 grün: Karotte 20,0 cm (15 % der Kind-Größe) · Apfel 7,8 cm · Ball 31,7 cm mit zwei Händen · Hüfte Kind 45,0 cm, Kopf 120,0 cm, Füße baumeln 23,0 cm · Erwachsene Sessel 42,0 cm, Füße 0,0 cm · Kleinkind liegt 92 × 49 cm auf 44,2 cm · Teddy 45,0 cm · Hund 49,4 cm < Tisch 77,8 cm · Griff-Abstand 0,00 cm |
| 2026-09-26 | 03 | Referenz-Küche nachgemessen (`p03_reference_kueche.gd`) | 13 Objekte: größte Abweichung **4,3 %** zur Maßstab-Tabelle (Teddy sitzt 45,0 cm) |
| 2026-09-26 | 02 | Leistung 250 Items + 1 Item im Dauer-Drag (`p02_perf_runner.gd`) | headless (nur Logik): **145 FPS** (6,9 ms/Frame) · llvmpipe-Software-Rendering 2 Kerne: 5,7 FPS @1080p / 11,2 @720p (61 Items: 17,7 @720p → Engpass ist das Software-Rendering, nicht die Items) · 613 Draw-Calls · 1040 Nodes · Greifen 0,7–0,9 ms, Zielsuche 1,1–2,0 ms. **GPU-60-FPS muss 👤 auf echter Hardware bestätigen.** |

## Log
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
