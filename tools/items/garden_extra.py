"""
Garten, Teil 3 (P07-Inventar, Wunsch 👤): Zäune in allen Arten und Größen, Beetkante, Insektenhotel,
Schildkröten-Gehege, Gartenlaube, Hasenstall, Hühnerstall, Vogeltränke, Futterhaus, Pflanzkübel, Sonnenschirm,
Sonnensegel, Fackel, Picknickdecke, Picknickkorb, Schlauchwagen, Schaukelgestell, Spielhaus.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Holz/Metall/Pflanzen.
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, ell, knob, leg, line, rrect, shaded, smooth, trap
from .yard import EARTH, _lf


def fence(it: Item, style: str = "picket", seed: int = 1):
    """picket (Latten) · wire (Maschendraht) · metal (Schmiede-Eisen) · privacy (Sichtschutz) · bamboo · rail (Koppel)."""
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    posts = max(2, int(W / 100) + 1)
    px = [x0 + 3 + k * (W - 6) / (posts - 1) for k in range(posts)]
    if style == "picket":
        n = max(3, int(W / 13))
        for y in (H * 0.22, H * 0.62):
            c.fill(rrect(x0, y, x1, y + max(3, H * 0.08), 0.4), zone=1, shade=0.86)
        for k in range(n):
            x = x0 + W * (k + 0.5) / n
            w = W / n * 0.34
            pts = [(x - w, 0), (x + w, 0), (x + w, H * 0.88), (x, H), (x - w, H * 0.88)]
            c.fill(pts, zone=1)
            c.line(pts + [pts[0]], INNER, zone=0)
    elif style == "wire":
        for x in px:
            c.fill(rrect(x - 2, 0, x + 2, H, 1), zone=3)
        mesh = rrect(x0 + 3, 2, x1 - 3, H - 3, 0.2)
        cl = c.mask(mesh)
        for k in range(-int(H / 8), int(W / 8) + 1):
            c.line([(x0 + k * 8, 0), (x0 + k * 8 + H, H)], 0.35, zone=1, clip=cl)
            c.line([(x0 + k * 8 + H, 0), (x0 + k * 8, H)], 0.35, zone=1, clip=cl)
        c.line([(x0 + 3, H - 3), (x1 - 3, H - 3)], 0.8, zone=1)
    elif style == "metal":
        for x in px:
            c.fill(rrect(x - 2.5, 0, x + 2.5, H + 3, 0.8), zone=1)
            c.fill(ell(x, H + 4, 3, 3, 16), zone=2)
        for y in (H * 0.1, H * 0.8):
            c.fill(rrect(x0, y, x1, y + 2, 0.4), zone=1)
        for k in range(int(W / 10)):
            x = x0 + 5 + k * 10
            c.line([(x, 0), (x, H * 0.95)], 1.0, zone=1)
            c.fill([(x - 1.6, H * 0.93), (x + 1.6, H * 0.93), (x, H * 1.02)], zone=2)
            if k % 2:
                c.line(ell(x + 5, H * 0.45, 3, 4, 16), 0.6, zone=2, closed=True)
    elif style == "privacy":
        body = rrect(x0, 0, x1, H, 0.6)
        cl = shaded(c, body, 1, "right", SOFT, 0.1)
        for k in range(1, int(H / 12) + 1):
            line(c, [(x0, k * 12), (x1, k * 12)], zone=1, clip=cl)
        for x in px:
            c.fill(rrect(x - 3, 0, x + 3, H + 2, 0.6), zone=3)
            c.line(rrect(x - 3, 0, x + 3, H + 2, 0.6), INNER, zone=0, closed=True)
        c.fill(rrect(x0, H - 2, x1, H + 2, 0.6), zone=3, shade=1.05)
    elif style == "bamboo":
        rng = random.Random(seed)
        n = int(W / 4.5)
        for k in range(n):
            x = x0 + (k + 0.5) * W / n
            hh = H * rng.uniform(0.94, 1.0)
            cane = rrect(x - 2, 0, x + 2, hh, 1.5)
            c.fill(cane, zone=1, shade=rng.choice([0.92, 1.0, 1.08]))
            for j in range(1, int(hh / 22) + 1):
                c.line([(x - 2, j * 22), (x + 2, j * 22)], 0.4, zone=0)
            c.line(cane, INNER * 0.7, zone=0, closed=True)
        for y in (H * 0.25, H * 0.75):
            c.line([(x0, y), (x1, y)], 0.8, zone=2)
    elif style == "rail":                                           # Koppelzaun
        for x in px:
            c.fill(rrect(x - 4, 0, x + 4, H, 2), zone=3)
            c.line(rrect(x - 4, 0, x + 4, H, 2), INNER, zone=0, closed=True)
        for y in (H * 0.35, H * 0.8):
            rail = rrect(x0, y, x1, y + 6, 3)
            shaded(c, rail, 1, "bottom", SHADE, 0.35)
    elif style == "edging":                                         # Beetkante: kleine Rundbögen / Pflöcke
        for k in range(int(W / 9)):
            x = x0 + 4.5 + k * 9
            log = rrect(x - 4, 0, x + 4, H * (0.8 + 0.2 * (k % 2)), 3.5)
            shaded(c, log, 1, "right", SHADE, 0.3)
            c.fill(ell(x, H * (0.8 + 0.2 * (k % 2)) - 1.5, 3.5, 1.3, 12), zone=2)


def garden_extra(it: Item, style: str = "insect_hotel", state: str = "", seed: int = 1):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    rng = random.Random(seed)
    if style == "insect_hotel":
        c.fill(rrect(-2, 0, 2, H * 0.25, 0.6), zone=3)
        box = rrect(x0 + 3, H * 0.22, x1 - 3, H * 0.8, 0.8)
        c.fill(box, zone=3)
        rows = [(H * 0.22, H * 0.4), (H * 0.42, H * 0.6), (H * 0.62, H * 0.8)]
        for j, (a, b) in enumerate(rows):
            for i in range(2):
                ca, cb = x0 + 5 + i * (W - 10) / 2, x0 + 3 + (i + 1) * (W - 10) / 2
                kind = (i + j) % 3
                c.fill(rrect(ca, a + 1, cb, b - 1, 0.4), zone=3, shade=0.5)
                if kind == 0:                                        # Holz mit Löchern
                    c.fill(rrect(ca, a + 1, cb, b - 1, 0.4), zone=1)
                    for _ in range(8):
                        c.ellipse(rng.uniform(ca + 2, cb - 2), rng.uniform(a + 3, b - 3), 0.8, 0.8, zone=0)
                elif kind == 1:                                      # Bambusröhrchen
                    for yy in range(int(a + 2.5), int(b - 1), 3):
                        for xx in range(int(ca + 2), int(cb - 1), 3):
                            c.fill(ell(xx, yy, 1.4, 1.4, 10), zone=2)
                            c.fill(ell(xx, yy, 0.6, 0.6, 8), zone=0)
                else:                                                # Zapfen/Stroh
                    for _ in range(6):
                        c.fill(ell(rng.uniform(ca + 3, cb - 3), rng.uniform(a + 3, b - 3), 2.2, 1.6, 12), zone=2, shade=0.8)
        c.line(box, INNER, zone=0, closed=True)
        roof = [(x0, H * 0.78), (x1, H * 0.78), (0, H)]
        shaded(c, roof, 1, "bottom", SHADE, 0.3)
        c.fill(ell(W * 0.25, H * 0.9, 1.6, 1.0, 12), zone=2, shade=1.4)                             # Biene
    elif style == "tortoise_pen":                                   # Gehege: Holzrand, Häuschen, Gras, Schildkröte
        c.fill(rrect(x0, 0, x1, H * 0.45, 1), zone=3)
        c.line(rrect(x0, 0, x1, H * 0.45, 1), INNER, zone=0, closed=True)
        for k in range(1, int(W / 30)):
            line(c, [(x0 + k * 30, 0), (x0 + k * 30, H * 0.45)], zone=3)
        c.fill(rrect(x0 + 2, H * 0.42, x1 - 2, H * 0.5, 0.6), zone=1, shade=1.05)
        for _ in range(int(W / 6)):
            x = rng.uniform(x0 + 4, x1 - 4)
            c.line([(x, H * 0.48), (x + rng.uniform(-1.5, 1.5), H * rng.uniform(0.56, 0.66))], 0.5, zone=1, shade=0.85)
        hx = x0 + W * 0.2
        c.fill(rrect(hx - 14, H * 0.46, hx + 14, H * 0.8, 0.6), zone=3, shade=1.1)
        c.fill(ell(hx, H * 0.46, 7, H * 0.18, 16), zone=0, alpha=0.8)
        c.fill([(hx - 18, H * 0.78), (hx + 18, H * 0.78), (hx, H)], zone=2)
        c.line([(hx - 18, H * 0.78), (hx + 18, H * 0.78), (hx, H), (hx - 18, H * 0.78)], INNER, zone=0)
        tx = W * 0.15
        shell = smooth([(tx - 10, H * 0.5, "s"), (tx + 10, H * 0.5, "s"), (tx + 6, H * 0.66), (tx - 6, H * 0.66)])
        c.fill(ell(tx + 12, H * 0.54, 3, 2.4, 12), zone=1, shade=0.8)
        shaded(c, shell, 2, "bottom", SHADE, 0.3)
        for k in range(3):
            c.line(ell(tx - 5 + k * 5, H * 0.58, 2, 1.5, 10), 0.3, zone=0, closed=True)
    elif style == "arbor":                                          # Gartenlaube: Häuschen mit Veranda + Fenster
        wall_top = H * 0.62
        body = rrect(x0 + 6, 0, x1 - W * 0.2, wall_top, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        for k in range(1, int(W / 12)):
            line(c, [(x0 + 6 + k * 12, 0), (x0 + 6 + k * 12, wall_top)], zone=1, clip=cl)
        door = rrect(x0 + W * 0.15, 0, x0 + W * 0.32, wall_top * 0.85, 1)
        c.fill(door, zone=2)
        c.line(door, INNER, zone=0, closed=True)
        knob(c, x0 + W * 0.29, wall_top * 0.42, 1.4)
        for wx in (x0 + W * 0.44, x0 + W * 0.62):
            win = rrect(wx - 9, wall_top * 0.4, wx + 9, wall_top * 0.78, 0.8)
            c.fill(win, zone=2, shade=1.5)
            c.line([(wx, wall_top * 0.4), (wx, wall_top * 0.78)], 0.8, zone=2, shade=0.8)
            c.line(win, INNER, zone=0, closed=True)
            c.fill(rrect(wx - 11, wall_top * 0.36, wx + 11, wall_top * 0.4, 0.4), zone=2, shade=0.9)
            for k in range(4):
                c.fill(ell(wx - 8 + k * 5.3, wall_top * 0.4 + 2, 2, 2, 10), zone=[1, 2][k % 2], shade=1.2)
        c.fill(rrect(x0, 0, x1, 6, 0.6), zone=3)                                                     # Veranda
        for x in (x1 - W * 0.18, x1 - 3):
            c.fill(rrect(x - 2, 6, x + 2, wall_top, 0.6), zone=3)
        c.line([(x1 - W * 0.18, 30), (x1 - 3, 30)], 1.4, zone=3)
        roof = [(x0 - 6, wall_top - 2), (x1 + 6, wall_top - 2), (x1 - W * 0.25, H), (x0 + W * 0.25, H)]
        rcl = shaded(c, roof, 2, "bottom", SHADE, 0.2)
        for k in range(1, 6):
            line(c, [(x0 - 6 + k * (W + 12) / 6, wall_top - 2), (x0 + W * 0.25 + k * W * 0.5 / 6, H)], zone=2, clip=rcl)
    elif style in ("hutch", "coop"):
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 5), 0, H * 0.3, 4, 4)
        body = rrect(x0 + 2, H * 0.28, x1 - 2, H * 0.78, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        mesh = rrect(x0 + 6, H * 0.33, 0, H * 0.73, 0.4)
        c.fill(mesh, zone=0, alpha=0.4)
        mcl = c.mask(mesh)
        for k in range(int(W / 4)):
            c.line([(x0 + 6 + k * 4, H * 0.33), (x0 + 6 + k * 4, H * 0.73)], 0.25, zone=3, shade=1.4, clip=mcl)
            c.line([(x0 + 6, H * 0.33 + k * 4), (0, H * 0.33 + k * 4)], 0.25, zone=3, shade=1.4, clip=mcl)
        c.line(mesh, INNER, zone=0, closed=True)
        c.fill(rrect(4, H * 0.33, x1 - 6, H * 0.73, 0.6), zone=2)
        c.line(rrect(4, H * 0.33, x1 - 6, H * 0.73, 0.6), INNER, zone=0, closed=True)
        if style == "coop":
            c.fill(smooth([(W * 0.16, H * 0.33), (W * 0.3, H * 0.33), (W * 0.3, H * 0.52), (W * 0.23, H * 0.58), (W * 0.16, H * 0.52)]),
                   zone=0, alpha=0.8)
            c.line([(W * 0.23, H * 0.33), (x1 + 8, 0)], 3.0, zone=3)                                   # Hühnerleiter
            for k in range(4):
                t = (k + 1) / 5
                c.line([(W * 0.23 + (x1 + 8 - W * 0.23) * t - 2, H * 0.33 * (1 - t)), (W * 0.23 + (x1 + 8 - W * 0.23) * t + 2,
                                                                                         H * 0.33 * (1 - t))], 0.8, zone=3, shade=0.8)
        roof = [(x0 - 3, H * 0.76), (x1 + 3, H * 0.76), (x1 - W * 0.1, H), (x0 + W * 0.1, H)] if style == "coop" else \
            [(x0 - 3, H * 0.76), (x1 + 3, H * 0.76), (x1 + 3, H * 0.84), (x0 - 3, H * 0.92)]
        c.fill(roof, zone=2, shade=0.85)
        c.line(roof + [roof[0]], INNER, zone=0)
    elif style == "bird_bath":
        c.fill(trap(-W * 0.3, W * 0.3, 0, -W * 0.16, W * 0.16, H * 0.1, 1), zone=1, shade=0.95)
        c.fill(rrect(-W * 0.1, H * 0.1, W * 0.1, H * 0.8, 2), zone=1)
        bowl = smooth([(x0, H, "s"), (x1, H, "s"), (W * 0.2, H * 0.78), (-W * 0.2, H * 0.78)])
        shaded(c, bowl, 1, "bottom", SHADE, 0.35)
        c.fill(ell(0, H - 0.5, W * 0.44, 1.8, 24), zone=2)
        c.fill(ell(W * 0.28, H + 4, 3.5, 2.8, 16), zone=3)                                              # Vogel
        c.fill(ell(W * 0.34, H + 6.5, 2, 2, 12), zone=3)
        c.fill([(W * 0.4, H + 6.8), (W * 0.45, H + 6.3), (W * 0.4, H + 6)], zone=2, shade=0.6)
    elif style == "bird_feeder":
        c.fill(rrect(-1.6, 0, 1.6, H * 0.65, 0.5), zone=3)
        c.fill(rrect(x0 + 2, H * 0.6, x1 - 2, H * 0.64, 0.4), zone=1, shade=0.9)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.34 - 1, H * 0.64, sx * W * 0.34 + 1, H * 0.84, 0.3), zone=1)
        for _ in range(12):
            c.ellipse(rng.uniform(-W * 0.3, W * 0.3), H * 0.66, 0.9, 0.6, zone=2, shade=0.8)
        roof = [(x0, H * 0.82), (x1, H * 0.82), (0, H)]
        shaded(c, roof, 1, "bottom", SHADE, 0.3)
        c.fill(ell(-W * 0.2, H * 0.7, 3.2, 2.6, 12), zone=2, shade=0.7)                                  # Meise
        c.fill(ell(-W * 0.26, H * 0.73, 1.8, 1.8, 12), zone=2, shade=0.7)
    elif style in ("planter_box", "planter_round", "planter_trough", "planter_tall", "planter_basket", "planter_tub"):
        kind = style.split("_")[1]
        top = {"box": 0.55, "round": 0.55, "trough": 0.5, "tall": 0.7, "basket": 0.5, "tub": 0.5}[kind] * H
        if kind == "round":
            pot = smooth([(x0, top, "s"), (x1, top, "s"), (W * 0.36, 0, "s"), (-W * 0.36, 0, "s")])
        elif kind == "tall":
            pot = trap(-W * 0.3, W * 0.3, 0, x0, x1, top, 1.5)
        elif kind == "tub":
            pot = smooth([(x0, top, "s"), (x1, top, "s"), (x1 - 3, 0, "s"), (x0 + 3, 0, "s")])
        else:
            pot = trap(x0 + 3, x1 - 3, 0, x0, x1, top, 1)
        cl = shaded(c, pot, 1, "right", SHADE, 0.25)
        if kind == "basket":
            for k in range(int(W / 5)):
                line(c, [(x0 + k * 5, 0), (x0 + k * 5 + 3, top)], zone=1, clip=cl)
            for j in range(1, 4):
                line(c, [(x0, top * j / 4), (x1, top * j / 4)], zone=1, clip=cl)
        elif kind == "tub":
            for y in (top * 0.2, top * 0.8):
                c.fill(rrect(x0, y, x1, y + 2, 0.4), zone=2, clip=cl)
        else:
            c.fill(rrect(x0 - 1, top - 3, x1 + 1, top, 1), zone=1, shade=1.08)
        c.fill(ell(0, top, W * 0.44, 2, 24), zone=3, shade=EARTH)
        for k in range(7):                                          # Pflanzen + Blüten
            x = x0 + W * (k + 0.5) / 7
            for a in (-0.5, 0.4):
                _lf(c, x, top, (H - top) * rng.uniform(0.6, 0.9), math.pi / 2 + a, zone=3, shade=rng.choice([0.95, 1.1]))
            if k % 2 == 0:
                c.fill(ell(x + 1, top + (H - top) * 0.7, 2.6, 2.6, 12), zone=2, shade=rng.choice([1.0, 1.2]))
    elif style == "parasol":
        c.fill(trap(-W * 0.12, W * 0.12, 0, -W * 0.08, W * 0.08, H * 0.05, 0.8), zone=3, shade=0.6)
        c.line([(0, H * 0.05), (0, H * 0.96)], 1.2, zone=3)
        if state == "closed":
            fold = smooth([(0, H * 0.5, "s"), (W * 0.05, H * 0.8), (0, H * 0.98, "s"), (-W * 0.05, H * 0.8)])
            shaded(c, fold, 1, "right", SHADE, 0.35)
        else:
            canopy = [(x0, H * 0.78)] + [(x0 + W * k / 8, H * 0.78 - 2 * math.sin(math.pi * (k % 1 + 0.5))) for k in range(1, 8)] + \
                     [(x1, H * 0.78), (W * 0.06, H), (-W * 0.06, H)]
            cl = shaded(c, canopy, 1, "bottom", SOFT, 0.2)
            for k in range(0, 8, 2):
                c.fill([(x0 + W * k / 8, H * 0.76), (x0 + W * (k + 1) / 8, H * 0.76), (0, H)], zone=2, clip=cl)
            for k in range(8):
                c.fill(ell(x0 + W * (k + 0.5) / 8, H * 0.78, W / 16, 3, 12), zone=[1, 2][k % 2])
    elif style == "sun_sail":
        for x, h in ((x0 + 2, H), (x1 - 2, H * 0.8)):
            c.fill(rrect(x - 2, 0, x + 2, h, 0.6), zone=3)
        sail = smooth([(x0 + 2, H, "s"), (x1 - 2, H * 0.8, "s"), (W * 0.1, H * 0.64)])
        shaded(c, sail, 1, "bottom", SHADE, 0.3)
        c.line([(x0 + 2, H), (x1 - 2, H * 0.8)], 0.4, zone=2)
    elif style == "torch":
        c.line([(0, 0), (0, H * 0.8)], 1.8, zone=3)
        c.fill(trap(-W * 0.3, W * 0.3, H * 0.78, x0, x1, H * 0.9, 0.6), zone=1)
        if state == "on":
            c.fill(smooth([(x0 + 1, H * 0.9), (0, H * 1.08), (x1 - 1, H * 0.9)]), zone=2)
            c.fill(smooth([(-W * 0.2, H * 0.9), (0, H * 1.0), (W * 0.2, H * 0.9)]), zone=2, shade=1.3)
    elif style == "picnic_blanket":                                 # flach (placement rug), kariert
        body = rrect(x0, 0, x1, H, 1)
        c.fill(body, zone=1)
        cl = c.mask(body)
        n = int(W / 14)
        for k in range(n):
            c.fill(rrect(x0 + k * 14, 0, x0 + k * 14 + 7, H, 0), zone=2, alpha=0.55, clip=cl)
        for j in range(int(H / 7) + 1):
            c.fill(rrect(x0, j * 7, x1, j * 7 + 3.5, 0), zone=2, alpha=0.45, clip=cl)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "picnic_basket":
        c.line(smooth([(-W * 0.3, H * 0.6), (0, H), (W * 0.3, H * 0.6)], closed=False), 1.4, zone=3)
        body = trap(x0 + 2, x1 - 2, 0, x0, x1, H * 0.62, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        for k in range(int(W / 4)):
            line(c, [(x0 + k * 4, 0), (x0 + k * 4 + 2, H * 0.62)], zone=1, clip=cl)
        c.fill(rrect(x0 - 1, H * 0.54, x1 + 1, H * 0.66, 1), zone=1, shade=0.95)
        c.fill(smooth([(-W * 0.2, H * 0.66), (W * 0.1, H * 0.62), (W * 0.2, H * 0.44), (-W * 0.1, H * 0.46)]), zone=2)
    elif style == "hose_reel":
        for x in (-W * 0.3, W * 0.2):
            c.fill(ell(x, H * 0.12, H * 0.12, H * 0.12, 16), zone=0, alpha=0.9)
        c.line([(-W * 0.3, H * 0.12), (0, H * 0.5), (W * 0.2, H * 0.12)], 1.4, zone=3)
        c.line([(0, H * 0.5), (W * 0.35, H)], 1.4, zone=3)
        for r in range(5):
            c.line(ell(0, H * 0.5, W * (0.36 - r * 0.05), H * (0.32 - r * 0.045), 40), 1.6, zone=1, closed=True)
        c.fill(ell(0, H * 0.5, W * 0.08, H * 0.08, 16), zone=2)
    elif style == "swing_set":                                      # Doppelschaukel mit A-Gestell
        for sx in (-1, 1):
            for dx in (-6, 6):
                c.line([(sx * W * 0.45 + dx, 0), (sx * W * 0.45, H)], 2.4, zone=3)
        c.fill(rrect(x0 + 2, H - 3, x1 - 2, H + 1, 1.5), zone=3)
        for k, x in enumerate((-W * 0.2, W * 0.2)):
            for dx in (-12, 12):
                c.line([(x + dx, H), (x + dx, H * 0.2)], 0.4, zone=0)
            seat = rrect(x - 16, H * 0.16, x + 16, H * 0.21, 1.5)
            shaded(c, seat, [1, 2][k], "bottom", SHADE, 0.35)
    elif style == "playhouse":
        c.fill(rrect(x0, 0, x1, 8, 0.6), zone=3)
        wall_top = H * 0.6
        body = rrect(x0 + 4, 6, x1 - 4, wall_top, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        for k in range(1, int(wall_top / 10)):
            line(c, [(x0 + 4, 6 + k * 10), (x1 - 4, 6 + k * 10)], zone=1, clip=cl)
        door = smooth([(-W * 0.14, 6, "s"), (W * 0.06, 6, "s"), (W * 0.06, wall_top * 0.7), (-W * 0.04, wall_top * 0.82), (-W * 0.14, wall_top * 0.7)])
        c.fill(door, zone=2)
        c.line(door, INNER, zone=0, closed=True)
        win = ell(W * 0.26, wall_top * 0.6, 8, 8, 24)
        c.fill(win, zone=2, shade=1.45)
        c.line([(W * 0.26 - 8, wall_top * 0.6), (W * 0.26 + 8, wall_top * 0.6)], 0.8, zone=2, shade=0.8)
        c.line(win, INNER, zone=0, closed=True)
        c.fill(rrect(W * 0.14, wall_top * 0.44, W * 0.38, wall_top * 0.48, 0.4), zone=2, shade=0.9)
        roof = [(x0 - 4, wall_top - 2), (x1 + 4, wall_top - 2), (0, H)]
        rcl = shaded(c, roof, 2, "bottom", SHADE, 0.2)
        for k in range(1, 5):
            y = wall_top + k * (H - wall_top) / 5
            line(c, [(x0, y - (H - wall_top) * 0.1), (x1, y - (H - wall_top) * 0.1)], zone=2, clip=rcl)
        c.fill(rrect(W * 0.18, H * 0.78, W * 0.3, H * 0.96, 0.6), zone=2, shade=0.8)                     # Schornstein
