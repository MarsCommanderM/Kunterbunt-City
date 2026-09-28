"""
Accessoires (Ebene „Accessory“) und Hilfsmittel (Ebene „Aid“) – Phase 04b.

Beide Ebenen hängen am Kopf (Anker = Kopfmitte) und liegen über den Haaren.
Zonen Accessoire: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Drittfarbe (Gläser, Blütenmitte).
Zonen Hilfsmittel: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Haut (Pflaster-Rand).
"""
from __future__ import annotations

import math

from .body import eye_pos, head_box
from .vec import ZCanvas, blob, smooth


class _N:
    def __init__(self, t: dict):
        hd = t["head"]
        self.R, self.H, self.cy, self.top = hd["w"] / 2, hd["h"] / 2, hd["cy"], t["hair_top"]

    def __call__(self, pts):
        return [(p[0] * self.R, self.cy + p[1] * self.H) + tuple(p[2:]) for p in pts]

    def p(self, x, y):
        return x * self.R, self.cy + y * self.H


ACC_STYLES = ["none", "glasses", "glasses_square", "sunglasses", "headband", "bow", "hairclip", "cap", "beanie",
              "sunhat", "flowers", "headphones"]
AID_STYLES = ["none", "hearing_aid", "cochlear", "eye_patch", "plaster", "arm_sling"]


def _frames(c: ZCanvas, t: dict, square: bool, lens_zone: int, lens_op: float, frame_w: float):
    N = _N(t)
    ex, ey, r = eye_pos(t)
    rr = r * 2.5
    lenses = []
    for sx in (-1, 1):
        x = sx * ex
        if square:
            pts = smooth([(x - rr, ey + rr * 0.85, "s"), (x + rr, ey + rr * 0.85, "s"), (x + rr * 0.95, ey - rr * 0.75, "s"),
                          (x - rr * 0.95, ey - rr * 0.75, "s")], n=2)
        else:
            pts = blob(x, ey, rr, rr * 0.95, n=48)
        lenses.append(pts)
        c.line(pts, frame_w, zone=1, closed=True)
    c.line([(-ex + rr * 0.95, ey + rr * 0.2), (0, ey + rr * 0.35), (ex - rr * 0.95, ey + rr * 0.2)], frame_w, zone=1)
    for sx in (-1, 1):   # Bügel zum Ohr
        c.line([(sx * (ex + rr), ey + rr * 0.3), (sx * N.R * 1.0, ey + rr * 0.45)], frame_w * 0.8, zone=1)
    c.outline_under(0.35)
    for pts in lenses:
        c.glass(pts, zone=lens_zone, opacity=lens_op)
    for sx in (-1, 1):   # Glanz auf dem Glas
        x = sx * ex
        c.line([(x - rr * 0.5, ey + rr * 0.45), (x - rr * 0.15, ey + rr * 0.62)], frame_w * 0.6, zone=2, alpha=0.9)


def draw_accessory(t: dict, style: str, ppc: float):
    N = _N(t)
    R, H, cy, top = N.R, N.H, N.cy, N.top
    c = ZCanvas(head_box(t, 20), ppc, outline_cm=0.5)
    if style == "none":
        c.ellipse(0, cy, 0.01, 0.01, zone=1)
        return c.render_part((0, cy))
    if style in ("glasses", "glasses_square"):
        _frames(c, t, style == "glasses_square", 3, 0.22, R * 0.05)
        return c.render_part((0, cy))
    if style == "sunglasses":
        _frames(c, t, True, 0, 0.88, R * 0.055)
        return c.render_part((0, cy))
    if style == "headband":
        band_o = [(math.cos(math.radians(a)) * R * 1.1, cy + H * 0.12 + math.sin(math.radians(a)) * (top - cy - H * 0.12 + 0.6))
                  for a in range(172, 7, -3)]
        band_i = [(math.cos(math.radians(a)) * R * 0.98, cy + H * 0.12 + math.sin(math.radians(a)) * (top - cy - H * 0.12 - 3.2))
                  for a in range(8, 173, 3)]
        c.fill(band_o + band_i, zone=1)
        c.fill(N([(-0.35, 1.02), (0.35, 1.02), (0.35, 0.95), (-0.35, 0.95)]), zone=1, shade=0.9, clip=c.mask(band_o + band_i))
    elif style == "bow":
        bx, by = 0.62, 0.88
        for sx in (-1, 1):
            wing = N(smooth([(bx, by, "s"), (bx + sx * 0.22, by + 0.2), (bx + sx * 0.36, by + 0.08),
                             (bx + sx * 0.34, by - 0.12), (bx + sx * 0.2, by - 0.18)]))
            c.fill(wing, zone=1)
            c.line(N(smooth([(bx + sx * 0.05, by), (bx + sx * 0.18, by + 0.06), (bx + sx * 0.26, by + 0.02)], closed=False, n=6)),
                   0.3, zone=1, shade=0.62)
        c.ellipse(*N.p(bx, by), R * 0.07, R * 0.08, zone=2)
    elif style == "hairclip":
        for i, (x, y) in enumerate(((0.55, 0.7), (0.72, 0.58))):
            c.fill(N(smooth([(x - 0.12, y - 0.02, "s"), (x + 0.12, y + 0.06, "s"), (x + 0.1, y + 0.12, "s"),
                             (x - 0.13, y + 0.04, "s")], n=2)), zone=1 if i == 0 else 2)
    elif style == "cap":
        dome = N(smooth([(-1.08, 0.5, "s"), (-1.0, 0.9), (-0.5, 1.2), (0.2, 1.24), (0.8, 1.08), (1.1, 0.62), (1.1, 0.5, "s")]))
        c.fill(dome, zone=1)
        cl = c.mask(dome)
        c.fill(N([(0.2, 1.4), (1.3, 1.4), (1.3, 0.4), (0.25, 0.4)]), zone=1, shade=0.88, clip=cl)
        c.line(N(smooth([(0.0, 1.24), (0.02, 0.9), (0.0, 0.52)], closed=False, n=8)), 0.35, zone=1, shade=0.62)
        brim = N(smooth([(-1.12, 0.56, "s"), (-0.4, 0.62), (0.4, 0.6), (1.1, 0.56, "s"), (1.62, 0.38, "s"), (1.2, 0.4),
                         (0.4, 0.44), (-1.1, 0.42, "s")]))
        c.fill(brim, zone=2)
        c.ellipse(*N.p(0.1, 1.24), R * 0.07, R * 0.05, zone=2)
    elif style == "beanie":
        dome = N(smooth([(-1.1, 0.4, "s"), (-1.06, 0.85), (-0.6, 1.22), (0.0, 1.3), (0.6, 1.22), (1.06, 0.85), (1.1, 0.4, "s")]))
        c.fill(dome, zone=1)
        cl = c.mask(dome)
        for i in range(-4, 5):
            x = i * 0.22
            c.line(N([(x, 0.62), (x * 0.95, 1.2)]), 0.3, zone=1, shade=0.7, clip=cl)
        cuff = N(smooth([(-1.14, 0.62, "s"), (1.14, 0.62, "s"), (1.14, 0.36, "s"), (-1.14, 0.36, "s")], n=2))
        c.fill(cuff, zone=2)
        for i in range(-5, 6):
            c.line(N([(i * 0.2, 0.4), (i * 0.2, 0.58)]), 0.3, zone=2, shade=0.72)
        c.ellipse(*N.p(0.0, 1.38), R * 0.2, R * 0.19, zone=2)
    elif style == "sunhat":
        brim = N(smooth([(-1.7, 0.55), (-1.2, 0.72), (0.0, 0.78), (1.2, 0.72), (1.7, 0.55), (1.2, 0.42), (0.0, 0.4),
                         (-1.2, 0.42)]))
        c.fill(brim, zone=1)
        crown = N(smooth([(-0.9, 0.62, "s"), (-0.85, 1.05), (-0.4, 1.3), (0.4, 1.3), (0.85, 1.05), (0.9, 0.62, "s")]))
        c.fill(crown, zone=1)
        c.fill(N(smooth([(-0.9, 0.82, "s"), (0.9, 0.82, "s"), (0.9, 0.64, "s"), (-0.9, 0.64, "s")], n=2)), zone=2)
        c.line(N(smooth([(-1.2, 0.6), (0.0, 0.66), (1.2, 0.6)], closed=False, n=8)), 0.3, zone=1, shade=0.7)
    elif style == "flowers":
        for i in range(7):
            a = math.radians(165 - i * 25)
            x, y = math.cos(a) * 1.02, 0.18 + math.sin(a) * 0.95
            fx, fy = N.p(x, y)
            pr = R * 0.1
            for k in range(5):
                b = 2 * math.pi * k / 5
                c.ellipse(fx + math.cos(b) * pr, fy + math.sin(b) * pr, pr * 0.85, pr * 0.85, zone=1 if i % 2 == 0 else 2)
            c.ellipse(fx, fy, pr * 0.55, pr * 0.55, zone=3)
    elif style == "headphones":
        band_o = [(math.cos(math.radians(a)) * R * 1.12, cy + math.sin(math.radians(a)) * (top - cy + 1.0)) for a in range(176, 3, -3)]
        band_i = [(math.cos(math.radians(a)) * R * 1.02, cy + math.sin(math.radians(a)) * (top - cy - 2.2)) for a in range(4, 177, 3)]
        c.fill(band_o + band_i, zone=1)
        for sx in (-1, 1):
            cup = N(smooth([(sx * 1.0, 0.25, "s"), (sx * 1.24, 0.22), (sx * 1.3, -0.12), (sx * 1.22, -0.4), (sx * 1.0, -0.42, "s")]))
            c.fill(cup, zone=2)
            c.fill(N(smooth([(sx * 0.94, 0.18, "s"), (sx * 1.08, 0.2), (sx * 1.1, -0.35), (sx * 0.94, -0.34, "s")])), zone=1)
    c.outline_under()
    return c.render_part((0, cy))


def draw_aid(t: dict, style: str, ppc: float):
    """Hilfsmittel: Hörgerät, Cochlea-Implantat, Augenklappe, Pflaster, Armschlinge (Oberkörper bewegt sich mit dem Kopf)."""
    N = _N(t)
    R, H, cy = N.R, N.H, N.cy
    c = ZCanvas(head_box(t, 60) if style == "arm_sling" else head_box(t, 12), ppc, outline_cm=0.45)
    if style == "none":
        c.ellipse(0, cy, 0.01, 0.01, zone=1)
        return c.render_part((0, cy))
    if style == "hearing_aid":
        c.fill(N(smooth([(1.02, 0.02), (1.14, 0.12), (1.16, -0.08), (1.06, -0.22), (0.99, -0.14)])), zone=1)
        c.line(N(smooth([(1.02, -0.18), (0.98, -0.28), (0.95, -0.22)], closed=False, n=6)), 0.35, zone=2)
    elif style == "cochlear":
        c.ellipse(*N.p(1.0, 0.32), R * 0.1, R * 0.1, zone=1)
        c.line(N(smooth([(1.02, 0.24), (1.12, 0.05), (1.12, -0.12)], closed=False, n=8)), 0.35, zone=1)
        c.fill(N(smooth([(1.04, -0.02), (1.15, 0.02), (1.17, -0.2), (1.07, -0.26)])), zone=2)
    elif style == "eye_patch":
        ex, ey, r = eye_pos(t)
        c.line(N(smooth([(-1.06, 0.42), (-0.2, 0.2), (0.4, -0.05), (1.04, -0.35)], closed=False, n=10)), R * 0.03, zone=0)
        c.fill(blob(ex, ey + 0.2, r * 2.6, r * 2.3, n=40), zone=1)
    elif style == "plaster":
        x, y = -0.46, 0.3
        pts = N(smooth([(x - 0.22, y + 0.02, "s"), (x + 0.2, y + 0.14, "s"), (x + 0.23, y + 0.03, "s"), (x - 0.19, y - 0.1, "s")], n=2))
        c.fill(pts, zone=1)
        c.fill(N(smooth([(x - 0.06, y + 0.02, "s"), (x + 0.07, y + 0.07, "s"), (x + 0.09, y - 0.0, "s"), (x - 0.04, y - 0.05, "s")], n=2)),
               zone=2)
    elif style == "arm_sling":
        # Dreieckstuch vor dem Bauch, Band um den Hals
        to = t["torso"]
        y0 = to["top"] - (to["top"] - to["bot"]) * 0.35
        sling = smooth([(-to["w_top"] * 0.45, y0, "s"), (to["w_top"] * 0.5, y0 + 1, "s"), (to["w_top"] * 0.1, to["bot"] + 2, "s")], n=2)
        c.fill(sling, zone=1)
        c.line([(-to["w_top"] * 0.3, y0 + 0.5), (-to["w_top"] * 0.18, to["top"] - 1)], 1.2, zone=1)
        c.line([(to["w_top"] * 0.35, y0 + 0.8), (to["w_top"] * 0.2, to["top"] - 1)], 1.2, zone=1)
    c.outline_under()
    return c.render_part((0, cy))
