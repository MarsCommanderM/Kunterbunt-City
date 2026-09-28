"""
Tierbedarf (P08-T07): Napf (leer/voll), Körbchen, Kissen, Kauknochen, Quietsch-Ball, Futtersack, Leine.
Die Haustier-KI (PetBrain) sucht diese Dinge: Hunger → Napf, Müdigkeit → Körbchen, Spieltrieb → Ball/Knochen.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Futter/Details.
"""
from __future__ import annotations

from .kit import INNER, SHADE, SOFT, Item, ell, line, rrect, shaded, smooth, trap


def pet_gear(it: Item, style: str = "bowl", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "bowl":                                             # Napf: breiter Rand, innen Futter wenn voll
        body = trap(x0 + W * 0.08, x1 - W * 0.08, 0, x0, x1, H * 0.85, 1.2)
        shaded(c, body, 1, "right", SHADE, 0.3)
        c.fill(ell(0, H * 0.85, W / 2, H * 0.2, 36), zone=1, shade=1.15)
        inner = ell(0, H * 0.85, W * 0.42, H * 0.14, 36)
        c.fill(inner, zone=1, shade=0.55)
        if state == "full":                                           # Futterberg ragt über den Rand
            c.fill(smooth([(x0 + W * 0.1, H * 0.84, "s"), (x0 + W * 0.25, H * 1.0), (0, H * 1.08), (x1 - W * 0.25, H * 1.0),
                           (x1 - W * 0.1, H * 0.84, "s")]), zone=3, shade=0.85)
            for k in range(11):
                x = x0 + W * 0.18 + (k % 6) * W * 0.13 + (k // 6) * W * 0.06
                y = H * 0.9 + (k // 6) * H * 0.1 + (0.04 if k % 2 else 0.0) * H
                c.fill(ell(x, y, W * 0.055, H * 0.09, 12), zone=3, shade=1.0 + 0.12 * (k % 3))
        c.fill(rrect(-W * 0.12, H * 0.25, W * 0.12, H * 0.5, 1.0), zone=2)          # Knochen-Schild
        c.line(body, INNER, zone=0, closed=True)
    elif style == "basket":                                         # Körbchen mit Kissen
        body = smooth([(x0, H * 0.7, "s"), (x0 + W * 0.04, 0, "s"), (x1 - W * 0.04, 0, "s"), (x1, H * 0.7, "s"),
                       (x1 - W * 0.06, H, "s"), (x1 - W * 0.16, H * 0.62), (x0 + W * 0.16, H * 0.62), (x0 + W * 0.06, H, "s")])
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        for k in range(1, 6):
            line(c, [(x0, k * H * 0.13), (x1, k * H * 0.13)], zone=1, clip=cl)
        c.fill(smooth([(x0 + W * 0.12, H * 0.34, "s"), (x1 - W * 0.12, H * 0.34, "s"), (x1 - W * 0.14, H * 0.66, "s"),
                       (0, H * 0.72), (x0 + W * 0.14, H * 0.66, "s")]), zone=2)
        c.fill(ell(0, H * 0.6, W * 0.3, H * 0.08, 24), zone=2, shade=1.15)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "cushion":                                        # rundes Hundebett mit dickem Rand
        body = rrect(x0, 0, x1, H, H * 0.48)
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(rrect(x0 + W * 0.1, H * 0.35, x1 - W * 0.1, H * 0.85, H * 0.25), zone=2)
        c.fill(rrect(x0 + W * 0.12, H * 0.62, x1 - W * 0.12, H * 0.85, H * 0.2), zone=2, shade=1.12)
        for k in range(4):                                          # Pfoten-Muster
            x = x0 + W * 0.26 + k * W * 0.16
            c.fill(ell(x, H * 0.52, W * 0.03, H * 0.08, 12), zone=1, shade=0.85)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "bone":
        for sx in (-1, 1):
            for sy in (0.3, 0.7):
                c.fill(ell(sx * W * 0.4, H * sy, W * 0.11, H * 0.3, 20), zone=1)
        c.fill(rrect(x0 + W * 0.12, H * 0.28, x1 - W * 0.12, H * 0.72, 1.2), zone=1)
        c.fill(rrect(x0 + W * 0.14, H * 0.3, x1 - W * 0.14, H * 0.42, 0.8), zone=1, shade=SOFT)
        c.line(rrect(x0 + W * 0.12, H * 0.28, x1 - W * 0.12, H * 0.72, 1.2), INNER, zone=0, closed=True)
    elif style == "ball":                                           # Quietsch-Ball mit Streifen
        b = ell(0, H / 2, W / 2, H / 2, 40)
        cl = shaded(c, b, 1, "right", SHADE, 0.35)
        c.fill(smooth([(x0, H * 0.45, "s"), (0, H * 0.62), (x1, H * 0.45, "s"), (x1, H * 0.58, "s"), (0, H * 0.75),
                       (x0, H * 0.58, "s")]), zone=2, clip=cl)
        c.fill(ell(-W * 0.18, H * 0.72, W * 0.1, H * 0.07, 16), zone=1, shade=1.5)
        c.line(b, INNER, zone=0, closed=True)
    elif style == "food_bag":                                       # Futtersack mit Pfote
        body = smooth([(x0 + W * 0.04, 0, "s"), (x1 - W * 0.04, 0, "s"), (x1, H * 0.85), (x1 - W * 0.06, H, "s"),
                       (x0 + W * 0.06, H, "s"), (x0, H * 0.85)])
        shaded(c, body, 1, "right", SHADE, 0.3)
        c.fill(rrect(x0, H * 0.86, x1, H, 0.8), zone=1, shade=0.8)
        c.fill(ell(0, H * 0.45, W * 0.28, H * 0.2, 28), zone=2)
        c.fill(ell(0, H * 0.4, W * 0.1, H * 0.07, 16), zone=3)
        for k in (-1, 0, 1):
            c.fill(ell(k * W * 0.11, H * 0.52 + (0.02 if k else 0.04) * H, W * 0.045, H * 0.04, 12), zone=3)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "leash":                                          # aufgerollte Leine: Schlaufe, Windungen, Karabiner
        c.line(ell(0, H * 0.78, W * 0.2, H * 0.2, 28), 2.2, zone=1, shade=0.9, closed=True)
        for k in range(4):
            c.line(ell(0, H * 0.36, W * (0.46 - k * 0.04), H * (0.3 - k * 0.03), 36), 1.8, zone=1,
                   shade=1.0 - 0.08 * k, closed=True)
        c.fill(rrect(W * 0.3, 0, W * 0.44, H * 0.14, 0.6), zone=3)
        c.line(ell(W * 0.37, H * 0.14, W * 0.07, H * 0.07, 16), 1.0, zone=3, shade=0.7, closed=True)
