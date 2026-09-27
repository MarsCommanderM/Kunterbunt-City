"""
Fest im Hintergrund – NUR Bauliches (Entscheidung 👤: Räume leer, nur Boden + Wände; Fenster, Türen, Teppiche
usw. sind Items, das Kind baut selbst): Dachschrägen und die Außen-Kulisse (Himmel, ferne Hügel und Bäume).
Fest eingefärbt („gebacken“), mit Tinten-Kontur wie Items.
"""
from __future__ import annotations

import math
import random

from items.kit import ell, rrect, smooth

from .base import INNER, WALL_H, Sheet, bake, canvas

def roof_slopes(sheet: Sheet, width: float, knee: float = 110.0):
    """Dachboden: schräge Decke links und rechts (Holzbretter parallel zur Schräge, zwei Sparren) – bleibt Wand."""
    cols = ["#d8b48a", "#c49a6c", "#8a5a3c"]
    for side in (-1, 1):
        x_edge = 0.0 if side < 0 else width
        x_in = width * 0.3 if side < 0 else width * 0.7
        c = canvas(min(x_edge, x_in) - 2, knee - 2, max(x_edge, x_in) + 2, WALL_H + 2)
        poly = [(x_edge, knee), (x_edge, WALL_H), (x_in, WALL_H)]
        c.fill(poly, zone=1)
        cl = c.mask(poly)
        n = 12
        for k in range(1, n):                            # Bretter parallel zur Schräge
            t = k / n
            a = (x_edge, knee + (WALL_H - knee) * t)
            b = (x_in + (x_edge - x_in) * t, WALL_H)
            c.line([a, b], INNER * 2.2, zone=3, shade=0.95, clip=cl)
            if k % 2:
                c.fill([a, b, (b[0] + (x_edge - x_in) / n, WALL_H), (x_edge, a[1] + (WALL_H - knee) / n)], zone=1,
                       shade=0.94, clip=cl)
        for t in (0.35, 0.72):                           # Sparren
            a = (x_edge, knee + (WALL_H - knee) * t)
            b = (x_in + (x_edge - x_in) * t, WALL_H)
            c.line([a, b], 5.0, zone=2, clip=cl)
            c.line([a, b], 1.0, zone=3, shade=0.8, clip=cl)
        c.line([(x_edge, knee), (x_in, WALL_H)], 4.0, zone=3)
        sheet.paste(bake(c, cols), min(x_edge, x_in) - 2, WALL_H + 2)


def outdoor(sheet: Sheet, width: float, seed: int = 5, edge: str = "none", top: float = WALL_H + 80):
    """Außen: Himmel (bis `top` cm, = Raumhöhe → weit rauszoomen ohne Rand), Wolken, ferne Hügel mit Bäumen.
    Zäune/Hecken sind Items (edge = "none")."""
    rng = random.Random(seed)
    sky = canvas(0, 0, width, top, outline=0)
    area = [(0, 0), (width, 0), (width, top), (0, top)]
    sky.fill(area, zone=1)
    for k in range(10):
        yy = top * (1 - k / 10)
        sky.fill([(0, 0), (width, 0), (width, yy), (0, yy)], zone=1, shade=1.0 + 0.01 * k, alpha=0.3)
    for _ in range(int(width / 110)):
        cx, cy = rng.uniform(0, width), rng.uniform(max(190.0, top * 0.4), top * 0.9)   # auch im Normal-Zoom sichtbar
        for dx, r in ((-14, 11), (0, 16), (15, 12), (6, 9)):
            sky.fill(ell(cx + dx, cy + (4 if r < 12 else 0), r * 1.4, r, 32), zone=2)
    far = [(-10, 0)] + [(width * k / 16, 70 + 30 * math.sin(k * 0.8 + seed)) for k in range(17)] + [(width + 10, 0)]
    sky.fill(smooth(far, closed=True), zone=3, shade=0.9)
    sheet.paste(bake(sky, ["#a8dcf2", "#ffffff", "#9ccf86"], outline=False), 0, top)
    trees = canvas(0, 0, width, 180)
    for _ in range(int(width / 70)):
        tx = rng.uniform(0, width)
        th = rng.uniform(70, 120)
        trees.fill(rrect(tx - 3, 30, tx + 3, 30 + th * 0.45, 1.5), zone=3)
        for dx, dy, r in ((0, th * 0.75, th * 0.28), (-th * 0.18, th * 0.6, th * 0.22), (th * 0.18, th * 0.6, th * 0.22)):
            trees.fill(ell(tx + dx, 30 + dy, r, r * 0.9, 28), zone=1, shade=rng.choice([0.9, 1.0]))
    sheet.paste(bake(trees, ["#6fb35f", "#ffffff", "#8a5a3c"]), 0, 180)
