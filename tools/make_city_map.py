#!/usr/bin/env python3
"""Stadtkarte (P05-T02): Hintergrundbild für das Startmenü – Stil C, 0 EUR, reproduzierbar.

Zeichnet eine warme Kartenwelt (Wiesen, Fluss, Straßen, Bäume, 12 Bereichs-Inseln) als
1920x1080-PNG. Die Bereiche liegen exakt an den Koordinaten aus data/areas/index.json,
die Knöpfe werden darüber gelegt.

Aufruf:  python3 tools/make_city_map.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "ui" / "city_map.png"
W, H = 1920, 1080

GRASS = (214, 234, 196)
GRASS_DARK = (196, 222, 178)
WATER = (166, 214, 232)
WATER_DARK = (140, 198, 222)
ROAD = (246, 238, 224)
ROAD_EDGE = (232, 220, 202)
TREE = (140, 196, 152)
TREE_DARK = (116, 172, 128)
TRUNK = (168, 128, 96)
SHADOW = (120, 110, 100)


def ellipse(d, cx, cy, rx, ry, color):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color)


def soft(base: Image.Image, px: int = 6) -> Image.Image:
    return base.filter(ImageFilter.GaussianBlur(px))


def tree(d, x: int, y: int, s: float = 1.0):
    d.rounded_rectangle([x - 4 * s, y, x + 4 * s, y + 26 * s], radius=4, fill=TRUNK)
    ellipse(d, x, y - 6 * s, 22 * s, 24 * s, TREE_DARK)
    ellipse(d, x - 3 * s, y - 12 * s, 19 * s, 20 * s, TREE)


def main() -> int:
    idx = json.loads((ROOT / "data" / "areas" / "index.json").read_text(encoding="utf-8"))
    areas = idx["areas"]

    base = Image.new("RGBA", (W, H), GRASS + (255,))
    d = ImageDraw.Draw(base)

    # sanfte Wiesen-Flecken
    for i, (cx, cy, r) in enumerate(((320, 220, 420), (1500, 300, 380), (900, 900, 460),
                                    (1700, 900, 320), (500, 620, 300))):
        col = GRASS_DARK if i % 2 == 0 else (206, 230, 190)
        ellipse(d, cx, cy, r, r * 0.52, col)

    # Fluss (geschwungene Linie von links unten nach rechts oben)
    river = [( -20, 980), (240, 900), (520, 930), (760, 830), (980, 860), (1240, 760),
             (1500, 700), (1780, 560), (1960, 520)]
    d.line(river, fill=WATER, width=54, joint="curve")
    d.line([(x, y + 16) for x, y in river], fill=WATER_DARK, width=18, joint="curve")

    # Straßen: verbinden die Bereiche in der Reihenfolge des Index
    pts = [(int(a["map_x"]), int(a["map_y"])) for a in areas]
    d.line(pts, fill=ROAD_EDGE, width=64, joint="curve")
    d.line(pts, fill=ROAD, width=44, joint="curve")
    d.line(pts, fill=(255, 255, 255, 90), width=6, joint="curve")

    # Bäume und Büsche (feste Positionen → reproduzierbar)
    trees = [(160, 300), (220, 470), (430, 260), (560, 420), (700, 180), (860, 300),
             (1010, 200), (1180, 380), (1330, 220), (1480, 420), (1640, 260), (1780, 420),
             (150, 700), (420, 780), (620, 520), (900, 660), (1120, 520), (1300, 640),
             (1560, 700), (1800, 680), (300, 950), (760, 960), (1200, 940), (1660, 940)]
    for i, (x, y) in enumerate(trees):
        tree(d, x, y, 0.85 + 0.35 * ((i * 7) % 5) / 5.0)

    # Bereichs-Inseln (weicher Schatten + farbiges Podest)
    pads = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pads)
    for a in areas:
        x, y = int(a["map_x"]), int(a["map_y"])
        col = tuple(int(a["color"].lstrip("#")[i * 2:i * 2 + 2], 16) for i in range(3))
        ellipse(pd, x, y + 18, 132, 96, SHADOW + (60,))
        ellipse(pd, x, y, 130, 96, (255, 255, 255, 235))
        ellipse(pd, x, y + 4, 112, 80, col + (225,))
    pads = soft(pads, 5)
    base = Image.alpha_composite(base, pads)
    d = ImageDraw.Draw(base)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT, optimize=True)
    print("Stadtkarte → %s (%d Bereiche)" % (OUT, len(areas)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
