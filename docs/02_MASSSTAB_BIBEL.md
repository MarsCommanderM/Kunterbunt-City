# 02 · Maßstab-Bibel 📏
> **Ziel:** Alles in Kunterbunt City ist **zueinander richtig groß**. Kein Apfel wie ein Fußball, kein Hund größer als der Tisch, keine Karotte wie ein Baseballschläger.
> **Quelle der Wahrheit:** `data/scale_table.json` (155+ Einträge) + `data/scale_rules.json` (43+ Regeln), geprüft von `tools/validate_scale.py`.
> **Referenzbilder:** `reference/kueche_stil_c_massstab.png` (Spielansicht) · `reference/lineup_stil_c.png` (alle Größen am Lineal)

---

## 1. Grundformel

```
1 Godot-Einheit = 1 cm
Welt-Höhe eines Sprites (cm)   = scale_table[scale_ref].h_cm × scale_mul        (scale_mul 0,7–1,3; Standard 1,0)
Sprite-Skalierung in Godot     = Welt-Höhe_cm / Textur-Höhe_px                (gleicher Faktor für x und y)
Tiefen-Faktor                  = 1 + 0,12 × t      mit t = 0 (hintere Bodenlinie) … 1 (vordere Bodenlinie)
Kamera-Zoom                    = Viewport-Höhe_px / sichtbare_Höhe_cm         (Standard 300 cm)
```

**Beispiel Karotte:** `food_carrot` h = 20 cm · Sprite-Textur 160 px hoch → `scale = 20/160 = 0,125` · steht das Kind vorne (t = 1), dann ist alles dort ×1,12, **auch das Kind selbst**. Das Verhältnis bleibt also gleich.

```gdscript
# src/items/item_node.gd (Ausschnitt)
func apply_world_size(def: ItemDefinition) -> void:
    var tex_h: float = $Sprite2D.texture.get_height()
    var world_h_cm: float = def.height_cm * def.scale_mul
    var s: float = world_h_cm / tex_h
    $Sprite2D.scale = Vector2(s, s)
    $Sprite2D.offset = Vector2(-def.pivot.x, -def.pivot.y) * $Sprite2D.texture.get_size()  # Pivot → Ursprung

# src/world/depth_sort.gd
static func depth_factor(y_cm: float, floor_back_y: float, floor_front_y: float) -> float:
    var t: float = clampf((y_cm - floor_back_y) / (floor_front_y - floor_back_y), 0.0, 1.0)
    return 1.0 + 0.12 * t
```

---

## 2. Referenzgrößen (Auszug – vollständig in `scale_table.json`)

### Figuren (Stil „großer Kopf“ seit P04b – Kind ≈ 2 Kopfhöhen; werden **nie** skaliert außer Tiefen-Faktor)
| Baby | Kleinkind | **Kind** | Teen | Erwachsen | Senior |
|---|---|---|---|---|---|
| 55 | 90 | **125** | 155 | 172 | 165 cm |

### Welt & Einbauten
| Tür | Raumhöhe | Arbeitsplatte | Esstisch | Couchtisch | Stuhl (Sitz) | Sofa (Sitz) | Bett Kind | Kühlschrank | Badewanne |
|---|---|---|---|---|---|---|---|---|---|
| 200 | 260 | 90 | 75 | 45 | 90 (45) | 85 (42) | 45 | 180 | 55 cm |

### Haustiere (sitzend)
| Hamster | Meerschw. | Kaninchen | Katze | Hund klein | **Hund mittel** | Hund groß | Pony (stehend) |
|---|---|---|---|---|---|---|---|
| 7 | 12 | 22 | 28 | 28 | **45** | 65 | 125 cm |
→ **Jeder Hund ist kleiner als der Esstisch (75 cm).** Diese Regel wird geprüft.

### Kleine Items
| Ei | Apfel | Tasse | Schoko-Ei | Eis | **Karotte** | Buch | Fußball | Teddy | Wasserball | Blumentopf |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 8 | 10 | 10 | 17 | **20** | 22 | 22 | 30 | 30 | 30 cm |
→ **Apfel (8) < Fußball (22)**: geprüft. **Karotte (20) ≪ Schläger (80)**: geprüft.

### Große Dinge (Kamera zoomt raus, nichts wird geschrumpft)
| Auto | Bus | Basketballkorb | Elefant | Giraffe |
|---|---|---|---|---|
| 155 × 380 | 300 × 1100 | 305 | 300 | 480 cm |

---

## 3. Größen-Regeln (Auszug aus `scale_rules.json`)

| Typ | Beispiel | Bedeutung |
|---|---|---|
| `lt` | `pet_dog_large < home_table_dining` | a muss kleiner sein als b |
| `hold_max` | `two_hands ≤ 60 cm` | tragbare Größe begrenzt |
| `surface_fit` | Items mit `placement: table` ≤ 60 cm | passt auf einen Tisch |
| `category_range` | `food` 2–35 cm | Ausreißer-Schutz |
| `seat_below_table` | Stuhlsitz ≥ 20 cm unter Tischplatte | Figur passt an den Tisch |

**Neue Regeln hinzufügen:** Immer wenn ein Größenfehler auffällt, bekommt er eine Regel. So kann er nie wieder passieren.

---

## 4. Bodenband & Tiefe

```
   Rückwand ──────────────────────────────────────────  y = floor_back_y   (t = 0, Faktor 1,00)
      │   Figuren, Tiere, Möbel stehen IRGENDWO im Band
      │   Sortierung: größeres y = weiter vorne = später gezeichnet
   Vorderkante ───────────────────────────────────────  y = floor_front_y  (t = 1, Faktor 1,12)
```
- Standard-Tiefe des Bodenbands: **60–120 cm** Welt-Tiefe (je Raum in `data/areas/*.json`).
- Items auf Oberflächen (Tisch) übernehmen den Tiefen-Faktor der Oberfläche.
- **Nie mehr als 1,12**, sonst wirken vordere Dinge zu groß (Fehler aus v1.x).

---

## 5. Kamera

| Situation | Sichtbare Höhe |
|---|---|
| Innenräume (Standard) | **300 cm** |
| Zoom-Bereich innen | 220–450 cm (Pinch) |
| Außen (Garten, Pausenhof, Spielplatz, Straße) | 350–600 cm |
| Zoo (Giraffe), Rummel (Riesenrad) | bis 700 cm |

Die Kamera scrollt horizontal durch breite Räume (Puppenhaus-Querschnitt). Vertikal scrollt sie nur in hohen Szenen (Riesenrad, Sprungturm).

---

## 6. Hintergründe einmessen (S-10)

1. 👤 Hintergrund generieren (nur Einbauten, siehe Stil-Guide).
2. Im Bild ein **Referenzmaß** markieren: Arbeitsplatte (90 cm) oder Tür (200 cm). Dazu die obere und untere y-Koordinate in `data/areas/<bereich>.json` unter `calibration` eintragen.
3. Tool `tools/asset_pipeline/calibrate_bg.py` berechnet px/cm, skaliert den Hintergrund auf **8 px/cm** (2× Referenz), trägt `floor_back_y`, `floor_front_y` und die Oberflächen (Arbeitsplatte, Fensterbank, Regale) in cm ein.
4. Prüfen: Die Test-Szene platziert automatisch Kind, Hund, Tisch und Apfel. Wirkt alles richtig? (👤 Blick-Check, Screenshot in `docs/tests/`)

---

## 7. Checkliste: neues Item anlegen

- [ ] Passender Eintrag in `scale_table.json` vorhanden? Wenn nicht: **echte Größe recherchieren** und Eintrag anlegen (h, w, hold, placement)
- [ ] Item-JSON mit `scale_ref`, optional `scale_mul` (0,7–1,3)
- [ ] `pivot` (unten Mitte, außer bei Wand-Items: oben Mitte), `grip` falls tragbar, `hold_angle`
- [ ] `python3 tools/validate_scale.py` grün (auch keine Seitenverhältnis-Warnung)
- [ ] Im Lineup und in der Test-Szene angesehen

## 8. Typische Fehler & Lösung

| Fehler | Ursache | Lösung |
|---|---|---|
| Item wirkt riesig | falscher `scale_ref` oder `scale_mul` > 1,3 | Tabelle prüfen |
| Seitenverhältnis-Warnung | KI hat zu breit/schmal gezeichnet oder Rand nicht abgeschnitten | neu generieren oder zuschneiden |
| Dinge vorne zu groß | Tiefen-Faktor > 1,12 | Raum-Daten prüfen |
| Alles winzig | Hintergrund nicht eingemessen | Kalibrierung (Abschnitt 6) |
| Item schwebt über dem Tisch | Pivot falsch oder Oberflächenhöhe falsch | Pivot = Unterkante, `surface_h_cm` prüfen |
| Hand greift daneben | `grip` falsch | Grip im Pipeline-Vorschaubild korrigieren |
