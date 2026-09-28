"""
Straße, Park & Spielplatz (P09-T02/T06/T07): Bushaltestelle, Straßenlaterne, Parkbank, Mülleimer, Fahrradständer,
Litfaßsäule, Markise; Klettergerüst, Karussell (Drehscheibe), Federwippe, Schaukel (Doppel), Rutsche mit Turm,
Wippe, Sandförmchen, Seifenblasen, Eiswagen; Enten, Tauben, Eichhörnchen (Wildtiere).
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Holz. Tiere: Zone 1 = Gefieder/Fell, 2 = Bauch/Schnabel, 3 = Beine.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, ell, line, rrect, shaded, smooth, trap


def _post(c, x: float, y0: float, y1: float, w: float = 3.0, zone: int = 3):
    p = rrect(x - w / 2, y0, x + w / 2, y1, w * 0.3)
    c.fill(p, zone=zone)
    c.fill(rrect(x + w * 0.1, y0, x + w / 2, y1, w * 0.3), zone=zone, shade=SHADE, clip=c.mask(p))
    c.line(p, INNER, zone=0, closed=True)


def _motif(c, m: str, cx: float, cy: float, r: float):
    """Laden-Symbol (kein Text, R-07): Brot, Blume, Shirt, Schere, Teddy, Pfote, Eis, Note, Wagen."""
    if m == "bread":
        c.fill(smooth([(cx - r, cy - r * 0.4, "s"), (cx + r, cy - r * 0.4, "s"), (cx + r * 0.9, cy + r * 0.3), (cx, cy + r * 0.6),
                       (cx - r * 0.9, cy + r * 0.3)]), zone=2)
        for k in (-0.4, 0, 0.4):
            c.line([(cx + k * r - r * 0.1, cy - r * 0.1), (cx + k * r + r * 0.15, cy + r * 0.35)], r * 0.08, zone=2, shade=0.7)
    elif m == "flower":
        for p in range(6):
            a = p * math.pi / 3
            c.fill(ell(cx + math.cos(a) * r * 0.5, cy + math.sin(a) * r * 0.5, r * 0.36, r * 0.36, 14), zone=2)
        c.fill(ell(cx, cy, r * 0.3, r * 0.3, 14), zone=1, shade=1.2)
    elif m == "shirt":
        c.fill([(cx - r * 0.5, cy - r * 0.8), (cx + r * 0.5, cy - r * 0.8), (cx + r * 0.5, cy + r * 0.3), (cx + r, cy + r * 0.1),
                (cx + r * 0.8, cy + r * 0.7), (cx + r * 0.3, cy + r * 0.8), (cx, cy + r * 0.55), (cx - r * 0.3, cy + r * 0.8),
                (cx - r * 0.8, cy + r * 0.7), (cx - r, cy + r * 0.1), (cx - r * 0.5, cy + r * 0.3)], zone=2)
    elif m == "scissors":
        for sx in (-1, 1):
            c.line(ell(cx + sx * r * 0.4, cy - r * 0.55, r * 0.25, r * 0.25, 14), r * 0.12, zone=2, closed=True)
            c.line([(cx + sx * r * 0.3, cy - r * 0.35), (cx - sx * r * 0.35, cy + r * 0.8)], r * 0.14, zone=2)
    elif m == "teddy":
        c.fill(ell(cx, cy - r * 0.35, r * 0.55, r * 0.5, 18), zone=2)
        c.fill(ell(cx, cy + r * 0.35, r * 0.45, r * 0.42, 18), zone=2)
        for sx in (-1, 1):
            c.fill(ell(cx + sx * r * 0.38, cy + r * 0.72, r * 0.18, r * 0.18, 10), zone=2)
    elif m == "paw":
        c.fill(ell(cx, cy - r * 0.25, r * 0.45, r * 0.38, 18), zone=2)
        for k, (dx, dy) in enumerate(((-0.55, 0.25), (-0.2, 0.6), (0.2, 0.6), (0.55, 0.25))):
            c.fill(ell(cx + dx * r, cy + dy * r, r * 0.18, r * 0.22, 10), zone=2)
    elif m == "icecream":
        c.fill([(cx - r * 0.45, cy), (cx + r * 0.45, cy), (cx, cy - r)], zone=3, shade=0.9)
        c.fill(ell(cx, cy + r * 0.25, r * 0.5, r * 0.42, 18), zone=2)
        c.fill(ell(cx, cy + r * 0.7, r * 0.35, r * 0.3, 16), zone=1, shade=1.3)
    elif m == "note":
        for dx in (-0.35, 0.45):
            c.fill(ell(cx + dx * r, cy - r * 0.55, r * 0.26, r * 0.2, 12), zone=2)
            c.line([(cx + dx * r + r * 0.22, cy - r * 0.55), (cx + dx * r + r * 0.22, cy + r * 0.6)], r * 0.1, zone=2)
        c.fill([(cx - r * 0.13, cy + r * 0.55), (cx + r * 0.67, cy + r * 0.7), (cx + r * 0.67, cy + r * 0.45),
                (cx - r * 0.13, cy + r * 0.3)], zone=2)
    else:                                                           # Einkaufswagen
        c.fill([(cx - r * 0.8, cy + r * 0.5), (cx + r * 0.8, cy + r * 0.5), (cx + r * 0.55, cy - r * 0.35),
                (cx - r * 0.55, cy - r * 0.35)], zone=2)
        c.line([(cx - r * 0.8, cy + r * 0.5), (cx - r * 1.0, cy + r * 0.8)], r * 0.1, zone=2)
        for sx in (-0.4, 0.4):
            c.fill(ell(cx + sx * r, cy - r * 0.62, r * 0.16, r * 0.16, 10), zone=2)


def street(it: Item, style: str = "bench", state: str = "", motif: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "bus_stop":                                         # Wartehäuschen: Dach, Glas, Bank, Haltestellen-Schild
        c.fill(rrect(x0, H - 10, x1, H, 1.5), zone=1)
        c.fill(rrect(x0, H - 12, x1, H - 10, 0.5), zone=1, shade=0.7)
        for x in (x0 + 4, x1 - 34):
            _post(c, x, 0, H - 10, 4)
        gl = rrect(x0 + 8, 30, x1 - 38, H - 16, 0.8)
        c.fill(gl, zone=3, shade=1.55, alpha=0.5)
        line(c, [(x0 + 20, H - 22), (x0 + 50, 50)], zone=3, shade=1.9, w=1.2)
        c.line(gl, INNER, zone=0, closed=True)
        seat = rrect(x0 + 20, 42, x1 - 60, 47, 1.0)
        c.fill(seat, zone=2)
        for x in (x0 + 26, x1 - 66):
            c.fill(rrect(x - 1.2, 0, x + 1.2, 42, 0.4), zone=3)
        c.line(seat, INNER, zone=0, closed=True)
        _post(c, x1 - 12, 0, H + 20, 3)                             # Haltestellen-Mast mit rundem Schild (Bus-Symbol)
        c.fill(ell(x1 - 12, H + 22, 13, 13, 32), zone=2, shade=1.2)
        c.fill(ell(x1 - 12, H + 22, 10, 10, 32), zone=1, shade=1.0)
        bus = rrect(x1 - 19, H + 17, x1 - 5, H + 27, 1.5)
        c.fill(bus, zone=2, shade=1.45)
        for wx in (x1 - 16, x1 - 8):
            c.fill(ell(wx, H + 17, 1.6, 1.6, 10), zone=0)
        c.fill(rrect(x1 - 17, H + 22, x1 - 7, H + 25.5, 0.5), zone=1, shade=1.3)
    elif style == "street_lamp":
        c.fill(trap(-6, 6, 0, -3, 3, 14, 0.6), zone=1)
        _post(c, 0, 14, H - 30, 4, zone=1)
        arm = smooth([(0, H - 32), (0, H - 14), (6, H - 6), (18, H - 4)], closed=False)
        c.line(arm, 3.0, zone=1)
        shade_ = trap(8, 30, H - 16, 12, 26, H - 4, 1.0)
        c.fill(shade_, zone=1, shade=0.9)
        c.fill(ell(19, H - 17, 9, 3, 20), zone=2, shade=1.4 if state == "on" else 0.95)
        c.line(shade_, INNER, zone=0, closed=True)
    elif style == "park_bench":
        for sx in (-1, 1):
            leg_ = smooth([(sx * W * 0.38 - 3, 0, "s"), (sx * W * 0.38 + 3, 0, "s"), (sx * W * 0.4 + 2, H * 0.55), (sx * W * 0.42, H * 0.95),
                           (sx * W * 0.4 - 3, H * 0.95), (sx * W * 0.38 - 3, H * 0.55)])
            c.fill(leg_, zone=3)
            c.line(leg_, INNER, zone=0, closed=True)
        for k in range(3):                                          # Sitz- und Lehnenlatten
            b = rrect(x0, H * 0.46 + k * 2.2, x1, H * 0.46 + k * 2.2 + 1.8, 0.4)
            c.fill(b, zone=1, shade=1.0 - 0.04 * k)
        for k in range(3):
            b = rrect(x0 + 2, H * 0.62 + k * H * 0.11, x1 - 2, H * 0.62 + k * H * 0.11 + H * 0.08, 0.6)
            c.fill(b, zone=1, shade=0.94)
            c.line(b, INNER, zone=0, closed=True)
    elif style == "bin_street":                                     # runder Mülleimer am Pfosten
        _post(c, 0, 0, H * 0.9, 5)
        bin_ = trap(-W * 0.45, W * 0.45, H * 0.25, -W / 2, W / 2, H, 1.2)
        shaded(c, bin_, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W / 2, H - 5, W / 2, H, 1.0), zone=1, shade=0.8)
        c.fill(ell(0, H * 0.6, W * 0.16, W * 0.16, 20), zone=2)
        c.line(bin_, INNER, zone=0, closed=True)
    elif style == "bike_stand":
        n = max(3, int(W / 40))
        for k in range(n):
            x = x0 + (k + 0.5) * W / n
            hoop = smooth([(x - 10, 0), (x - 10, H * 0.7), (x - 7, H * 0.95), (x, H), (x + 7, H * 0.95), (x + 10, H * 0.7), (x + 10, 0)],
                          closed=False)
            c.line(hoop, 2.4, zone=1)
        c.fill(rrect(x0, 0, x1, 2, 0.5), zone=3, shade=0.7)
    elif style == "advert_column":                                  # Litfaßsäule mit bunten Plakaten (Bilder, kein Text)
        body = rrect(-W / 2, 8, W / 2, H - 18, 1.0)
        shaded(c, body, 1, "right", SHADE, 0.25)
        cl = c.mask(body)
        for k, (y0, y1) in enumerate(((14, H * 0.45), (H * 0.47, H * 0.8))):
            p = rrect(-W * 0.38, y0, W * 0.3, y1, 0.8)
            c.fill(p, zone=2, shade=1.2 if k else 0.9, clip=cl)
            if k:
                c.fill(ell(-W * 0.04, (y0 + y1) / 2, W * 0.14, W * 0.14, 20), zone=1, shade=1.3, clip=cl)
            else:
                c.fill([(-W * 0.3, y0 + 4), (-W * 0.05, y1 - 6), (W * 0.2, y0 + 4)], zone=1, shade=1.25, clip=cl)
        c.fill(rrect(-W / 2 - 3, 0, W / 2 + 3, 8, 1.0), zone=3)
        dome = smooth([(-W / 2 - 3, H - 18, "s"), (W / 2 + 3, H - 18, "s"), (W / 2 - 2, H - 6), (0, H, "s"), (-W / 2 + 2, H - 6)])
        c.fill(dome, zone=3, shade=0.9)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "awning":                                         # Markise (Wand): gestreift, Wellenkante
        top = rrect(x0, H - 6, x1, H, 1.0)
        c.fill(top, zone=3)
        n = max(4, int(W / 24))
        for k in range(n):
            sx0 = x0 + k * W / n
            sx1 = sx0 + W / n
            strip = [(sx0, H - 6), (sx1, H - 6), (sx1 + 4, 8), (sx0 + 4, 8)]
            c.fill(strip, zone=1 if k % 2 else 2)
            c.fill(smooth([(sx0 + 4, 9, "s"), (sx1 + 4, 9, "s"), ((sx0 + sx1) / 2 + 4, 0)]), zone=1 if k % 2 else 2, shade=0.9)
        c.line([(x0, H - 6), (x0 + 4, 8)], INNER, zone=0)
        c.line([(x1, H - 6), (x1 + 4, 8)], INNER, zone=0)
    elif style == "shop_sign":                                      # Laden-Schild (Wand, nur Symbol): Rahmen + Motiv
        board = rrect(x0, 0, x1, H, H * 0.25)
        shaded(c, board, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(x0 + 3, 3, x1 - 3, H - 3, H * 0.2), zone=3, shade=1.7)
        _motif(c, motif or "cart", 0, H * 0.5, H * 0.34)
        c.line(board, INNER, zone=0, closed=True)
    elif style == "bus":                                            # Linienbus seitlich (Bereichswechsel an der Haltestelle)
        body = rrect(x0, 14, x1, H, 8.0)
        shaded(c, body, 1, "bottom", SHADE, 0.25)
        cl = c.mask(body)
        c.fill(rrect(x0, 14, x1, 34, 4.0), zone=2, clip=cl)
        n = max(3, int(W / 110))
        for k in range(n):
            wx = x0 + 30 + k * (W - 80) / n
            win = rrect(wx, H * 0.5, wx + (W - 80) / n - 10, H - 18, 3.0)
            c.fill(win, zone=3, shade=1.5)
            line(c, [(wx + 6, H - 24), (wx + 22, H * 0.55)], zone=3, shade=1.9, w=1.4)
            c.line(win, INNER, zone=0, closed=True)
        door = rrect(x1 - 70, 20, x1 - 30, H - 16, 2.0)
        c.fill(door, zone=3, shade=1.35)
        line(c, [(x1 - 50, 20), (x1 - 50, H - 16)], zone=3, shade=0.7, w=1.0)
        c.fill(rrect(x1 - 12, H * 0.5, x1 - 2, H - 20, 3.0), zone=3, shade=1.5)          # Frontscheibe
        c.fill(ell(x1 - 6, 30, 4, 3, 12), zone=2, shade=1.6)                              # Scheinwerfer
        for wx in (x0 + 70, x1 - 90):
            c.fill(ell(wx, 14, 20, 20, 32), zone=0)
            c.fill(ell(wx, 14, 9, 9, 20), zone=3, shade=1.2)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "icecream_cart":                                  # Eiswagen mit Schirm und Rädern
        box = rrect(x0 + 6, 20, x1 - 16, H * 0.55, 2.0)
        shaded(c, box, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 + 6, H * 0.35, x1 - 16, H * 0.42, 0.6), zone=2)
        for k in range(4):
            c.fill(ell(x0 + 16 + k * (W - 38) / 3, H * 0.57, 5, 3, 14), zone=2 if k % 2 else 1, shade=[1.4, 1.2, 1.5, 0.9][k])
        for wx in (x0 + 16, x1 - 28):
            c.fill(ell(wx, 10, 10, 10, 28), zone=3, shade=0.5)
            c.fill(ell(wx, 10, 4, 4, 16), zone=3, shade=1.2)
        c.line([(x1 - 16, H * 0.5), (x1 - 2, H * 0.62)], 2.0, zone=3)
        _post(c, 0, H * 0.55, H * 0.8, 2)
        um = smooth([(x0 - 4, H * 0.8, "s"), (0, H, "s"), (x1 + 4, H * 0.8, "s")])
        c.fill(um, zone=2)
        for k in range(1, 6):
            a = math.pi * k / 6
            line(c, [(0, H), (math.cos(a) * (W / 2 + 4), H * 0.8)], zone=2, shade=0.75, w=0.5)
        c.line(box, INNER, zone=0, closed=True)


def play(it: Item, style: str = "climber", state: str = "", shape: str = ""):
    c, W, H = it.c, it.w, it.h
    state = shape or state
    x0, x1 = -W / 2, W / 2
    if style == "climber":                                          # Klettergerüst: Turm, Dach, Kletterwand, Rutschstange
        for x in (x0 + 6, x0 + W * 0.55):
            _post(c, x, 0, H * 0.78, 5)
        c.fill(rrect(x0 + 2, H * 0.42, x0 + W * 0.6, H * 0.47, 0.8), zone=3)       # Podest
        roof = [(x0 - 2, H * 0.78), (x0 + W * 0.64, H * 0.78), (x0 + W * 0.3, H)]
        c.fill(roof, zone=1)
        c.line(roof, INNER, zone=0, closed=True)
        wall = [(x0 + W * 0.6, H * 0.45), (x1 - 4, 0), (x1 - 18, 0), (x0 + W * 0.58, H * 0.3)]
        c.fill(wall, zone=2)
        for k in range(5):                                          # Klettergriffe
            t = (k + 0.5) / 5
            gx = x0 + W * 0.6 + (x1 - 10 - x0 - W * 0.6) * t
            gy = H * 0.38 * (1 - t)
            c.fill(ell(gx, gy + 2, 2.4, 2.0, 12), zone=1, shade=[1.2, 0.85, 1.35, 1.0, 1.2][k])
        c.line(wall, INNER, zone=0, closed=True)
        for k in range(1, 6):                                       # Leiter
            line(c, [(x0 + 6, H * 0.42 * k / 6), (x0 + 16, H * 0.42 * k / 6)], zone=3, shade=0.8, w=1.4)
        _post(c, x0 + 16, 0, H * 0.45, 2.4)
        for k in range(8):                                          # Geländer
            _post(c, x0 + 8 + k * W * 0.07, H * 0.47, H * 0.6, 1.4, zone=1)
        c.fill(rrect(x0 + 6, H * 0.6, x0 + W * 0.57, H * 0.63, 0.5), zone=1)
    elif style == "roundabout":                                     # Drehscheibe (Karussell) mit Haltebügeln
        disc = smooth([(x0, H * 0.18, "s"), (x0 + 6, H * 0.3), (x1 - 6, H * 0.3), (x1, H * 0.18, "s"), (x1 - 6, H * 0.06),
                       (x0 + 6, H * 0.06)])
        c.fill(trap(-8, 8, 0, -6, 6, H * 0.1, 0.6), zone=3, shade=0.7)
        shaded(c, disc, 1, "bottom", SHADE, 0.45)
        n = 6
        for k in range(n):
            a = 2 * math.pi * k / n + (0.4 if state == "on" else 0.0)
            x = math.sin(a) * W * 0.42
            if math.cos(a) < -0.2:
                continue
            c.line([(x, H * 0.24), (x, H * 0.72), (x * 0.2, H * 0.92)], 1.8, zone=2, shade=0.95 + 0.1 * math.cos(a))
        c.fill(ell(0, H * 0.94, 5, 3, 16), zone=2)
        c.line(disc, INNER, zone=0, closed=True)
    elif style == "spring_rider":                                   # Federwippe: Tier auf Feder (Pferdchen/Ente)
        coil = [(math.sin(k * 0.9) * W * 0.15, 4 + k * (H * 0.4) / 14) for k in range(15)]
        c.line(coil, 2.0, zone=3)
        c.fill(ell(0, 3, W * 0.3, 3, 20), zone=3, shade=0.7)
        body = smooth([(-W * 0.4, H * 0.45, "s"), (W * 0.25, H * 0.45, "s"), (W * 0.35, H * 0.6), (W * 0.2, H * 0.72),
                       (-W * 0.38, H * 0.7)])
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        head = ell(W * 0.3, H * 0.82, W * 0.17, H * 0.14, 24)
        c.fill(head, zone=1)
        c.fill(trap(W * 0.42, W * 0.5, H * 0.76, W * 0.42, W * 0.52, H * 0.84, 0.5), zone=2)   # Schnabel
        c.fill(ell(W * 0.32, H * 0.86, 1.6, 1.6, 10), zone=0)
        c.fill(ell(W * 0.31, H * 0.87, 0.6, 0.6, 8), zone=2, shade=1.8)
        c.fill(smooth([(-W * 0.4, H * 0.62, "s"), (-W * 0.5, H * 0.78), (-W * 0.3, H * 0.66, "s")]), zone=1, shade=0.9)
        c.fill(rrect(-W * 0.12, H * 0.68, W * 0.08, H * 0.74, 1.0), zone=2)        # Sattel
        c.line([(W * 0.2, H * 0.8), (W * 0.2, H * 0.95)], 1.4, zone=3)            # Griff
        c.line(body, INNER, zone=0, closed=True)
        c.line(head, INNER, zone=0, closed=True)
    elif style == "swing_double":                                   # Doppelschaukel: A-Gestell, zwei Sitze
        for sx in (-1, 1):
            c.line([(sx * W / 2, 0), (sx * (W / 2 - 14), H)], 5.0, zone=3)
            c.line([(sx * (W / 2 - 28), 0), (sx * (W / 2 - 14), H)], 5.0, zone=3)
        c.fill(rrect(x0 + 8, H - 5, x1 - 8, H, 1.4), zone=1)
        for sx in (-1, 1):
            cx = sx * W * 0.2
            for dx in (-12, 12):
                line(c, [(cx + dx, H - 4), (cx + dx, 40)], zone=3, shade=0.6, w=0.6)
            seat = rrect(cx - 15, 36, cx + 15, 41, 1.5)
            c.fill(seat, zone=2 if sx < 0 else 1)
            c.line(seat, INNER, zone=0, closed=True)
    elif style == "tower_slide":                                    # Rutsche mit Turm, Leiter und Wellen-Bahn
        _post(c, x0 + 6, 0, H * 0.85, 4)
        _post(c, x0 + 36, 0, H * 0.85, 4)
        c.fill(rrect(x0 + 2, H * 0.5, x0 + 40, H * 0.54, 0.6), zone=3)
        roof = [(x0, H * 0.85), (x0 + 42, H * 0.85), (x0 + 21, H)]
        c.fill(roof, zone=2)
        c.line(roof, INNER, zone=0, closed=True)
        for k in range(1, 7):
            line(c, [(x0 + 6, H * 0.5 * k / 7), (x0 + 36, H * 0.5 * k / 7)], zone=3, shade=0.8, w=1.2)
        bahn = smooth([(x0 + 38, H * 0.54, "s"), (x0 + W * 0.45, H * 0.46), (x0 + W * 0.62, H * 0.24), (x0 + W * 0.8, H * 0.16),
                       (x1, H * 0.06, "s"), (x1, 0, "s"), (x0 + W * 0.78, H * 0.08), (x0 + W * 0.6, H * 0.15),
                       (x0 + W * 0.43, H * 0.36), (x0 + 38, H * 0.46, "s")])
        shaded(c, bahn, 1, "bottom", SHADE, 0.35)
        line(c, [(x0 + 40, H * 0.52), (x0 + W * 0.62, H * 0.22), (x1 - 2, H * 0.05)], zone=1, shade=1.25, w=1.0)
        c.line(bahn, INNER, zone=0, closed=True)
    elif style == "sand_mold":                                      # Sandförmchen (Stern/Fisch/Burg)
        if state == "fish":
            b = smooth([(x0, H * 0.5), (x0 + W * 0.25, H, "s"), (x1 - W * 0.25, H * 0.6), (x1, H, "s"), (x1, 0, "s"),
                        (x1 - W * 0.25, H * 0.4), (x0 + W * 0.25, 0, "s")])
        elif state == "castle":
            b = [(x0, 0), (x1, 0), (x1, H), (x1 - W * 0.2, H), (x1 - W * 0.2, H * 0.8), (x0 + W * 0.6, H * 0.8), (x0 + W * 0.6, H),
                 (x0 + W * 0.4, H), (x0 + W * 0.4, H * 0.8), (x0 + W * 0.2, H * 0.8), (x0 + W * 0.2, H), (x0, H)]
        else:
            b = [(math.cos(math.pi / 2 + k * math.pi / 5) * (W / 2 if k % 2 == 0 else W * 0.22),
                  H / 2 + math.sin(math.pi / 2 + k * math.pi / 5) * (H / 2 if k % 2 == 0 else H * 0.22)) for k in range(10)]
        shaded(c, b, 1, "bottom", SHADE, 0.3)
        c.line(b, INNER, zone=0, closed=True)
    elif style == "bubble_wand":                                    # Seifenblasen-Dose mit Stab
        can = rrect(-W * 0.3, 0, W * 0.3, H * 0.6, 1.2)
        shaded(c, can, 1, "right", SHADE, 0.3)
        c.fill(rrect(-W * 0.32, H * 0.55, W * 0.32, H * 0.65, 0.8), zone=2)
        c.line([(W * 0.05, H * 0.6), (W * 0.25, H * 0.9)], 1.0, zone=2)
        c.line(ell(W * 0.3, H * 0.95, W * 0.12, W * 0.12, 20), 0.9, zone=2, closed=True)
        for bx, by, r in ((W * 0.55, H * 1.05, W * 0.1), (W * 0.7, H * 0.85, W * 0.07)):
            c.line(ell(bx, by, r, r, 20), 0.4, zone=3, shade=1.2, closed=True)
            c.fill(ell(bx - r * 0.3, by + r * 0.3, r * 0.25, r * 0.2, 10), zone=3, shade=1.8)
        c.line(can, INNER, zone=0, closed=True)


def critter(it: Item, style: str = "duck", state: str = ""):
    """Wildtiere im Park, gleicher Stil wie die Haustiere (großer Kopf, Kulleraugen)."""
    c, W, H = it.c, it.w, it.h
    if style == "duck":                                             # Ente seitlich, schwimmfähig
        body = smooth([(-W * 0.45, H * 0.35, "s"), (-W * 0.2, H * 0.08), (W * 0.25, H * 0.05, "s"), (W * 0.4, H * 0.25),
                       (W * 0.28, H * 0.5), (-W * 0.3, H * 0.55), (-W * 0.5, H * 0.6, "s")])
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(smooth([(-W * 0.15, H * 0.3, "s"), (W * 0.18, H * 0.28), (W * 0.1, H * 0.45), (-W * 0.2, H * 0.44, "s")]), zone=1,
               shade=0.88)                                          # Flügel
        head = ell(W * 0.22, H * 0.72, W * 0.2, H * 0.24, 28)
        c.fill(head, zone=1, shade=1.05)
        bill = smooth([(W * 0.36, H * 0.7, "s"), (W * 0.52, H * 0.68), (W * 0.52, H * 0.62, "s"), (W * 0.36, H * 0.6)])
        c.fill(bill, zone=2)
        c.fill(ell(W * 0.26, H * 0.77, W * 0.045, W * 0.05, 14), zone=0)
        c.fill(ell(W * 0.25, H * 0.79, W * 0.015, W * 0.015, 8), zone=2, shade=2.0)
        c.fill(ell(W * 0.18, H * 0.68, W * 0.05, W * 0.03, 12), zone=2, shade=1.1, alpha=0.4)
        c.line(bill, INNER, zone=0, closed=True)
    elif style == "pigeon":
        body = smooth([(-W * 0.5, H * 0.35, "s"), (-W * 0.2, H * 0.15), (W * 0.2, H * 0.15, "s"), (W * 0.32, H * 0.45),
                       (W * 0.2, H * 0.62), (-W * 0.25, H * 0.5)])
        for sx in (-0.05, 0.08):
            c.line([(W * sx, H * 0.16), (W * sx, 0)], 0.5, zone=3)
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(smooth([(W * 0.05, H * 0.45, "s"), (W * 0.3, H * 0.5), (W * 0.2, H * 0.62)]), zone=2, shade=1.0)   # Hals schillernd
        head = ell(W * 0.25, H * 0.78, W * 0.16, H * 0.2, 24)
        c.fill(head, zone=1, shade=1.05)
        c.fill([(W * 0.38, H * 0.8), (W * 0.5, H * 0.74), (W * 0.38, H * 0.72)], zone=3, shade=0.8)
        c.fill(ell(W * 0.28, H * 0.82, W * 0.045, W * 0.05, 12), zone=0)
        c.fill(ell(W * 0.27, H * 0.84, W * 0.015, W * 0.015, 8), zone=2, shade=2.0)
    elif style == "squirrel":
        tail = smooth([(-W * 0.1, H * 0.12, "s"), (-W * 0.5, H * 0.35), (-W * 0.48, H * 0.85), (-W * 0.2, H), (-W * 0.25, H * 0.7),
                       (-W * 0.28, H * 0.35)])
        shaded(c, tail, 1, "right", SHADE, 0.3)
        body = ell(W * 0.05, H * 0.3, W * 0.22, H * 0.3, 28)
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(ell(W * 0.12, H * 0.28, W * 0.1, H * 0.18, 20), zone=2)
        head = ell(W * 0.2, H * 0.66, W * 0.2, H * 0.19, 28)
        c.fill(head, zone=1, shade=1.05)
        for ex in (W * 0.1, W * 0.26):
            c.fill(trap(ex - 2.2, ex + 2.2, H * 0.78, ex - 0.8, ex + 0.8, H * 0.92, 0.3), zone=1)
        c.fill(ell(W * 0.26, H * 0.68, W * 0.05, W * 0.055, 12), zone=0)
        c.fill(ell(W * 0.25, H * 0.7, W * 0.016, W * 0.016, 8), zone=2, shade=2.0)
        c.fill(ell(W * 0.38, H * 0.62, W * 0.03, W * 0.025, 8), zone=0)
        c.fill(ell(W * 0.3, H * 0.3, W * 0.06, W * 0.06, 12), zone=3)          # Nuss
        c.line(tail, INNER, zone=0, closed=True)
