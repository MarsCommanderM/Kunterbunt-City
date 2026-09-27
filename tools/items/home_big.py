"""
Große Einrichtung fürs Zuhause (P07-Inventar): Ecksofa, Kamin, Klavier, Schminktisch, Garderobe, Treppe,
Hochstuhl, Kinderwagen, Matratze, Kratzbaum, Großgeräte (Spülmaschine, Trockner, Gefriertruhe, Dunstabzug),
Drucker, Grammophon, Wäscheständer, Bügelbrett, Staubsauger, Bad (Wanne, Dusche, Toilette, Waschbecken), Autos.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe (Polster, Glas, Fronten) · 3 = Holz/Metall/Details.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, cushion, ell, knob, leg, line, rrect, shaded, smooth, trap


def big(it: Item, style: str = "sofa_corner", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "sofa_corner":                                   # Ecksofa: lange Seite + Ottomane rechts vorn
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 6), 0, 7, 3, 2.4)
        c.fill(rrect(x0, 6, x1, H * 0.5, 4), zone=1, shade=0.9)
        cushion(c, x0 + 4, H * 0.48, x1 - 4, H, zone=1)
        for k in range(3):
            a = x0 + 12 + k * (W * 0.62 - 12) / 3
            cushion(c, a, H * 0.32, a + (W * 0.62 - 12) / 3 - 2, H * 0.55, zone=1)
        chaise = rrect(x1 - W * 0.36, 4, x1, H * 0.46, 5)
        shaded(c, chaise, 1, "bottom", SHADE, 0.3)
        cushion(c, x1 - W * 0.34, H * 0.3, x1 - 3, H * 0.5, zone=1)
        arm = rrect(x0, 6, x0 + 14, H * 0.66, 6)
        shaded(c, arm, 1, "right", SHADE, 0.3)
        for x in (x0 + W * 0.25, x0 + W * 0.45):
            cushion(c, x - 10, H * 0.55, x + 10, H * 0.82, zone=2, r=5)
    elif style == "fireplace":
        c.fill(rrect(x0, 0, x1, H * 0.12, 1), zone=3)
        body = rrect(x0 + 4, H * 0.1, x1 - 4, H * 0.88, 1.5)
        shaded(c, body, 1, "right", SHADE, 0.12)
        for r in range(6):                                       # Steine/Ziegel
            y = H * 0.1 + r * H * 0.13
            for k in range(6):
                x = x0 + 4 + k * (W - 8) / 6 + (W / 12 if r % 2 else 0)
                c.line(rrect(x, y, x + (W - 8) / 6 - 1, y + H * 0.13 - 1, 1), INNER, zone=1, shade=0.8, closed=True)
        hole = smooth([(-W * 0.28, H * 0.12, "s"), (W * 0.28, H * 0.12, "s"), (W * 0.28, H * 0.5), (0, H * 0.6), (-W * 0.28, H * 0.5)])
        c.fill(hole, zone=0, alpha=0.9)
        if state == "on":
            c.fill(smooth([(0, H * 0.5), (W * 0.14, H * 0.26), (W * 0.1, H * 0.14), (-W * 0.1, H * 0.14), (-W * 0.14, H * 0.26)]), zone=2)
            c.fill(smooth([(0, H * 0.36), (W * 0.06, H * 0.22), (0, H * 0.15), (-W * 0.06, H * 0.22)]), zone=2, shade=1.3)
        for k in range(3):
            c.line([(-W * 0.2 + k * W * 0.08, H * 0.13), (W * 0.1 + k * W * 0.06, H * 0.17)], 2.4, zone=3, shade=0.6)
        c.fill(rrect(x0, H * 0.86, x1, H, 1.2), zone=3)            # Kaminsims
        c.line(rrect(x0, H * 0.86, x1, H, 1.2), INNER, zone=0, closed=True)
    elif style == "piano":
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 5), 0, H * 0.42, 4, 3.4, zone=1)
        body = rrect(x0, H * 0.4, x1, H, 2)
        shaded(c, body, 1, "right", SHADE, 0.1)
        c.fill(rrect(x0 - 2, H * 0.52, x1 + 2, H * 0.6, 1), zone=1, shade=0.8)
        keys = rrect(x0 + 3, H * 0.6, x1 - 3, H * 0.66, 0.5)
        c.fill(keys, zone=2)
        for k in range(int((W - 6) / 2.4)):
            x = x0 + 3 + k * 2.4
            c.line([(x, H * 0.6), (x, H * 0.66)], 0.2, zone=0)
            if k % 7 not in (2, 6):
                c.fill(rrect(x + 1.4, H * 0.63, x + 2.8, H * 0.66, 0.2), zone=0)
        c.fill(rrect(-W * 0.2, H * 0.78, W * 0.2, H * 0.9, 0.8), zone=2)          # Notenblatt
        c.line([(-W * 0.14, H * 0.82), (W * 0.1, H * 0.84)], 0.4, zone=0)
    elif style == "vanity":                                      # Schminktisch mit rundem Spiegel
        c.fill(ell(0, H * 0.78, W * 0.28, H * 0.22, 48), zone=3)
        c.fill(ell(0, H * 0.78, W * 0.23, H * 0.18, 48), zone=2, shade=1.2)
        c.fill([(-W * 0.12, H * 0.9), (-W * 0.02, H * 0.9), (-W * 0.16, H * 0.66)], zone=2, shade=1.35, alpha=0.5)
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 4), 0, H * 0.45, 3, 2.2, zone=3)
        top = rrect(x0, H * 0.42, x1, H * 0.52, 1.5)
        shaded(c, top, 1, "bottom", SHADE, 0.3)
        c.line(rrect(-W * 0.3, H * 0.44, W * 0.3, H * 0.5, 0.8), INNER, zone=1, shade=0.7, closed=True)
        knob(c, 0, H * 0.47, 1.0)
        for k, x in enumerate((-W * 0.3, -W * 0.2, W * 0.25)):
            c.fill(rrect(x - 1.5, H * 0.52, x + 1.5, H * 0.52 + 6 + k * 2, 0.8), zone=2, shade=0.9)
    elif style in ("clothes_rack", "coat_rack"):
        if style == "coat_rack":                                 # Garderobenständer rund
            c.fill(ell(0, 1.5, W * 0.3, 1.5), zone=3)
            c.fill(rrect(-1.6, 0, 1.6, H * 0.95, 1), zone=3)
            for k, (sx, y) in enumerate(((-1, 0.9), (1, 0.85), (-1, 0.72), (1, 0.66))):
                c.line([(0, H * y), (sx * W * 0.3, H * y + 5)], 1.2, zone=3)
            coat = smooth([(-W * 0.32, H * 0.88), (-W * 0.2, H * 0.9), (-W * 0.14, H * 0.4, "s"), (-W * 0.44, H * 0.4, "s")])
            shaded(c, coat, 1, "right", SHADE, 0.3)
            c.fill(ell(W * 0.3, H * 0.8, W * 0.12, W * 0.08, 24), zone=2)  # Mütze
        else:
            for sx in (-1, 1):
                c.line([(sx * W / 2, 0), (sx * W / 2, H)], 2.2, zone=3)
                c.line([(sx * (W / 2 - 8), 1), (sx * (W / 2 + 6), 1)], 2.2, zone=3)
            c.line([(x0, H - 1), (x1, H - 1)], 2.2, zone=3)
            for k in range(5):
                x = x0 + 10 + k * (W - 20) / 5
                piece = trap(x, x + (W - 20) / 5 - 3, H * 0.35 + (k % 2) * 10, x + 2, x + (W - 20) / 5 - 5, H - 6, 2)
                shaded(c, piece, [1, 2][k % 2], "right", SHADE, 0.25)
                c.line([(x + (W - 20) / 10, H - 6), (x + (W - 20) / 10, H - 1)], 0.5, zone=3)
    elif style == "stairs":                                      # Treppe nach oben (Deko, begehbar ist sie nicht)
        n = 10
        for k in range(n):
            y = H * k / n
            x = x0 + W * k / n
            step = rrect(x, 0, x1, y + H / n, 0.8)
            c.fill(step, zone=1, shade=0.92 + (k % 2) * 0.05)
            c.fill(rrect(x - 1, y + H / n - 2.5, x1, y + H / n, 0.6), zone=3)
            c.line(step, INNER, zone=0, closed=True)
        for k in range(0, n, 2):                                  # Geländer
            x = x0 + W * k / n + 4
            c.line([(x, H * k / n + H / n), (x, H * k / n + H / n + 60)], 1.2, zone=3)
        c.line([(x0 + 4, H / n + 60), (x1 - W / n + 4, H + 60 - H / n)], 2.4, zone=3)
    elif style == "highchair":
        for sx in (-1, 1):
            c.line([(sx * W * 0.45, 0), (sx * W * 0.22, H * 0.55)], 2.4, zone=3)
        c.line([(-W * 0.38, H * 0.22), (W * 0.38, H * 0.22)], 1.8, zone=3)
        seat = rrect(-W * 0.3, H * 0.5, W * 0.3, H * 0.62, 2)
        shaded(c, seat, 1, "bottom", SHADE, 0.3)
        back = rrect(-W * 0.26, H * 0.58, W * 0.26, H, 4)
        shaded(c, back, 1, "right", SHADE, 0.2)
        tray = rrect(-W * 0.5, H * 0.66, W * 0.1, H * 0.72, 1.5)
        c.fill(tray, zone=2)
        c.line(tray, INNER, zone=0, closed=True)
    elif style == "stroller":
        for x in (-W * 0.3, W * 0.25):
            c.fill(ell(x, H * 0.1, H * 0.1, H * 0.1, 32), zone=3, shade=0.6)
            c.fill(ell(x, H * 0.1, H * 0.04, H * 0.04, 16), zone=3)
        c.line([(-W * 0.3, H * 0.1), (0, H * 0.4), (W * 0.25, H * 0.1)], 1.4, zone=3)
        c.line([(W * 0.2, H * 0.45), (W * 0.48, H), (W * 0.36, H)], 1.6, zone=3)
        basket = smooth([(-W * 0.42, H * 0.7), (W * 0.3, H * 0.7), (W * 0.26, H * 0.38), (-W * 0.38, H * 0.38)])
        shaded(c, basket, 1, "bottom", SHADE, 0.35)
        hood = smooth([(-W * 0.44, H * 0.7, "s"), (-W * 0.02, H * 0.7, "s"), (-W * 0.1, H * 0.95), (-W * 0.36, H * 0.95)])
        shaded(c, hood, 2, "right", SHADE, 0.3)
        for k in range(1, 3):
            line(c, [(-W * 0.44 + k * W * 0.14, H * 0.7), (-W * 0.36 + k * W * 0.1, H * 0.94)], zone=2, shade=0.75)
    elif style == "mattress":
        body = rrect(x0, 0, x1, H, H * 0.4)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        for k in range(1, 10):
            x = x0 + W * k / 10
            c.ellipse(x, H * 0.55, 0.9, 0.9, zone=1, shade=0.7, clip=cl)
        c.line([(x0 + 3, H * 0.22), (x1 - 3, H * 0.22)], 0.4, zone=2, clip=cl)
    elif style == "cat_tree":
        c.fill(rrect(x0, 0, x1, H * 0.08, 2), zone=2)
        for x, y0, y1 in ((-W * 0.2, H * 0.08, H * 0.62), (W * 0.18, H * 0.08, H * 0.4), (W * 0.1, H * 0.62, H * 0.9)):
            post = rrect(x - 3.5, y0, x + 3.5, y1, 1.5)
            c.fill(post, zone=3)
            for k in range(int((y1 - y0) / 3)):
                c.line([(x - 3.5, y0 + k * 3), (x + 3.5, y0 + k * 3 + 1.2)], 0.4, zone=3, shade=0.75)
            c.line(post, INNER, zone=0, closed=True)
        for (a, b, y) in ((-W * 0.46, W * 0.02, H * 0.6), (W * 0.02, W * 0.46, H * 0.38), (-W * 0.1, W * 0.34, H * 0.88)):
            pad = rrect(a, y, b, y + H * 0.06, 2.5)
            shaded(c, pad, 2, "bottom", SHADE, 0.35)
        c.fill(ell(-W * 0.22, H * 0.7, W * 0.2, H * 0.08, 32), zone=2)          # Höhle
        c.fill(ell(-W * 0.22, H * 0.69, W * 0.1, H * 0.05, 24), zone=0, alpha=0.8)
        c.line([(W * 0.3, H * 0.38), (W * 0.3, H * 0.28)], 0.5, zone=3)
        c.ellipse(W * 0.3, H * 0.27, 2, 2, zone=2, shade=0.8)
    elif style in ("dishwasher", "dryer", "freezer"):
        body = rrect(x0, 0, x1, H, 2)
        cl = shaded(c, body, 1, "right", SHADE, 0.1)
        c.fill(rrect(x0 + 2, H * 0.84, x1 - 2, H - 2, 1), zone=1, shade=0.93)
        c.ellipse(x1 - 8, H * 0.91, 1.8, 1.8, zone=2)
        if style == "dishwasher":
            c.fill(rrect(x0 + 6, H * 0.74, x1 - 6, H * 0.78, 1), zone=3)
            if state == "on":
                c.fill(ell(x1 - 14, H * 0.91, 1.2, 1.2, 12), zone=2, shade=1.3)
        elif style == "dryer":
            c.fill(ell(0, H * 0.45, W * 0.32, W * 0.32, 48), zone=3, shade=0.9)
            win = ell(0, H * 0.45, W * 0.24, W * 0.24, 48)
            c.fill(win, zone=2, shade=0.6 if state != "on" else 0.8)
            if state == "on":
                for k in range(3):
                    a = k * 2.1 + 0.5
                    c.fill(ell(W * 0.12 * math.cos(a), H * 0.45 + W * 0.12 * math.sin(a), 3.5, 2.5, 16), zone=2, shade=1.2, clip=c.mask(win))
            c.line(win, INNER, zone=0, closed=True)
        else:                                                    # Gefriertruhe (quer, Deckel oben)
            c.fill(rrect(x0 - 1, H * 0.86, x1 + 1, H, 2), zone=1, shade=1.03)
            c.fill(rrect(-W * 0.12, H * 0.8, W * 0.12, H * 0.86, 1), zone=3)
            for k in range(3):
                c.fill(ell(x0 + 8 + k * 5, H * 0.08, 1.5, 1.5, 12), zone=3, shade=0.7)
    elif style == "hood":                                        # Dunstabzugshaube (hängt an der Wand)
        c.fill(rrect(-W * 0.14, H * 0.45, W * 0.14, H, 1), zone=1, shade=0.95)
        body = trap(x0, x1, 0, -W * 0.18, W * 0.18, H * 0.5, 1.5)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 + 1, 0, x1 - 1, H * 0.1, 1), zone=3)
        for k in range(2):
            c.ellipse(x0 + 10 + k * 7, H * 0.05, 1.4, 1.4, zone=2, shade=1.2 if state == "on" else 0.7)
        if state == "on":
            c.glass(smooth([(x0 + 4, 0, "s"), (x1 - 4, 0, "s"), (x1 + 6, -H * 0.8, "s"), (x0 - 6, -H * 0.8, "s")], n=2), zone=2, opacity=0.2)
    elif style == "printer":
        body = rrect(x0, 0, x1, H * 0.7, 2)
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(trap(-W * 0.3, W * 0.3, H * 0.66, -W * 0.26, W * 0.26, H, 0.5), zone=2, shade=1.2)
        c.fill(rrect(-W * 0.34, H * 0.18, W * 0.34, H * 0.26, 0.6), zone=1, shade=0.7)
        c.fill(rrect(-W * 0.28, H * 0.05, W * 0.28, H * 0.2, 0.4), zone=2, shade=1.2)
        c.ellipse(W * 0.36, H * 0.52, 1.2, 1.2, zone=3)
    elif style == "gramophone":
        box = rrect(x0, 0, x1, H * 0.3, 1.5)
        shaded(c, box, 1, "right", SHADE, 0.2)
        c.fill(ell(-W * 0.1, H * 0.31, W * 0.3, 1.2, 24), zone=0, alpha=0.9)
        c.line([(W * 0.2, H * 0.3), (W * 0.24, H * 0.55), (W * 0.05, H * 0.62)], 1.6, zone=3)
        horn = smooth([(W * 0.02, H * 0.6, "s"), (-W * 0.5, H * 0.8), (-W * 0.36, H, "s"), (W * 0.08, H * 0.66, "s")])
        shaded(c, horn, 2, "bottom", SHADE, 0.3)
        c.fill(ell(-W * 0.43, H * 0.9, W * 0.08, H * 0.1, 24), zone=2, shade=0.6)
    elif style == "drying_rack":
        for sx in (-1, 1):
            c.line([(sx * W * 0.45, 0), (sx * W * 0.1, H)], 1.4, zone=3)
            c.line([(sx * W * 0.1, 0), (sx * W * 0.45, H)], 1.4, zone=3)
        for k in range(4):
            y = H * (0.55 + k * 0.12)
            c.line([(-W * 0.4, y), (W * 0.4, y)], 0.8, zone=3)
        for k, (x, z) in enumerate(((-W * 0.3, 1), (-W * 0.05, 2), (W * 0.22, 1))):
            sock = smooth([(x - 4, H * 0.91), (x + 4, H * 0.91), (x + 4, H * 0.6), (x + 9, H * 0.52), (x + 7, H * 0.46), (x - 4, H * 0.52)]) \
                if k == 1 else rrect(x - 7, H * 0.55, x + 7, H * 0.91, 2)
            shaded(c, sock, z, "right", SHADE, 0.3)
    elif style == "ironing_board":
        c.line([(-W * 0.3, 0), (W * 0.2, H * 0.92)], 1.4, zone=3)
        c.line([(W * 0.3, 0), (-W * 0.2, H * 0.92)], 1.4, zone=3)
        board = smooth([(x0, H * 0.92, "s"), (W * 0.32, H * 0.92), (x1, H * 0.96), (W * 0.32, H), (x0, H, "s")])
        shaded(c, board, 1, "bottom", SHADE, 0.3)
        cl = c.mask(board)
        for k in range(8):
            c.ellipse(x0 + 10 + k * W * 0.1, H * 0.96, 1.2, 0.8, zone=2, clip=cl)
    elif style == "vacuum":
        c.fill(ell(-W * 0.2, H * 0.12, W * 0.14, H * 0.1, 24), zone=3, shade=0.6)
        body = smooth([(-W * 0.45, H * 0.08), (-W * 0.44, H * 0.34), (-W * 0.1, H * 0.4), (W * 0.02, H * 0.1)])
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.line(smooth([(-W * 0.1, H * 0.3), (W * 0.1, H * 0.5), (W * 0.2, H * 0.95)], closed=False), 1.6, zone=2)
        c.line([(W * 0.2, H * 0.95), (W * 0.38, 0.8)], 1.8, zone=3)
        c.fill(rrect(W * 0.28, 0, W * 0.5, 3, 1), zone=3, shade=0.7)
    elif style == "tub":                                         # Badewanne auf Füßen
        for sx in (-1, 1):
            c.fill(smooth([(sx * W * 0.36, H * 0.12), (sx * W * 0.42, 0), (sx * W * 0.32, 0)]), zone=3)
        tub = smooth([(x0, H, "s"), (x1, H, "s"), (W * 0.44, H * 0.3), (W * 0.3, H * 0.08), (-W * 0.3, H * 0.08), (-W * 0.44, H * 0.3)])
        shaded(c, tub, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(x0 - 1, H * 0.92, x1 + 1, H + 1.5, 1.5), zone=1, shade=1.04)
        if state == "on":                                        # Schaum
            for k in range(9):
                c.fill(ell(x0 + 10 + k * W * 0.1, H + 2 + (k % 3) * 2, 6, 4.5, 20), zone=2, shade=1.2)
        c.line([(x1 - 10, H), (x1 - 10, H + 18), (x1 - 18, H + 20)], 1.4, zone=3)
    elif style == "shower":                                      # Duschkabine mit Glas
        c.fill(rrect(x0, 0, x1, 6, 1), zone=1)
        c.line([(x0 + 2, 6), (x0 + 2, H)], 1.2, zone=3)
        c.line([(x0 + 2, H), (x1 - 2, H)], 1.2, zone=3)
        c.line([(x1 - 2, 6), (x1 - 2, H)], 1.2, zone=3)
        c.glass(rrect(x0 + 3, 6, x1 - 3, H - 1, 1), zone=2, opacity=0.35)
        c.line([(x0 + W * 0.3, H - 10), (x0 + W * 0.3, H - 30), (x0 + W * 0.5, H - 32)], 1.2, zone=3)
        c.fill(ell(x0 + W * 0.52, H - 32, 4, 1.5, 16), zone=3)
        if state == "on":
            for k in range(7):
                x = x0 + W * 0.44 + k * 1.8
                c.line([(x, H - 34), (x - 3 + k, 10)], 0.4, zone=2, shade=1.2)
    elif style == "toilet":
        tank = rrect(-W * 0.36, H * 0.5, W * 0.4, H, 2)
        shaded(c, tank, 1, "right", SHADE, 0.15)
        c.fill(rrect(W * 0.1, H * 0.92, W * 0.24, H + 1.5, 0.8), zone=3)
        bowl = smooth([(-W / 2, H * 0.5, "s"), (W * 0.1, H * 0.5), (W * 0.08, H * 0.22), (-W * 0.1, 0, "s"), (-W * 0.3, 0, "s"), (-W * 0.36, H * 0.24)])
        shaded(c, bowl, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(-W / 2 - 1, H * 0.48, W * 0.14, H * 0.55, 2), zone=2)
        if state == "on":
            c.fill(smooth([(-W * 0.3, H * 0.56), (-W * 0.2, H * 0.66), (-W * 0.1, H * 0.56)]), zone=2, shade=1.2, alpha=0.7)
    elif style == "washbasin":
        c.fill(rrect(-W * 0.12, 0, W * 0.12, H * 0.72, 3), zone=1, shade=0.94)
        basin = smooth([(x0, H * 0.8, "s"), (x1, H * 0.8, "s"), (W * 0.36, H * 0.62), (-W * 0.36, H * 0.62)])
        shaded(c, basin, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(x0 - 1, H * 0.78, x1 + 1, H * 0.84, 1.5), zone=1, shade=1.04)
        c.line([(0, H * 0.84), (0, H * 0.96), (W * 0.12, H)], 1.6, zone=3)
        if state == "on":
            c.line([(W * 0.12, H * 0.98), (W * 0.12, H * 0.8)], 0.8, zone=2, shade=1.2)


def car(it: Item, style: str = "hatch"):
    """Autos (Seitenansicht, fährt nach rechts): hatch, sedan, van, jeep, beetle, pickup.
    Reihenfolge: Karosserie → dunkle Radkästen → Räder davor → Fenster, Türen, Lichter, Stoßstangen."""
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    wr = H * (0.21 if style != "jeep" else 0.24)                  # Rad-Radius
    wx = (-W * 0.3, W * 0.3) if style not in ("van", "pickup") else (-W * 0.32, W * 0.3)
    belt = H * 0.52                                               # Gürtellinie (Unterkante Fenster)
    roof = {"hatch": (-0.38, 0.12, 0.98), "sedan": (-0.26, 0.16, 0.92), "van": (-0.46, 0.34, 1.0),
            "jeep": (-0.4, 0.14, 1.0), "beetle": (-0.3, 0.14, 1.0), "pickup": (-0.02, 0.22, 0.98)}[style]
    rx0, rx1, rtop = W * roof[0], W * roof[1], H * roof[2]
    if style == "beetle":
        body = smooth([(x0 + 4, wr * 0.8, "s"), (x1 - 4, wr * 0.8, "s"), (x1, H * 0.34), (W * 0.36, H * 0.5), (W * 0.22, H * 0.56),
                       (W * 0.1, H * 0.92), (-W * 0.08, H), (-W * 0.3, H * 0.9), (-W * 0.44, H * 0.6), (x0, H * 0.36)])
    elif style == "pickup":
        body = smooth([(x0, wr * 0.8, "s"), (x1, wr * 0.8, "s"), (x1, H * 0.5), (W * 0.4, H * 0.56), (rx1 + W * 0.04, H * 0.58),
                       (rx1, rtop, "s"), (rx0 + W * 0.02, rtop, "s"), (rx0, belt + H * 0.04, "s"), (x0, belt + H * 0.04, "s")])
    else:
        nose = {"hatch": 0.2, "sedan": 0.14, "van": 0.08, "jeep": 0.18}[style]
        tail = {"hatch": 0.04, "sedan": 0.16, "van": 0.02, "jeep": 0.03}[style]
        body = smooth([(x0, wr * 0.8, "s"), (x1, wr * 0.8, "s"), (x1, H * 0.46), (x1 - W * nose * 0.3, H * 0.56),
                       (rx1 + W * nose * 0.7, H * 0.6), (rx1, rtop, "s"), (rx0, rtop, "s"), (rx0 - W * tail, belt + H * 0.06),
                       (x0, belt)])
    cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
    for x in wx:                                                   # Radkästen
        c.fill(ell(x, wr * 0.9, wr * 1.18, wr * 1.1, 32), zone=0, alpha=0.85, clip=cl)
    # Fenster (je nach Form 2 oder 3)
    if style == "beetle":
        win = smooth([(-W * 0.24, H * 0.58, "s"), (W * 0.18, H * 0.58, "s"), (W * 0.06, H * 0.9), (-W * 0.08, H * 0.94), (-W * 0.26, H * 0.82)])
        c.fill(win, zone=2, clip=cl)
        c.line([(-W * 0.04, H * 0.58), (-W * 0.04, H * 0.94)], 1.4, zone=1, clip=cl)
        c.line(win, INNER, zone=0, closed=True)
    else:
        n = 3 if style in ("van", "sedan") else 2
        a, b = rx0 + 2.5, rx1 - 1.5
        for k in range(n):
            wa = a + (b - a) * k / n + (1.5 if k else 0)
            wb = a + (b - a) * (k + 1) / n - (1.5 if k < n - 1 else 0)
            front = k == n - 1
            pts = [(wa, belt + 3), (wb + (W * 0.03 if front else 0), belt + 3), (wb - (W * 0.02 if front else 0), rtop - 3),
                   (wa + (W * 0.02 if k == 0 and style == "sedan" else 0), rtop - 3)]
            win = smooth([(p[0], p[1], "s") for p in pts], n=2)
            c.fill(win, zone=2, clip=cl)
            c.fill([(wa + 2, rtop - 4), (wa + 5, rtop - 4), (wa + 2, belt + 5)], zone=2, shade=1.3, alpha=0.6, clip=cl)
            c.line(win, INNER, zone=0, closed=True)
        if style == "pickup":                                      # Ladefläche
            c.line([(x0 + 2, belt + H * 0.04), (rx0 - 2, belt + H * 0.04)], 1.6, zone=1, shade=0.8)
    # Türen + Griffe
    dx = (rx0 + rx1) / 2 if style != "beetle" else -W * 0.04
    for x in ((dx,) if style in ("hatch", "beetle", "pickup") else (dx - (rx1 - rx0) * 0.17, dx + (rx1 - rx0) * 0.17)):
        line(c, [(x, wr * 1.2), (x, belt + 2)], zone=1, clip=cl)
        c.fill(rrect(x + 2, belt - 5, x + 7, belt - 3.8, 0.5), zone=3)
    # Lichter + Stoßstangen
    c.fill(ell(x1 - 3, H * 0.42, 3, 2.4, 16), zone=2, shade=1.3)
    c.fill(rrect(x0 - 0.5, H * 0.4, x0 + 3, H * 0.47, 0.8), zone=1, shade=0.6)
    for xa, xb in ((x0 - 1.5, x0 + 10), (x1 - 10, x1 + 1.5)):
        c.fill(rrect(xa, wr * 0.75, xb, wr * 1.25, 1.2), zone=3)
        c.line(rrect(xa, wr * 0.75, xb, wr * 1.25, 1.2), INNER, zone=0, closed=True)
    for x in wx:                                                   # Räder vorne drauf
        c.fill(ell(x, wr, wr, wr, 40), zone=0, alpha=0.95)
        c.fill(ell(x, wr, wr * 0.55, wr * 0.55, 32), zone=3)
        c.fill(ell(x, wr, wr * 0.18, wr * 0.18, 16), zone=3, shade=0.7)
        c.line(ell(x, wr, wr * 0.55, wr * 0.55, 32), INNER, zone=0, closed=True)
    if style == "jeep":                                            # Reserverad hinten
        c.fill(rrect(x0 - 5, H * 0.3, x0 + 1, H * 0.7, 2.5), zone=0, alpha=0.95)
