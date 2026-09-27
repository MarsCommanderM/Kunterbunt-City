# Asset-Einstellungen für den Menschen 👤 (ComfyUI, 0 €)

> Phase 06 · P06-T12. Alles hier ist **kostenlos**: lokal statt Cloud, offene
> Modelle, freie Werkzeuge. Kein Kauf, kein Abo, keine Lizenz-Falle.
> Prompt-Vorlagen mit Begründung: [`03_STIL_GUIDE_C.md`](03_STIL_GUIDE_C.md) §3.

## 1. Der Kreislauf

```
👤 1. Generieren      ComfyUI (lokal)  →  incoming/<bereich>/<blatt>.png
👤 2. Beschreiben     incoming/<bereich>/<blatt>.yaml  (IDs in Lesereihenfolge)
🤖 3. Pipeline        python3 tools/asset_pipeline/run.py incoming/<bereich>
🤖 4. Prüfen          Lineup-Bild ansehen + Warnungen lesen  →  OK oder neu generieren
```

Ein **neues Blatt landet ohne Code-Änderung im Spiel**: `run.py` schreibt die
Sprites nach `assets/sprites/<bereich>/` und trägt die Items in
`data/items/<datei>.json` ein (Bestehendes wird aktualisiert, nichts dupliziert).

## 2. ComfyUI einrichten (einmalig, lokal, kostenlos)

| Einstellung | Empfehlung |
|---|---|
| Modell | **SDXL**-Feingewicht mit offener Lizenz (z. B. SDXL 1.0, DreamShaper XL, Juggernaut XL) – Downloads wiegen 6–7 GB, läuft ab GTX 1060/8 GB |
| Auflösung Item-Blatt | **1024 × 1024** (SDXL) – bei 9–15 Objekten reicht das; KI-Blatt erst ab 1536×1536, wenn die Einzelteile < 1024 px breit werden |
| Auflösung Raum | **1536 × 864** (16:9) |
| Sampler / Scheduler | DPM++ 2M Karras |
| Schritte | 25–35 |
| CFG | 5,5–7 (Stil-Block „zieht“ sonst zu hart) |
| Seed | festhalten (bei Treffern notieren) – nur so ist der Lauf reproduzierbar |
| Karten-Trennung | Abstand zwischen Objekten ≥ 40 px, sonst schneidet `split.py` sie zusammen |
| Speicherformat | PNG, ohne eingebettete Prompt-Texte (sonst Land-Text im Bild) |

**Negativ-Prompt (in JEDEN Lauf):**

```
text, letters, watermark, logo, signature, photo, realistic, 3d render,
black outlines, harsh shadows, cropped, cut off, multiple views of same object, scary
```

**Stil-Block (in JEDEN Prompt, Wortlaut exakt wie Stil-Guide §3):**

```
high-end modern vector illustration style for a premium children's game, crisp clean rounded shapes,
rich soft gradients, soft painted shading, light from top left, glossy highlights, subtle grain texture,
thin darker colored outlines (not black), warm harmonious colors, cute and friendly
```

### Blatt-A-Item-Blatt (Vorlage)

```
Game asset sheet, <STIL-BLOCK>. <N> separate objects arranged in a neat grid with large empty spacing,
each object fully visible, not touching, front view slightly from above: <LISTE: 1 …, 2 …, 3 …>.
Plain pure white background, no cast shadows, no text, no labels.
```

* **Nur ähnliche Größenklasse pro Blatt** (Küche klein, Möbel groß …).
  Die echte Größe kommt nie aus dem Bild, sondern aus `data/scale_table.json`.
* Reihenfolge im Prompt = Reihenfolge in der YAML. Zeile für Zeile, links → rechts.
* YAML-Beispiel: [`reference/raw_items.yaml`](../reference/raw_items.yaml)
  (`sheet`, `area`, `room`, `items_json` optional, `items:` mit `id` + `scale_ref`).

### Blatt-B-Leerer Raum (Hintergrund)

```
Premium children's game background, <STIL-BLOCK>. Side-view cross-section of an EMPTY <RAUM> like a dollhouse
room, wide 16:9, straight-on camera, flat horizontal floor line, only fixed built-in elements: <EINBAUTEN>.
The floor is completely EMPTY: no people, no animals, no loose furniture, no loose objects. No text.
```

* Einbauten = alles, was in `05_WELT_UND_BEREICHE.md` mit 🔒 markiert ist.
  **Bewegbares nie in den Hintergrund malen.**
* Anschließend einmessen:
  `python3 tools/asset_pipeline/calibrate_bg.py data/areas/<bereich>.json --room <raum>`
  (Arbeitsplatte = 90 cm, Kacheln ≤ 2048 px – siehe Datei-Kopf).

### Blatt-C/D – Figurenteile (Schablone → Teil-Ebene)

1. Schablone generieren (Stil-Guide §3C: Unterwäsche-Basis, Glatze, neutral).
2. Variante per **img2img/Inpainting auf der Schablone** erzeugen
   (Stil-Guide §3D; Denoise 0,55–0,75).
3. Differenz zur Schablone als Teil-Ebene:

```bash
python3 tools/asset_pipeline/figure_parts.py neu.png schablone.png \
    --name hair_front_mohawk --template kid --anchor 23.8 29.84
```

   Anker immer in **cm von unten-links** wie in `assets/characters/parts/parts.json`
   (Kopf = oben Mitte, Schulter = oben, Hüfte = unten …). Ergebnis: PNG +
   `parts.json`-Eintrag (Upsert). Vorschau: `--threshold` erhöhen, wenn zu viel
   hängenbleibt; leere Differenz → Schablone stimmt nicht.

### Blatt-E – Tiere

```
Single animal game asset, <STIL-BLOCK>. A cute <TIER>, <POSE: sitting side view facing right>, full body visible,
plain pure white background, no shadow, no text.
```

## 3. Nach dem Lauf: die drei Checks

1. **Warnungen lesen** – `run.py` meldet z. B.
   `Breite 14,2 cm weicht >30 % von Tabellen-Breite ab` → Blatt neu generieren
   oder in der YAML `scale_ref`/`scale_mul` korrigieren.
2. **`docs/tests/lineup_<bereich>.png` ansehen** – Kind, Hund, Tisch stehen
   am Lineal daneben. Wirkt ein Apfel wie ein Fußball → nicht akzeptieren.
3. **`python3 tools/validate_scale.py`** muss grün sein (läuft auch in
   `scripts/check.sh` und in CI). Rot = nicht committen.

Häufige Fehler:

| Symptom | Ursache | Fix |
|---|---|---|
| `X Objekte gefunden, Y erwartet` | Karten zu nah beieinander oder YAML-Reihenfolge falsch | Blatt neu generieren (mehr Abstand) oder YAML korrigieren – das Vorschaubild `*_split_preview.png` nummeriert die Funde |
| Elemente hängen zusammen | Berührung/Dilation | Abstand ≥ 40 px im Prompt erzwingen |
| Weiße Inseln im Sprite | zu wenig Weiß im Hintergrund | Prompt „plain pure white background“ betonen |
| Matschige Details | Objekt zu klein auf dem Blatt | eigene Blätter pro Größenklasse, nie alles auf eins |

## 4. Stil-Konsistenz: LoRA (optional, kostenlos)

Wenn die Ergebnisse trotz Stil-Block „driften“, trainiere **einen Stil-LoRA**
statt Prompts nachzubessern – alles lokal und frei:

1. **Daten**: 20–40 der besten eigenen Bilder (alles aus dieser Pipeline!),
   quadratisch zugeschnitten, nur Stil-Beispiele – keine fremden Künstler-Bilder.
2. **Werkzeug**: [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts)
   (MIT-Lizenz) oder das Kohya-Web-UI; SDXL-LoRA, Rang 16–32.
3. **Parameter**, die sich bewährt haben: 1.000–1.500 Schritte gesamt,
   LR 1e-4 (AdamW8bit), Text-LR 5e-5, Batch 1–2, Seed fest.
4. **Nutzen**: LoRA mit Gewicht **0,6–0,8** in ComfyUI dazuladen, Stil-Block
   trotzdem drinlassen. Nie über 0,9 – sonst kippt es ins „LoRA-Look“.
5. **Abnahme** wie immer: ein Test-Blatt erzeugen, Lineup ansehen, erst dann
   die große Welle.

Kostenpunkt: 0 €. Braucht nur Festplattenplatz und eine GPU mit ≥ 8 GB
(für SDXL-LoRA reicht eine RTX 3060 12 GB / gebrauchte Karten ab ~100 € –
falls gar keine GPU da ist: ohne LoRA weitermachen, Stil-Block reicht meist).

## 5. Qualitätserwartung (Stil C, „besser als Toca Boca“)

* Kanten sauber, kein weißer Saum (macht `cutout.py`), keine Text-Reste.
* Größenverhältnisse **im Blatt** plausibel (Karotte kleiner als der Tisch) –
  die Zahlen kommen ohnehin aus der Tabelle.
* Ein Blatt = ein Stil-Load. Bei sichtbaren Stilbrüchen: LoRA-Schritt §4.
* Alles Prüfbare ist automatisiert: bei grünem `scripts/check.sh` ist die
  Pipeline in Ordnung; **die menschliche Entscheidung bleibt Lineup-Blick
  und „fühlt sich das Kind-Spiel richtig an?“**
