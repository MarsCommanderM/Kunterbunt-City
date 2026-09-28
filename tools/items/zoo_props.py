"""
Zoo-Einrichtung (P10g): Felsen, Akazie, Wasserbecken (flach), Eisschollen, Terrarium, Aquarium-Becken (Fische,
Zustand „feed“ = Futter rieselt), Kletter-Gerüst mit Seilen, Heuraufe, Tierschild (Bild statt Text), Futter
(Fleisch, Fisch, Blätterzweig, Heu, Körner), Futtereimer.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe/hell · 3 = Akzent.
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, ell, rrect, shaded, smooth, trap


def _fish(c, x: float, y: float, s: float, zone: int, clip=None, flip: bool = False):
    d = -1 if flip else 1
    c.fill(ell(x, y, s, s * 0.55, 16), zone=zone, clip=clip)
    c.fill([(x - d * s * 0.9, y), (x - d * s * 1.5, y + s * 0.5), (x - d * s * 1.5, y - s * 0.5)], zone=zone, shade=0.9, clip=clip)
    c.fill(ell(x + d * s * 0.45, y + s * 0.12, s * 0.14, s * 0.14, 8), zone=0, clip=clip)


def zoo_prop(it: Item, style: str = "rock", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    rng = random.Random(int(W * 7 + H))
    if style == "rock":                                             # großer Felsen
        rock = smooth([(x0, 0, "s"), (x1, 0, "s"), (x1 - W * 0.06, H * 0.5), (W * 0.2, H * 0.92), (-W * 0.1, H),
                       (x0 + W * 0.12, H * 0.7)])
        shaded(c, rock, 1, "right", SHADE, 0.3)
        cl = c.mask(rock)
        for _ in range(6):
            x, y = rng.uniform(x0, x1), rng.uniform(H * 0.1, H * 0.8)
            c.line(smooth([(x, y), (x + 14, y - 6), (x + 24, y - 2)], closed=False), INNER, zone=0, shade=0.8, clip=cl)
        c.fill(ell(-W * 0.1, H * 0.9, W * 0.2, H * 0.08, 20), zone=2, clip=cl, alpha=0.6)
        c.line(rock, INNER, zone=0, closed=True)
    elif style == "acacia":                                         # Akazie (flache Krone)
        c.fill(trap(-W * 0.04, W * 0.04, 0, -W * 0.025, W * 0.025, H * 0.7, 1), zone=3)
        for sx in (-1, 1):
            c.line(smooth([(0, H * 0.55), (sx * W * 0.15, H * 0.72), (sx * W * 0.3, H * 0.78)], closed=False), W * 0.025, zone=3)
        crown = smooth([(x0, H * 0.78, "s"), (x1, H * 0.78, "s"), (x1 - W * 0.06, H * 0.92), (W * 0.2, H), (-W * 0.2, H),
                        (x0 + W * 0.06, H * 0.92)])
        shaded(c, crown, 1, "bottom", SHADE, 0.35)
        for _ in range(8):
            c.fill(ell(rng.uniform(x0 + 30, x1 - 30), rng.uniform(H * 0.84, H * 0.96), W * 0.06, H * 0.03, 16), zone=1, shade=1.1)
        c.line(crown, INNER, zone=0, closed=True)
    elif style == "pond":                                           # flaches Wasserbecken (Elefanten, Pinguine, Krokodil)
        water = ell(0, H * 0.5, W * 0.48, H * 0.42, 64)
        c.fill(ell(0, H * 0.5, W * 0.5, H * 0.5, 64), zone=1)
        c.fill(water, zone=2)
        cl = c.mask(water)
        for k in range(5):
            x = x0 + W * (0.2 + k * 0.15)
            c.line(smooth([(x - 14, H * 0.5), (x, H * 0.56), (x + 14, H * 0.5)], closed=False), 0.6, zone=2, shade=1.35, clip=cl)
    elif style == "ice_floe":                                       # Eisschollen / Pinguin-Felsen
        for k in range(3):
            b = smooth([(x0 + k * W * 0.3, 0, "s"), (x0 + k * W * 0.3 + W * 0.42, 0, "s"), (x0 + k * W * 0.3 + W * 0.38, H * (0.5 + k * 0.2)),
                        (x0 + k * W * 0.3 + W * 0.05, H * (0.55 + k * 0.2))])
            shaded(c, b, 1, "right", SHADE, 0.3)
            c.fill(rrect(x0 + k * W * 0.3 + W * 0.05, H * (0.45 + k * 0.2), x0 + k * W * 0.3 + W * 0.36, H * (0.55 + k * 0.2), 4), zone=2)
            c.line(b, INNER, zone=0, closed=True)
    elif style == "terrarium":                                      # Terrarium: Glas, Sand, Ast, Wärmelampe
        c.fill(rrect(x0, 0, x1, H * 0.2, 1), zone=1)
        box = rrect(x0, H * 0.2, x1, H, 1.5)
        c.fill(rrect(x0 + 2, H * 0.2, x1 - 2, H - 2, 1), zone=3, shade=0.55)          # Rückwand (dunkel)
        c.fill(rrect(x0 + 3, H * 0.2, x1 - 3, H * 0.35, 1), zone=2)
        c.line(smooth([(x0 + W * 0.1, H * 0.35), (0, H * 0.6), (x1 - W * 0.15, H * 0.7)], closed=False), 3.0, zone=1, shade=0.8)
        c.fill(ell(x1 - W * 0.2, H * 0.4, W * 0.08, H * 0.1, 16), zone=3, shade=0.7)
        for k in range(3):                                          # Glas: nur Glanzstreifen, damit man hineinsieht
            c.line([(x0 + W * (0.1 + k * 0.06), H * 0.9), (x0 + W * (0.16 + k * 0.06), H * 0.6)], 0.8, zone=3, shade=1.4)
        c.fill(rrect(x0, H - 6, x1, H, 1), zone=1)
        c.fill(ell(x0 + W * 0.2, H * 0.9, W * 0.06, H * 0.04, 12), zone=3, shade=1.5)
        c.line(box, INNER, zone=0, closed=True)
    elif style == "tank":                                           # Aquarium-Becken mit Fischen (feed = Futter)
        c.fill(rrect(x0, 0, x1, H * 0.22, 2), zone=1)
        box = rrect(x0, H * 0.22, x1, H, 2)
        water = rrect(x0 + 4, H * 0.24, x1 - 4, H * 0.94, 1)
        c.fill(water, zone=2)
        cl = c.mask(water)
        c.fill(rrect(x0 + 4, H * 0.24, x1 - 4, H * 0.32, 1), zone=3, shade=0.9, clip=cl)
        for k in range(int(W / 50)):
            x = x0 + 20 + k * 50
            c.line(smooth([(x, H * 0.3), (x - 6, H * 0.45), (x + 4, H * 0.6)], closed=False), 2.5, zone=1, shade=0.8, clip=cl)
        for k in range(int(W / 40)):
            _fish(c, x0 + 30 + k * 40 + rng.uniform(-8, 8), rng.uniform(H * 0.4, H * 0.85), rng.uniform(7, 12),
                  3 if k % 2 else 1, clip=cl, flip=k % 3 == 0)
        if state == "feed":
            for k in range(20):
                c.fill(ell(rng.uniform(x0 + 20, x1 - 20), rng.uniform(H * 0.6, H * 0.92), 1.2, 1.2, 6), zone=1, shade=0.6, clip=cl)
        c.line(box, INNER, zone=0, closed=True)
    elif style == "climb_frame":                                    # Kletter-Gerüst mit Seilen und Plattform
        for x in (x0 + 10, x1 - 10):
            c.fill(rrect(x - 6, 0, x + 6, H, 3), zone=1)
        c.fill(rrect(x0, H * 0.94, x1, H, 3), zone=1, shade=0.9)
        c.fill(rrect(x0 + 10, H * 0.55, x0 + W * 0.45, H * 0.6, 2), zone=1, shade=1.1)
        for k in range(4):
            x = x0 + W * (0.2 + k * 0.2)
            c.line(smooth([(x, H * 0.94), (x + 10, H * 0.6), (x - 5, H * 0.3)], closed=False), 2.0, zone=2)
        c.line(smooth([(x0 + W * 0.5, H * 0.94), (0, H * 0.75), (x1 - W * 0.1, H * 0.94)], closed=False), 2.5, zone=2)
        c.fill(ell(x1 - W * 0.25, H * 0.3, W * 0.08, W * 0.08, 20), zone=3)
        c.erase(ell(x1 - W * 0.25, H * 0.3, W * 0.05, W * 0.05, 16))
        c.line([(x1 - W * 0.25, H * 0.3 + W * 0.08), (x1 - W * 0.25, H * 0.94)], 1.2, zone=2)
    elif style == "hay_rack":                                       # Heuraufe
        for x in (x0 + 6, x1 - 6):
            c.fill(rrect(x - 4, 0, x + 4, H, 1), zone=1)
        c.fill(trap(x0 + 4, x1 - 4, H * 0.45, x0, x1, H * 0.95, 1), zone=3)
        for k in range(8):
            x = x0 + 10 + k * (W - 20) / 7
            c.line([(x, H * 0.45), (x + 4, H * 0.95)], 1.2, zone=1, shade=0.8)
        c.fill(rrect(x0, H * 0.94, x1, H, 1.5), zone=1)
    elif style == "sign":                                           # Tierschild auf Pfosten (Tier-Pfote statt Text)
        c.fill(rrect(-3, 0, 3, H * 0.6, 1), zone=1, shade=0.8)
        b = rrect(x0, H * 0.55, x1, H, 3)
        c.fill(b, zone=1)
        c.fill(rrect(x0 + 5, H * 0.6, x1 - 5, H - 5, 2), zone=2)
        cx, cy, r = 0, H * 0.75, W * 0.12
        c.fill(ell(cx, cy - r * 0.3, r, r * 0.8, 20), zone=3)
        for k in range(4):
            a = math.pi * (0.2 + k * 0.2)
            c.fill(ell(cx + math.cos(a) * r * 1.6, cy + math.sin(a) * r * 1.3, r * 0.4, r * 0.45, 12), zone=3)
        c.line(b, INNER, zone=0, closed=True)
    elif style == "meat":                                           # Futter: Fleisch (Knochen)
        c.fill(ell(0, H * 0.5, W * 0.35, H * 0.45, 20), zone=1)
        c.fill(ell(W * 0.05, H * 0.55, W * 0.18, H * 0.2, 12), zone=1, shade=1.15)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.32 - W * 0.1, H * 0.38, sx * W * 0.32 + W * 0.1, H * 0.62, 2), zone=2)
            c.fill(ell(sx * W * 0.45, H * 0.35, W * 0.06, H * 0.14, 10), zone=2)
            c.fill(ell(sx * W * 0.45, H * 0.65, W * 0.06, H * 0.14, 10), zone=2)
    elif style == "fish_food":                                      # Futter: Fisch
        _fish(c, W * 0.1, H * 0.5, W * 0.32, 1)
        c.fill(ell(W * 0.05, H * 0.4, W * 0.2, H * 0.12, 12), zone=2)
    elif style == "leaves":                                         # Futter: Blätterzweig
        c.line(smooth([(x0, H * 0.1), (0, H * 0.4), (x1, H * 0.7)], closed=False), 1.4, zone=3)
        for k in range(6):
            t = (k + 0.5) / 6
            x, y = x0 + W * t, H * (0.1 + 0.6 * t)
            c.fill(ell(x, y + H * 0.15, W * 0.08, H * 0.13, 12), zone=1, shade=1.0 + (k % 2) * 0.1)
            c.fill(ell(x + W * 0.03, y - H * 0.1, W * 0.08, H * 0.12, 12), zone=1, shade=0.92)
    elif style == "hay":                                            # Futter: Heubündel
        b = smooth([(x0, 0, "s"), (x1, 0, "s"), (x1, H * 0.7), (0, H), (x0, H * 0.7)])
        c.fill(b, zone=1)
        for k in range(10):
            x = x0 + k * W / 9
            c.line([(x, H * 0.1), (x + rng.uniform(-4, 4), H * 0.9)], 0.5, zone=1, shade=0.8)
        c.fill(rrect(x0, H * 0.4, x1, H * 0.5, 0.5), zone=3)
    elif style == "seeds":                                          # Futter: Körnerschale
        c.fill(trap(x0, x1, 0, x0 - 2, x1 + 2, H * 0.6, 1), zone=3)
        for k in range(12):
            c.fill(ell(rng.uniform(x0 + 3, x1 - 3), rng.uniform(H * 0.55, H * 0.9), 1.2, 0.8, 6), zone=1)
    elif style == "bucket":                                         # Futtereimer
        b = trap(-W * 0.36, W * 0.36, 0, x0, x1, H * 0.8, 1)
        shaded(c, b, 1, "right", SOFT, 0.25)
        c.line(smooth([(x0 + 2, H * 0.8), (0, H), (x1 - 2, H * 0.8)], closed=False), 0.8, zone=3)
        c.fill(ell(0, H * 0.8, W * 0.5, H * 0.06, 20), zone=2)
        c.line(b, INNER, zone=0, closed=True)
    else:
        raise ValueError(style)
