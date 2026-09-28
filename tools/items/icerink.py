"""
Eishalle (P10f, Welt-Doku §9): Eisfläche (glänzend / zerkratzt), Eismaschine, Bande, Eishockey-Tor, Lauflern-Pinguin,
Discokugel, Verleih-Theke mit Schlittschuh-Regal, Imbiss-Dinge (Kakao, Brezel, Pommes).
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Weiß.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, cushion, ell, rrect, shaded, smooth, trap


def icerink(it: Item, style: str = "surface", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "surface":                                          # Eisfläche (flach): shiny = frisch, scratched = Spuren
        ice = rrect(x0, 0, x1, H, 6)
        c.fill(ice, zone=1)
        cl = c.mask(ice)
        c.fill(rrect(x0, H * 0.55, x1, H, 4), zone=1, shade=1.06, clip=cl)
        if state == "scratched":
            for k in range(int(W / 70)):
                cx = x0 + 40 + k * 70
                c.line(smooth([(cx - 50, H * 0.3 + (k % 3) * 8), (cx, H * 0.6 - (k % 2) * 10), (cx + 50, H * 0.4)], closed=False),
                       0.6, zone=3, shade=0.8, clip=cl)
        else:
            for k in range(int(W / 160)):
                cx = x0 + 80 + k * 160
                c.fill(ell(cx, H * 0.6, 50, 4, 24), zone=3, shade=1.3, clip=cl, alpha=0.7)
        c.line(rrect(x0 + 20, H * 0.2, x1 - 20, H * 0.85, 4), 0.8, zone=2, shade=1.0, closed=True, clip=cl)
        c.line([(0, H * 0.2), (0, H * 0.85)], 1.2, zone=2)
    elif style == "resurfacer":                                     # Eismaschine: Kasten, Fahrersitz, Räder
        body = smooth([(x0 + 6, H * 0.12, "s"), (x1 - 6, H * 0.12, "s"), (x1, H * 0.6), (x1 - W * 0.3, H * 0.7),
                       (x0 + W * 0.05, H * 0.7), (x0, H * 0.4)])
        shaded(c, body, 1, "right", SHADE, 0.2)
        for x in (x0 + W * 0.2, x1 - W * 0.2):
            c.fill(ell(x, H * 0.14, H * 0.14, H * 0.14, 20), zone=0)
            c.fill(ell(x, H * 0.14, H * 0.06, H * 0.06, 12), zone=3)
        c.fill(rrect(x0 - 8, H * 0.05, x0 + 10, H * 0.3, 2), zone=3, shade=0.8)
        cushion(c, x1 - W * 0.3, H * 0.62, x1 - W * 0.1, H * 0.7, zone=2)
        c.fill(rrect(x1 - W * 0.32, H * 0.7, x1 - W * 0.28, H * 0.9, 1), zone=2)
        c.line([(x1 - W * 0.12, H * 0.6), (x1 - W * 0.14, H * 0.82)], 1.6, zone=3)
        c.fill(ell(x1 - W * 0.14, H * 0.84, 8, 3, 12), zone=0)
        c.fill(rrect(x0 + W * 0.12, H * 0.35, x0 + W * 0.5, H * 0.55, 3), zone=2, shade=1.1)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "boards":                                         # Bande mit Plexiglas
        c.fill(rrect(x0, 0, x1, H * 0.5, 2), zone=1)
        c.fill(rrect(x0, H * 0.46, x1, H * 0.52, 1), zone=2)
        c.glass(rrect(x0, H * 0.52, x1, H, 1), zone=3, opacity=0.25, shade=1.2)
        for k in range(int(W / 120) + 1):
            c.fill(rrect(x0 + k * (W - 4) / max(1, int(W / 120)), H * 0.5, x0 + 4 + k * (W - 4) / max(1, int(W / 120)), H, 0.5), zone=3)
        c.line(rrect(x0, 0, x1, H * 0.5, 2), INNER, zone=0, closed=True)
    elif style == "hockey_goal":                                    # Eishockey-Tor (Rahmen rot, Netz)
        c.fill(trap(x0 + 14, x1 - 14, 0, x0 + 4, x1 - 4, H * 0.9, 0.5), zone=3, shade=0.9, alpha=0.3)
        for k in range(1, int(W / 10)):
            c.line([(x0 + k * 10, 0), (x0 + k * 10, H * 0.9)], 0.3, zone=0, shade=0.7)
        for k in range(1, int(H / 10)):
            c.line([(x0 + 4, k * 10), (x1 - 4, k * 10)], 0.3, zone=0, shade=0.7)
        for x in (x0 + 3, x1 - 3):
            c.fill(rrect(x - 3, 0, x + 3, H, 1.5), zone=1)
        c.fill(rrect(x0, H - 6, x1, H, 2), zone=1)
    elif style == "penguin":                                        # Lauflern-Pinguin mit Griff
        c.fill(rrect(x0 + 4, 0, x1 - 4, 6, 3), zone=3, shade=0.8)
        body = ell(0, H * 0.4, W * 0.36, H * 0.38, 32)
        c.fill(body, zone=1)
        c.fill(ell(0, H * 0.36, W * 0.24, H * 0.3, 24), zone=3)
        c.fill(ell(0, H * 0.78, W * 0.24, H * 0.16, 24), zone=1)
        for dx in (-0.08, 0.08):
            c.fill(ell(W * dx, H * 0.8, 2.6, 3.2, 10), zone=3)
            c.fill(ell(W * dx, H * 0.8, 1.3, 1.8, 8), zone=0)
        c.fill([(-5, H * 0.72), (5, H * 0.72), (0, H * 0.66)], zone=2)
        c.line(smooth([(-W * 0.4, H * 0.6), (-W * 0.5, H), (W * 0.5, H), (W * 0.4, H * 0.6)], closed=False), 3.0, zone=2)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "disco_ball":                                     # Discokugel an der Decke (on = glitzert)
        c.line([(0, H * 0.6), (0, H)], 0.6, zone=3)
        b = ell(0, H * 0.32, W * 0.5, W * 0.5, 40)
        c.fill(b, zone=3, shade=0.9)
        cl = c.mask(b)
        for i in range(8):
            for j in range(8):
                cx = x0 + (i + 0.5) * W / 8
                cy = H * 0.32 - W / 2 + (j + 0.5) * W / 8
                on = state == "on" and (i + j) % 3 == 0
                c.fill(rrect(cx - W / 20, cy - W / 20, cx + W / 20, cy + W / 20, 0.3), zone=1 if on else 3,
                       shade=1.5 if on else 0.8 + ((i * 7 + j * 3) % 5) * 0.08, clip=cl)
        c.line(b, INNER, zone=0, closed=True)
    elif style == "rental":                                         # Verleih-Theke mit Schlittschuh-Fächern
        c.fill(rrect(x0 + 10, H * 0.45, x1 - 10, H, 1), zone=3, shade=0.8)
        for i in range(5):
            for j in range(2):
                cx = x0 + 20 + (i + 0.5) * (W - 40) / 5
                cy = H * (0.55 + j * 0.22)
                c.fill(rrect(cx - 12, cy, cx + 8, cy + 14, 3), zone=2 if (i + j) % 2 else 1)
                c.line([(cx - 12, cy), (cx + 10, cy)], 0.8, zone=3, shade=1.3)
        counter = rrect(x0, 0, x1, H * 0.42, 1.2)
        shaded(c, counter, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0 - 3, H * 0.4, x1 + 3, H * 0.45, 1), zone=2)
        c.line(counter, INNER, zone=0, closed=True)
    elif style == "cocoa":                                          # Becher Kakao mit Sahne
        cup = trap(-W * 0.35, W * 0.35, 0, -W * 0.45, W * 0.45, H * 0.75, 0.6)
        shaded(c, cup, 1, "right", SOFT, 0.3)
        c.fill(smooth([(-W * 0.45, H * 0.75), (-W * 0.3, H * 0.95), (0, H), (W * 0.3, H * 0.95), (W * 0.45, H * 0.75)]), zone=3)
        c.fill(rrect(-W * 0.45, H * 0.3, W * 0.45, H * 0.45, 0.3), zone=2)
        c.line(cup, INNER, zone=0, closed=True)
    elif style == "pretzel":                                        # Brezel
        for pts in ([(-W * 0.45, H * 0.3), (-W * 0.3, H * 0.95), (0, H * 0.55), (W * 0.3, H * 0.95), (W * 0.45, H * 0.3),
                     (0, H * 0.05), (-W * 0.45, H * 0.3)],):
            c.line(smooth(pts, closed=False), W * 0.16, zone=1)
            c.line(smooth(pts, closed=False), W * 0.07, zone=1, shade=1.12)
        for k in range(6):
            c.fill(ell(-W * 0.3 + k * W * 0.12, H * (0.5 + (k % 2) * 0.25), 0.8, 0.8, 6), zone=3)
    elif style == "fries":                                          # Pommes in der Tüte
        for k in range(7):
            x = -W * 0.3 + k * W * 0.1
            c.fill(rrect(x - W * 0.04, H * 0.4, x + W * 0.04, H * (0.85 + (k % 3) * 0.05), 0.4), zone=2, shade=1.0 + (k % 2) * 0.08)
        bag = trap(-W * 0.3, W * 0.3, 0, -W * 0.45, W * 0.45, H * 0.6, 0.6)
        shaded(c, bag, 1, "right", SOFT, 0.25)
        c.line(bag, INNER, zone=0, closed=True)
    else:
        raise ValueError(style)
