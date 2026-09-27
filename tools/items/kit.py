"""
Werkzeugkasten für Items (P04b-T09): gleiche Tinte, gleiche Kontur, gleiche Schattierung wie die Figuren.

Koordinaten in cm, Ursprung = unten Mitte (Aufstellpunkt), y nach oben.
Farbzonen: 1 = Hauptfarbe (umfärbbar) · 2 = Zweitfarbe (umfärbbar) · 3 = Drittfarbe (Holz, Metall, Erde …).
Jede Zeichen-Funktion bekommt ein `Item` und malt hinein; `finish()` setzt Kontur und schneidet zu.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chibi.vec import ZCanvas, blob, bumpy, path, smooth, sym  # noqa: E402,F401

OUT = 0.5          # Kontur in cm (wie die Figuren)
SHADE = 0.86       # Schattenseite
SOFT = 0.93        # leichter Schatten
DEEP = 0.64        # Linien in der Fläche (Nähte, Fugen, Maserung)
LINE = 0.3         # feine Innenlinie in cm
INNER = 0.3        # Kontur einzelner Bauteile (Polster, Beine, Türen)


class Item:
    """Zeichenfläche für ein Item mit Rand; w/h = gewünschte Welt-Größe in cm."""

    def __init__(self, w: float, h: float, ppc: float = 8.0, margin: float = 6.0):
        self.w, self.h = w, h
        # oben mehr Platz: offene Deckel, Dampf, Flammen ragen über die Grundhöhe (wird danach eng zugeschnitten);
        # höchstens 70 cm, sonst werden große Dinge (Baumhaus 4 m) zu Speicherfressern
        top = max(margin, min(h * 0.8, 70.0))
        self.c = ZCanvas((-w / 2 - margin, -margin, w / 2 + margin, h + top), ppc, outline_cm=OUT)

    def finish(self):
        self.c.outline_under()
        return self.c.render_part((0, self.c.content_bottom_cm()), pad_cm=0.125)


# ------------------------------------------------------------------ Formen
def rrect(x0: float, y0: float, x1: float, y1: float, r: float, n: int = 6) -> list:
    """Abgerundetes Rechteck (Ecken-Radius r)."""
    r = max(0.0, min(r, (x1 - x0) / 2, (y1 - y0) / 2))
    pts = []
    for cx, cy, a0 in ((x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def trap(x0b: float, x1b: float, y0: float, x0t: float, x1t: float, y1: float, r: float = 0.6) -> list:
    """Trapez (unten x0b…x1b, oben x0t…x1t) mit leicht runden Ecken."""
    return smooth([(x0b, y0, "s"), (x1b, y0, "s"), (x1t, y1, "s"), (x0t, y1, "s")], n=2) if r <= 0 else \
        _round_poly([(x0b, y0), (x1b, y0), (x1t, y1), (x0t, y1)], r)


def _round_poly(pts: list, r: float) -> list:
    out = []
    m = len(pts)
    for i in range(m):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % m]
        d0 = math.dist(p0, p1) or 1.0
        d2 = math.dist(p1, p2) or 1.0
        rr = min(r, d0 / 2, d2 / 2)
        a = (p1[0] + (p0[0] - p1[0]) * rr / d0, p1[1] + (p0[1] - p1[1]) * rr / d0)
        b = (p1[0] + (p2[0] - p1[0]) * rr / d2, p1[1] + (p2[1] - p1[1]) * rr / d2)
        for k in range(5):
            t = k / 4
            out.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * p1[0] + t * t * b[0],
                        (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * p1[1] + t * t * b[1]))
    return out


def ell(cx: float, cy: float, rx: float, ry: float, n: int = 48) -> list:
    return blob(cx, cy, rx, ry, n=n)


# ------------------------------------------------------------------ Malen mit Schatten
def shaded(c: ZCanvas, pts: list, zone: int, side: str = "right", amount: float = SHADE, frac: float = 0.28,
           outline: bool = True):
    """Fläche malen + Schattenstreifen an einer Seite (rechts/unten) + feine eigene Kontur – der Stil der Vorlage."""
    c.fill(pts, zone=zone)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    cl = c.mask(pts)
    if side == "right":
        xs0 = x1 - (x1 - x0) * frac
        c.fill([(xs0, y0 - 1), (x1 + 1, y0 - 1), (x1 + 1, y1 + 1), (xs0, y1 + 1)], zone=zone, shade=amount, clip=cl)
    elif side == "bottom":
        ys1 = y0 + (y1 - y0) * frac
        c.fill([(x0 - 1, y0 - 1), (x1 + 1, y0 - 1), (x1 + 1, ys1), (x0 - 1, ys1)], zone=zone, shade=amount, clip=cl)
    if outline:
        c.line(pts, INNER, zone=0, closed=True)
    return cl


def line(c: ZCanvas, pts: list, zone: int = 1, shade: float = DEEP, w: float = LINE, clip=None, closed=False):
    c.line(pts, w, zone=zone, shade=shade, clip=clip, closed=closed)


def knob(c: ZCanvas, x: float, y: float, r: float = 1.2, zone: int = 3):
    c.ellipse(x, y, r, r, zone=zone)
    c.line(blob(x, y, r, r, n=24), 0.25, zone=0, closed=True)


def leg(c: ZCanvas, x: float, y0: float, y1: float, w0: float, w1: float, zone: int = 3):
    """Möbelbein (oben breiter w0, unten w1)."""
    pts = [(x - w0 / 2, y1), (x + w0 / 2, y1), (x + w1 / 2, y0), (x - w1 / 2, y0)]
    c.fill(_round_poly(pts, 0.4), zone=zone)
    c.fill([(x + w1 * 0.1, y1), (x + w0, y1), (x + w1, y0), (x + w1 * 0.1, y0)], zone=zone, shade=SHADE,
           clip=c.mask(_round_poly(pts, 0.4)))
    c.line(_round_poly(pts, 0.4), INNER, zone=0, closed=True)


def grain(c: ZCanvas, x0: float, x1: float, y0: float, y1: float, clip, zone: int = 3, n: int = 3):
    """Holzmaserung: ein paar feine Wellenlinien."""
    for i in range(n):
        y = y0 + (y1 - y0) * (i + 1) / (n + 1)
        pts = [(x0 + (x1 - x0) * k / 8, y + math.sin(k * 1.3 + i) * (y1 - y0) * 0.04) for k in range(9)]
        c.line(pts, 0.22, zone=zone, shade=0.78, clip=clip)


def cushion(c: ZCanvas, x0: float, y0: float, x1: float, y1: float, zone: int = 1, r: float | None = None):
    """Weiches Polster mit Schatten unten und Naht-Linie."""
    rr = r if r is not None else min(x1 - x0, y1 - y0) * 0.35
    pts = rrect(x0, y0, x1, y1, rr)
    c.fill(pts, zone=zone)
    cl = c.mask(pts)
    c.fill(rrect(x0 - 2, y0 - 2, x1 + 2, y0 + (y1 - y0) * 0.3, rr), zone=zone, shade=SOFT, clip=cl)
    c.line(pts, INNER, zone=0, closed=True)
    return cl
