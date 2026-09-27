"""
Frisuren (vorne + hinten) im Stil „großer Kopf“ – Phase 04b.

Vorderteil liegt ÜBER dem Gesicht (Pony, Seitensträhnen), Hinterteil HINTER dem Kopf (Volumen, lange
Haare, Zöpfe). Zone 1 = Haarfarbe, Strähnen-Linien = dunklere Haarfarbe (shade), Zone 2 = Haarband/Spange.
Anker beider Teile = (0, hair_top) – so sitzt jede Frisur auf jeder Schablone.
"""
from __future__ import annotations

import math

from .body import DEEP, head_box, head_outline
from .vec import ZCanvas, blob, path


def _geo(t: dict):
    hd = t["head"]
    return hd["w"] / 2, hd["h"] / 2, hd["cy"], t["hair_top"]


def _cap(t: dict, brow: float, side: float, puff: float = 1.0) -> list:
    """Haarkappe: oben über dem Kopf, Stirnlinie bei brow (Anteil der Kopfhöhe über der Mitte), Seiten bis side."""
    R, H, cy, top = _geo(t)
    g = 1.2 * puff
    pts = []
    n = 60
    for i in range(n + 1):             # Außenbogen von links-unten über oben nach rechts-unten
        a = math.pi * (1.0 + 0.12) - (math.pi * 1.24) * i / n
        pts.append((math.cos(a) * (R + g), cy + math.sin(a) * (top - cy)))
    return pts + [(R * 0.98, cy + H * side), (R * 0.2, cy + H * brow), (-R * 0.2, cy + H * brow), (-R * 0.98, cy + H * side)]


def _fringe(t: dict, brow: float, n: int, depth: float, side: float = -0.05) -> list:
    """Pony aus n runden Strähnen: Unterkante gewellt."""
    R, H, cy, top = _geo(t)
    pts = [(-R - 1.2, cy + H * side), (-R - 1.2, cy + H * 0.2)]
    arc = []
    for i in range(61):
        a = math.pi - math.pi * i / 60
        arc.append((math.cos(a) * (R + 1.2), cy + math.sin(a) * (top - cy)))
    pts += arc + [(R + 1.2, cy + H * 0.2), (R + 1.2, cy + H * side)]
    # gewellte Unterkante von rechts nach links
    xs = [R * 0.98 - (2 * R * 0.98) * k / n for k in range(n + 1)]
    for k in range(n):
        x0, x1 = xs[k], xs[k + 1]
        yb = cy + H * brow
        mid = (x0 + x1) / 2
        pts += [(x0, yb + H * 0.05), (mid, yb - H * depth), (x1, yb + H * 0.05)]
    return pts


def _strands(c: ZCanvas, t: dict, clip, n: int = 4, y0: float = 0.75, y1: float = 0.25):
    R, H, cy, top = _geo(t)
    for k in range(n):
        x = -R * 0.6 + R * 1.2 * (k + 0.5) / n
        c.line([(x * 0.6, cy + H * y0), (x, cy + H * (y0 + y1) / 2), (x * 1.1, cy + H * y1)], 0.55, zone=1, shade=DEEP, clip=clip)


HAIR_STYLES = ["short", "spiky", "side_part", "curly", "afro", "bob", "long", "pigtails", "ponytail", "bun",
               "space_buns", "braids", "wavy", "pixie", "buzz", "bald"]


def draw_hair_front(t: dict, style: str, ppc: float):
    R, H, cy, top = _geo(t)
    c = ZCanvas(head_box(t, 16), ppc)
    head = c.mask(head_outline(t, 2.0))
    if style == "bald":
        c.ellipse(0, cy, 0.01, 0.01, zone=1)
        return c.render_part((0, top))
    if style == "buzz":
        cap = _cap(t, 0.52, 0.15, 0.3)
        c.fill(cap, zone=1, clip=head)
        c.fill(cap, zone=1, shade=0.93, clip=c.mask(blob(0, cy, R * 2, H * 0.6)))
    elif style in ("short", "spiky", "pixie"):
        f = _fringe(t, 0.45 if style != "pixie" else 0.36, 5 if style != "spiky" else 7, 0.1 if style != "spiky" else 0.2)
        c.fill(f, zone=1)
        if style == "spiky":       # Zacken oben
            for k in range(5):
                x = -R * 0.7 + R * 1.4 * k / 4
                c.fill([(x - R * 0.2, top - 3), (x + R * 0.05, top + 3.2), (x + R * 0.2, top - 3)], zone=1)
        _strands(c, t, c.mask(f), 3)
    elif style == "side_part":
        pts = _cap(t, 0.42, -0.1)
        pts = pts[:-4] + [(R * 0.98, cy - H * 0.1), (R * 0.6, cy + H * 0.36), (-R * 0.1, cy + H * 0.55), (-R * 0.7, cy + H * 0.38),
                          (-R * 0.98, cy + H * 0.1)]
        c.fill(pts, zone=1)
        c.line([(-R * 0.25, top - 0.5), (-R * 0.1, cy + H * 0.6)], 0.55, zone=1, shade=DEEP, clip=c.mask(pts))
    elif style in ("curly", "afro"):
        k = 1.0 if style == "curly" else 1.25
        rr = R * (0.28 if style == "curly" else 0.3)
        for i in range(9):
            a = math.pi * (0.05 + 0.9 * i / 8)
            c.ellipse(math.cos(a) * R * 0.92 * k, cy + H * 0.18 + math.sin(a) * (top - cy - H * 0.18) * 0.96, rr, rr, zone=1)
        c.fill(_cap(t, 0.5, 0.2, 1.1), zone=1)
        for i in range(5):
            x = -R * 0.6 + R * 1.2 * i / 4
            c.ellipse(x, cy + H * 0.5, R * 0.2, R * 0.16, zone=1)
            c.line([(x - R * 0.1, cy + H * 0.47), (x, cy + H * 0.42), (x + R * 0.1, cy + H * 0.47)], 0.5, zone=1, shade=DEEP)
    else:
        # langes/mittleres Haar: Mittel- oder Seitenscheitel, Strähnen seitlich bis Kinnhöhe
        brow = {"bob": 0.3, "long": 0.4, "wavy": 0.4, "pigtails": 0.35, "ponytail": 0.45, "bun": 0.45,
                "space_buns": 0.4, "braids": 0.42}.get(style, 0.4)
        if style in ("bob", "pigtails"):
            f = _fringe(t, brow, 6, 0.08, side=-0.55)
        else:
            f = path((-R - 1.5, cy - H * 0.55), ((-R - 3.5, cy + H * 0.5), (-R * 0.8, top + 1.5), (0, top + 1.2)),
                     ((R * 0.8, top + 1.5), (R + 3.5, cy + H * 0.5), (R + 1.5, cy - H * 0.55)),
                     ((R * 0.84, cy - H * 0.3),), ((R * 0.95, cy + H * 0.15), (R * 0.5, cy + H * brow), (0.4, cy + H * 0.62)),
                     ((-R * 0.5, cy + H * brow), (-R * 0.95, cy + H * 0.15), (-R * 0.84, cy - H * 0.3)))
        c.fill(f, zone=1)
        cl = c.mask(f)
        if style not in ("bob", "pigtails"):
            c.line([(0.4, cy + H * 0.62), (0.2, top)], 0.55, zone=1, shade=DEEP, clip=cl)
        for sx in (-1, 1):
            c.line([(sx * R * 0.55, top - 3), (sx * (R + 0.5), cy), (sx * (R - 0.5), cy - H * 0.45)], 0.55, zone=1,
                   shade=DEEP, clip=cl)
        if style in ("pigtails", "space_buns", "ponytail"):
            for sx in ((-1, 1) if style != "ponytail" else ()):
                c.ellipse(sx * R * 0.93, cy + H * 0.52, R * 0.1, R * 0.1, zone=2)
    c.outline_under()
    return c.render_part((0, top))


def draw_hair_back(t: dict, style: str, ppc: float):
    R, H, cy, top = _geo(t)
    c = ZCanvas((-R * 2.4, cy - H * 3.2, R * 2.4, top + 22), ppc)
    if style in ("bald", "buzz", "short", "spiky", "pixie", "side_part"):
        grow = {"short": 1.4, "spiky": 1.4, "pixie": 1.6, "side_part": 1.4}.get(style, 0.0)
        if grow == 0.0:
            c.ellipse(0, cy, 0.01, 0.01, zone=1)
            return c.render_part((0, top))
        c.fill(blob(0, cy + H * 0.12, R + grow, top - cy - H * 0.12 + grow * 0.3, n=64), zone=1, shade=0.88)
    elif style in ("curly", "afro"):
        k = 1.15 if style == "curly" else 1.45
        for i in range(14):
            a = 2 * math.pi * i / 14
            c.ellipse(math.cos(a) * R * k, cy + H * 0.2 + math.sin(a) * H * 0.95 * k * 0.85, R * 0.32, R * 0.32, zone=1, shade=0.88)
        c.ellipse(0, cy + H * 0.2, R * k, H * 0.95 * k * 0.85, zone=1, shade=0.88)
    elif style == "bob":
        c.fill(path((-R - 3, cy + H * 0.3), ((-R - 4.5, cy - H * 0.6),), ((-R * 0.4, cy - H * 0.78), (R * 0.4, cy - H * 0.78), (R + 4.5, cy - H * 0.6)),
                    ((R + 3, cy + H * 0.3),), ((R + 3, top + 2), (-R - 3, top + 2), (-R - 3, cy + H * 0.3))), zone=1, shade=0.88)
    elif style in ("long", "wavy", "braids"):
        low = cy - H * (1.55 if style != "braids" else 0.7)
        if style == "wavy":
            pts = [(-R - 3, cy + H * 0.3)]
            for i in range(9):
                y = cy + H * 0.2 - (cy + H * 0.2 - low) * i / 8
                pts.append((-R - 3.5 - (1.8 if i % 2 else -0.5), y))
            pts += [(-R * 0.5, low - 1), (R * 0.5, low - 1)]
            for i in range(9):
                y = low + (cy + H * 0.2 - low) * i / 8
                pts.append((R + 3.5 + (1.8 if i % 2 else -0.5), y))
            pts += [(R + 3, cy + H * 0.3), (R, top), (-R, top)]
            c.fill(pts, zone=1, shade=0.88)
        else:
            c.fill(path((-R - 2.5, cy + H * 0.3), ((-R - 4, low + 3),), ((-R * 0.5, low - 1), (R * 0.5, low - 1), (R + 4, low + 3)),
                        ((R + 2.5, cy + H * 0.3),), ((R + 2.5, top + 2), (-R - 2.5, top + 2), (-R - 2.5, cy + H * 0.3))), zone=1, shade=0.88)
        if style == "braids":
            for sx in (-1, 1):
                x = sx * (R + 1)
                for i in range(6):
                    y = cy - H * 0.55 - i * H * 0.17
                    c.ellipse(x, y, R * 0.17, H * 0.11, zone=1)
                c.ellipse(x, cy - H * 0.55 - 6 * H * 0.17 + H * 0.05, R * 0.1, R * 0.1, zone=2)
                c.fill(path((x - R * 0.08, cy - H * 1.62), ((x + R * 0.08, cy - H * 1.62),), ((x + R * 0.15, cy - H * 1.85),), ((x - R * 0.15, cy - H * 1.85),)), zone=1)
    elif style in ("pigtails", "space_buns", "ponytail", "bun"):
        c.fill(blob(0, cy + H * 0.12, R + 1.5, top - cy - H * 0.12 + 0.5, n=64), zone=1, shade=0.88)
        if style == "pigtails":
            for sx in (-1, 1):
                x = sx * (R + R * 0.32)
                c.fill(path((sx * R * 0.9, cy + H * 0.55), ((x + sx * R * 0.45, cy + H * 0.5), (x + sx * R * 0.35, cy - H * 0.55), (x, cy - H * 0.75)),
                            ((x - sx * R * 0.25, cy - H * 0.5), (sx * R * 0.95, cy - H * 0.1), (sx * R * 0.9, cy + H * 0.55))), zone=1)
        elif style == "space_buns":
            for sx in (-1, 1):
                c.ellipse(sx * R * 0.72, top - 2, R * 0.34, R * 0.32, zone=1)
                c.line([(sx * R * 0.55, top - 1), (sx * R * 0.72, top + 1.5), (sx * R * 0.9, top - 1)], 0.5, zone=1, shade=DEEP)
        elif style == "bun":
            c.ellipse(0, top + R * 0.12, R * 0.38, R * 0.32, zone=1)
            c.line([(-R * 0.2, top + 1), (0, top + R * 0.2), (R * 0.2, top + 1)], 0.5, zone=1, shade=DEEP)
        else:
            c.fill(path((R * 0.7, cy + H * 0.55), ((R * 1.6, cy + H * 0.7), (R * 1.7, cy - H * 0.4), (R * 1.25, cy - H * 0.9)),
                        ((R * 1.1, cy - H * 0.4), (R * 1.1, cy + H * 0.1), (R * 0.8, cy + H * 0.2))), zone=1)
    c.outline_under()
    return c.render_part((0, top))
