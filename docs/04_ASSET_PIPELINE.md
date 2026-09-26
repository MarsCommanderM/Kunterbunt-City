# 04 · Asset-Pipeline (0 €) 🏭
> Referenz-Implementierung (funktioniert, Demo): `reference/pipeline_demo_kueche.py` → erzeugte `reference/kueche_stil_c_massstab.png`.
> In **Phase 6** baut der Agent daraus das produktive Werkzeug `tools/asset_pipeline/`.

## 1. Ablauf

```
👤 1. Generieren   ComfyUI + Stil-Block + LoRA  →  incoming/<bereich>/<blatt>.png  (+ blatt.yaml: Liste der IDs in Lesereihenfolge)
🤖 2. Freistellen  cutout.py   weiß → transparent (Flood-Fill vom Rand), Löcher >500 px & sehr weiß → transparent,
                               Figuren: Löcher AUS (Augenweiß!), Kanten-Entmischung (kein weißer Saum)
🤖 3. Zerlegen     split.py    Objekte finden, Zeilen nach vertikaler Mitte, dann links→rechts, Anzahl muss = YAML
🤖 4. Maßstab      scale.py    Höhe aus scale_table (scale_ref, scale_mul) → Breite aus Seitenverhältnis → Warnung bei >30 % Abweichung
🤖 5. Punkte       points.py   Pivot (unten Mitte), Grip (Vorgabe je Kategorie, im Vorschaubild korrigierbar)
🤖 6. Export       export.py   PNG mit 8 px/cm (2× Referenz), Kanten-Padding 4 px, → assets/sprites/<bereich>/, Item-JSON → data/items/
🤖 7. Atlas        atlas.py    pro Bereich ein Atlas (max. 4096²), Godot-Import: Filter an, Mipmaps an, VRAM-komprimiert
🤖 8. Prüfen       validate_scale.py + lineup.py (Lineup-Bild) + scene_test.py (Test-Szene mit Kind/Hund/Tisch)
👤 9. Blick-Check  Lineup & Test-Szene ansehen → OK oder Blatt neu generieren
```

## 2. Blatt-Beschreibung (YAML, pro generiertem Bild)
```yaml
sheet: home_kitchen_small_01.png
area: home
room: kitchen
items:            # exakt in Lesereihenfolge (Zeile für Zeile, links → rechts)
  - { id: food_carrot,        scale_ref: food_carrot }
  - { id: food_apple_red,     scale_ref: food_apple }
  - { id: kitchen_mug_pink,   scale_ref: kitchen_mug }
  - { id: kitchen_cup_orange, scale_ref: kitchen_mug, scale_mul: 0.9 }
```

## 3. Benennung
`<bereich|kategorie>_<ding>_<variante>` in snake_case, Englisch: `food_apple_red`, `home_chair_mint`, `shop_register_01`.
Figurenteile: `char_<schablone>_<slot>_<name>`, z. B. `char_kid_hair_pigtails_brown`.

## 4. Auflösung & Speicher
- Quelle: **8 px/cm** (Kind 125 cm → 1.000 px hoch; Apfel 8 cm → 64 px)
- Kleinste Items: mind. 64 px Kantenlänge (sonst werden Details matschig) → ggf. mit höherer Dichte exportieren, die Weltgröße bleibt gleich
- Hintergründe: 8 px/cm → ein 6 m breiter Raum = 4.800 px (als 2–3 Kacheln à ≤ 2.048 px)

## 5. Platzhalter (bis echte Grafik da ist)
`tools/make_placeholders.py` erzeugt pro `scale_table`-Eintrag ein PNG: abgerundetes Rechteck in Kategorie-Farbe, Umriss, Kurzname und Größe in cm. Die cm-Maße sind exakt, das Seitenverhältnis kommt aus w/h der Tabelle. **Der Tausch gegen die echte Grafik ist nur ein anderer Sprite-Pfad im JSON.**

## 6. Bekannte Fallen (aus dem Demo gelernt)
| Problem | Lösung |
|---|---|
| Augenweiß wurde transparent | bei Figuren/Tieren keine Loch-Entfernung |
| Tassenhenkel-Loch blieb weiß | eingeschlossene Flächen > 500 px und Mittelwert > 250 entfernen |
| Reihenfolge vertauscht (Tulpe ↔ Teddy) | Zeilen über die **vertikale Mitte** bilden, nicht über die Oberkante |
| KI liefert mehr Items als bestellt | Anzahl gegen YAML prüfen → Fehler statt raten |
| KI-Raum zu hoch | Hintergrund einmessen (Maßstab-Bibel §6) |
