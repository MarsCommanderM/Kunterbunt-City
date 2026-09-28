"""
Fest im Hintergrund – NUR Bauliches (Entscheidung 👤: Räume leer, nur Boden + Wände; Fenster, Türen, Teppiche
usw. sind Items, das Kind baut selbst): Dachschrägen und die Außen-Kulisse (Himmel, ferne Hügel und Bäume).
Fest eingefärbt („gebacken“), mit Tinten-Kontur wie Items.
"""
from __future__ import annotations

import math
import random

from items.kit import ell, rrect, smooth

from .base import INNER, WALL_H, Sheet, bake, canvas

def roof_slopes(sheet: Sheet, width: float, knee: float = 110.0):
    """Dachboden: schräge Decke links und rechts (Holzbretter parallel zur Schräge, zwei Sparren) – bleibt Wand."""
    cols = ["#d8b48a", "#c49a6c", "#8a5a3c"]
    for side in (-1, 1):
        x_edge = 0.0 if side < 0 else width
        x_in = width * 0.3 if side < 0 else width * 0.7
        c = canvas(min(x_edge, x_in) - 2, knee - 2, max(x_edge, x_in) + 2, WALL_H + 2)
        poly = [(x_edge, knee), (x_edge, WALL_H), (x_in, WALL_H)]
        c.fill(poly, zone=1)
        cl = c.mask(poly)
        n = 12
        for k in range(1, n):                            # Bretter parallel zur Schräge
            t = k / n
            a = (x_edge, knee + (WALL_H - knee) * t)
            b = (x_in + (x_edge - x_in) * t, WALL_H)
            c.line([a, b], INNER * 2.2, zone=3, shade=0.95, clip=cl)
            if k % 2:
                c.fill([a, b, (b[0] + (x_edge - x_in) / n, WALL_H), (x_edge, a[1] + (WALL_H - knee) / n)], zone=1,
                       shade=0.94, clip=cl)
        for t in (0.35, 0.72):                           # Sparren
            a = (x_edge, knee + (WALL_H - knee) * t)
            b = (x_in + (x_edge - x_in) * t, WALL_H)
            c.line([a, b], 5.0, zone=2, clip=cl)
            c.line([a, b], 1.0, zone=3, shade=0.8, clip=cl)
        c.line([(x_edge, knee), (x_in, WALL_H)], 4.0, zone=3)
        sheet.paste(bake(c, cols), min(x_edge, x_in) - 2, WALL_H + 2)


def outdoor(sheet: Sheet, width: float, seed: int = 5, edge: str = "none", top: float = WALL_H + 80):
    """Außen: Himmel (bis `top` cm, = Raumhöhe → weit rauszoomen ohne Rand), Wolken, ferne Hügel mit Bäumen.
    Zäune/Hecken sind Items (edge = "none")."""
    rng = random.Random(seed)
    sky = canvas(0, 0, width, top, outline=0)
    area = [(0, 0), (width, 0), (width, top), (0, top)]
    sky.fill(area, zone=1)
    for k in range(10):
        yy = top * (1 - k / 10)
        sky.fill([(0, 0), (width, 0), (width, yy), (0, yy)], zone=1, shade=1.0 + 0.01 * k, alpha=0.3)
    for _ in range(int(width / 110)):
        cx, cy = rng.uniform(0, width), rng.uniform(max(190.0, top * 0.4), top * 0.9)   # auch im Normal-Zoom sichtbar
        for dx, r in ((-14, 11), (0, 16), (15, 12), (6, 9)):
            sky.fill(ell(cx + dx, cy + (4 if r < 12 else 0), r * 1.4, r, 32), zone=2)
    far = [(-10, 0)] + [(width * k / 16, 70 + 30 * math.sin(k * 0.8 + seed)) for k in range(17)] + [(width + 10, 0)]
    sky.fill(smooth(far, closed=True), zone=3, shade=0.9)
    sheet.paste(bake(sky, ["#a8dcf2", "#ffffff", "#9ccf86"], outline=False), 0, top)
    trees = canvas(0, 0, width, 180)
    for _ in range(int(width / 70)):
        tx = rng.uniform(0, width)
        th = rng.uniform(70, 120)
        trees.fill(rrect(tx - 3, 30, tx + 3, 30 + th * 0.45, 1.5), zone=3)
        for dx, dy, r in ((0, th * 0.75, th * 0.28), (-th * 0.18, th * 0.6, th * 0.22), (th * 0.18, th * 0.6, th * 0.22)):
            trees.fill(ell(tx + dx, 30 + dy, r, r * 0.9, 28), zone=1, shade=rng.choice([0.9, 1.0]))
    sheet.paste(bake(trees, ["#6fb35f", "#ffffff", "#8a5a3c"]), 0, 180)


def sky(sheet: Sheet, width: float, top: float, seed: int = 5, strip: float = 600.0):
    """Nur Himmel + Wolken (für Stadt): bis `top` cm – in Streifen gezeichnet (ein 37-m-Himmel am Stück sprengt den Speicher)."""
    rng = random.Random(seed)
    clouds = [(rng.uniform(0, width), rng.uniform(max(420.0, top * 0.6), top * 0.95)) for _ in range(int(width / 150))]
    x0 = 0.0
    while x0 < width:
        x1 = min(width, x0 + strip)
        s = canvas(x0, 0, x1, top, outline=0)
        s.fill([(x0, 0), (x1, 0), (x1, top), (x0, top)], zone=1)
        for k in range(10):
            yy = top * (1 - k / 10)
            s.fill([(x0, 0), (x1, 0), (x1, yy), (x0, yy)], zone=1, shade=1.0 + 0.01 * k, alpha=0.3)
        for cx, cy in clouds:
            if x0 - 60 < cx < x1 + 60:
                for dx, r in ((-14, 11), (0, 16), (15, 12), (6, 9)):
                    s.fill(ell(cx + dx, cy + (4 if r < 12 else 0), r * 1.4, r, 32), zone=2)
        sheet.paste(bake(s, ["#a8dcf2", "#ffffff", "#9ccf86"], outline=False), x0, top)
        x0 = x1


HOUSE_COLS = [["#f6d98a", "#fbfaf7", "#c96a4a"], ["#a9c3dd", "#fbfaf7", "#6d6f78"], ["#f0b6c2", "#fbfaf7", "#8a5e3f"],
              ["#9fc3a0", "#fbfaf7", "#c96a4a"], ["#f5f3ee", "#e07a7a", "#6d6f78"], ["#f09a55", "#fbfaf7", "#8a5e3f"],
              ["#b9a6d6", "#fbfaf7", "#6d6f78"], ["#e8e2d8", "#48b0a0", "#c96a4a"], ["#f4c95d", "#fbfaf7", "#2e3140"]]


def town(sheet: Sheet, width: float, fronts: list, top: float, seed: int = 5):
    """Einkaufsstraße: Himmel, dahinter eine Reihe Häuser. `fronts` = [(x_mitte_cm, breite_cm)] je Laden:
    dort ein großes Schaufenster + Eingang (Tür, Markise, Schild sind Items). Zwischen den Läden schmale Häuser."""
    sky(sheet, width, top, seed)
    rng = random.Random(seed)
    spans = []
    x = 0.0
    for cx, w in sorted(fronts):
        if cx - w / 2 - x > 60:
            spans.append((x, cx - w / 2, False))
        spans.append((cx - w / 2, cx + w / 2, True))
        x = cx + w / 2
    if width - x > 20:
        spans.append((x, width, False))
    for i, (a, b, shop) in enumerate(spans):
        w = b - a
        h = rng.choice([520, 600, 680, 560]) if shop else rng.choice([460, 540, 620])
        h = min(h, top - 40)
        cols = HOUSE_COLS[(i * 5 + seed) % len(HOUSE_COLS)]
        c = canvas(a - 6, 0, b + 6, h + 60)
        g = canvas(a - 6, 0, b + 6, h + 60)                    # Glas + Eingangsnische (eigene Farben)
        body = [(a, 0), (b, 0), (b, h), (a, h)]
        c.fill(body, zone=1)
        c.fill([(b - w * 0.08, 0), (b, 0), (b, h), (b - w * 0.08, h)], zone=1, shade=0.9)
        c.line([(a, 0), (a, h)], INNER, zone=0)
        # Dach: Giebel oder Gesims
        if (i + seed) % 3 == 0 and w < 520:
            roof = [(a - 6, h), (b + 6, h), ((a + b) / 2, h + min(60, w * 0.3))]
            c.fill(roof, zone=3)
            c.line(roof, INNER, zone=0, closed=True)
        else:
            c.fill([(a - 6, h - 12), (b + 6, h - 12), (b + 6, h), (a - 6, h)], zone=2)
            c.line([(a - 6, h - 12), (b + 6, h - 12)], INNER, zone=0)
        # Obergeschosse: Fenster mit Rahmen, Sprosse, Blumenkasten
        floors = int((h - 300) // 120) + 1
        nwin = max(1, int(w // 110))
        for f in range(floors):
            y0 = 300 + f * 120
            if y0 + 90 > h - 14:
                break
            for k in range(nwin):
                wx = a + (k + 0.5) * w / nwin
                win = rrect(wx - 26, y0, wx + 26, y0 + 80, 3)
                c.fill(rrect(wx - 30, y0 - 4, wx + 30, y0 + 84, 3), zone=2)
                g.fill(win, zone=1, shade=1.0 if (k + f) % 2 else 0.94)
                g.line([(wx - 18, y0 + 72), (wx - 4, y0 + 56)], 2.0, zone=2)
                g.line([(wx, y0), (wx, y0 + 80)], 2.2, zone=2)
                g.line([(wx - 26, y0 + 50), (wx + 26, y0 + 50)], 2.2, zone=2)
                if (k + f + i) % 3 == 0:
                    c.fill(rrect(wx - 32, y0 - 10, wx + 32, y0 - 2, 2), zone=3, shade=0.8)
                    for p in range(6):
                        c.fill(ell(wx - 26 + p * 10.5, y0 - 1, 4, 4, 12), zone=2, shade=rng.choice([0.9, 1.0]))
        # Erdgeschoss
        if shop:
            win = rrect(a + 18, 24, b - 110, 220, 4)
            c.fill(rrect(a + 12, 18, b - 104, 226, 4), zone=2)
            g.fill(win, zone=1)
            for k in range(3):                                   # Spiegelung
                g.line([(a + 40 + k * 60, 200), (a + 90 + k * 60, 60)], 3.0, zone=2)
            g.fill(rrect(b - 96, 0, b - 14, 225, 3), zone=3)     # Eingangsnische (Tür ist ein Item)
            c.fill([(a, 0), (b, 0), (b, 16), (a, 16)], zone=3, shade=0.8)
        else:
            dw = min(60, w * 0.4)
            dx = (a + b) / 2
            door = rrect(dx - dw / 2, 0, dx + dw / 2, 210, 4)
            c.fill(door, zone=2, shade=0.8)
            c.fill(ell(dx + dw * 0.3, 105, 2.5, 2.5, 12), zone=3)
            c.line(door, INNER, zone=0, closed=True)
            for sx in (-1, 1):
                if w > 180:
                    win = rrect(dx + sx * (dw / 2 + 30) - 25, 90, dx + sx * (dw / 2 + 30) + 25, 180, 3)
                    g.fill(win, zone=1)
        sheet.paste(bake(c, cols), a - 6, h + 60)
        sheet.paste(bake(g, ["#cfe6f2", "#ffffff", "#5a4e4a"]), a - 6, h + 60)
    # Gehweg-Kante hinten (Hausfuß)
    k = canvas(0, 0, width, 6, outline=0)
    k.fill([(0, 0), (width, 0), (width, 6), (0, 6)], zone=1)
    sheet.paste(bake(k, ["#8a8780"], outline=False), 0, 6)
