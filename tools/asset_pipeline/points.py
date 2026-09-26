#!/usr/bin/env python3
"""P06-T04 – Pivot + Grip-Vorgaben je Kategorie, Griff für Figuren, Vorschaubild.

* ``pivot``  = Aufhebepunkt relativ zum Sprite, Standard (0.5, 1.0) = unten Mitte.
* ``grip``   = Griffpunkt, Standard je Kategorie (Tasse → Henkel = rechte Kante
  bei 45 % Höhe), spezifiziert in der Blatt-YAML (``grip: [x, y]``) – die YAML
  gewinnt immer; ``preview()`` markiert beide Punkte zum Korrigieren.
* ``find_hand_grip()``: Handmitte einer Figur über Hautfarb-Erkennung
  (wie reference/pipeline_demo_kueche.py find_fist).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Kategorie → Standard-Grip (None = nicht haltbar, z. B. Möbel/Fixtures)
CATEGORY_GRIP: dict[str, list[float] | None] = {
    "food": [0.5, 0.45],
    "kitchen": [0.9, 0.45],   # Henkel: rechte Kante, 45 % Höhe
    "toy": [0.5, 0.5],
    "item": [0.5, 0.45],
    "pet": [0.5, 0.45],
    "school": [0.5, 0.45],
    "health": [0.5, 0.45],
    "pool": [0.5, 0.45],
    "shop": [0.5, 0.45],
    "sport": [0.5, 0.45],
    "fair": [0.5, 0.45],
    "garage": [0.5, 0.45],
    "zoo_animal": [0.5, 0.45],
    "furniture": None,
    "fixture": None,
    "character": None,
}
DEFAULT_PIVOT = [0.5, 1.0]


def points(spec: dict, entry: dict | None) -> dict:
    """Pivot/Grip/Hold für ein YAML-Item (``entry`` = Zeile aus scale_table).

    Reihenfolge der Bestimmung: YAML-Override → Tabellen-Hold → Kategorie-Default.
    """
    pivot = list(spec.get("pivot") or DEFAULT_PIVOT)
    hold = spec.get("hold")
    grip = spec.get("grip")
    if entry is not None:
        cat = entry.get("category", "item")
        if hold is None:
            hold = entry.get("hold", "none")
        if grip is None and hold != "none":
            grip = CATEGORY_GRIP.get(cat, [0.5, 0.45])
    if hold == "none" and "grip" not in spec:
        grip = None
    return {
        "pivot": pivot,
        "grip": list(grip) if grip else None,
        "hold": hold or "none",
        "hold_angle": int(spec.get("hold_angle", 0)),
    }


def find_hand_grip(img: Image.Image) -> list[float]:
    """Handmitte der (erhobenen) Figurhand: äußerster Hautpunkt oben rechts.

    Liefert normalisierte [x, y] relativ zum Sprite – wie find_fist der Demo.
    """
    a = np.asarray(img.convert("RGBA")).astype(int)
    h, w = a.shape[:2]
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    skin = (al > 200) & (r > 200) & (g > 150) & (g < 215) & (b > 120) & (b < 190) & (r - b > 40)
    ys, xs = np.nonzero(skin[: int(h * 0.62), int(w * 0.62):])
    if len(xs) == 0:
        return [0.5, 0.5]
    xs = xs + int(w * 0.62)
    sel = xs > xs.max() - 0.09 * w
    return [round(float(xs[sel].mean()) / w, 3), round(float(ys[sel].mean()) / h, 3)]


def preview(img: Image.Image, pts: dict, out: Path) -> Path:
    """Vorschaubild: Pivot = blauenes Kreuz, Grip = roter Ring (mit Etikett)."""
    vis = img.convert("RGBA")
    d = ImageDraw.Draw(vis)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    px, py = pts["pivot"][0] * vis.width, pts["pivot"][1] * vis.height
    d.line([(px - 10, py), (px + 10, py)], fill=(30, 90, 220), width=3)
    d.line([(px, py - 10), (px, py + 10)], fill=(30, 90, 220), width=3)
    if pts.get("grip"):
        gx, gy = pts["grip"][0] * vis.width, pts["grip"][1] * vis.height
        d.ellipse([gx - 9, gy - 9, gx + 9, gy + 9], outline=(220, 30, 30), width=3)
        d.text((gx + 12, gy - 8), "grip", fill=(220, 30, 30), font=font)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    vis.save(out)
    return out
