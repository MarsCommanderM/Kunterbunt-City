"""
Kleine Dinge fürs Zuhause (P07-Inventar): Küchenhelfer, Bad-Kleinkram, Bettzeug, Kleidung, Baby-Sachen,
Deko-Kleinkram. Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe/Muster · 3 = Metall/Holz/Details.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, ell, knob, line, rrect, shaded, smooth, trap


def small(it: Item, style: str = "knife", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    # ---------------------------------------------------------------- Küche
    if style == "knife":
        c.fill(rrect(-W * 0.16, 0, W * 0.16, H * 0.4, W * 0.14), zone=1)
        for k in range(2):
            c.ellipse(0, H * (0.12 + k * 0.16), W * 0.05, W * 0.05, zone=3)
        blade = smooth([(-W * 0.12, H * 0.4, "s"), (W * 0.18, H * 0.4, "s"), (W * 0.1, H * 0.85), (-W * 0.12, H, "s")])
        shaded(c, blade, 3, "right", 0.9, 0.3)
    elif style == "woodspoon":
        c.fill(rrect(-W * 0.1, 0, W * 0.1, H * 0.7, W * 0.1), zone=1)
        c.fill(ell(0, H * 0.82, W * 0.45, H * 0.17, 32), zone=1)
        c.fill(ell(0, H * 0.83, W * 0.3, H * 0.11, 24), zone=1, shade=0.82)
    elif style == "rolling_pin":
        body = rrect(-W * 0.36, 0, W * 0.36, H, H * 0.45)
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.36 - (W * 0.14 if sx > 0 else 0) + (0 if sx > 0 else -W * 0.14 + W * 0.14), H * 0.25,
                         sx * W * 0.5 if sx > 0 else -W * 0.36, H * 0.75, H * 0.2), zone=2)
    elif style == "teapot":
        c.line(smooth([(W * 0.3, H * 0.62), (W * 0.48, H * 0.55), (W * 0.35, H * 0.22)], closed=False), 1.4, zone=1)
        c.fill(smooth([(-W * 0.3, H * 0.35), (-W * 0.5, H * 0.62), (-W * 0.44, H * 0.66), (-W * 0.26, H * 0.52)]), zone=1)
        body = ell(0, H * 0.4, W * 0.34, H * 0.36, 48)
        shaded(c, body, 1, "right", SHADE, 0.3)
        c.fill(ell(0, H * 0.4, W * 0.34, H * 0.08, 32), zone=2, clip=c.mask(body))
        c.fill(trap(-W * 0.18, W * 0.18, H * 0.72, -W * 0.12, W * 0.12, H * 0.84, 0.5), zone=1, shade=0.95)
        knob(c, 0, H * 0.9, 1.4, zone=2)
    elif style == "tray":
        c.fill(trap(x0, x1, 0, x0 + 2, x1 - 2, H, 0.8), zone=1)
        c.fill(rrect(x0 + 3, H * 0.4, x1 - 3, H * 0.7, 0.4), zone=1, shade=0.8)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.42 - 2, H * 0.3, sx * W * 0.42 + 2, H * 0.75, 0.6), zone=2)
    elif style == "breadbox":
        body = smooth([(x0, 0, "s"), (x1, 0, "s"), (x1, H * 0.55), (W * 0.3, H), (-W * 0.3, H), (x0, H * 0.55)])
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.line(smooth([(x0 + 3, H * 0.5), (-W * 0.26, H * 0.92), (W * 0.26, H * 0.92), (x1 - 3, H * 0.5)], closed=False), INNER, zone=0)
        c.fill(rrect(-W * 0.12, H * 0.5, W * 0.12, H * 0.58, 1), zone=3)
        if state == "open":
            c.fill(ell(0, H * 0.35, W * 0.3, H * 0.22, 32), zone=2)
    elif style == "fruit_bowl":
        for k, (x, y, r, z) in enumerate(((-W * 0.2, H * 0.62, W * 0.16, 2), (W * 0.15, H * 0.66, W * 0.15, 3), (0, H * 0.78, W * 0.14, 2))):
            c.fill(ell(x, y, r, r, 32), zone=z, shade=1.0 - 0.05 * k)
            c.line(ell(x, y, r, r, 32), INNER, zone=0, closed=True)
        c.fill(smooth([(W * 0.22, H * 0.7), (W * 0.46, H * 0.9), (W * 0.42, H * 0.95), (W * 0.18, H * 0.78)]), zone=2, shade=1.2)
        bowl = smooth([(x0, H * 0.6, "s"), (x1, H * 0.6, "s"), (W * 0.3, H * 0.12), (0, 0), (-W * 0.3, H * 0.12)])
        shaded(c, bowl, 1, "bottom", SHADE, 0.35)
    elif style == "spice_rack":
        c.fill(rrect(x0, 0, x1, H * 0.1, 0.6), zone=3)
        c.fill(rrect(x0, H * 0.5, x1, H * 0.58, 0.6), zone=3)
        for sx in (-1, 1):
            c.fill(rrect(sx * W / 2 - (2 if sx > 0 else 0), 0, sx * W / 2 + (0 if sx > 0 else 2), H * 0.95, 0.5), zone=3)
        for row, y in enumerate((H * 0.1, H * 0.58)):
            for k in range(4):
                x = x0 + 4 + k * (W - 8) / 4
                c.fill(rrect(x, y, x + (W - 8) / 4 - 2, y + H * 0.32, 0.8), zone=1, shade=1.1, alpha=0.9)
                c.fill(rrect(x, y + H * 0.28, x + (W - 8) / 4 - 2, y + H * 0.36, 0.5), zone=2 if (k + row) % 2 else 1)
                c.fill(rrect(x + 1, y + H * 0.08, x + (W - 8) / 4 - 3, y + H * 0.18, 0.3), zone=[2, 3][k % 2], shade=0.9)
    elif style == "trash":
        can = trap(x0 + 2, x1 - 2, 0, x0, x1, H * 0.88, 1.5)
        shaded(c, can, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 - 1, H * 0.86, x1 + 1, H * 0.94, 1.5), zone=1, shade=0.94)
        c.fill(ell(0, H * 0.96, W * 0.2, H * 0.05, 20), zone=3)
        c.fill(rrect(-W * 0.3, H * 0.06, -W * 0.12, H * 0.1, 0.6), zone=3)
    elif style == "dish_rack":
        c.fill(rrect(x0, 0, x1, H * 0.12, 1), zone=3)
        for k in range(5):
            x = x0 + 5 + k * (W - 10) / 4
            c.line([(x, H * 0.1), (x, H * 0.5)], 0.6, zone=3)
        for k in range(3):
            x = x0 + 8 + k * 8
            c.fill(ell(x, H * 0.55, 3, H * 0.42, 24), zone=1, shade=1.0 - k * 0.04)
            c.line(ell(x, H * 0.55, 3, H * 0.42, 24), INNER, zone=0, closed=True)
        c.fill(rrect(W * 0.12, H * 0.1, W * 0.34, H * 0.55, 1.5), zone=2, alpha=0.8)
    elif style == "baking_tray":
        c.fill(trap(x0, x1, 0, x0 + 1.5, x1 - 1.5, H, 0.6), zone=3)
        for k in range(4):
            c.fill(ell(x0 + 6 + k * (W - 12) / 3, H * 0.9, 3, 1.4, 16), zone=1)
    elif style == "scale":
        c.fill(rrect(x0, 0, x1, H * 0.5, 2), zone=1)
        c.fill(rrect(-W * 0.25, H * 0.12, W * 0.25, H * 0.36, 1), zone=2)
        c.line(rrect(-W * 0.25, H * 0.12, W * 0.25, H * 0.36, 1), INNER, zone=0, closed=True)
        c.fill(ell(0, H * 0.72, W * 0.45, H * 0.26, 32), zone=3)
        c.fill(ell(0, H * 0.72, W * 0.3, H * 0.14, 32), zone=3, shade=0.8)
    elif style == "salt_pepper":
        for sx, z in ((-1, 1), (1, 2)):
            x = sx * W * 0.24
            b = rrect(x - W * 0.2, 0, x + W * 0.2, H * 0.8, W * 0.12)
            shaded(c, b, z, "right", SHADE, 0.3)
            c.fill(ell(x, H * 0.86, W * 0.18, H * 0.12, 24), zone=3)
            for k in range(3):
                c.ellipse(x - 2 + k * 2, H * 0.9, 0.4, 0.4, zone=0)
    elif style == "canister":
        body = rrect(x0, 0, x1, H * 0.84, 1.5)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 - 1, H * 0.8, x1 + 1, H, 1.5), zone=3)
        c.fill(rrect(-W * 0.3, H * 0.3, W * 0.3, H * 0.55, 0.8), zone=2)
    elif style == "paper_roll":
        c.fill(rrect(-W * 0.08, 0, W * 0.08, H, 0.5), zone=3)
        c.fill(ell(0, 1, W * 0.45, 1, 20), zone=3)
        roll = rrect(-W * 0.4, H * 0.1, W * 0.4, H * 0.9, W * 0.1)
        shaded(c, roll, 1, "right", SOFT, 0.3)
        for k in range(1, 5):
            line(c, [(-W * 0.4, H * 0.1 + k * H * 0.16), (W * 0.4, H * 0.1 + k * H * 0.16)], zone=2, shade=0.9)
    elif style == "sieve":
        c.fill(rrect(W * 0.3, H * 0.6, W / 2, H * 0.7, 0.6), zone=3)
        bowl = smooth([(-W * 0.35, H * 0.7, "s"), (W * 0.32, H * 0.7, "s"), (W * 0.15, 0), (-W * 0.18, 0)])
        c.fill(bowl, zone=1)
        cl = c.mask(bowl)
        for k in range(8):
            line(c, [(-W * 0.3 + k * W * 0.08, 0), (-W * 0.3 + k * W * 0.08, H * 0.7)], zone=1, clip=cl, shade=0.72)
            line(c, [(-W * 0.4, k * H * 0.1), (W * 0.4, k * H * 0.1)], zone=1, clip=cl, shade=0.72)
        c.line(bowl, INNER, zone=0, closed=True)
    # ---------------------------------------------------------------- Bad
    elif style == "cup":
        body = trap(-W * 0.36, W * 0.36, 0, x0, x1, H, 1)
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.line([(-W * 0.12, H * 0.5), (-W * 0.04, H * 1.5)], 1.0, zone=2)
        c.line([(W * 0.1, H * 0.5), (W * 0.18, H * 1.45)], 1.0, zone=3)
    elif style == "bath_scale":
        body = rrect(x0, 0, x1, H, 2)
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(-W * 0.15, H * 0.3, W * 0.15, H * 0.75, 0.6), zone=2)
    elif style == "potty":
        body = smooth([(x0, H * 0.7, "s"), (x1, H * 0.7, "s"), (W * 0.36, H * 0.12), (W * 0.2, 0), (-W * 0.2, 0), (-W * 0.36, H * 0.12)])
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(rrect(x0 - 1, H * 0.66, x1 + 1, H * 0.78, 2), zone=2)
        c.fill(smooth([(W * 0.3, H * 0.75), (W * 0.35, H), (W * 0.48, H * 0.95), (W * 0.46, H * 0.72)]), zone=2)
    elif style == "robe":
        robe = smooth([(-W * 0.16, H, "s"), (W * 0.16, H, "s"), (W * 0.42, H * 0.82), (x1, H * 0.5), (W * 0.36, H * 0.46), (W * 0.36, 0, "s"),
                       (-W * 0.36, 0, "s"), (-W * 0.36, H * 0.46), (x0, H * 0.5), (-W * 0.42, H * 0.82)])
        shaded(c, robe, 1, "right", SHADE, 0.25)
        c.fill([(-W * 0.14, H), (W * 0.14, H), (0, H * 0.55)], zone=2)
        c.fill(rrect(-W * 0.38, H * 0.44, W * 0.38, H * 0.5, 1), zone=2)
        c.fill(rrect(x0 - 1, 0, -W * 0.02, H * 0.06, 0.5), zone=0, alpha=0.0)
    elif style == "sponge":
        body = rrect(x0, 0, x1, H, 2)
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(x0, H * 0.7, x1, H, 1.5), zone=2)
        for k in range(6):
            c.ellipse(x0 + 3 + k * W * 0.16, H * (0.25 + (k % 2) * 0.2), 0.8, 0.8, zone=1, shade=0.7)
    # ---------------------------------------------------------------- Bettzeug & Wohnen
    elif style == "duvet":                                       # zusammengelegte Bettdecke
        for k in range(3):
            y = k * H / 3
            fold = rrect(x0 + k * 1.5, y, x1 - k * 1.5, y + H / 3 + 1.5, H * 0.16)
            shaded(c, fold, 1, "bottom", SHADE, 0.35)
            if k == 1:
                for j in range(6):
                    c.ellipse(x0 + 6 + j * (W - 12) / 5, y + H / 6, 1.4, 1.4, zone=2)
            elif k == 2:
                c.fill(rrect(x0 + k * 1.5, y + H * 0.12, x1 - k * 1.5, y + H * 0.2, 0.8), zone=2)
    elif style == "pillow":
        body = smooth([(x0, H * 0.2), (0, 0), (x1, H * 0.2), (x1 - 2, H * 0.8), (0, H), (x0 + 2, H * 0.8)])
        shaded(c, body, 1, "bottom", SOFT, 0.3)
        c.line(smooth([(x0 + 5, H * 0.45), (0, H * 0.4), (x1 - 5, H * 0.45)], closed=False), INNER, zone=1, shade=0.8)
        c.fill(rrect(x0 + 4, H * 0.2, x1 - 4, H * 0.3, 1), zone=2, alpha=0.6)
    elif style == "throw":                                       # zusammengelegte Kuscheldecke mit Fransen
        body = rrect(x0, 0, x1, H, 2)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        for k in range(0, int(W / 6)):
            c.fill([(x0 + k * 6, 0), (x0 + k * 6 + 3, 0), (x0 + k * 6 + 3, H), (x0 + k * 6, H)], zone=2, clip=cl)
        for k in range(int(H / 2.2)):
            c.line([(x1, k * 2.2 + 1), (x1 + 3, k * 2.2 + 0.6)], 0.5, zone=2)
    elif style == "magazines":
        for k in range(4):
            y = k * H / 4
            c.fill(rrect(x0 + (k % 2) * 2, y, x1 - (k % 2) * 3, y + H / 4 - 0.3, 0.3), zone=[1, 2, 3, 1][k])
            c.line(rrect(x0 + (k % 2) * 2, y, x1 - (k % 2) * 3, y + H / 4 - 0.3, 0.3), INNER, zone=0, closed=True)
    elif style == "speaker":
        body = rrect(x0, 0, x1, H, 2)
        shaded(c, body, 1, "right", SHADE, 0.15)
        for y, r in ((H * 0.3, W * 0.3), (H * 0.75, W * 0.18)):
            c.fill(ell(0, y, r, r, 32), zone=2)
            c.fill(ell(0, y, r * 0.4, r * 0.4, 20), zone=3)
            c.line(ell(0, y, r, r, 32), INNER, zone=0, closed=True)
        if state == "on":
            for k in range(2):
                a = [(x1 + 2 + k * 3, H * 0.4), (x1 + 4 + k * 3, H * 0.55), (x1 + 2 + k * 3, H * 0.7)]
                c.line(smooth(a, closed=False), 0.6, zone=2)
    elif style == "remote":
        body = rrect(x0, 0, x1, H, W * 0.4)
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.ellipse(0, H * 0.85, W * 0.2, W * 0.2, zone=2)
        for k in range(3):
            for j in range(2):
                c.ellipse(-W * 0.18 + j * W * 0.36, H * (0.2 + k * 0.17), W * 0.12, W * 0.1, zone=3)
    elif style == "alarm":
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.3, H * 0.9, W * 0.16, H * 0.1, 20), zone=2)
            c.line([(sx * W * 0.34, 0), (sx * W * 0.2, H * 0.2)], 1.0, zone=3)
        face = ell(0, H * 0.48, W * 0.44, H * 0.42, 48)
        shaded(c, face, 1, "bottom", SHADE, 0.25)
        c.fill(ell(0, H * 0.48, W * 0.32, H * 0.3, 40), zone=2, shade=1.25)
        c.line([(0, H * 0.48), (0, H * 0.7)], 0.8, zone=0)
        c.line([(0, H * 0.48), (W * 0.14, H * 0.48)], 0.8, zone=0)
    elif style == "nightlight":
        base = rrect(-W * 0.3, 0, W * 0.3, H * 0.18, 1.5)
        c.fill(base, zone=3)
        body = ell(0, H * 0.55, W * 0.42, H * 0.42, 48) if state != "moon" else ell(0, H * 0.55, W * 0.42, H * 0.42, 48)
        if state == "on":
            c.glass(ell(0, H * 0.55, W * 0.9, H * 0.8, 40), zone=1, opacity=0.25)
        shaded(c, body, 1, "bottom", 0.98 if state == "on" else SHADE, 0.25)
        c.fill(ell(-W * 0.12, H * 0.58, W * 0.06, H * 0.07, 16), zone=0)
        c.fill(ell(W * 0.12, H * 0.58, W * 0.06, H * 0.07, 16), zone=0)
        c.line(smooth([(-W * 0.1, H * 0.44), (0, H * 0.38), (W * 0.1, H * 0.44)], closed=False), 0.5, zone=0)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.26, H * 0.46, W * 0.07, H * 0.04, 12), zone=2, alpha=0.8)
    elif style == "key_board":
        board = rrect(x0, 0, x1, H, 2)
        shaded(c, board, 1, "bottom", SHADE, 0.25)
        for k in range(4):
            x = x0 + 6 + k * (W - 12) / 3
            c.fill(ell(x, H * 0.7, 1, 1, 12), zone=3)
            c.line([(x, H * 0.7), (x, H * 0.4)], 0.5, zone=3)
            c.fill(rrect(x - 1.8, H * 0.18, x + 1.8, H * 0.42, 0.8), zone=[2, 3][k % 2])
    elif style == "suitcase":
        c.line(smooth([(-W * 0.18, H * 0.9), (-W * 0.18, H), (W * 0.18, H), (W * 0.18, H * 0.9)], closed=False), 1.8, zone=3)
        body = rrect(x0, 0, x1, H * 0.9, 3)
        cl = shaded(c, body, 1, "right", SHADE, 0.15)
        for x in (-W * 0.28, W * 0.28):
            c.fill(rrect(x - 2, 0, x + 2, H * 0.9, 0.8), zone=2, clip=cl)
        c.fill(ell(-W * 0.1, H * 0.5, W * 0.12, W * 0.08, 20), zone=2, shade=1.1)
    elif style == "umbrella":                                    # zusammengerollter Regenschirm (stehend)
        c.line(smooth([(0, H * 0.05), (-W * 0.3, 0), (-W * 0.45, H * 0.08)], closed=False), 1.4, zone=3)
        c.line([(0, H * 0.05), (0, H)], 1.0, zone=3)
        body = smooth([(0, H * 0.18, "s"), (W * 0.36, H * 0.8), (0, H * 0.95, "s"), (-W * 0.32, H * 0.8)])
        shaded(c, body, 1, "right", SHADE, 0.35)
        c.fill(rrect(-W * 0.3, H * 0.62, W * 0.32, H * 0.67, 0.8), zone=2)
    elif style == "umbrella_stand":
        body = trap(x0 + 2, x1 - 2, 0, x0, x1, H * 0.7, 1.5)
        shaded(c, body, 1, "right", SHADE, 0.2)
        for k, (x, z) in enumerate(((-W * 0.2, 2), (W * 0.15, 3))):
            c.line([(x, H * 0.6), (x + k * 3, H)], 1.4, zone=z)
            c.line(smooth([(x + k * 3, H), (x + k * 3 + 5, H * 1.02), (x + k * 3 + 6, H * 0.94)], closed=False), 1.2, zone=z)
        c.fill(rrect(x0 - 1, H * 0.66, x1 + 1, H * 0.72, 1), zone=1, shade=0.9)
    elif style == "mirror":                                       # Wandspiegel oval
        frame = ell(0, H / 2, W / 2, H / 2, 64)
        c.fill(frame, zone=1)
        glass = ell(0, H / 2, W / 2 - 3, H / 2 - 3, 64)
        c.fill(glass, zone=2, shade=1.12)
        cl = c.mask(glass)
        c.fill([(-W * 0.3, H * 0.9), (-W * 0.1, H * 0.9), (-W * 0.3, H * 0.2), (-W * 0.5, H * 0.2)], zone=2, shade=1.35, alpha=0.6, clip=cl)
        c.line(glass, INNER, zone=0, closed=True)
    elif style == "mirror_stand":
        for sx in (-1, 1):
            c.line([(sx * W * 0.4, 0), (sx * W * 0.3, H * 0.4)], 1.6, zone=3)
        frame = rrect(-W * 0.36, H * 0.12, W * 0.36, H, W * 0.3)
        c.fill(frame, zone=1)
        glass = rrect(-W * 0.3, H * 0.15, W * 0.3, H * 0.97, W * 0.26)
        c.fill(glass, zone=2, shade=1.12)
        c.fill([(-W * 0.2, H * 0.9), (-W * 0.05, H * 0.9), (-W * 0.2, H * 0.3), (-W * 0.3, H * 0.3)], zone=2, shade=1.35, alpha=0.6,
               clip=c.mask(glass))
        c.line(glass, INNER, zone=0, closed=True)
    elif style == "light_switch":                                 # Lichtschalter (Wand): Wippe oben = an
        plate = rrect(x0, 0, x1, H, 1.2)
        shaded(c, plate, 1, "bottom", SOFT, 0.2)
        rock = rrect(-W * 0.26, H * 0.2, W * 0.26, H * 0.8, 0.8)
        c.fill(rock, zone=2)
        c.fill(rrect(-W * 0.26, H * 0.5, W * 0.26, H * 0.8, 0.8) if state != "off" else rrect(-W * 0.26, H * 0.2, W * 0.26, H * 0.5, 0.8),
               zone=2, shade=0.82)
        c.line(rock, INNER, zone=0, closed=True)
        c.ellipse(0, H * (0.68 if state != "off" else 0.32), W * 0.07, W * 0.07, zone=3, shade=1.2 if state != "off" else 0.6)
    # ---------------------------------------------------------------- Baby
    elif style == "rattle":
        c.fill(rrect(-W * 0.1, 0, W * 0.1, H * 0.55, W * 0.1), zone=2)
        head = ell(0, H * 0.75, W * 0.45, H * 0.25, 32)
        shaded(c, head, 1, "bottom", SHADE, 0.3)
        for k in range(3):
            c.ellipse(-W * 0.2 + k * W * 0.2, H * 0.78, W * 0.06, W * 0.06, zone=3)
    elif style == "baby_bottle":
        c.fill(smooth([(-W * 0.18, H * 0.82), (W * 0.18, H * 0.82), (W * 0.08, H), (-W * 0.08, H)]), zone=3, shade=1.1)
        c.fill(rrect(-W * 0.44, H * 0.72, W * 0.44, H * 0.84, 1), zone=2)
        body = rrect(-W * 0.4, 0, W * 0.4, H * 0.74, W * 0.25)
        c.glass(body, zone=1, opacity=0.55)
        c.fill(rrect(-W * 0.38, 0, W * 0.38, H * 0.45, W * 0.22), zone=2, shade=1.3, clip=c.mask(body))
        c.line(body, INNER, zone=0, closed=True)
    elif style == "pacifier":
        c.line(ell(0, H * 0.75, W * 0.2, H * 0.18, 24), 1.2, zone=3, closed=True)
        shield = smooth([(x0, H * 0.4), (0, H * 0.62), (x1, H * 0.4), (0, H * 0.18)])
        shaded(c, shield, 1, "bottom", SHADE, 0.3)
        c.fill(ell(0, H * 0.12, W * 0.16, H * 0.14, 20), zone=2)
    # ---------------------------------------------------------------- Kleidung (liegend/hängend dargestellt)
    elif style == "shirt":
        pts = smooth([(-W * 0.28, 0, "s"), (W * 0.28, 0, "s"), (W * 0.28, H * 0.6, "s"), (W * 0.46, H * 0.52, "s"), (x1, H * 0.78, "s"),
                      (W * 0.2, H, "s"), (-W * 0.2, H, "s"), (x0, H * 0.78, "s"), (-W * 0.46, H * 0.52, "s"), (-W * 0.28, H * 0.6, "s")], n=3)
        shaded(c, pts, 1, "right", SHADE, 0.25)
        c.fill(smooth([(-W * 0.14, H), (0, H * 0.82), (W * 0.14, H)]), zone=2)
        c.fill(ell(0, H * 0.4, W * 0.12, W * 0.12, 20), zone=2)
    elif style == "pants":
        pts = smooth([(-W * 0.4, H, "s"), (W * 0.4, H, "s"), (x1, 0, "s"), (W * 0.08, 0, "s"), (0, H * 0.65), (-W * 0.08, 0, "s"), (x0, 0, "s")], n=3)
        shaded(c, pts, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W * 0.4, H * 0.9, W * 0.4, H, 0.5), zone=2)
    elif style == "dress":
        pts = smooth([(-W * 0.2, H, "s"), (W * 0.2, H, "s"), (W * 0.18, H * 0.62), (x1, 0, "s"), (x0, 0, "s"), (-W * 0.18, H * 0.62)])
        shaded(c, pts, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W * 0.2, H * 0.58, W * 0.2, H * 0.66, 1), zone=2)
        for k in range(5):
            c.ellipse(-W * 0.3 + k * W * 0.15, H * 0.25, 1.5, 1.5, zone=2)
    elif style == "jacket":
        pts = smooth([(-W * 0.3, 0, "s"), (W * 0.3, 0, "s"), (W * 0.3, H * 0.62, "s"), (W * 0.46, H * 0.1, "s"), (x1, H * 0.12, "s"),
                      (W * 0.42, H * 0.85, "s"), (W * 0.18, H, "s"), (-W * 0.18, H, "s"), (-W * 0.42, H * 0.85, "s"), (x0, H * 0.12, "s"),
                      (-W * 0.46, H * 0.1, "s"), (-W * 0.3, H * 0.62, "s")], n=3)
        shaded(c, pts, 1, "right", SHADE, 0.25)
        c.line([(0, 0), (0, H * 0.95)], 0.6, zone=3)
        c.fill(smooth([(-W * 0.2, H), (0, H * 0.88), (W * 0.2, H), (0, H * 1.08)]), zone=2)
    elif style in ("shoes", "slippers", "boots"):
        for dx, sh in ((W * 0.08, 0.86), (-W * 0.06, 1.0)):
            if style == "boots":
                shoe = smooth([(x0 * 0.9 + dx, 0, "s"), (W * 0.38 + dx, 0, "s"), (W * 0.4 + dx, H * 0.22), (W * 0.02 + dx, H * 0.3),
                               (W * 0.02 + dx, H, "s"), (-W * 0.3 + dx, H, "s")])
            else:
                shoe = smooth([(x0 * 0.9 + dx, 0, "s"), (W * 0.42 + dx, 0, "s"), (W * 0.44 + dx, H * 0.35), (W * 0.1 + dx, H * 0.6),
                               (-W * 0.22 + dx, H * 0.75), (-W * 0.44 + dx, H * 0.55)])
            shaded(c, shoe, 1, "bottom", SHADE * sh, 0.3)
            c.fill(rrect(x0 * 0.9 + dx, 0, W * 0.42 + dx, H * 0.08, 1), zone=2, shade=sh)
            if style == "slippers":
                c.fill(ell(W * 0.1 + dx, H * 0.55, W * 0.12, H * 0.16, 20), zone=2, shade=sh)
            elif style == "shoes":
                for k in range(3):
                    c.line([(-W * 0.1 + k * W * 0.06 + dx, H * (0.62 - k * 0.08)), (W * 0.02 + k * W * 0.06 + dx, H * (0.58 - k * 0.08))], 0.5,
                           zone=3)
    elif style == "hat":
        c.fill(ell(0, H * 0.18, W / 2, H * 0.18, 40), zone=1, shade=0.9)
        crown = smooth([(-W * 0.3, H * 0.2, "s"), (W * 0.3, H * 0.2, "s"), (W * 0.26, H * 0.85), (0, H), (-W * 0.26, H * 0.85)])
        shaded(c, crown, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W * 0.3, H * 0.2, W * 0.3, H * 0.34, 1), zone=2)
