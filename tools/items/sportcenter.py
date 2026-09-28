"""
Sportzentrum (P10e, Welt-Doku §8): Laufband, Heimtrainer, Hantelbank, Gymnastikball, Tribüne, Anzeigetafel
(Punkte statt Ziffern), Kletterwand mit Seil, Ballettstange, Spiegelwand, Tennisnetz, Fußball, Tennisball,
Fußballtor 5 × 2 m mit Netz, Eckfahne, Spielfeld-Markierung, Tutu, Ballettschuhe.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Weiß.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, cushion, ell, leg, rrect, shaded, smooth, trap


def sportcenter(it: Item, style: str = "treadmill", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "treadmill":                                        # Laufband (on = Band läuft, Anzeige leuchtet)
        belt = rrect(x0, 4, x1 - W * 0.1, 22, 6)
        shaded(c, belt, 1, "bottom", SHADE, 0.3)
        for k in range(8 if state == "on" else 0):
            c.line([(x0 + 14 + k * (W * 0.85 - 20) / 8, 20), (x0 + 20 + k * (W * 0.85 - 20) / 8, 20)], 0.8, zone=3, shade=0.8)
        c.fill(ell(x0 + 10, 12, 8, 8, 16), zone=3, shade=0.8)
        c.line(smooth([(x1 - W * 0.14, 16), (x1 - W * 0.06, H * 0.7), (x1 - W * 0.02, H * 0.72)], closed=False), 2.4, zone=3)
        c.line([(x1 - W * 0.08, H * 0.7), (x1 - W * 0.38, H * 0.66)], 1.8, zone=3)
        scr = rrect(x1 - W * 0.14, H * 0.72, x1, H, 3)
        c.fill(scr, zone=2, shade=1.4 if state == "on" else 0.8)
        c.line(scr, INNER, zone=0, closed=True)
        c.line(belt, INNER, zone=0, closed=True)
    elif style == "bike":                                           # Heimtrainer
        c.fill(rrect(x0 + 6, 0, x1 - 6, 6, 3), zone=3, shade=0.8)
        c.line([(x0 + W * 0.3, 4), (x0 + W * 0.4, H * 0.7)], 3.0, zone=1)
        c.line([(x1 - W * 0.25, 4), (x1 - W * 0.2, H * 0.8)], 3.0, zone=1)
        c.fill(ell(x1 - W * 0.3, H * 0.3, W * 0.18, W * 0.18, 32), zone=2)
        c.fill(ell(x1 - W * 0.3, H * 0.3, W * 0.05, W * 0.05, 16), zone=3)
        cushion(c, x0 + W * 0.26, H * 0.7, x0 + W * 0.56, H * 0.78, zone=1)
        c.line([(x1 - W * 0.2, H * 0.8), (x1 - W * 0.36, H * 0.95)], 2.0, zone=3)
        c.fill(rrect(x1 - W * 0.3, H * 0.84, x1 - W * 0.1, H * 0.92, 2), zone=2, shade=1.2)
    elif style == "bench":                                          # Hantelbank mit Stange
        for x in (x0 + 18, x1 - 18):
            leg(c, x, 0, H * 0.7, 5, 5, zone=3)
        cushion(c, x0, H * 0.62, x1, H * 0.8, zone=1)
        for sx in (-1, 1):
            c.line([(sx * W * 0.34, H * 0.8), (sx * W * 0.34, H)], 2.0, zone=3)
    elif style == "yoga_ball":                                      # Gymnastikball
        b = ell(0, H / 2, W / 2, H / 2, 48)
        shaded(c, b, 1, "right", SOFT, 0.35)
        c.fill(ell(-W * 0.18, H * 0.72, W * 0.12, H * 0.07, 16), zone=3, shade=1.3, alpha=0.6)
        c.line(b, INNER, zone=0, closed=True)
    elif style == "bleachers":                                      # Tribüne: 3 Stufen mit Sitzschalen
        for k in range(3):
            y0, y1 = k * H / 3, (k + 1) * H / 3
            step = rrect(x0 + k * 20, 0, x1 - k * 20, y1, 1)
            c.fill(step, zone=3, shade=0.9 - k * 0.04)
            c.line(step, INNER, zone=0, closed=True)
            n = int((W - k * 40) / 60)
            for j in range(n):
                sx = x0 + k * 20 + 10 + j * (W - k * 40 - 20) / n
                seat = rrect(sx + 4, y1 - 4, sx + (W - k * 40 - 20) / n - 4, y1 + 8, 3)
                c.fill(seat, zone=1 if (j + k) % 2 else 2)
    elif style == "scoreboard":                                     # Anzeigetafel: Tore als Bälle (s0 … s5)
        box = rrect(x0, 0, x1, H, 3)
        c.fill(box, zone=1)
        c.fill(rrect(x0 + 6, 6, x1 - 6, H - 6, 2), zone=3, shade=0.2)
        n = int(state[1:]) if state.startswith("s") else 0
        for k in range(5):
            cx = x0 + W * (0.14 + k * 0.18)
            c.fill(ell(cx, H * 0.5, W * 0.07, W * 0.07, 24), zone=2 if k < n else 3, shade=1.4 if k < n else 0.35)
        c.line(box, INNER, zone=0, closed=True)
    elif style == "climbing_wall":                                  # Kletterwand mit bunten Griffen und Seil
        wall = trap(x0, x1, 0, x0 + 6, x1 - 6, H, 2)
        shaded(c, wall, 3, "right", SHADE, 0.12)
        for k in range(int(H / 40)):
            for j in range(4):
                gx = x0 + W * (0.12 + j * 0.25) + math.sin(k * 1.7 + j) * W * 0.06
                gy = 30 + k * 40 + math.cos(k + j * 2.1) * 8
                if gy > H - 30:
                    continue
                c.fill(ell(gx, gy, 9, 6, 12), zone=1 if (k + j) % 3 == 0 else 2 if (k + j) % 3 == 1 else 3, shade=1.0 if (k + j) % 3 < 2 else 0.6)
        for x in (x0 + W * 0.3, x1 - W * 0.3):
            c.line([(x, H - 10), (x, 90)], 1.4, zone=2, shade=0.8)
        c.fill(rrect(x0, H - 14, x1, H, 2), zone=1, shade=0.8)
        c.line(wall, INNER, zone=0, closed=True)
    elif style == "barre":                                          # Ballettstange (2 Höhen)
        for x in (x0 + 12, x1 - 12):
            c.fill(rrect(x - 3, 0, x + 3, H, 1), zone=3)
        for fy in (0.66, 0.97):
            c.fill(rrect(x0, H * fy - 3, x1, H * fy + 3, 3), zone=1)
    elif style == "mirror":                                         # Spiegelwand (Wand)
        fr = rrect(x0, 0, x1, H, 2)
        c.fill(fr, zone=1)
        c.glass(rrect(x0 + 5, 5, x1 - 5, H - 5, 1), zone=3, opacity=0.6, shade=1.2)
        for k in range(3):
            c.line([(x0 + W * (0.2 + k * 0.25), H * 0.2), (x0 + W * (0.3 + k * 0.25), H * 0.8)], 1.5, zone=3, shade=1.4)
        c.line(fr, INNER, zone=0, closed=True)
    elif style == "tennis_net":                                     # Tennisnetz mit Pfosten
        for x in (x0 + 4, x1 - 4):
            c.fill(rrect(x - 4, 0, x + 4, H, 1.5), zone=3, shade=0.8)
        for k in range(int((W - 16) / 8)):
            c.line([(x0 + 8 + k * 8, 4), (x0 + 8 + k * 8, H * 0.86)], 0.35, zone=0, shade=0.8)
        for k in range(int(H * 0.86 / 8)):
            c.line([(x0 + 8, 4 + k * 8), (x1 - 8, 4 + k * 8)], 0.35, zone=0, shade=0.8)
        c.fill(rrect(x0 + 6, H * 0.86, x1 - 6, H * 0.92, 1), zone=3, shade=1.2)
    elif style in ("football", "tennis_ball"):                      # Fußball (Fünfecke) / Tennisball (Naht)
        b = ell(0, H / 2, W / 2, H / 2, 40)
        c.fill(b, zone=3 if style == "football" else 1)
        cl = c.mask(b)
        if style == "football":
            c.fill(ell(0, H * 0.5, W * 0.14, H * 0.14, 5), zone=0)
            for k in range(5):
                a = math.pi / 2 + k * 2 * math.pi / 5
                c.fill(ell(math.cos(a) * W * 0.42, H * 0.5 + math.sin(a) * H * 0.42, W * 0.13, H * 0.13, 5), zone=0, clip=cl)
        else:
            c.line(smooth([(-W * 0.5, H * 0.7), (0, H * 0.5), (W * 0.5, H * 0.7)], closed=False), 0.4, zone=3, clip=cl)
            c.line(smooth([(-W * 0.5, H * 0.3), (0, H * 0.5), (W * 0.5, H * 0.3)], closed=False), 0.4, zone=3, clip=cl)
        c.line(b, INNER, zone=0, closed=True)
    elif style == "goal":                                           # Fußballtor 5 × 2 m mit Netz-Tiefe
        c.fill(trap(x0 + 20, x1 - 20, H * 0.05, x0 + 8, x1 - 8, H * 0.92, 0.5), zone=3, shade=0.9, alpha=0.25)
        for k in range(1, int(W / 16)):
            c.line([(x0 + k * 16, 0), (x0 + 8 + k * 16 * (W - 16) / W, H * 0.92)], 0.35, zone=0, shade=0.7)
        for k in range(1, int(H / 16)):
            c.line([(x0 + 6, k * 16), (x1 - 6, k * 16)], 0.35, zone=0, shade=0.7)
        for x in (x0 + 4, x1 - 4):
            c.fill(rrect(x - 5, 0, x + 5, H, 2), zone=1)
        c.fill(rrect(x0, H - 10, x1, H, 3), zone=1)
    elif style == "corner_flag":                                    # Eckfahne
        c.fill(rrect(-1.2, 0, 1.2, H, 0.6), zone=3)
        c.fill([(1, H), (W - 2, H * 0.86), (1, H * 0.72)], zone=1)
    elif style == "pitch":                                          # Spielfeld-Markierung (flach am Boden)
        c.fill(rrect(x0, 0, x1, H, 2), zone=1)
        for k in range(int(W / 80)):
            c.fill(rrect(x0 + k * 80, 0, x0 + k * 80 + 40, H, 0.5), zone=1, shade=1.06)
        c.line(rrect(x0 + 10, H * 0.1, x1 - 10, H * 0.9, 1), 1.4, zone=3, closed=True)
        c.line([(0, H * 0.1), (0, H * 0.9)], 1.4, zone=3)
        c.line(ell(0, H * 0.5, H * 0.9, H * 0.36, 48), 1.4, zone=3, closed=True)
    elif style == "court":                                          # Tennisplatz (flach, Sand)
        c.fill(rrect(x0, 0, x1, H, 2), zone=1)
        c.line(rrect(x0 + 10, H * 0.1, x1 - 10, H * 0.9, 1), 1.2, zone=3, closed=True)
        c.line([(x0 + 10, H * 0.5), (x1 - 10, H * 0.5)], 1.0, zone=3)
    elif style == "tutu":                                           # Tutu (zum Anziehen)
        c.fill(rrect(x0 + W * 0.25, H * 0.6, x1 - W * 0.25, H, 2), zone=2)
        t = smooth([(x0 + W * 0.2, H * 0.6), (x0, H * 0.2), (x0 + W * 0.2, 0), (x1 - W * 0.2, 0), (x1, H * 0.2), (x1 - W * 0.2, H * 0.6)])
        c.fill(t, zone=1)
        for k in range(6):
            c.line([(x0 + W * (0.2 + k * 0.12), H * 0.55), (x0 + W * (0.1 + k * 0.16), H * 0.05)], 0.5, zone=1, shade=0.85)
        c.line(t, INNER, zone=0, closed=True)
    elif style == "ballet_shoes":                                   # Ballettschuhe mit Bändern
        for sx in (-1, 1):
            s = ell(sx * W * 0.24, H * 0.3, W * 0.22, H * 0.3, 24)
            shaded(c, s, 1, "right", SOFT, 0.3)
            c.line(smooth([(sx * W * 0.24, H * 0.5), (sx * W * 0.1, H * 0.9), (sx * W * 0.3, H)], closed=False), 0.6, zone=2)
            c.line(s, INNER, zone=0, closed=True)
    else:
        raise ValueError(style)
