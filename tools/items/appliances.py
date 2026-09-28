"""
Große Geräte mit Zuständen (P04b-T10): Kühlschrank (auf/zu), Herd, Backofen, Waschmaschine, Spüle, Ventilator,
Computer, Spielkonsole (aus/an) + gekochte Speisen (Ergebnisse der Rezepte).
Zonen: 1 = Gehäuse (umfärbbar) · 2 = Akzent/Licht · 3 = Metall/Detail.
"""
from __future__ import annotations

import math

from .household import _band, _steam
from .kit import SHADE, SOFT, Item, ell, knob, leg, line, rrect, shaded, smooth, trap


def appliance(it: Item, style: str = "fridge", state: str = ""):
    c, W, H = it.c, it.w, it.h
    on = state in ("on", "open")
    if style == "fridge":
        body = rrect(-W / 2, 2, W / 2, H, 3)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        if on:
            c.fill(rrect(-W / 2 + 2.5, 4, W / 2 - 2.5, H - 3, 1.5), zone=2, shade=1.0)          # Licht innen
            for y in (H * 0.28, H * 0.5, H * 0.72):
                c.fill(rrect(-W / 2 + 3, y, W / 2 - 3, y + 1.2, 0.3), zone=3)
            for k, (x, y, z) in enumerate(((-W * 0.25, H * 0.29, 3), (W * 0.1, H * 0.51, 1), (-W * 0.05, H * 0.73, 3))):
                c.fill(rrect(x - 5, y + 1.2, x + 5, y + 12, 1.5), zone=z, shade=0.9)
                c.line(rrect(x - 5, y + 1.2, x + 5, y + 12, 1.5), 0.3, zone=0, closed=True)
            door = [(W / 2, 4), (W * 0.95, 10), (W * 0.95, H - 6), (W / 2, H - 1)]
            shaded(c, door, 1, "bottom", SHADE, 0.2)
            c.fill(rrect(W * 0.55, H * 0.5, W * 0.62, H * 0.75, 0.6), zone=3)
        else:
            line(c, [(-W / 2, H * 0.62), (W / 2, H * 0.62)], clip=cl, w=0.5)
            for y0, y1 in ((H * 0.7, H * 0.85), (H * 0.3, H * 0.5)):
                c.fill(rrect(W * 0.3, y0, W * 0.36, y1, 0.6), zone=3)
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 4), 0, 2.5, 3, 3)
    elif style in ("stove", "oven"):
        body = rrect(-W / 2, 2, W / 2, H, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        c.fill(rrect(-W / 2 - 0.5, H - 3, W / 2 + 0.5, H, 0.8), zone=3)
        for k in range(4):
            knob(c, -W * 0.36 + k * W * 0.24, H - 8, 1.6)
        win = rrect(-W * 0.38, 8, W * 0.38, H * 0.62, 2)
        c.fill(win, zone=0, alpha=0.85)
        c.fill(rrect(-W * 0.3, H * 0.66, W * 0.3, H * 0.7, 0.6), zone=3)
        if on:
            c.fill(win, zone=2, alpha=0.6)
            for k in range(3):
                c.fill(rrect(-W * 0.3, 12 + k * 1.2, W * 0.3, 12.8 + k * 1.2, 0.3), zone=2, alpha=0.5)
            if style == "stove":   # Flammen oben
                for x in (-W * 0.25, W * 0.25):
                    for k in (-1, 0, 1):
                        c.fill(smooth([(x + k * 2.2, H + 4.5), (x + k * 2.2 + 1.2, H + 0.5), (x + k * 2.2 - 1.2, H + 0.5)]),
                               zone=2)
        if style == "stove":
            for x in (-W * 0.25, W * 0.25):
                c.fill(ell(x, H + 0.3, W * 0.14, 0.9), zone=0)
    elif style == "washer":
        body = rrect(-W / 2, 1, W / 2, H, 2)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        line(c, [(-W / 2, H * 0.82), (W / 2, H * 0.82)], clip=cl)
        knob(c, W * 0.3, H * 0.9, 2.0)
        c.fill(rrect(-W * 0.4, H * 0.86, -W * 0.05, H * 0.94, 0.6), zone=2)
        r = W * 0.3
        c.fill(ell(0, H * 0.42, r, r), zone=3)
        c.fill(ell(0, H * 0.42, r * 0.78, r * 0.78), zone=0, alpha=0.85)
        if on:
            c.fill(smooth([(-r * 0.7, H * 0.42 - r * 0.2), (0, H * 0.42 + r * 0.1), (r * 0.7, H * 0.42 - r * 0.2),
                           (r * 0.6, H * 0.42 - r * 0.55), (-r * 0.6, H * 0.42 - r * 0.55)]), zone=2, alpha=0.8)
            for k in range(3):
                a = math.radians(40 + k * 50)
                c.glass(ell(math.cos(a) * r * 0.4, H * 0.42 + math.sin(a) * r * 0.3, r * 0.14, r * 0.14), zone=1, opacity=0.6)
        c.line(ell(0, H * 0.42, r * 0.78, r * 0.78), 0.4, zone=0, closed=True)
    elif style == "sink":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.72, 1.5), zone=1)
        cl = shaded(c, rrect(-W / 2, 0, W / 2, H * 0.72, 1.5), 1, "right", SHADE, 0.12)
        for sx in (-1, 1):
            c.line(rrect(sx * W * 0.25 - W * 0.2, 4, sx * W * 0.25 + W * 0.2, H * 0.62, 1), 0.3, zone=1, shade=0.7, closed=True)
        c.fill(rrect(-W / 2 - 1, H * 0.7, W / 2 + 1, H * 0.76, 0.6), zone=3)
        c.line(smooth([(0, H * 0.76), (0, H), (W * 0.15, H * 1.05), (W * 0.2, H * 0.92)], closed=False), 1.3, zone=3)
        knob(c, -W * 0.12, H * 0.8, 1.3)
        if on:
            c.glass(_band([(W * 0.2, H * 0.92), (W * 0.2, H * 0.76)], 0.7), zone=2, opacity=0.7)
            for k in range(4):
                c.glass(ell(W * 0.2 + (k - 1.5) * 1.5, H * 0.78, 0.6, 0.6), zone=2, opacity=0.6)
    elif style == "fan":
        c.fill(ell(0, 1.5, W * 0.3, 1.5), zone=1)
        c.fill(rrect(-1.2, 1, 1.2, H * 0.55, 0.6), zone=1, shade=0.9)
        cx, cy, r = 0, H * 0.72, W * 0.48
        c.line(ell(cx, cy, r, r), 0.8, zone=3, closed=True)
        for k in range(3):
            a = math.radians(90 + k * 120 + (35 if on else 0))
            blade = smooth([(cx, cy), (cx + math.cos(a - 0.35) * r * 0.9, cy + math.sin(a - 0.35) * r * 0.9),
                            (cx + math.cos(a + 0.35) * r * 0.9, cy + math.sin(a + 0.35) * r * 0.9)])
            c.fill(blade, zone=2, shade=0.95 if on else 1.0)
            c.line(blade, 0.3, zone=0, closed=True)
        c.fill(ell(cx, cy, r * 0.14, r * 0.14), zone=1)
        if on:
            for k in range(3):
                c.line(smooth([(r * 1.05, cy + (k - 1) * r * 0.4), (r * 1.3, cy + (k - 1) * r * 0.45)], closed=False), 0.5,
                       zone=0, alpha=0.4)
    elif style in ("computer", "console"):
        if style == "computer":
            c.fill(rrect(-W * 0.18, 0, W * 0.18, 2, 0.8), zone=1)
            c.fill(rrect(-1.5, 2, 1.5, H * 0.3, 0.5), zone=1, shade=0.85)
            body = rrect(-W / 2, H * 0.28, W / 2, H, 1.5)
            c.fill(body, zone=1)
            scr = rrect(-W / 2 + 1.8, H * 0.28 + 1.8, W / 2 - 1.8, H - 1.8, 0.8)
        else:
            c.fill(rrect(-W / 2, 0, W / 2, H * 0.4, 1.5), zone=1)
            c.fill(ell(W * 0.3, H * 0.2, 1.2, 1.2), zone=2 if on else 3)
            scr = None
            for sx in (-1, 1):
                pad = smooth([(sx * W * 0.1, H * 0.5), (sx * W * 0.45, H * 0.52), (sx * W * 0.48, H * 0.8), (sx * W * 0.1, H * 0.8)])
                c.fill(pad, zone=3)
                c.line(pad, 0.3, zone=0, closed=True)
        if scr is not None:
            c.fill(scr, zone=2 if on else 0, shade=1.0)
            if on:
                c.fill(rrect(-W * 0.35, H * 0.8, -W * 0.1, H * 0.9, 0.5), zone=3, alpha=0.8)
                c.fill(rrect(-W * 0.35, H * 0.55, W * 0.3, H * 0.62, 0.4), zone=1, alpha=0.5)
                c.fill(rrect(-W * 0.35, H * 0.44, W * 0.1, H * 0.5, 0.4), zone=1, alpha=0.5)


def cooked(it: Item, style: str = "toast"):
    """Gekochte Speisen – Ergebnisse der Rezepte."""
    c, W, H = it.c, it.w, it.h
    if style in ("toast", "bread_slice"):
        body = smooth([(-W / 2, 0, "s"), (W / 2, 0, "s"), (W / 2, H * 0.72), (W * 0.35, H), (-W * 0.35, H), (-W / 2, H * 0.72)])
        c.fill(body, zone=2)
        c.fill(smooth([(-W * 0.4, 1, "s"), (W * 0.4, 1, "s"), (W * 0.4, H * 0.7), (W * 0.28, H * 0.9), (-W * 0.28, H * 0.9),
                       (-W * 0.4, H * 0.7)]), zone=1)
        c.line(body, 0.3, zone=0, closed=True)
    elif style == "fried_egg":
        c.fill(smooth([(-W / 2, H * 0.3), (-W * 0.2, 0), (W * 0.3, H * 0.1), (W / 2, H * 0.5), (W * 0.1, H), (-W * 0.35, H * 0.8)]),
               zone=1)
        c.fill(ell(W * 0.05, H * 0.5, W * 0.18, H * 0.25), zone=2)
    elif style == "smoothie":
        body = trap(-W * 0.36, W * 0.36, 0, -W / 2, W / 2, H * 0.85, 0.8)
        c.glass(body, zone=3, opacity=0.35)
        c.fill(trap(-W * 0.34, W * 0.34, 0.5, -W * 0.46, W * 0.46, H * 0.78, 0.6), zone=1)
        c.line(body, 0.3, zone=0, closed=True)
        c.line([(W * 0.1, H * 0.7), (W * 0.25, H)], 0.8, zone=2)
        c.fill(ell(-W * 0.3, H * 0.84, W * 0.14, W * 0.14), zone=2)
    elif style == "soup":
        body = smooth([(-W * 0.3, 0.2, "s"), (W * 0.3, 0.2, "s"), (W / 2, H * 0.7, "s"), (-W / 2, H * 0.7, "s")])
        shaded(c, body, 3, "right", SHADE, 0.25)
        c.fill(ell(0, H * 0.7, W * 0.46, H * 0.12), zone=1)
        _steam(c, 0, H * 0.75, W * 0.4)
    elif style == "pancakes":
        c.fill(ell(0, H * 0.08, W / 2, H * 0.08), zone=3)
        for k in range(4):
            y = H * (0.15 + k * 0.16)
            c.fill(rrect(-W * 0.42, y, W * 0.42, y + H * 0.14, H * 0.07), zone=1)
            c.line(rrect(-W * 0.42, y, W * 0.42, y + H * 0.14, H * 0.07), 0.3, zone=0, closed=True)
        c.fill(smooth([(-W * 0.2, H * 0.78), (W * 0.2, H * 0.8), (W * 0.1, H * 0.55), (-W * 0.12, H * 0.6)]), zone=2)
        c.fill(rrect(-W * 0.08, H * 0.8, W * 0.08, H * 0.9, 0.3), zone=2, shade=1.0)
    elif style == "sausage":
        for k in range(2):
            y = H * (0.25 + k * 0.45)
            c.fill(rrect(-W / 2, y - H * 0.2, W / 2, y + H * 0.2, H * 0.2), zone=1)
            for g in (-0.2, 0.0, 0.2):
                c.line([(g * W - 1, y + H * 0.15), (g * W + 1, y - H * 0.1)], 0.4, zone=0, alpha=0.6)
    elif style == "hot_drink":
        body = rrect(-W * 0.36, 0, W * 0.36, H * 0.75, 1.2)
        c.line(smooth([(W * 0.36, H * 0.6), (W / 2, H * 0.5), (W * 0.36, H * 0.25)], closed=False), 1.0, zone=3)
        shaded(c, body, 3, "right", SHADE, 0.25)
        c.fill(ell(0, H * 0.73, W * 0.32, H * 0.06), zone=1)
        _steam(c, 0, H * 0.78, W * 0.4)
    elif style == "popcorn_bowl":
        body = smooth([(-W * 0.3, 0.2, "s"), (W * 0.3, 0.2, "s"), (W / 2, H * 0.55, "s"), (-W / 2, H * 0.55, "s")])
        shaded(c, body, 3, "right", SHADE, 0.25)
        for k in range(9):
            c.fill(ell(-W * 0.38 + k * W * 0.095, H * (0.62 + (k % 3) * 0.12), W * 0.1, H * 0.1), zone=1)
    elif style == "cake_baked":
        from .fun import food
        food(it, "cake")
