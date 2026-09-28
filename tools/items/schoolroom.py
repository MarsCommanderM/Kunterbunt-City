"""
Schule & Pausenhof (P10a): Schulbank, Lehrerpult, Tafel mit Kreide-Bildern (Zustände), Spinde, Schulglocke,
Weltkarte, Notenständer, Triangel, Tamburin, Maltisch, Farbpalette, Tontopf, Labortisch, Vulkan-Experiment,
Erlenmeyer-Kolben, Skelett, Sprungkasten, Schwebebalken, Ringe, Ballwagen, Essensausgabe, Tablett, Hüpfkästchen,
Postfächer, Kopierer.  Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Holz.
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, ell, leg, line, rrect, shaded, smooth, trap

CHALK = 1.9          # Kreide = sehr helle Zone-2-Schattierung


def _chalk(c, pts, w: float = 0.7, closed: bool = False, clip=None):
    c.line(pts, w, zone=2, shade=CHALK, closed=closed, clip=clip)


def school(it: Item, style: str = "desk", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "desk":                                             # Schulbank (Zweier-Tisch) mit Ablage
        for x in (x0 + 4, x1 - 4):
            leg(c, x, 0, H - 4, 3.0, 2.4, zone=3)
        shelf = rrect(x0 + 2, H * 0.62, x1 - 2, H * 0.72, 0.6)
        c.fill(shelf, zone=1, shade=0.75)
        c.line(shelf, INNER, zone=0, closed=True)
        top = rrect(x0, H - 4, x1, H, 0.8)
        shaded(c, top, 1, "bottom", SHADE, 0.4)
        c.line(top, INNER, zone=0, closed=True)
    elif style == "teacher_desk":                                   # Lehrerpult mit Schubladen-Seite
        side = rrect(x1 - W * 0.36, 0, x1 - 2, H - 4, 0.8)
        shaded(c, side, 1, "right", SHADE, 0.2)
        for k in range(3):
            y = 4 + k * (H - 10) / 3
            d = rrect(x1 - W * 0.34, y + 1, x1 - 4, y + (H - 10) / 3 - 1, 0.6)
            c.fill(d, zone=1, shade=0.95)
            c.fill(rrect(x1 - W * 0.2 - 3, y + (H - 10) / 6 - 0.6, x1 - W * 0.2 + 3, y + (H - 10) / 6 + 0.6, 0.4), zone=3)
            c.line(d, INNER, zone=0, closed=True)
        leg(c, x0 + 4, 0, H - 4, 3.0, 2.4, zone=3)
        c.fill(rrect(x0 + 2, H * 0.3, x1 - W * 0.36, H - 4, 0.6), zone=1, shade=0.8)     # Blende
        top = rrect(x0 - 2, H - 4, x1 + 2, H, 0.8)
        c.fill(top, zone=2)
        c.line(top, INNER, zone=0, closed=True)
        c.line(side, INNER, zone=0, closed=True)
    elif style == "blackboard":                                     # Wandtafel (Wand-Item) – Kreide-Bild je Zustand
        frame = rrect(x0, H * 0.08, x1, H, 1.2)
        c.fill(frame, zone=3)
        board = rrect(x0 + 4, H * 0.12, x1 - 4, H - 4, 0.6)
        c.fill(board, zone=1)
        cl = c.mask(board)
        c.fill(rrect(x0 + 6, H * 0.12, x1 - 6, H * 0.35, 0.4), zone=1, shade=1.08, clip=cl, alpha=0.3)
        c.fill(rrect(x0 + 2, 0, x1 - 2, H * 0.1, 0.6), zone=3, shade=0.85)            # Kreideleiste
        for k, dx in enumerate((-W * 0.3, -W * 0.25, W * 0.2)):
            c.fill(rrect(dx, H * 0.1, dx + 7, H * 0.13, 0.5), zone=2, shade=[1.9, 1.5, 1.7][k])
        cx, cy, r = 0.0, H * 0.58, min(W, H) * 0.25
        if state == "sun":
            _chalk(c, ell(cx - W * 0.2, cy + r * 0.3, r * 0.4, r * 0.4, 28), 0.9, True, cl)
            for k in range(10):
                a = k * math.pi / 5
                _chalk(c, [(cx - W * 0.2 + math.cos(a) * r * 0.55, cy + r * 0.3 + math.sin(a) * r * 0.55),
                           (cx - W * 0.2 + math.cos(a) * r * 0.8, cy + r * 0.3 + math.sin(a) * r * 0.8)], 0.8, clip=cl)
            _chalk(c, [(cx, cy - r * 0.9), (cx + W * 0.1, cy - r * 0.2), (cx + W * 0.2, cy - r * 0.7), (cx + W * 0.3, cy - r * 0.1),
                       (cx + W * 0.38, cy - r * 0.9)], 0.8, clip=cl)           # Berge
        elif state == "house":
            _chalk(c, [(cx - r, cy - r), (cx + r, cy - r), (cx + r, cy + r * 0.3), (cx - r, cy + r * 0.3)], 0.9, True, cl)
            _chalk(c, [(cx - r * 1.2, cy + r * 0.3), (cx, cy + r * 1.2), (cx + r * 1.2, cy + r * 0.3)], 0.9, clip=cl)
            _chalk(c, [(cx - r * 0.2, cy - r), (cx - r * 0.2, cy - r * 0.2), (cx + r * 0.2, cy - r * 0.2), (cx + r * 0.2, cy - r)], 0.8,
                   clip=cl)
            _chalk(c, ell(cx + r * 0.6, cy, r * 0.18, r * 0.18, 16), 0.7, True, cl)
            _chalk(c, [(cx + W * 0.25, cy - r), (cx + W * 0.25, cy)], 0.9, clip=cl)
            _chalk(c, ell(cx + W * 0.25, cy + r * 0.3, r * 0.35, r * 0.35, 20), 0.8, True, cl)
        elif state == "cat":
            _chalk(c, ell(cx, cy - r * 0.3, r * 0.7, r * 0.55, 28), 0.9, True, cl)
            _chalk(c, ell(cx, cy + r * 0.55, r * 0.45, r * 0.4, 24), 0.9, True, cl)
            for sx in (-1, 1):
                _chalk(c, [(cx + sx * r * 0.2, cy + r * 0.85), (cx + sx * r * 0.35, cy + r * 1.15), (cx + sx * r * 0.42, cy + r * 0.75)],
                       0.8, clip=cl)
                c.fill(ell(cx + sx * r * 0.16, cy + r * 0.6, r * 0.05, r * 0.07, 10), zone=2, shade=CHALK, clip=cl)
                _chalk(c, [(cx + sx * r * 0.1, cy + r * 0.45), (cx + sx * r * 0.6, cy + r * 0.5)], 0.5, clip=cl)
            _chalk(c, smooth([(cx + r * 0.65, cy - r * 0.5), (cx + r * 1.1, cy - r * 0.2), (cx + r * 1.0, cy + r * 0.3)],
                             closed=False), 0.9, clip=cl)
        elif state == "shapes":                                     # Formen zählen: 1 Kreis, 2 Dreiecke, 3 Quadrate
            for k in range(1):
                _chalk(c, ell(x0 + W * 0.2, cy + r * 0.5, r * 0.25, r * 0.25, 20), 0.8, True, cl)
            for k in range(2):
                bx = x0 + W * 0.4 + k * r * 0.7
                _chalk(c, [(bx - r * 0.25, cy + r * 0.25), (bx + r * 0.25, cy + r * 0.25), (bx, cy + r * 0.75)], 0.8, True, cl)
            for k in range(3):
                bx = x0 + W * 0.2 + k * r * 0.7
                _chalk(c, [(bx - r * 0.22, cy - r * 0.8), (bx + r * 0.22, cy - r * 0.8), (bx + r * 0.22, cy - r * 0.36),
                           (bx - r * 0.22, cy - r * 0.36)], 0.8, True, cl)
            for k in range(3):                                      # Punkte-Würfel
                c.fill(ell(x1 - W * 0.22 + (k - 1) * r * 0.3, cy + (k - 1) * r * 0.3, r * 0.07, r * 0.07, 10), zone=2, shade=CHALK,
                       clip=cl)
            _chalk(c, [(x1 - W * 0.22 - r * 0.5, cy - r * 0.5), (x1 - W * 0.22 + r * 0.5, cy - r * 0.5), (x1 - W * 0.22 + r * 0.5,
                       cy + r * 0.5), (x1 - W * 0.22 - r * 0.5, cy + r * 0.5)], 0.8, True, cl)
        c.line(board, INNER, zone=0, closed=True)
    elif style == "locker":                                         # 3 Spinde, Tür auf (Jacke + Rucksack drin)
        n = 3
        cw = W / n
        for k in range(n):
            lx = x0 + k * cw
            box = rrect(lx + 0.5, 0, lx + cw - 0.5, H, 0.6)
            c.fill(box, zone=1, shade=1.0 - 0.04 * (k % 2))
            if state == "open" and k == 1:
                c.fill(rrect(lx + 2, 4, lx + cw - 2, H - 4, 0.4), zone=1, shade=0.45)
                c.fill(rrect(lx + cw * 0.25, H * 0.5, lx + cw * 0.75, H * 0.85, 2.0), zone=2)       # Jacke
                c.fill(rrect(lx + cw * 0.2, 6, lx + cw * 0.8, H * 0.3, 3.0), zone=2, shade=0.75)    # Rucksack
                door = [(lx + cw - 0.5, 0), (lx + cw + cw * 0.35, 4), (lx + cw + cw * 0.35, H - 4), (lx + cw - 0.5, H)]
                c.fill(door, zone=1, shade=0.88)
                c.line(door, INNER, zone=0, closed=True)
            else:
                for s in range(4):
                    line(c, [(lx + cw * 0.3, H * 0.82 + s * 2.2), (lx + cw * 0.7, H * 0.82 + s * 2.2)], zone=1, w=0.5)
                c.fill(rrect(lx + cw * 0.72, H * 0.5, lx + cw * 0.82, H * 0.58, 0.4), zone=3)
                c.fill(rrect(lx + cw * 0.3, H * 0.7, lx + cw * 0.7, H * 0.76, 0.4), zone=2)       # Namensschild (Farbe)
            c.line(box, INNER, zone=0, closed=True)
    elif style == "bell":                                           # Schulglocke (Wand)
        c.fill(rrect(-W * 0.12, H * 0.8, W * 0.12, H, 0.6), zone=3)
        bell = smooth([(-W * 0.45, H * 0.2, "s"), (W * 0.45, H * 0.2, "s"), (W * 0.35, H * 0.35), (W * 0.3, H * 0.7), (0, H * 0.85),
                       (-W * 0.3, H * 0.7), (-W * 0.35, H * 0.35)])
        shaded(c, bell, 1, "right", SHADE, 0.3)
        c.fill(ell(0, H * 0.12, W * 0.12, W * 0.12, 16), zone=3)
        if state == "ring":
            for sx in (-1, 1):
                for k in range(2):
                    c.line(smooth([(sx * W * (0.55 + k * 0.12), H * 0.3), (sx * W * (0.62 + k * 0.12), H * 0.5),
                                   (sx * W * (0.55 + k * 0.12), H * 0.7)], closed=False), 0.6, zone=2)
        c.line(bell, INNER, zone=0, closed=True)
    elif style == "world_map":                                      # Weltkarte (Wand): Meer + Kontinente
        frame = rrect(x0, 0, x1, H, 1.0)
        c.fill(frame, zone=3)
        sea = rrect(x0 + 3, 3, x1 - 3, H - 3, 0.5)
        c.fill(sea, zone=1)
        cl = c.mask(sea)
        rng = random.Random(4)
        for cx_, cy_, rr in ((-0.28, 0.62, 0.16), (-0.2, 0.3, 0.1), (0.05, 0.6, 0.12), (0.08, 0.35, 0.12), (0.3, 0.55, 0.18),
                             (0.33, 0.25, 0.07)):
            pts = [(cx_ * W + math.cos(k * 0.52) * rr * W * rng.uniform(0.7, 1.1),
                    cy_ * H + math.sin(k * 0.52) * rr * H * rng.uniform(0.9, 1.6)) for k in range(12)]
            c.fill(smooth(pts), zone=2, clip=cl)
        c.line(sea, INNER, zone=0, closed=True)
    elif style == "music_stand":
        c.line([(0, 4), (0, H * 0.7)], 1.2, zone=3)
        for sx in (-1, 0, 1):
            c.line([(0, 4), (sx * W * 0.35, 0)], 1.0, zone=3)
        desk = [(x0, H * 0.72), (x1, H * 0.72), (x1 - 2, H), (x0 + 2, H)]
        c.fill(desk, zone=3)
        c.fill(rrect(x0 + 4, H * 0.76, x1 - 4, H * 0.96, 0.4), zone=2, shade=1.4)            # Notenblatt
        for k in range(4):
            line(c, [(x0 + 6, H * 0.8 + k * H * 0.035), (x1 - 6, H * 0.8 + k * H * 0.035)], zone=3, w=0.3)
        for k in range(5):
            c.fill(ell(x0 + 9 + k * (W - 18) / 4, H * (0.81 + 0.035 * (k % 3)), 1.2, 0.9, 10), zone=0)
        c.line(desk, INNER, zone=0, closed=True)
    elif style == "triangle":
        c.line([(x0 + 7, 2), (x1 - 2, 2), (0, H - 4), (x0 + 2, 4)], 1.4, zone=1)      # Dreieck mit kleiner Lücke
        c.line([(0, H - 4), (0, H)], 0.6, zone=2)
        c.line([(x1 - 3, H * 0.6), (x1 + 2, H * 0.2)], 0.8, zone=3)
    elif style == "tambourine":
        rim = ell(0, H / 2, W / 2, H / 2, 36)
        c.fill(rim, zone=1)
        c.fill(ell(0, H / 2, W * 0.4, H * 0.4, 32), zone=2, shade=1.3)
        for k in range(6):
            a = k * math.pi / 3
            c.fill(ell(math.cos(a) * W * 0.45, H / 2 + math.sin(a) * H * 0.45, W * 0.06, W * 0.06, 12), zone=3)
        c.line(rim, INNER, zone=0, closed=True)
    elif style == "art_table":                                      # Maltisch mit Farbklecksen
        for x in (x0 + 4, x1 - 4):
            leg(c, x, 0, H - 4, 3.0, 2.4, zone=3)
        top = rrect(x0, H - 4, x1, H, 0.8)
        c.fill(top, zone=1)
        rng = random.Random(9)
        for k in range(6):
            c.fill(ell(rng.uniform(x0 + 6, x1 - 6), H - 2.2, rng.uniform(2, 4), 1.2, 12), zone=2,
                   shade=rng.choice([0.7, 1.0, 1.3]))
        c.line(top, INNER, zone=0, closed=True)
    elif style == "palette":                                        # Farbpalette mit Pinsel
        p = smooth([(x0, H * 0.4, "s"), (x0 + W * 0.2, 0, "s"), (x1 - W * 0.1, H * 0.1, "s"), (x1, H * 0.6, "s"),
                    (x1 - W * 0.2, H, "s"), (x0 + W * 0.2, H * 0.9, "s")])
        c.fill(p, zone=3)
        for k, (dx, dy) in enumerate(((0.45, 0.75), (0.65, 0.6), (0.72, 0.35), (0.5, 0.2), (0.3, 0.3))):
            c.fill(ell(x0 + W * dx, H * dy, W * 0.08, H * 0.1, 14), zone=1 if k % 2 else 2, shade=[1.0, 1.2, 0.8, 1.35, 0.9][k])
        c.line(p, INNER, zone=0, closed=True)
    elif style == "clay_pot":                                       # getöpferter Topf
        pot = smooth([(x0 + W * 0.2, 0, "s"), (x1 - W * 0.2, 0, "s"), (x1, H * 0.5), (x1 - W * 0.15, H * 0.85), (x1 - W * 0.1, H, "s"),
                       (x0 + W * 0.1, H, "s"), (x0 + W * 0.15, H * 0.85), (x0, H * 0.5)])
        cl = shaded(c, pot, 1, "right", SHADE, 0.3)
        for k in range(3):
            line(c, [(x0, H * (0.35 + k * 0.12)), (x1, H * (0.35 + k * 0.12))], zone=2, w=0.8, clip=cl)
        c.line(pot, INNER, zone=0, closed=True)
    elif style == "lab_table":                                      # Labortisch mit Becken und Hahn
        body = rrect(x0, 0, x1, H - 5, 0.8)
        shaded(c, body, 1, "right", SHADE, 0.15)
        for k in range(1, 3):
            line(c, [(x0 + k * W / 3, 4), (x0 + k * W / 3, H - 9)], zone=1)
        top = rrect(x0 - 2, H - 5, x1 + 2, H, 0.8)
        c.fill(top, zone=3, shade=0.4)
        c.fill(rrect(x1 - W * 0.3, H - 3, x1 - W * 0.1, H - 0.5, 0.6), zone=3, shade=0.9)
        c.line([(x1 - W * 0.2, H), (x1 - W * 0.2, H + 14), (x1 - W * 0.26, H + 14), (x1 - W * 0.26, H + 10)], 1.2, zone=3)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "volcano":                                        # Vulkan-Experiment (Zustand: bricht aus)
        c.fill(rrect(x0, 0, x1, H * 0.1, 1.0), zone=3)
        mtn = [(x0 + 3, H * 0.1), (x1 - 3, H * 0.1), (W * 0.12, H * 0.72), (-W * 0.12, H * 0.72)]
        cl = shaded(c, mtn, 1, "right", SHADE, 0.3)
        c.fill(ell(0, H * 0.72, W * 0.12, H * 0.03, 16), zone=0, shade=1.0)
        if state == "erupt":
            lava = smooth([(-W * 0.1, H * 0.72, "s"), (-W * 0.25, H * 0.95), (0, H * 1.25), (W * 0.25, H * 0.95), (W * 0.1, H * 0.72, "s")])
            c.fill(lava, zone=2)
            for sx in (-1, 1):
                c.fill(smooth([(sx * W * 0.1, H * 0.72, "s"), (sx * W * 0.2, H * 0.5), (sx * W * 0.14, H * 0.45, "s")]), zone=2,
                       clip=cl)
            for k in range(5):
                c.fill(ell((k - 2) * W * 0.12, H * (1.3 + 0.06 * (k % 2)), W * 0.05, W * 0.05, 12), zone=2, shade=1.3)
        c.line(mtn, INNER, zone=0, closed=True)
    elif style == "flask":                                          # Erlenmeyer-Kolben (Zustand: blubbert)
        f = [(x0 + 1, 0), (x1 - 1, 0), (W * 0.15, H * 0.7), (W * 0.15, H), (-W * 0.15, H), (-W * 0.15, H * 0.7)]
        c.fill(f, zone=3, shade=1.6)
        c.fill([(x0 + 2, 1), (x1 - 2, 1), (W * 0.3, H * 0.45), (-W * 0.3, H * 0.45)], zone=1)
        if state == "bubble":
            for k in range(5):
                c.line(ell((k - 2) * W * 0.1, H * (1.05 + 0.08 * k), W * 0.06, W * 0.06, 12), 0.3, zone=1, closed=True)
        c.line(f, INNER, zone=0, closed=True)
    elif style == "skeleton":                                       # Anschauungs-Skelett (freundlich, lächelt)
        c.line([(0, 0), (0, 10)], 1.4, zone=3)
        c.fill(ell(0, 2, W * 0.35, 2, 16), zone=3)
        c.line([(0, 10), (0, H * 0.75)], 1.4, zone=1)
        for k in range(5):
            c.line(smooth([(-W * 0.22, H * (0.52 + k * 0.045)), (0, H * (0.54 + k * 0.045)), (W * 0.22, H * (0.52 + k * 0.045))],
                          closed=False), 0.9, zone=1)
        for sx in (-1, 1):
            c.line([(sx * W * 0.12, H * 0.45), (sx * W * 0.18, H * 0.22), (sx * W * 0.2, H * 0.04)], 1.0, zone=1)
            c.line([(sx * W * 0.25, H * 0.73), (sx * W * 0.35, H * 0.55), (sx * W * 0.33, H * 0.4)], 0.9, zone=1)
        c.fill(ell(0, H * 0.45, W * 0.18, H * 0.04, 16), zone=1)
        head = ell(0, H * 0.86, W * 0.2, H * 0.1, 24)
        c.fill(head, zone=1)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.07, H * 0.87, W * 0.05, H * 0.03, 12), zone=0)
        c.line(smooth([(-W * 0.08, H * 0.81), (0, H * 0.79), (W * 0.08, H * 0.81)], closed=False), 0.4, zone=0)
        c.line(head, INNER, zone=0, closed=True)
    elif style == "vault_box":                                      # Sprungkasten (Turnhalle)
        n = 4
        for k in range(n):
            y0, y1 = k * (H - 10) / n, (k + 1) * (H - 10) / n
            ww = W * (1 - 0.06 * k)
            seg = rrect(-ww / 2, y0, ww / 2, y1 - 0.4, 0.8)
            c.fill(seg, zone=3)
            c.fill(rrect(-ww * 0.2, (y0 + y1) / 2 - 2, ww * 0.2, (y0 + y1) / 2 + 2, 1.0), zone=3, shade=0.6)
            c.line(seg, INNER, zone=0, closed=True)
        topp = rrect(-W * 0.42, H - 10, W * 0.42, H, 3.0)
        shaded(c, topp, 1, "bottom", SHADE, 0.35)
        c.line(topp, INNER, zone=0, closed=True)
    elif style == "balance_beam":
        for x in (x0 + 20, x1 - 20):
            c.fill(trap(x - 10, x + 10, 0, x - 4, x + 4, H - 10, 0.6), zone=3)
        beam = rrect(x0, H - 10, x1, H, 1.0)
        shaded(c, beam, 1, "bottom", SHADE, 0.3)
        c.line(beam, INNER, zone=0, closed=True)
    elif style == "ball_cart":                                      # Ballwagen voller Bälle
        cart = rrect(x0, 12, x1, H * 0.7, 1.2)
        for wx in (x0 + 8, x1 - 8):
            c.fill(ell(wx, 5, 5, 5, 16), zone=0)
        rng = random.Random(3)
        for k in range(9):
            bx = x0 + 10 + (k % 5) * (W - 20) / 4 + (k // 5) * 6
            by = H * 0.72 + (k // 5) * 10 + rng.uniform(-2, 2)
            c.fill(ell(bx, by, 9, 9, 20), zone=2, shade=[0.8, 1.0, 1.25][k % 3])
        for k in range(8):
            c.line([(x0 + k * W / 7, 12), (x0 + k * W / 7, H * 0.7)], 0.8, zone=1)
        c.line(cart, 1.4, zone=1, closed=True)
    elif style == "serving_counter":                                # Essensausgabe mit Wärmebehältern
        body = rrect(x0, 0, x1, H - 5, 0.8)
        shaded(c, body, 1, "right", SHADE, 0.15)
        top = rrect(x0 - 2, H - 5, x1 + 2, H, 0.8)
        c.fill(top, zone=3)
        n = max(3, int(W / 45))
        for k in range(n):
            tx = x0 + (k + 0.5) * W / n
            c.fill(rrect(tx - W / n * 0.4, H - 1, tx + W / n * 0.4, H + 6, 1.0), zone=3, shade=0.8)
            c.fill(ell(tx, H + 6, W / n * 0.36, 2.5, 16), zone=2, shade=[1.0, 1.3, 0.8, 1.15][k % 4])
        c.fill(rrect(x0, H + 22, x1, H + 25, 0.5), zone=3, shade=1.5, alpha=0.6)         # Spuckschutz
        for x in (x0 + 2, x1 - 2):
            c.line([(x, H), (x, H + 25)], 0.8, zone=3)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "tray":
        t = rrect(x0, 0, x1, H, H * 0.4)
        shaded(c, t, 1, "bottom", SHADE, 0.5)
        c.line(t, INNER, zone=0, closed=True)
    elif style == "hopscotch":                                      # Hüpfkästchen flach auf dem Boden (Aufsicht, perspektivisch flach)
        cells = [(0, 0, 1), (1, 0, 1), (2, 0, 0.5), (2, 0.5, 0.5), (3, 0, 1), (4, 0, 0.5), (4, 0.5, 0.5), (5, 0, 1)]
        cw = W / 6.0
        for k, (gx, gy, gh) in enumerate(cells):
            b = rrect(x0 + gx * cw + 0.8, gy * H + 0.6, x0 + (gx + 1) * cw - 0.8, (gy + gh) * H - 0.6, 0.6)
            c.fill(b, zone=1 if k % 2 else 2)
            c.line(b, 0.8, zone=3, shade=1.8, closed=True)
            for d in range(k % 3 + 1):                              # Punkte statt Zahlen (R-07)
                c.fill(ell(x0 + (gx + 0.5) * cw + (d - (k % 3) / 2) * cw * 0.2, (gy + gh / 2) * H, cw * 0.06, H * gh * 0.12, 10),
                       zone=3, shade=1.8)
    elif style == "cubbies":                                        # Postfächer im Lehrerzimmer (Wand)
        frame = rrect(x0, 0, x1, H, 0.8)
        c.fill(frame, zone=1)
        for i in range(4):
            for j in range(3):
                cx0 = x0 + 2 + i * (W - 4) / 4
                cy0 = 2 + j * (H - 4) / 3
                cell = rrect(cx0 + 0.6, cy0 + 0.6, cx0 + (W - 4) / 4 - 0.6, cy0 + (H - 4) / 3 - 0.6, 0.3)
                c.fill(cell, zone=1, shade=0.5)
                if (i + j) % 2 == 0:
                    c.fill(rrect(cx0 + 2, cy0 + 1, cx0 + (W - 4) / 4 - 3, cy0 + (H - 4) / 3 * 0.6, 0.3), zone=2, shade=1.5)
        c.line(frame, INNER, zone=0, closed=True)
    elif style == "copier":                                         # Kopierer
        body = rrect(x0, 0, x1, H * 0.8, 1.2)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 + 4, H * 0.8, x1 - 4, H * 0.88, 0.8), zone=1, shade=0.9)
        c.fill(rrect(x0 + 8, H * 0.88, x0 + W * 0.6, H, 0.8), zone=3, shade=0.8)
        c.fill(rrect(x1 - W * 0.3, H * 0.82, x1 - 6, H * 0.87, 0.5), zone=2)
        c.fill(rrect(x0 - 6, H * 0.55, x0 + 2, H * 0.6, 0.4), zone=2, shade=1.5)         # Papier kommt raus
        for k in range(3):
            c.fill(rrect(x0 + 6, H * (0.1 + k * 0.2), x1 - 6, H * (0.26 + k * 0.2), 0.6), zone=1, shade=0.95)
        c.line(body, INNER, zone=0, closed=True)
