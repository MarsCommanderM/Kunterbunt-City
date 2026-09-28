"""
Sport, Freizeit, Kleidung & Musik (P07-Inventar, Wunsch 👤): Inliner, Rollschuhe, Schoner, Kindersitze, Laufrad,
Fahrradanhänger, Tischtennis, Badminton, Mini-Tor, Ski, Snowboard, Angel, Springseil, Hula-Hoop, Frisbee;
Schal, Mütze, Handschuhe, Basecap, Regenjacke, Sonnenbrille, Rucksack, Handtasche; Schlagzeug, Keyboard, Geige, Flöte.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Holz/Details.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, ell, knob, leg, line, rrect, shaded, smooth, trap


def _wheel(c, x: float, y: float, r: float, spokes: int = 0, zone_rim: int = 3):
    c.fill(ell(x, y, r, r, 32), zone=0, alpha=0.95)
    c.fill(ell(x, y, r * 0.55, r * 0.55, 24), zone=zone_rim)
    for k in range(spokes):
        a = math.pi * k / spokes
        c.line([(x - math.cos(a) * r * 0.8, y - math.sin(a) * r * 0.8), (x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8)],
               0.15, zone=3)


def sporty(it: Item, style: str = "inline_skates", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style in ("inline_skates", "roller_skates"):
        for dx, sh in ((W * 0.1, 0.85), (-W * 0.08, 1.0)):
            if style == "inline_skates":
                for k in range(4):
                    c.fill(ell(x0 * 0.8 + dx + k * W * 0.22, H * 0.09, H * 0.09, H * 0.09, 20), zone=2, shade=sh)
                    c.line(ell(x0 * 0.8 + dx + k * W * 0.22, H * 0.09, H * 0.09, H * 0.09, 20), INNER, zone=0, closed=True)
                c.fill(rrect(x0 * 0.9 + dx, H * 0.15, W * 0.4 + dx, H * 0.22, 0.6), zone=3, shade=sh)
            else:
                for k in (0, 1):
                    c.fill(ell(x0 * 0.6 + dx + k * W * 0.55, H * 0.1, H * 0.1, H * 0.1, 20), zone=2, shade=sh)
                    c.line(ell(x0 * 0.6 + dx + k * W * 0.55, H * 0.1, H * 0.1, H * 0.1, 20), INNER, zone=0, closed=True)
                c.fill(rrect(x0 * 0.9 + dx, H * 0.16, W * 0.42 + dx, H * 0.23, 0.6), zone=3, shade=sh)
                c.fill(ell(W * 0.46 + dx, H * 0.2, 1.4, 1.4, 12), zone=2, shade=sh * 0.8)       # Stopper
            boot = smooth([(x0 * 0.9 + dx, H * 0.22, "s"), (W * 0.42 + dx, H * 0.22, "s"), (W * 0.42 + dx, H * 0.4), (W * 0.05 + dx, H * 0.55),
                           (W * 0.02 + dx, H, "s"), (-W * 0.36 + dx, H, "s"), (x0 * 0.9 + dx, H * 0.5)])
            shaded(c, boot, 1, "right", SHADE * sh, 0.3)
            for k in range(3):
                c.line([(-W * 0.3 + dx, H * (0.5 + k * 0.14)), (W * 0.0 + dx, H * (0.55 + k * 0.14))], 0.8, zone=2, shade=sh)
    elif style == "pads":                                          # Knie- und Ellenbogenschoner + Handgelenk
        for k, (x, s) in enumerate(((-W * 0.3, 1.0), (0, 0.85), (W * 0.3, 0.7))):
            pad = rrect(x - W * 0.14 * s, 0, x + W * 0.14 * s, H * s, W * 0.08)
            shaded(c, pad, 2, "right", SHADE, 0.25)
            c.fill(ell(x, H * s * 0.55, W * 0.1 * s, H * s * 0.28, 20), zone=1)
            c.line(ell(x, H * s * 0.55, W * 0.1 * s, H * s * 0.28, 20), INNER, zone=0, closed=True)
            c.fill(rrect(x - W * 0.14 * s, H * s * 0.12, x + W * 0.14 * s, H * s * 0.2, 0.4), zone=3)
    elif style == "bike_seat":                                     # Fahrrad-Kindersitz
        c.line([(W * 0.1, 0), (W * 0.1, H * 0.3), (W * 0.35, H * 0.3)], 1.4, zone=3)
        shell = smooth([(-W * 0.4, H * 0.35, "s"), (W * 0.3, H * 0.3, "s"), (W * 0.35, H * 0.5), (W * 0.1, H * 0.55),
                        (-W * 0.25, H, "s"), (x0, H * 0.95, "s")])
        shaded(c, shell, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.3, H * 0.45, W * 0.1, H * 0.55, 1.5), zone=2)
        c.fill(rrect(-W * 0.38, H * 0.55, -W * 0.28, H * 0.9, 1.5), zone=2)
        c.line([(-W * 0.15, H * 0.9), (-W * 0.05, H * 0.55)], 0.8, zone=3)
    elif style == "car_seat":                                      # Auto-Kindersitz (Vorderansicht): Schale, Kopfstütze, Gurte
        base = trap(x0, x1, 0, x0 + 3, x1 - 3, H * 0.18, 2)
        shaded(c, base, 1, "bottom", SHADE, 0.35)
        shell = smooth([(x0 + 2, H * 0.16, "s"), (x1 - 2, H * 0.16, "s"), (x1, H * 0.5), (W * 0.42, H * 0.72), (W * 0.4, H, "s"),
                        (-W * 0.4, H, "s"), (-W * 0.42, H * 0.72), (x0, H * 0.5)])
        shaded(c, shell, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.3, H * 0.2, W * 0.3, H * 0.66, 5), zone=2)
        head = rrect(-W * 0.32, H * 0.7, W * 0.32, H * 0.96, 6)
        shaded(c, head, 2, "bottom", SHADE, 0.3)
        for sx in (-1, 1):
            c.line([(sx * W * 0.14, H * 0.66), (sx * W * 0.05, H * 0.36)], 1.4, zone=3, shade=0.6)
        c.fill(rrect(-W * 0.08, H * 0.3, W * 0.08, H * 0.38, 1), zone=3, shade=1.4)
        c.line([(0, H * 0.3), (0, H * 0.2)], 1.4, zone=3, shade=0.6)
    elif style == "balance_bike":
        for x in (-W * 0.32, W * 0.32):
            _wheel(c, x, H * 0.28, H * 0.28, 0)
        c.line([(-W * 0.32, H * 0.28), (-W * 0.1, H * 0.62), (W * 0.2, H * 0.62), (W * 0.32, H * 0.28)], 2.2, zone=1)
        c.line([(W * 0.2, H * 0.62), (W * 0.14, H)], 1.6, zone=1)
        c.line([(W * 0.04, H), (W * 0.24, H)], 1.6, zone=2)
        c.fill(rrect(-W * 0.24, H * 0.64, -W * 0.02, H * 0.72, 1.2), zone=2)
    elif style == "bike_trailer":
        _wheel(c, -W * 0.1, H * 0.2, H * 0.2, 8)
        c.line([(W * 0.2, H * 0.25), (x1, H * 0.2)], 1.2, zone=3)
        body = smooth([(x0, H * 0.2, "s"), (W * 0.25, H * 0.2, "s"), (W * 0.2, H * 0.7), (-W * 0.1, H), (x0, H * 0.9)])
        cl = shaded(c, body, 1, "bottom", SHADE, 0.2)
        c.fill(smooth([(-W * 0.35, H * 0.35), (W * 0.1, H * 0.35), (W * 0.05, H * 0.7), (-W * 0.15, H * 0.85), (-W * 0.35, H * 0.8)]),
               zone=2, clip=cl)
        c.line([(x0 + 3, H * 0.9), (x0 + 3, H * 1.3)], 0.5, zone=3)
        c.fill([(x0 + 3, H * 1.3), (x0 + 12, H * 1.25), (x0 + 3, H * 1.2)], zone=2, shade=1.2)       # Fähnchen
    elif style == "table_tennis":
        for sx in (-1, 1):
            leg(c, sx * W * 0.4, 0, H * 0.94, 3, 3)
            c.line([(sx * W * 0.4, H * 0.1), (sx * W * 0.2, H * 0.1)], 1.0, zone=3)
        top = rrect(x0, H * 0.93, x1, H, 0.6)
        cl = shaded(c, top, 1, "bottom", SHADE, 0.4)
        line(c, [(x0 + 1, H * 0.995), (x1 - 1, H * 0.995)], zone=2, shade=1.4, w=0.4, clip=cl)
        c.glass(rrect(-0.6, H, 0.6, H + 15.25, 0.2), zone=2, opacity=0.5)
        c.line([(0, H), (0, H + 15.25)], 0.6, zone=3)
        c.fill(rrect(-W * 0.02, H + 14, W * 0.02, H + 15.5, 0.3), zone=2)
    elif style in ("tt_paddle", "badminton"):
        if style == "tt_paddle":
            c.fill(rrect(-W * 0.12, 0, W * 0.12, H * 0.4, 1), zone=3)
            head = ell(0, H * 0.68, W / 2, H * 0.32, 40)
            shaded(c, head, 1, "bottom", SHADE, 0.25)
            c.ellipse(W * 0.4, H * 0.95, 1.8, 1.8, zone=2, shade=1.3)
        else:
            c.line([(0, 0), (0, H * 0.55)], 0.9, zone=3)
            c.fill(rrect(-W * 0.1, 0, W * 0.1, H * 0.26, 0.8), zone=2)
            head = ell(0, H * 0.76, W * 0.42, H * 0.23, 36)
            c.line(head, 1.0, zone=1, closed=True)
            cl = c.mask(head)
            for k in range(-5, 6):
                c.line([(k * W * 0.08, H * 0.5), (k * W * 0.08, H)], 0.12, zone=3, shade=1.4, clip=cl)
                c.line([(x0, H * 0.76 + k * H * 0.04), (x1, H * 0.76 + k * H * 0.04)], 0.12, zone=3, shade=1.4, clip=cl)
            c.fill(ell(W * 0.7, H * 0.3, 1.2, 1.2, 12), zone=3, shade=1.5)                         # Federball
            c.fill(trap(W * 0.62, W * 0.78, H * 0.32, W * 0.58, W * 0.82, H * 0.42, 0.3), zone=3, shade=1.8)
    elif style == "goal_small":                                   # Mini-Tor mit Netz
        d = H * 0.3
        c.line([(x0, 0), (x0, H), (x1, H), (x1, 0)], 2.0, zone=1)
        for k in range(1, 10):
            c.line([(x0 + k * W / 10, H), (x0 + k * W / 10 + d * 0.4, H + d * 0.3)], 0.15, zone=2)
            c.line([(x0 + k * W / 10, 0), (x0 + k * W / 10, H)], 0.15, zone=2)
        for k in range(1, 6):
            c.line([(x0, k * H / 6), (x1, k * H / 6)], 0.15, zone=2)
        c.line([(x0, H), (x0 + d * 0.4, H + d * 0.3), (x1 + d * 0.4, H + d * 0.3), (x1, H)], 0.8, zone=1, shade=0.8)
    elif style in ("skis", "snowboard"):
        if style == "skis":
            for dx in (-W * 0.2, W * 0.2):
                ski = smooth([(dx - W * 0.16, 0, "s"), (dx + W * 0.16, 0, "s"), (dx + W * 0.16, H * 0.92), (dx, H, "s"), (dx - W * 0.16, H * 0.92)])
                shaded(c, ski, 1, "right", SHADE, 0.3)
                c.fill(rrect(dx - W * 0.16, H * 0.4, dx + W * 0.16, H * 0.52, 0.5), zone=3)
                c.fill(rrect(dx - W * 0.04, H * 0.05, dx + W * 0.04, H * 0.85, 0.5), zone=2)
        else:
            board = rrect(x0, 0, x1, H, W * 0.48)
            cl = shaded(c, board, 1, "right", SHADE, 0.3)
            c.fill(ell(0, H * 0.5, W * 0.3, H * 0.14, 28), zone=2, clip=cl)
            for y in (H * 0.3, H * 0.66):
                c.fill(rrect(-W * 0.4, y, W * 0.4, y + H * 0.06, 1), zone=3)
    elif style == "fishing_rod":
        c.line([(0, 0), (W * 0.45, H)], 0.9, zone=1)
        c.fill(rrect(-1.2, 0, 1.2, H * 0.22, 0.8), zone=3)
        c.fill(ell(W * 0.08, H * 0.2, W * 0.08, W * 0.08, 16), zone=2)
        c.line([(W * 0.45, H), (W * 0.48, H * 0.3)], 0.12, zone=0)
        c.fill(ell(W * 0.48, H * 0.3, 1.4, 1.8, 12), zone=2, shade=1.2)
    elif style == "jump_rope":
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.4 - 1.4, 0, sx * W * 0.4 + 1.4, H * 0.45, 1.2), zone=2)
        c.line(smooth([(-W * 0.4, H * 0.45), (-W * 0.3, H), (0, H * 0.6), (W * 0.2, H * 0.95), (W * 0.4, H * 0.45)], closed=False),
               0.7, zone=1)
    elif style == "hoop":
        c.line(ell(0, H / 2, W / 2 - 1, H / 2 - 1, 64), 2.2, zone=1, closed=True)
        for k in range(8):
            a = k * math.pi / 4
            c.fill(ell(math.cos(a) * (W / 2 - 1), H / 2 + math.sin(a) * (H / 2 - 1), 1.8, 1.8, 12), zone=2)
    elif style == "frisbee":
        disc = ell(0, H * 0.5, W / 2, H / 2, 40)
        shaded(c, disc, 1, "bottom", SHADE, 0.45)
        c.fill(ell(0, H * 0.62, W * 0.3, H * 0.2, 28), zone=2)


def outfit(it: Item, style: str = "scarf", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "scarf":                                          # zusammengelegt mit Fransen
        body = smooth([(x0, H * 0.3), (W * 0.2, H * 0.3), (W * 0.3, H * 0.6), (x1, H * 0.62), (x1, H), (-W * 0.2, H), (x0, H * 0.6)])
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        for k in range(8):
            c.fill(rrect(x0 + k * W / 8, 0, x0 + k * W / 8 + W / 16, H, 0), zone=2, clip=cl)
        tail = rrect(W * 0.05, 0, W * 0.3, H * 0.34, 1)
        shaded(c, tail, 1, "right", SHADE, 0.3)
        for k in range(5):
            c.line([(W * 0.07 + k * W * 0.05, 0), (W * 0.07 + k * W * 0.05, -2.5)], 0.5, zone=1)
    elif style == "beanie":
        cap = smooth([(x0, H * 0.25, "s"), (x1, H * 0.25, "s"), (W * 0.42, H * 0.65), (0, H * 0.85), (-W * 0.42, H * 0.65)])
        cl = shaded(c, cap, 1, "right", SHADE, 0.25)
        for k in range(1, 8):
            line(c, [(x0 + k * W / 8, H * 0.25), (x0 + k * W / 8 * 0.9 + W * 0.05, H * 0.8)], zone=1, clip=cl)
        c.fill(rrect(x0 - 0.5, 0, x1 + 0.5, H * 0.3, 2), zone=2)
        c.line(rrect(x0 - 0.5, 0, x1 + 0.5, H * 0.3, 2), INNER, zone=0, closed=True)
        c.fill(ell(0, H * 0.88, W * 0.16, H * 0.13, 20), zone=2, shade=1.05)
    elif style in ("gloves", "mittens"):
        for dx, sh in ((W * 0.18, 0.86), (-W * 0.14, 1.0)):
            if style == "mittens":
                hand = smooth([(dx - W * 0.22, 0, "s"), (dx + W * 0.22, 0, "s"), (dx + W * 0.26, H * 0.6), (dx + W * 0.1, H), (dx - W * 0.2, H * 0.85)])
                thumb = ell(dx - W * 0.28, H * 0.5, W * 0.1, H * 0.18, 16)
                shaded(c, thumb, 1, "bottom", SHADE * sh, 0.3)
            else:
                hand = smooth([(dx - W * 0.2, 0, "s"), (dx + W * 0.2, 0, "s"), (dx + W * 0.22, H * 0.55)] +
                              [(dx + W * (0.18 - k * 0.1), H * (0.95 - abs(k - 1.5) * 0.06)) for k in range(4)] + [(dx - W * 0.22, H * 0.5)])
                c.fill(ell(dx - W * 0.28, H * 0.45, W * 0.08, H * 0.16, 16), zone=1, shade=0.95 * sh)
            shaded(c, hand, 1, "right", SHADE * sh, 0.3)
            c.fill(rrect(dx - W * 0.22, 0, dx + W * 0.22, H * 0.18, 1.2), zone=2, shade=sh)
    elif style == "cap":
        c.fill(smooth([(0, H * 0.2), (x1, H * 0.12), (x1 - 1, H * 0.25), (W * 0.1, H * 0.34)]), zone=2)
        crown = smooth([(-W * 0.4, H * 0.2, "s"), (W * 0.2, H * 0.2, "s"), (W * 0.18, H * 0.7), (-W * 0.1, H), (-W * 0.38, H * 0.7)])
        shaded(c, crown, 1, "right", SHADE, 0.25)
        c.fill(ell(-W * 0.1, H * 0.98, 1.4, 1.2, 12), zone=2)
        c.fill(ell(-W * 0.1, H * 0.55, W * 0.1, H * 0.12, 20), zone=2)
    elif style == "raincoat":
        pts = smooth([(-W * 0.3, 0, "s"), (W * 0.3, 0, "s"), (W * 0.3, H * 0.6, "s"), (W * 0.46, H * 0.1, "s"), (x1, H * 0.12, "s"),
                      (W * 0.4, H * 0.8, "s"), (W * 0.16, H * 0.9), (0, H), (-W * 0.16, H * 0.9), (-W * 0.4, H * 0.8, "s"), (x0, H * 0.12, "s"),
                      (-W * 0.46, H * 0.1, "s"), (-W * 0.3, H * 0.6, "s")], n=3)
        shaded(c, pts, 1, "right", SHADE, 0.25)
        c.fill(smooth([(-W * 0.2, H * 0.84), (0, H), (W * 0.2, H * 0.84), (0, H * 0.78)]), zone=1, shade=0.85)
        for k in range(4):
            c.ellipse(W * 0.04, H * (0.2 + k * 0.15), 1.2, 1.2, zone=2)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.22 - 4, H * 0.18, sx * W * 0.22 + 4, H * 0.3, 1), zone=1, shade=0.88)
    elif style == "sunglasses":
        for sx in (-1, 1):
            lens = ell(sx * W * 0.25, H * 0.45, W * 0.22, H * 0.42, 28)
            c.fill(lens, zone=2, shade=0.55)
            c.fill(ell(sx * W * 0.25 - W * 0.06, H * 0.6, W * 0.06, H * 0.1, 12), zone=2, shade=1.3, alpha=0.6)
            c.line(lens, 1.1, zone=1, closed=True)
        c.line(smooth([(-W * 0.06, H * 0.6), (0, H * 0.7), (W * 0.06, H * 0.6)], closed=False), 1.0, zone=1)
    elif style == "backpack":
        c.line(smooth([(-W * 0.2, H * 0.9), (0, H * 1.08), (W * 0.2, H * 0.9)], closed=False), 1.4, zone=3)
        body = rrect(x0, 0, x1, H * 0.95, W * 0.3)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W * 0.34, H * 0.08, W * 0.34, H * 0.46, W * 0.14), zone=2, clip=cl)
        c.line(rrect(-W * 0.34, H * 0.08, W * 0.34, H * 0.46, W * 0.14), INNER, zone=0, closed=True)
        c.line(smooth([(x0 + 3, H * 0.7), (0, H * 0.9), (x1 - 3, H * 0.7)], closed=False), 0.5, zone=3)
        c.fill(ell(W * 0.1, H * 0.62, W * 0.1, W * 0.1, 16), zone=2, shade=1.2)                     # Anstecker
    elif style == "handbag":
        c.line(smooth([(-W * 0.3, H * 0.6), (0, H), (W * 0.3, H * 0.6)], closed=False), 1.2, zone=3)
        body = trap(x0, x1, 0, -W * 0.4, W * 0.4, H * 0.62, 1.5)
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(trap(-W * 0.4, W * 0.4, H * 0.4, -W * 0.4, W * 0.4, H * 0.62, 1), zone=1, shade=0.9)
        c.fill(rrect(-2, H * 0.36, 2, H * 0.46, 0.6), zone=2)


def music(it: Item, style: str = "drums", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "drums":
        c.fill(ell(-W * 0.3, H * 0.7, W * 0.16, H * 0.03, 20), zone=3, shade=1.2)                       # Becken
        c.line([(-W * 0.3, H * 0.7), (-W * 0.34, 0)], 0.8, zone=3)
        for x, y, r, h in ((W * 0.28, H * 0.3, W * 0.16, H * 0.2), (-W * 0.12, H * 0.45, W * 0.12, H * 0.14), (W * 0.1, H * 0.5, W * 0.11, H * 0.13)):
            c.fill(rrect(x - r, y - h / 2, x + r, y + h / 2, 1), zone=1)
            c.fill(rrect(x - r, y + h / 2 - 1.5, x + r, y + h / 2, 0.6), zone=3)
            c.fill(ell(x, y + h / 2, r, 1.5, 20), zone=2, shade=1.2)
            c.line(rrect(x - r, y - h / 2, x + r, y + h / 2, 1), INNER, zone=0, closed=True)
        bass = ell(0, H * 0.22, W * 0.24, H * 0.22, 40)
        shaded(c, bass, 1, "right", SHADE, 0.2)
        c.fill(ell(0, H * 0.22, W * 0.19, H * 0.17, 36), zone=2, shade=1.15)
        c.line(ell(0, H * 0.22, W * 0.19, H * 0.17, 36), INNER, zone=0, closed=True)
        for sx in (-1, 1):
            c.line([(sx * W * 0.2, 0), (sx * W * 0.12, H * 0.06)], 0.8, zone=3)
    elif style == "keyboard":
        for sx in (-1, 1):
            c.line([(sx * W * 0.35, 0), (-sx * W * 0.2, H * 0.72)], 1.2, zone=3)
        body = rrect(x0, H * 0.7, x1, H, 1.5)
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        keys = rrect(x0 + 3, H * 0.72, x1 - 3, H * 0.86, 0.4)
        c.fill(keys, zone=2)
        for k in range(int((W - 6) / 2.4)):
            x = x0 + 3 + k * 2.4
            c.line([(x, H * 0.72), (x, H * 0.86)], 0.15, zone=0)
            if k % 7 not in (2, 6):
                c.fill(rrect(x + 1.4, H * 0.79, x + 2.8, H * 0.86, 0.2), zone=0)
        for k in range(4):
            c.ellipse(x0 + 8 + k * 5, H * 0.93, 1.1, 1.1, zone=3)
    elif style == "violin":
        c.fill(rrect(-W * 0.06, H * 0.55, W * 0.06, H * 0.92, 0.5), zone=3, shade=0.5)
        c.fill(ell(0, H * 0.95, W * 0.1, H * 0.05, 12), zone=1, shade=0.8)
        body = smooth([(0, H * 0.58), (W * 0.42, H * 0.52), (W * 0.3, H * 0.34), (x1, H * 0.16), (0, 0), (x0, H * 0.16), (-W * 0.3, H * 0.34),
                       (-W * 0.42, H * 0.52)])
        shaded(c, body, 1, "right", SHADE, 0.25)
        for sx in (-1, 1):
            c.line(smooth([(sx * W * 0.12, H * 0.38), (sx * W * 0.18, H * 0.3), (sx * W * 0.12, H * 0.22)], closed=False), 0.5, zone=0)
        c.fill(rrect(-W * 0.12, H * 0.12, W * 0.12, H * 0.15, 0.3), zone=3, shade=0.5)
        c.line([(x1 + 2, 0), (x0 - 2, H * 0.9)], 0.5, zone=2)                                            # Bogen
    elif style == "flute":                                        # Blockflöte
        body = trap(-W * 0.3, W * 0.3, 0, -W * 0.38, W * 0.38, H * 0.88, 0.8)
        shaded(c, body, 1, "right", SHADE, 0.3)
        c.fill(trap(-W * 0.38, W * 0.38, H * 0.86, -W * 0.3, W * 0.3, H, 1), zone=2)
        for k in range(6):
            c.ellipse(0, H * (0.2 + k * 0.1), W * 0.12, W * 0.12, zone=0)
        c.fill(rrect(-W * 0.2, H * 0.8, W * 0.2, H * 0.84, 0.3), zone=0, alpha=0.8)
