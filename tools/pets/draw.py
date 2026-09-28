"""
Haustiere im Stil C (P04b-T07): Vektor, weiche Schattierung, braune Tinte, großer Kopf wie die Figuren.

Gezeichnet in Entwurfs-Einheiten: Höhe = 100, Breite = 100 · w/h aus der Maßstab-Tabelle (Ursprung unten
Mitte, y nach oben). So hat jedes Tier dieselbe Strichstärke im Bild – egal ob Hamster (7 cm) oder Pony.
Zonen: 1 = Fell/Körper · 2 = Bauch, Schnauze, Pfoten, Glanzpunkte · 3 = Halsband, Mähne, Flügel, Schnabel.
Augen, Nase, Mund = Tinte.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chibi.vec import ZCanvas  # noqa: E402
from items.kit import ell, rrect, smooth  # noqa: E402

OUT = 1.3          # Kontur in Entwurfs-Einheiten (≈ 1,3 % der Tierhöhe)
INNER = 0.6        # feine Innenlinie
SHADE = 0.84


class Pet:
    def __init__(self, w: float, h: float = 100.0, ppc: float = 8.0):
        self.w, self.h = w, h
        m = 24.0      # Platz für Schwanz/Ohren/Flügel – danach wird eng zugeschnitten
        self.c = ZCanvas((-w / 2 - m, -m, w / 2 + m, h + m), ppc, outline_cm=OUT)

    def finish(self):
        self.c.outline_under()
        return self.c.render_part((0, self.c.content_bottom_cm()), pad_cm=0.4)


def shaded(c, pts, zone=1, side="bottom", amount=SHADE, frac=0.3, inner=True):
    c.fill(pts, zone=zone)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    cl = c.mask(pts)
    if side == "right":
        xs0 = x1 - (x1 - x0) * frac
        c.fill([(xs0, y0 - 1), (x1 + 1, y0 - 1), (x1 + 1, y1 + 1), (xs0, y1 + 1)], zone=zone, shade=amount, clip=cl)
    else:
        ys1 = y0 + (y1 - y0) * frac
        c.fill([(x0 - 1, y0 - 1), (x1 + 1, y0 - 1), (x1 + 1, ys1), (x0 - 1, ys1)], zone=zone, shade=amount, clip=cl)
    if inner:
        c.line(pts, INNER, zone=0, closed=True)
    return cl


def eye(c, x, y, r, look=(0.0, 0.0)):
    """Großes Kulleraugen-Paar-Auge: Tinte + zwei Glanzpunkte (Zone 2 hell)."""
    c.fill(ell(x, y, r * 0.86, r, 32), zone=0)
    c.fill(ell(x - r * 0.28 + look[0], y + r * 0.34 + look[1], r * 0.34, r * 0.36, 20), zone=2, shade=1.25)
    c.fill(ell(x + r * 0.3, y - r * 0.38, r * 0.14, r * 0.14, 12), zone=2, shade=1.25)


def blush(c, x, y, r):
    c.fill(ell(x, y, r, r * 0.6, 20), zone=3, alpha=0.35)


def smile(c, x, y, s):
    c.line(smooth([(x - s, y + s * 0.3), (x - s * 0.5, y - s * 0.2), (x, y + s * 0.2), (x + s * 0.5, y - s * 0.2),
                   (x + s, y + s * 0.3)], closed=False), INNER * 1.2, zone=0)


def collar(c, x, y, w, h):
    band = smooth([(x - w / 2, y + h * 0.2), (x, y - h * 0.3), (x + w / 2, y + h * 0.2), (x + w / 2, y + h),
                   (x, y + h * 0.5), (x - w / 2, y + h)])
    c.fill(band, zone=3)
    c.line(band, INNER, zone=0, closed=True)
    c.fill(ell(x, y - h * 0.25, h * 0.7, h * 0.7, 24), zone=3, shade=1.12)
    c.line(ell(x, y - h * 0.25, h * 0.7, h * 0.7, 24), INNER, zone=0, closed=True)


# ------------------------------------------------------------------ sitzende Vierbeiner (Hund, Katze, Hase, Drache)
def sitting(p: Pet, ears: str = "flop", tail: str = "wag", wings: bool = False, whiskers: bool = False):
    c, W, H = p.c, p.w, p.h
    hr = min(W * 0.36, 30.0)                      # Kopf-Radius (großer Kopf)
    hy = H - hr * 0.95
    bw = min(W * 0.34, 26.0)
    # Schwanz hinter dem Körper
    if tail == "wag":
        t = smooth([(bw * 0.6, 12), (bw * 1.3, 18), (bw * 1.55, 34), (bw * 1.3, 38), (bw * 1.15, 24), (bw * 0.5, 20)])
        shaded(c, t, 1, "right", 0.86, 0.4)
    elif tail == "long":
        t = smooth([(bw * 0.5, 6), (bw * 1.3, 6), (bw * 1.7, 18), (bw * 1.6, 34), (bw * 1.35, 36), (bw * 1.35, 20),
                    (bw * 1.1, 13), (bw * 0.5, 14)])
        shaded(c, t, 1, "right", 0.86, 0.4)
    elif tail == "puff":
        c.fill(ell(bw * 0.95, 10, 7, 6.5, 32), zone=2)
        c.line(ell(bw * 0.95, 10, 7, 6.5, 32), INNER, zone=0, closed=True)
    elif tail == "dragon":
        t = smooth([(bw * 0.5, 4), (bw * 1.7, 2), (bw * 2.0, 8, "s"), (bw * 1.5, 10), (bw * 0.6, 16)])
        shaded(c, t, 1, "bottom", 0.86, 0.4)
        c.fill([(bw * 1.85, 6), (bw * 2.25, 12), (bw * 2.0, 3)], zone=3)
    if wings:
        for sx, sh in ((-1, 0.82), (1, 0.9)):
            wg = smooth([(sx * bw * 0.4, 36), (sx * bw * 1.4, 52, "s"), (sx * bw * 1.25, 38), (sx * bw * 1.5, 30, "s"),
                         (sx * bw * 1.05, 26), (sx * bw * 1.2, 18, "s"), (sx * bw * 0.5, 24)])
            c.fill(wg, zone=3, shade=sh)
            c.line(wg, INNER, zone=0, closed=True)
    # Hinterbeine (Keulen) + Körper
    for sx in (-1, 1):
        c.fill(ell(sx * bw * 0.72, 9, bw * 0.46, 9.5, 32), zone=1, shade=0.88)
        c.line(ell(sx * bw * 0.72, 9, bw * 0.46, 9.5, 32), INNER, zone=0, closed=True)
    body = smooth([(-bw, 3), (-bw * 0.95, 20), (-bw * 0.62, 40), (0, hy - hr * 0.55), (bw * 0.62, 40), (bw * 0.95, 20),
                   (bw, 3), (0, 0)])
    cl = shaded(c, body, 1, "right", 0.88, 0.28)
    c.fill(ell(0, 18, bw * 0.55, 16, 32), zone=2, clip=cl)
    # Vorderpfoten
    for sx in (-1, 1):
        c.fill(rrect(sx * bw * 0.32 - 4.2, 0, sx * bw * 0.32 + 4.2, 22, 4), zone=1, shade=0.95)
        paw = ell(sx * bw * 0.32, 3.2, 5.2, 3.6, 24)
        c.fill(paw, zone=2)
        c.line(paw, INNER, zone=0, closed=True)
        c.line([(sx * bw * 0.32 - 1.3, 1.5), (sx * bw * 0.32 - 1.3, 4.5)], INNER * 0.8, zone=0)
        c.line([(sx * bw * 0.32 + 1.3, 1.5), (sx * bw * 0.32 + 1.3, 4.5)], INNER * 0.8, zone=0)
    # Ohren hinter dem Kopf
    if ears == "point":
        for sx in (-1, 1):
            e = smooth([(sx * hr * 0.25, hy + hr * 0.7, "s"), (sx * hr * 0.95, hy + hr * 1.28, "s"), (sx * hr * 0.95, hy + hr * 0.3, "s")], n=3)
            c.fill(e, zone=1)
            c.line(e, INNER, zone=0, closed=True)
            c.fill(smooth([(sx * hr * 0.45, hy + hr * 0.72, "s"), (sx * hr * 0.86, hy + hr * 1.1, "s"), (sx * hr * 0.86, hy + hr * 0.5, "s")], n=3),
                   zone=2, alpha=0.9)
    elif ears == "long":
        for sx in (-1, 1):
            e = ell(sx * hr * 0.4, hy + hr * 1.35, hr * 0.26, hr * 0.8, 32)
            c.fill(e, zone=1)
            c.line(e, INNER, zone=0, closed=True)
            c.fill(ell(sx * hr * 0.4, hy + hr * 1.3, hr * 0.13, hr * 0.6, 24), zone=2)
    elif ears == "horns":
        for sx in (-1, 1):
            hn = smooth([(sx * hr * 0.28, hy + hr * 0.78, "s"), (sx * hr * 0.5, hy + hr * 1.12, "s"), (sx * hr * 0.52, hy + hr * 0.74, "s")], n=3)
            c.fill(hn, zone=2)
            c.line(hn, INNER, zone=0, closed=True)
    # Kopf
    head = ell(0, hy, hr, hr * 0.92, 64)
    shaded(c, head, 1, "bottom", 0.9, 0.24)
    if ears == "flop":
        for sx in (-1, 1):
            e = smooth([(sx * hr * 0.55, hy + hr * 0.75), (sx * hr * 1.15, hy + hr * 0.45), (sx * hr * 1.12, hy - hr * 0.45),
                        (sx * hr * 0.9, hy - hr * 0.55), (sx * hr * 0.72, hy + hr * 0.1)])
            c.fill(e, zone=1, shade=0.78)
            c.line(e, INNER, zone=0, closed=True)
    c.fill(ell(0, hy - hr * 0.38, hr * 0.46, hr * 0.32, 40), zone=2)             # Schnauze
    c.fill(ell(0, hy - hr * 0.22, hr * 0.14, hr * 0.1, 20), zone=0)              # Nase
    c.fill(ell(-hr * 0.04, hy - hr * 0.18, hr * 0.05, hr * 0.03, 12), zone=2, shade=1.2)
    smile(c, 0, hy - hr * 0.44, hr * 0.13)
    collar(c, 0, hy - hr * 0.97, bw * 1.0, 4.0)                                # unter dem Kinn sichtbar
    for sx in (-1, 1):
        eye(c, sx * hr * 0.42, hy + hr * 0.08, hr * 0.17)
        if whiskers:
            for dy in (0.0, -0.1):
                c.line([(sx * hr * 0.42, hy - hr * (0.36 - dy)), (sx * hr * 0.98, hy - hr * (0.3 - dy * 2))], INNER * 0.7, zone=0)


# ------------------------------------------------------------------ Nager (Hamster, Meerschweinchen)
def rodent(p: Pet, long: bool = False):
    c, W, H = p.c, p.w, p.h
    bw = W * 0.46
    body = smooth([(-bw, 8), (-bw * 0.9, 55), (-bw * 0.45, 88), (bw * 0.2, 95), (bw * 0.8, 72), (bw, 30), (bw * 0.8, 2), (-bw * 0.8, 2)])
    cl = shaded(c, body, 1, "bottom", 0.88, 0.25)
    c.fill(ell(bw * 0.1, 28, bw * 0.6, 26, 40), zone=2, clip=cl)
    fx = bw * (0.45 if long else 0.25)
    for sx in (-1, 1):
        ex = fx + sx * bw * 0.32 - bw * 0.05
        e = ell(ex, 90, 9, 8, 24)
        c.fill(e, zone=1)
        c.line(e, INNER, zone=0, closed=True)
        c.fill(ell(ex, 90, 4.5, 4, 16), zone=3, alpha=0.6)
    for sx in (-1, 1):
        eye(c, fx + sx * bw * 0.26, 64, 6.5)
        c.fill(ell(fx + sx * bw * 0.42, 50, 9, 7, 24), zone=2, alpha=0.85)     # Pausbacken
    c.fill(ell(fx, 52, 3, 2.2, 16), zone=3)
    smile(c, fx, 46, 3)
    for sx in (-1, 1):
        for dy in (0, -3):
            c.line([(fx + sx * 5, 50 + dy), (fx + sx * 18, 52 + dy * 1.6)], INNER * 0.7, zone=0)
        c.fill(ell(fx + sx * 9, 4, 6, 4, 20), zone=2)
        c.line(ell(fx + sx * 9, 4, 6, 4, 20), INNER, zone=0, closed=True)


# ------------------------------------------------------------------ Vogel, Fisch, Schildkröte
def bird(p: Pet):
    c, W, H = p.c, p.w, p.h
    for x in (-6, 6):
        c.line([(x, 0), (x, 12)], 2.0, zone=3, shade=0.8)
        c.line([(x - 4, 0.5), (x + 4, 0.5)], 1.6, zone=3, shade=0.8)
    tail = smooth([(-W * 0.2, 30), (-W * 0.62, 12, "s"), (-W * 0.48, 34)])
    c.fill(tail, zone=1, shade=0.8)
    c.line(tail, INNER, zone=0, closed=True)
    body = smooth([(-W * 0.42, 40), (-W * 0.3, 80), (0, 97), (W * 0.36, 86), (W * 0.46, 55), (W * 0.3, 16), (-W * 0.2, 12)])
    cl = shaded(c, body, 1, "bottom", 0.88, 0.25)
    c.fill(ell(W * 0.05, 34, W * 0.3, 24, 40), zone=2, clip=cl)
    wing = smooth([(-W * 0.32, 60), (-W * 0.05, 66), (W * 0.1, 50), (-W * 0.06, 30), (-W * 0.36, 34)])
    c.fill(wing, zone=1, shade=0.8, clip=cl)
    c.line(wing, INNER, zone=0, closed=True)
    beak = smooth([(W * 0.4, 72, "s"), (W * 0.62, 66, "s"), (W * 0.4, 60, "s")], n=2)
    c.fill(beak, zone=3)
    c.line(beak, INNER, zone=0, closed=True)
    eye(c, W * 0.2, 74, 7.5)
    c.fill(smooth([(W * 0.0, 96), (W * 0.06, 106), (W * 0.12, 95)]), zone=1)


def fish(p: Pet):
    c, W, H = p.c, p.w, p.h
    tail = smooth([(-W * 0.26, 50), (-W * 0.5, 90, "s"), (-W * 0.42, 50), (-W * 0.5, 10, "s")], n=3)
    c.fill(tail, zone=1, shade=0.85)
    c.line(tail, INNER, zone=0, closed=True)
    body = smooth([(-W * 0.3, 50), (-W * 0.05, 92), (W * 0.3, 85), (W * 0.48, 50), (W * 0.3, 15), (-W * 0.05, 8)])
    cl = shaded(c, body, 1, "bottom", 0.86, 0.3)
    for x in (-W * 0.05, W * 0.12):
        c.fill(smooth([(x - 4, 95), (x + 6, 50), (x - 4, 5), (x + 4, 5), (x + 14, 50), (x + 4, 95)]), zone=2, clip=cl)
    c.fill(smooth([(W * 0.0, 88), (W * 0.1, 100), (W * 0.2, 86)]), zone=3)
    eye(c, W * 0.3, 58, 10)
    smile(c, W * 0.4, 36, 4)


def turtle(p: Pet):
    c, W, H = p.c, p.w, p.h
    for x in (-W * 0.3, W * 0.22):
        c.fill(rrect(x - 7, 0, x + 7, 30, 6), zone=2, shade=0.9)
        c.line(rrect(x - 7, 0, x + 7, 30, 6), INNER, zone=0, closed=True)
    head = ell(W * 0.36, 52, 19, 21, 40)
    shaded(c, head, 2, "bottom", 0.9, 0.3)
    eye(c, W * 0.4, 58, 6.5)
    smile(c, W * 0.43, 44, 3.5)
    shell = smooth([(-W * 0.46, 22, "s"), (W * 0.32, 22, "s"), (W * 0.26, 70), (0, 96), (-W * 0.32, 72)])
    cl = shaded(c, shell, 1, "bottom", 0.84, 0.3)
    c.fill(rrect(-W * 0.48, 16, W * 0.34, 26, 5), zone=3)
    c.line(rrect(-W * 0.48, 16, W * 0.34, 26, 5), INNER, zone=0, closed=True)
    for cx, cy in ((-W * 0.08, 60), (-W * 0.26, 42), (W * 0.1, 42)):
        hexa = [(cx + 10 * __import__("math").cos(a * 1.0472), cy + 10 * __import__("math").sin(a * 1.0472)) for a in range(6)]
        c.fill(hexa, zone=1, shade=1.08, clip=cl)
        c.line(hexa, INNER, zone=0, closed=True, clip=cl)


# ------------------------------------------------------------------ stehend (Pony, Einhorn)
def standing(p: Pet, horn: bool = False):
    c, W, H = p.c, p.w, p.h
    by = 38
    tail = smooth([(-W * 0.36, by + 18), (-W * 0.5, by + 4), (-W * 0.48, by - 26), (-W * 0.38, by - 30), (-W * 0.4, by)])
    c.fill(tail, zone=3)
    c.line(tail, INNER, zone=0, closed=True)
    legs = [(-W * 0.28, 0.82), (W * 0.08, 0.82), (-W * 0.2, 1.0), (W * 0.16, 1.0)]
    for x, sh in legs[:2]:
        c.fill(rrect(x - 5.5, 4, x + 5.5, by, 4), zone=1, shade=sh)
        c.line(rrect(x - 5.5, 4, x + 5.5, by, 4), INNER, zone=0, closed=True)
        c.fill(rrect(x - 6, 0, x + 6, 7, 2.5), zone=2, shade=0.8)
    body = ell(-W * 0.06, by + 10, W * 0.33, 22, 48)
    shaded(c, body, 1, "bottom", 0.88, 0.3)
    for x, sh in legs[2:]:
        c.fill(rrect(x - 5.5, 4, x + 5.5, by, 4), zone=1, shade=sh)
        c.line(rrect(x - 5.5, 4, x + 5.5, by, 4), INNER, zone=0, closed=True)
        c.fill(rrect(x - 6, 0, x + 6, 7, 2.5), zone=2)
        c.line(rrect(x - 6, 0, x + 6, 7, 2.5), INNER, zone=0, closed=True)
    neck = smooth([(W * 0.06, by + 18), (W * 0.16, by + 44), (W * 0.32, by + 42), (W * 0.26, by + 8)])
    c.fill(neck, zone=1)
    hx, hy = W * 0.29, H - 26
    ear = smooth([(hx - 12, hy + 17, "s"), (hx - 9, hy + 31, "s"), (hx - 2, hy + 20, "s")], n=3)
    c.fill(ear, zone=1)
    c.line(ear, INNER, zone=0, closed=True)
    head = ell(hx, hy, 24, 22, 48)
    shaded(c, head, 1, "bottom", 0.9, 0.26)
    c.fill(ell(hx + 15, hy - 9, 13, 10.5, 32), zone=2)
    c.fill(ell(hx + 20, hy - 7, 1.8, 1.4, 12), zone=0)
    smile(c, hx + 16, hy - 13, 3.5)
    eye(c, hx + 2, hy + 3, 6.5)
    mane = smooth([(hx - 14, hy + 20), (hx + 2, hy + 23), (hx - 6, hy + 10), (hx - 16, hy - 2), (W * 0.1, by + 34), (W * 0.0, by + 18),
                   (W * 0.12, by + 22), (hx - 24, hy + 4)])
    c.fill(mane, zone=3)
    c.line(mane, INNER, zone=0, closed=True)
    if horn:
        hn = smooth([(hx - 2, hy + 19, "s"), (hx + 4, hy + 40, "s"), (hx + 7, hy + 18, "s")], n=3)
        c.fill(hn, zone=2, shade=1.05)
        c.line(hn, INNER, zone=0, closed=True)
        for k in range(3):
            y = hy + 23 + k * 5
            c.line([(hx - 0.5 + k * 0.9, y), (hx + 6 - k * 0.5, y + 2)], INNER * 0.8, zone=0, shade=1.0)
