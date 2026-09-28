"""
Frisuren (vorne + hinten) im Stil „großer Kopf“ – Phase 04b.

Jede Frisur ist als wenige Stützpunkte beschrieben (weiche Kurve durch alle Punkte, "s" = Spitze/Ecke),
in Kopf-Einheiten: x = ±1 an den Kopfseiten, y = +1 Scheitel, −1 Kinn (Mitte = Kopfmitte).
  • Vorderteil (über dem Gesicht): rahmt das Gesicht, Pony/Scheitel, Seitensträhnen, feine Strähnen-Linien.
  • Hinterteil (hinter Kopf UND Körper): Volumen, lange Haare, Zopf, Dutt.
Zonen: 1 = Haarfarbe · 2 = Glanz (automatisch heller) · 3 = Haargummi/Spange.
Anker beider Teile = (0, hair_top) – so sitzt jede Frisur auf jeder Schablone.
"""
from __future__ import annotations

import math

from .body import head_box
from .vec import ZCanvas, bumpy, smooth, sym

STRAND = 0.62        # Strähnen-Linien: dunklere Haarfarbe
BACK = 0.84          # Hinterteil etwas dunkler (liegt im Schatten)


class _N:
    """Kopf-Einheiten → Figuren-cm."""

    def __init__(self, t: dict):
        hd = t["head"]
        self.R, self.H, self.cy, self.top = hd["w"] / 2, hd["h"] / 2, hd["cy"], t["hair_top"]

    def __call__(self, pts):
        return [(p[0] * self.R, self.cy + p[1] * self.H) + tuple(p[2:]) for p in pts]


# ------------------------------------------------------------------ Formen je Frisur
# Vorderteile als geschlossene Umrisse. „Glatt zurück“-Ansatz (Dutt, Pferdeschwanz): rechte Hälfte.
_ARCH = [(0.0, 1.13), (0.5, 1.08), (0.9, 0.84), (1.1, 0.42), (1.04, -0.05, "s"), (0.93, 0.16), (0.8, 0.42),
         (0.5, 0.58), (0.18, 0.66), (0.0, 0.72, "s")]
FRONT: dict[str, list] = {
    "short": [(-1.03, 0.05, "s"), (-1.1, 0.46), (-0.95, 0.88), (-0.55, 1.1), (0.05, 1.15), (0.6, 1.09), (1.0, 0.82),
              (1.12, 0.42), (1.04, 0.05, "s"), (0.95, 0.2), (0.9, 0.38, "s"), (0.6, 0.5), (0.2, 0.52), (-0.08, 0.45),
              (-0.26, 0.28, "s"), (-0.4, 0.42), (-0.65, 0.4), (-0.86, 0.32, "s"), (-0.96, 0.15)],
    "side_part": [(-1.04, 0.0, "s"), (-1.13, 0.5), (-0.93, 0.93), (-0.45, 1.12), (0.15, 1.15), (0.7, 1.07), (1.06, 0.78),
                  (1.14, 0.35), (1.06, -0.02, "s"), (0.96, 0.22), (0.9, 0.46, "s"), (0.58, 0.58), (0.12, 0.62),
                  (-0.35, 0.52), (-0.72, 0.34), (-0.9, 0.1, "s")],
    "spiky": [(-1.03, 0.05, "s"), (-1.1, 0.5), (-1.0, 0.85), (-0.86, 1.26, "s"), (-0.6, 1.06), (-0.38, 1.36, "s"),
              (-0.15, 1.12), (0.1, 1.42, "s"), (0.3, 1.13), (0.56, 1.34, "s"), (0.73, 1.06), (0.96, 1.2, "s"),
              (1.06, 0.85), (1.12, 0.42), (1.04, 0.05, "s"), (0.92, 0.3, "s"), (0.7, 0.46), (0.5, 0.36, "s"),
              (0.3, 0.5), (0.1, 0.38, "s"), (-0.1, 0.5), (-0.3, 0.38, "s"), (-0.5, 0.5), (-0.75, 0.42, "s"),
              (-0.95, 0.2)],
    "pixie": [(-1.03, -0.2, "s"), (-1.13, 0.35), (-1.0, 0.82), (-0.55, 1.1), (0.05, 1.15), (0.62, 1.09), (1.02, 0.8),
              (1.14, 0.3), (1.08, -0.25, "s"), (0.97, -0.05), (0.9, 0.3, "s"), (0.55, 0.42), (0.15, 0.34),
              (-0.2, 0.16), (-0.46, 0.02, "s"), (-0.56, 0.24), (-0.8, 0.3), (-0.93, 0.05)],
    "buzz": [(-1.0, 0.12, "s"), (-1.05, 0.5), (-0.8, 0.95), (-0.3, 1.07), (0.3, 1.07), (0.8, 0.95), (1.05, 0.5),
             (1.0, 0.12, "s"), (0.9, 0.36), (0.5, 0.55), (0.0, 0.6), (-0.5, 0.55), (-0.9, 0.36)],
    "bob": [(-1.2, -0.84, "s"), (-1.25, -0.2), (-1.15, 0.45), (-0.82, 0.93), (-0.3, 1.13), (0.3, 1.13), (0.82, 0.93),
            (1.15, 0.45), (1.25, -0.2), (1.2, -0.84, "s"), (1.0, -0.94, "s"), (0.9, -0.5), (0.86, 0.0),
            (0.84, 0.3, "s"), (0.52, 0.4), (0.27, 0.31, "s"), (0.0, 0.41), (-0.27, 0.31, "s"), (-0.52, 0.4),
            (-0.84, 0.3, "s"), (-0.86, 0.0), (-0.9, -0.5), (-1.0, -0.94, "s")],
    "bun": sym(_ARCH), "space_buns": sym(_ARCH), "ponytail": sym(_ARCH),
    "pigtails": sym([(0.0, 1.13), (0.5, 1.08), (0.92, 0.84), (1.12, 0.42), (1.1, 0.02, "s"), (0.95, 0.12),
                     (0.86, 0.38, "s"), (0.62, 0.44), (0.44, 0.36, "s"), (0.22, 0.46), (0.0, 0.4, "s")]),
}
# Mittelscheitel mit Seitensträhnen (rechte Hälfte, geschlossen; links gespiegelt)
PART_SIDE = {
    "long": [(0.0, 1.13, "s"), (0.45, 1.08), (0.86, 0.84), (1.12, 0.4), (1.18, -0.1), (1.16, -0.6), (1.12, -1.05),
             (1.03, -1.38, "s"), (0.92, -1.1), (0.87, -0.6), (0.85, -0.1), (0.79, 0.25), (0.56, 0.48), (0.26, 0.6),
             (0.04, 0.72, "s")],
    "wavy": [(0.0, 1.13, "s"), (0.45, 1.09), (0.88, 0.86), (1.16, 0.42), (1.26, -0.1), (1.16, -0.45), (1.27, -0.85),
             (1.12, -1.2), (1.08, -1.45, "s"), (0.94, -1.15), (0.99, -0.8), (0.88, -0.45), (0.86, -0.1), (0.8, 0.25),
             (0.56, 0.48), (0.26, 0.6), (0.04, 0.72, "s")],
    "braids": [(0.0, 1.13, "s"), (0.5, 1.08), (0.9, 0.84), (1.12, 0.42), (1.12, -0.02, "s"), (0.94, 0.12), (0.8, 0.42),
               (0.5, 0.58), (0.18, 0.66), (0.03, 0.72, "s")],
}
# Hinterteile (rechte Hälfte, oben Mitte → unten Mitte, links gespiegelt)
BACK_SIL = {
    "short": [(0.0, 1.13), (0.62, 1.07), (1.02, 0.78), (1.13, 0.35), (1.07, 0.0), (0.9, -0.08), (0.0, -0.1)],
    "long": [(0.0, 1.13), (0.6, 1.05), (1.0, 0.74), (1.15, 0.25), (1.16, -0.3), (1.12, -0.9), (1.1, -1.45),
             (1.02, -1.78), (0.88, -1.86), (0.72, -1.8), (0.0, -1.8)],
    "wavy": [(0.0, 1.13), (0.62, 1.05), (1.02, 0.76), (1.2, 0.25), (1.3, -0.3), (1.2, -0.8), (1.3, -1.3),
             (1.18, -1.74), (1.0, -1.86), (0.84, -1.76), (0.66, -1.84), (0.0, -1.82)],
    "bob": [(0.0, 1.13), (0.62, 1.06), (1.04, 0.74), (1.24, 0.2), (1.28, -0.4), (1.22, -0.88), (1.05, -1.0),
            (0.6, -0.98), (0.0, -0.95)],
}
STRANDS = {  # Strähnen-Linien (offene Kurven) im Vorderteil
    "short": [[(0.35, 1.02), (0.05, 0.82), (-0.2, 0.46)], [(0.62, 0.96), (0.4, 0.72), (0.25, 0.54)],
              [(-0.35, 1.02), (-0.62, 0.8), (-0.8, 0.42)]],
    "side_part": [[(0.42, 1.16), (0.38, 0.9), (0.46, 0.64)], [(0.3, 1.04), (-0.2, 0.94), (-0.68, 0.62), (-0.86, 0.24)],
                  [(0.22, 0.84), (-0.2, 0.74), (-0.56, 0.5)]],
    "spiky": [[(0.1, 1.2), (0.05, 0.9), (-0.05, 0.55)], [(-0.4, 1.15), (-0.45, 0.85), (-0.55, 0.55)],
              [(0.55, 1.15), (0.5, 0.85), (0.45, 0.55)]],
    "pixie": [[(0.4, 1.1), (0.0, 0.82), (-0.4, 0.1)], [(0.7, 0.98), (0.4, 0.7), (0.1, 0.4)],
              [(-0.4, 1.02), (-0.7, 0.72), (-0.85, 0.3)]],
    "bob": [[(0.0, 1.1), (0.0, 0.9), (0.02, 0.44)], [(0.5, 1.02), (0.55, 0.7), (0.52, 0.42)],
            [(-0.5, 1.02), (-0.55, 0.7), (-0.52, 0.42)], [(1.05, 0.3), (1.08, -0.3), (1.05, -0.8)],
            [(-1.05, 0.3), (-1.08, -0.3), (-1.05, -0.8)]],
    "part": [[(0.03, 0.74), (0.02, 0.95), (0.0, 1.1)], [(0.14, 1.0), (0.55, 0.84), (0.88, 0.4), (0.98, -0.2)],
             [(0.1, 0.84), (0.45, 0.7), (0.72, 0.4)], [(1.02, -0.3), (1.04, -0.8), (1.0, -1.2)]],
    "arch": [[(0.0, 1.1), (0.0, 0.72)], [(0.12, 1.0), (0.5, 0.88), (0.86, 0.5)], [(0.1, 0.84), (0.5, 0.7)]],
}
HAIR_STYLES = ["short", "spiky", "side_part", "curly", "afro", "bob", "long", "pigtails", "ponytail", "bun",
               "space_buns", "braids", "wavy", "pixie", "buzz", "bald"]


# ------------------------------------------------------------------ Hilfen
def _shine(c: ZCanvas, N: _N, clip):
    """Weicher Glanz oben links (Zone 2 = hellere Haarfarbe) + zwei feine Glanzstriche."""
    arc_o = [(math.cos(math.radians(a)) * 0.9, 0.12 + math.sin(math.radians(a)) * 0.92) for a in range(150, 64, -4)]
    arc_i = [(math.cos(math.radians(a)) * 0.74, 0.12 + math.sin(math.radians(a)) * 0.78) for a in range(66, 152, 4)]
    c.fill(N(arc_o + arc_i), zone=2, clip=clip, alpha=0.32)
    for a in (128, 104):
        c.line(N([(math.cos(math.radians(a)) * 0.84, 0.12 + math.sin(math.radians(a)) * 0.86),
                  (math.cos(math.radians(a - 14)) * 0.8, 0.12 + math.sin(math.radians(a - 14)) * 0.83)]),
               0.32, zone=2, clip=clip, alpha=0.8)


def _lines(c: ZCanvas, N: _N, curves, clip, mirror: bool = False):
    for cv in curves:
        for s in ((1, -1) if mirror else (1,)):
            pts = [(p[0] * s, p[1]) for p in cv]
            c.line(N(smooth(pts, closed=False, n=10)), 0.3, zone=1, shade=STRAND, clip=clip)


def _curly_front(N: _N, afro: bool) -> list:
    k = 1.22 if afro else 1.0
    outer = bumpy(0, 0.1, 1.08 * k, 1.0 * k, 188, -8, 9, 0.1)
    inner = bumpy(0, 0.1, 0.88, 0.34, -2, 182, 6, -0.12)
    return N(outer + inner)


# ------------------------------------------------------------------ Teile
def draw_hair_front(t: dict, style: str, ppc: float):
    N = _N(t)
    c = ZCanvas(head_box(t, 26), ppc)
    if style == "bald":
        c.ellipse(0, N.cy, 0.01, 0.01, zone=1)
        return c.render_part((0, N.top))
    if style in ("curly", "afro"):
        shape = _curly_front(N, style == "afro")
        c.fill(shape, zone=1)
        clip = c.mask(shape)
        for i in range(7):   # Locken-Kringel
            x = -0.66 + 1.32 * i / 6
            c.line(N(smooth([(x - 0.08, 0.52), (x, 0.6), (x + 0.08, 0.53)], closed=False, n=8)), 0.3, zone=1,
                   shade=STRAND, clip=clip)
        _shine(c, N, clip)
    elif style in PART_SIDE:
        right = N(smooth(PART_SIDE[style]))
        left = [(-x, y) for x, y in right]
        c.fill(right, zone=1)
        c.fill(left, zone=1)
        _lines(c, N, STRANDS["part"] if style != "braids" else STRANDS["arch"], None, mirror=True)
        _shine(c, N, c.mask(right))
        if style == "braids":
            for sx in (-1, 1):
                _braid(c, N, sx)
    else:
        shape = N(smooth(FRONT[style]))
        c.fill(shape, zone=1)
        clip = c.mask(shape)
        key = "arch" if style in ("bun", "space_buns", "ponytail", "pigtails") else style
        if key in STRANDS:
            _lines(c, N, STRANDS[key], clip, mirror=key == "arch")
        _shine(c, N, clip)
        if style == "pigtails":
            for sx in (-1, 1):
                c.ellipse(sx * 1.08 * N.R, N.cy + 0.18 * N.H, N.R * 0.1, N.R * 0.13, zone=3)
        if style == "ponytail":
            c.ellipse(0.98 * N.R, N.cy + 0.66 * N.H, N.R * 0.09, N.R * 0.12, zone=3)
    c.outline_under()
    return c.render_part((0, N.top))


def _braid(c: ZCanvas, N: _N, sx: int):
    """Zopf vor der Schulter: Glieder von der Schläfe bis unter das Kinn, unten Haargummi + Pinsel."""
    x0, y0 = 1.02 * sx, -0.1
    for i in range(8):
        y = y0 - i * 0.2
        x = x0 + sx * 0.03 * i
        c.ellipse(x * N.R, N.cy + y * N.H, N.R * 0.15, N.H * 0.12, zone=1)
        c.line(N([(x - 0.1 * sx, y + 0.05), (x + 0.1 * sx, y - 0.05)]), 0.3, zone=1, shade=STRAND)
    yb = y0 - 8 * 0.2 + 0.08
    xb = x0 + sx * 0.24
    c.ellipse(xb * N.R, N.cy + yb * N.H, N.R * 0.09, N.R * 0.07, zone=3)
    c.fill(N(smooth([(xb - 0.07, yb - 0.04, "s"), (xb + 0.07, yb - 0.04, "s"), (xb + 0.12, yb - 0.26, "s"),
                     (xb, yb - 0.2), (xb - 0.12, yb - 0.26, "s")])), zone=1)


def draw_hair_back(t: dict, style: str, ppc: float):
    N = _N(t)
    R, H, cy, top = N.R, N.H, N.cy, N.top
    c = ZCanvas((-R * 2.4, cy - H * 3.2, R * 2.4, top + 24), ppc)
    if style in ("bald", "buzz"):
        c.ellipse(0, cy, 0.01, 0.01, zone=1)
        return c.render_part((0, top))
    if style in ("curly", "afro"):
        k = 1.22 if style == "curly" else 1.55
        c.fill(N(bumpy(0, 0.05, 1.12 * k, 1.05 * k, 0, 360, 16, 0.12)), zone=1, shade=BACK)
    elif style in BACK_SIL:
        c.fill(N(smooth(sym(BACK_SIL[style]))), zone=1, shade=BACK)
        if style in ("long", "wavy"):
            for sx in (-1, 1):
                _lines(c, N, [[(sx * 1.06, -0.2), (sx * 1.04, -0.9), (sx * 0.98, -1.6)],
                              [(sx * 0.9, -0.9), (sx * 0.86, -1.62)]], None)
    else:
        c.fill(N(smooth(sym(BACK_SIL["short"]))), zone=1, shade=BACK)
    if style == "pigtails":
        for sx in (-1, 1):
            tail = [(sx * 1.05, 0.3, "s"), (sx * 1.35, 0.3), (sx * 1.6, -0.1), (sx * 1.66, -0.6), (sx * 1.5, -1.05, "s"),
                    (sx * 1.38, -0.62), (sx * 1.2, -0.25), (sx * 1.02, 0.02, "s")]
            c.fill(N(smooth(tail)), zone=1)
            _lines(c, N, [[(sx * 1.25, 0.15), (sx * 1.48, -0.3), (sx * 1.5, -0.8)]], None)
    elif style == "ponytail":
        tail = [(0.8, 0.82, "s"), (1.2, 0.95), (1.5, 0.6), (1.58, 0.0), (1.48, -0.7), (1.3, -1.05, "s"), (1.3, -0.5),
                (1.22, 0.1), (1.0, 0.5, "s")]
        c.fill(N(smooth(tail)), zone=1)
        _lines(c, N, [[(1.15, 0.8), (1.42, 0.3), (1.4, -0.5)]], None)
    elif style == "bun":
        c.ellipse(0, cy + H * 1.24, R * 0.4, R * 0.34, zone=1)
        _lines(c, N, [[(-0.24, 1.12), (0.0, 1.34), (0.24, 1.12)], [(-0.12, 1.4), (0.14, 1.2)]], None)
    elif style == "space_buns":
        for sx in (-1, 1):
            c.ellipse(sx * R * 0.66, cy + H * 1.12, R * 0.33, R * 0.3, zone=1)
            _lines(c, N, [[(sx * 0.5, 1.02), (sx * 0.66, 1.22), (sx * 0.82, 1.02)]], None)
    c.outline_under()
    return c.render_part((0, top))
