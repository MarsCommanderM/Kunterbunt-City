"""
Kinderzimmer & Rest-Inventar (P07): Kuscheltiere (6 Arten), Puppenhaus, Kaufladen, Spielzelt, Bällebad, Puppenwagen,
Gitarre, Wickeltisch, Truhe, Bügeleisen, Handtuchhalter, Werkzeugwand, Rasenmäher.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Holz/Metall/Details.
"""
from __future__ import annotations

import math
import random

from .cabinets import cabinet
from .kit import INNER, SHADE, SOFT, Item, cushion, ell, knob, leg, line, rrect, shaded, smooth, trap


def _eyes(c, x: float, y: float, d: float, r: float):
    for sx in (-1, 1):
        c.fill(ell(x + sx * d, y, r, r * 1.15, 16), zone=0)
        c.ellipse(x + sx * d + r * 0.35, y + r * 0.4, r * 0.35, r * 0.35, zone=1, shade=1.6)


def plush(it: Item, animal: str = "bunny"):
    """Kuscheltier sitzend: Hase, Bär, Elefant, Einhorn, Dino, Katze. Zone 1 Fell, 2 Bauch/Innenohr, 3 Details."""
    c, W, H = it.c, it.w, it.h
    hy, hr = H * 0.68, W * 0.3                                    # Kopf-Mitte, Radius
    if animal == "bunny":
        for sx in (-1, 1):
            ear = ell(sx * W * 0.12, H * 0.9, W * 0.08, H * 0.16, 24)
            shaded(c, ear, 1, "right", SHADE, 0.3)
            c.fill(ell(sx * W * 0.12, H * 0.9, W * 0.04, H * 0.11, 16), zone=2)
    elif animal in ("bear", "cat"):
        for sx in (-1, 1):
            if animal == "bear":
                c.fill(ell(sx * hr * 0.75, hy + hr * 0.75, hr * 0.32, hr * 0.32, 20), zone=1)
                c.fill(ell(sx * hr * 0.75, hy + hr * 0.75, hr * 0.17, hr * 0.17, 16), zone=2)
            else:
                c.fill([(sx * hr * 0.9, hy + hr * 0.3), (sx * hr * 0.2, hy + hr * 0.8), (sx * hr * 0.8, hy + hr * 1.25)], zone=1)
                c.fill([(sx * hr * 0.75, hy + hr * 0.45), (sx * hr * 0.35, hy + hr * 0.75), (sx * hr * 0.72, hy + hr * 1.05)], zone=2)
    elif animal == "elephant":
        for sx in (-1, 1):
            ear = ell(sx * hr * 1.05, hy, hr * 0.55, hr * 0.7, 28)
            shaded(c, ear, 1, "bottom", SHADE, 0.3)
            c.fill(ell(sx * hr * 1.05, hy, hr * 0.35, hr * 0.5, 24), zone=2)
    elif animal == "dino":
        for k in range(5):                                       # Rückenzacken
            a = math.pi * (0.2 + 0.6 * k / 4)
            x, y = math.cos(a) * hr * 1.05, hy + math.sin(a) * hr * 1.05
            c.fill([(x - 2.2, y - 1), (x + 2.2, y - 1), (x + math.cos(a) * 4, y + math.sin(a) * 4)], zone=2)
        c.fill(smooth([(W * 0.2, H * 0.12), (W * 0.5, H * 0.05), (W * 0.46, H * 0.16), (W * 0.24, H * 0.3)]), zone=1)
    body = ell(0, H * 0.3, W * 0.36, H * 0.3, 40)
    shaded(c, body, 1, "right", SHADE, 0.25)
    c.fill(ell(0, H * 0.28, W * 0.2, H * 0.18, 32), zone=2)
    for sx in (-1, 1):                                            # Füße + Arme
        c.fill(ell(sx * W * 0.2, H * 0.06, W * 0.13, H * 0.07, 24), zone=1, shade=0.95)
        c.fill(ell(sx * W * 0.2, H * 0.06, W * 0.07, H * 0.04, 16), zone=2)
        c.fill(ell(sx * W * 0.33, H * 0.36, W * 0.09, H * 0.12, 20), zone=1, shade=0.93)
    head = ell(0, hy, hr, hr * 0.92, 48)
    shaded(c, head, 1, "bottom", SOFT, 0.3)
    _eyes(c, 0, hy + hr * 0.1, hr * 0.38, hr * 0.13)
    if animal == "elephant":
        c.fill(smooth([(-hr * 0.2, hy - hr * 0.1), (hr * 0.2, hy - hr * 0.1), (hr * 0.3, hy - hr * 0.9), (hr * 0.6, hy - hr * 1.1),
                       (hr * 0.1, hy - hr * 0.95)]), zone=1)
    else:
        c.fill(ell(0, hy - hr * 0.3, hr * 0.32, hr * 0.22, 24), zone=2, shade=1.1)
        c.fill(ell(0, hy - hr * 0.2, hr * 0.1, hr * 0.07, 12), zone=3, shade=0.7)
    for sx in (-1, 1):
        c.fill(ell(sx * hr * 0.6, hy - hr * 0.2, hr * 0.12, hr * 0.07, 12), zone=2, alpha=0.7)
    if animal == "unicorn":
        c.fill([(-hr * 0.15, hy + hr * 0.8), (hr * 0.15, hy + hr * 0.8), (0, hy + hr * 1.5)], zone=3)
        for k in range(3):
            c.line([(-hr * 0.12 + k * 0.02 * hr, hy + hr * (0.9 + k * 0.18)), (hr * 0.1, hy + hr * (0.95 + k * 0.18))], 0.4, zone=0)
        for k in range(4):
            c.fill(ell(-hr * (0.7 - k * 0.12), hy + hr * (0.75 - k * 0.2), hr * 0.25, hr * 0.18, 16), zone=2)
        for sx in (-1, 1):
            c.fill([(sx * hr * 0.55, hy + hr * 0.55), (sx * hr * 0.25, hy + hr * 0.8), (sx * hr * 0.6, hy + hr * 1.05)], zone=1)


def toy_big(it: Item, style: str = "dollhouse", state: str = "", seed: int = 1):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "dollhouse":                                     # offen: zwei Etagen mit Möbeln
        wall_top = H * 0.62
        body = rrect(x0 + 2, 0, x1 - 2, wall_top, 1)
        c.fill(body, zone=1)
        for y0, y1 in ((2, wall_top * 0.48), (wall_top * 0.52, wall_top - 2)):
            for k, (a, b) in enumerate(((x0 + 5, -1.5), (1.5, x1 - 5))):
                c.fill(rrect(a, y0, b, y1, 0.5), zone=2, shade=1.12 if k else 1.0)
                c.fill(rrect(a, y0, b, y0 + 1.5, 0.3), zone=3)
        c.fill(rrect(x0 + 8, 3.5, x0 + 18, 9, 0.8), zone=1, shade=0.8)                    # Sofa
        c.fill(rrect(8, 3.5, 12, 14, 0.4), zone=3)                                        # Regal
        c.fill(rrect(x0 + 8, wall_top * 0.52 + 1.5, x0 + 20, wall_top * 0.52 + 6, 1), zone=1, shade=1.2)   # Bett
        c.fill(ell(10, wall_top * 0.8, 3, 3, 16), zone=3, shade=1.3)                      # Lampe
        c.line(body, INNER, zone=0, closed=True)
        roof = [(x0 - 3, wall_top - 1), (x1 + 3, wall_top - 1), (0, H)]
        cl = shaded(c, roof, 3, "bottom", SHADE, 0.15)
        for k in range(1, 5):
            line(c, [(x0 + k * W / 5 - 4, wall_top), (x0 + k * W / 5 + 2, wall_top + 5)], zone=3, clip=cl)
        c.fill(ell(0, wall_top + (H - wall_top) * 0.4, 3.5, 3.5, 20), zone=2, shade=1.3)
    elif style == "shop_stand":                                  # Kaufladen mit Markise
        for sx in (-1, 1):
            c.fill(rrect(sx * W / 2 - (3 if sx > 0 else 0), 0, sx * W / 2 + (0 if sx > 0 else 3), H * 0.82, 0.6), zone=3)
        counter = rrect(x0, 0, x1, H * 0.5, 1)
        cl = shaded(c, counter, 3, "right", SHADE, 0.12)
        c.fill(rrect(x0 + 5, H * 0.1, x1 - 5, H * 0.4, 0.8), zone=1, clip=cl)
        c.fill(rrect(x0 - 1, H * 0.48, x1 + 1, H * 0.53, 0.6), zone=3, shade=1.1)
        c.fill(rrect(W * 0.1, H * 0.53, W * 0.35, H * 0.62, 1), zone=1, shade=0.8)          # Kasse
        c.fill(rrect(W * 0.14, H * 0.58, W * 0.3, H * 0.6, 0.4), zone=2)
        for k in range(3):                                       # Obst im Regal
            c.fill(ell(x0 + 12 + k * 7, H * 0.57, 3, 3, 16), zone=[2, 1, 2][k], shade=1.1)
        awn = rrect(x0 - 4, H * 0.8, x1 + 4, H, 1)
        cl = c.mask(awn)
        c.fill(awn, zone=1)
        for k in range(0, int(W / 8) + 2, 2):
            c.fill(rrect(x0 - 4 + k * 8, H * 0.8, x0 + 4 + k * 8, H, 0), zone=2, clip=cl)
        for k in range(int(W / 8) + 1):
            c.fill(ell(x0 - 4 + k * 8 + 4, H * 0.8, 4, 2.5, 16), zone=[1, 2][k % 2])
        c.line(awn, INNER, zone=0, closed=True)
    elif style == "tipi":
        for sx in (-1, 1):
            c.line([(sx * W * 0.1, H * 0.85), (-sx * W * 0.08, H)], 1.4, zone=3)
        tent = [(x0, 0), (x1, 0), (W * 0.06, H * 0.88), (-W * 0.06, H * 0.88)]
        cl = shaded(c, tent, 1, "right", SHADE, 0.2)
        for k in range(4):
            y = H * (0.1 + k * 0.2)
            c.fill([(x0, y), (x1, y), (x1, y + H * 0.05), (x0, y + H * 0.05)], zone=2, clip=cl)
        door = [(-W * 0.2, 0), (W * 0.2, 0), (0, H * 0.55)]
        c.fill(door, zone=0, alpha=0.75)
        c.fill([(W * 0.2, 0), (W * 0.32, 0), (0, H * 0.55)], zone=1, shade=0.9)
        for k in range(7):                                       # Wimpel am Eingang
            x = -W * 0.3 + k * W * 0.1
            c.fill([(x - 2.5, H * 0.62), (x + 2.5, H * 0.62), (x, H * 0.55)], zone=[2, 3][k % 2])
    elif style == "ball_pit":
        rng = random.Random(seed)
        pit = rrect(x0, 0, x1, H, H * 0.45)
        cl = shaded(c, pit, 1, "bottom", SHADE, 0.3)
        for _ in range(int(W / 5)):
            x = rng.uniform(x0 + 4, x1 - 4)
            y = H * rng.uniform(0.85, 1.12)
            c.fill(ell(x, y, 3.5, 3.5, 16), zone=[1, 2, 3][rng.randrange(3)], shade=rng.choice([0.95, 1.1, 1.25]))
            c.line(ell(x, y, 3.5, 3.5, 16), INNER, zone=0, closed=True)
        c.fill(rrect(x0 + 6, H * 0.35, x1 - 6, H * 0.5, 2), zone=1, shade=1.1, clip=cl)
    elif style == "pram":                                        # Puppenwagen
        for x in (-W * 0.3, W * 0.25):
            c.fill(ell(x, H * 0.1, H * 0.1, H * 0.1, 24), zone=3, shade=0.6)
        c.line([(W * 0.2, H * 0.4), (W * 0.45, H), (W * 0.32, H)], 1.3, zone=3)
        basket = smooth([(x0 + 2, H * 0.72), (W * 0.32, H * 0.72), (W * 0.28, H * 0.22), (-W * 0.36, H * 0.22)])
        shaded(c, basket, 1, "bottom", SHADE, 0.35)
        hood = smooth([(x0, H * 0.72, "s"), (-W * 0.02, H * 0.72, "s"), (-W * 0.1, H * 0.98), (-W * 0.38, H * 0.98)])
        cl = shaded(c, hood, 2, "right", SHADE, 0.3)
        for k in range(1, 3):
            line(c, [(x0 + k * W * 0.16, H * 0.72), (-W * 0.38 + k * W * 0.1, H * 0.98)], zone=2, clip=cl)
        c.fill(ell(W * 0.1, H * 0.74, W * 0.1, H * 0.06, 16), zone=2, shade=1.2)            # Puppen-Köpfchen
    elif style == "guitar":
        c.fill(rrect(-W * 0.07, H * 0.45, W * 0.07, H * 0.9, 0.6), zone=3)
        c.fill(rrect(-W * 0.12, H * 0.88, W * 0.12, H, 1), zone=3, shade=0.8)
        for k in range(3):
            for sx in (-1, 1):
                c.ellipse(sx * W * 0.16, H * (0.9 + k * 0.035), 0.7, 0.5, zone=3, shade=1.3)
        body = smooth([(0, H * 0.5), (x1, H * 0.4), (W * 0.36, H * 0.26), (x1, H * 0.12), (0, 0), (x0, H * 0.12), (-W * 0.36, H * 0.26),
                       (x0, H * 0.4)])
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(ell(0, H * 0.3, W * 0.12, W * 0.12, 20), zone=0, alpha=0.85)
        c.fill(rrect(-W * 0.18, H * 0.1, W * 0.18, H * 0.13, 0.4), zone=2)
        for k in range(4):
            c.line([(-W * 0.045 + k * W * 0.03, H * 0.12), (-W * 0.045 + k * W * 0.03, H * 0.9)], 0.15, zone=2, shade=1.3)
    elif style == "changing":                                    # Wickeltisch: Kommode + Auflage + Rand
        cabinet(it, "W/W|D", top="flat", legs="short")
        c.fill(rrect(x0 + 2, H - 0.5, x1 - 2, H + 5, 2.5), zone=2)
        c.line(rrect(x0 + 2, H - 0.5, x1 - 2, H + 5, 2.5), INNER, zone=0, closed=True)
        for k in range(1, 4):
            line(c, [(x0 + 2 + k * (W - 4) / 4, H), (x0 + 2 + k * (W - 4) / 4, H + 5)], zone=2)
        c.fill(rrect(x1 - 3, H, x1 + 1, H + 12, 1), zone=3)
    elif style == "chest":                                       # Truhe mit Beschlägen (offen: Deckel hoch, Decken drin)
        body = rrect(x0, 0, x1, H * 0.78, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.15)
        for x in (x0 + 6, x1 - 6):
            c.fill(rrect(x - 2, 0, x + 2, H * 0.78, 0.4), zone=3, clip=cl)
        if state == "open":
            c.fill(rrect(x0 + 3, H * 0.7, x1 - 3, H * 0.82, 2), zone=2)
            c.fill(rrect(x0 + 10, H * 0.72, x0 + 30, H * 0.86, 2), zone=2, shade=1.2)
            lid = rrect(x0, H * 0.78, x1, H * 1.25, 3)
            shaded(c, lid, 1, "right", 0.8, 0.2)
        else:
            lid = smooth([(x0, H * 0.76, "s"), (x1, H * 0.76, "s"), (x1 - 2, H * 0.94), (0, H), (x0 + 2, H * 0.94)])
            shaded(c, lid, 1, "bottom", SOFT, 0.3)
            c.fill(rrect(-4, H * 0.62, 4, H * 0.8, 0.8), zone=3)
            c.fill(ell(0, H * 0.68, 1.2, 1.2, 12), zone=0)
    elif style == "iron":                                        # Bügeleisen (an: Dampf)
        c.fill(smooth([(x0, 0, "s"), (x1, 0, "s"), (W * 0.2, H * 0.5), (x0 + 2, H * 0.5)]), zone=3)
        body = smooth([(x0 + 1, H * 0.1, "s"), (W * 0.46, H * 0.1, "s"), (W * 0.18, H * 0.55), (x0 + 2, H * 0.55)])
        shaded(c, body, 1, "right", SHADE, 0.3)
        c.line(smooth([(x0 + 4, H * 0.55), (x0 + 6, H * 0.95), (W * 0.1, H * 0.95), (W * 0.14, H * 0.55)], closed=False), 1.8, zone=2)
        c.ellipse(-W * 0.05, H * 0.32, 1.2, 1.2, zone=2)
        if state == "on":
            for k in range(3):
                c.glass(ell(x1 + 2 + k * 3, H * (0.2 + k * 0.3), 2.5, 2.2, 16), zone=0, opacity=0.18)
    elif style == "towel_rail":                                  # Handtuchhalter (Wand) mit Handtuch
        c.line([(x0 + 2, H * 0.8), (x1 - 2, H * 0.8)], 1.6, zone=3)
        for sx in (-1, 1):
            c.fill(rrect(sx * W / 2 - (3 if sx > 0 else 0), H * 0.7, sx * W / 2 + (0 if sx > 0 else 3), H, 0.8), zone=3)
        towel = rrect(-W * 0.36, 0, W * 0.36, H * 0.84, 1.5)
        cl = shaded(c, towel, 1, "right", SHADE, 0.25)
        for y in (H * 0.1, H * 0.16):
            c.fill(rrect(-W * 0.36, y, W * 0.36, y + H * 0.03, 0.3), zone=2, clip=cl)
    elif style == "tool_wall":                                   # Lochwand mit Werkzeug (Wand)
        board = rrect(x0, 0, x1, H, 1.5)
        cl = shaded(c, board, 1, "bottom", SOFT, 0.15)
        for i in range(int(W / 5)):
            for j in range(int(H / 5)):
                c.ellipse(x0 + 2.5 + i * 5, 2.5 + j * 5, 0.4, 0.4, zone=1, shade=0.7, clip=cl)
        c.fill(rrect(x0 + 8, H * 0.35, x0 + 11, H * 0.85, 0.6), zone=3)                      # Hammer
        c.fill(rrect(x0 + 4, H * 0.78, x0 + 15, H * 0.88, 1), zone=2)
        c.line([(x0 + 22, H * 0.3), (x0 + 22, H * 0.85)], 1.6, zone=3)                      # Schraubenschlüssel
        c.line(ell(x0 + 22, H * 0.87, 2.5, 2.5, 16), 1.2, zone=3, closed=True)
        c.fill(rrect(x0 + 30, H * 0.55, x0 + 34, H * 0.85, 1), zone=2)                      # Schraubendreher
        c.line([(x0 + 32, H * 0.25), (x0 + 32, H * 0.55)], 0.8, zone=3)
        c.fill(smooth([(W * 0.05, H * 0.85), (W * 0.35, H * 0.85), (W * 0.35, H * 0.7), (W * 0.1, H * 0.62)]), zone=3, shade=1.2)  # Säge
        c.fill(rrect(W * 0.02, H * 0.72, W * 0.1, H * 0.88, 1), zone=2)
        for k in range(4):                                       # Schraubgläser
            c.fill(rrect(x0 + 8 + k * 10, H * 0.06, x0 + 15 + k * 10, H * 0.2, 1), zone=2, shade=1.2, alpha=0.8)
            c.fill(rrect(x0 + 8 + k * 10, H * 0.18, x0 + 15 + k * 10, H * 0.22, 0.5), zone=3)
        c.fill(rrect(x0 + 5, H * 0.04, x0 + 50, H * 0.06, 0.3), zone=3)
        c.line(smooth([(W * 0.2, H * 0.45), (W * 0.35, H * 0.4), (W * 0.42, H * 0.3), (W * 0.3, H * 0.2), (W * 0.18, H * 0.3)]), 1.2, zone=2,
               closed=True)                                      # Kabelrolle
    elif style in ("mower", "mower_ride"):
        if style == "mower_ride":                                # Aufsitzmäher
            for x, r in ((-W * 0.3, H * 0.22), (W * 0.32, H * 0.15)):
                c.fill(ell(x, r, r, r, 24), zone=0, alpha=0.95)
                c.fill(ell(x, r, r * 0.45, r * 0.45, 16), zone=3)
            body = smooth([(x0, H * 0.2, "s"), (x1, H * 0.2, "s"), (x1, H * 0.45), (W * 0.1, H * 0.5), (-W * 0.2, H * 0.48), (x0, H * 0.45)])
            shaded(c, body, 1, "bottom", SHADE, 0.3)
            c.fill(rrect(-W * 0.42, H * 0.46, -W * 0.14, H * 0.58, 2), zone=2)
            c.fill(rrect(-W * 0.42, H * 0.56, -W * 0.34, H * 0.8, 2), zone=2)
            c.line([(W * 0.1, H * 0.5), (W * 0.02, H * 0.85)], 1.4, zone=3)
            c.fill(ell(W * 0.02, H * 0.86, W * 0.08, H * 0.02, 16), zone=3)
            return
        c.line([(-W * 0.2, H * 0.3), (-W * 0.45, H)], 1.6, zone=3)
        c.line([(-W * 0.45, H), (-W * 0.3, H)], 1.8, zone=3)
        c.fill(rrect(-W * 0.4, H * 0.5, -W * 0.2, H * 0.72, 1.5), zone=2)                    # Fangkorb
        for x in (-W * 0.3, W * 0.3):
            c.fill(ell(x, H * 0.08, H * 0.08, H * 0.08, 20), zone=0, alpha=0.95)
            c.fill(ell(x, H * 0.08, H * 0.035, H * 0.035, 12), zone=3)
        deck = smooth([(-W * 0.4, H * 0.1, "s"), (W * 0.46, H * 0.1, "s"), (W * 0.4, H * 0.3), (-W * 0.2, H * 0.36)])
        shaded(c, deck, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(-W * 0.02, H * 0.3, W * 0.2, H * 0.4, 1.5), zone=3, shade=0.8)
