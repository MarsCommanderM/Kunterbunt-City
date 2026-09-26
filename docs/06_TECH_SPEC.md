# 06 · Technische Spezifikation ⚙️

## 1. Projekt-Einstellungen (Godot)
| Einstellung | Wert |
|---|---|
| Renderer | **Compatibility** |
| Viewport-Basis | 1920 × 1080, Stretch `canvas_items`, Aspect `expand` |
| Physik | 2D, Gravitation wird nur für fallende Items genutzt (eigene einfache Simulation, keine RigidBody-Stapel) |
| Texturen | Filter **Linear**, Mipmaps **an** (Zoom), VRAM-Kompression **an** |
| Web-Export | Thread Support **aus**, Kompression an, Ziel < 150 MB |
| Android | min SDK laut Godot-Standard, nur Querformat, keine Berechtigungen außer Vibration (optional) |
| Eingabe | `emulate_mouse_from_touch` **aus**, eigene Touch- und Maus-Behandlung im `DragController` |

## 2. Autoloads
| Name | Aufgabe |
|---|---|
| `Log` | einfache Log-Funktion (nur lokal, Konsole) |
| `Settings` | Lautstärken (Musik/Effekte/Tiere), Sprache, reduzierte Animation, große UI; gespeichert in `user://settings.json` |
| `ItemDB` | lädt `scale_table.json`, `items/*.json`, `recipes/*.json`; validiert; liefert `ItemDefinition` per ID |
| `SaveSystem` | Speichern/Laden (Raumzustände, Figuren, Haustiere, Rucksack), Versionsnummer + Migrationen |
| `Game` | aktive Figur, aktive Haustiere, aktueller Bereich, Rucksack-Inhalt |
| `SceneRouter` | Bereichswechsel mit Ladebildschirm (< 2 s), Spawn-Punkt, Zurück zur Stadtkarte |
| `AudioBus` | SFX/Musik/Ambiente, **Tierlaut-Limiter** (global max. 1 Tierlaut / 8 s pro Szene) |

## 3. Datenformate

### 3.1 Item (`data/items/<bereich>_<raum>.json`)
```json
{ "area": "home", "room": "kitchen", "items": [
  { "id": "food_carrot",
    "scale_ref": "food_carrot",          // Pflicht → scale_table
    "scale_mul": 1.0,                     // optional 0.7–1.3
    "size_cm": [8.4, 20.0],               // von der Pipeline berechnet (Höhe = Tabelle × mul)
    "pivot": [0.5, 1.0],                  // 0..1 im Sprite
    "grip": [0.5, 0.36],                  // Pflicht, wenn hold != none
    "hold": "one_hand",                   // one_hand | two_hands | none
    "hold_angle": -20,
    "placement": "table",                 // floor | table | shelf | wall | seat
    "movable": true,
    "states": ["whole", "sliced"],        // optional
    "tags": ["food", "vegetable"],
    "sfx": { "pickup": "soft", "drop": "soft", "use": "crunch" },
    "sprite": "res://assets/sprites/home/food_carrot.png" } ] }
```

### 3.2 Bereich/Raum (`data/areas/<bereich>.json`)
```json
{ "id": "home", "name_key": "AREA_HOME", "icon": "res://assets/ui/area_home.png",
  "spawn": { "room": "hallway", "x_cm": 120, "y_cm": 40 },
  "rooms": [
    { "id": "kitchen", "width_cm": 620, "height_cm": 300,
      "background": "res://assets/backgrounds/home/kitchen.bg.json",   // von calibrate_bg.py erzeugt (Kacheln ≤ 2048 px + Ursprung)
      "calibration": { "ref": "fix_counter", "px_top": 434, "px_bottom": 600, "source_px_per_cm": 1.83 },
      "floor": { "back_y_cm": 0, "front_y_cm": 90, "depth_scale_max": 1.12 },
      "camera": { "default_h_cm": 300, "min_h_cm": 220, "max_h_cm": 450 },
      "surfaces": [
        { "id": "counter_top", "type": "table", "x_cm": [40, 480], "h_cm": 90, "depth_y_cm": 0 },
        { "id": "window_sill", "type": "shelf", "x_cm": [500, 600], "h_cm": 95, "depth_y_cm": 0 } ],
      "fixtures": [ { "id": "stove", "x_cm": 180, "interaction": "cook" } ],
      "start_items": [ { "id": "home_table_dining", "x_cm": 420, "y_cm": 40 } ],
      "doors": [ { "to_room": "living_room", "x_cm": 10 } ] } ] }
```

### 3.3 Rezept (`data/recipes/*.json`)
```json
{ "id": "bake_bread", "inputs": ["food_dough"], "station": "fixture:oven", "requires_state": {"oven": "on"},
  "duration_s": 3, "output": "food_bread_loaf", "fx": "steam", "sfx": "ding" }
```

### 3.4 NPC-Rolle (`data/npc_roles/cashier.json`) & NPC (`data/npcs/*.json`)
```json
{ "role": "cashier",
  "states": ["idle", "serve", "tidy", "carried", "return_to_post"],
  "idle_anims": ["look_around", "count_money"], "tidy_every_s": [60, 120],
  "reactions": { "picked_up": "surprised", "item_at_register": "serve" },
  "return_after_s": 20 }
```
```json
{ "id": "npc_supermarket_cashier", "role": "cashier", "area": "shopping", "room": "supermarket",
  "post": { "x_cm": 310, "y_cm": 20, "fixture": "register_01" }, "look": "char_adult_preset_07" }
```

### 3.5 Speicherstand (`user://save_<slot>.json`)
```json
{ "save_version": 1, "created": "…", "characters": [ … ], "pets": [ … ], "backpack": ["food_apple_red#12"],
  "rooms": { "home/kitchen": { "items": [ { "uid": 12, "id": "food_apple_red", "x_cm": 210.5, "y_cm": 34.0,
             "state": "whole", "parent": "surface:counter_top" } ] } } }
```
Migration: `SaveSystem.MIGRATIONS = { 1: func(d): …, 2: … }`. Jede Migration hat einen GUT-Test mit einer alten Beispieldatei in `tests/fixtures/`.

## 4. Systeme – Verhalten

### 4.1 DragController (Zustandsmaschine)
`IDLE → PRESS (Finger auf Tippfläche) → LIFT (nach 80 ms oder 8 px Bewegung: Item hebt sich 6 cm, Schatten wächst, Hüpf-Effekt) → DRAG (folgt Finger mit leichter Verzögerung) → DROP`
- **DROP-Ziele (Priorität):** Hand einer Figur (Radius 25 cm) → Sitzplatz (SeatSlot) → Behälter → Oberfläche (Surface) unter dem Item → Bodenband.
- **Einrasten:** Das Item landet mit Pivot exakt auf der Oberflächenhöhe. Liegt das Ziel außerhalb aller Flächen, **fällt es sanft** auf die nächste Fläche darunter (max. 0,4 s).
- **Stapeln:** Nur Items mit Tag `stackable` (Teller, Bücher, Klötze), max. 8.
- **Multitouch:** bis 3 Items gleichzeitig ziehen (Tablet).
- **Rückgängig:** jede DROP-Aktion → `UndoStack` (30 Schritte, pro Raum).
- **Umsetzung (Phase 02, verbindlich):**
  - API in Welt-cm: `DragController.press/move/release(id, world)`; Eingabe-Events werden nur übersetzt (Maus = id 1000, Touch = index). Tests und Skripte (`scripted_move`, später NPCs) nutzen denselben Weg.
  - **Greif-Versatz** = Pivot − Punkt beim *Antippen* (nicht beim Anheben): Die angefasste Stelle bleibt unter dem Finger.
  - **Tippen** = < 8 px und ≤ 300 ms → `on_tap()` (Behälter öffnen/schließen, sonst Hüpfer). Feste Dinge ohne Funktion geben das Event an die Kamera weiter (scrollen).
  - **Greifen:** Treffer auf sichtbaren Pixeln (Alpha-BitMap je Textur) oder in der Mindest-Tippfläche 48 dp / Zoom. Reihenfolge: *direkt getroffen* vor *nur Tippfläche* → Tiefe (y des Boden-Vorfahren) → Schachtelung → kleinere Fläche.
  - **Zielsuche** (`Placement.find_target`): offener Behälter unter dem Finger (der **innerste** gewinnt) → höchste Fläche mit Oberkante ≥ Pivot − 10 cm (Raum-Flächen, Item-Flächen wie Tische, Stapel-Spitzen) → Boden. Im Bodenband gewinnt ein Ziel bis 10 cm unterhalb des Pivots noch vor dem Boden.
  - **Ablehnung** (Grund als Text, `deny`-Sound): Möbel/Fixture/Figur auf Flächen · > 60 cm (S-11) · breiter als die Fläche · höher als der Platz bis zur Fläche darüber · Stapel > 8 · Behälter zu klein/voll/> 2 Ebenen → Item landet auf dem Boden **15 cm vor** der Fläche.
  - **Eltern-Knoten:** Boden & Raum-Flächen → `YSortRoot` (Skalierung = Tiefen-Faktor); Tisch/Stapel → `OnTop` des Ziel-Items (lokal ×1, wandert mit); Behälter → `Contents`.
  - **Behälter-Inhalt** in **echter Größe** als Regal-Layout (Reihen, unten bündig, nach Platz sortiert); die Innenfläche wächst bei Bedarf nach oben, nichts steht über. Herausnehmen ordnet neu.
  - **Tisch-Oberkante** aus dem Sprite gemessen: `surface_frac_y` (Anteil von oben, z. B. Stil-C-Tisch 0,12 → 66 cm). Ohne Angabe: `surface_h_cm`.
  - Ruhende Items ticken nicht (`_process` aus); Animationen nur über Tweens. Tests schalten `animate = false`.

### 4.2 Hand & Griff (P03, umgesetzt)
- `CharacterRig` baut `HandSlot` vorne (Index 0), hinten (1) und „beide Hände“ (2). Beim Übergeben wird das
  Item Kind des Slots, Position = `CharacterRig.grip_local(item)` (Griffpunkt exakt auf dem Slot-Ursprung),
  Rotation = `hold_angle` (Slot dreht sich gegen den Arm, damit das Item aufrecht bleibt).
- **Zeichenreihenfolge:** Arm (Haut, Ärmel, Handfläche) < Item < **Finger-Ebene** (`hand_front`, liegt vor dem
  Item). Beim Zwei-Hand-Griff schaltet die Finger-Ebene in die Ebene `HandsTop` über dem Item um
  (Test: `test_draw_order_arm_item_hand`).
- `two_hands` (Wasserball, Katze, Wassermelone): Item sitzt mittig zwischen beiden Händen, die **Arme werden
  aus der Item-Breite gerechnet** – die Hände greifen links und rechts, nicht über Kreuz. Belegt beide Hände:
  `hand_slots()` ist danach leer.
- `SpriteCharacter` (fertig gemaltes Mädchen, `char_girl_01`): ein Hand-Slot an der gemessenen Faust-Position
  (`grip_px` aus `char_girl_01.json`) + Faust-Ebene, die nur beim Halten sichtbar ist.
- Gemessene Genauigkeit: Griff-Abstand **0,00 cm**, gehaltene Größe unverändert (Apfel 7,8 cm, Karotte 20,6 cm).

### 4.3 Sitzen & Liegen (P03, umgesetzt)
- `Seats` liefert Plätze aus der **Maßstab-Tabelle**: `seat_h_cm` Stuhl/Hocker 45, Sofa/Sessel 42, Bett 45;
  `seat_slots` (Sofa 3, Stuhl/Bett 1); Platzbreite 70 % der Möbelbreite.
- Die Figur rastet ein, wenn ihr **Becken-Punkt** innerhalb 30 cm losgelassen wird
  (`Seats.CHARACTER_SNAP_CM`); Figuren werden über `hip_offset()` einsortiert, der Knoten-Ursprung (Füße)
  steht danach `Hüfthöhe` unter dem Sitzpunkt. Items (Teddy, Tier) rasten mit dem Pivot ein.
- Pose kommt aus dem Möbel (`seat_pose`): `sit` (Stuhl/Sofa/Sessel) oder `lie` (Bett).
  - `sit`: Beine hängen ab der Hüfte, Knie auf Sitzhöhe; reicht das Schienbein nicht bis zum Boden
    (Erwachsene auf 42 cm), verkürzt es sich perspektivisch (min. Faktor 0,55) → **Füße stehen auf, nie
    darunter** (gemessen: Erwachsene 0,0 cm, Kind baumelt 23,0 cm).
  - `lie`: Körper um die Hüfte waagerecht gedreht, um die halbe Rumpfdicke über die Matratze gehoben,
    **Kopf bleibt aufrecht** (eigener `HeadPivot`, um die halbe Kopfdicke angehoben), beide Arme liegen oben.
- Beim Aufstehen/Abheben wechselt die Pose zurück auf `stand`; der `Swing`-Knoten pendelt am Griffpunkt
  (Feder, gedämpft, ±0,55 rad).
- Nur `character`, `pet`, `toy` dürfen sich setzen – Geschirr & Co. nutzen die Abstellfläche.

### 4.4 Tiefe & Sortierung
`YSortRoot` mit `y_sort_enabled`. Item-y (cm) = Tiefe im Bodenband bzw. die Tiefe der Oberfläche. Skalierung =
`depth_factor(y)` (max. 1,12) gilt für **alle** Objekte gleich – Figuren und Tiere eingeschlossen
(Test: `test_depth_factor_applies_to_characters`). Dadurch bleibt der Hund in **jeder** Tiefe kleiner als der
Tisch (49,4 cm gegen 77,8 cm, auch vorne gegen hinten).

### 4.5 NPC-Zustandsmaschine
Basis-Zustände für jede Rolle: `idle`, `work` (rollenspezifisch), `react`, `carried`, `return_to_post`. Übergänge per Timer, Ereignis (Item an Kasse, Glocke, Tor) oder Spieler-Aktion. **Garantien (getestet):** NPC blockiert nie einen Drop, verlässt nie seinen Raum, kehrt spätestens nach `return_after_s` zurück.

### 4.6 PetBrain (Utility light)
Bedürfnisse (0–1): Hunger, Spieltrieb, Müdigkeit, Zuneigung. Sie steigen langsam, die höchste gewinnt die Aktion (Napf, Ball, Körbchen, der Besitzerin folgen). **Rein kosmetisch:** Tiere werden nie krank oder traurig. Laute über den `AudioBus`-Limiter, das Intervall pro Tier ist zufällig 15–60 s.

### 4.7 Rucksack
20 Plätze, überall sichtbar (HUD). Items hineinziehen → werden aus dem Raum entfernt und im Rucksack gespeichert, herausziehen → erscheinen am Finger.

## 5. Performance-Budgets
| Wert | Budget |
|---|---|
| FPS | 60 (Referenz: Tablet von 2019 / Web auf Mittelklasse-Laptop), mind. 30 auf schwachen Geräten |
| Lose Items pro Raum | ≤ 250 |
| Aktive NPCs + Tiere pro Raum | ≤ 15 |
| RAM pro Bereich | < 250 MB |
| Bereichswechsel | < 2 s |
| Web-Download | < 150 MB (Bereiche als PCK nachladen, falls nötig) |

## 6. Tests (Mindestumfang)
- `tests/test_scale.gd`: ItemDB lädt, jede Definition hat gültigen `scale_ref`, Welt-Höhe = Tabelle × mul
- `tests/test_drag_drop.gd`: Drop auf Tisch → Pivot-Höhe = Tischhöhe; Drop ins Leere → fällt auf den Boden
- `tests/test_hand.gd`: Grip landet auf HandSlot-Position (±0,5 cm)
- `tests/test_depth.gd`: Faktor 1,00 hinten, 1,12 vorne, nie größer
- `tests/test_save_migration.gd`: alte Speicherdateien laden
- `tests/test_no_network.gd`: kein `HTTPRequest`, `HTTPClient`, `WebSocketPeer`, `StreamPeerTCP`, `PacketPeerUDP` in `src/`
- `tools/tests/test_pipeline.py`: Freistellen (Augenweiß bleibt, Henkel-Loch wird transparent), Reihenfolge, Maßstab

### 6.1 Beweis-Werkzeuge (statt Augenmaß)
Jede Phase liefert Zahlen, nicht nur Bilder. Alle Läufer starten mit
`xvfb-run -a godot --rendering-driver opengl3 --resolution <W>x<H> -s tools/godot/run.gd -- res://tools/godot/<datei>.gd [arg]`.

| Läufer | Was er misst |
|---|---|
| `p02_perf_runner.gd` | 250 Items: Spawn-, Greif-, Zielsuche-Zeit |
| `p03_pose_dump.gd` | jede Figur-Ebene in cm über dem Standpunkt, je Pose |
| `p03_check.gd` | 37 Akzeptanz-Prüfungen (Griff, Sitz-, Liegehöhe, Größen, Tier) → `p03_messwerte.json` |
| `p03_scenario_runner.gd` | Beweisbilder; prüft je Bild „im Bild / angeschnitten“ |
| `p03_reference_kueche.gd` | Referenz-Küche nachmessen (Soll cm gegen gemessene Bildgröße) |

**Silhouetten-Differenz** (in `p03_check.gd`, `p03_reference_kueche.gd`): Item-Ebenen ausblenden, zweites
Bild rendern, Differenz → Bounding-Box in Pixel → cm über den Kamera-Maßstab. Damit zählt nur, was wirklich
sichtbar ist: verdeckte Teile (Finger vor dem Apfel) werden korrekt nicht mitgemessen.

Deterministisch: `PetNode.autonomous = false` (Tiere nur per `tick()`), `CharacterRig.animate_poses = false`
(Posen springen), `AudioBus.clock` als Fake-Uhr, `drag.animate = false`.
