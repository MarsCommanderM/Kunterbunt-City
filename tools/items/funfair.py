"""
Rummelplatz (P10d, Welt-Doku §7): Riesenrad, Karussell, Autoscooter (Wagen + Fahrfläche), Achterbahn (Schiene +
Wagen), Geisterbahn (Haus + Wagen, lustig), Spielbude, Dosenwerfen, Entenangeln, Lostrommel, Hau den Lukas,
Bühne mit Vorhang, Zauberhut, Jonglierbälle, Plüsch-Gewinn, Luftballon, Liebesapfel, Zuckerwatte-Stand, Eingangstor.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Weiß.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, cushion, ell, rrect, shaded, smooth, trap


def coaster_y(u: float, h: float) -> float:
    """Höhe der Achterbahn-Schiene bei u ∈ [0, 1] (auch vom Spiel für die Fahrt benutzt – gleiche Formel)."""
    return 30.0 + (h - 60.0) * (0.75 * math.sin(math.pi * u) ** 2 + 0.25 * abs(math.sin(3 * math.pi * u)))


def _bulbs(c, pts: list, every: int = 1):
    for k, (x, y) in enumerate(pts):
        if k % every == 0:
            c.fill(ell(x, y, 2.2, 2.2, 10), zone=2, shade=1.4)


def _flag_top(c, x: float, y: float, s: float = 20.0):
    c.line([(x, y), (x, y + s)], 1.0, zone=3)
    c.fill([(x, y + s), (x + s * 0.7, y + s * 0.8), (x, y + s * 0.6)], zone=2)


def funfair(it: Item, style: str = "ferris_wheel", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "ferris_wheel":                                     # Kinder-Riesenrad, Gondel unten = Einstieg
        cy, r = H * 0.58, min(W * 0.44, H * 0.4)
        for sx in (-1, 1):
            c.line([(sx * W * 0.3, 0), (0, cy)], 4.0, zone=3, shade=0.9)
        c.line(ell(0, cy, r, r, 64), 3.0, zone=1, closed=True)
        c.line(ell(0, cy, r * 0.94, r * 0.94, 64), 1.2, zone=1, shade=1.2, closed=True)
        n = 8
        for k in range(n):
            a = 2 * math.pi * k / n
            c.line([(0, cy), (math.cos(a) * r, cy + math.sin(a) * r)], 1.0, zone=3)
        _bulbs(c, [(math.cos(2 * math.pi * k / 32) * r, cy + math.sin(2 * math.pi * k / 32) * r) for k in range(32)])
        c.fill(ell(0, cy, 14, 14, 24), zone=2)
        for k in range(n):
            a = 2 * math.pi * k / n - math.pi / 2
            gx, gy = math.cos(a) * r, cy + math.sin(a) * r
            g = rrect(gx - 48, gy - 92, gx + 48, gy - 10, 10)
            c.line([(gx, gy), (gx, gy - 10)], 1.6, zone=3)
            c.fill(g, zone=1 if k % 2 else 2)
            c.fill(rrect(gx - 38, gy - 58, gx + 38, gy - 26, 5), zone=3, shade=0.9)
            c.line(g, INNER, zone=0, closed=True)
        c.fill(rrect(-W * 0.34, 0, W * 0.34, 8, 2), zone=3, shade=0.8)
    elif style == "carousel":                                       # Karussell: Dach, Mittelsäule, Pferde
        c.fill(rrect(x0 + 10, 0, x1 - 10, H * 0.1, 3), zone=2)
        c.fill(rrect(x0 + 6, H * 0.08, x1 - 6, H * 0.12, 2), zone=3)
        c.fill(rrect(-W * 0.07, H * 0.12, W * 0.07, H * 0.78, 2), zone=3, shade=0.95)
        for k in range(3):
            px = x0 + W * (0.2 + k * 0.3)
            c.line([(px, H * 0.12), (px, H * 0.78)], 2.0, zone=3, shade=1.2)
            hy = H * (0.3 + 0.05 * (k % 2))
            z = 3 if k % 2 else 1
            for dx in (-34, -20, 22, 36):                            # Beine im Galopp
                c.line([(px + dx, hy - 12), (px + dx * 1.15, hy - 48)], 5.0, zone=z, shade=0.95)
            body = ell(px, hy, 52, 22, 32)
            c.fill(body, zone=z, shade=1.05)
            c.line([(px + 38, hy + 8), (px + 50, hy + 40)], 14.0, zone=z)
            head = ell(px + 58, hy + 44, 18, 13, 20)
            c.fill(head, zone=z)
            c.fill(ell(px + 60, hy + 48, 2.2, 2.2, 8), zone=0)
            c.line(smooth([(px + 44, hy + 50), (px + 34, hy + 30), (px + 30, hy + 12)], closed=False), 4.0, zone=2)
            c.line(smooth([(px - 50, hy + 4), (px - 64, hy - 10), (px - 62, hy - 30)], closed=False), 5.0, zone=2)
            c.fill(ell(px - 4, hy + 20, 18, 7, 16), zone=2)
            c.line(body, INNER, zone=0, closed=True)
            c.line(head, INNER, zone=0, closed=True)
        roof = [(x0, H * 0.78), (x1, H * 0.78), (x1 - W * 0.1, H * 0.9), (0, H * 0.99), (x0 + W * 0.1, H * 0.9)]
        c.fill(roof, zone=1)
        for k in range(12):
            a = x0 + k * W / 12
            c.fill([(a, H * 0.78), (a + W / 12, H * 0.78), (a + W / 24, H * 0.72)], zone=2 if k % 2 else 3)
        _bulbs(c, [(x0 + 8 + k * (W - 16) / 20, H * 0.8) for k in range(21)])
        _flag_top(c, 0, H * 0.96, 18)
    elif style == "bumper_car":                                     # Autoscooter-Wagen mit Stange
        body = smooth([(x0, H * 0.08, "s"), (x1, H * 0.08, "s"), (x1, H * 0.35), (x1 - W * 0.2, H * 0.5), (x0 + W * 0.25, H * 0.5),
                       (x0, H * 0.38)])
        c.fill(rrect(x0 - 2, 0, x1 + 2, H * 0.14, 5), zone=3, shade=0.4)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 + W * 0.15, H * 0.4, x0 + W * 0.42, H * 0.66, 3), zone=1, shade=0.9)
        c.fill(ell(x1 - W * 0.26, H * 0.52, 8, 3, 12), zone=0)
        c.line([(x0 + W * 0.22, H * 0.5), (x0 + W * 0.22, H)], 1.2, zone=3)
        c.fill(ell(x1 - W * 0.12, H * 0.25, 6, 5, 12), zone=2, shade=1.4)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "bumper_floor":                                   # Fahrfläche (flach am Boden) mit Bande
        c.fill(rrect(x0, 0, x1, H, 3), zone=3, shade=0.55)
        for k in range(int(W / 60)):
            c.line([(x0 + 30 + k * 60, H * 0.3), (x0 + 50 + k * 60, H * 0.7)], 0.5, zone=3, shade=0.7)
        c.fill(rrect(x0, 0, x1, H * 0.2, 2), zone=1)
        c.fill(rrect(x0, H * 0.85, x1, H, 2), zone=2)
    elif style == "coaster_track":                                  # Schiene (Hügel) auf Stützen, links Bahnhof
        pts = [(x0 + u * W, coaster_y(u, H)) for u in [k / 80 for k in range(81)]]
        for k in range(0, 81, 8):
            x, y = pts[k]
            c.line([(x, 0), (x, y - 6)], 2.0, zone=3, shade=0.9)
            c.line([(x - 10, 0), (x, y * 0.5)], 1.0, zone=3, shade=0.8)
        c.line(smooth(pts, closed=False), 10.0, zone=1)
        c.line(smooth([(x, y - 4) for x, y in pts], closed=False), 1.4, zone=3, shade=1.2)
        c.fill(rrect(x0, 0, x0 + 150, 14, 2), zone=2)
        c.fill(rrect(x0 + 10, 14, x0 + 20, 120, 1), zone=3)
        c.fill(rrect(x0 + 130, 14, x0 + 140, 120, 1), zone=3)
        c.fill(trap(x0 - 10, x0 + 160, 120, x0 + 20, x0 + 130, 150, 1), zone=2, shade=0.95)
    elif style in ("coaster_car", "ghost_car"):                     # Wagen: 2 Sitze vorne/hinten (Geist: 1 + Gesicht)
        body = smooth([(x0 + 4, H * 0.1, "s"), (x1 - 4, H * 0.1, "s"), (x1, H * 0.55), (x1 - W * 0.1, H * 0.7), (x0 + W * 0.08, H * 0.6),
                       (x0, H * 0.45)])
        for x in (x0 + W * 0.22, x1 - W * 0.22):
            c.fill(ell(x, H * 0.1, H * 0.1, H * 0.1, 16), zone=0)
            c.fill(ell(x, H * 0.1, H * 0.04, H * 0.04, 10), zone=3)
        shaded(c, body, 1, "right", SHADE, 0.2)
        if style == "ghost_car":
            c.fill(ell(x1 - W * 0.18, H * 0.4, W * 0.08, W * 0.08, 16), zone=3)
            for dx in (-0.03, 0.03):
                c.fill(ell(x1 - W * (0.18 + dx), H * 0.44, 1.8, 2.4, 8), zone=0)
        else:
            c.fill(rrect(x0 + W * 0.3, H * 0.55, x0 + W * 0.34, H * 0.9, 1), zone=2)
            c.fill(rrect(x0 + W * 0.66, H * 0.55, x0 + W * 0.7, H * 0.9, 1), zone=2)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "ghost_house":                                    # Geisterbahn: Haus mit lachendem Gespenst
        body = rrect(x0, 0, x1, H * 0.75, 2)
        shaded(c, body, 1, "right", SHADE, 0.15)
        roof = [(x0 - 10, H * 0.75), (x1 + 10, H * 0.75), (x1 - W * 0.2, H * 0.92), (x0 + W * 0.2, H * 0.92)]
        c.fill(roof, zone=2, shade=0.9)
        for k in range(3):
            c.fill(trap(x0 + W * (0.22 + k * 0.22), x0 + W * (0.34 + k * 0.22), H * 0.9, x0 + W * (0.27 + k * 0.22),
                        x0 + W * (0.29 + k * 0.22), H, 0.5), zone=2, shade=0.8)
        door = smooth([(x0 + W * 0.12, 0, "s"), (x0 + W * 0.36, 0, "s"), (x0 + W * 0.36, H * 0.35), (x0 + W * 0.24, H * 0.45),
                       (x0 + W * 0.12, H * 0.35)])
        c.fill(door, zone=3, shade=0.3)
        gx, gy, g = W * 0.18, H * (0.4 if state != "boo" else 0.55), 1.8
        ghost = smooth([(gx - 50 * g, gy - 60 * g), (gx - 30 * g, gy - 45 * g), (gx - 10 * g, gy - 60 * g), (gx + 10 * g, gy - 45 * g),
                        (gx + 30 * g, gy - 60 * g), (gx + 50 * g, gy - 45 * g), (gx + 45 * g, gy + 40 * g), (gx, gy + 80 * g),
                        (gx - 45 * g, gy + 40 * g)])
        c.fill(ghost, zone=3, shade=1.2)
        for dx in (-16, 16):
            c.fill(ell(gx + dx * g, gy + 30 * g, 6 * g, 9 * g, 12), zone=0)
        mouth = ell(gx, gy + 5 * g, (14 if state == "boo" else 8) * g, (10 if state == "boo" else 4) * g, 16)
        c.fill(mouth, zone=0)
        c.fill(ell(gx - 32 * g, gy + 16 * g, 7 * g, 4 * g, 12), zone=1, shade=1.3, alpha=0.7)
        c.fill(ell(gx + 32 * g, gy + 16 * g, 7 * g, 4 * g, 12), zone=1, shade=1.3, alpha=0.7)
        c.line(ghost, INNER, zone=0, closed=True)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "booth":                                          # Spielbude: Theke, Markise, Regal mit Preisen
        c.fill(rrect(x0 + 6, 0, x0 + 12, H * 0.82, 1), zone=3)
        c.fill(rrect(x1 - 12, 0, x1 - 6, H * 0.82, 1), zone=3)
        c.fill(rrect(x0 + 12, H * 0.38, x1 - 12, H * 0.82, 1), zone=3, shade=0.7)
        for k in range(2):
            y = H * (0.52 + k * 0.16)
            c.fill(rrect(x0 + 16, y - 2, x1 - 16, y, 0.6), zone=1, shade=0.8)
            for j in range(5):
                px = x0 + W * (0.2 + j * 0.15)
                c.fill(ell(px, y + 9, 8, 9, 16), zone=2 if (j + k) % 2 else 1, shade=1.1)
                c.fill(ell(px - 5, y + 17, 3, 3, 8), zone=2 if (j + k) % 2 else 1, shade=1.1)
                c.fill(ell(px + 5, y + 17, 3, 3, 8), zone=2 if (j + k) % 2 else 1, shade=1.1)
        counter = rrect(x0, 0, x1, H * 0.38, 1.2)
        shaded(c, counter, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0 - 3, H * 0.36, x1 + 3, H * 0.4, 1), zone=2)
        for k in range(8):
            s = [(x0 - 6 + k * (W + 12) / 8, H * 0.93), (x0 - 6 + (k + 1) * (W + 12) / 8, H * 0.93),
                 (x0 - 6 + (k + 1) * (W + 12) / 8, H * 0.84), (x0 - 6 + (k + 0.5) * (W + 12) / 8, H * 0.8),
                 (x0 - 6 + k * (W + 12) / 8, H * 0.84)]
            c.fill(s, zone=2 if k % 2 else 3)
        c.fill(rrect(x0 + W * 0.3, H * 0.93, x1 - W * 0.3, H, 2), zone=1)
        c.line(counter, INNER, zone=0, closed=True)
    elif style == "cans":                                           # Dosenpyramide (Zustand „fallen“ = umgeworfen)
        cw, ch = W / 3.2, H / 3.1
        spots = [(-1, 0), (0, 0), (1, 0), (-0.5, 1), (0.5, 1), (0, 2)] if state != "fallen" else \
                [(-1.2, 0), (-0.2, 0), (0.9, 0), (1.9, 0)]
        for k, (i, j) in enumerate(spots):
            can = rrect(i * cw * 1.02 - cw / 2, j * ch, i * cw * 1.02 + cw / 2, j * ch + ch * 0.96, 0.6)
            c.fill(can, zone=1 if k % 2 else 2)
            c.fill(rrect(i * cw * 1.02 - cw / 2, j * ch + ch * 0.4, i * cw * 1.02 + cw / 2, j * ch + ch * 0.6, 0.3), zone=3)
            c.line(can, INNER, zone=0, closed=True)
    elif style == "duck_pond":                                      # Entenangeln: rundes Becken mit Enten
        body = trap(x0, x1, 0, x0 + 6, x1 - 6, H * 0.7, 3)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 - 3, H * 0.62, x1 + 3, H * 0.72, 3), zone=3)
        for k in range(5):
            dx = x0 + W * (0.14 + k * 0.18)
            c.fill(ell(dx, H * 0.8, 10, 7, 16), zone=2)
            c.fill(ell(dx + 7, H * 0.94, 5, 5, 12), zone=2)
            c.fill([(dx + 11, H * 0.94), (dx + 16, H * 0.92), (dx + 11, H * 0.9)], zone=1, shade=1.2)
            c.line([(dx, H * 0.86), (dx - 2, H * 0.96)], 0.5, zone=0)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "lottery":                                        # Losrad auf Ständer (Zustand „spin“)
        c.fill(trap(-W * 0.3, W * 0.3, 0, -W * 0.08, W * 0.08, H * 0.4, 0.6), zone=3)
        wheel = ell(0, H * 0.62, W * 0.46, H * 0.38, 48)
        c.fill(wheel, zone=3)
        cl = c.mask(wheel)
        off = 0.4 if state == "spin" else 0.0
        for k in range(8):
            a = 2 * math.pi * k / 8 + off
            c.fill([(0, H * 0.62), (math.cos(a) * W, H * 0.62 + math.sin(a) * H), (math.cos(a + 0.785) * W, H * 0.62 + math.sin(a + 0.785) * H)],
                   zone=1 if k % 2 else 2, clip=cl)
        c.fill(ell(0, H * 0.62, 3, 3, 10), zone=3)
        c.fill([(-4, H * 1.0), (4, H * 1.0), (0, H * 0.92)], zone=0)
        c.line(wheel, INNER, zone=0, closed=True)
    elif style == "high_striker":                                   # Hau den Lukas: Turm, Skala, Glocke (ring)
        c.fill(rrect(-W * 0.4, 0, W * 0.4, 12, 2), zone=2)
        c.fill(rrect(-8, 12, 8, H * 0.92, 2), zone=3)
        for k in range(10):
            y = 20 + k * (H * 0.85 - 20) / 10
            c.fill(rrect(-W * 0.3, y, W * 0.3, y + 8, 2), zone=1 if k % 2 else 2, shade=1.0 + k * 0.02)
        py = H * 0.86 if state == "ring" else H * 0.1
        c.fill(ell(0, py, 7, 7, 16), zone=2, shade=0.8)
        c.fill(ell(0, H * 0.96, 16, 10, 24), zone=2, shade=1.2 if state == "ring" else 0.9)
        if state == "ring":
            for a in (-0.6, -0.3, 0.3, 0.6):
                c.line([(math.sin(a) * 22, H * 0.96 + math.cos(a) * 14), (math.sin(a) * 34, H * 0.96 + math.cos(a) * 24)],
                       1.2, zone=2, shade=1.3)
    elif style == "stage":                                          # Bühne mit Vorhang (open/closed)
        floor = rrect(x0, 0, x1, H * 0.34, 1.5)
        shaded(c, floor, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0 - 3, H * 0.32, x1 + 3, H * 0.36, 1), zone=3)
        c.fill(rrect(x0, H * 0.36, x0 + 16, H, 1), zone=1, shade=0.8)
        c.fill(rrect(x1 - 16, H * 0.36, x1, H, 1), zone=1, shade=0.8)
        c.fill(rrect(x0, H * 0.9, x1, H, 1), zone=2)
        cover = 0.12 if state == "open" else 0.5
        for sx in (-1, 1):
            edge = sx * W * (0.5 - cover)
            cur = [(sx * (W / 2 - 16), H * 0.9), (edge, H * 0.9), (edge + sx * 10, H * 0.36), (sx * (W / 2 - 16), H * 0.36)]
            c.fill(cur, zone=2, shade=0.9)
            for k in range(1, 6):
                xx = sx * (W / 2 - 16) + (edge - sx * (W / 2 - 16)) * k / 6
                c.line([(xx, H * 0.9), (xx + sx * 2, H * 0.36)], 0.8, zone=2, shade=0.75)
        _bulbs(c, [(x0 + 20 + k * (W - 40) / 16, H * 0.93) for k in range(17)])
        c.line(floor, INNER, zone=0, closed=True)
    elif style == "magic_hat":                                      # Zylinder (Zustand „rabbit“ = Hase schaut raus)
        if state == "rabbit":
            c.fill(ell(0, H * 0.9, W * 0.18, H * 0.16, 16), zone=3)
            for dx in (-0.08, 0.08):
                c.fill(ell(W * dx, H * 1.1, W * 0.05, H * 0.16, 12), zone=3)
            for dx in (-0.06, 0.06):
                c.fill(ell(W * dx, H * 0.92, 1.2, 1.6, 8), zone=0)
        c.fill(ell(0, H * 0.08, W * 0.5, H * 0.08, 24), zone=1)
        hat = trap(-W * 0.34, W * 0.34, H * 0.08, -W * 0.3, W * 0.3, H * 0.75, 0.8)
        shaded(c, hat, 1, "right", SOFT, 0.2)
        c.fill(rrect(-W * 0.34, H * 0.12, W * 0.34, H * 0.24, 0.4), zone=2)
        c.line(hat, INNER, zone=0, closed=True)
    elif style == "juggling":                                       # 3 Jonglierbälle
        for k, z in enumerate((1, 2, 3)):
            b = ell(x0 + W * (0.18 + k * 0.32), H * 0.5, W * 0.16, H * 0.48, 24)
            shaded(c, b, z, "right", SOFT, 0.3)
            c.line(b, INNER, zone=0, closed=True)
    elif style == "prize":                                          # Plüsch-Gewinn: großer Bär mit Schleife
        c.fill(ell(0, H * 0.3, W * 0.42, H * 0.3, 32), zone=1)
        c.fill(ell(0, H * 0.72, W * 0.34, H * 0.26, 32), zone=1)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.26, H * 0.94, W * 0.12, H * 0.08, 16), zone=1, shade=0.95)
            c.fill(ell(sx * W * 0.3, H * 0.1, W * 0.14, H * 0.1, 16), zone=1, shade=0.95)
            c.fill(ell(sx * W * 0.12, H * 0.76, W * 0.035, H * 0.04, 10), zone=0)
        c.fill(ell(0, H * 0.64, W * 0.12, H * 0.08, 16), zone=3)
        c.fill(ell(0, H * 0.67, W * 0.04, H * 0.03, 10), zone=0)
        c.fill([(-W * 0.2, H * 0.5), (0, H * 0.46), (-W * 0.2, H * 0.42)], zone=2)
        c.fill([(W * 0.2, H * 0.5), (0, H * 0.46), (W * 0.2, H * 0.42)], zone=2)
    elif style == "balloon":                                        # Luftballon an Schnur (Griff unten)
        c.line(smooth([(0, 0), (3, H * 0.25), (-2, H * 0.45), (0, H * 0.6)], closed=False), 0.4, zone=3, shade=0.7)
        b = ell(0, H * 0.8, W * 0.5, H * 0.2, 32)
        shaded(c, b, 1, "right", SOFT, 0.3)
        c.fill(ell(-W * 0.18, H * 0.86, W * 0.1, H * 0.05, 12), zone=3, shade=1.4, alpha=0.7)
        c.fill([(-2, H * 0.6), (2, H * 0.6), (0, H * 0.62)], zone=1)
        c.line(b, INNER, zone=0, closed=True)
    elif style == "candy_apple":                                    # Liebesapfel am Stiel
        c.fill(rrect(-0.6, H * 0.4, 0.6, H, 0.3), zone=3)
        a = ell(0, H * 0.25, W * 0.5, H * 0.25, 24)
        shaded(c, a, 1, "right", SOFT, 0.3)
        c.fill(ell(-W * 0.18, H * 0.34, W * 0.12, H * 0.06, 12), zone=3, shade=1.3, alpha=0.8)
        c.line(a, INNER, zone=0, closed=True)
    elif style == "candy_stand":                                    # Zuckerwatte-Stand mit Wattebausch-Schild
        body = rrect(x0, 0, x1, H * 0.45, 1.2)
        shaded(c, body, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0 - 3, H * 0.43, x1 + 3, H * 0.47, 1), zone=3)
        c.fill(ell(0, H * 0.54, W * 0.14, H * 0.06, 24), zone=3, shade=0.9)
        for k in range(3):
            c.fill(ell(-W * 0.06 + k * W * 0.06, H * 0.6, W * 0.07, H * 0.05, 16), zone=2, shade=1.2)
        c.fill(rrect(x0 + 8, H * 0.47, x0 + 12, H * 0.85, 1), zone=3)
        c.fill(rrect(x1 - 12, H * 0.47, x1 - 8, H * 0.85, 1), zone=3)
        c.fill(smooth([(x0 - 6, H * 0.85, "s"), (0, H * 0.95), (x1 + 6, H * 0.85, "s")]), zone=2)
        c.fill(ell(0, H * 0.95, W * 0.12, H * 0.05, 20), zone=2, shade=1.3)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "gate":                                           # Eingangstor: Bogen mit Lichtern und Fahnen
        for sx in (-1, 1):
            p = rrect(sx * W / 2 - 20, 0, sx * W / 2 + 20, H * 0.82, 3)
            shaded(c, p, 1, "right", SHADE, 0.2)
            c.line(p, INNER, zone=0, closed=True)
            _flag_top(c, sx * W / 2, H * 0.94, 24)
        arch = smooth([(x0, H * 0.72), (0, H * 0.94), (x1, H * 0.72), (x1, H * 0.84), (0, H * 1.0), (x0, H * 0.84)])
        c.fill(arch, zone=2)
        _bulbs(c, [(x0 + (x1 - x0) * k / 24, H * (0.78 + 0.18 * math.sin(math.pi * k / 24))) for k in range(25)])
        c.fill(ell(0, H * 0.88, 40, 24, 32), zone=3)
        c.fill(ell(0, H * 0.88, 26, 14, 24), zone=1)
        c.line(arch, INNER, zone=0, closed=True)
    else:
        raise ValueError(style)
