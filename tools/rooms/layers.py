"""
Wand und Boden als ZONEN-Ebenen (P07-T04): das Spiel färbt sie per Shader – Tapete und Boden wählbar
(Farben + Muster), ohne neue Bilder. Eine Ebene je Raumbreite wird von allen Räumen dieser Breite geteilt.

Wand:  Zone 1 = Tapete (bekommt das Muster) · Zone 2 = Leisten (Sockel, Stuhlleiste, Decke) · Zone 3 = Wandsockel-Paneel
Boden: Zone 1 = Grundton · Zone 2 = zweiter Ton (Dielen/Fliesen im Wechsel) · Zone 3 = Fugen/Rand
"""
from __future__ import annotations

import math
import random

from items.kit import rrect  # noqa: F401

from .base import BOTTOM, FRONT, INNER, WALL_H, canvas, raw

DEPTH_MAX = 1.12                # S-07: vorn 12 % größer


def _persp(x: float, cx: float, depth_cm: float) -> float:
    """x an der Rückwand → x in der Tiefe depth_cm (Fluchtpunkt in der Mitte)."""
    f = 1.0 + (DEPTH_MAX - 1.0) * depth_cm / FRONT
    return cx + (x - cx) * f


def wall(width: float, height: float = WALL_H, wainscot: bool = True):
    c = canvas(0, 0, width, height, outline=0)
    c.fill([(0, 0), (width, 0), (width, height), (0, height)], zone=1)
    if wainscot:
        c.fill([(0, 12), (width, 12), (width, 92), (0, 92)], zone=3)
        n = max(2, round(width / 110))
        for k in range(n):                                     # Paneel-Felder
            x0 = 12 + k * (width - 24) / n
            x1 = x0 + (width - 24) / n - 14
            c.line(rrect(x0, 22, x1, 82, 1.5), INNER, zone=3, shade=0.8, closed=True)
            c.fill([(x0, 80), (x1, 80), (x1, 82), (x0, 82)], zone=3, shade=1.08)
        c.fill([(0, 92), (width, 92), (width, 98), (0, 98)], zone=2)                       # Stuhlleiste
        c.fill([(0, 95.5), (width, 95.5), (width, 98), (0, 98)], zone=2, shade=0.88)
        c.line([(0, 92), (width, 92)], INNER, zone=0)
        c.line([(0, 98), (width, 98)], INNER, zone=0)
    c.fill([(0, 0), (width, 0), (width, 12), (0, 12)], zone=2)                            # Sockelleiste
    c.fill([(0, 0), (width, 0), (width, 3), (0, 3)], zone=2, shade=0.84)
    c.line([(0, 12), (width, 12)], INNER, zone=0)
    c.fill([(0, height - 9), (width, height - 9), (width, height), (0, height)], zone=2)  # Deckenleiste
    c.fill([(0, height - 9), (width, height - 9), (width, height - 6), (0, height - 6)], zone=2, shade=0.86)
    c.line([(0, height - 9), (width, height - 9)], INNER, zone=0)
    # weicher Schatten oben (Decke) und unten (Ecke) – lebendiger als flach
    for k in range(10):
        c.fill([(0, height - 9 - k * 3), (width, height - 9 - k * 3), (width, height - 12 - k * 3), (0, height - 12 - k * 3)],
               zone=1, shade=0.93 + k * 0.007, alpha=0.5)
    return raw(c)


def floor(width: float, kind: str = "planks", seed: int = 3):
    """Boden von der Rückwand (y_up = 0) bis BOTTOM nach vorn, mit Perspektive."""
    rng = random.Random(seed)
    c = canvas(0, -BOTTOM, width, 0, outline=0)
    cx = width / 2
    area = [(0, 0), (width, 0), (width, -BOTTOM), (0, -BOTTOM)]
    c.fill(area, zone=1)
    if kind == "planks":
        pw = 22.0                                           # Dielenbreite an der Wand
        xs = [cx + k * pw for k in range(-int(width / pw) - 8, int(width / pw) + 9)]
        for i, x in enumerate(xs[:-1]):
            poly = [(x, 0), (xs[i + 1], 0), (_persp(xs[i + 1], cx, BOTTOM), -BOTTOM), (_persp(x, cx, BOTTOM), -BOTTOM)]
            if i % 3 == 1:
                c.fill(poly, zone=2, alpha=0.85)
            elif i % 3 == 2:
                c.fill(poly, zone=1, shade=0.95)
            c.line([(x, 0), (_persp(x, cx, BOTTOM), -BOTTOM)], INNER * 0.9, zone=3)
            # Stoßfugen versetzt
            d = rng.uniform(10, BOTTOM - 10)
            xa, xb = _persp(x, cx, d), _persp(xs[i + 1], cx, d)
            c.line([(xa, -d), (xb, -d)], INNER * 0.9, zone=3)
    elif kind == "tiles":
        rows = [0.0]
        step = 16.0
        while rows[-1] < BOTTOM:
            rows.append(rows[-1] + step)
            step *= 1.1
        tw = 30.0
        xs = [cx + k * tw for k in range(-int(width / tw) - 8, int(width / tw) + 9)]
        for ri in range(len(rows) - 1):
            for i, x in enumerate(xs[:-1]):
                if (i + ri) % 2:
                    d0, d1 = rows[ri], min(rows[ri + 1], BOTTOM)
                    c.fill([(_persp(x, cx, d0), -d0), (_persp(xs[i + 1], cx, d0), -d0), (_persp(xs[i + 1], cx, d1), -d1),
                            (_persp(x, cx, d1), -d1)], zone=2)
        for d in rows:
            c.line([(-10, -d), (width + 10, -d)], INNER * 1.3, zone=3)
        for x in xs:
            c.line([(x, 0), (_persp(x, cx, BOTTOM), -BOTTOM)], INNER * 1.3, zone=3)
    elif kind == "carpet":
        for _ in range(int(width * BOTTOM / 60)):
            x, d = rng.uniform(0, width), rng.uniform(0, BOTTOM)
            c.fill([(x, -d), (x + 1.2, -d), (x + 1.2, -d - 0.8), (x, -d - 0.8)], zone=2, alpha=0.35)
        c.fill([(0, 0), (width, 0), (width, -5), (0, -5)], zone=3, alpha=0.6)
    elif kind == "concrete":
        for _ in range(int(width * BOTTOM / 120)):
            x, d = rng.uniform(0, width), rng.uniform(0, BOTTOM)
            r = rng.uniform(0.4, 1.4)
            c.fill([(x - r, -d), (x + r, -d), (x + r, -d - r), (x - r, -d - r)], zone=2, alpha=0.4)
        for x in (width * 0.33, width * 0.66):
            c.line([(x, 0), (_persp(x, cx, BOTTOM), -BOTTOM)], INNER, zone=3)
    elif kind == "grass":
        for _ in range(int(width * BOTTOM / 25)):
            x, d = rng.uniform(0, width), rng.uniform(0, BOTTOM)
            h = rng.uniform(1.5, 3.5) * (1 + d / BOTTOM * 0.3)
            c.fill([(x - 0.6, -d), (x + 0.6, -d), (x + rng.uniform(-0.8, 0.8), -d + h)], zone=2 if rng.random() < 0.6 else 3)
    elif kind == "sand":
        for _ in range(int(width * BOTTOM / 40)):
            x, d = rng.uniform(0, width), rng.uniform(0, BOTTOM)
            c.fill([(x, -d), (x + 0.9, -d), (x + 0.9, -d - 0.9), (x, -d - 0.9)], zone=2, alpha=0.5)
    # Ecke Wand/Boden: Kontaktschatten
    for k in range(6):
        c.fill([(0, 0), (width, 0), (width, -1.2 - k * 1.2), (0, -1.2 - k * 1.2)], zone=1, shade=0.9, alpha=0.12)
    return raw(c)


FLOOR_KINDS = ["planks", "tiles", "carpet", "concrete", "grass", "sand"]
