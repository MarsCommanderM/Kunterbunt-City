"""
Bauteile als Items (P07, Wunsch 👤): Räume sind leer – Fenster, Türen, Vorhänge, Teppiche, Läufer, Fußmatten,
Poster, Heizkörper baut das Kind selbst. Wand-Items hängen an der Wand (placement "wall"), Teppiche liegen flach
unter allem (placement "rug").

Zonen – Fenster: 1 = Rahmen · 2 = Himmel · 3 = Hügel/Garten draußen
         Türen:  1 = Türblatt · 2 = Zarge/Glas · 3 = Griff/Beschläge
         Stoffe: 1 = Stoff · 2 = Muster · 3 = Stange/Rand/Fransen
"""
from __future__ import annotations

import math
import random

from .kit import INNER, SHADE, SOFT, Item, ell, line, rrect, shaded, smooth, trap


def _view(c, x0, y0, x1, y1, clip, seed=1):
    """Blick nach draußen (Himmel Zone 2, Wolken heller, Hügel Zone 3) – nur innerhalb clip."""
    rng = random.Random(seed)
    c.fill([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], zone=2, clip=clip)
    for k in range(6):
        yy = y0 + (y1 - y0) * k / 6
        c.fill([(x0, y0), (x1, y0), (x1, yy), (x0, yy)], zone=2, shade=1.02, alpha=0.3, clip=clip)
    for _ in range(max(1, int((x1 - x0) / 40))):
        cx, cy = rng.uniform(x0, x1), rng.uniform(y0 + (y1 - y0) * 0.55, y1 - 4)
        for dx, r in ((-5, 4), (0, 6), (6, 4.5)):
            c.fill(ell(cx + dx, cy, r * 1.3, r, 20), zone=2, shade=1.32, clip=clip)
    hill = [(x0 - 4, y0)] + [(x0 + (x1 - x0) * k / 10, y0 + (y1 - y0) * (0.22 + 0.08 * math.sin(k * 0.9 + seed)))
                             for k in range(11)] + [(x1 + 4, y0)]
    c.fill(smooth(hill), zone=3, clip=clip)
    for _ in range(max(1, int((x1 - x0) / 28))):
        tx = rng.uniform(x0, x1)
        ty = y0 + (y1 - y0) * rng.uniform(0.18, 0.3)
        c.fill(ell(tx, ty + 5, 4.2, 5.5, 16), zone=3, shade=0.8, clip=clip)
    for a, b in ((0.12, 0.3), (0.38, 0.45)):              # Spiegelung auf dem Glas
        xa, xb = x0 + (x1 - x0) * a, x0 + (x1 - x0) * b
        c.fill([(xa, y1), (xb, y1), (xb - (y1 - y0) * 0.45, y0), (xa - (y1 - y0) * 0.45, y0)], zone=2, shade=1.3,
               alpha=0.35, clip=clip)


# ------------------------------------------------------------------ Fenster
def window(it: Item, style: str = "double"):
    """Reihenfolge: Rahmen-Fläche → Aussicht in die Scheiben (übermalt den Rahmen dort) → Sprossen/Griffe → Linien."""
    c, W, H = it.c, it.w, it.h
    fw = max(3.0, min(W, H) * 0.06)                        # Rahmenbreite
    sill = style not in ("round", "porthole")
    y0 = 5.0 if sill else 0.0
    x0, x1 = (-W / 2 + 6, W / 2 - 6) if sill else (-W / 2, W / 2)
    if style in ("round", "porthole"):
        r = min(W, H) / 2
        c.fill(ell(0, r, r, r, 64), zone=1)
        glass = ell(0, r, r - fw, r - fw, 64)
        _view(c, -r, 0, r, 2 * r, c.mask(glass))
        if style == "round":
            c.line([(-r + fw, r), (r - fw, r)], fw * 0.5, zone=1)
            c.line([(0, fw), (0, 2 * r - fw)], fw * 0.5, zone=1)
        else:
            for k in range(8):
                a = 2 * math.pi * k / 8
                c.ellipse((r - fw / 2) * math.cos(a), r + (r - fw / 2) * math.sin(a), fw * 0.18, fw * 0.18, zone=1, shade=0.7)
        c.line(glass, INNER, zone=0, closed=True)
        return
    if style == "arch":
        rr = (x1 - x0) / 2
        outer = [(x0, y0), (x1, y0)] + [(rr * math.cos(math.radians(a)), H - rr + rr * math.sin(math.radians(a)))
                                         for a in range(0, 181, 8)]
        glass = [(x0 + fw, y0 + fw), (x1 - fw, y0 + fw)] + [((rr - fw) * math.cos(math.radians(a)),
                                                            H - rr + (rr - fw) * math.sin(math.radians(a))) for a in range(0, 181, 8)]
        c.fill(outer, zone=1)
        _view(c, x0, y0, x1, H, c.mask(glass))
        gcl = c.mask(glass)
        c.line([(0, y0 + fw), (0, H - fw)], fw * 0.55, zone=1, clip=gcl)
        c.line([(x0 + fw, y0 + (H - y0) * 0.45), (x1 - fw, y0 + (H - y0) * 0.45)], fw * 0.55, zone=1, clip=gcl)
        c.line(glass, INNER, zone=0, closed=True)
    elif style == "gable":                                  # Giebelfenster (spitz)
        outer = [(x0, y0), (x1, y0), (x1, H * 0.62), (0, H), (x0, H * 0.62)]
        glass = [(x0 + fw, y0 + fw), (x1 - fw, y0 + fw), (x1 - fw, H * 0.62 - fw * 0.3), (0, H - fw * 1.6),
                 (x0 + fw, H * 0.62 - fw * 0.3)]
        c.fill(outer, zone=1)
        _view(c, x0, y0, x1, H, c.mask(glass))
        c.line([(0, y0 + fw), (0, H - fw)], fw * 0.5, zone=1, clip=c.mask(glass))
        c.line(glass, INNER, zone=0, closed=True)
    elif style == "stained":                                # Buntglas: bunte Rauten
        c.fill(rrect(x0, y0, x1, H, 1.5), zone=1)
        gl = rrect(x0 + fw, y0 + fw, x1 - fw, H - fw, 1)
        cl = c.mask(gl)
        c.fill(gl, zone=2, clip=cl)
        s = (x1 - x0) / 5
        for i in range(-2, 8):
            for j in range(0, int(H / s) + 3):
                cx, cy = x0 + i * s + (s / 2 if j % 2 else 0), y0 + j * s * 0.7
                d = [(cx, cy - s * 0.35), (cx + s * 0.5, cy), (cx, cy + s * 0.35), (cx - s * 0.5, cy)]
                c.fill(d, zone=3 if (i + j) % 3 == 0 else 2, shade=1.0 if (i + j) % 2 else 1.25, clip=cl)
                c.line(d, INNER * 1.3, zone=0, closed=True, clip=cl)
        c.line(gl, INNER, zone=0, closed=True)
    else:
        panes = {"single": 1, "small": 1, "basement": 2, "double": 2, "floor": 1, "triple": 3, "shop": 3, "tilt": 1}.get(style, 2)
        outer = rrect(x0, y0, x1, H, 1.5)
        c.fill(outer, zone=1)
        pw = (x1 - x0 - fw * (panes + 1)) / panes
        for k in range(panes):
            px = x0 + fw + k * (pw + fw)
            hole = rrect(px, y0 + fw, px + pw, H - fw, 0.8)
            hcl = c.mask(hole)
            _view(c, x0, y0, x1, H, hcl, seed=k + 1)
            if style not in ("small", "basement", "shop", "floor"):
                c.line([(px, y0 + (H - y0) * 0.58), (px + pw, y0 + (H - y0) * 0.58)], fw * 0.45, zone=1, clip=hcl)
            if style == "basement":
                for bx in range(1, 4):
                    c.line([(px + pw * bx / 4, y0 + fw), (px + pw * bx / 4, H - fw)], fw * 0.3, zone=1, shade=0.7, clip=hcl)
            if style != "shop":
                c.fill(rrect(px + pw - fw * 0.9, y0 + (H - y0) * 0.44, px + pw - fw * 0.35, y0 + (H - y0) * 0.56, 0.4),
                       zone=1, shade=0.7)
            c.line(hole, INNER, zone=0, closed=True)
        if style == "tilt":                                  # Kippfenster offen: schräger Flügel
            c.fill([(x0 + fw, H - fw), (x1 - fw, H - fw), (x1 - fw * 0.2, H - fw * 3), (x0 + fw * 0.2, H - fw * 3)], zone=1,
                   shade=0.85)
    if sill:
        c.fill(rrect(-W / 2, 0, W / 2, 5.5, 1.2), zone=1, shade=0.93)
        c.fill(rrect(-W / 2, 0, W / 2, 2.2, 1.0), zone=1, shade=0.8)
        c.line(rrect(-W / 2, 0, W / 2, 5.5, 1.2), INNER, zone=0, closed=True)


# ------------------------------------------------------------------ Türen (Deko an der Wand, bis zum Boden)
def _frosted(c, pts):
    """Milchglas (Zone 2 der Tür = Zarge, leicht abgedunkelt) mit zwei hellen Glanzstreifen."""
    cl = c.mask(pts)
    c.fill(pts, zone=2, shade=0.9, clip=cl)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for a, b in ((0.15, 0.32), (0.42, 0.5)):
        xa, xb = x0 + (x1 - x0) * a, x0 + (x1 - x0) * b
        c.fill([(xa, y1), (xb, y1), (xb - (y1 - y0) * 0.4, y0), (xa - (y1 - y0) * 0.4, y0)], zone=2, shade=1.08, alpha=0.8, clip=cl)
    c.line(pts, INNER, zone=0, closed=True)


def door(it: Item, style: str = "wood"):
    c, W, H = it.c, it.w, it.h
    tw = 6.0
    c.fill(rrect(-W / 2, 0, W / 2, H, 1.2), zone=2)                        # Zarge
    c.line(rrect(-W / 2, 0, W / 2, H, 1.2), INNER, zone=0, closed=True)
    x0, x1, y1 = -W / 2 + tw, W / 2 - tw, H - tw
    if style == "arch":
        rr = (x1 - x0) / 2
        leaf = [(x0, 0), (x1, 0)] + [(rr * math.cos(math.radians(a)), y1 - rr + rr * math.sin(math.radians(a))) for a in range(0, 181, 8)]
    else:
        leaf = rrect(x0, 0, x1, y1, 1.0)
    cl = shaded(c, leaf, 1, "right", SHADE, 0.12)
    if style in ("wood", "arch"):
        for yy0, yy1 in ((y1 * 0.08, y1 * 0.45), (y1 * 0.52, y1 * 0.9)):
            p = rrect(x0 + (x1 - x0) * 0.16, yy0, x1 - (x1 - x0) * 0.16, yy1, 1.5)
            c.fill(p, zone=1, shade=0.92, clip=cl)
            c.line(p, INNER, zone=0, closed=True, clip=cl)
    elif style == "glass":
        _frosted(c, rrect(x0 + (x1 - x0) * 0.14, y1 * 0.45, x1 - (x1 - x0) * 0.14, y1 * 0.92, 1.5))
        p = rrect(x0 + (x1 - x0) * 0.16, y1 * 0.08, x1 - (x1 - x0) * 0.16, y1 * 0.36, 1.5)
        c.fill(p, zone=1, shade=0.92, clip=cl)
        c.line(p, INNER, zone=0, closed=True)
    elif style == "barn":
        for k in range(1, 5):
            xx = x0 + (x1 - x0) * k / 5
            line(c, [(xx, 2), (xx, y1 - 2)], zone=1, clip=cl, shade=0.7)
        c.line([(x0 + 4, y1 * 0.15), (x1 - 4, y1 * 0.85)], 4, zone=1, shade=0.85)
        c.line([(x0 + 4, y1 * 0.85), (x1 - 4, y1 * 0.15)], 4, zone=1, shade=0.85)
        c.fill(rrect(-W / 2 - 4, H - 2, W / 2 + 4, H + 3, 1), zone=3)       # Laufschiene
    elif style == "double":
        c.line([(0, 0), (0, y1)], INNER * 2, zone=0)
        for sx in (-1, 1):
            g = rrect(sx * (x1 - x0) * 0.08 if sx > 0 else x0 + (x1 - x0) * 0.06, y1 * 0.2,
                      x1 - (x1 - x0) * 0.06 if sx > 0 else -(x1 - x0) * 0.08, y1 * 0.92, 1.2)
            _frosted(c, g)
    elif style == "garage":
        n = 7
        for k in range(n):
            y = y1 * k / n
            c.fill([(x0, y), (x1, y), (x1, y + 3), (x0, y + 3)], zone=1, shade=1.08, clip=cl)
            line(c, [(x0, y + y1 / n), (x1, y + y1 / n)], zone=1, clip=cl, shade=0.62)
        c.fill(rrect(-14, y1 * 0.2, 14, y1 * 0.2 + 5, 2), zone=3)
        return
    kx = x1 - (x1 - x0) * 0.16 if style != "double" else -(x1 - x0) * 0.08
    c.fill(rrect(kx - 1.5, y1 * 0.44, kx + 1.5, y1 * 0.56, 1), zone=3)
    c.fill(rrect(kx - 4.5, y1 * 0.49, kx + 1.5, y1 * 0.52, 0.8), zone=3, shade=1.1)
    if style == "double":
        c.fill(rrect(-kx - 1.5, y1 * 0.44, -kx + 1.5, y1 * 0.56, 1), zone=3)


# ------------------------------------------------------------------ Vorhänge & Rollos
def curtain(it: Item, style: str = "long", pattern: str = "plain"):
    c, W, H = it.c, it.w, it.h
    rod_y = H - 3
    if style == "blind":
        body = rrect(-W / 2 + 3, H * 0.25, W / 2 - 3, H - 6, 1)
        cl = shaded(c, body, 1, "bottom", SOFT, 0.2)
        _pattern(c, pattern, -W / 2, H * 0.25, W / 2, H - 6, cl)
        c.fill(rrect(-W / 2, H - 8, W / 2, H, 3), zone=3)
        c.fill(rrect(-W / 2 + 2, H * 0.25 - 3, W / 2 - 2, H * 0.25 + 1, 1.2), zone=3, shade=0.9)
        c.line([(W * 0.3, H * 0.25), (W * 0.3, H * 0.08)], 0.5, zone=3)
        c.ellipse(W * 0.3, H * 0.07, 1.4, 1.8, zone=3)
        return
    c.fill(rrect(-W / 2, rod_y - 1.2, W / 2, rod_y + 1.2, 1.2), zone=3)     # Stange
    for sx in (-1, 1):
        c.ellipse(sx * W / 2, rod_y, 2.4, 2.4, zone=3, shade=0.9)
    alpha = 0.72 if style == "sheer" else 1.0
    bottom = 0.0 if style in ("long", "sheer") else H * 0.1
    for sx in (-1, 1):
        inner_x = sx * W * (0.16 if style in ("long", "sheer") else 0.02)
        outer_x = sx * W / 2
        tie_y = H * 0.42
        pts = smooth([(outer_x, rod_y), (inner_x, rod_y, "s"), (inner_x + sx * W * 0.06, tie_y + 10),
                      (outer_x - sx * W * 0.12, tie_y), (outer_x - sx * W * 0.05, bottom + 12), (outer_x - sx * W * 0.06, bottom, "s"),
                      (outer_x + sx * 1, bottom, "s")]) if style in ("long", "sheer") else \
            smooth([(outer_x, rod_y, "s"), (inner_x, rod_y, "s"), (inner_x, bottom + 3), (outer_x, bottom, "s")])
        c.fill(pts, zone=1, alpha=alpha)
        cl = c.mask(pts)
        for k in range(1, 5):                                  # Falten
            fx = outer_x + (inner_x - outer_x) * k / 5
            c.line([(fx, rod_y - 2), (fx + sx * 2, bottom + 4)], 1.8, zone=1, shade=0.86, clip=cl)
        _pattern(c, pattern, min(outer_x, inner_x) - 10, bottom, max(outer_x, inner_x) + 10, rod_y, cl)
        c.line(pts, INNER, zone=0, closed=True)
        if style in ("long", "sheer"):
            c.fill(rrect(outer_x - sx * W * 0.16 - 3, H * 0.4, outer_x - sx * W * 0.08 + 3, H * 0.45, 1.5), zone=2)


def _pattern(c, pattern, x0, y0, x1, y1, clip):
    if pattern == "dots":
        for i in range(int((x1 - x0) / 9) + 1):
            for j in range(int((y1 - y0) / 9) + 1):
                c.ellipse(x0 + i * 9 + (4.5 if j % 2 else 0), y0 + j * 9, 1.6, 1.6, zone=2, clip=clip)
    elif pattern == "stripes":
        for i in range(int((x1 - x0) / 10) + 1):
            xx = x0 + i * 10
            c.fill([(xx, y0), (xx + 4, y0), (xx + 4, y1), (xx, y1)], zone=2, clip=clip)
    elif pattern == "stars":
        for i in range(int((x1 - x0) / 14) + 1):
            for j in range(int((y1 - y0) / 14) + 1):
                cx, cy = x0 + i * 14 + (7 if j % 2 else 0), y0 + j * 14
                c.fill([(cx + 3 * math.cos(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.45),
                         cy + 3 * math.sin(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.45)) for k in range(10)],
                       zone=2, clip=clip)


# ------------------------------------------------------------------ Teppiche, Läufer, Matten (flach auf dem Boden)
def _flat(W, H, taper=0.07, r=2.0):
    """Flache Fläche von leicht schräg oben: hintere Kante etwas schmaler (Perspektive wie das Bodenband)."""
    t = W * taper / 2
    return smooth([(-W / 2, 1.5, "s"), (W / 2, 1.5, "s"), (W / 2 - t, H, "s"), (-W / 2 + t, H, "s")], n=2)


def rug(it: Item, style: str = "rect"):
    c, W, H = it.c, it.w, it.h
    rng = random.Random(len(style))
    if style == "round":
        edge = ell(0, H / 2, W / 2, H / 2 - 0.4, 64)
        c.fill(ell(0, H / 2 - 1.2, W / 2, H / 2 - 0.4, 64), zone=1, shade=0.78)
        c.fill(edge, zone=1)
        cl = c.mask(edge)
        for k, f in enumerate((0.78, 0.55, 0.3)):
            c.line(ell(0, H / 2, W / 2 * f, H / 2 * f, 48), max(1.2, W * 0.02), zone=2 if k % 2 == 0 else 3, closed=True, clip=cl)
        c.line(edge, INNER, zone=0, closed=True)
        return
    if style == "flower":
        pet = []
        for k in range(8):
            a = 2 * math.pi * k / 8
            pet.append(ell(W * 0.3 * math.cos(a), H / 2 + H * 0.3 * math.sin(a), W * 0.19, H * 0.19, 32))
        for p in pet:
            c.fill(p, zone=1)
            c.line(p, INNER, zone=0, closed=True)
        c.fill(ell(0, H / 2, W * 0.2, H * 0.2, 40), zone=2)
        c.line(ell(0, H / 2, W * 0.2, H * 0.2, 40), INNER, zone=0, closed=True)
        return
    if style == "sheepskin":
        pts = [((W / 2) * (0.9 + 0.1 * rng.random()) * math.cos(2 * math.pi * k / 18),
                H / 2 + (H / 2) * (0.85 + 0.15 * rng.random()) * math.sin(2 * math.pi * k / 18)) for k in range(18)]
        body = smooth(pts)
        c.fill(body, zone=1)
        cl = c.mask(body)
        for _ in range(int(W / 3)):
            x, y = rng.uniform(-W / 2, W / 2), rng.uniform(0, H)
            c.line(smooth([(x, y), (x + 2, y + 1.5), (x + 3.5, y)], closed=False), 0.4, zone=1, shade=0.86, clip=cl)
        c.line(body, INNER, zone=0, closed=True)
        return
    body = _flat(W, H, 0.07 if W > 60 else 0.05, 2.0)
    c.fill(_flat(W, H - 0.3, 0.07, 2.0), zone=1, shade=0.72)          # Kante vorn (Dicke)
    top = [(x, y + 1.2) for x, y in body]
    c.fill(top, zone=1)
    cl = c.mask(top)
    if style in ("rect", "runner"):
        b = max(2.0, min(W, H) * 0.12)
        inner = _flat(W - 2 * b, H - 2 * b * 0.6, 0.07)
        inner = [(x, y + 1.2 + b * 0.6) for x, y in inner]
        c.fill(inner, zone=3, clip=cl)
        c.line(inner, INNER, zone=0, closed=True, clip=cl)
        inner2 = [(x * 0.9, 1.2 + b * 0.6 + (y - 1.2 - b * 0.6) * 0.8 + (H - 2 * b * 0.6) * 0.1) for x, y in inner]
        c.fill(inner2, zone=1, clip=cl)
        n = max(3, int(W / 30))
        for k in range(n):                                     # Rauten-Muster
            cx = -W / 2 + b + (W - 2 * b) * (k + 0.5) / n
            cy = H / 2 + 1
            d = [(cx, cy - H * 0.16), (cx + W * 0.05, cy), (cx, cy + H * 0.16), (cx - W * 0.05, cy)]
            c.fill(d, zone=2, clip=cl)
        for sx in (-1, 1):                                     # Fransen
            for k in range(int(H / 2.2)):
                y = 2 + k * 2.2
                c.line([(sx * (W / 2 - W * 0.035 * y / H), y), (sx * (W / 2 - W * 0.035 * y / H + 3), y - 0.3)], 0.45, zone=3)
    elif style == "doormat":
        for k in range(int(W / 2.4)):
            x = -W / 2 + k * 2.4
            line(c, [(x, 1.5), (x + 0.6, H)], zone=1, clip=cl, shade=0.8)
        heart = smooth([(0, H * 0.25, "s"), (W * 0.1, H * 0.6), (W * 0.06, H * 0.82), (0, H * 0.66, "s"), (-W * 0.06, H * 0.82),
                        (-W * 0.1, H * 0.6)])
        c.fill(heart, zone=2, clip=cl)
        c.line([(x, y + 1.2) for x, y in _flat(W - 6, H - 5, 0.05)], 1.2, zone=3, closed=True, clip=cl)
    elif style == "bathmat":
        for k in range(int(W / 4)):
            x = -W / 2 + 2 + k * 4
            c.ellipse(x, H / 2, 1.6, H * 0.36, zone=1, shade=1.06, clip=cl)
        c.line([(x, y + 1.2) for x, y in _flat(W - 4, H - 3, 0.05)], 0.8, zone=2, closed=True, clip=cl)
    elif style == "roads":                                     # Spielteppich mit Straßen
        c.fill(top, zone=1, clip=cl)
        for yy in (H * 0.35,):
            c.fill([(-W / 2, yy - H * 0.1), (W / 2, yy - H * 0.1), (W / 2, yy + H * 0.1), (-W / 2, yy + H * 0.1)], zone=2, clip=cl)
            for k in range(int(W / 14)):
                x = -W / 2 + k * 14
                c.fill([(x, yy - 0.5), (x + 7, yy - 0.5), (x + 7, yy + 0.5), (x, yy + 0.5)], zone=3, clip=cl)
        for xx in (-W * 0.2, W * 0.25):
            c.fill([(xx - W * 0.04, 0), (xx + W * 0.04, 0), (xx + W * 0.04 - W * 0.01, H), (xx - W * 0.04 - W * 0.01, H)], zone=2,
                   clip=cl)
        for (hx, hy, hc) in ((-W * 0.38, H * 0.7, 3), (W * 0.05, H * 0.72, 3), (W * 0.4, H * 0.12, 3)):
            c.fill(rrect(hx - 5, hy - 3, hx + 5, hy + 4, 1), zone=hc, shade=0.85, clip=cl)
            c.fill([(hx - 6, hy + 4), (hx + 6, hy + 4), (hx, hy + 8)], zone=2, shade=0.7, clip=cl)
        for (tx, ty) in ((W * 0.36, H * 0.72), (-W * 0.05, H * 0.1), (-W * 0.4, H * 0.12)):
            c.ellipse(tx, ty, 3.5, 2.6, zone=1, shade=0.72, clip=cl)
    c.line(top, INNER, zone=0, closed=True)


# ------------------------------------------------------------------ Wand-Deko & Heizkörper
def poster(it: Item, motif: str = "rocket"):
    c, W, H = it.c, it.w, it.h
    frame = rrect(-W / 2, 0, W / 2, H, 1)
    c.fill(frame, zone=3)
    pic = rrect(-W / 2 + 2, 2, W / 2 - 2, H - 2, 0.6)
    cl = c.mask(pic)
    c.fill(pic, zone=1, clip=cl)
    if motif == "rocket":
        body = smooth([(0, H * 0.9), (W * 0.14, H * 0.6), (W * 0.12, H * 0.25, "s"), (-W * 0.12, H * 0.25, "s"), (-W * 0.14, H * 0.6)])
        c.fill(body, zone=2, clip=cl)
        c.line(body, INNER, zone=0, closed=True, clip=cl)
        c.ellipse(0, H * 0.6, W * 0.06, W * 0.06, zone=3, clip=cl)
        c.fill([(-W * 0.06, H * 0.25), (W * 0.06, H * 0.25), (0, H * 0.1)], zone=3, clip=cl)
        for sx in (-1, 1):
            c.fill([(sx * W * 0.12, H * 0.25), (sx * W * 0.24, H * 0.18), (sx * W * 0.13, H * 0.45)], zone=3, clip=cl)
    elif motif == "rainbow":
        for k, z in enumerate((2, 3, 2)):
            r = W * (0.4 - k * 0.09)
            c.fill(ell(0, H * 0.3, r, r, 48), zone=z, shade=1.0 - k * 0.08, clip=cl)
        c.fill(ell(0, H * 0.3, W * 0.13, W * 0.13, 32), zone=1, clip=cl)
        c.fill([(-W, 0), (W, 0), (W, H * 0.3), (-W, H * 0.3)], zone=1, clip=cl)
    elif motif == "dino":
        body = smooth([(-W * 0.3, H * 0.2), (-W * 0.35, H * 0.45), (-W * 0.1, H * 0.55), (W * 0.1, H * 0.75), (W * 0.3, H * 0.78),
                       (W * 0.32, H * 0.66), (W * 0.15, H * 0.6), (W * 0.15, H * 0.2)])
        c.fill(body, zone=2, clip=cl)
        c.line(body, INNER, zone=0, closed=True, clip=cl)
        c.ellipse(W * 0.24, H * 0.72, 0.8, 0.8, zone=0, clip=cl)
    elif motif == "sun":
        c.fill(ell(0, H * 0.55, W * 0.2, W * 0.2, 40), zone=2, clip=cl)
        for k in range(10):
            a = 2 * math.pi * k / 10
            c.line([(W * 0.26 * math.cos(a), H * 0.55 + W * 0.26 * math.sin(a)),
                    (W * 0.36 * math.cos(a), H * 0.55 + W * 0.36 * math.sin(a))], 1.4, zone=2, clip=cl)
        c.fill([(-W, 0), (W, 0), (W, H * 0.2), (-W, H * 0.2)], zone=3, clip=cl)
    c.line(pic, INNER, zone=0, closed=True)


def radiator(it: Item):
    c, W, H = it.c, it.w, it.h
    for sx in (-1, 1):
        c.fill(rrect(sx * W * 0.42 - 1.5, 0, sx * W * 0.42 + 1.5, 10, 0.8), zone=2)
    n = max(4, int(W / 8))
    for k in range(n):
        x = -W / 2 + (k + 0.5) * W / n
        fin = rrect(x - W / n * 0.42, 8, x + W / n * 0.42, H, W / n * 0.4)
        shaded(c, fin, 1, "right", SHADE, 0.3)
    c.fill(rrect(-W / 2, H * 0.62, W / 2, H * 0.7, 1), zone=1, shade=0.9)
    c.fill(rrect(W / 2 - 2, H * 0.72, W / 2 + 3, H * 0.9, 1.2), zone=3)


def sconce(it: Item, state: str = ""):
    c, W, H = it.c, it.w, it.h
    c.fill(rrect(-W * 0.16, H * 0.1, W * 0.16, H * 0.45, 1), zone=3)
    c.line(smooth([(0, H * 0.3), (W * 0.25, H * 0.45), (W * 0.1, H * 0.6)], closed=False), 1.2, zone=3)
    shade = trap(-W / 2, W / 2, H * 0.55, -W * 0.3, W * 0.3, H, 1)
    if state == "on":
        c.glass(smooth([(-W * 0.45, H * 0.55, "s"), (W * 0.45, H * 0.55, "s"), (W * 0.8, 0, "s"), (-W * 0.8, 0, "s")], n=2),
                zone=2, opacity=0.35)
    shaded(c, shade, 1, "right", 0.98 if state == "on" else SHADE, 0.25)
