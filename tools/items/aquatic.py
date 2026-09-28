"""
Freizeitbad (P10c, Welt-Doku §6): Schwimmerbecken mit Bahnen-Leinen, Babybecken mit Pilz-Dusche, Sprungturm
(1/3/5 m), Wasserrutsche, Whirlpool (Blubbern), Bademeister-Hochstuhl, Rettungsring, Dusche, Startblock,
Schwimmbrett, Tauchringe, Wasserball, Kiosk, Spinde, Umkleidekabine, Drehkreuz, Wellen-Anzeige.
Zonen: 1 = Hauptfarbe · 2 = Wasser/Zweitfarbe · 3 = Metall/Weiß.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, cushion, ell, leg, rrect, shaded, smooth, trap


def _tiles(c, x0: float, x1: float, y0: float, y1: float, step: float = 20.0):
    for k in range(int((x1 - x0) / step)):
        t = rrect(x0 + k * step, y0, x0 + k * step + step - 1, y1, 0.5)
        c.fill(t, zone=3, shade=1.0 + (k % 2) * 0.05)
        c.line(t, INNER, zone=0, closed=True)


def _water(c, x0: float, x1: float, y0: float, y1: float, waves: int = 8, bubbles: bool = False):
    water = rrect(x0, y0, x1, y1, 1)
    c.fill(water, zone=2)
    cl = c.mask(water)
    W = x1 - x0
    c.fill(rrect(x0, y1 - (y1 - y0) * 0.25, x1, y1, 0.5), zone=2, shade=1.12, clip=cl)
    for k in range(waves):
        a = x0 + k * W / waves
        c.line(smooth([(a, y1 - 3), (a + W / waves * 0.25, y1 - 1.5), (a + W / waves * 0.5, y1 - 3)], closed=False),
               0.6, zone=2, shade=1.4, clip=cl)
    if bubbles:
        for k in range(int(W / 14)):
            bx = x0 + 6 + k * 14 + (k % 3) * 3
            by = y0 + (y1 - y0) * (0.3 + 0.5 * ((k * 37) % 10) / 10)
            c.fill(ell(bx, by, 2.2, 2.2, 10), zone=3, shade=1.2, clip=cl, alpha=0.8)
    return cl


def _ladder(c, x: float, y0: float, y1: float, w: float = 10.0):
    for sx in (-1, 1):
        c.line(smooth([(x + sx * w / 2, y0), (x + sx * w / 2, y1), (x + sx * w / 2 - 6, y1 + 6)], closed=False), 1.4, zone=3, shade=1.2)
    for k in range(1, 4):
        y = y0 + k * (y1 - y0) / 4
        c.line([(x - w / 2, y), (x + w / 2, y)], 1.0, zone=3)


def aquatic(it: Item, style: str = "basin", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "basin":                                            # Schwimmerbecken: Kante, Wasser, Leinen, Leiter
        _tiles(c, x0, x1, 0, H * 0.22)
        c.fill(rrect(x0, H * 0.78, x1, H, 0.8), zone=3, shade=1.1)
        cl = _water(c, x0 + 2, x1 - 2, H * 0.22, H * 0.8)
        for k in range(1, 4):                                       # Bahnen-Leinen mit Schwimmern
            y = H * 0.22 + k * H * 0.58 / 4
            for j in range(int(W / 12)):
                c.fill(ell(x0 + 6 + j * 12, y, 3.2, 1.6, 10), zone=1 if (j // 4) % 2 else 3, clip=cl)
        _ladder(c, x1 - 40, H * 0.4, H + 14)
    elif style == "baby_pool":                                      # Babybecken, flach, Pilz-Brunnen in der Mitte
        body = rrect(x0, 0, x1, H * 0.7, 3)
        c.fill(body, zone=1)
        c.fill(rrect(x0 - 2, H * 0.62, x1 + 2, H * 0.72, 2), zone=3)
        _water(c, x0 + 4, x1 - 4, H * 0.1, H * 0.64, waves=5)
        c.fill(rrect(-4, H * 0.5, 4, H * 0.95, 1.5), zone=3)
        cap = smooth([(-W * 0.14, H * 0.9, "s"), (0, H * 1.12), (W * 0.14, H * 0.9, "s")])
        c.fill(cap, zone=1, shade=1.1)
        for dx in (-0.08, 0, 0.08):
            c.fill(ell(W * dx, H * 0.98, 2.4, 2.4, 10), zone=3, shade=1.3)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "diving_tower":                                   # Sprungturm mit Brettern 1 m, 3 m, 5 m
        col = rrect(x0 + W * 0.55, 0, x1 - 6, H * 0.94, 2)
        shaded(c, col, 3, "right", SHADE, 0.2)
        c.line(col, INNER, zone=0, closed=True)
        for k, fy in enumerate((100 / 540, 300 / 540, 500 / 540)):
            y = H * fy
            reach = W * (0.3 if k == 0 else 0.1 if k == 1 else 0.0)
            board = rrect(x0 + reach, y - 5, x1 - 6, y + 5, 2)
            c.fill(board, zone=1, shade=1.0 - k * 0.04)
            c.line(board, INNER, zone=0, closed=True)
            c.line([(x1 - 10, y + 3), (x1 - 10, y + 24), (x0 + W * 0.58, y + 24)], 1.0, zone=3, shade=0.8)
        _ladder(c, x1 - 16, 0, H * 0.94, 14)
        c.fill(rrect(x0 + W * 0.52, H * 0.94, x1 - 4, H, 1), zone=2)   # Fahne oben
    elif style == "water_slide":                                    # Röhren-Rutsche: Turm links, Kurve, Auslauf rechts
        c.fill(rrect(x0 + 6, 0, x0 + W * 0.2, H * 0.86, 1.5), zone=3, shade=0.9)
        _ladder(c, x0 + W * 0.13, 0, H * 0.86, 16)
        c.fill(rrect(x0, H * 0.84, x0 + W * 0.26, H * 0.88, 1), zone=1, shade=0.85)
        tube = [(x0 + W * 0.22, H * 0.86), (x0 + W * 0.45, H * 0.8), (x0 + W * 0.62, H * 0.62), (x0 + W * 0.5, H * 0.45),
                (x0 + W * 0.62, H * 0.28), (x1 - 20, H * 0.12), (x1, H * 0.1)]
        c.line(smooth(tube, closed=False), 26.0, zone=1)
        c.line(smooth(tube, closed=False), 18.0, zone=1, shade=1.12)
        c.line(smooth([(p[0], p[1] + 6) for p in tube], closed=False), 3.0, zone=2, shade=1.2)
        for fx in (0.45, 0.6, 0.75):
            c.fill(rrect(x0 + W * fx - 2, 0, x0 + W * fx + 2, H * (0.7 - fx * 0.7), 0.4), zone=3)
    elif style == "whirlpool":                                      # rundes Becken, Zustand „on“ = Blubbern
        body = trap(x0, x1, 0, x0 + 6, x1 - 6, H * 0.72, 3)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 - 3, H * 0.66, x1 + 3, H * 0.76, 3), zone=3)
        cl = _water(c, x0 + 10, x1 - 10, H * 0.72, H * 0.9, waves=4, bubbles=state == "on")
        if state == "on":
            for k in range(7):
                bx = x0 + 20 + k * (W - 40) / 6
                c.fill(ell(bx, H * 0.92 + (k % 2) * 3, 4, 3, 12), zone=3, shade=1.25, alpha=0.9)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "guard_chair":                                    # Bademeister-Hochstuhl mit Schirm
        for sx in (-1, 1):
            c.line([(sx * W * 0.4, 0), (sx * W * 0.22, H * 0.66)], 2.4, zone=3)
        for k in range(1, 4):
            y = k * H * 0.16
            c.line([(-W * (0.4 - 0.18 * y / (H * 0.66)), y), (W * (0.4 - 0.18 * y / (H * 0.66)), y)], 1.4, zone=3)
        cushion(c, -W * 0.3, H * 0.66, W * 0.3, H * 0.72, zone=1)
        c.fill(rrect(-W * 0.28, H * 0.72, -W * 0.22, H * 0.88, 1), zone=1, shade=0.9)
        c.line([(W * 0.26, H * 0.66), (W * 0.26, H * 0.96)], 1.0, zone=3)
        c.fill(smooth([(W * 0.26 - 26, H * 0.94, "s"), (W * 0.26, H), (W * 0.26 + 26, H * 0.94, "s")]), zone=2)
    elif style == "lifebuoy":                                       # Rettungsring: rot-weiß
        ring = ell(0, H / 2, W / 2, H / 2, 48)
        c.fill(ring, zone=1)
        cl = c.mask(ring)
        for a in (0.25, 0.75):
            ang = a * math.pi
            c.fill([(0, H / 2), (math.cos(ang - 0.3) * W, H / 2 + math.sin(ang - 0.3) * H),
                    (math.cos(ang + 0.3) * W, H / 2 + math.sin(ang + 0.3) * H)], zone=3, clip=cl)
            c.fill([(0, H / 2), (-math.cos(ang - 0.3) * W, H / 2 - math.sin(ang - 0.3) * H),
                    (-math.cos(ang + 0.3) * W, H / 2 - math.sin(ang + 0.3) * H)], zone=3, clip=cl)
        c.erase(ell(0, H / 2, W * 0.26, H * 0.26, 32))
        c.line(ring, INNER, zone=0, closed=True)
    elif style == "shower":                                         # freistehende Dusche, Zustand „on“ = Wasser
        c.fill(rrect(-W * 0.4, 0, W * 0.4, 4, 1), zone=3, shade=0.9)
        c.fill(rrect(-2, 0, 2, H * 0.9, 0.8), zone=3)
        c.line([(0, H * 0.9), (0, H * 0.97), (W * 0.3, H * 0.97)], 1.6, zone=3)
        c.fill(ell(W * 0.3, H * 0.95, W * 0.16, 3, 16), zone=3, shade=1.2)
        c.fill(ell(0, H * 0.5, 4, 4, 12), zone=1)
        if state == "on":
            for k in range(6):
                x = W * 0.3 + (k - 2.5) * 3
                c.line([(x, H * 0.93), (x + (k - 2.5) * 1.5, H * 0.35)], 1.4, zone=2, shade=0.9)
    elif style == "start_block":                                    # Startblock mit Nummer (Punkte statt Ziffer)
        body = trap(x0 + 4, x1 - 4, 0, x0, x1, H * 0.85, 1)
        shaded(c, body, 3, "right", SHADE, 0.2)
        top = trap(x0 - 2, x1 + 2, H * 0.85, x0 + 2, x1 + 6, H, 1)
        c.fill(top, zone=2)
        for k in range(3):
            c.fill(ell(-8 + k * 8, H * 0.45, 2.6, 2.6, 10), zone=2)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "kickboard":                                      # Schwimmbrett (von vorne, leicht schräg)
        b = smooth([(x0, 0, "s"), (x1, 0, "s"), (x1, H * 0.8), (0, H), (x0, H * 0.8)])
        shaded(c, b, 1, "right", SOFT, 0.25)
        c.fill(ell(0, H * 0.7, W * 0.18, H * 0.08, 16), zone=2)
        c.line(b, INNER, zone=0, closed=True)
    elif style == "dive_rings":                                     # 3 Tauchringe
        for k, z in enumerate((1, 2, 3)):
            r = ell(x0 + W * (0.25 + k * 0.25), H * 0.45, W * 0.13, H * 0.42, 24)
            c.fill(r, zone=z)
            c.erase(ell(x0 + W * (0.25 + k * 0.25), H * 0.45, W * 0.07, H * 0.22, 16))
    elif style == "beach_ball":                                     # Wasserball mit Segmenten
        ball = ell(0, H / 2, W / 2, H / 2, 48)
        c.fill(ball, zone=3)
        cl = c.mask(ball)
        for k, z in enumerate((1, 2, 1, 2)):
            a0 = k * math.pi / 2 + 0.2
            c.fill([(0, H / 2), (math.cos(a0) * W, H / 2 + math.sin(a0) * W), (math.cos(a0 + 0.7) * W, H / 2 + math.sin(a0 + 0.7) * W)],
                   zone=z, clip=cl)
        c.fill(ell(0, H / 2, W * 0.1, H * 0.1, 16), zone=3)
        c.fill(ell(-W * 0.18, H * 0.72, W * 0.1, H * 0.06, 12), zone=3, shade=1.3, clip=cl, alpha=0.7)
        c.line(ball, INNER, zone=0, closed=True)
    elif style == "kiosk":                                          # Kiosk: Theke, Fenster, Markise, Eis-Symbol
        body = rrect(x0, 0, x1, H * 0.72, 1.2)
        shaded(c, body, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0 + 10, H * 0.46, x1 - 10, H * 0.7, 0.8), zone=3, shade=0.5)
        c.fill(rrect(x0 - 4, H * 0.44, x1 + 4, H * 0.48, 0.8), zone=3)
        for k in range(8):
            s = [(x0 - 6 + k * (W + 12) / 8, H * 0.86), (x0 - 6 + (k + 1) * (W + 12) / 8, H * 0.86),
                 (x0 - 6 + (k + 1) * (W + 12) / 8, H * 0.76), (x0 - 6 + (k + 0.5) * (W + 12) / 8, H * 0.72),
                 (x0 - 6 + k * (W + 12) / 8, H * 0.76)]
            c.fill(s, zone=2 if k % 2 else 3)
        c.fill(rrect(x0 + W * 0.3, H * 0.88, x1 - W * 0.3, H, 2), zone=3)
        c.fill(trap(-5, 5, H * 0.89, -7, 7, H * 0.95, 0.4), zone=1, shade=0.8)
        c.fill(ell(0, H * 0.965, 6, 4, 16), zone=2)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "lockers":                                        # Spinde (2 × 3), Zustand „open“ = eine Tür offen
        body = rrect(x0, 0, x1, H, 1)
        c.fill(body, zone=1)
        for i in range(2):
            for j in range(3):
                d = rrect(x0 + 4 + i * (W - 8) / 2, 4 + j * (H - 8) / 3, x0 + 2 + (i + 1) * (W - 8) / 2, 2 + (j + 1) * (H - 8) / 3, 0.8)
                if state == "open" and i == 1 and j == 1:
                    c.fill(d, zone=3, shade=0.45)
                    c.fill(ell(x0 + W * 0.75, 4 + 1.5 * (H - 8) / 3, 6, 6, 12), zone=2)
                    continue
                shaded(c, d, 1, "right", SHADE, 0.2)
                c.line(d, INNER, zone=0, closed=True)
                c.fill(ell(x0 + 8 + i * (W - 8) / 2, 4 + (j + 0.5) * (H - 8) / 3, 1.8, 1.8, 8), zone=3)
                for k in range(3):
                    c.fill(rrect(x0 + (i + 0.35) * (W - 8) / 2 + k * 5, 4 + (j + 0.8) * (H - 8) / 3,
                                 x0 + (i + 0.35) * (W - 8) / 2 + k * 5 + 3, 4 + (j + 0.85) * (H - 8) / 3, 0.3), zone=1, shade=0.8)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "cabin":                                          # Umkleidekabine mit Vorhang (open = zur Seite)
        c.fill(rrect(x0, 0, x0 + 4, H, 0.6), zone=3)
        c.fill(rrect(x1 - 4, 0, x1, H, 0.6), zone=3)
        c.fill(rrect(x0, H - 6, x1, H, 0.6), zone=1)
        c.fill(rrect(x0 + 4, 12, x1 - 4, H - 6, 0.5), zone=3, shade=0.6)
        cw = (W - 8) * (0.25 if state == "open" else 1.0)
        cur = rrect(x0 + 4, 14, x0 + 4 + cw, H - 8, 1.5)
        c.fill(cur, zone=2)
        for k in range(1, int(cw / 10) + 1):
            c.line([(x0 + 4 + k * 10, H - 8), (x0 + 4 + k * 10, 14)], 0.5, zone=2, shade=0.8)
    elif style == "turnstile":                                      # Drehkreuz am Eingang
        body = rrect(x0, 0, x0 + W * 0.4, H, 2)
        shaded(c, body, 3, "right", SHADE, 0.2)
        c.fill(ell(x0 + W * 0.2, H * 0.85, W * 0.12, H * 0.05, 12), zone=2, shade=1.3)
        for a in (0.1, 0.5, 0.9):
            c.line([(x0 + W * 0.4, H * 0.7), (x0 + W * 0.4 + math.cos(a) * W * 0.6, H * 0.7 - math.sin(a) * H * 0.15)], 2.0, zone=1)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "wave_sign":                                      # Wellen-Anzeige: Ampel, Zustand „on“ = Wellen
        box = rrect(x0, 0, x1, H, 3)
        c.fill(box, zone=1)
        c.fill(rrect(x0 + 5, 5, x1 - 5, H - 5, 2), zone=3, shade=0.3)
        glow = 1.6 if state == "on" else 0.8
        for k in range(3):
            y = H * (0.3 + k * 0.2)
            c.line(smooth([(x0 + 10, y), (x0 + W * 0.3, y + 5), (0, y), (W * 0.2, y + 5), (x1 - 10, y)], closed=False),
                   2.0, zone=2, shade=glow)
        c.line(box, INNER, zone=0, closed=True)
    elif style == "bench_tiled":                                    # geflieste Sitzbank am Beckenrand
        for x in (x0 + 10, x1 - 10):
            leg(c, x, 0, H * 0.8, 6, 6, zone=3)
        cushion(c, x0, H * 0.8, x1, H, zone=1)
    else:
        raise ValueError(style)
