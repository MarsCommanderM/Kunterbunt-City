"""
Frisuren (vorne + hinten) im Stil „großer Kopf“ – Phase 04b.

Aufbau jeder Frisur:
  • Vorderteil (über dem Gesicht): Haarkappe − Gesichtsfenster (Haaransatz) + Seitensträhnen,
    Strähnen-Linien in dunklerer Haarfarbe, Naht-Linie (gestrichelt) in Zone 2 = hellere Haarfarbe.
  • Hinterteil (hinter dem Kopf): Volumen, lange Haare, Zöpfe, Dutts.
Zonen: 1 = Haarfarbe · 2 = Glanz/Naht (automatisch heller) · 3 = Haargummi/Spange.
Anker beider Teile = (0, hair_top) – so sitzt jede Frisur auf jeder Schablone.
"""
from __future__ import annotations

import math

from .body import DEEP, head_box
from .vec import ZCanvas, blob, path


def _geo(t: dict):
    hd = t["head"]
    return hd["w"] / 2, hd["h"] / 2, hd["cy"], t["hair_top"]


def _cap(t: dict, grow: float = 1.6, low: float = 0.25) -> list:
    """Haarkappe über dem Kopf: reicht an den Seiten bis low·H über der Kopfmitte hinab."""
    R, H, cy, top = _geo(t)
    ry = top - cy + 0.2
    pts = []
    for i in range(97):
        a = math.pi * (1 + low * 0.35) - math.pi * (1 + low * 0.7) * i / 96
        pts.append((math.cos(a) * (R + grow), cy + math.sin(a) * ry))
    return pts


def _window(t: dict, kind: str, brow: float) -> list:
    """Gesichtsfenster unter dem Haaransatz. kind: part (Mittelscheitel), side (Seitenscheitel), fringe (Pony),
    round (runder Ansatz). brow = Höhe des Ansatzes über der Kopfmitte (Anteil von H)."""
    R, H, cy, top = _geo(t)
    yb = cy + H * brow
    side = R * 0.84
    low = cy - H * 1.6
    if kind == "part":
        return path((-side, low), ((-side, cy - H * 0.05),), ((-side * 0.95, yb - H * 0.05), (-R * 0.3, yb + H * 0.02), (0, yb + H * 0.16)),
                    ((R * 0.3, yb + H * 0.02), (side * 0.95, yb - H * 0.05), (side, cy - H * 0.05)), ((side, low),))
    if kind == "side":
        px = -R * 0.3
        return path((-side, low), ((-side, cy - H * 0.05),), ((-side, yb - H * 0.1), (px - R * 0.3, yb + H * 0.12), (px, yb + H * 0.14)),
                    ((px + R * 0.6, yb + H * 0.02), (side, yb - H * 0.2), (side, cy - H * 0.1)), ((side, low),))
    if kind == "fringe":
        pts = [(-side, low), (-side, yb - H * 0.12)]
        n = 5
        for k in range(n):
            x0 = -side + 2 * side * k / n
            x1 = -side + 2 * side * (k + 1) / n
            pts += [(x0, yb - H * 0.03), ((x0 + x1) / 2, yb - H * 0.1), (x1, yb - H * 0.03)]
        return pts + [(side, yb - H * 0.12), (side, low)]
    # round
    return path((-side, low), ((-side, cy),), ((-side, yb), (-R * 0.4, yb + H * 0.1), (0, yb + H * 0.1)),
                ((R * 0.4, yb + H * 0.1), (side, yb), (side, cy)), ((side, low),))


def _side_locks(c: ZCanvas, t: dict, down: float, width: float = 0.3, flare: float = 1.0):
    """Seitliche Haarsträhnen neben dem Gesicht bis down·H unter die Kopfmitte."""
    R, H, cy, top = _geo(t)
    for sx in (-1, 1):
        o = sx * (R + 2.0 * flare)
        i = sx * R * (1 - width)
        lock = path((i, cy + H * 0.45), ((o, cy + H * 0.5), (o + sx * 0.8, cy - H * 0.2), (o, cy - H * down)),
                    ((o - sx * R * 0.12, cy - H * (down + 0.08)), (i, cy - H * (down - 0.05)), (i + sx * R * 0.06, cy - H * (down * 0.5))),
                    ((i, cy), (i - sx * 0.5, cy + H * 0.3), (i, cy + H * 0.45)))
        c.fill(lock, zone=1)


def _stitch(c: ZCanvas, t: dict, inset: float, from_a: float, to_a: float, clip):
    """Naht-Linie (gestrichelt, Zone 2) parallel zum Haar-Außenrand."""
    R, H, cy, top = _geo(t)
    ry = top - cy - inset
    rx = R + 1.2 - inset
    pts = [(math.cos(math.radians(a)) * rx, cy + math.sin(math.radians(a)) * ry)
           for a in [from_a + (to_a - from_a) * k / 40 for k in range(41)]]
    c.dashed(pts, 0.55, 1.6, zone=2, clip=clip)


def _strands(c: ZCanvas, t: dict, xs: list, y0: float, y1: float, clip):
    R, H, cy, top = _geo(t)
    for x in xs:
        c.line([(x * R * 0.55, cy + H * y0), (x * R * 0.9, cy + H * (y0 + y1) / 2), (x * R * 0.95, cy + H * y1)],
               0.5, zone=1, shade=DEEP, clip=clip)


HAIR_STYLES = ["short", "spiky", "side_part", "curly", "afro", "bob", "long", "pigtails", "ponytail", "bun",
               "space_buns", "braids", "wavy", "pixie", "buzz", "bald"]

# Stil → (Fenster, Ansatz-Höhe, Seitensträhnen bis …·H oder 0)
FRONT = {
    "short": ("fringe", 0.42, 0.0), "spiky": ("fringe", 0.46, 0.0), "side_part": ("side", 0.4, 0.0),
    "pixie": ("side", 0.34, 0.15), "buzz": ("round", 0.55, 0.0), "bob": ("fringe", 0.3, 0.55),
    "long": ("part", 0.42, 0.9), "wavy": ("part", 0.42, 0.9), "braids": ("part", 0.45, 0.3),
    "pigtails": ("fringe", 0.36, 0.2), "ponytail": ("part", 0.48, 0.0), "bun": ("part", 0.5, 0.0),
    "space_buns": ("part", 0.46, 0.0), "curly": ("round", 0.42, 0.0), "afro": ("round", 0.42, 0.0),
}


def draw_hair_front(t: dict, style: str, ppc: float):
    R, H, cy, top = _geo(t)
    c = ZCanvas(head_box(t, 16), ppc)
    if style == "bald":
        c.ellipse(0, cy, 0.01, 0.01, zone=1)
        return c.render_part((0, top))
    kind, brow, locks = FRONT[style]
    if style in ("curly", "afro"):
        k = 1.0 if style == "curly" else 1.12
        rr = R * (0.26 if style == "curly" else 0.3)
        for i in range(11):
            a = math.pi * (-0.02 + 1.04 * i / 10)
            c.ellipse(math.cos(a) * R * 0.95 * k, cy + H * 0.12 + math.sin(a) * (top - cy - H * 0.12) * 0.98, rr, rr * 0.95, zone=1)
        c.fill(_cap(t, 1.6 * k, 0.1), zone=1)
    elif style == "buzz":
        c.fill(_cap(t, 0.4, 0.05), zone=1)
    else:
        c.fill(_cap(t, 1.6 if style not in ("bob", "wavy") else 2.4, 0.3), zone=1)
    if style == "spiky":
        for k in range(6):
            x = -R * 0.75 + R * 1.5 * k / 5
            c.fill([(x - R * 0.2, top - 4), (x + R * 0.06, top + 3.5), (x + R * 0.2, top - 4)], zone=1)
    if locks:
        _side_locks(c, t, locks, 0.26 if style != "bob" else 0.2, 1.4 if style in ("bob", "wavy") else 1.0)
    clip = c.mask(_cap(t, 3.0, 1.2))
    if style in ("curly", "afro"):
        for i in range(6):
            x = -R * 0.62 + R * 1.24 * i / 5
            c.line([(x - R * 0.09, cy + H * 0.5), (x, cy + H * 0.44), (x + R * 0.09, cy + H * 0.5)], 0.5, zone=1, shade=DEEP)
    elif style != "buzz":
        if kind == "part":
            c.line([(0, cy + H * (brow + 0.16)), (0.3, top - 0.5)], 0.55, zone=1, shade=DEEP)
            _strands(c, t, [-0.55, 0.55], 0.62, 0.15, clip)
        elif kind == "side":
            c.line([(-R * 0.3, cy + H * (brow + 0.14)), (-R * 0.2, top - 0.5)], 0.55, zone=1, shade=DEEP)
            _strands(c, t, [0.5], 0.65, 0.2, clip)
        else:
            _strands(c, t, [-0.3, 0.3], 0.7, 0.5, clip)
        _stitch(c, t, 3.2, 160, 20, c.mask(_cap(t, 3.0, 1.2)))
    c.erase(_window(t, kind, brow))
    if style in ("pigtails",):
        for sx in (-1, 1):
            c.ellipse(sx * R * 0.97, cy + H * 0.36, R * 0.09, R * 0.12, zone=3)
    c.outline_under()
    return c.render_part((0, top))


def draw_hair_back(t: dict, style: str, ppc: float):
    R, H, cy, top = _geo(t)
    c = ZCanvas((-R * 2.4, cy - H * 3.2, R * 2.4, top + 22), ppc)
    base = blob(0, cy + H * 0.1, R + 2.0, top - cy - H * 0.1 + 0.6, n=72)
    if style in ("bald", "buzz"):
        c.ellipse(0, cy, 0.01, 0.01, zone=1)
        return c.render_part((0, top))
    if style in ("short", "spiky", "pixie", "side_part", "ponytail", "bun", "space_buns", "pigtails"):
        c.fill(base, zone=1, shade=0.88)
    if style in ("curly", "afro"):
        k = 1.12 if style == "curly" else 1.42
        for i in range(16):
            a = 2 * math.pi * i / 16
            c.ellipse(math.cos(a) * R * k, cy + H * 0.15 + math.sin(a) * H * 0.92 * k * 0.86, R * 0.3, R * 0.3, zone=1, shade=0.88)
        c.ellipse(0, cy + H * 0.15, R * k, H * 0.92 * k * 0.86, zone=1, shade=0.88)
    elif style == "bob":
        c.fill(path((-R - 3.5, cy + H * 0.3), ((-R - 5, cy - H * 0.62),), ((-R * 0.4, cy - H * 0.8), (R * 0.4, cy - H * 0.8), (R + 5, cy - H * 0.62)),
                    ((R + 3.5, cy + H * 0.3),), ((R + 3.5, top + 2), (-R - 3.5, top + 2), (-R - 3.5, cy + H * 0.3))), zone=1, shade=0.88)
    elif style in ("long", "wavy", "braids"):
        low = cy - H * (1.7 if style != "braids" else 0.75)
        if style == "wavy":
            pts = []
            for side in (-1, 1):
                seq = []
                for i in range(10):
                    y = cy + H * 0.25 - (cy + H * 0.25 - low) * i / 9
                    seq.append((side * (R + 4 + (2.2 if i % 2 else 0.0)), y))
                pts += seq if side < 0 else seq[::-1]
                if side < 0:
                    pts += [(-R * 0.5, low - 1.5), (R * 0.5, low - 1.5)]
            pts += [(R + 3, top), (-R - 3, top)]
            c.fill(pts, zone=1, shade=0.88)
        else:
            c.fill(path((-R - 2.5, cy + H * 0.3), ((-R - 4.5, low + 4),), ((-R * 0.5, low - 1.5), (R * 0.5, low - 1.5), (R + 4.5, low + 4)),
                        ((R + 2.5, cy + H * 0.3),), ((R + 2.5, top + 2), (-R - 2.5, top + 2), (-R - 2.5, cy + H * 0.3))), zone=1, shade=0.88)
        if style == "braids":
            for sx in (-1, 1):
                x = sx * (R + 1)
                for i in range(7):
                    y = cy - H * 0.5 - i * H * 0.16
                    c.ellipse(x, y, R * 0.16, H * 0.1, zone=1)
                    c.line([(x - R * 0.1, y + H * 0.03), (x + R * 0.1, y - H * 0.03)], 0.45, zone=1, shade=DEEP)
                yb = cy - H * 0.5 - 7 * H * 0.16
                c.ellipse(x, yb + H * 0.07, R * 0.1, R * 0.08, zone=3)
                c.fill(path((x - R * 0.07, yb + H * 0.04), ((x + R * 0.07, yb + H * 0.04),), ((x + R * 0.13, yb - H * 0.12),),
                            ((x - R * 0.13, yb - H * 0.12),)), zone=1)
    if style == "pigtails":
        for sx in (-1, 1):
            x = sx * (R + R * 0.34)
            c.fill(path((sx * R * 0.92, cy + H * 0.42), ((x + sx * R * 0.5, cy + H * 0.45), (x + sx * R * 0.4, cy - H * 0.6), (x, cy - H * 0.82)),
                        ((x - sx * R * 0.28, cy - H * 0.55), (sx * R * 0.98, cy - H * 0.15), (sx * R * 0.92, cy + H * 0.42))), zone=1)
            c.line([(x + sx * R * 0.05, cy + H * 0.1), (x, cy - H * 0.5)], 0.5, zone=1, shade=DEEP)
    elif style == "space_buns":
        for sx in (-1, 1):
            c.ellipse(sx * R * 0.7, top - 1, R * 0.34, R * 0.32, zone=1)
            c.line([(sx * R * 0.52, top - 0.5), (sx * R * 0.7, top + 2), (sx * R * 0.88, top - 0.5)], 0.5, zone=1, shade=DEEP)
    elif style == "bun":
        c.ellipse(0, top + R * 0.12, R * 0.4, R * 0.33, zone=1)
        c.line([(-R * 0.22, top + 1), (0, top + R * 0.22), (R * 0.22, top + 1)], 0.5, zone=1, shade=DEEP)
    elif style == "ponytail":
        c.ellipse(R * 0.92, cy + H * 0.5, R * 0.1, R * 0.12, zone=3)
        c.fill(path((R * 0.8, cy + H * 0.52), ((R * 1.7, cy + H * 0.62), (R * 1.75, cy - H * 0.5), (R * 1.3, cy - H * 0.95)),
                    ((R * 1.12, cy - H * 0.45), (R * 1.12, cy + H * 0.1), (R * 0.85, cy + H * 0.25))), zone=1)
    c.outline_under()
    return c.render_part((0, top))
