"""
Keller & Haushalt (P07-Inventar): Schwerlastregal, Weinregal, Weinfass, Weinflasche, Getränkekiste, Aufbewahrungsbox,
Einmachgläser, Kartoffelsack, Heizkessel, Taschenlampe, Eimer, Kehrblech, Pinnwand, Kalender.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Holz/Details.
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, ell, knob, line, rrect, shaded, smooth, trap


def _bottle(c, x: float, y: float, h: float, zone: int = 2, shade: float = 1.0, lying: bool = False):
    if lying:                                                       # liegend im Weinregal: nur der Boden ist zu sehen
        c.fill(ell(x, y, h * 0.14, h * 0.14, 16), zone=zone, shade=shade * 0.7)
        c.fill(ell(x, y, h * 0.07, h * 0.07, 12), zone=zone, shade=shade * 1.2)
        return
    b = smooth([(x - h * 0.12, y, "s"), (x + h * 0.12, y, "s"), (x + h * 0.12, y + h * 0.6), (x + h * 0.04, y + h * 0.78),
                (x + h * 0.04, y + h, "s"), (x - h * 0.04, y + h, "s"), (x - h * 0.04, y + h * 0.78), (x - h * 0.12, y + h * 0.6)])
    shaded(c, b, zone, "right", SHADE * shade, 0.3)
    c.fill(rrect(x - h * 0.1, y + h * 0.25, x + h * 0.1, y + h * 0.45, 0.4), zone=3, shade=1.4)


def cellar(it: Item, style: str = "heavy_shelf", state: str = "", seed: int = 2):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    rng = random.Random(seed)
    if style == "heavy_shelf":                                      # Stecksystem aus Metall mit Holzböden + Kisten
        for x in (x0 + 2, x1 - 2):
            c.fill(rrect(x - 2, 0, x + 2, H, 0.4), zone=3)
            for k in range(int(H / 6)):
                c.fill(rrect(x - 0.8, 3 + k * 6, x + 0.8, 4.2 + k * 6, 0.2), zone=0, alpha=0.6)
        n = 4
        for k in range(n):
            y = 8 + k * (H - 10) / (n - 1) if k else 8
            c.fill(rrect(x0 + 1, y - 3, x1 - 1, y, 0.4), zone=1)
            c.line(rrect(x0 + 1, y - 3, x1 - 1, y, 0.4), INNER, zone=0, closed=True)
            if k < n - 1:
                gap = (H - 10) / (n - 1)
                xx = x0 + 6
                while xx < x1 - 16:
                    bw = rng.choice([22, 28, 34])
                    bh = rng.uniform(0.45, 0.8) * gap
                    if xx + bw > x1 - 5:
                        break
                    box = rrect(xx, y, xx + bw, y + bh, 1)
                    shaded(c, box, 2, "right", SHADE, 0.2)
                    c.fill(rrect(xx, y + bh - 3, xx + bw, y + bh, 1), zone=2, shade=1.12)
                    xx += bw + 3
    elif style == "wine_rack":
        body = rrect(x0, 0, x1, H, 1)
        c.fill(body, zone=1, shade=0.6)
        cl = c.mask(body)
        cols, rows = max(2, int(W / 12)), max(2, int(H / 12))
        for i in range(cols):
            for j in range(rows):
                x = x0 + (i + 0.5) * W / cols
                y = (j + 0.5) * H / rows
                c.fill(ell(x, y, W / cols * 0.42, H / rows * 0.42, 20), zone=1, shade=0.4, clip=cl)
                if rng.random() < 0.75:
                    _bottle(c, x, y, min(W / cols, H / rows) * 2.3, zone=2, shade=rng.choice([0.9, 1.0, 1.1]), lying=True)
        for i in range(cols + 1):
            c.line([(x0 + i * W / cols, 0), (x0 + i * W / cols, H)], 1.4, zone=1)
        for j in range(rows + 1):
            c.line([(x0, j * H / rows), (x1, j * H / rows)], 1.4, zone=1)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "barrel":                                         # Weinfass liegend auf Böcken
        for sx in (-1, 1):
            c.fill(trap(sx * W * 0.3 - 6, sx * W * 0.3 + 6, 0, sx * W * 0.3 - 3, sx * W * 0.3 + 3, H * 0.2, 0.6), zone=3, shade=0.8)
        body = smooth([(x0 + 4, H * 0.1, "s"), (x1 - 4, H * 0.1, "s"), (x1, H * 0.55), (x1 - 4, H, "s"), (x0 + 4, H, "s"), (x0, H * 0.55)])
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        for k in range(1, 7):
            line(c, [(x0, H * 0.1 + k * H * 0.9 / 7), (x1, H * 0.1 + k * H * 0.9 / 7)], zone=1, clip=cl)
        for x in (x0 + W * 0.15, x1 - W * 0.15):
            c.fill(rrect(x - 2, H * 0.08, x + 2, H * 1.02, 0.6), zone=3, clip=cl)
        c.fill(rrect(-2, H * 0.3, 2, H * 0.4, 0.5), zone=2)
        c.fill(rrect(-1, H * 0.2, 1, H * 0.32, 0.3), zone=2, shade=0.8)
    elif style == "wine":
        _bottle(c, 0, 0, H, zone=1)
        c.fill(rrect(-W * 0.14, H * 0.9, W * 0.14, H, 0.4), zone=2)
    elif style == "crate":                                          # Getränkekiste mit Flaschen
        for k in range(4):
            _bottle(c, x0 + W * (k + 0.5) / 4, H * 0.3, H * 1.1, zone=2, shade=1.0 - (k % 2) * 0.1)
        body = rrect(x0, 0, x1, H * 0.62, 1.2)
        cl = shaded(c, body, 1, "right", SHADE, 0.15)
        c.fill(rrect(-W * 0.2, H * 0.44, W * 0.2, H * 0.54, 1), zone=0, alpha=0.8, clip=cl)
        for k in range(1, 4):
            line(c, [(x0 + k * W / 4, 0), (x0 + k * W / 4, H * 0.35)], zone=1, clip=cl)
    elif style == "box":                                            # Aufbewahrungsbox mit Deckel (Kunststoff/Karton)
        body = trap(x0 + 2, x1 - 2, 0, x0, x1, H * 0.85, 1.2)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 - 1, H * 0.82, x1 + 1, H, 1.2), zone=2)
        c.line(rrect(x0 - 1, H * 0.82, x1 + 1, H, 1.2), INNER, zone=0, closed=True)
        c.fill(rrect(-W * 0.18, H * 0.45, W * 0.18, H * 0.62, 0.6), zone=3, shade=1.3, clip=cl)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.42 - 2, H * 0.55, sx * W * 0.42 + 2, H * 0.62, 0.5), zone=0, alpha=0.6)
    elif style == "jars":                                           # drei Einmachgläser
        for k, (x, h, z) in enumerate(((-W * 0.3, H * 0.8, 1), (0, H, 2), (W * 0.3, H * 0.7, 1))):
            jar = rrect(x - W * 0.14, 0, x + W * 0.14, h * 0.82, 1.2)
            c.glass(jar, zone=3, opacity=0.4)
            c.fill(rrect(x - W * 0.12, 0.5, x + W * 0.12, h * 0.62, 1), zone=z, shade=1.0 - k * 0.05)
            for j in range(3):
                c.ellipse(x - W * 0.06 + j * W * 0.06, h * (0.2 + 0.15 * (j % 2)), W * 0.03, W * 0.03, zone=z, shade=0.7)
            c.fill(rrect(x - W * 0.15, h * 0.82, x + W * 0.15, h, 1), zone=2 if z == 1 else 1, shade=1.1)
            c.fill(rrect(x - W * 0.1, h * 0.3, x + W * 0.1, h * 0.45, 0.4), zone=3, shade=1.6)
            c.line(jar, INNER, zone=0, closed=True)
    elif style == "sack":                                           # Kartoffelsack
        for k in range(3):
            c.fill(ell(-W * 0.2 + k * W * 0.2, H * 0.9, W * 0.12, H * 0.08, 16), zone=2)
            c.line(ell(-W * 0.2 + k * W * 0.2, H * 0.9, W * 0.12, H * 0.08, 16), INNER, zone=0, closed=True)
        body = smooth([(x0 + 3, 0, "s"), (x1 - 3, 0, "s"), (x1, H * 0.5), (W * 0.36, H * 0.9), (-W * 0.36, H * 0.9), (x0, H * 0.5)])
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        for k in range(1, 7):
            line(c, [(x0, k * H / 7), (x1, k * H / 7 + 1)], zone=1, clip=cl, shade=0.85)
        c.fill(rrect(-W * 0.25, H * 0.35, W * 0.25, H * 0.55, 0.6), zone=3, shade=1.4, clip=cl)
    elif style == "boiler":                                         # Heizkessel mit Rohren und Anzeige
        for k, x in enumerate((-W * 0.25, -W * 0.05, W * 0.15)):
            c.line([(x, H * 0.9), (x, H + 30)], 3.0, zone=3, shade=0.9 + k * 0.05)
        body = rrect(x0, 0, x1, H * 0.92, 3)
        cl = shaded(c, body, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0 + 4, H * 0.6, x1 - 4, H * 0.85, 1.5), zone=2, clip=cl)
        c.fill(ell(-W * 0.15, H * 0.72, W * 0.1, W * 0.1, 20), zone=1, shade=1.3)
        c.line([(-W * 0.15, H * 0.72), (-W * 0.1, H * 0.78)], 0.6, zone=0)
        for k in range(3):
            knob(c, W * 0.05 + k * W * 0.1, H * 0.72, 1.4, zone=3)
        if state == "on":
            c.fill(ell(0, H * 0.3, W * 0.14, W * 0.1, 20), zone=0, alpha=0.85)
            c.fill(smooth([(-W * 0.08, H * 0.26), (0, H * 0.36), (W * 0.08, H * 0.26)]), zone=2, shade=1.3)
    elif style == "flashlight":
        body = rrect(x0, H * 0.2, W * 0.2, H * 0.8, H * 0.25)
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(smooth([(W * 0.2, H * 0.15), (x1, 0), (x1, H), (W * 0.2, H * 0.85)]), zone=1, shade=1.05)
        c.fill(rrect(x1 - 1.5, H * 0.05, x1, H * 0.95, 0.4), zone=2, shade=1.3)
        c.fill(rrect(-W * 0.1, H * 0.75, 0, H * 0.88, 0.4), zone=3)
        if state == "on":
            c.glass([(x1, 0), (x1 + W * 1.2, -H * 0.8), (x1 + W * 1.2, H * 1.8), (x1, H)], zone=2, opacity=0.22)
    elif style == "bucket":
        c.line(smooth([(x0 + 2, H * 0.9), (0, H * 1.25), (x1 - 2, H * 0.9)], closed=False), 0.6, zone=3)
        body = trap(-W * 0.36, W * 0.36, 0, x0, x1, H * 0.92, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(rrect(x0 - 0.5, H * 0.86, x1 + 0.5, H * 0.94, 0.5), zone=1, shade=1.08)
        line(c, [(x0, H * 0.3), (x1, H * 0.3)], zone=1, clip=cl)
    elif style == "dustpan":
        c.fill(rrect(W * 0.2, H * 0.1, x1, H * 0.3, 1), zone=1)
        pan = smooth([(x0, 0, "s"), (W * 0.22, 0, "s"), (W * 0.22, H * 0.4), (x0 + 2, H * 0.05)])
        shaded(c, pan, 1, "bottom", SHADE, 0.3)
        c.line([(-W * 0.1, H * 0.2), (-W * 0.3, H)], 1.4, zone=2)
        c.fill(rrect(-W * 0.45, H * 0.85, -W * 0.15, H, 1), zone=2, shade=0.9)
        for k in range(8):
            c.line([(-W * 0.44 + k * W * 0.04, H * 0.86), (-W * 0.45 + k * W * 0.04, H * 0.7)], 0.3, zone=3)
    elif style == "pinboard":
        board = rrect(x0, 0, x1, H, 1.5)
        c.fill(board, zone=3)
        c.fill(rrect(x0 + 3, 3, x1 - 3, H - 3, 0.6), zone=3, shade=1.25)
        for k in range(5):
            x, y = rng.uniform(x0 + 10, x1 - 10), rng.uniform(10, H - 12)
            c.fill(rrect(x - 7, y - 5, x + 7, y + 5, 0.4), zone=[1, 2][k % 2], shade=1.1)
            c.line(rrect(x - 7, y - 5, x + 7, y + 5, 0.4), INNER, zone=0, closed=True)
            c.fill(ell(x, y + 4, 1.1, 1.1, 10), zone=[2, 1][k % 2], shade=0.8)
        c.line(board, INNER, zone=0, closed=True)
    elif style == "calendar":
        c.fill(ell(0, H + 1, 1, 1, 10), zone=3)
        page = rrect(x0, 0, x1, H, 0.8)
        shaded(c, page, 3, "bottom", SOFT, 0.1)
        c.fill(rrect(x0, H * 0.55, x1, H, 0.8), zone=1)
        c.fill(ell(-W * 0.1, H * 0.78, W * 0.18, H * 0.12, 20), zone=2)
        for i in range(7):
            for j in range(4):
                c.fill(rrect(x0 + 2 + i * (W - 4) / 7, 2 + j * H * 0.12, x0 + 1 + (i + 1) * (W - 4) / 7, 1 + (j + 1) * H * 0.12, 0.2),
                       zone=2 if (i == 3 and j == 2) else 3, shade=0.9 if (i + j) % 2 else 1.0)
        for k in range(6):
            c.ellipse(x0 + 4 + k * (W - 8) / 5, H - 0.5, 0.6, 0.6, zone=0)


def garage(it: Item, style: str = "tire", seed: int = 2):
    """Garage: Reifen (Sommer/Winter/Felgen), Reifenstapel, Wagenheber, Ölkanne, Luftpumpe, Autowasch-Set,
    Werkzeugwagen, Schneeschaufel, Kabeltrommel."""
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style.startswith("tire"):
        kind = style.split("_")[1] if "_" in style else "summer"
        if kind == "stack":                                          # vier Reifen liegend gestapelt
            n = 4
            for k in range(n):
                y = k * H / n
                t = rrect(x0, y, x1, y + H / n - 0.5, H / n * 0.45)
                shaded(c, t, 1, "bottom", SHADE, 0.3)
                for j in range(8):
                    line(c, [(x0 + 4 + j * (W - 8) / 7, y + 2), (x0 + 6 + j * (W - 8) / 7, y + H / n - 2)], zone=1, shade=0.6)
            c.fill(ell(0, H - 0.5, W * 0.28, H / n * 0.2, 24), zone=0, alpha=0.85)
            return
        r = min(W, H) / 2
        c.fill(ell(0, r, r, r, 48), zone=1)
        c.line(ell(0, r, r, r, 48), INNER, zone=0, closed=True)
        for k in range(24):                                          # Profil
            a = k * math.pi / 12
            c.line([(math.cos(a) * r * 0.86, r + math.sin(a) * r * 0.86), (math.cos(a) * r * 0.99, r + math.sin(a) * r * 0.99)],
                   0.8 if kind == "winter" else 0.5, zone=1, shade=0.6)
        rim = ell(0, r, r * 0.6, r * 0.6, 40)
        c.fill(rim, zone=3)
        c.line(rim, INNER, zone=0, closed=True)
        spokes = {"summer": 5, "winter": 0, "sport": 10, "steel": 0}.get(kind, 5)
        for k in range(spokes):
            a = k * 2 * math.pi / spokes
            c.line([(math.cos(a) * r * 0.12, r + math.sin(a) * r * 0.12), (math.cos(a) * r * 0.55, r + math.sin(a) * r * 0.55)],
                   r * (0.12 if spokes <= 5 else 0.05), zone=2)
        if kind in ("winter", "steel"):
            for k in range(8):
                a = k * math.pi / 4
                c.fill(ell(math.cos(a) * r * 0.38, r + math.sin(a) * r * 0.38, r * 0.07, r * 0.07, 12), zone=0, alpha=0.7)
        if kind == "winter":
            c.fill(ell(-r * 0.7, r * 1.5, r * 0.12, r * 0.12, 6), zone=2, shade=1.4)                   # Schneeflocke-Symbol
        c.fill(ell(0, r, r * 0.12, r * 0.12, 16), zone=2, shade=0.8)
    elif style == "car_jack":
        c.fill(rrect(x0, 0, x1, H * 0.15, 1), zone=1)
        for sx in (-1, 1):
            c.line([(sx * W * 0.35, H * 0.15), (0, H * 0.55)], 1.6, zone=1, shade=0.9)
            c.line([(sx * W * 0.35, H * 0.95), (0, H * 0.55)], 1.6, zone=1)
        c.fill(rrect(-W * 0.2, H * 0.9, W * 0.2, H, 0.6), zone=1)
        c.line([(x0, H * 0.55), (x1 + 6, H * 0.55)], 0.9, zone=3)
        c.fill(ell(x1 + 7, H * 0.55, 1.6, 1.6, 12), zone=2)
    elif style == "oil_can":
        body = rrect(x0, 0, W * 0.3, H * 0.75, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(rrect(x0, H * 0.25, W * 0.3, H * 0.5, 0.4), zone=2, clip=cl)
        c.fill(trap(-W * 0.12, W * 0.08, H * 0.74, -W * 0.06, W * 0.02, H, 0.5), zone=3)
        c.line([(W * 0.3, H * 0.65), (x1, H * 0.95)], 1.0, zone=3)
        c.line(smooth([(x0 + 2, H * 0.75), (-W * 0.2, H * 0.95), (W * 0.05, H * 0.75)], closed=False), 0.8, zone=3)
    elif style == "bike_pump":
        c.fill(rrect(x0, 0, x1, H * 0.05, 0.6), zone=3)
        body = rrect(-W * 0.18, H * 0.05, W * 0.18, H * 0.8, W * 0.1)
        shaded(c, body, 1, "right", SHADE, 0.3)
        c.fill(ell(0, H * 0.6, W * 0.15, W * 0.15, 16), zone=2, shade=1.3)
        c.line([(0, H * 0.8), (0, H * 0.95)], 0.8, zone=3)
        c.fill(rrect(x0 + 1, H * 0.94, x1 - 1, H, 1), zone=2)
        c.line(smooth([(-W * 0.2, H * 0.2), (x0 - 2, H * 0.3), (x0 - 1, H * 0.7)], closed=False), 0.6, zone=0)
    elif style == "car_wash":                                        # Eimer mit Schaum + Schwamm
        c.line(smooth([(x0 + 2, H * 0.7), (0, H * 1.0), (x1 - 2, H * 0.7)], closed=False), 0.6, zone=3)
        body = trap(-W * 0.36, W * 0.36, 0, x0, x1, H * 0.72, 1)
        shaded(c, body, 1, "right", SHADE, 0.25)
        for k in range(5):
            c.fill(ell(x0 + 4 + k * (W - 8) / 4, H * 0.75, 3.2, 2.4, 12), zone=2, shade=1.3)
        c.fill(rrect(W * 0.1, H * 0.74, W * 0.42, H * 0.9, 1.5), zone=3, shade=1.6)
    elif style == "tool_cart":                                       # Werkzeugwagen mit Schubladen
        for x in (x0 + 5, x1 - 5):
            c.fill(ell(x, 3, 3, 3, 12), zone=0, alpha=0.9)
        body = rrect(x0, 5, x1, H * 0.92, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.15)
        n = 5
        for k in range(n):
            y = 8 + k * (H * 0.92 - 11) / n
            c.fill(rrect(x0 + 3, y, x1 - 3, y + (H * 0.92 - 11) / n - 2, 0.6), zone=1, shade=1.05, clip=cl)
            c.fill(rrect(-W * 0.2, y + 2, W * 0.2, y + 3.4, 0.4), zone=3)
        c.fill(rrect(x0 - 1, H * 0.9, x1 + 1, H, 1), zone=2)
        c.line([(x1, H * 0.7), (x1 + 6, H * 0.7), (x1 + 6, H * 0.95)], 1.2, zone=3)
    elif style == "snow_shovel":
        c.fill(rrect(-W * 0.05, H * 0.2, W * 0.05, H * 0.95, 0.5), zone=3)
        c.fill(rrect(-W * 0.2, H * 0.94, W * 0.2, H, 0.6), zone=2)
        blade = trap(x0, x1, 0, -W * 0.36, W * 0.36, H * 0.28, 1.2)
        shaded(c, blade, 1, "right", SHADE, 0.3)
    elif style == "cable_reel":
        c.fill(rrect(-W * 0.08, 0, W * 0.08, H * 0.3, 0.6), zone=3)
        c.fill(ell(0, H * 0.55, W / 2, H * 0.45, 32), zone=1)
        for r in range(4):
            c.line(ell(0, H * 0.55, W * (0.38 - r * 0.06), H * (0.34 - r * 0.05), 32), 1.2, zone=2, shade=1.0 - r * 0.05, closed=True)
        c.fill(ell(0, H * 0.55, W * 0.1, H * 0.1, 16), zone=3)
        c.line(ell(0, H * 0.55, W / 2, H * 0.45, 32), INNER, zone=0, closed=True)
        c.line([(0, H), (0, H * 0.95)], 1.2, zone=3)
