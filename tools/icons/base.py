"""
Icon-Baukasten (P04b-T08): Symbole im selben Stil wie Figuren und Items – Vektor, weiche Schattierung,
braune Tinten-Kontur. Jedes Icon besteht aus 1…n Ebenen; jede Ebene hat bis zu 3 Farbzonen (R/G/B) + Tinte
und wird wie im Spiel-Shader eingefärbt („gebacken“), dann übereinandergelegt. Ergebnis: feste Farben,
kein `modulate` mehr nötig.

Koordinaten: Einheiten, Ursprung = Mitte, y nach oben, sichtbarer Bereich ±15.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chibi.vec import ZCanvas  # noqa: E402
from items.kit import ell, rrect, smooth, trap  # noqa: E402,F401

SIZE = 256                 # Ausgabe in px
BOX = (-16.0, -16.0, 16.0, 16.0)
PPC = SIZE / 32.0          # px je Einheit
OUT = 0.75                 # Kontur (Einheiten) – kräftiger als bei Items, Icons sind klein
INNER = 0.38               # feine Innenlinie
SHADE = 0.84
SOFT = 0.92
INK = np.array([0x3B, 0x2A, 0x2A], np.float32) / 255.0

P = {
    "orange": "#ff9f45", "teal": "#48b0a0", "pink": "#ef6f6c", "yellow": "#ffd166", "lilac": "#8f7ac0",
    "sky": "#7cc4e8", "leaf": "#6cbf6a", "cream": "#fff4e0", "white": "#ffffff", "wood": "#c98e5a",
    "grey": "#b4bcc8", "red": "#e5534b", "navy": "#5a6fa3", "skin": "#f2c29b", "brown": "#8a5a3c",
    "gold": "#f4c542", "water": "#5fb7e6", "mint": "#9bd8c0", "rose": "#f7a8b8", "dark": "#5b4d6b",
    "sand": "#f0d9a6", "green": "#3f9a5a", "coral": "#f28b6c", "black": "#4a4150",
}


def col(name: str) -> np.ndarray:
    h = P.get(name, name).lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


class Icon:
    """Sammelt Ebenen; `bake()` liefert das fertige RGBA-Bild (SIZE×SIZE, zentriert)."""

    def __init__(self):
        self.layers: list[tuple[ZCanvas, list[str], bool]] = []

    def layer(self, *colors: str, outline: bool = True) -> ZCanvas:
        c = ZCanvas(BOX, PPC, outline_cm=OUT)
        self.layers.append((c, list(colors) + ["white"] * (3 - len(colors)), outline))
        return c

    def bake(self) -> Image.Image:
        out = np.zeros((SIZE, SIZE, 4), np.float32)
        for c, cols, outline in self.layers:
            if outline:
                c.outline_under()
            a = np.asarray(c.render(), np.float32) / 255.0
            if a.shape[:2] != (SIZE, SIZE):
                a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((SIZE, SIZE)), np.float32) / 255.0
            r, g, b, al = a[..., 0:1], a[..., 1:2], a[..., 2:3], a[..., 3:4]
            rest = np.clip(1.0 - r - g - b, 0.0, 1.0)
            z = [col(x) for x in cols[:3]]
            rgb = r * z[0] + g * z[1] + b * z[2] + rest * INK
            out[..., :3] = rgb * al + out[..., :3] * (1 - al)
            out[..., 3:4] = al + out[..., 3:4] * (1 - al)
        img = Image.fromarray(np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")
        return _center(img)


def _center(img: Image.Image) -> Image.Image:
    """Inhalt mittig setzen (optische Mitte = Hülle), Größe bleibt – gleiche Strichstärke für alle Icons."""
    bb = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb is None:
        return img
    part = img.crop(bb)
    if max(part.size) > SIZE - 8:
        f = (SIZE - 8) / max(part.size)
        part = part.resize((max(1, int(part.width * f)), max(1, int(part.height * f))), Image.LANCZOS)
    res = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    res.alpha_composite(part, ((SIZE - part.width) // 2, (SIZE - part.height) // 2))
    return res


# ------------------------------------------------------------------ kleine Helfer (Stil der Items)
def shaded(c: ZCanvas, pts, zone: int = 1, side: str = "right", amount: float = SHADE, frac: float = 0.3,
           inner: bool = True):
    """Fläche + Schattenstreifen (rechts/unten) + feine Innenkontur."""
    c.fill(pts, zone=zone)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    cl = c.mask(pts)
    if side == "right":
        xs0 = x1 - (x1 - x0) * frac
        c.fill([(xs0, y0 - 1), (x1 + 1, y0 - 1), (x1 + 1, y1 + 1), (xs0, y1 + 1)], zone=zone, shade=amount, clip=cl)
    elif side == "bottom":
        ys1 = y0 + (y1 - y0) * frac
        c.fill([(x0 - 1, y0 - 1), (x1 + 1, y0 - 1), (x1 + 1, ys1), (x0 - 1, ys1)], zone=zone, shade=amount, clip=cl)
    if inner:
        c.line(pts, INNER, zone=0, closed=True)
    return cl


def gloss(c: ZCanvas, x: float, y: float, rx: float, ry: float, zone: int = 2):
    """Glanzpunkt oben links (in einer hellen Zone)."""
    c.fill(ell(x, y, rx, ry, 24), zone=zone, alpha=0.85)


def band(pts, r: float):
    """Linie → Fläche (für Striche mit eigener Kontur)."""
    import math
    left, right = [], []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / n * r, dx / n * r
        left.append((pts[i][0] + nx, pts[i][1] + ny))
        right.append((pts[i][0] - nx, pts[i][1] - ny))
    return left + right[::-1]


def circle(cx: float, cy: float, r: float, n: int = 48):
    return ell(cx, cy, r, r, n)
