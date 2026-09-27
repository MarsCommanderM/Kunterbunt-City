#!/usr/bin/env python3
"""P06-T11 – Figurenteile: Differenz (Teil-Bild − Schablone) → Teil-Ebene.

Wie im Rig (src/characters/character_rig.gd) und in parts.json:

* Ein Teil ist eine **tighte Box** bei **8 px/cm** (Kopf kid: 50,32 × 43,6 cm →
  403 × 349 px), Alpha-BBox des Inhalts.
* ``anchor_cm`` = Anker **von unten-links**, y nach oben (Kopf: oben Mitte,
  Schulter: oben, Hüfte: unten …) – genau so zieht das Rig die Ebene.
* ``diff_layer()``: Pixel, die sich gegenüber der Schablone geändert haben,
  werden zur Teil-Ebene (Maske aus der Farbdistanz), alles andere fällt raus.
* ``extract_part()``: ohne Schablone → Freistellen (Figuren-Modus, Augenweiß
  bleibt), mit Schablone → Differenz; Rückgabe = PNG + Meta für parts.json.
* ``save_part()``: nach ``assets/characters/parts/<schablone>/<name>.png`` +
  Upsert in ``parts.json`` (bestehende Einträge aktualisieren, nie duplizieren).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from cutout import cutout_character  # noqa: E402

PARTS_ROOT = ROOT / "assets" / "characters" / "parts"
PARTS_JSON = PARTS_ROOT / "parts.json"
PPC = 8                      # px pro cm (Konvention aller Teile)
DEFAULT_THRESHOLD = 24       # Farb-Distanz (0–255), unter der „gleich“ zählt


class PartError(Exception):
    """Teil-Bild und Schablone passen nicht zusammen o. Ä."""


def diff_layer(new_img: Image.Image, base_img: Image.Image,
               threshold: int = DEFAULT_THRESHOLD) -> Image.Image:
    """Pixel mit Distanz > threshold gegenüber der Schablone → Teil-Ebene."""
    if new_img.size != base_img.size:
        raise PartError(f"Größen stimmen nicht: {new_img.size} ≠ {base_img.size}")
    a = np.asarray(new_img.convert("RGBA")).astype(np.int16)
    b = np.asarray(base_img.convert("RGBA")).astype(np.int16)
    dist = np.abs(a[..., :3] - b[..., :3]).max(axis=2)
    neu_alpha = a[..., 3]
    changed = ((dist > threshold) | ((b[..., 3] == 0) & (neu_alpha > 16))) & (neu_alpha > 16)
    out = a.copy()
    out[..., 3] = np.where(changed, neu_alpha, 0)
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def extract_part(new_img: Image.Image, base_img: Image.Image | None = None,
                 *, threshold: int = DEFAULT_THRESHOLD,
                 anchor_cm: list[float] | None = None) -> tuple[Image.Image, dict]:
    """Teil-Ebene + Meta (w_cm, h_cm, anchor_cm) für parts.json.

    Ohne ``base_img`` wird neu freigestellt (Figuren-Modus); der Anker
    defaultet auf die Mitte, sonst gilt: ``anchor_cm`` von unten-links.
    """
    if base_img is None:
        rgba, _fg = cutout_character(new_img)
        layer = Image.fromarray(rgba, "RGBA")
    else:
        layer = diff_layer(new_img, base_img, threshold)
    bb = layer.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    if not bb:
        raise PartError("kein Inhalt – Differenz/Freistellung ist leer")
    layer = layer.crop(bb)
    w_cm = round(layer.width / PPC, 3)
    h_cm = round(layer.height / PPC, 3)
    anchor = list(anchor_cm) if anchor_cm else [round(w_cm / 2, 3), round(h_cm / 2, 3)]
    meta = {"w_cm": w_cm, "h_cm": h_cm, "anchor_cm": anchor}
    return layer, meta


def save_part(name: str, layer: Image.Image, meta: dict, template: str,
              *, parts_root: Path | None = None,
              parts_json: Path | None = None) -> dict:
    """PNG schreiben + parts.json-Upsert (Schlüsselreihenfolge bleibt)."""
    root = Path(parts_root) if parts_root else PARTS_ROOT
    jp = Path(parts_json) if parts_json else root / "parts.json"
    out = root / template / f"{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    layer.save(out)

    data = json.loads(jp.read_text(encoding="utf-8")) if jp.exists() else {}
    tpl = data.setdefault(template, {})
    tpl[name] = {**{k: v for k, v in tpl.get(name, {}).items()
                    if k in ("note", "zones", "part", "part_back")}, **meta}
    jp.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n",
                  encoding="utf-8")
    return tpl[name]


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("neu", help="neues Teil-Bild (PNG)")
    ap.add_argument("schablone", nargs="?", help="Schablone/Basis (PNG), sonst Freistellung")
    ap.add_argument("--name", required=True, help="Teilname, z. B. hair_front_mohawk")
    ap.add_argument("--template", default="kid", choices=["kid", "adult", "toddler"])
    ap.add_argument("--anchor", type=float, nargs=2, default=None,
                    metavar=("X_CM", "Y_CM"), help="Anker von unten-links")
    ap.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    a = ap.parse_args(argv)
    neu = Image.open(a.neu)
    base = Image.open(a.schablone) if a.schablone else None
    layer, meta = extract_part(neu, base, threshold=a.threshold, anchor_cm=a.anchor)
    save_part(a.name, layer, meta, a.template)
    print(f"✓ {a.template}/{a.name}.png  {layer.size} px  "
          f"{meta['w_cm']}×{meta['h_cm']} cm  Anker {meta['anchor_cm']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
