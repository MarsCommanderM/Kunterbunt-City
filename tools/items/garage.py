"""
Werkstatt (P10h, Welt-Doku §11): Hebebühne (up = Arme oben), Zapfsäule (fuel = Schlauch am Auto, Anzeige leuchtet),
Waschanlage (on = Bürsten + Schaum), Lackierkabine, Sprühpistole, Fahrrad-Montageständer, Schrotthaufen (found =
Schatz blitzt), Schrottauto, goldene Radkappe (Schatz), Ölfass.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe/hell · 3 = Metall/Akzent.
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, ell, rrect, shaded, smooth, trap


def garage(it: Item, style: str = "car_lift", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    rng = random.Random(int(W * 3 + H))
    if style == "car_lift":                                         # 2-Säulen-Hebebühne; up = Tragarme oben
        for x in (x0 + 14, x1 - 14):
            col = rrect(x - 12, 0, x + 12, H, 3)
            shaded(c, col, 1, "right", SHADE, 0.25)
            c.line(col, INNER, zone=0, closed=True)
        arm_y = H * (0.62 if state == "up" else 0.06)
        for x in (x0 + 26, x1 - 26):
            d = 1 if x < 0 else -1
            c.fill(rrect(min(x, x + d * W * 0.3), arm_y, max(x, x + d * W * 0.3), arm_y + 8, 2), zone=3)
            c.fill(rrect(x + d * W * 0.3 - 10, arm_y + 8, x + d * W * 0.3 + 10, arm_y + 14, 2), zone=2)
        c.fill(rrect(x0, H - 10, x1, H, 3), zone=1, shade=0.9)
        c.fill(rrect(x0 + 6, 0, x1 - 6, 4, 1), zone=2, shade=0.8)
    elif style == "gas_pump":                                       # Zapfsäule mit Anzeige und Schlauch
        body = rrect(x0 + 6, 0, x1 - 6, H * 0.85, 4)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 + 4, H * 0.85, x1 - 4, H, 4), zone=2)
        scr = rrect(x0 + 14, H * 0.58, x1 - 14, H * 0.76, 2)
        c.fill(scr, zone=3, shade=1.5 if state == "fuel" else 0.35)
        for k in range(3):
            c.fill(ell(x0 + W * (0.3 + k * 0.2), H * 0.67, 3, 5, 10), zone=1, shade=0.6 if state == "fuel" else 1.0)
        c.fill(ell(0, H * 0.92, W * 0.14, H * 0.03, 16), zone=1)
        hose_end = (x1 + W * 0.5, H * 0.45) if state == "fuel" else (x1 - 4, H * 0.3)
        c.line(smooth([(x1 - 8, H * 0.5), (x1 + 6, H * 0.35), hose_end], closed=False), 3.0, zone=0, shade=0.6)
        c.fill(rrect(hose_end[0] - 6, hose_end[1] - 4, hose_end[0] + 8, hose_end[1] + 6, 2), zone=2, shade=0.8)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "wash_tunnel":                                    # Waschanlage: Portal, Bürsten (on = drehen + Schaum)
        for x in (x0 + 10, x1 - 10):
            c.fill(rrect(x - 10, 0, x + 10, H * 0.9, 3), zone=1)
        c.fill(rrect(x0, H * 0.85, x1, H, 4), zone=1, shade=0.9)
        c.fill(rrect(x0 + W * 0.3, H * 0.88, x1 - W * 0.3, H * 0.97, 3), zone=2)
        for k, x in enumerate((x0 + W * 0.28, x1 - W * 0.28)):
            brush = rrect(x - 26, 10, x + 26, H * 0.8, 20)
            c.fill(brush, zone=2 if k else 3, shade=1.0)
            for j in range(10):
                y = 16 + j * (H * 0.8 - 20) / 10
                off = (6 if state == "on" and j % 2 else 0)
                c.line([(x - 26 + off, y), (x + 26 - off, y + 4)], 1.2, zone=2 if k else 3, shade=0.8)
        if state == "on":
            for _ in range(28):
                c.fill(ell(rng.uniform(x0 + 30, x1 - 30), rng.uniform(20, H * 0.75), rng.uniform(5, 10), rng.uniform(4, 8), 12), zone=2,
                       shade=1.3, alpha=0.85)
    elif style == "paint_booth":                                    # Lackierkabine: Glaswand, Lüfter, Lampen
        frame = rrect(x0, 0, x1, H, 3)
        c.fill(frame, zone=1)
        c.fill(rrect(x0 + 10, 8, x1 - 10, H - 30, 2), zone=3, shade=0.9)
        for k in range(4):
            c.line([(x0 + W * (0.1 + k * 0.25), H * 0.9), (x0 + W * (0.2 + k * 0.25), H * 0.2)], 1.6, zone=3, shade=1.3)
        for k in range(3):
            c.fill(ell(x0 + W * (0.25 + k * 0.25), H - 16, 16, 8, 16), zone=2, shade=1.4)
        c.line(frame, INNER, zone=0, closed=True)
    elif style == "spray_gun":                                      # Sprühpistole mit Farbbecher (Zone 2 = Farbe)
        c.fill(rrect(-W * 0.1, 0, W * 0.1, H * 0.5, 1), zone=3)
        c.fill(rrect(-W * 0.4, H * 0.45, W * 0.45, H * 0.7, 2), zone=1)
        c.fill(rrect(W * 0.4, H * 0.52, W * 0.5, H * 0.62, 0.5), zone=3)
        c.fill(trap(-W * 0.3, W * 0.1, H * 0.7, -W * 0.34, W * 0.14, H, 1), zone=2)
        c.line(rrect(-W * 0.4, H * 0.45, W * 0.45, H * 0.7, 2), INNER, zone=0, closed=True)
    elif style == "bike_stand":                                     # Montageständer für Fahrräder
        c.fill(trap(-W * 0.45, W * 0.45, 0, -W * 0.1, W * 0.1, 8, 1), zone=3)
        c.fill(rrect(-4, 0, 4, H * 0.8, 1), zone=1)
        c.line([(0, H * 0.8), (W * 0.3, H * 0.95)], 3.0, zone=1)
        c.fill(rrect(W * 0.22, H * 0.9, W * 0.42, H, 2), zone=2)
    elif style == "scrap_pile":                                     # Schrotthaufen (found = etwas Goldenes blitzt)
        pile = smooth([(x0, 0, "s"), (x1, 0, "s"), (x1 - W * 0.1, H * 0.4), (W * 0.1, H * 0.95), (-W * 0.15, H), (x0 + W * 0.15, H * 0.5)])
        shaded(c, pile, 1, "right", SHADE, 0.3)
        cl = c.mask(pile)
        for _ in range(16):
            x, y = rng.uniform(x0 + 20, x1 - 20), rng.uniform(10, H * 0.9)
            k = rng.random()
            if k < 0.35:
                c.fill(ell(x, y, 14, 14, 16), zone=0, shade=0.7, clip=cl)
                c.fill(ell(x, y, 6, 6, 12), zone=3, clip=cl)
            elif k < 0.7:
                c.fill(rrect(x - 18, y - 6, x + 18, y + 6, 2), zone=2, shade=0.8 + rng.random() * 0.3, clip=cl)
            else:
                c.line([(x - 20, y), (x + 20, y + rng.uniform(-10, 10))], 2.0, zone=3, shade=0.8, clip=cl)
        if state == "found":
            c.fill(ell(W * 0.15, H * 0.55, 16, 16, 20), zone=2, shade=1.6)
            for a in range(8):
                ang = a * math.pi / 4
                c.line([(W * 0.15 + math.cos(ang) * 20, H * 0.55 + math.sin(ang) * 20),
                        (W * 0.15 + math.cos(ang) * 30, H * 0.55 + math.sin(ang) * 30)], 1.4, zone=2, shade=1.6)
        c.line(pile, INNER, zone=0, closed=True)
    elif style == "scrap_car":                                      # rostiges Schrottauto ohne Räder (lustig, nicht traurig)
        body = smooth([(x0, H * 0.15, "s"), (x1, H * 0.15, "s"), (x1, H * 0.5), (x1 - W * 0.25, H * 0.55), (x1 - W * 0.35, H * 0.95),
                       (x0 + W * 0.3, H * 0.95), (x0 + W * 0.18, H * 0.55), (x0, H * 0.5)])
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        cl = c.mask(body)
        for _ in range(10):
            c.fill(ell(rng.uniform(x0, x1), rng.uniform(H * 0.2, H * 0.9), rng.uniform(6, 16), rng.uniform(4, 10), 12), zone=3, clip=cl)
        c.fill(rrect(x0 + W * 0.32, H * 0.6, x1 - W * 0.4, H * 0.88, 3), zone=2, shade=0.7)
        for x in (x0 + W * 0.2, x1 - W * 0.2):
            c.fill(rrect(x - 20, 0, x + 20, H * 0.15, 3), zone=0, shade=0.8)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "hubcap":                                         # goldene Radkappe (Schatz)
        cap = ell(0, H / 2, W / 2, H / 2, 32)
        shaded(c, cap, 1, "right", SOFT, 0.3)
        for a in range(5):
            ang = a * 2 * math.pi / 5
            c.line([(0, H / 2), (math.cos(ang) * W * 0.4, H / 2 + math.sin(ang) * H * 0.4)], 1.0, zone=2)
        c.fill(ell(-W * 0.15, H * 0.65, W * 0.1, H * 0.06, 12), zone=2, shade=1.4, alpha=0.8)
        c.line(cap, INNER, zone=0, closed=True)
    elif style == "oil_drum":                                       # Ölfass
        d = rrect(x0, 0, x1, H, 3)
        shaded(c, d, 1, "right", SHADE, 0.25)
        for fy in (0.3, 0.7):
            c.fill(rrect(x0, H * fy - 2, x1, H * fy + 2, 1), zone=1, shade=0.8)
        c.fill(ell(0, H * 0.5, W * 0.18, H * 0.1, 16), zone=2)
        c.line(d, INNER, zone=0, closed=True)
    else:
        raise ValueError(style)
