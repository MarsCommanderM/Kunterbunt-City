# 03 · Stil-Guide „Stil C – Premium Vektor“ 🎨
> Referenzen: `reference/stil_C_premium_vector.png` (Zielbild) · `reference/kueche_stil_c_massstab.png` (echte Szene aus Einzelteilen) · `reference/sprites/` (freigestellte Beispiele)

## 1. Stil-Regeln

| Merkmal | Regel | ❌ Nicht |
|---|---|---|
| Formen | klar, weich, rund, freundlich | spitz, kantig, realistisch-fotografisch |
| Linien | dünne Umrisslinie in **dunklerer Eigenfarbe** | schwarze Comic-Linien, gar keine Linien |
| Licht | weiche gemalte Verläufe, Licht **oben links**, Glanzpunkte auf glatten Flächen | harte Schlagschatten, Licht von unten |
| Textur | feines Korn, Holzmaserung, Stoffstruktur (dezent) | stark verrauscht, Foto-Texturen |
| Farben | warm & harmonisch: Creme, Mint, Holz, Pastell + kräftige Akzente (Rot, Gelb, Pink, Blau) | Neon (außer Rummel abends), grau-trist |
| Figuren | ~3 Kopfhöhen (Kind), große Augen mit Glanzlicht, rosige Wangen, detaillierte Kleidung | realistische Proportionen, gruselig, sexualisiert |
| Ansicht | **frontal/seitlich** (Puppenhaus-Querschnitt), Items leicht 3/4 von vorne | Vogelperspektive, starke Perspektive |
| Vielfalt | alle Hautfarben, Haartypen, Familienformen, Hilfsmittel (Rollstuhl, Brille, Hörgerät) | Klischees |

## 2. Master-Palette (Richtwerte)
Creme `#FFF3DC` · Wand hell `#FBF1E1` · Mint `#8FCFB0` · Mint dunkel `#5FA88A` · Holz hell `#E0A76B` · Holz `#B9763F` · Holz dunkel `#7A4A26` · Rot `#E5484D` · Orange `#F59A3C` · Gelb `#FFCD3C` · Pink `#F58FB5` · Himmelblau `#6EC6F0` · Blau `#3F7FD6` · Lila `#9A7CEB` · Grün `#5DB85A` · Haut-Töne: 12 Stufen von `#FFE0CC` bis `#5A3522`

## 3. Prompt-Vorlagen (für ComfyUI, 👤)

**STIL-BLOCK (in JEDEN Prompt kopieren):**
```
high-end modern vector illustration style for a premium children's game, crisp clean rounded shapes,
rich soft gradients, soft painted shading, light from top left, glossy highlights, subtle grain texture,
thin darker colored outlines (not black), warm harmonious colors, cute and friendly
```

**A) Item-Blatt (9–15 Items pro Bild):**
```
Game asset sheet, <STIL-BLOCK>. <N> separate objects arranged in a neat grid with large empty spacing,
each object fully visible, not touching, front view slightly from above: <LISTE: 1 …, 2 …, 3 …>.
Plain pure white background, no cast shadows, no text, no labels.
```
> Regel: **Nur Items ähnlicher Größenklasse** auf ein Blatt (z. B. „Küche klein“), damit Details gleich fein werden. Die echte Größe kommt **nicht** aus dem Bild, sondern aus `scale_table.json`.

**B) Leerer Raum (Hintergrund):**
```
Premium children's game background, <STIL-BLOCK>. Side-view cross-section of an EMPTY <RAUM> like a dollhouse
room, wide 16:9, straight-on camera, flat horizontal floor line, only fixed built-in elements: <EINBAUTEN>.
The floor is completely EMPTY: no people, no animals, no loose furniture, no loose objects. No text.
```
> Einbauten = alles, was in `05_WELT_UND_BEREICHE.md` als 🔒 markiert ist. **Bewegbares nie in den Hintergrund malen.**

**C) Körper-Schablone (Charakter-Editor, 3× nötig: Kleinkind / Kind / Erwachsen):**
```
Character base template, <STIL-BLOCK>. A neutral cute <ALTER> figure, plain light grey underwear-like base
outfit, bald head, neutral friendly face, full body, front view, arms slightly away from body, standing straight,
plain pure white background, no shadow, no text.
```
**D) Editor-Teile (auf Schablone, img2img/Inpainting):** Frisur / Oberteil / Hose / Schuhe / Accessoire jeweils einzeln auf der Schablone erzeugen → freistellen → Differenz zur Schablone = Teil-Ebene. Nachbesserung in Krita.

**E) Tiere:**
```
Single animal game asset, <STIL-BLOCK>. A cute <TIER>, <POSE: sitting side view facing right>, full body visible,
plain pure white background, no shadow, no text.
```

**NEGATIV (immer):** `text, letters, watermark, logo, signature, photo, realistic, 3d render, black outlines, harsh shadows, cropped, cut off, multiple views of same object, scary`

## 4. Konsistenz über 1.000 Assets
1. Die besten 50–100 Stil-C-Bilder sammeln (`reference/` + neue Favoriten).
2. **Stil-LoRA** lokal trainieren (kostenlos, z. B. kohya_ss) → Trigger-Wort `kbcstyle`.
3. Feste Einstellungen dokumentieren (Modell, Sampler, Schritte, CFG, Auflösung) in `docs/asset_settings.md`.
4. Jedes neue Blatt: Stil-Check gegen `reference/kueche_stil_c_massstab.png`. Passt es nicht, wird es verworfen.

## 5. Stil-QA-Checkliste pro Blatt
- [ ] Linien dunkle Eigenfarbe, nicht schwarz · [ ] Licht oben links · [ ] keine Schrift/Wasserzeichen
- [ ] Objekt vollständig, nicht abgeschnitten · [ ] weißer, schattenloser Hintergrund
- [ ] Nach Freistellen: kein weißer Rand, Augenweiß vorhanden, Löcher (Henkel) transparent
- [ ] Im Lineup und in der Test-Szene stimmig
