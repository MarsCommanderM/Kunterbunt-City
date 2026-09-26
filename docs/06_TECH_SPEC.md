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

### 4.2 Hand & Griff
- `CharacterRig` hat `HandSlot` rechts und links (Marker2D). Beim Übergeben: Item wird Kind des HandSlots, `offset = −grip × Texturgröße`, Rotation = `hold_angle`.
- **Zeichenreihenfolge:** Arm-Ebene < Item < **Hand-Ebene** (Finger liegen über dem Item).
- `two_hands`: Figur wechselt in die Pose „trägt vor Bauch“, das Item sitzt mittig zwischen beiden HandSlots.

### 4.3 Sitzen & Liegen
`SeatSlot` (Position, Sitzhöhe cm, Pose `sit`/`lie`/`ride`, Blickrichtung). Die Figur rastet ein, wenn ihr Becken-Punkt in einem Radius von 30 cm losgelassen wird. Items können auch auf SeatSlots sitzen (Teddy auf dem Stuhl).

### 4.4 Tiefe & Sortierung
`YSortRoot` mit `y_sort_enabled`. Item-y (cm) = Tiefe im Bodenband bzw. die Tiefe der Oberfläche. Skalierung = `depth_factor(y)` (max. 1,12) gilt für **alle** Objekte gleich.

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
