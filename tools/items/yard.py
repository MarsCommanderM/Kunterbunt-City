"""
Großer Garten (P07, Wunsch 👤): Säen · Gießen · Ernten, Blumenbeete (müssen gegossen werden), Sitzen/Feiern/Grillen,
Pool, Teich, Pavillon, Spielgeräte, Gartenhaus … jeweils in mehreren Formen und Größen.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe (Blüten, Stoff, Wasser) · 3 = Holz/Metall/Erde.

Wachstum: Beete haben die Zustände "" (leer) → "sprout" → "grown" → "ripe"; Blumenbeete "" (blüht) und "dry" (welk).
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, ell, knob, leg, line, rrect, shaded, smooth, trap
from .plants import leaf

EARTH = 0.55     # Erde = Zone 3 dunkel


def _lf(c, x: float, y: float, length: float, ang: float, zone: int = 1, shade: float = 1.0, clip=None):
    """Blatt (Winkel im Bogenmaß) – kurze Form von plants.leaf."""
    leaf(c, x, y, length, length * 0.42, math.degrees(ang), zone=zone, shade=shade, rib=False, clip=clip)


def _soil(c, x0: float, x1: float, y0: float, y1: float, seed: int = 3):
    rng = random.Random(seed)
    top = smooth([(x0, y0, "s"), (x1, y0, "s"), (x1, y1 - 1)] + [(x1 - (x1 - x0) * k / 6, y1 + rng.uniform(-0.8, 0.8)) for k in range(1, 6)]
                 + [(x0, y1 - 1)])
    c.fill(top, zone=3, shade=EARTH)
    for _ in range(int((x1 - x0) / 5)):
        c.ellipse(rng.uniform(x0 + 2, x1 - 2), rng.uniform(y0 + 1, y1 - 1), 0.6, 0.4, zone=3, shade=0.4)


def _crop(c, x: float, y: float, crop: str, stage: str, s: float = 1.0):
    """Eine Pflanze im Beet – Größe nach Wachstumsstufe."""
    if stage == "":
        c.ellipse(x, y + 0.4, 1.4 * s, 0.6 * s, zone=3, shade=0.4)         # Saatloch
        return
    k = {"sprout": 0.35, "grown": 0.8, "ripe": 1.0}[stage]
    h = 14 * s * k
    for a in (-0.5, 0.0, 0.5):
        _lf(c, x, y, h, math.pi / 2 + a, zone=1, shade=1.0 - abs(a) * 0.15)
    if stage != "ripe":
        return
    if crop == "carrot":
        c.fill(trap(x - 2 * s, x + 2 * s, y + 0.5, x - 1.4 * s, x + 1.4 * s, y + 3 * s, 0.6), zone=2)
    elif crop == "tomato":
        for dx, dy in ((-3, 6), (3, 8), (0, 11)):
            c.fill(ell(x + dx * s, y + dy * s, 2.2 * s, 2.0 * s, 20), zone=2)
            c.line(ell(x + dx * s, y + dy * s, 2.2 * s, 2.0 * s, 20), INNER, zone=0, closed=True)
    elif crop == "lettuce":
        c.fill(ell(x, y + 3 * s, 6 * s, 3.5 * s, 28), zone=1, shade=1.15)
        c.line(ell(x, y + 3 * s, 6 * s, 3.5 * s, 28), INNER, zone=0, closed=True)
    elif crop == "strawberry":
        for dx in (-4, 4):
            c.fill(smooth([(x + dx * s - 1.8 * s, y + 3 * s), (x + dx * s + 1.8 * s, y + 3 * s), (x + dx * s, y)]), zone=2)
    elif crop == "pumpkin":
        c.fill(ell(x, y + 4 * s, 6 * s, 4.2 * s, 32), zone=2)
        for dx in (-2.5, 0, 2.5):
            line(c, [(x + dx * s, y + 0.5), (x + dx * s * 0.8, y + 8 * s)], zone=2, shade=0.75)
        c.line(ell(x, y + 4 * s, 6 * s, 4.2 * s, 32), INNER, zone=0, closed=True)
    elif crop == "sunflower":
        c.line([(x, y), (x, y + 26 * s)], 0.9, zone=1)
        for i in range(10):
            a = i * math.pi / 5
            c.fill(ell(x + math.cos(a) * 4 * s, y + 26 * s + math.sin(a) * 4 * s, 2.2 * s, 1.2 * s, 12), zone=2)
        c.fill(ell(x, y + 26 * s, 2.6 * s, 2.6 * s, 20), zone=3, shade=0.6)


def _flower(c, x: float, y: float, h: float, dry: bool, zone: int = 2, shade: float = 1.0):
    if dry:                                                          # welk: Stiel hängt, Blüte kleiner und blass
        c.line(smooth([(x, y), (x + 1, y + h * 0.6), (x + 4, y + h * 0.55)], closed=False), 0.6, zone=1, shade=0.7)
        c.fill(ell(x + 4.5, y + h * 0.5, 1.8, 1.4, 16), zone=zone, shade=0.72)
        return
    c.line([(x, y), (x, y + h)], 0.6, zone=1)
    _lf(c, x, y + h * 0.35, h * 0.35, math.pi / 2 - 0.9, zone=1)
    for i in range(5):
        a = i * 2 * math.pi / 5 + 0.3
        c.fill(ell(x + math.cos(a) * 2.2, y + h + math.sin(a) * 2.2, 1.8, 1.8, 14), zone=zone, shade=shade)
    c.ellipse(x, y + h, 1.2, 1.2, zone=3, shade=1.6)


def yard(it: Item, style: str = "raised_bed", state: str = "", crop: str = "carrot", seed: int = 3):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    # ---------------------------------------------------------------- Säen, Gießen, Ernten
    if style == "raised_bed":                                        # Hochbeet aus Brettern
        for sx in (-1, 1):
            c.fill(rrect(sx * W / 2 - (5 if sx > 0 else 0), 0, sx * W / 2 + (0 if sx > 0 else 5), H * 0.72, 0.8), zone=3, shade=0.85)
        box = rrect(x0 + 2, 2, x1 - 2, H * 0.7, 0.8)
        cl = shaded(c, box, 3, "bottom", SHADE, 0.15)
        for k in range(1, 4):
            line(c, [(x0 + 2, H * 0.7 * k / 4), (x1 - 2, H * 0.7 * k / 4)], zone=3, clip=cl)
        _soil(c, x0 + 3, x1 - 3, H * 0.62, H * 0.72, seed)
        for k in range(4):
            _crop(c, x0 + W * (k + 0.5) / 4, H * 0.71, crop, state)
    elif style == "veg_bed":                                         # Beet am Boden mit Holzrand
        c.fill(rrect(x0, 0, x1, H * 0.45, 1), zone=3)
        c.line(rrect(x0, 0, x1, H * 0.45, 1), INNER, zone=0, closed=True)
        _soil(c, x0 + 2, x1 - 2, H * 0.3, H * 0.5, seed)
        n = max(3, int(W / 25))
        for k in range(n):
            _crop(c, x0 + W * (k + 0.5) / n, H * 0.48, crop, state, 0.9)
    elif style == "seeds":                                           # Samentüte mit Bild
        body = trap(x0, x1, 0, x0 + 0.3, x1 - 0.3, H, 0.4)
        shaded(c, body, 3, "right", SHADE, 0.2)
        c.fill(rrect(x0 + 1, H * 0.25, x1 - 1, H * 0.75, 0.6), zone=3, shade=1.3)
        _crop(c, 0, H * 0.3, crop, "ripe", 0.28)
        c.fill(rrect(x0, H * 0.88, x1, H, 0.3), zone=3, shade=0.8)
    elif style == "sprinkler":                                      # Kreisregner: runder Fuß, Säule, Dreh-Arm mit Düsen
        base = smooth([(x0, 0, "s"), (x1, 0, "s"), (W * 0.3, H * 0.35), (-W * 0.3, H * 0.35)])
        shaded(c, base, 1, "bottom", SHADE, 0.4)
        c.fill(rrect(-W * 0.06, H * 0.3, W * 0.06, H * 0.8, 0.8), zone=3)
        arm = rrect(-W * 0.44, H * 0.74, W * 0.44, H * 0.86, H * 0.06)
        shaded(c, arm, 1, "bottom", SHADE, 0.35)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.44, H * 0.8, W * 0.06, H * 0.1, 12), zone=2)
        c.fill(ell(0, H * 0.8, W * 0.09, H * 0.12, 16), zone=3)
        c.line([(-W * 0.3, H * 0.05), (-W * 0.5 - 6, H * 0.05)], 1.4, zone=1, shade=0.8)       # Schlauch-Anschluss
        if state == "on":                                            # Wasserbogen
            for sx in (-1, 1):
                for k in range(4):
                    a = sx * (0.35 + k * 0.18)
                    pts = [(sx * W * 0.4 + math.sin(a) * t * 30, H + t * 30 - t * t * 22) for t in (0, 0.3, 0.6, 0.9, 1.2)]
                    c.line(smooth(pts, closed=False), 0.5, zone=2, shade=1.2)
    elif style in ("spade", "rake", "shovel"):
        c.fill(rrect(-W * 0.06, H * 0.18, W * 0.06, H * 0.95, 0.6), zone=3)
        if style == "spade":
            c.fill(rrect(-W * 0.3, H * 0.92, W * 0.3, H, 1), zone=1)
            blade = rrect(-W * 0.36, 0, W * 0.36, H * 0.22, 1.5)
            shaded(c, blade, 2, "right", SHADE, 0.3)
        elif style == "shovel":
            c.fill(ell(0, H * 0.97, W * 0.18, H * 0.03, 16), zone=1)
            blade = smooth([(-W * 0.42, H * 0.22, "s"), (W * 0.42, H * 0.22, "s"), (W * 0.36, H * 0.05), (0, 0), (-W * 0.36, H * 0.05)])
            shaded(c, blade, 2, "right", SHADE, 0.3)
        else:
            c.fill(rrect(-W * 0.06, H * 0.9, W * 0.06, H, 0.6), zone=1)
            c.fill(rrect(x0, H * 0.14, x1, H * 0.2, 0.8), zone=2)
            for k in range(9):
                x = x0 + 1 + k * (W - 2) / 8
                c.line([(x, H * 0.15), (x, 0)], 0.8, zone=2)
    elif style == "flower_bed":                                      # Blumenbeet: welkt ohne Wasser
        c.fill(rrect(x0, 0, x1, H * 0.3, 2), zone=3, shade=0.8)
        for k in range(int(W / 12)):                                 # Steinkante
            c.fill(ell(x0 + 6 + k * 12, H * 0.08, 5.5, 3.6, 16), zone=3, shade=1.0 + (k % 2) * 0.1)
            c.line(ell(x0 + 6 + k * 12, H * 0.08, 5.5, 3.6, 16), INNER, zone=0, closed=True)
        _soil(c, x0 + 2, x1 - 2, H * 0.18, H * 0.32, seed)
        rng = random.Random(seed)
        n = int(W / 10)
        for k in range(n):
            x = x0 + 6 + k * (W - 12) / max(1, n - 1)
            _flower(c, x, H * 0.3, H * rng.uniform(0.45, 0.65), state == "dry", zone=2, shade=[1.0, 1.18, 0.88][k % 3])
    # ---------------------------------------------------------------- Zäune, Hecken, Wege
    elif style == "fence_rustic":                                    # Jägerzaun (gekreuzte Latten)
        for x in (x0 + 3, 0, x1 - 3):
            c.fill(rrect(x - 3, 0, x + 3, H, 1.5), zone=1)
            c.line(rrect(x - 3, 0, x + 3, H, 1.5), INNER, zone=0, closed=True)
        for k in range(8):
            a, b = x0 + k * W / 8, x0 + (k + 1) * W / 8
            c.line([(a, H * 0.15), (b + W / 8, H * 0.85)], 2.2, zone=1, shade=0.94)
            c.line([(b + W / 8, H * 0.15), (a, H * 0.85)], 2.2, zone=1, shade=0.9)
    elif style == "fence_lattice":                                   # Rankgitter mit Blüten
        c.fill(rrect(x0, 0, x0 + 5, H, 1), zone=1)
        c.fill(rrect(x1 - 5, 0, x1, H, 1), zone=1)
        grid = rrect(x0 + 5, H * 0.08, x1 - 5, H * 0.95, 0.5)
        cl = c.mask(grid)
        for k in range(-6, 12):
            c.line([(x0 + k * 12, H * 0.05), (x0 + k * 12 + H, H)], 1.2, zone=1, clip=cl)
            c.line([(x0 + k * 12 + H, H * 0.05), (x0 + k * 12, H)], 1.2, zone=1, shade=0.9, clip=cl)
        rng = random.Random(seed)
        for _ in range(9):
            x, y = rng.uniform(x0 + 8, x1 - 8), rng.uniform(H * 0.2, H * 0.9)
            _lf(c, x, y, 7, rng.uniform(0, 6.2), zone=3, shade=1.0)
            c.fill(ell(x + 2, y + 2, 2, 2, 12), zone=2)
    elif style == "hedge":
        rng = random.Random(seed)
        top = [(x1, 0), (x0, 0)]
        for k in range(9):
            top.append((x0 + W * k / 8, H * (0.9 + rng.uniform(-0.05, 0.08))))
        body = smooth([(x0, 0, "s"), (x1, 0, "s")] + [(x1, H * 0.85)] + top[2:][::-1] + [(x0, H * 0.85)])
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        for _ in range(int(W * H / 180)):
            x, y = rng.uniform(x0, x1), rng.uniform(4, H)
            _lf(c, x, y, 6, rng.uniform(0, 6.2), zone=1, shade=rng.choice([0.88, 1.08, 1.15]), clip=cl)
        if state != "plain":
            for _ in range(int(W / 25)):
                c.ellipse(rng.uniform(x0 + 5, x1 - 5), rng.uniform(H * 0.3, H * 0.85), 1.6, 1.6, zone=2, clip=cl)
    elif style == "gate":
        for sx in (-1, 1):
            c.fill(rrect(sx * W / 2 - 4, 0, sx * W / 2 + 4, H, 1.5), zone=3)
            c.fill(ell(sx * W / 2, H + 2, 4.5, 3, 16), zone=3, shade=1.1)
        for k in range(6):
            x = x0 + 8 + k * (W - 16) / 5
            top = H * 0.8 + math.sin(math.pi * k / 5) * H * 0.12
            c.fill([(x - 4, 4), (x + 4, 4), (x + 4, top), (x, top + 4), (x - 4, top)], zone=1)
            c.line([(x - 4, 4), (x - 4, top), (x, top + 4), (x + 4, top), (x + 4, 4)], INNER, zone=0)
        for y in (H * 0.2, H * 0.6):
            c.fill(rrect(x0 + 4, y, x1 - 4, y + 5, 1), zone=1, shade=0.88)
        knob(c, x1 - 10, H * 0.5, 1.4)
    elif style in ("path_stones", "path_gravel", "path_deck"):      # flach am Boden (placement rug)
        rng = random.Random(seed)
        if style == "path_stones":
            for k in range(4):
                x = x0 + W * (k + 0.5) / 4
                st = ell(x, H * 0.5, W * 0.1, H * 0.42, 24)
                shaded(c, st, 1, "bottom", SHADE, 0.3)
        elif style == "path_gravel":
            body = rrect(x0, 0, x1, H, H * 0.45)
            cl = shaded(c, body, 1, "bottom", SOFT, 0.3)
            for _ in range(int(W * H / 5)):
                c.ellipse(rng.uniform(x0, x1), rng.uniform(0, H), 0.9, 0.6, zone=[1, 2, 3][rng.randrange(3)], shade=0.85, clip=cl)
        else:
            body = rrect(x0, 0, x1, H, 0.6)
            cl = shaded(c, body, 1, "bottom", SHADE, 0.2)
            for k in range(1, int(W / 14)):
                line(c, [(x0 + k * 14, 0), (x0 + k * 14, H)], zone=1, clip=cl)
    # ---------------------------------------------------------------- Wasser
    elif style == "pool_frame":                                      # Aufstellpool mit Leiter
        body = rrect(x0, 0, x1, H, 3)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.12)
        for k in range(1, int(W / 30)):
            c.fill(rrect(x0 + k * 30 - 1.5, 0, x0 + k * 30 + 1.5, H, 0.5), zone=3, clip=cl)
        c.fill(rrect(x0 - 1, H - 4, x1 + 1, H, 1.5), zone=3)
        c.fill(ell(0, H - 2, W * 0.46, 2, 40), zone=2, shade=1.1)
        for sx in (-1, 1):
            c.line([(x1 - 22 + sx * 5, 0), (x1 - 20 + sx * 5, H + 18)], 1.2, zone=3)
        for k in range(4):
            c.line([(x1 - 27, 8 + k * (H + 8) / 4), (x1 - 15, 8 + k * (H + 8) / 4)], 1.0, zone=3)
    elif style == "pool_big":                                        # großer Pool (eingelassen, Kante + Wasser)
        c.fill(rrect(x0, 0, x1, H * 0.2, 1), zone=3)
        water = rrect(x0 + 4, H * 0.18, x1 - 4, H * 0.78, 1)
        cl = c.mask(water)
        c.fill(water, zone=2)
        for k in range(8):
            c.line(smooth([(x0 + k * W / 8, H * 0.6), (x0 + k * W / 8 + W / 32, H * 0.64), (x0 + (k + 0.5) * W / 8, H * 0.6)], closed=False),
                   0.6, zone=2, shade=1.35, clip=cl)
        for k in range(int(W / 20)):
            c.fill(rrect(x0 + k * 20, H * 0.78, x0 + k * 20 + 19, H, 0.5), zone=1, shade=1.0 + (k % 2) * 0.04)
            c.line(rrect(x0 + k * 20, H * 0.78, x0 + k * 20 + 19, H, 0.5), INNER, zone=0, closed=True)
        for sx in (-1, 1):
            c.line(smooth([(x1 - 30 + sx * 5, H * 0.3), (x1 - 30 + sx * 5, H + 16), (x1 - 36 + sx * 5, H + 22)], closed=False), 1.4,
                   zone=3, shade=1.2)
    elif style == "pond":                                            # flach am Boden (placement rug)
        rng = random.Random(seed)
        water = ell(0, H * 0.5, W * 0.46, H * 0.4, 64)
        c.fill(water, zone=2)
        cl = c.mask(water)
        c.fill(ell(0, H * 0.6, W * 0.4, H * 0.24, 48), zone=2, shade=1.15, clip=cl)
        for _ in range(3):
            x = rng.uniform(-W * 0.3, W * 0.3)
            c.line(smooth([(x - 8, H * 0.5), (x, H * 0.54), (x + 8, H * 0.5)], closed=False), 0.5, zone=2, shade=1.4, clip=cl)
        for k in range(int(W / 11)):
            a = 2 * math.pi * k / int(W / 11)
            x, y = math.cos(a) * W * 0.47, H * 0.5 + math.sin(a) * H * 0.42
            st = ell(x, y, 6, 3.2, 16)
            c.fill(st, zone=1, shade=0.95 + (k % 3) * 0.05)
            c.line(st, INNER, zone=0, closed=True)
        for sx in (-1, 1):                                           # Schilf
            for k in range(4):
                x = sx * W * 0.4 + k * 2 * sx
                c.line([(x, H * 0.5), (x + sx * 2, H * 0.5 + 24 + k * 4)], 0.7, zone=3)
                if k % 2:
                    c.fill(ell(x + sx * 2, H * 0.5 + 22 + k * 4, 1.1, 3, 12), zone=3, shade=0.6)
    elif style == "lily":
        pad = smooth([(x0, H * 0.3), (0, 0), (x1, H * 0.3), (W * 0.1, H * 0.45), (0, H * 0.3), (-W * 0.1, H * 0.45)])
        c.fill(pad, zone=3)
        c.line(pad, INNER, zone=0, closed=True)
        for i in range(7):
            a = math.pi * (0.15 + 0.7 * i / 6)
            c.fill(ell(math.cos(a) * W * 0.18, H * 0.45 + math.sin(a) * H * 0.3, W * 0.1, H * 0.22, 16), zone=1,
                   shade=1.0 + (i % 2) * 0.1)
        c.ellipse(0, H * 0.5, W * 0.07, H * 0.12, zone=2)
    elif style == "fountain":
        c.fill(trap(-W * 0.5, W * 0.5, 0, -W * 0.46, W * 0.46, H * 0.3, 2), zone=1)
        c.fill(ell(0, H * 0.3, W * 0.46, H * 0.04, 40), zone=2)
        c.fill(rrect(-W * 0.07, H * 0.3, W * 0.07, H * 0.62, 1.5), zone=1, shade=0.95)
        bowl = smooth([(-W * 0.3, H * 0.66, "s"), (W * 0.3, H * 0.66, "s"), (W * 0.1, H * 0.56), (-W * 0.1, H * 0.56)])
        shaded(c, bowl, 1, "bottom", SHADE, 0.35)
        c.fill(rrect(-W * 0.04, H * 0.66, W * 0.04, H * 0.8, 1), zone=1)
        if state == "on":
            for sx in (-1, 1):
                c.line(smooth([(0, H * 0.8), (sx * W * 0.12, H * 0.95), (sx * W * 0.25, H * 0.7), (sx * W * 0.3, H * 0.66)], closed=False),
                       0.7, zone=2, shade=1.25)
                c.line(smooth([(sx * W * 0.3, H * 0.64), (sx * W * 0.36, H * 0.45), (sx * W * 0.4, H * 0.32)], closed=False), 0.7, zone=2,
                       shade=1.25)
