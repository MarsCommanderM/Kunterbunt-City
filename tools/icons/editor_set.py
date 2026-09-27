"""Editor-Kategorien (Kleidung, Frisur, Gesicht …) und Tier-Symbole im Stil C."""
from __future__ import annotations

import math

from .base import Icon, band, circle, ell, gloss, rrect, shaded, smooth, trap


# ------------------------------------------------------------------ Figur & Kleidung
def shirt(i: Icon):
    c = i.layer("teal", "cream", "yellow")
    pts = smooth([(-6, -11, "s"), (6, -11, "s"), (6, 3, "s"), (9, 1, "s"), (12.5, 5.5, "s"), (6.5, 10.5, "s"), (3, 10.5, "s"),
                   (0, 8), (-3, 10.5, "s"), (-6.5, 10.5, "s"), (-12.5, 5.5, "s"), (-9, 1, "s"), (-6, 3, "s")], n=3)
    shaded(c, pts, 1, "right", 0.86, 0.25)
    c.fill(band(smooth([(-3, 10.2), (0, 7.4), (3, 10.2)], closed=False), 0.9), zone=2)
    s = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        r = 4.2 if k % 2 == 0 else 1.9
        s.append((r * math.cos(a), -2 + r * math.sin(a)))
    c.fill(s, zone=3)
    c.line(s, 0.3, zone=0, closed=True)


def pants(i: Icon):
    c = i.layer("navy", "wood", "sky")
    pts = [(-8, 11), (8, 11), (9.5, -12), (2.5, -12), (0, 1), (-2.5, -12), (-9.5, -12)]
    shaded(c, smooth([(x, y, "s") for x, y in pts], n=2), 1, "right", 0.86, 0.25)
    c.fill(rrect(-8.2, 8, 8.2, 11, 0.6), zone=2)
    c.fill(rrect(-1, 8.3, 1, 10.7, 0.4), zone=3)
    for sx in (-1, 1):
        c.line(smooth([(sx * 7.6, 7.5), (sx * 4.6, 4.5), (sx * 2.5, 7.5)], closed=False), 0.35, zone=0)


def shoe(i: Icon):
    c = i.layer("pink", "white", "yellow")
    body = smooth([(-12, -5, "s"), (12, -5, "s"), (12.5, 0), (8, 3), (1, 4.5), (-3, 9), (-9, 9, "s"), (-12, 4)])
    shaded(c, body, 1, "bottom", 0.88, 0.3)
    c.fill(rrect(-12.5, -8.5, 12.8, -4.5, 1.8), zone=2)
    c.line([(-12, -6.5), (12.5, -6.5)], 0.3, zone=0)
    for k in range(3):
        c.fill(band([(-2 + k * 2.6, 6 - k * 0.9), (0.6 + k * 2.6, 3.8 - k * 0.9)], 0.55), zone=3)


def hair(i: Icon):
    c = i.layer("skin", "brown", "rose")
    c.fill(smooth([(-11, 2), (-10.5, -9), (-6, -12), (-7, 0)]), zone=2)       # Haar hinten links
    c.fill(smooth([(11, 2), (10.5, -9), (6, -12), (7, 0)]), zone=2)
    shaded(c, circle(0, -1, 8.5), 1, "right", 0.9, 0.25)
    c.fill(smooth([(-10, 0), (-9.5, 8), (-3, 12), (5, 11.5), (10, 6), (10, 0), (6, 4.5), (1, 3), (-4, 5)]), zone=2)
    for sx in (-1, 1):
        c.fill(ell(sx * 5, -4, 1.6, 1.0, 16), zone=3, alpha=0.8)
    gloss(c, -4, 9, 2.6, 1, zone=1)


def eye(i: Icon):
    c = i.layer("white", "sky", "white")
    lid = smooth([(-12, 0, "s"), (-5, 6.5), (5, 6.5), (12, 0, "s"), (5, -6.5), (-5, -6.5)])
    c.fill(lid, zone=1)
    cl = c.mask(lid)
    c.fill(circle(0, 0, 5.4), zone=2, clip=cl)
    c.fill(circle(0, 0, 2.6), zone=0, clip=cl)
    c.fill(circle(-1.6, 1.8, 1.2), zone=3, clip=cl)
    c.line(lid, 0.6, zone=0, closed=True)
    for k in (-1, 0, 1):
        c.fill(band([(k * 4, 6.4 - abs(k) * 0.6), (k * 5.5, 10 - abs(k))], 0.5), zone=0)


def mouth(i: Icon):
    c = i.layer("red", "pink", "white")
    m = smooth([(-11, 3, "s"), (0, 2), (11, 3, "s"), (6, -6), (0, -8), (-6, -6)])
    shaded(c, m, 1, "bottom", 0.85, 0.3)
    cl = c.mask(m)
    c.fill(rrect(-7, 0, 7, 3.5, 1), zone=3, clip=cl)
    c.fill(ell(0, -5.5, 4.5, 2.6, 24), zone=2, clip=cl)


def bow(i: Icon):
    c = i.layer("pink", "rose")
    for sx in (-1, 1):
        wing = smooth([(0, 0), (sx * 7, 7.5), (sx * 12.5, 5), (sx * 12.5, -5), (sx * 7, -7.5)])
        shaded(c, wing, 1, "bottom", 0.86, 0.35)
        c.fill(smooth([(sx * 2, 0), (sx * 7, 3.5), (sx * 9, 0), (sx * 7, -3.5)]), zone=2)
    c.fill(rrect(-2.8, -3.4, 2.8, 3.4, 1.4), zone=1, shade=0.94)
    c.line(rrect(-2.8, -3.4, 2.8, 3.4, 1.4), 0.35, zone=0, closed=True)


def glasses(i: Icon):
    c = i.layer("lilac", "sky", "white")
    for sx in (-1, 1):
        c.fill(rrect(sx * 7 - 5.5, -4.5, sx * 7 + 5.5, 4.5, 3.2), zone=1)
        c.fill(rrect(sx * 7 - 4, -3, sx * 7 + 4, 3, 2), zone=2, alpha=0.95)
        c.fill(band([(sx * 7 - 2.5, 1.5), (sx * 7 - 0.5, -0.5)], 0.5), zone=3)
    c.fill(band(smooth([(-1.6, 1), (0, 2.4), (1.6, 1)], closed=False), 0.8), zone=1)


def person(i: Icon):
    c = i.layer("orange", "skin", "brown")
    shaded(c, smooth([(-10, -13, "s"), (10, -13, "s"), (9, -5), (4, -2.5), (-4, -2.5), (-9, -5)]), 1, "right", 0.86, 0.25)
    c.fill(circle(0, 4.5, 7.5), zone=2)
    c.fill(smooth([(-8, 4), (-7.5, 10), (-2, 13), (4, 12.5), (8, 9), (8, 4), (4, 8), (-3, 8)]), zone=3)
    for sx in (-1, 1):
        c.fill(ell(sx * 2.6, 3.2, 0.9, 1.2, 16), zone=0)
    c.line(smooth([(-2, 0.6), (0, -0.5), (2, 0.6)], closed=False), 0.45, zone=0)


def hand(i: Icon):
    c = i.layer("skin", "rose")
    pts = []
    for k, (x, h) in enumerate(((-8.5, 3), (-4.5, 9), (0, 11), (4.5, 9.5))):
        c.fill(rrect(x - 2, -2, x + 2, h, 2), zone=1)
    palm = smooth([(-10.5, -1), (7, -1), (7, -8), (2, -12.5), (-6, -12.5), (-10, -8)])
    shaded(c, palm, 1, "right", 0.9, 0.3)
    c.fill(smooth([(6, -6), (12, 1), (10, 3), (4, -2)]), zone=1)
    for x in (-8.5, -4.5, 0, 4.5):
        c.line([(x - 2, -1), (x + 2, -1)], 0.3, zone=0, alpha=0.4)


def paw(i: Icon):
    c = i.layer("brown", "rose")
    c.fill(smooth([(-7, -4), (0, -1), (7, -4), (8, -10), (0, -12), (-8, -10)]), zone=1)
    c.fill(smooth([(-5, -6), (0, -4), (5, -6), (4, -9.5), (-4, -9.5)]), zone=2)
    for x, y in ((-9, 2), (-3.5, 6.5), (3.5, 6.5), (9, 2)):
        c.fill(ell(x, y, 2.9, 3.6, 24), zone=1)
        c.fill(ell(x, y - 0.5, 1.6, 2.1, 16), zone=2)


# ------------------------------------------------------------------ Tiere (Gesichter)
def _face(i: Icon, fur: str, second: str, ears: str, snout: bool = True, whiskers: bool = False, nose: str = "pink"):
    c = i.layer(fur, second, nose)
    if ears == "flop":
        for sx in (-1, 1):
            c.fill(smooth([(sx * 7, 7), (sx * 13, 3), (sx * 12, -6), (sx * 8, -2)]), zone=2)
    elif ears == "point":
        for sx in (-1, 1):
            c.fill(smooth([(sx * 3, 8, "s"), (sx * 10, 12.5, "s"), (sx * 10, 2, "s")], n=2), zone=1)
            c.fill(smooth([(sx * 5, 7.5, "s"), (sx * 9, 10.5, "s"), (sx * 9, 4, "s")], n=2), zone=3, alpha=0.7)
    elif ears == "long":
        for sx in (-1, 1):
            c.fill(ell(sx * 4, 10, 2.8, 6.5, 24), zone=1)
            c.fill(ell(sx * 4, 10, 1.4, 4.5, 16), zone=3, alpha=0.7)
    elif ears == "round":
        for sx in (-1, 1):
            c.fill(circle(sx * 7.5, 7, 3.4), zone=1)
            c.fill(circle(sx * 7.5, 7, 1.8), zone=3, alpha=0.7)
    head = ell(0, -1, 10.5, 9.5, 48)
    shaded(c, head, 1, "bottom", 0.9, 0.25)
    if snout:
        c.fill(ell(0, -5, 5.2, 3.8, 32), zone=2)
    for sx in (-1, 1):
        c.fill(ell(sx * 4.2, 0.5, 1.4, 1.9, 16), zone=0)
        c.fill(circle(sx * 4.2 - 0.4, 1.2, 0.5, 12), zone=2)
    c.fill(ell(0, -3.4, 1.8, 1.2, 16), zone=3)
    c.line(smooth([(-2.2, -5.3), (-1.1, -6.5), (0, -5.4), (1.1, -6.5), (2.2, -5.3)], closed=False), 0.4, zone=0)
    if whiskers:
        for sx in (-1, 1):
            for dy in (0, -1.6):
                c.line([(sx * 4.5, -4.5 + dy), (sx * 10, -3.5 + dy * 1.5)], 0.3, zone=0)
    return c


def dog(i: Icon):
    _face(i, "wood", "cream", "flop", nose="black")


def cat(i: Icon):
    _face(i, "orange", "cream", "point", whiskers=True)


def bunny(i: Icon):
    _face(i, "cream", "white", "long", whiskers=True)


def hamster(i: Icon):
    _face(i, "sand", "white", "round", whiskers=True)


def bird(i: Icon):
    c = i.layer("sky", "yellow", "white")
    body = smooth([(-10, -2), (-6, 8), (4, 10), (10, 4), (9, -6), (2, -10), (-7, -8)])
    shaded(c, body, 1, "bottom", 0.88, 0.3)
    c.fill(smooth([(-6, -1), (0, 2), (4, -4), (-2, -6)]), zone=1, shade=0.8)
    c.fill([(9.5, 3), (14, 1), (9.5, -1)], zone=2)
    c.fill(circle(4.5, 4, 1.4), zone=0)
    c.fill(circle(4.1, 4.5, 0.45, 12), zone=3)
    c.fill(smooth([(-10, 0), (-14, 3), (-13.5, -2)]), zone=1, shade=0.8)


def fish(i: Icon):
    c = i.layer("orange", "white", "yellow")
    body = smooth([(-8, 0), (0, 7.5), (8, 5), (11, 0), (8, -5), (0, -7.5)])
    shaded(c, body, 1, "bottom", 0.86, 0.35)
    c.fill(smooth([(-7, 0, "s"), (-13, 7, "s"), (-12, 0), (-13, -7, "s")], n=2), zone=1, shade=0.9)
    cl = c.mask(body)
    for x in (-2, 2.5):
        c.fill(band(smooth([(x, 7), (x + 1.5, 0), (x, -7)], closed=False), 1.0), zone=2, clip=cl)
    c.fill(circle(6, 1.5, 1.4), zone=0)
    c.fill(circle(5.6, 2, 0.45, 12), zone=2)
