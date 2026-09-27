"""
Vorrat & Gerichte (P07-Inventar): Spaghetti, Nudelpackung, Reis, Brötchen, Brezel, Baguette, Croissant, Milch, Joghurt,
Butter, Müsli, Marmelade, Honig, Saft, Wasser, Kekse, Schokolade, Bonbons, Donut, Lutscher, Burger, Pommes, Hotdog,
Sandwich, Salat.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe (Etikett, Glasur, Soße) · 3 = Dritte (Deckel, Teller, Grün).
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, ell, line, rrect, shaded, smooth, trap


def _plate(c, W: float, H: float, zone: int = 3):
    c.fill(ell(0, H * 0.12, W / 2, H * 0.12, 32), zone=zone, shade=0.9)
    c.fill(ell(0, H * 0.16, W * 0.4, H * 0.08, 32), zone=zone, shade=1.1)
    c.line(ell(0, H * 0.12, W / 2, H * 0.12, 32), INNER, zone=0, closed=True)


def _jar(c, W: float, H: float, label: bool = True):
    body = rrect(-W * 0.42, 0, W * 0.42, H * 0.8, W * 0.12)
    cl = shaded(c, body, 1, "right", SHADE, 0.25)
    c.fill(rrect(-W * 0.46, H * 0.78, W * 0.46, H, 1), zone=3)
    c.line(rrect(-W * 0.46, H * 0.78, W * 0.46, H, 1), INNER, zone=0, closed=True)
    if label:
        c.fill(rrect(-W * 0.42, H * 0.25, W * 0.42, H * 0.55, 0.4), zone=2, clip=cl)
    return cl


def pantry(it: Item, style: str = "spaghetti"):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "spaghetti":                                          # Teller Spaghetti mit Soße
        _plate(c, W, H)
        nest = smooth([(-W * 0.36, H * 0.2), (W * 0.36, H * 0.2), (W * 0.26, H * 0.7), (0, H * 0.8), (-W * 0.26, H * 0.7)])
        cl = shaded(c, nest, 1, "bottom", SHADE, 0.3)
        for k in range(10):
            a = k * 0.7
            c.line(smooth([(-W * 0.3 + k * W * 0.06, H * 0.22), (-W * 0.2 + k * W * 0.04 + math.sin(a) * 3, H * 0.5),
                           (-W * 0.1 + k * W * 0.03, H * 0.75)], closed=False), 0.3, zone=1, shade=0.8, clip=cl)
        c.fill(ell(0, H * 0.7, W * 0.2, H * 0.14, 20), zone=2)
        for dx in (-W * 0.06, W * 0.07):
            c.fill(ell(dx, H * 0.8, W * 0.05, W * 0.05, 12), zone=2, shade=0.75)
        c.fill(ell(W * 0.05, H * 0.86, W * 0.04, H * 0.03, 10), zone=3, shade=0.7)
    elif style in ("pasta_spaghetti", "pasta_penne", "pasta_farfalle"):  # Packung mit Sichtfenster
        body = rrect(x0, 0, x1, H, 0.8)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        win = rrect(-W * 0.3, H * 0.2, W * 0.3, H * 0.62, 1)
        c.fill(win, zone=2, clip=cl)
        wl = c.mask(win)
        for k in range(8):
            if style == "pasta_spaghetti":
                c.line([(-W * 0.28 + k * W * 0.08, H * 0.2), (-W * 0.26 + k * W * 0.08, H * 0.62)], 0.3, zone=2, shade=0.8, clip=wl)
            elif style == "pasta_penne":
                c.fill(rrect(-W * 0.3 + (k % 4) * W * 0.16, H * (0.25 + (k // 4) * 0.18), -W * 0.2 + (k % 4) * W * 0.16,
                             H * (0.38 + (k // 4) * 0.18), 0.4), zone=2, shade=0.85, clip=wl)
            else:
                x, y = -W * 0.2 + (k % 3) * W * 0.2, H * (0.3 + (k // 3) * 0.12)
                c.fill([(x - 2, y - 1.2), (x, y), (x - 2, y + 1.2)], zone=2, shade=0.85, clip=wl)
                c.fill([(x + 2, y - 1.2), (x, y), (x + 2, y + 1.2)], zone=2, shade=0.85, clip=wl)
        c.line(win, INNER, zone=0, closed=True)
        c.fill(rrect(x0, H * 0.78, x1, H * 0.9, 0.3), zone=3, clip=cl)
    elif style == "rice":
        bag = smooth([(x0, 0, "s"), (x1, 0, "s"), (x1, H * 0.85), (W * 0.3, H), (-W * 0.3, H), (x0, H * 0.85)])
        cl = shaded(c, bag, 1, "right", SHADE, 0.2)
        c.fill(ell(0, H * 0.45, W * 0.3, H * 0.18, 20), zone=2, clip=cl)
        for k in range(6):
            c.ellipse(-W * 0.15 + (k % 3) * W * 0.15, H * (0.4 + (k // 3) * 0.1), 0.5, 0.3, zone=1, shade=1.3, clip=cl)
    elif style in ("roll", "pretzel", "baguette", "croissant"):
        if style == "roll":
            body = ell(0, H * 0.45, W / 2, H * 0.45, 28)
            cl = shaded(c, body, 1, "bottom", SHADE, 0.35)
            line(c, [(-W * 0.3, H * 0.6), (W * 0.3, H * 0.62)], zone=1, clip=cl, shade=0.7, w=0.6)
            for k in range(6):
                c.ellipse(-W * 0.3 + k * W * 0.12, H * 0.8, 0.4, 0.25, zone=2)
        elif style == "baguette":
            body = rrect(x0, 0, x1, H, H * 0.48)
            cl = shaded(c, body, 1, "bottom", SHADE, 0.35)
            for k in range(4):
                line(c, [(x0 + W * (0.15 + k * 0.2), H * 0.45), (x0 + W * (0.25 + k * 0.2), H * 0.9)], zone=1, clip=cl, shade=0.72, w=0.6)
        elif style == "croissant":
            for k in range(5):
                a = math.pi * (k / 4)
                x = -math.cos(a) * W * 0.34
                seg = ell(x, H * 0.3 + math.sin(a) * H * 0.3, W * (0.12 + 0.06 * (2 - abs(k - 2))), H * (0.2 + 0.08 * (2 - abs(k - 2))), 20)
                shaded(c, seg, 1, "bottom", SHADE, 0.35)
        else:
            c.line(smooth([(-W * 0.4, H * 0.1), (-W * 0.45, H * 0.7), (-W * 0.1, H * 0.95), (W * 0.1, H * 0.95), (W * 0.45, H * 0.7),
                           (W * 0.4, H * 0.1)], closed=False), W * 0.16, zone=1)
            c.line([(-W * 0.4, H * 0.1), (W * 0.15, H * 0.6)], W * 0.14, zone=1, shade=0.95)
            c.line([(W * 0.4, H * 0.1), (-W * 0.15, H * 0.6)], W * 0.14, zone=1, shade=0.9)
            for k in range(8):
                c.ellipse(-W * 0.35 + k * W * 0.1, H * (0.5 + 0.3 * math.sin(k)), 0.5, 0.4, zone=2)
    elif style in ("milk", "juice", "water"):
        if style == "water":
            body = smooth([(-W * 0.4, 0, "s"), (W * 0.4, 0, "s"), (W * 0.4, H * 0.7), (W * 0.15, H * 0.85), (W * 0.15, H, "s"),
                           (-W * 0.15, H, "s"), (-W * 0.15, H * 0.85), (-W * 0.4, H * 0.7)])
            c.glass(body, zone=1, opacity=0.5)
            c.fill(rrect(-W * 0.4, H * 0.3, W * 0.4, H * 0.5, 0.3), zone=2, clip=c.mask(body))
            c.fill(rrect(-W * 0.17, H * 0.92, W * 0.17, H, 0.5), zone=3)
            c.line(body, INNER, zone=0, closed=True)
        else:
            c.fill([(x0, H * 0.8), (0, H * 0.95), (x1, H * 0.8)], zone=1, shade=0.95)
            c.fill(rrect(W * 0.1, H * 0.86, W * 0.3, H, 0.5), zone=3)
            body = rrect(x0, 0, x1, H * 0.82, 0.5)
            cl = shaded(c, body, 1, "right", SHADE, 0.25)
            if style == "milk":
                c.fill(smooth([(x0, H * 0.3), (-W * 0.2, H * 0.42), (W * 0.1, H * 0.3), (x1, H * 0.42), (x1, 0), (x0, 0)]), zone=2, clip=cl)
            else:
                c.fill(ell(0, H * 0.45, W * 0.3, W * 0.3, 20), zone=2, clip=cl)
                c.fill(ell(W * 0.1, H * 0.45 + W * 0.28, W * 0.12, W * 0.06, 12), zone=3, clip=cl)
    elif style in ("yogurt", "butter"):
        if style == "yogurt":
            body = trap(-W * 0.38, W * 0.38, 0, x0, x1, H * 0.9, 0.8)
            cl = shaded(c, body, 1, "right", SHADE, 0.25)
            c.fill(ell(0, H * 0.45, W * 0.25, H * 0.2, 20), zone=2, clip=cl)
            c.fill(rrect(x0 - 0.5, H * 0.88, x1 + 0.5, H, 0.5), zone=3, shade=1.2)
        else:
            body = rrect(x0, 0, x1, H, 0.6)
            cl = shaded(c, body, 1, "right", SHADE, 0.25)
            c.fill(rrect(x0, H * 0.3, x1, H * 0.7, 0.3), zone=2, clip=cl)
    elif style == "cereal":
        body = rrect(x0, 0, x1, H, 0.6)
        cl = shaded(c, body, 1, "right", SHADE, 0.15)
        bowl = smooth([(-W * 0.35, H * 0.45), (W * 0.35, H * 0.45), (W * 0.2, H * 0.2), (-W * 0.2, H * 0.2)])
        c.fill(bowl, zone=3, clip=cl)
        for k in range(7):
            c.fill(ell(-W * 0.25 + k * W * 0.08, H * (0.48 + 0.04 * (k % 2)), 1.2, 1.2, 10), zone=2, clip=cl)
        c.fill(rrect(x0 + 2, H * 0.7, x1 - 2, H * 0.9, 0.5), zone=2, shade=1.2, clip=cl)
    elif style in ("jam", "honey"):
        cl = _jar(c, W, H, label=style == "jam")
        if style == "honey":
            c.fill(ell(0, H * 0.4, W * 0.24, H * 0.18, 6), zone=2, clip=cl)
            c.line(ell(0, H * 0.4, W * 0.24, H * 0.18, 6), 0.3, zone=0, closed=True)
        else:
            c.fill(ell(W * 0.15, H * 0.4, W * 0.1, W * 0.1, 12), zone=1, shade=0.8, clip=cl)
    elif style in ("cookie", "chocolate", "candy", "donut", "lollipop"):
        if style == "cookie":
            for k, (dx, dy) in enumerate(((0, 0), (W * 0.05, H * 0.35), (-W * 0.04, H * 0.66))):
                ck = ell(dx, dy + H * 0.16, W * 0.48, H * 0.16, 28)
                shaded(c, ck, 1, "bottom", SHADE, 0.4)
                for j in range(4):
                    c.ellipse(dx - W * 0.3 + j * W * 0.2, dy + H * 0.2, 0.7, 0.5, zone=2)
        elif style == "chocolate":
            bar = rrect(x0, 0, x1, H, 0.5)
            c.fill(bar, zone=2)
            cl = c.mask(bar)
            for i in range(3):
                for j in range(2):
                    c.fill(rrect(x0 + 1 + i * (W - 2) / 3, 1 + j * (H - 2) / 2, x0 + (i + 1) * (W - 2) / 3, (j + 1) * (H - 2) / 2, 0.3),
                           zone=2, shade=1.1, clip=cl)
            c.fill([(x0, H * 0.45), (x1, H * 0.2), (x1, 0), (x0, 0)], zone=1)
            c.line(bar, INNER, zone=0, closed=True)
        elif style == "candy":
            for k, (dx, z) in enumerate(((-W * 0.25, 1), (W * 0.2, 2), (0, 3))):
                y = H * (0.3 if k < 2 else 0.7)
                c.fill([(dx - W * 0.3, y - H * 0.18), (dx - W * 0.14, y), (dx - W * 0.3, y + H * 0.18)], zone=z, shade=0.9)
                c.fill([(dx + W * 0.3, y - H * 0.18), (dx + W * 0.14, y), (dx + W * 0.3, y + H * 0.18)], zone=z, shade=0.9)
                shaded(c, ell(dx, y, W * 0.16, H * 0.2, 16), z, "bottom", SHADE, 0.3)
        elif style == "donut":
            body = ell(0, H * 0.45, W / 2, H * 0.45, 32)
            shaded(c, body, 1, "bottom", SHADE, 0.3)
            glaze = smooth([(x0 + 1, H * 0.55), (-W * 0.3, H * 0.4), (0, H * 0.48), (W * 0.3, H * 0.38), (x1 - 1, H * 0.55), (W * 0.3, H * 0.9),
                            (-W * 0.3, H * 0.9)])
            c.fill(glaze, zone=2)
            c.fill(ell(0, H * 0.62, W * 0.14, H * 0.08, 16), zone=0, alpha=0.8)
            for k in range(8):
                a = k * 0.8
                c.line([(math.cos(a) * W * 0.32, H * 0.62 + math.sin(a) * H * 0.2), (math.cos(a) * W * 0.32 + 1, H * 0.62 + math.sin(a) * H * 0.2 + 0.6)],
                       0.4, zone=3)
        else:
            c.line([(0, 0), (0, H * 0.55)], 0.8, zone=3, shade=1.6)
            disc = ell(0, H * 0.75, W / 2, H * 0.25, 32)
            shaded(c, disc, 1, "bottom", SHADE, 0.3)
            c.line(smooth([(0, H * 0.75), (W * 0.15, H * 0.8), (W * 0.05, H * 0.92), (-W * 0.2, H * 0.82), (-W * 0.1, H * 0.6),
                           (W * 0.3, H * 0.65)], closed=False), W * 0.08, zone=2)
    elif style == "burger":
        c.fill(rrect(x0 + 1, 0, x1 - 1, H * 0.22, H * 0.1), zone=1, shade=0.9)
        c.fill(rrect(x0, H * 0.2, x1, H * 0.38, H * 0.08), zone=1, shade=0.45)                         # Fleisch
        c.fill(smooth([(x0 - 1, H * 0.4), (-W * 0.2, H * 0.34), (0, H * 0.42), (W * 0.2, H * 0.34), (x1 + 1, H * 0.4), (x1, H * 0.46),
                       (x0, H * 0.46)]), zone=3)                                                            # Salat
        c.fill([(x0 + 2, H * 0.46), (x1 - 2, H * 0.46), (x1 - 4, H * 0.54), (x0 + 4, H * 0.54)], zone=2)    # Käse
        bun = smooth([(x0, H * 0.52, "s"), (x1, H * 0.52, "s"), (W * 0.4, H * 0.85), (0, H), (-W * 0.4, H * 0.85)])
        shaded(c, bun, 1, "bottom", SHADE, 0.3)
        for k in range(6):
            c.ellipse(-W * 0.3 + k * W * 0.12, H * (0.78 + 0.06 * (k % 2)), 0.5, 0.3, zone=2, shade=1.4)
    elif style == "fries":
        for k in range(7):
            x = -W * 0.3 + k * W * 0.1
            c.fill(rrect(x - 0.9, H * 0.5, x + 0.9, H * (0.85 + 0.12 * ((k * 3) % 3) / 2), 0.4), zone=2, shade=1.0 + (k % 2) * 0.1)
        box = trap(-W * 0.34, W * 0.34, 0, x0, x1, H * 0.65, 0.8)
        shaded(c, box, 1, "right", SHADE, 0.25)
        c.fill(ell(0, H * 0.3, W * 0.14, H * 0.1, 16), zone=3, shade=1.3)
    elif style == "hotdog":
        c.fill(rrect(x0 + 2, 0, x1 - 2, H * 0.6, H * 0.3), zone=1)
        c.fill(rrect(x0, H * 0.35, x1, H * 0.75, H * 0.2), zone=3, shade=0.6)
        c.line(smooth([(x0 + 4, H * 0.62), (-W * 0.2, H * 0.72), (0, H * 0.62), (W * 0.2, H * 0.72), (x1 - 4, H * 0.62)], closed=False),
               0.6, zone=2)
        bun = rrect(x0 + 2, 0, x1 - 2, H * 0.5, H * 0.25)
        shaded(c, bun, 1, "bottom", SHADE, 0.35)
    elif style == "sandwich":
        tri = [(x0, 0), (x1, 0), (0, H)]
        c.fill([(x0 + 1, H * 0.1), (x1 - 1, H * 0.1), (0, H * 0.95)], zone=3)
        c.fill([(x0, 0), (x1, 0), (W * 0.45, H * 0.08), (-W * 0.45, H * 0.08)], zone=2)
        shaded(c, [(x0 + 2, H * 0.14), (x1 - 2, H * 0.14), (0, H)], 1, "bottom", SHADE, 0.3)
        c.line(tri + [tri[0]], INNER, zone=0)
    elif style == "salad":
        bowl = smooth([(x0, H * 0.55, "s"), (x1, H * 0.55, "s"), (W * 0.3, 0), (-W * 0.3, 0)])
        for k in range(7):
            x = -W * 0.36 + k * W * 0.12
            c.fill(ell(x, H * (0.62 + 0.1 * (k % 2)), W * 0.1, H * 0.16, 16), zone=3, shade=1.0 + (k % 3) * 0.08)
        for x in (-W * 0.15, W * 0.2):
            c.fill(ell(x, H * 0.75, W * 0.06, W * 0.06, 12), zone=2)
        shaded(c, bowl, 1, "bottom", SHADE, 0.35)
