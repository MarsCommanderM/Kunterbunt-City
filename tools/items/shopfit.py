"""
Ladeneinrichtung (P09-T02): Regale, Kühlregal, Kassentheke mit Band, Theke, Vitrine, Obststand, Blumentreppe,
Eistheke, Umkleide, Haarwaschbecken, Trockenhaube, Brotregal, Zeitschriftenständer, Aquarienregal.
Zonen: 1 = Möbelfarbe · 2 = Ware/Akzent (in Schattierungen) · 3 = Metall/Holz/Glas.
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, ell, line, rrect, shaded, smooth, trap

GLASS = 1.55     # sehr helle Zone-3-Schattierung = Glas


def _goods(c, x0: float, x1: float, y: float, h: float, rng: random.Random, kind: str = "box", clip=None):
    """Ware auf einem Regalboden: Schachteln, Flaschen, Dosen, Gläser – in Zone 2 mit wechselnder Helligkeit."""
    x = x0 + 1.5
    while x < x1 - 4:
        k = kind if kind != "mix" else rng.choice(["box", "bottle", "can", "jar"])
        sh = rng.choice([0.72, 0.85, 1.0, 1.15, 1.3])
        if k == "box":
            w, hh = rng.uniform(7, 12), h * rng.uniform(0.6, 0.9)
            if x + w > x1 - 1.5:
                break
            b = rrect(x, y, x + w, y + hh, 0.6)
            c.fill(b, zone=2, shade=sh, clip=clip)
            c.fill(rrect(x + w * 0.2, y + hh * 0.45, x + w * 0.8, y + hh * 0.75, 0.5), zone=1, shade=1.25, clip=clip)
            c.line(b, INNER, zone=0, closed=True, clip=clip)
        elif k == "bottle":
            w, hh = 5.0, h * rng.uniform(0.75, 0.95)
            if x + w > x1 - 1.5:
                break
            b = smooth([(x, y, "s"), (x + w, y, "s"), (x + w, y + hh * 0.6), (x + w * 0.65, y + hh * 0.8), (x + w * 0.65, y + hh, "s"),
                        (x + w * 0.35, y + hh, "s"), (x + w * 0.35, y + hh * 0.8), (x, y + hh * 0.6)])
            c.fill(b, zone=2, shade=sh, clip=clip)
            c.fill(rrect(x + 0.6, y + hh * 0.25, x + w - 0.6, y + hh * 0.45, 0.3), zone=3, shade=1.4, clip=clip)
            c.line(b, INNER, zone=0, closed=True, clip=clip)
        elif k == "can":
            w, hh = 6.0, h * 0.5
            if x + w > x1 - 1.5:
                break
            for s in range(2 if h > 18 else 1):
                b = rrect(x, y + s * hh, x + w, y + (s + 1) * hh - 0.3, 0.8)
                c.fill(b, zone=2, shade=sh, clip=clip)
                c.fill(rrect(x, y + s * hh + hh * 0.35, x + w, y + s * hh + hh * 0.6, 0.2), zone=3, shade=1.4, clip=clip)
                c.line(b, INNER, zone=0, closed=True, clip=clip)
        else:                                                     # Glas mit Deckel
            w, hh = 7.0, h * 0.55
            if x + w > x1 - 1.5:
                break
            b = rrect(x, y, x + w, y + hh, 1.2)
            c.fill(b, zone=2, shade=sh, clip=clip)
            c.fill(rrect(x - 0.3, y + hh - 1.6, x + w + 0.3, y + hh, 0.5), zone=3, clip=clip)
            c.line(b, INNER, zone=0, closed=True, clip=clip)
        x += w + rng.uniform(0.8, 2.0)


def _fruit_row(c, x0: float, x1: float, y: float, r: float, rng: random.Random, clip=None):
    x = x0 + r
    while x < x1 - r:
        sh = rng.choice([0.8, 0.95, 1.1, 1.25])
        for dy in (0, r * 1.3):
            c.fill(ell(x + (r * 0.5 if dy else 0), y + r + dy, r, r * 0.95, 16), zone=2, shade=sh, clip=clip)
            c.fill(ell(x - r * 0.3 + (r * 0.5 if dy else 0), y + r * 1.35 + dy, r * 0.28, r * 0.22, 10), zone=2, shade=1.5, clip=clip)
        x += r * 2.1


def _frame(c, W: float, H: float, zone: int = 1):
    body = rrect(-W / 2, 0, W / 2, H, 1.0)
    shaded(c, body, zone, "right", SHADE, 0.12)
    return body


def shopfit(it: Item, style: str = "shelf_market", state: str = "", seed: int = 3):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    rng = random.Random(seed + int(W) + int(H))
    if style in ("shelf_market", "shelf_toys", "shelf_electro", "shelf_pets", "shelf_bread", "shelf_books"):
        body = _frame(c, W, H)
        c.fill(rrect(x0 + 3, 8, x1 - 3, H - 10, 0.6), zone=1, shade=0.62)           # Rückwand innen
        c.fill(rrect(x0, H - 10, x1, H, 1.0), zone=2, shade=1.0)                    # Kopfschild (Farbe, kein Text)
        c.fill(ell(0, H - 5, 3.2, 3.2, 20), zone=1, shade=1.35)
        n = 4 if H > 140 else 3
        gap = (H - 18) / n
        kind = {"shelf_market": "mix", "shelf_bread": "bread", "shelf_toys": "toys", "shelf_electro": "electro",
                "shelf_pets": "mix", "shelf_books": "books"}[style]
        for k in range(n):
            y = 8 + k * gap
            c.fill(rrect(x0 + 1, y - 2.5, x1 - 1, y, 0.4), zone=3)
            c.fill(rrect(x0 + 1, y - 2.5, x1 - 1, y - 1.6, 0.3), zone=2, shade=0.8)      # Preisleiste
            if kind == "mix":
                _goods(c, x0 + 3, x1 - 3, y, gap - 4, rng, "mix")
            elif kind == "bread":
                xx = x0 + 5
                while xx < x1 - 16:
                    lw = rng.uniform(12, 20)
                    loaf = smooth([(xx, y, "s"), (xx + lw, y, "s"), (xx + lw, y + gap * 0.3), (xx + lw * 0.5, y + gap * 0.5),
                                   (xx, y + gap * 0.3)])
                    c.fill(loaf, zone=2, shade=rng.choice([0.8, 0.95, 1.1]))
                    for s in range(3):
                        line(c, [(xx + lw * (0.25 + s * 0.2), y + gap * 0.2), (xx + lw * (0.35 + s * 0.2), y + gap * 0.42)], zone=2)
                    c.line(loaf, INNER, zone=0, closed=True)
                    xx += lw + 3
            elif kind == "books":
                xx = x0 + 4
                while xx < x1 - 6:
                    bw = rng.uniform(2.5, 4.5)
                    bh = gap * rng.uniform(0.55, 0.8)
                    b = rrect(xx, y, xx + bw, y + bh, 0.3)
                    c.fill(b, zone=2, shade=rng.choice([0.7, 0.85, 1.0, 1.2, 1.35]))
                    c.line(b, INNER, zone=0, closed=True)
                    xx += bw + 0.4
            elif kind == "toys":                                   # Bälle, Teddys, Autos, Klötze
                xx = x0 + 6
                while xx < x1 - 14:
                    t = rng.choice(["ball", "teddy", "car", "blocks"])
                    sh = rng.choice([0.85, 1.0, 1.2])
                    if t == "ball":
                        c.fill(ell(xx + 6, y + 6, 6, 6, 24), zone=2, shade=sh)
                        c.fill(ell(xx + 4, y + 8, 1.6, 1.2, 10), zone=2, shade=1.6)
                        xx += 14
                    elif t == "teddy":
                        c.fill(ell(xx + 7, y + 6, 6, 6, 20), zone=3, shade=0.9)
                        c.fill(ell(xx + 7, y + 15, 5, 5, 20), zone=3, shade=0.95)
                        for sx in (-1, 1):
                            c.fill(ell(xx + 7 + sx * 4, y + 19, 1.8, 1.8, 12), zone=3, shade=0.8)
                        c.fill(ell(xx + 7, y + 13.5, 2, 1.4, 12), zone=3, shade=1.3)
                        xx += 16
                    elif t == "car":
                        c.fill(rrect(xx, y + 3, xx + 16, y + 9, 1.5), zone=2, shade=sh)
                        c.fill(rrect(xx + 4, y + 8, xx + 12, y + 13, 1.5), zone=2, shade=sh * 0.9)
                        for wx in (xx + 4, xx + 12):
                            c.fill(ell(wx, y + 3, 2.4, 2.4, 14), zone=0)
                        xx += 20
                    else:
                        for bx, by in ((0, 0), (6, 0), (3, 6)):
                            b = rrect(xx + bx, y + by, xx + bx + 5.5, y + by + 5.5, 0.6)
                            c.fill(b, zone=2, shade=rng.choice([0.8, 1.0, 1.25]))
                            c.line(b, INNER, zone=0, closed=True)
                        xx += 14
            elif kind == "electro":                                # Fernseher, Lautsprecher, Kopfhörer
                xx = x0 + 5
                while xx < x1 - 14:
                    if rng.random() < 0.5:
                        scr = rrect(xx, y + 3, xx + 24, y + gap * 0.62, 1.0)
                        c.fill(scr, zone=0)
                        c.fill(rrect(xx + 1.5, y + 4.5, xx + 22.5, y + gap * 0.62 - 1.5, 0.6), zone=2, shade=rng.choice([0.8, 1.2]))
                        c.fill(rrect(xx + 10, y, xx + 14, y + 3, 0.4), zone=3)
                        xx += 28
                    else:
                        b = rrect(xx, y, xx + 10, y + gap * 0.55, 1.2)
                        c.fill(b, zone=3, shade=0.5)
                        c.fill(ell(xx + 5, y + gap * 0.18, 3.2, 3.2, 16), zone=3, shade=0.9)
                        c.fill(ell(xx + 5, y + gap * 0.42, 2, 2, 14), zone=3, shade=0.9)
                        c.line(b, INNER, zone=0, closed=True)
                        xx += 14
        c.line(body, INNER, zone=0, closed=True)
    elif style == "fridge_shelf":                                  # offenes Kühlregal mit Glasfront oben
        body = _frame(c, W, H)
        inner = rrect(x0 + 4, 30, x1 - 4, H - 14, 0.8)
        c.fill(inner, zone=3, shade=1.35)
        cl = c.mask(inner)
        gap = (H - 44) / 4
        for k in range(4):
            y = 30 + k * gap
            c.fill(rrect(x0 + 4, y, x1 - 4, y + 1.4, 0.3), zone=3, shade=0.8)
            _goods(c, x0 + 6, x1 - 6, y + 1.4, gap - 5, rng, "bottle" if k % 2 else "box", clip=cl)
        c.fill(rrect(x0 + 4, 30, x1 - 4, H - 14, 0.8), zone=3, shade=GLASS, alpha=0.25)
        for k in range(1, 4):
            c.line([(x0 + 4 + (W - 8) * k / 4, 30), (x0 + 4 + (W - 8) * k / 4, H - 14)], 0.8, zone=3, shade=0.7)
        c.fill(rrect(x0, H - 14, x1, H, 1.0), zone=2)
        c.fill(rrect(x0, 0, x1, 30, 1.0), zone=1, shade=0.9)
        for k in range(6):
            c.line([(x0 + 6 + k * (W - 12) / 5, 6), (x0 + 6 + k * (W - 12) / 5, 22)], 0.6, zone=1, shade=0.7)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "checkout":                                      # Kassentheke mit Laufband
        body = rrect(x0, 0, x1, H - 4, 1.2)
        shaded(c, body, 1, "bottom", SHADE, 0.2)
        c.fill(rrect(x0, H - 6, x1, H, 0.8), zone=3, shade=0.5)                # Band
        for k in range(12):
            xx = x0 + 3 + k * (W - 6) / 12
            line(c, [(xx, H - 5.6), (xx + 2, H - 0.4)], zone=3, shade=0.8, w=0.4)
        c.fill(ell(x0 + 3, H - 3, 3, 3, 16), zone=3, shade=0.8)
        c.fill(ell(x1 - 3, H - 3, 3, 3, 16), zone=3, shade=0.8)
        c.fill(rrect(x0 + 6, H * 0.35, x1 - 6, H * 0.55, 1.0), zone=2)
        c.line(body, INNER, zone=0, closed=True)
    elif style in ("counter", "counter_glass"):                   # Theke (Bäckerei, Café, Blumen, Tierhandlung)
        top = rrect(x0 - 2, H - 5, x1 + 2, H, 1.0)
        body = rrect(x0, 0, x1, H - 5, 1.0)
        shaded(c, body, 1, "right", SHADE, 0.15)
        if style == "counter_glass":                                # Vitrine mit Kuchen/Gebäck
            gl = rrect(x0 + 4, H * 0.3, x1 - 4, H - 8, 1.0)
            c.fill(gl, zone=3, shade=1.35)
            cl = c.mask(gl)
            for row, y in enumerate((H * 0.32, H * 0.58)):
                c.fill(rrect(x0 + 4, y - 1.2, x1 - 4, y, 0.3), zone=3, shade=0.8, clip=cl)
                xx = x0 + 8
                while xx < x1 - 16:
                    t = rng.choice(["cake", "croissant", "tart", "cupcake"])
                    sh = rng.choice([0.85, 1.0, 1.15])
                    if t == "cake":
                        cake = rrect(xx, y, xx + 16, y + 10, 1.2)
                        c.fill(cake, zone=2, shade=sh, clip=cl)
                        c.fill(rrect(xx, y + 7, xx + 16, y + 10, 1.2), zone=2, shade=1.4, clip=cl)
                        c.fill(ell(xx + 8, y + 11, 1.4, 1.4, 12), zone=1, shade=1.1, clip=cl)
                        xx += 20
                    elif t == "croissant":
                        cr = smooth([(xx, y + 1, "s"), (xx + 6, y + 6), (xx + 12, y + 1, "s"), (xx + 6, y + 3)])
                        c.fill(cr, zone=2, shade=0.9, clip=cl)
                        xx += 15
                    elif t == "tart":
                        c.fill(ell(xx + 7, y + 2.5, 7, 2.5, 20), zone=2, shade=0.95, clip=cl)
                        for k in range(3):
                            c.fill(ell(xx + 3 + k * 4, y + 4, 1.6, 1.2, 10), zone=1, shade=1.1, clip=cl)
                        xx += 17
                    else:
                        c.fill(trap(xx, xx + 7, y, xx - 0.6, xx + 7.6, y + 4, 0.3), zone=3, shade=1.2, clip=cl)
                        c.fill(ell(xx + 3.5, y + 5.5, 4, 2.6, 16), zone=2, shade=1.35, clip=cl)
                        xx += 11
            c.fill(rrect(x0 + 4, H * 0.3, x1 - 4, H - 8, 1.0), zone=3, shade=GLASS, alpha=0.22)
            line(c, [(x0 + 8, H - 12), (x0 + 20, H * 0.4)], zone=3, shade=1.8, w=0.8)
            c.line(gl, INNER, zone=0, closed=True)
        else:
            for k in range(1, 4):
                line(c, [(x0 + W * k / 4, 4), (x0 + W * k / 4, H - 9)], zone=1)
            c.fill(rrect(x0 + 6, H * 0.45, x1 - 6, H * 0.6, 1.0), zone=2)
        c.fill(top, zone=3)
        c.line(body, INNER, zone=0, closed=True)
        c.line(top, INNER, zone=0, closed=True)
    elif style == "produce_stand":                                 # schräge Obst-/Gemüsekisten auf Gestell
        for sx in (-1, 1):
            c.fill(rrect(sx * (W / 2 - 4) - 2, 0, sx * (W / 2 - 4) + 2, H * 0.6, 0.6), zone=3)
        for row in range(2):
            y = H * (0.22 + row * 0.36)
            n = 3
            for k in range(n):
                bx0 = x0 + 2 + k * (W - 4) / n
                bx1 = bx0 + (W - 4) / n - 2
                box = trap(bx0, bx1, y, bx0 + 1, bx1 - 1, y + H * 0.14, 0.4)
                c.fill(box, zone=3, shade=0.95)
                _fruit_row(c, bx0 + 1.5, bx1 - 1.5, y + H * 0.1, 3.4, random.Random(seed + k + row * 3))
                c.fill(trap(bx0, bx1, y, bx0 + 1, bx1 - 1, y + H * 0.12, 0.4), zone=3, shade=0.85)
                for s in (0.35, 0.7):
                    line(c, [(bx0, y + H * 0.12 * s), (bx1, y + H * 0.12 * s)], zone=3)
                c.line(box, INNER, zone=0, closed=True)
        c.fill(rrect(x0, H * 0.9, x1, H, 1.0), zone=1)                          # Dach-Brett
        for k in range(8):
            c.fill(rrect(x0 + k * W / 8, H * 0.86, x0 + (k + 0.5) * W / 8, H * 0.9, 0.3), zone=2)
    elif style == "flower_stand":                                  # Blumentreppe mit Eimern voller Blumen
        for step in range(3):
            y = step * H * 0.25
            sw = W * (1 - step * 0.25)
            st = rrect(-sw / 2, y, sw / 2, y + 4, 0.5)
            c.fill(st, zone=3)
            c.line(st, INNER, zone=0, closed=True)
            n = max(2, int(sw / 22))
            for k in range(n):
                bx = -sw / 2 + (k + 0.5) * sw / n
                bucket = trap(bx - 7, bx + 7, y + 4, bx - 8.5, bx + 8.5, y + 18, 0.5)
                c.fill(bucket, zone=3, shade=0.7)
                fr = random.Random(seed + step * 7 + k)
                for f in range(7):
                    fx = bx + fr.uniform(-8, 8)
                    fy = y + 18 + fr.uniform(8, 20)
                    c.line([(bx + (fx - bx) * 0.3, y + 16), (fx, fy)], 0.6, zone=3, shade=0.4)
                    col = fr.choice([1, 2])
                    for p in range(5):
                        a = p * 1.2566
                        c.fill(ell(fx + math.cos(a) * 2.2, fy + math.sin(a) * 2.2, 1.9, 1.9, 10), zone=col,
                               shade=fr.choice([0.95, 1.1]))
                    c.fill(ell(fx, fy, 1.3, 1.3, 10), zone=2 if col == 1 else 1, shade=1.3)
                c.line(bucket, INNER, zone=0, closed=True)
    elif style == "icecream_counter":                              # Eistheke: Glasbogen, bunte Eiswannen
        body = rrect(x0, 0, x1, H * 0.7, 1.2)
        shaded(c, body, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0 + 5, H * 0.25, x1 - 5, H * 0.55, 1.2), zone=2)
        n = max(4, int(W / 20))
        for k in range(n):
            tx = x0 + 6 + (k + 0.5) * (W - 12) / n
            c.fill(trap(tx - 8, tx + 8, H * 0.7, tx - 8.5, tx + 8.5, H * 0.74, 0.3), zone=3, shade=1.2)
            c.fill(smooth([(tx - 8, H * 0.74, "s"), (tx - 4, H * 0.8), (tx + 1, H * 0.77), (tx + 6, H * 0.81), (tx + 8, H * 0.74, "s")]),
                   zone=2 if k % 2 else 1, shade=[1.35, 1.1, 0.9, 1.5, 0.8][k % 5])
        dome = smooth([(x0 + 2, H * 0.7, "s"), (x0 + 2, H * 0.84), (x0 + 8, H, "s"), (x1 - 2, H, "s"), (x1 - 2, H * 0.7, "s")])
        c.fill(dome, zone=3, shade=GLASS, alpha=0.3)
        c.line(dome, 0.6, zone=3, shade=0.7, closed=False)
        line(c, [(x0 + 10, H * 0.95), (x0 + 30, H * 0.78)], zone=3, shade=1.9, w=0.8)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "fitting_room":                                  # Umkleide: Rahmen + Vorhang (auf/zu)
        c.fill(rrect(x0, H - 6, x1, H, 0.8), zone=3)
        for sx in (-1, 1):
            c.fill(rrect(sx * W / 2 - 2, 0, sx * W / 2 + 2, H, 0.6), zone=3)
        c.fill(rrect(x0 + 2, 0, x1 - 2, H - 6, 0.5), zone=1, shade=0.6)
        c.fill(ell(0, H * 0.55, W * 0.18, H * 0.2, 24), zone=3, shade=1.6)        # Spiegel
        if state == "open":
            cur = smooth([(x0 + 2, H - 6, "s"), (x0 + W * 0.22, H - 6, "s"), (x0 + W * 0.18, H * 0.5), (x0 + W * 0.24, 2, "s"),
                          (x0 + 2, 2, "s")])
        else:
            cur = rrect(x0 + 2, 2, x1 - 2, H - 6, 0.5)
        cl = shaded(c, cur, 2, "right", SHADE, 0.12)
        cx0 = x0 + 2
        cx1 = x0 + W * 0.24 if state == "open" else x1 - 2
        for k in range(1, 9):
            xx = cx0 + (cx1 - cx0) * k / 9
            line(c, [(xx, 3), (xx, H - 7)], zone=2, clip=cl)
        for k in range(10):
            c.fill(ell(x0 + 4 + k * (W - 8) / 9, H - 5, 1.2, 1.2, 10), zone=3, shade=0.8)
    elif style == "hair_sink":                                     # Haarwaschbecken mit Sitz
        seat = rrect(x0, H * 0.35, x0 + W * 0.7, H * 0.5, 2.0)
        c.fill(trap(x0 + W * 0.15, x0 + W * 0.55, 0, x0 + W * 0.2, x0 + W * 0.5, H * 0.35, 0.6), zone=3, shade=0.7)
        c.fill(seat, zone=1)
        c.fill(rrect(x0 + W * 0.02, H * 0.5, x0 + W * 0.18, H * 0.9, 2.0), zone=1, shade=0.92)
        c.fill(trap(x1 - W * 0.35, x1, 0, x1 - W * 0.3, x1 - 2, H * 0.62, 0.6), zone=1, shade=0.85)
        basin = smooth([(x1 - W * 0.42, H * 0.62, "s"), (x1, H * 0.62, "s"), (x1 - 2, H * 0.78), (x1 - W * 0.4, H * 0.78)])
        c.fill(basin, zone=3, shade=1.5)
        c.fill(ell(x1 - W * 0.2, H * 0.74, W * 0.14, H * 0.03, 16), zone=3, shade=1.0)
        c.line([(x1 - 4, H * 0.78), (x1 - 4, H * 0.92), (x1 - 12, H * 0.92)], 1.0, zone=3, shade=0.8)
        c.line(seat, INNER, zone=0, closed=True)
    elif style == "dryer_hood":                                    # Trockenhaube auf Ständer
        c.fill(ell(0, 2, W * 0.4, 2.5, 20), zone=3, shade=0.8)
        c.fill(rrect(-1.5, 2, 1.5, H * 0.6, 0.6), zone=3)
        hood = smooth([(-W / 2, H * 0.62, "s"), (-W / 2 + 2, H * 0.9), (0, H, "s"), (W / 2 - 2, H * 0.9), (W / 2, H * 0.62, "s")])
        shaded(c, hood, 1, "right", SHADE, 0.3)
        c.fill(ell(0, H * 0.62, W / 2, H * 0.06, 24), zone=1, shade=0.6)
        c.fill(rrect(W * 0.15, H * 0.78, W * 0.35, H * 0.84, 0.6), zone=2)
        c.line(hood, INNER, zone=0, closed=True)
    elif style == "magazine_rack":                                 # Zeitschriften-/Postkartenständer
        c.fill(rrect(-2, 0, 2, H, 0.6), zone=3)
        c.fill(ell(0, 2, W * 0.45, 2, 20), zone=3, shade=0.8)
        for row in range(4):
            y = H * 0.25 + row * H * 0.18
            for k in range(3):
                x = -W * 0.4 + k * W * 0.28
                mg = rrect(x, y, x + W * 0.24, y + H * 0.16, 0.4)
                c.fill(mg, zone=2, shade=[0.8, 1.0, 1.2, 1.35][(row + k) % 4])
                c.fill(rrect(x + 1, y + H * 0.08, x + W * 0.24 - 1, y + H * 0.13, 0.3), zone=1, shade=1.3)
                c.line(mg, INNER, zone=0, closed=True)
    elif style == "tank_shelf":                                    # Tierhandlung: Regal mit Aquarien + Käfig
        body = _frame(c, W, H)
        for row, y in enumerate((6, H * 0.52)):
            tank = rrect(x0 + 4, y, x1 - 4, y + H * 0.4, 0.8)
            c.fill(tank, zone=3, shade=1.45)
            cl = c.mask(tank)
            c.fill(rrect(x0 + 4, y, x1 - 4, y + H * 0.06, 0.5), zone=3, shade=0.9, clip=cl)
            if row == 0:
                for k in range(4):
                    fx = x0 + 12 + k * (W - 24) / 3
                    fy = y + H * (0.15 + 0.06 * (k % 2))
                    c.fill(ell(fx, fy, 3.2, 2, 14), zone=2, shade=[1.0, 1.3, 0.8, 1.15][k], clip=cl)
                    c.fill([(fx + 2.8, fy), (fx + 5, fy + 1.8), (fx + 5, fy - 1.8)], zone=2, shade=0.8, clip=cl)
                for k in range(3):
                    line(c, [(x0 + 8 + k * 9, y + 2), (x0 + 6 + k * 9, y + H * 0.3)], zone=1, shade=0.7, w=0.8, clip=cl)
            else:
                for k in range(int(W / 5)):
                    line(c, [(x0 + 5 + k * 5, y), (x0 + 5 + k * 5, y + H * 0.4)], zone=3, shade=0.7, w=0.5, clip=cl)
                c.fill(ell(0, y + H * 0.08, 7, 5, 16), zone=2, shade=1.2, clip=cl)
            c.line(tank, INNER, zone=0, closed=True)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "coffee_machine":                                # Siebträger-Kaffeemaschine (Café)
        body = rrect(x0, 0, x1, H * 0.85, 2.0)
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(rrect(x0, H * 0.85, x1, H, 1.0), zone=3)
        for sx in (-0.25, 0.25):
            c.fill(rrect(sx * W - 5, H * 0.5, sx * W + 5, H * 0.58, 1.0), zone=3, shade=0.7)
            c.fill(rrect(sx * W - 1, H * 0.35, sx * W + 1, H * 0.5, 0.4), zone=3, shade=0.6)
            c.fill(trap(sx * W - 3, sx * W + 3, H * 0.08, sx * W - 3.5, sx * W + 3.5, H * 0.2, 0.4), zone=2, shade=1.3)
        c.fill(rrect(x0 + 2, H * 0.05, x1 - 2, H * 0.08, 0.4), zone=3, shade=0.7)
        c.fill(ell(0, H * 0.72, 3, 3, 16), zone=2)
        c.line(body, INNER, zone=0, closed=True)


def flowers(it: Item, style: str = "stem", kind: str = "rose"):
    """Blumenladen: einzelne Blume (Rose, Tulpe, Sonnenblume, Gerbera) und gebundener Strauß mit Papier + Schleife."""
    c, W, H = it.c, it.w, it.h

    def bloom(x: float, y: float, r: float, k: str, zone: int = 1, sh: float = 1.0):
        if k == "tulip":
            b = smooth([(x - r, y + r * 0.3, "s"), (x - r * 0.9, y - r * 0.7), (x, y - r, "s"), (x + r * 0.9, y - r * 0.7),
                        (x + r, y + r * 0.3, "s"), (x + r * 0.5, y + r), (x, y + r * 0.4), (x - r * 0.5, y + r)])
            c.fill(b, zone=zone, shade=sh)
            line(c, [(x, y + r * 0.4), (x, y - r * 0.6)], zone=zone)
            c.line(b, INNER, zone=0, closed=True)
        elif k == "sunflower":
            for p in range(12):
                a = p * math.pi / 6
                c.fill(ell(x + math.cos(a) * r * 0.75, y + math.sin(a) * r * 0.75, r * 0.38, r * 0.38, 10), zone=2, shade=1.25)
            c.fill(ell(x, y, r * 0.5, r * 0.5, 20), zone=3, shade=0.45)
        elif k == "gerbera":
            for p in range(14):
                a = p * math.pi / 7
                c.fill(ell(x + math.cos(a) * r * 0.7, y + math.sin(a) * r * 0.7, r * 0.3, r * 0.3, 10), zone=zone, shade=sh)
            c.fill(ell(x, y, r * 0.35, r * 0.35, 16), zone=2, shade=1.2)
        else:                                                       # Rose: Blütenkopf mit Spirale
            b = ell(x, y, r, r * 0.92, 24)
            c.fill(b, zone=zone, shade=sh)
            c.line([(x + math.cos(t * 0.6) * r * t / 10, y + math.sin(t * 0.6) * r * t / 10) for t in range(1, 11)], 0.35,
                   zone=zone, shade=0.7)
            c.line(b, INNER, zone=0, closed=True)

    if style == "stem":
        c.line([(0, 0), (0.6, H * 0.8)], 0.8, zone=3, shade=0.45)
        c.fill(smooth([(0.3, H * 0.35), (W * 0.45, H * 0.45), (0.3, H * 0.5)]), zone=3, shade=0.55)
        bloom(0.6, H * 0.84, W * 0.42, kind)
    else:                                                           # Strauß
        rng = random.Random(7)
        for k in range(9):
            x = rng.uniform(-W * 0.3, W * 0.3)
            y = H * rng.uniform(0.62, 0.9)
            c.line([(0, H * 0.3), (x, y)], 0.6, zone=3, shade=0.45)
        for k in range(9):
            x = rng.uniform(-W * 0.32, W * 0.32)
            y = H * rng.uniform(0.62, 0.9)
            bloom(x, y, W * 0.14, rng.choice(["rose", "tulip", "gerbera"]), zone=1 if k % 2 else 2, sh=rng.choice([0.9, 1.1]))
        paper = [(-W * 0.12, 0), (W * 0.12, 0), (W * 0.5, H * 0.66), (-W * 0.5, H * 0.66)]
        c.fill(paper, zone=3, shade=1.55)
        c.fill([(-W * 0.12, 0), (W * 0.12, 0), (W * 0.2, H * 0.3), (-W * 0.2, H * 0.3)], zone=3, shade=1.4)
        c.line(paper, INNER, zone=0, closed=True)
        c.fill(ell(0, H * 0.3, W * 0.08, W * 0.06, 12), zone=2, shade=0.8)
        for sx in (-1, 1):
            c.fill(smooth([(0, H * 0.3), (sx * W * 0.22, H * 0.38, "s"), (sx * W * 0.2, H * 0.24, "s")]), zone=2, shade=0.8)
            c.line([(0, H * 0.28), (sx * W * 0.1, H * 0.1)], 0.6, zone=2, shade=0.8)
