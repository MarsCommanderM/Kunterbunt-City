"""
Großer Garten, Teil 2 (P07): Sitzen, Feiern, Grillen (Tische, Stühle, Liege, Hängematte, Hollywoodschaukel, Gasgrill,
Feuerschale, Lichterkette, Wimpel, Pavillon) und Bauten/Spielgeräte (Trampolin, Baumhaus, Gewächshaus, Gartenhaus,
Hundehütte, Kompost, Mülltonne, Briefkasten, Wäschespinne, Regentonne).
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe (Stoff, Dach, Glas) · 3 = Holz/Metall.
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, cushion, ell, knob, leg, line, rrect, shaded, smooth, trap
from .yard import EARTH, _lf


def patio(it: Item, style: str = "table_bistro", state: str = "", seed: int = 3):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    # ---------------------------------------------------------------- Sitzen, Feiern, Grillen
    if style in ("table_bistro", "table_wood", "table_plastic"):
        if style == "table_bistro":
            c.line([(0, H * 0.9), (0, 3)], 2.0, zone=3)
            for sx in (-1, 1):
                c.line(smooth([(0, H * 0.3), (sx * W * 0.2, H * 0.08), (sx * W * 0.32, 0)], closed=False), 1.4, zone=3)
            top = ell(0, H - 2, W / 2, 2.4, 40)
            shaded(c, top, 1, "bottom", SHADE, 0.4)
            c.fill(ell(0, H - 2, W * 0.1, 1.2, 20), zone=2, alpha=0.7)
        else:
            for sx in (-1, 1):
                leg(c, sx * (W / 2 - 8), 0, H - 3, 5 if style == "table_wood" else 4, 5 if style == "table_wood" else 3,
                    zone=1 if style == "table_plastic" else 3)
            top = rrect(x0, H - 5, x1, H, 1.2)
            cl = shaded(c, top, 1, "bottom", SHADE, 0.35)
            if style == "table_wood":
                for k in range(1, 6):
                    line(c, [(x0 + W * k / 6, H - 5), (x0 + W * k / 6, H)], zone=1, clip=cl)
    elif style in ("chair_bistro", "chair_wood", "chair_plastic", "lounger"):
        seat_h = 45 if style != "lounger" else 32
        if style == "lounger":                                       # Sonnenliege mit Auflage
            for x in (x0 + 10, x1 - 10):
                leg(c, x, 0, seat_h - 4, 3, 3)
            c.fill(rrect(x0, seat_h - 6, x1 - W * 0.2, seat_h, 1.5), zone=3)
            back = [(x1 - W * 0.22, seat_h - 4), (x1 - W * 0.02, seat_h + H * 0.45), (x1 + 3, seat_h + H * 0.42), (x1 - W * 0.12, seat_h - 5)]
            c.fill(back, zone=3)
            cush = rrect(x0 + 2, seat_h - 1, x1 - W * 0.22, seat_h + 5, 2.5)
            shaded(c, cush, 1, "bottom", SHADE, 0.3)
            c.fill(smooth([(x1 - W * 0.22, seat_h), (x1 - W * 0.04, seat_h + H * 0.4), (x1 + 1, seat_h + H * 0.38),
                           (x1 - W * 0.14, seat_h - 1)]), zone=1, shade=0.96)
            c.line(smooth([(x1 - W * 0.22, seat_h), (x1 - W * 0.04, seat_h + H * 0.4), (x1 + 1, seat_h + H * 0.38),
                           (x1 - W * 0.14, seat_h - 1)]), INNER, zone=0, closed=True)
            return
        zl = 3 if style != "chair_plastic" else 1
        if style == "chair_bistro":
            for sx in (-1, 1):
                c.line([(sx * W * 0.4, 0), (sx * W * 0.3, seat_h)], 1.4, zone=3)
            c.line([(W * 0.34, seat_h), (W * 0.4, H)], 1.4, zone=3)
            c.line(ell(W * 0.1, H * 0.78, W * 0.26, H * 0.18, 32), 1.2, zone=3, closed=True)
            seat = ell(0, seat_h, W * 0.46, 2.6, 32)
        else:
            for sx in (-1, 1):
                leg(c, sx * W * 0.38, 0, seat_h, 3, 3, zone=zl)
            back = rrect(W * 0.26, seat_h, W * 0.46, H, 1.5)
            c.fill(back, zone=zl)
            c.line(back, INNER, zone=0, closed=True)
            if style == "chair_wood":
                for k in range(3):
                    c.fill(rrect(-W * 0.44, seat_h + 8 + k * 9, W * 0.46, seat_h + 13 + k * 9, 1), zone=1)
                    c.line(rrect(-W * 0.44, seat_h + 8 + k * 9, W * 0.46, seat_h + 13 + k * 9, 1), INNER, zone=0, closed=True)
            seat = rrect(x0, seat_h - 3, x1, seat_h + 1, 1.2)
        shaded(c, seat, 1, "bottom", SHADE, 0.35)
        if style == "chair_bistro":
            cush = rrect(-W * 0.4, seat_h + 1, W * 0.4, seat_h + 4, 1.5)
            shaded(c, cush, 2, "bottom", SHADE, 0.3)
    elif style == "hammock":
        for sx in (-1, 1):
            c.line([(sx * W * 0.48, 0), (sx * W * 0.4, H)], 3.0, zone=3)
        c.line([(x0 + 2, 2), (x1 - 2, 2)], 3.0, zone=3)
        cloth = smooth([(-W * 0.36, H * 0.85, "s"), (0, H * 0.3), (W * 0.36, H * 0.85, "s"), (0, H * 0.46)])
        cl = shaded(c, cloth, 1, "bottom", SHADE, 0.3)
        for k in range(1, 5):
            c.line(smooth([(-W * 0.36, H * 0.85), (0, H * (0.3 + k * 0.035)), (W * 0.36, H * 0.85)], closed=False), 1.2, zone=2, clip=cl)
        for sx in (-1, 1):
            c.line([(sx * W * 0.36, H * 0.85), (sx * W * 0.41, H * 0.95)], 0.6, zone=3)
    elif style == "swing_bench":                                     # Hollywoodschaukel mit Dach
        for sx in (-1, 1):
            c.line([(sx * W * 0.48, 0), (sx * W * 0.4, H * 0.86)], 2.6, zone=3)
            c.line([(sx * W * 0.3, H * 0.84), (sx * W * 0.3, H * 0.5)], 0.5, zone=3)
        roof = smooth([(x0, H * 0.84, "s"), (x1, H * 0.84, "s"), (W * 0.42, H), (-W * 0.42, H)])
        cl = shaded(c, roof, 1, "bottom", SHADE, 0.3)
        for k in range(8):
            c.fill(rrect(x0 + k * W / 8, H * 0.8, x0 + k * W / 8 + W / 16, H, 0.3), zone=2, clip=cl)
        for k in range(12):
            c.fill(ell(x0 + 4 + k * (W - 8) / 11, H * 0.83, W / 26, 2.4, 16), zone=[1, 2][k % 2])
        c.fill(rrect(-W * 0.34, H * 0.2, W * 0.34, H * 0.27, 1.2), zone=3)
        cushion(c, -W * 0.34, H * 0.26, W * 0.34, H * 0.34, zone=1)
        cushion(c, -W * 0.3, H * 0.33, W * 0.3, H * 0.52, zone=1)
    elif style == "grill_gas":                                       # Gasgrill mit Seitenablagen
        for sx in (-1, 1):
            leg(c, sx * W * 0.3, 0, H * 0.45, 3, 3)
            c.fill(ell(sx * W * 0.3, 3, 3.5, 3.5, 20), zone=0, alpha=0.9)
        cab = rrect(-W * 0.34, 6, W * 0.34, H * 0.5, 1.5)
        shaded(c, cab, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0, H * 0.5, x1, H * 0.55, 0.8), zone=3)
        body = rrect(-W * 0.34, H * 0.5, W * 0.34, H * 0.7, 1.5)
        shaded(c, body, 1, "right", SHADE, 0.2)
        for k in range(3):
            knob(c, -W * 0.15 + k * W * 0.15, H * 0.6, 1.6, zone=3)
        if state == "on":
            lid = smooth([(-W * 0.34, H * 0.72, "s"), (W * 0.34, H * 0.72, "s"), (W * 0.3, H * 1.02), (-W * 0.3, H * 1.02)])
            shaded(c, lid, 1, "bottom", SHADE, 0.3)
            for k in range(6):
                x = -W * 0.28 + k * W * 0.11
                c.fill(smooth([(x - 3, H * 0.7), (x, H * (0.77 + 0.02 * (k % 2))), (x + 3, H * 0.7)]), zone=2)
            c.fill(rrect(-W * 0.34, H * 0.69, W * 0.34, H * 0.72, 0.3), zone=3)
        else:
            lid = smooth([(-W * 0.34, H * 0.7, "s"), (W * 0.34, H * 0.7, "s"), (W * 0.3, H * 0.84), (-W * 0.3, H * 0.84)])
            shaded(c, lid, 1, "bottom", SOFT, 0.3)
            c.fill(rrect(-W * 0.14, H * 0.78, W * 0.14, H * 0.8, 0.5), zone=3)
    elif style == "fire_bowl":
        for sx in (-1, 1):
            leg(c, sx * W * 0.28, 0, H * 0.4, 2.5, 2.5)
        bowl = smooth([(x0, H * 0.62, "s"), (x1, H * 0.62, "s"), (W * 0.3, H * 0.3), (-W * 0.3, H * 0.3)])
        shaded(c, bowl, 1, "bottom", SHADE, 0.4)
        for k in range(3):
            c.line([(-W * 0.25 + k * W * 0.16, H * 0.6), (-W * 0.05 + k * W * 0.14, H * 0.68)], 2.4, zone=3, shade=0.6)
        if state == "on":
            for k, (x, hh) in enumerate(((-W * 0.2, 0.9), (0, 1.1), (W * 0.2, 0.85))):
                c.fill(smooth([(x - W * 0.1, H * 0.62), (x, H * hh), (x + W * 0.1, H * 0.62)]), zone=2)
                c.fill(smooth([(x - W * 0.04, H * 0.62), (x, H * (hh - 0.15)), (x + W * 0.04, H * 0.62)]), zone=2, shade=1.35)
    elif style in ("lights", "bunting"):                             # hängt an der Wand/zwischen Pfosten
        cord = [(x0 + W * k / 20, H * (1 - 0.35 * math.sin(math.pi * k / 20))) for k in range(21)]
        c.line(smooth(cord, closed=False), 0.5, zone=3)
        for k in range(1, 20 if style == "lights" else 12):
            t = k / (20 if style == "lights" else 12)
            x, y = x0 + W * t, H * (1 - 0.35 * math.sin(math.pi * t))
            if style == "lights":
                bulb = ell(x, y - 3, 1.6, 2.4, 16)
                if state == "on":
                    c.glass(ell(x, y - 3, 5, 5, 20), zone=[1, 2][k % 2], opacity=0.35)
                c.fill(bulb, zone=[1, 2][k % 2], shade=1.25 if state == "on" else 0.9)
                c.line(bulb, INNER, zone=0, closed=True)
            else:
                flag = [(x - 5, y), (x + 5, y), (x, y - 12)]
                c.fill(flag, zone=[1, 2, 3][k % 3], shade=1.0)
                c.line(flag + [flag[0]], INNER, zone=0)
    elif style in ("pavilion", "gazebo"):
        if style == "pavilion":                                      # Party-Zelt: Stoffdach mit Volant
            for sx in (-1, 1):
                c.fill(rrect(sx * W * 0.46 - 1.5, 0, sx * W * 0.46 + 1.5, H * 0.72, 0.6), zone=3)
            roof = smooth([(x0, H * 0.7, "s"), (x1, H * 0.7, "s"), (W * 0.1, H), (-W * 0.1, H)])
            cl = shaded(c, roof, 1, "bottom", SOFT, 0.2)
            for k in range(6):
                c.fill([(x0 + k * W / 6, H * 0.7), (x0 + k * W / 6 + W / 12, H * 0.7), (-W * 0.05 + k * 0.02 * W, H), (-W * 0.06 + k * 0.02 * W, H)],
                       zone=2, clip=cl)
            for k in range(12):
                c.fill(ell(x0 + W / 24 + k * W / 12, H * 0.7, W / 24, 5, 16), zone=[1, 2][k % 2])
            for sx in (-1, 1):
                c.fill(smooth([(sx * W * 0.47, H * 0.7), (sx * W * 0.44, H * 0.4), (sx * W * 0.38, H * 0.66)]), zone=1, shade=0.95)
        else:                                                        # Holz-Pavillon mit Dachspitze
            for x in (x0 + 6, -W * 0.16, W * 0.16, x1 - 6):
                c.fill(rrect(x - 3, 0, x + 3, H * 0.65, 1), zone=1)
                c.line(rrect(x - 3, 0, x + 3, H * 0.65, 1), INNER, zone=0, closed=True)
            c.fill(rrect(x0 + 3, H * 0.28, x1 - 3, H * 0.31, 0.5), zone=1, shade=0.9)
            for k in range(12):
                x = x0 + 8 + k * (W - 16) / 11
                c.line([(x, H * 0.02), (x, H * 0.29)], 0.9, zone=1, shade=0.9)
            roof = [(x0 - 6, H * 0.64), (x1 + 6, H * 0.64), (0, H)]
            cl = shaded(c, roof, 2, "bottom", SHADE, 0.2)
            for k in range(1, 6):
                line(c, [(x0 - 6 + k * 8, H * 0.64), (0, H)], zone=2, clip=cl)
                line(c, [(x1 + 6 - k * 8, H * 0.64), (0, H)], zone=2, clip=cl)
            c.fill(ell(0, H + 2, 3, 3, 16), zone=3)
    # ---------------------------------------------------------------- Spielen & Bauten
    elif style == "trampoline":
        for k in range(5):
            x = x0 + 8 + k * (W - 16) / 4
            c.line(smooth([(x, H * 0.3), (x + 3, H * 0.12), (x, 0)], closed=False), 1.8, zone=3)
        c.fill(ell(0, H * 0.32, W / 2, H * 0.08, 48), zone=1)
        c.fill(ell(0, H * 0.33, W * 0.42, H * 0.05, 48), zone=0, alpha=0.85)
        for x in (x0 + 4, -W * 0.18, W * 0.18, x1 - 4):
            c.line([(x, H * 0.32), (x, H)], 1.4, zone=3)
        net = rrect(x0 + 4, H * 0.34, x1 - 4, H, 1)
        ncl = c.mask(net)
        for k in range(int(W / 5)):
            c.line([(x0 + 4 + k * 5, H * 0.34), (x0 + 4 + k * 5, H)], 0.15, zone=2, shade=0.7, clip=ncl)
        for k in range(int(H * 0.66 / 5)):
            c.line([(x0 + 4, H * 0.34 + k * 5), (x1 - 4, H * 0.34 + k * 5)], 0.15, zone=2, shade=0.7, clip=ncl)
        c.fill(rrect(-W * 0.12, H * 0.34, W * 0.12, H * 0.8, 1), zone=0, alpha=0.0)
        c.line([(x0 + 4, H), (x1 - 4, H)], 2.4, zone=1)
    elif style == "treehouse":
        c.fill(rrect(-W * 0.08, 0, W * 0.08, H * 0.6, 3), zone=3, shade=0.8)
        rng = random.Random(seed)
        crown = smooth([(-W * 0.48, H * 0.62), (-W * 0.44, H * 0.8), (-W * 0.28, H * 0.95), (0, H), (W * 0.3, H * 0.95), (W * 0.46, H * 0.8),
                        (W * 0.48, H * 0.6), (W * 0.36, H * 0.5), (-W * 0.36, H * 0.5)])
        ccl = shaded(c, crown, 1, "bottom", SHADE, 0.3)
        for _ in range(40):
            x, y = rng.uniform(-W * 0.44, W * 0.44), rng.uniform(H * 0.52, H * 0.96)
            c.fill(ell(x, y, W * 0.07, H * 0.035, 20), zone=1, shade=rng.choice([0.9, 1.08, 1.15]), clip=ccl)
        for sx in (-1, 1):
            c.line([(sx * W * 0.2, 0), (sx * W * 0.2, H * 0.42)], 2.0, zone=3)
        plat = rrect(-W * 0.3, H * 0.4, W * 0.3, H * 0.44, 1)
        c.fill(plat, zone=3)
        house = rrect(-W * 0.22, H * 0.44, W * 0.22, H * 0.66, 1)
        cl = shaded(c, house, 3, "right", SHADE, 0.15)
        for k in range(1, 5):
            line(c, [(-W * 0.22, H * 0.44 + k * H * 0.044), (W * 0.22, H * 0.44 + k * H * 0.044)], zone=3, clip=cl)
        c.fill(rrect(-W * 0.06, H * 0.5, W * 0.06, H * 0.6, 1), zone=0, alpha=0.8)
        c.fill([(-W * 0.28, H * 0.65), (W * 0.28, H * 0.65), (0, H * 0.8)], zone=2)
        c.line([(-W * 0.28, H * 0.65), (W * 0.28, H * 0.65), (0, H * 0.8), (-W * 0.28, H * 0.65)], INNER, zone=0)
        for k in range(8):                                           # Strickleiter
            y = H * 0.04 + k * H * 0.045
            c.line([(W * 0.26, y), (W * 0.34, y)], 1.0, zone=3, shade=1.2)
        for x in (W * 0.26, W * 0.34):
            c.line([(x, 0), (x, H * 0.42)], 0.5, zone=3, shade=1.2)
    elif style in ("greenhouse", "shed", "doghouse"):
        roof_h = {"greenhouse": 0.3, "shed": 0.3, "doghouse": 0.4}[style]
        wall_top = H * (1 - roof_h)
        body = rrect(x0 + 3, 0, x1 - 3, wall_top, 1)
        if style == "greenhouse":
            c.fill(rrect(x0 + 3, 0, x1 - 3, 6, 0.6), zone=1)
            c.glass(body, zone=2, opacity=0.3)
            roof = [(x0, wall_top), (x1, wall_top), (0, H)]
            c.glass(roof, zone=2, opacity=0.35)
            for k in range(6):
                x = x0 + 3 + k * (W - 6) / 5
                c.line([(x, 0), (x, wall_top)], 1.2, zone=1)
            c.line([(x0 + 3, wall_top * 0.5), (x1 - 3, wall_top * 0.5)], 1.0, zone=1)
            c.line([(x0, wall_top), (0, H), (x1, wall_top), (x0, wall_top)], 1.4, zone=1)
            for k in range(5):
                x = x0 + 14 + k * (W - 28) / 4
                c.fill(trap(x - 5, x + 5, 0, x - 6, x + 6, 10, 0.6), zone=1, shade=0.8)
                for a in (-0.5, 0, 0.5):
                    _lf(c, x, 10, 16, math.pi / 2 + a, zone=3)
            return
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        for k in range(1, int(W / 12)):
            line(c, [(x0 + 3 + k * 12, 0), (x0 + 3 + k * 12, wall_top)], zone=1, clip=cl)
        roof = [(x0 - 4, wall_top - 2), (x1 + 4, wall_top - 2), (0, H)] if style == "doghouse" else \
            [(x0 - 5, wall_top - 2), (x1 + 5, wall_top - 2), (x1 - W * 0.15, H), (x0 + W * 0.15, H)]
        c.fill(roof, zone=2)
        c.line(roof + [roof[0]], INNER, zone=0)
        c.fill(rrect(roof[0][0], wall_top - 3, roof[1][0], wall_top + 1, 0.8), zone=2, shade=0.8)
        if style == "doghouse":
            c.fill(smooth([(-W * 0.2, 0, "s"), (W * 0.2, 0, "s"), (W * 0.2, wall_top * 0.6), (0, wall_top * 0.85), (-W * 0.2, wall_top * 0.6)]),
                   zone=0, alpha=0.85)
            c.fill(rrect(-W * 0.18, wall_top * 0.9, W * 0.18, wall_top * 1.02, 1), zone=3)
        else:
            door = rrect(-W * 0.14, 0, W * 0.14, wall_top * 0.82, 1)
            if state == "open":
                c.fill(door, zone=0, alpha=0.8)
                for k, (x, hh) in enumerate(((-W * 0.08, 0.5), (W * 0.06, 0.62))):
                    c.line([(x, 2), (x + 2, wall_top * hh)], 1.2, zone=3, shade=1.3)
                c.fill([(W * 0.14, 0), (W * 0.26, -2), (W * 0.26, wall_top * 0.86), (W * 0.14, wall_top * 0.82)], zone=2, shade=0.9)
            else:
                c.fill(door, zone=2, shade=0.95)
                c.line(door, INNER, zone=0, closed=True)
                knob(c, W * 0.1, wall_top * 0.42, 1.4)
            win = rrect(W * 0.24, wall_top * 0.45, W * 0.4, wall_top * 0.75, 0.8)
            c.fill(win, zone=2, shade=1.4)
            c.line(win, INNER, zone=0, closed=True)
    elif style == "compost":
        body = rrect(x0, 0, x1, H * 0.85, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.15)
        for k in range(1, 6):
            c.fill(rrect(x0, H * 0.85 * k / 6 - 1, x1, H * 0.85 * k / 6 + 1, 0.3), zone=0, alpha=0.5, clip=cl)
        rng = random.Random(seed)
        c.fill(smooth([(x0 + 2, H * 0.84), (x1 - 2, H * 0.84), (W * 0.2, H), (-W * 0.25, H * 0.98)]), zone=3, shade=EARTH)
        for _ in range(6):
            _lf(c, rng.uniform(x0 + 8, x1 - 8), H * 0.9, 8, rng.uniform(0.5, 2.6), zone=2)
    elif style == "bin":                                             # Mülltonne mit Deckel und Rädern
        c.fill(ell(W * 0.28, 5, 5, 5, 20), zone=0, alpha=0.9)
        body = trap(x0 + 3, x1 - 3, 3, x0, x1, H * 0.88, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        for k in (0.3, 0.6):
            c.fill(rrect(x0, H * k, x1, H * k + 1.2, 0.3), zone=1, shade=0.8, clip=cl)
        if state == "open":
            c.fill([(x0 - 1, H * 0.88), (x0 + 3, H * 0.88), (x0 - 4, H * 1.35), (x0 - 7, H * 1.32)], zone=1, shade=0.95)
            c.fill(ell(0, H * 0.88, W * 0.46, 2, 24), zone=0, alpha=0.85)
        else:
            c.fill(rrect(x0 - 1, H * 0.86, x1 + 2, H, 1.5), zone=1, shade=1.05)
            c.fill(rrect(x1 - 2, H * 0.9, x1 + 3, H * 0.96, 0.6), zone=1, shade=0.9)
    elif style == "mailbox":
        c.fill(rrect(-2, 0, 2, H * 0.72, 0.6), zone=3)
        box = smooth([(x0, H * 0.7, "s"), (x1, H * 0.7, "s"), (x1, H * 0.88), (0, H), (x0, H * 0.88)])
        shaded(c, box, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.3, H * 0.84, W * 0.3, H * 0.87, 0.4), zone=0, alpha=0.8)
        c.fill(rrect(x1 - 2, H * 0.78, x1 + 1, H * 0.96, 0.4), zone=2)
        c.fill(rrect(x1 - 2, H * 0.93, x1 + 6, H * 0.97, 0.6), zone=2)
    elif style == "clothesline":                                     # Wäschespinne mit Wäsche
        c.line([(0, 0), (0, H)], 2.2, zone=3)
        for sx in (-1, 1):
            c.line([(0, H * 0.72), (sx * W * 0.48, H * 0.95)], 1.2, zone=3)
        c.line([(-W * 0.48, H * 0.95), (W * 0.48, H * 0.95)], 0.4, zone=3)
        for k, (x, z, kind) in enumerate(((-W * 0.36, 1, "shirt"), (-W * 0.14, 2, "sock"), (W * 0.12, 1, "towel"), (W * 0.34, 2, "shirt"))):
            if kind == "towel":
                cl = shaded(c, rrect(x - 11, H * 0.6, x + 11, H * 0.95, 1), z, "right", SHADE, 0.25)
                c.fill(rrect(x - 11, H * 0.64, x + 11, H * 0.67, 0.3), zone=[2, 1][z - 1], clip=cl)
            elif kind == "sock":
                shaded(c, smooth([(x - 3, H * 0.95), (x + 3, H * 0.95), (x + 3, H * 0.75), (x + 8, H * 0.7), (x + 6, H * 0.66), (x - 3, H * 0.72)]),
                       z, "right", SHADE, 0.3)
            else:
                shaded(c, smooth([(x - 7, H * 0.66, "s"), (x + 7, H * 0.66, "s"), (x + 7, H * 0.86), (x + 11, H * 0.82), (x + 11, H * 0.95),
                                  (x - 11, H * 0.95), (x - 11, H * 0.82), (x - 7, H * 0.86)]), z, "right", SHADE, 0.25)
            c.fill(rrect(x - 1, H * 0.93, x + 1, H * 0.98, 0.3), zone=3, shade=1.4)
    elif style == "rain_barrel":
        body = smooth([(x0 + 2, 0, "s"), (x1 - 2, 0, "s"), (x1, H * 0.5), (x1 - 2, H * 0.94, "s"), (x0 + 2, H * 0.94, "s"), (x0, H * 0.5)])
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        for y in (H * 0.2, H * 0.75):
            c.fill(rrect(x0, y, x1, y + 2.5, 0.6), zone=3, clip=cl)
        c.fill(ell(0, H * 0.95, W * 0.44, 2.5, 32), zone=2)
        c.fill(rrect(W * 0.2, H * 0.12, W * 0.42, H * 0.17, 0.8), zone=3)
