"""
Möbel, Teil 2 (P07-Inventar, Wunsch 👤): Betten (Himmelbett, Hochbett, Schlafsofa, Tagesbett), Tische in allen Formen
(oval, quadratisch, lang, ausziehbar, Klapp-, Bistro-, Bar-, Konsolen-, runder Couchtisch, Satztische), Ohrensessel,
Fernsehsessel, Klappstuhl, Eckbank, Hocker (Tritt-, Klavier-, Melk-, Fuß-), Gardinenstange, Raffrollo, Jalousie.
Zonen: 1 = Hauptfarbe/Polster · 2 = Zweitfarbe/Stoff · 3 = Holz/Metall.
"""
from __future__ import annotations

import math

from . import furniture as F
from .kit import INNER, SHADE, SOFT, Item, cushion, ell, grain, knob, leg, line, rrect, shaded, smooth, trap


def _bedding(c, x0: float, x1: float, mh: float):
    """Matratze, Kissen, Decke – wie furniture.bed."""
    c.fill(rrect(x0 + 2, mh - 11, x1 - 2, mh - 1, 3.5), zone=2)
    pil = smooth([(x0 + 4, mh - 2), (x0 + 3, mh + 7), (x0 + 16, mh + 10), (x0 + 30, mh + 7), (x0 + 29, mh - 2)])
    shaded(c, pil, 2, "bottom", SOFT, 0.35)
    bl = smooth([(x0 + 26, mh + 1), (x0 + 32, mh + 5), (x1 - 6, mh + 4), (x1 - 2, mh - 2), (x1 - 2, mh - 14, "s"), (x0 + 26, mh - 14, "s")])
    cl = shaded(c, bl, 1, "bottom", SHADE, 0.35)
    for k in range(1, 4):
        line(c, [(x0 + 26 + k * (x1 - x0 - 30) / 4, mh + 3), (x0 + 24 + k * (x1 - x0 - 30) / 4, mh - 13)], clip=cl, shade=0.8)


def bed2(it: Item, style: str = "canopy", mattress_h: float = 50.0):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    mh = mattress_h
    if style == "canopy":                                            # Himmelbett: 4 Pfosten, Himmel, Vorhänge
        for x in (x0 + 3, x1 - 3):
            c.fill(rrect(x - 2.5, 0, x + 2.5, H, 1), zone=3)
            c.line(rrect(x - 2.5, 0, x + 2.5, H, 1), INNER, zone=0, closed=True)
        shaded(c, rrect(x0 + 3, 8, x1 - 3, mh - 10, 2), 3, "bottom", SHADE, 0.4)
        c.fill(rrect(x0 + 3, 0, x0 + 12, mh + 38, 3), zone=3, shade=0.95)
        _bedding(c, x0 + 12, x1 - 6, mh)
        top = rrect(x0 - 2, H - 10, x1 + 2, H, 2)
        cl = shaded(c, top, 2, "bottom", SHADE, 0.3)
        for k in range(12):
            c.fill(ell(x0 + (k + 0.5) * W / 12, H - 10, W / 24, 4, 12), zone=2, shade=0.95)
        for sx in (-1, 1):                                           # zusammengebundene Vorhänge
            x = sx * (W / 2 - 8)
            cur = smooth([(x - 7, H - 10), (x + 7, H - 10), (x + 2, H * 0.55), (x + 7, mh - 12), (x - 7, mh - 12), (x - 2, H * 0.55)])
            shaded(c, cur, 2, "right", SHADE, 0.3)
            c.fill(rrect(x - 3, H * 0.53, x + 3, H * 0.58, 1), zone=1)
    elif style == "loft":                                            # Hochbett mit Leiter und Spielecke darunter
        for x in (x0 + 3, x1 - 3):
            c.fill(rrect(x - 3, 0, x + 3, H, 1), zone=3)
        mh = H - 30
        shaded(c, rrect(x0 + 2, mh - 18, x1 - 2, mh - 10, 2), 3, "bottom", SHADE, 0.4)
        _bedding(c, x0 + 6, x1 - 6, mh)
        c.fill(rrect(x0 + 2, H - 4, x1 - 2, H, 1.2), zone=3)
        for k in range(8):
            c.fill(rrect(x0 + 10 + k * (W - 30) / 8, mh, x0 + 12 + k * (W - 30) / 8, H - 3, 0.5), zone=3, shade=0.95)
        for x in (x1 - 30, x1 - 16):
            c.line([(x, 0), (x, mh - 10)], 2.0, zone=3)
        for k in range(1, 6):
            c.line([(x1 - 30, k * (mh - 12) / 6), (x1 - 16, k * (mh - 12) / 6)], 1.6, zone=3)
        for xa, xb in ((x0 + 6, x0 + 30), (x1 - 62, x1 - 36)):   # Vorhänge links/rechts gerafft → Spielecke darunter
            cur = smooth([(xa, mh - 18), (xb, mh - 18), ((xa + xb) / 2 + 3, mh * 0.45), (xb - 2, 2), (xa + 2, 2), ((xa + xb) / 2 - 3, mh * 0.45)])
            cl = shaded(c, cur, 1, "right", SHADE, 0.25)
            line(c, [((xa + xb) / 2, mh - 18), ((xa + xb) / 2, 2)], zone=1, clip=cl)
            c.fill(rrect((xa + xb) / 2 - 5, mh * 0.43, (xa + xb) / 2 + 5, mh * 0.48, 1), zone=2)
        for k in range(2):
            cushion(c, x0 + 38 + k * 42, 2, x0 + 76 + k * 42, 20, zone=2)
        for k in range(9):
            t = k / 8
            x = x0 + 34 + t * (W - 104)
            c.fill(ell(x, mh - 24 - 5 * (1 - (2 * t - 1) ** 2), 1.4, 1.8, 10), zone=[1, 2][k % 2], shade=1.25)
    elif style == "sofa_bed":                                        # ausgeklappt = Sofa mit liegender Matratze davor
        F.sofa(it, "modern", 42, 3)
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 10), 0, 8, 3, 2.4)
        mat = rrect(x0 + 2, 6, x1 - 2, 24, 4)
        cl = shaded(c, mat, 2, "bottom", SHADE, 0.35)
        for k in range(1, 8):
            c.ellipse(x0 + k * W / 8, 16, 0.8, 0.8, zone=2, shade=0.75, clip=cl)
        pil = smooth([(x0 + 8, 22), (x0 + 7, 32), (x0 + 24, 35), (x0 + 42, 32), (x0 + 40, 22)])
        shaded(c, pil, 2, "bottom", SOFT, 0.35)
        bl = rrect(x0 + 46, 20, x1 - 10, 29, 4)
        shaded(c, bl, 1, "bottom", SHADE, 0.35)
    elif style == "daybed":                                          # Tagesbett: drei Seiten Lehne, Kissen
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 6), 0, 12, 3.4, 2.6)
        body = rrect(x0, 10, x1, mh - 8, 2)
        shaded(c, body, 3, "bottom", SHADE, 0.35)
        for x in (x0, x1 - 6):
            c.fill(rrect(x, 10, x + 6, H * 0.85, 3), zone=3)
            c.line(rrect(x, 10, x + 6, H * 0.85, 3), INNER, zone=0, closed=True)
        c.fill(rrect(x0 + 6, mh - 10, x1 - 6, mh, 3), zone=1)
        c.line(rrect(x0 + 6, mh - 10, x1 - 6, mh, 3), INNER, zone=0, closed=True)
        c.fill(rrect(x0 + 6, mh, x1 - 6, H * 0.8, 3), zone=1, shade=0.9)
        for k in range(3):
            cushion(c, x0 + 12 + k * (W - 24) / 3, mh + 1, x0 + 8 + (k + 1) * (W - 24) / 3, mh + 22, zone=2)


def table2(it: Item, style: str = "oval"):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    tt = 4.5
    if style in ("oval", "coffee_round"):
        leg(c, 0, 4, H - tt, W * 0.1, W * 0.06)
        c.fill(ell(0, 3, W * 0.25, 3, 24), zone=3, shade=0.9)
        top = ell(0, H - tt / 2, W / 2, tt / 2 + 1, 48)
        cl = shaded(c, top, 3, "bottom", SHADE, 0.45)
        return
    if style in ("square", "long", "extend"):
        inset = 5.0
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - inset), 0, H - tt, 5, 4)
        if style == "long":
            leg(c, 0, 0, H - tt, 5, 4)
        c.fill(rrect(x0 + inset, H - tt - 7, x1 - inset, H - tt, 1), zone=3, shade=0.85)
        top = rrect(x0, H - tt, x1, H, 1.5)
        cl = shaded(c, top, 3, "bottom", SHADE, 0.4)
        grain(c, x0 + 3, x1 - 3, H - tt, H - 1.5, cl, n=1)
        if style == "extend":                                        # Einlegeplatte in der Mitte (andere Farbe)
            c.fill(rrect(-W * 0.15, H - tt, W * 0.15, H, 0.3), zone=1, clip=cl)
            for x in (-W * 0.15, W * 0.15):
                c.line([(x, H - tt), (x, H)], 0.3, zone=0)
        return
    if style == "folding":
        for sx in (-1, 1):
            c.line([(sx * W * 0.35, 0), (-sx * W * 0.3, H - tt)], 1.6, zone=3)
        top = rrect(x0, H - tt, x1, H, 1)
        shaded(c, top, 1, "bottom", SHADE, 0.4)
    elif style in ("bistro", "bar"):
        c.fill(ell(0, 2, W * 0.3, 2, 24), zone=3, shade=0.8)
        c.fill(rrect(-2, 2, 2, H - tt, 1), zone=3)
        if style == "bar":
            c.line([(-W * 0.18, H * 0.3), (W * 0.18, H * 0.3)], 1.4, zone=3)
        top = ell(0, H - tt / 2, W / 2, tt / 2 + 0.5, 40) if style == "bistro" else rrect(x0, H - tt, x1, H, 1.5)
        shaded(c, top, 1, "bottom", SHADE, 0.4)
    elif style == "console":                                         # schmaler Wandtisch mit Schublade + Ablage
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 3), 0, H - tt, 3, 2.4)
        c.fill(rrect(x0 + 3, H * 0.2, x1 - 3, H * 0.24, 0.6), zone=3, shade=0.9)
        c.fill(rrect(x0 + 2, H - tt - 10, x1 - 2, H - tt, 1), zone=1)
        c.line(rrect(x0 + 2, H - tt - 10, x1 - 2, H - tt, 1), INNER, zone=0, closed=True)
        knob(c, 0, H - tt - 5, 1.2)
        top = rrect(x0, H - tt, x1, H, 1.2)
        shaded(c, top, 3, "bottom", SHADE, 0.4)
    elif style == "nesting":                                         # zwei Satztische, der kleine steht davor
        for k, (dx, s, z) in enumerate(((-W * 0.15, 1.0, 3), (W * 0.18, 0.78, 1))):
            w, h = W * 0.62 * s, H * s
            for sx in (-1, 1):
                leg(c, dx + sx * (w / 2 - 2.5), 0, h - 3, 2.6, 2.2, zone=z)
            top = rrect(dx - w / 2, h - 3, dx + w / 2, h, 1)
            shaded(c, top, z, "bottom", SHADE, 0.4)


def seat2(it: Item, style: str = "wing", seat_h: float = 42.0):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "wing":                                              # Ohrensessel (Oma/Opa)
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 8), 0, 12, 3.6, 2.6)
        back = smooth([(x0 + 6, seat_h, "s"), (x1 - 6, seat_h, "s"), (x1 - 8, H * 0.9), (x1 - 2, H), (x1 - 12, H), (0, H * 1.02),
                       (x0 + 12, H), (x0 + 2, H), (x0 + 8, H * 0.9)])
        shaded(c, back, 1, "right", SHADE, 0.22)
        for sx in (-1, 1):                                           # Ohren
            ear = ell(sx * (W / 2 - 9), H * 0.82, 8, 14, 24)
            shaded(c, ear, 1, "right", SOFT, 0.3)
        c.fill(rrect(x0 + 4, 10, x1 - 4, seat_h, 3), zone=1, shade=0.92)
        cushion(c, x0 + 12, seat_h - 4, x1 - 12, seat_h + 5, zone=2)
        for sx in (-1, 1):
            arm = rrect(x1 - 12, 10, x1, seat_h + 18, 6) if sx > 0 else rrect(x0, 10, x0 + 12, seat_h + 18, 6)
            shaded(c, arm, 1, "right", SHADE, 0.3)
        for k in range(3):
            c.ellipse(x0 + W * 0.35 + k * W * 0.15, H * 0.75, 1.0, 1.0, zone=1, shade=0.7)
    elif style == "recliner":                                        # Fernsehsessel: breit, weich, Fußstütze ausgeklappt
        c.fill(rrect(x0 + 10, 0, x1 - 10, 6, 2), zone=3, shade=0.7)
        back = rrect(x0 + 10, seat_h - 4, x1 - 10, H, 12)
        shaded(c, back, 1, "bottom", SOFT, 0.3)
        for k in range(3):
            cushion(c, x0 + 18, seat_h + 4 + k * (H - seat_h - 10) / 3, x1 - 18, seat_h + 2 + (k + 1) * (H - seat_h - 10) / 3, zone=1)
        c.fill(rrect(x0 + 8, 5, x1 - 8, seat_h, 5), zone=1, shade=0.9)
        cushion(c, x0 + 16, seat_h - 6, x1 - 16, seat_h + 5, zone=1)
        for sx in (-1, 1):
            arm = rrect(x1 - 17, 5, x1, seat_h + 16, 8) if sx > 0 else rrect(x0, 5, x0 + 17, seat_h + 16, 8)
            shaded(c, arm, 1, "right", SHADE, 0.3)
        foot = rrect(x0 + 20, 12, x1 - 20, 26, 5)                     # Fußstütze kommt nach vorne
        shaded(c, foot, 2, "bottom", SHADE, 0.35)
        c.fill(rrect(x1 - 6, seat_h - 2, x1 - 3, seat_h + 8, 1), zone=3)
    elif style == "folding":                                         # Klappstuhl (Vorderansicht): Rohrgestell, Loch in der Lehne
        for sx in (-1, 1):
            c.line([(sx * (W / 2 - 3), 0), (sx * (W / 2 - 4), H - 2)], 1.6, zone=3)
            c.line([(sx * (W / 2 - 3), 0), (sx * (W / 2 - 7), seat_h - 3)], 1.2, zone=3, shade=0.8)
        c.line([(x0 + 4, seat_h * 0.3), (x1 - 4, seat_h * 0.3)], 1.0, zone=3, shade=0.8)
        seat = rrect(x0 + 1, seat_h - 3, x1 - 1, seat_h + 1, 1.2)
        shaded(c, seat, 1, "bottom", SHADE, 0.4)
        back = rrect(x0 + 2, H - 22, x1 - 2, H, 2)
        cl = shaded(c, back, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(-W * 0.18, H - 7, W * 0.18, H - 3.5, 1.5), zone=0, alpha=0.85, clip=cl)
    elif style == "bench_kitchen":                                   # Eckbank (Sitzbank mit Rückenlehne, Truhe)
        body = rrect(x0, 0, x1, seat_h - 4, 1.5)
        cl = shaded(c, body, 3, "right", SHADE, 0.12)
        for k in range(1, int(W / 50) + 1):
            line(c, [(x0 + k * 50, 2), (x0 + k * 50, seat_h - 6)], zone=3, clip=cl)
        c.fill(rrect(x0 - 1, seat_h - 5, x1 + 1, seat_h - 1, 1), zone=3, shade=1.05)
        cushion(c, x0 + 2, seat_h - 2, x1 - 2, seat_h + 4, zone=1)
        back = rrect(x0, seat_h + 4, x1, H, 1.5)
        bcl = shaded(c, back, 3, "bottom", SOFT, 0.15)
        for k in range(1, int(W / 12)):
            line(c, [(x0 + k * 12, seat_h + 4), (x0 + k * 12, H)], zone=3, clip=bcl)
        for k in range(int(W / 60)):
            cushion(c, x0 + 6 + k * 60, seat_h + 8, x0 + 54 + k * 60, H - 6, zone=2)
    elif style == "step":                                            # Tritthocker mit zwei Stufen
        for k, (y, x) in enumerate(((H * 0.48, x0), (H, x0 + W * 0.35))):
            step = rrect(x, y - 5, x1, y, 1.2)
            shaded(c, step, 1, "bottom", SHADE, 0.35)
            c.fill(rrect(x + 3, y - 1.5, x1 - 3, y, 0.5), zone=2)
        for x in (x0 + 2, x1 - 3):
            c.line([(x, 0), (x, H * 0.44)], 2.2, zone=3)
        c.line([(x0 + W * 0.37, H * 0.44), (x0 + W * 0.37, H - 5)], 2.2, zone=3)
        c.line([(x1 - 3, H * 0.44), (x1 - 3, H - 5)], 2.2, zone=3)
    elif style == "piano":                                           # Klavierhocker, drehbar
        c.fill(trap(-W * 0.3, W * 0.3, 0, -W * 0.08, W * 0.08, H * 0.2, 1), zone=3)
        c.fill(rrect(-2.2, H * 0.2, 2.2, H * 0.8, 1), zone=3, shade=0.9)
        for k in range(4):
            c.line([(-2.2, H * (0.35 + k * 0.1)), (2.2, H * (0.38 + k * 0.1))], 0.3, zone=0)
        cushion(c, x0, H * 0.78, x1, H, zone=1)
    elif style == "milk":                                            # Melkschemel, drei Beine
        for x, a in ((-W * 0.35, -0.2), (0, 0.0), (W * 0.35, 0.2)):
            c.line([(x, 0), (x * 0.5, H - 3)], 2.2, zone=3)
        top = ell(0, H - 2, W / 2, 2.4, 28)
        shaded(c, top, 1, "bottom", SHADE, 0.45)
    elif style == "footstool":
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 4), 0, 8, 3, 2.2)
        body = rrect(x0, 6, x1, H, 5)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        for k in range(3):
            c.ellipse(x0 + W * (k + 1) / 4, H * 0.65, 0.9, 0.9, zone=1, shade=0.7, clip=cl)
        c.fill(rrect(x0, 6, x1, 10, 1), zone=2)


def window_deco(it: Item, style: str = "rod"):
    """Gardinenstange, Raffrollo, Jalousie (Wand)."""
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style in ("rod", "rod_rings"):
        c.line([(x0 + 3, H / 2), (x1 - 3, H / 2)], 1.4, zone=1)
        for sx in (-1, 1):
            c.fill(ell(sx * (W / 2 - 3), H / 2, 3, 3, 16), zone=2)
            c.line(ell(sx * (W / 2 - 3), H / 2, 3, 3, 16), INNER, zone=0, closed=True)
            c.fill(rrect(sx * (W / 2 - 14) - 1, H / 2, sx * (W / 2 - 14) + 1, H, 0.4), zone=1, shade=0.8)
        if style == "rod_rings":
            for k in range(int((W - 20) / 8)):
                c.line(ell(x0 + 12 + k * 8, H / 2, 1.6, 1.6, 12), 0.5, zone=2, closed=True)
    elif style == "roman":                                           # Raffrollo in Falten
        c.fill(rrect(x0, H - 3, x1, H, 0.8), zone=3)
        n = 4
        for k in range(n):
            y0 = H - 3 - (k + 1) * (H - 3) / n
            fold = smooth([(x0, y0 + (H - 3) / n, "s"), (x1, y0 + (H - 3) / n, "s"), (x1 - 1, y0 + 2), (0, y0), (x0 + 1, y0 + 2)])
            shaded(c, fold, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(x0, 0, x1, 2.5, 0.6), zone=2)
        c.line([(x1 - 4, H - 3), (x1 - 4, H * 0.2)], 0.3, zone=2)
        c.fill(ell(x1 - 4, H * 0.18, 1.2, 2, 10), zone=2)
    elif style == "venetian":                                        # Jalousie mit Lamellen
        c.fill(rrect(x0, H - 4, x1, H, 0.8), zone=3)
        for k in range(int((H - 4) / 3.2)):
            y = H - 4 - (k + 1) * 3.2
            c.fill(rrect(x0 + 1, y, x1 - 1, y + 2.4, 0.6), zone=1, shade=1.0 if k % 2 else 0.95)
            c.line(rrect(x0 + 1, y, x1 - 1, y + 2.4, 0.6), 0.15, zone=0, closed=True)
        for x in (-W * 0.3, W * 0.3):
            c.line([(x, H - 4), (x, 0)], 0.2, zone=2)
        c.line([(x1 - 3, H - 4), (x1 - 3, H * 0.3)], 0.3, zone=2)
