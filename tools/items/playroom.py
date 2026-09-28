"""
Kinderzimmer & Baby, Teil 2 (P07-Inventar): Spielküche, Kinder-Werkbank, Brettspiel, Stifte, Malkasten, Stapelturm,
Spielmatte, Babywippe, Babyphone, Windeln, Babybadewanne.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Holz/Details.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, ell, knob, leg, line, rrect, shaded, smooth, trap

RAINBOW = [(1, 1.0), (2, 1.0), (3, 1.0), (1, 1.25), (2, 1.25), (3, 0.8)]


def playroom(it: Item, style: str = "play_kitchen", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "play_kitchen":                                     # Herd, Spüle, Backofen, Regal
        c.fill(rrect(x0 + 2, H * 0.55, x1 - 2, H, 1), zone=1, shade=0.93)
        c.fill(rrect(x0 + 6, H * 0.62, -2, H * 0.92, 0.6), zone=2, shade=1.3)                        # Fliesenwand
        for k in range(3):
            c.fill(ell(x0 + 12 + k * 9, H * 0.84, 3, 2, 12), zone=[2, 3, 1][k], shade=0.9)           # Töpfchen
        c.fill(rrect(4, H * 0.8, x1 - 6, H * 0.84, 0.4), zone=3)                                      # Regal
        for k in range(3):
            c.fill(rrect(8 + k * 7, H * 0.84, 12 + k * 7, H * 0.9, 0.4), zone=[1, 2, 3][k], shade=1.2)
        body = rrect(x0, 0, x1, H * 0.55, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        oven = rrect(x0 + 5, 5, -2, H * 0.4, 1.5)
        c.fill(oven, zone=2, shade=0.9)
        c.fill(rrect(x0 + 9, 9, -6, H * 0.34, 1.2), zone=2, shade=0.5)
        c.line(oven, INNER, zone=0, closed=True)
        c.fill(rrect(4, 5, x1 - 5, H * 0.4, 1.5), zone=2, shade=1.05)
        c.line(rrect(4, 5, x1 - 5, H * 0.4, 1.5), INNER, zone=0, closed=True)
        knob(c, x1 - 9, H * 0.22, 1.2)
        c.fill(rrect(x0 - 1, H * 0.53, x1 + 1, H * 0.58, 0.8), zone=3)
        for k in range(2):                                           # Kochplatten
            c.fill(ell(x0 + 10 + k * 12, H * 0.585, 5, 0.9, 16), zone=0, alpha=0.85)
        c.fill(ell(W * 0.24, H * 0.585, W * 0.14, 1.2, 20), zone=2, shade=0.6)                        # Spüle
        c.line([(W * 0.3, H * 0.58), (W * 0.3, H * 0.66), (W * 0.24, H * 0.68)], 1.0, zone=3, shade=1.3)
        for k in range(3):
            knob(c, x0 + 10 + k * 7, H * 0.47, 1.4, zone=3)
    elif style == "workbench":                                      # Kinder-Werkbank mit Werkzeug
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 4), 0, H * 0.58, 4, 4)
        c.fill(rrect(x0 + 3, H * 0.15, x1 - 3, H * 0.2, 0.6), zone=3, shade=0.9)
        top = rrect(x0, H * 0.56, x1, H * 0.64, 1)
        shaded(c, top, 3, "bottom", SHADE, 0.35)
        back = rrect(x0 + 3, H * 0.64, x1 - 3, H, 1)
        c.fill(back, zone=1)
        c.line(back, INNER, zone=0, closed=True)
        c.fill(rrect(x0 + 8, H * 0.72, x0 + 11, H * 0.95, 0.6), zone=3)                             # Hammer
        c.fill(rrect(x0 + 5, H * 0.9, x0 + 14, H * 0.96, 0.8), zone=2)
        c.fill(rrect(x0 + 20, H * 0.75, x0 + 23, H * 0.95, 0.8), zone=2, shade=1.2)                 # Schraubendreher
        c.line(ell(W * 0.2, H * 0.84, 4, 4, 16), 1.2, zone=2, closed=True)                          # Schlüssel
        for k in range(4):                                           # Schrauben + Mutter auf der Platte
            c.fill(ell(x0 + 8 + k * 6, H * 0.66, 1.5, 1.2, 10), zone=[1, 2][k % 2], shade=1.1)
        c.fill(rrect(W * 0.18, H * 0.64, W * 0.36, H * 0.7, 0.8), zone=2)                           # Schraubstock
    elif style == "board_game":                                     # Schachtel mit Spielbrett und Figuren daneben
        box = rrect(x0, 0, x1, H * 0.45, 0.8)
        cl = shaded(c, box, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0, H * 0.3, x1, H * 0.45, 0.8), zone=1, shade=1.08, clip=cl)
        for k in range(4):
            c.fill(ell(x0 + 8 + k * (W - 16) / 3, H * 0.18, 2.5, 2.5, 12), zone=[2, 3][k % 2], shade=1.2, clip=cl)
        c.fill(rrect(-W * 0.3, H * 0.34, W * 0.3, H * 0.41, 0.6), zone=2, shade=1.1)
        for k, (x, z) in enumerate(((-W * 0.3, 2), (-W * 0.1, 3), (W * 0.15, 1), (W * 0.32, 2))):  # Spielfiguren
            c.fill(trap(x - 1.8, x + 1.8, H * 0.45, x - 1.0, x + 1.0, H * 0.8, 0.4), zone=z, shade=1.1)
            c.fill(ell(x, H * 0.86, 1.6, 1.6, 12), zone=z, shade=1.1)
            c.line(ell(x, H * 0.86, 1.6, 1.6, 12), 0.2, zone=0, closed=True)
        c.fill(rrect(W * 0.38, H * 0.46, W * 0.48, H * 0.6, 0.6), zone=3, shade=1.5)                 # Würfel
        c.ellipse(W * 0.43, H * 0.53, 0.5, 0.5, zone=0)
    elif style == "crayons":                                        # Stifte im Becher
        for k, (z, sh) in enumerate(RAINBOW):
            x = x0 + 3 + k * (W - 6) / 5
            h = H * (0.8 + 0.2 * ((k * 3) % 4) / 3)
            c.fill(rrect(x - 1.2, H * 0.3, x + 1.2, h - 2, 0.5), zone=z, shade=sh)
            c.fill([(x - 1.2, h - 2), (x + 1.2, h - 2), (x, h)], zone=z, shade=sh * 0.85)
        cup = trap(x0 + 1, x1 - 1, 0, x0, x1, H * 0.55, 1)
        shaded(c, cup, 1, "right", SHADE, 0.25)
        c.fill(rrect(x0, H * 0.2, x1, H * 0.3, 0.4), zone=2)
    elif style == "paints":                                         # Malkasten offen mit Pinsel
        box = rrect(x0, 0, x1, H * 0.6, 1)
        shaded(c, box, 3, "right", SHADE, 0.15)
        for k, (z, sh) in enumerate(RAINBOW):
            x = x0 + 4 + (k % 3) * (W - 8) / 3 + (W - 8) / 6
            y = H * (0.18 if k < 3 else 0.42)
            c.fill(ell(x, y, (W - 8) / 7.5, H * 0.08, 16), zone=z, shade=sh)
            c.line(ell(x, y, (W - 8) / 7.5, H * 0.08, 16), INNER, zone=0, closed=True)
        c.line([(x0 + 2, H * 0.65), (x1 - 2, H * 0.95)], 0.8, zone=3, shade=0.7)                      # Pinsel
        c.fill(ell(x1 - 3, H * 0.93, 1.4, 1.0, 10), zone=2)
    elif style == "stacker":                                        # Stapelturm (Ringe)
        c.fill(rrect(-W * 0.06, H * 0.08, W * 0.06, H * 0.95, 1), zone=3)
        c.fill(ell(0, H * 0.95, W * 0.1, H * 0.06, 16), zone=3)
        c.fill(rrect(x0, 0, x1, H * 0.1, 2), zone=3, shade=0.9)
        for k, (z, sh) in enumerate(RAINBOW[:5]):
            r = W * (0.46 - k * 0.07)
            y = H * (0.16 + k * 0.15)
            ring = ell(0, y, r, H * 0.075, 28)
            shaded(c, ring, z, "bottom", SHADE * sh, 0.35)
    elif style == "play_mat":                                       # flach: Spielmatte mit Tiermotiven (placement rug)
        body = rrect(x0, 0, x1, H, H * 0.25)
        cl = shaded(c, body, 1, "bottom", SOFT, 0.2)
        for k in range(4):
            x = x0 + W * (k + 0.5) / 4
            c.fill(ell(x, H * 0.5, W * 0.08, H * 0.3, 20), zone=[2, 3][k % 2], clip=cl)
            c.line(ell(x, H * 0.5, W * 0.08, H * 0.3, 20), INNER, zone=0, closed=True)
        for k in range(12):
            c.ellipse(x0 + 6 + k * (W - 12) / 11, H * 0.1, 0.9, 0.9, zone=2, shade=1.2)
    elif style == "bouncer":                                        # Babywippe mit Spielbogen
        c.line(smooth([(x0, 0), (0, H * 0.06), (x1, 0)], closed=False), 1.4, zone=3)
        seat = smooth([(x0 + 2, H * 0.12, "s"), (W * 0.2, H * 0.1, "s"), (W * 0.46, H * 0.62), (W * 0.36, H * 0.7), (W * 0.1, H * 0.3)])
        shaded(c, seat, 1, "bottom", SHADE, 0.35)
        c.fill(smooth([(x0 + 6, H * 0.16), (W * 0.16, H * 0.16), (W * 0.34, H * 0.56), (W * 0.26, H * 0.6), (W * 0.05, H * 0.3)]), zone=2)
        c.line(smooth([(x0 + 4, H * 0.14), (-W * 0.05, H), (W * 0.4, H * 0.64)], closed=False), 1.0, zone=3)
        for k, t in enumerate((0.3, 0.55, 0.8)):
            x = x0 + 4 + (W * 0.3) * t
            y = H * (0.3 + 0.6 * math.sin(math.pi * t))
            c.line([(x, y), (x, y - 8)], 0.3, zone=0)
            c.fill(ell(x, y - 10, 2.4, 2.4, 12), zone=[2, 1, 2][k], shade=1.2)
    elif style == "baby_monitor":
        c.line([(W * 0.25, H * 0.7), (W * 0.35, H)], 1.0, zone=3)
        body = rrect(x0, 0, x1, H * 0.78, W * 0.3)
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W * 0.3, H * 0.4, W * 0.3, H * 0.66, 1), zone=2, shade=0.7)
        for k in range(3):
            c.fill(rrect(-W * 0.2 + k * W * 0.15, H * 0.44, -W * 0.12 + k * W * 0.15, H * (0.48 + 0.05 * k), 0.2), zone=2, shade=1.4)
        c.ellipse(0, H * 0.18, W * 0.12, W * 0.12, zone=3)
    elif style == "diapers":                                        # Windelpaket
        body = rrect(x0, 0, x1, H, 2)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(ell(0, H * 0.5, W * 0.3, H * 0.22, 28), zone=2, clip=cl)
        c.fill(ell(-W * 0.06, H * 0.53, W * 0.08, H * 0.07, 16), zone=3, shade=1.3, clip=cl)           # Baby-Gesicht
        c.fill(rrect(x0, H * 0.86, x1, H, 1.5), zone=1, shade=0.9)
        c.line(smooth([(-W * 0.2, H), (0, H * 1.15), (W * 0.2, H)], closed=False), 1.0, zone=1, shade=0.8)
    elif style == "baby_bath":
        for sx in (-1, 1):
            c.line([(sx * W * 0.4, 0), (sx * W * 0.3, H * 0.6)], 1.4, zone=3)
        tub = smooth([(x0, H, "s"), (x1, H, "s"), (W * 0.4, H * 0.62), (W * 0.28, H * 0.52), (-W * 0.28, H * 0.52), (-W * 0.4, H * 0.62)])
        shaded(c, tub, 1, "bottom", SHADE, 0.35)
        c.fill(rrect(x0 - 1, H * 0.94, x1 + 1, H + 1.5, 1.5), zone=1, shade=1.06)
        if state == "on":
            for k in range(6):
                c.fill(ell(x0 + 6 + k * W * 0.15, H + 2 + (k % 2) * 1.5, 3.5, 2.6, 16), zone=2, shade=1.25)
        c.fill(ell(W * 0.3, H + 3, 3, 2.4, 12), zone=2, shade=0.8)                                  # Entchen
