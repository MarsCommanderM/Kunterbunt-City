# PHASE 06 · Asset-Pipeline (produktiv)
**Ziel:** Aus KI-Bildern werden mit **einem Befehl** fertige, maßstabsgetreue Sprites samt Item-JSON und Atlas, inklusive automatischer Prüfung.
**Voraussetzung:** Phase 02 (ItemDB/Platzhalter). Kann parallel zu 04/05 laufen.
**Referenz:** `reference/pipeline_demo_kueche.py` (funktionierende Demo) + `docs/04_ASSET_PIPELINE.md`.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P06-T01 | `tools/asset_pipeline/cutout.py` aus der Demo übernehmen und härten: Loch-Regel (> 500 px, Mittelwert > 250), Modus `character` (keine Löcher), Kanten-Entmischung + pytest mit Testbildern (Augenweiß bleibt, Henkel wird transparent) |
| P06-T02 | `split.py`: Objekte finden, Zeilen über die vertikale Mitte, Anzahl == YAML, sonst Fehler mit Vorschaubild der gefundenen Objekte |
| P06-T03 | `scale.py`: Höhe aus `scale_table` × `scale_mul`, Breite aus dem Seitenverhältnis, Warnung bei > 30 % Abweichung |
| P06-T04 | `points.py`: Pivot + Grip-Vorgaben je Kategorie (z. B. Tasse → Henkel = rechte Kante 45 % Höhe), Vorschaubild mit markierten Punkten zum Korrigieren (YAML-Override) |
| P06-T05 | `export.py`: 8 px/cm, 4 px Padding, `assets/sprites/<bereich>/…png`, Item-JSON in `data/items/` (bestehende Einträge aktualisieren, nicht duplizieren) |
| P06-T06 | `atlas.py`: Atlas pro Bereich (≤ 4096², Godot-kompatibel) + Import-Einstellungen |
| P06-T07 | `calibrate_bg.py` (aus Phase 01) fertigstellen: Hintergründe einmessen, in Kacheln ≤ 2048 px zerlegen |
| P06-T08 | `lineup.py`: alle Items eines Bereichs + Kind + Hund + Tisch am cm-Lineal → `docs/tests/lineup_<bereich>.png` |
| P06-T09 | `scene_test.py`: Test-Komposition wie die Referenz-Küche (Kind hält ein Item, Teddy auf dem Stuhl, Items auf dem Tisch) |
| P06-T10 | `run.py incoming/<bereich>/` = alles in einem Durchlauf (2→8) + Zusammenfassung (neu/aktualisiert/Warnungen) |
| P06-T11 | Figurenteile-Modus: Differenz Teil-Bild − Schablone → Teil-Ebene, Ausrichtung an Schablonen-Ankern (Kopf, Hals, Hüfte, Hände) |
| P06-T12 | Anleitung `docs/asset_settings.md` für 👤: ComfyUI-Einstellungen, Stil-Block, Negativ-Prompt, LoRA-Training (kostenlos) |

## Akzeptanzkriterien
- [ ] `python3 tools/asset_pipeline/run.py reference/` erzeugt aus den Demo-Rohbildern dieselben 18 Sprites + JSON wie die Referenz
- [ ] Maßstab-Prüfer grün, keine Seitenverhältnis-Warnung für die Demo-Items
- [ ] Lineup- und Test-Szenen-Bild werden erzeugt
- [ ] Neues Blatt → im Spiel sichtbar, ohne Code-Änderung
- [ ] pytest-Abdeckung für cutout/split/scale
- [ ] `check.sh` grün

## 👤 Mensch
ComfyUI + Modell lokal einrichten, erste echte Blätter für die Zuhause-Küche generieren (Stil-Guide §3A/3B), in `incoming/home/` legen, Lineup ansehen.

## Startprompt
> Lies MASTERPROMPT.md, docs/03_STIL_GUIDE_C.md, docs/04_ASSET_PIPELINE.md, reference/pipeline_demo_kueche.py und docs/phasen/PHASE_06_ASSET_PIPELINE.md. Baue die produktive Pipeline. Maßstab kommt ausschließlich aus data/scale_table.json. Phasenbericht und stoppen.
