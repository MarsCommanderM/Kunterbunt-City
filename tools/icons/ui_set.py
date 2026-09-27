"""UI-Symbole (Aktionen + Editor-Kategorien) im Stil C. Jede Funktion bekommt ein Icon und malt hinein."""
from __future__ import annotations

import math

from .base import Icon, band, circle, ell, gloss, rrect, shaded, smooth, trap


# ------------------------------------------------------------------ Aktionen
def check(i: Icon):
    c = i.layer("leaf", "white")
    c.fill(band(smooth([(-10, 1), (-4, -6), (10, 9)], closed=False, n=6), 3.2), zone=1)
    c.fill(band([(-8.8, 1.6), (-4, -3.6)], 0.8), zone=2, alpha=0.6)


def close(i: Icon):
    c = i.layer("red", "white")
    for a, b in (((-8, 8), (8, -8)), ((-8, -8), (8, 8))):
        c.fill(band([a, b], 3.1), zone=1)
    c.fill(band([(-7, 6.4), (-4.6, 4)], 0.7), zone=2, alpha=0.6)


def _arrow(i: Icon, sx: int):
    c = i.layer("orange", "white")
    pts = [(-10 * sx, 0), (0, 10), (0, 4.5), (10 * sx, 4.5), (10 * sx, -4.5), (0, -4.5), (0, -10)]
    shaded(c, smooth([(x, y, "s") for x, y in pts], n=2), 1, "bottom", SHADE_B, 0.35)


SHADE_B = 0.86


def back(i: Icon):
    _arrow(i, 1)


def forward(i: Icon):
    _arrow(i, -1)


def undo(i: Icon):
    c = i.layer("lilac", "white")
    arc = [(8 * math.cos(math.radians(a)), -1 + 8 * math.sin(math.radians(a))) for a in range(-150, 91, 10)]
    c.fill(band(arc[::-1], 2.4), zone=1)
    c.fill([(-12.5, 1), (-3.5, 1), (-8, -7)], zone=1)
    c.line([(-12.5, 1), (-3.5, 1), (-8, -7)], 0.3, zone=0, closed=True)


def plus(i: Icon):
    c = i.layer("orange", "yellow", "white")
    shaded(c, circle(0, 0, 12), 1, "bottom", 0.9, 0.3)
    c.fill(rrect(-2.4, -7.5, 2.4, 7.5, 1.4), zone=3)
    c.fill(rrect(-7.5, -2.4, 7.5, 2.4, 1.4), zone=3)
    gloss(c, -6, 6.5, 2.6, 1.5, zone=3)


def trash(i: Icon):
    c = i.layer("grey", "white", "sky")
    shaded(c, trap(-7, 7, -12, -8.5, 8.5, 6, 1.2), 1, "right", 0.85, 0.3)
    for x in (-3.5, 0, 3.5):
        c.fill(rrect(x - 0.7, -9, x + 0.7, 3, 0.6), zone=1, shade=0.72)
    c.fill(rrect(-10, 6, 10, 9, 1.2), zone=1, shade=1.05)
    c.fill(rrect(-3, 9, 3, 11.5, 1), zone=1, shade=0.9)
    c.line(rrect(-10, 6, 10, 9, 1.2), 0.35, zone=0, closed=True)


def copy(i: Icon):
    c = i.layer("sky", "white")
    shaded(c, rrect(-2, -4, 11, 12, 2), 1, "right", 0.85)
    c2 = i.layer("mint", "white")
    shaded(c2, rrect(-11, -12, 3, 5, 2), 1, "right", 0.85)
    for y in (0, -3.5, -7):
        c2.fill(rrect(-8, y - 0.6, 0, y + 0.6, 0.5), zone=2)


def folder(i: Icon):
    c = i.layer("gold", "yellow")
    c.fill(smooth([(-12, -9, "s"), (12, -9, "s"), (12, 7, "s"), (-1, 7, "s"), (-3, 10, "s"), (-12, 10, "s")], n=2), zone=1,
           shade=0.85)
    shaded(c, smooth([(-12.5, -9, "s"), (12.5, -9, "s"), (13.5, 4.5, "s"), (-11.5, 4.5, "s")], n=2), 2, "bottom", 0.88, 0.3)


def gear(i: Icon):
    c = i.layer("grey", "white")
    pts = []
    for k in range(48):
        a = 2 * math.pi * k / 48
        r = 12 if (k // 3) % 2 == 0 else 9.4
        pts.append((r * math.cos(a), r * math.sin(a)))
    shaded(c, pts, 1, "bottom", 0.84, 0.35)
    c.fill(circle(0, 0, 3.8), zone=2)
    c.line(circle(0, 0, 3.8), 0.35, zone=0, closed=True)


def map_(i: Icon):
    c = i.layer("cream", "leaf", "water")
    w = [(-12, -9), (-4, -11), (4, -9), (12, -11), (12, 9), (4, 11), (-4, 9), (-12, 11)]
    c.fill(w, zone=1)
    cl = c.mask(w)
    c.fill(smooth([(-12, -2), (-6, 2), (0, -3), (5, 3), (12, 0), (12, -12), (-12, -12)]), zone=2, clip=cl)
    c.fill(band(smooth([(-12, 6), (-3, 3), (4, 7), (12, 5)], closed=False, n=8), 1.2), zone=3, clip=cl)
    for x in (-4, 4):
        c.line([(x, -11 if x < 0 else -9), (x, 9 if x < 0 else 11)], 0.35, zone=0, clip=cl)
    c.line(w, 0.35, zone=0, closed=True)
    p = i.layer("red", "white")
    p.fill(smooth([(6, -1, "s"), (9.5, 5), (6, 8.5), (2.5, 5)]), zone=1)
    p.fill(circle(6, 5, 1.3), zone=2)


def heart(i: Icon):
    c = i.layer("pink", "white")
    pts = smooth([(0, -11, "s"), (11, 0), (10, 8), (5, 10.5), (0, 6.5, "s"), (-5, 10.5), (-10, 8), (-11, 0)])
    shaded(c, pts, 1, "bottom", 0.86, 0.3)
    gloss(c, -5.5, 5.5, 2.4, 1.6)


def star(i: Icon):
    c = i.layer("yellow", "white")
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        r = 12.5 if k % 2 == 0 else 5.6
        pts.append((r * math.cos(a), r * math.sin(a) - 1, "s"))
    shaded(c, smooth(pts, n=2), 1, "bottom", 0.88, 0.35)
    gloss(c, -2.5, 4, 1.6, 1.1)


def speaker(i: Icon, mute: bool = False):
    c = i.layer("grey", "dark")
    shaded(c, smooth([(-11, -4, "s"), (-5, -4, "s"), (2, -10, "s"), (2, 10, "s"), (-5, 4, "s"), (-11, 4, "s")], n=2), 1,
           "bottom", 0.85, 0.3)
    if mute:
        x = i.layer("red")
        for a, b in (((5, 5), (12, -2)), ((5, -2), (12, 5))):
            x.fill(band([a, b], 1.4), zone=1)
        return
    w = i.layer("orange")
    for r in (6.5, 10.5):
        arc = [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a))) for a in range(-45, 46, 9)]
        w.fill(band(arc, 1.25), zone=1)


def mute(i: Icon):
    speaker(i, True)


def palette(i: Icon):
    c = i.layer("wood", "cream")
    pts = smooth([(-12, 0), (-8, 9), (2, 11), (10, 7), (12, -1), (7, -4), (3, -3), (1, -7), (-3, -11), (-9, -8)])
    shaded(c, pts, 1, "bottom", 0.86, 0.3)
    c.erase(circle(3.6, -7.2, 1.8))
    for (x, y, colr) in ((-6, 4, "red"), (0, 7, "yellow"), (6, 4.5, "leaf"), (-7, -3, "sky")):
        d = i.layer(colr, "white")
        d.fill(circle(x, y, 2.4), zone=1)
        gloss(d, x - 0.8, y + 0.8, 0.7, 0.5)


def dice(i: Icon):
    c = i.layer("white", "cream")
    shaded(c, rrect(-10, -10, 10, 10, 3.2), 1, "right", 0.86, 0.28)
    for x, y in ((-5, 5), (0, 0), (5, -5), (5, 5), (-5, -5)):
        c.fill(circle(x, y, 1.9), zone=0)


def magnifier(i: Icon):
    c = i.layer("wood", "sky")
    c.fill(band([(4, -4), (11, -11)], 2.1), zone=1)
    g = i.layer("grey", "sky", "white")
    g.fill(circle(-3, 3, 8.5), zone=1)
    g.fill(circle(-3, 3, 6.3), zone=2, alpha=0.9)
    gloss(g, -5.5, 5.5, 2, 1.3, zone=3)


def lock(i: Icon):
    c = i.layer("grey")
    arc = [(5.5 * math.cos(math.radians(a)), 2 + 6 * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    c.fill(band(arc, 1.4), zone=1)
    b = i.layer("gold", "brown")
    shaded(b, rrect(-9, -11, 9, 3, 2.4), 1, "right", 0.85)
    b.fill(circle(0, -3, 1.8), zone=2)
    b.fill(rrect(-0.8, -8, 0.8, -3, 0.4), zone=2)


def home(i: Icon):
    from .area_set import area_home
    area_home(i)


def brush(i: Icon):
    c = i.layer("wood", "grey", "pink")
    c.fill(band([(-9, -9), (2, 2)], 1.6), zone=1)
    c.fill(band([(1, 1), (4, 4)], 2.2), zone=2)
    c.fill(smooth([(3, 6), (6, 3), (11, 10, "s"), (10, 11, "s")]), zone=3)
    s = i.layer("yellow")
    for x, y in ((-6, 8), (-2, 11), (-9, 3)):
        s.fill([(x, y + 1.6), (x + 0.6, y + 0.6), (x + 1.6, y), (x + 0.6, y - 0.6), (x, y - 1.6), (x - 0.6, y - 0.6),
                (x - 1.6, y), (x - 0.6, y + 0.6)], zone=1)


def pencil(i: Icon):
    c = i.layer("yellow", "skin", "pink")
    body = [(-10, -6), (4, 8), (8, 4), (-6, -10)]
    shaded(c, body, 1, "right", 0.86, 0.35)
    c.fill([(4, 8), (8, 4), (11, 11)], zone=2)
    c.fill([(9.6, 9.6), (11, 11), (10.2, 8.2)], zone=0)
    c.fill(smooth([(-10, -6), (-6, -10), (-9, -13, "s"), (-13, -9, "s")]), zone=3)


def backpack(i: Icon):
    c = i.layer("orange", "yellow", "brown")
    c.fill(band(smooth([(-5, 9), (0, 13), (5, 9)], closed=False), 1.1), zone=3)
    shaded(c, rrect(-9, -12, 9, 10, 4.5), 1, "right", 0.86, 0.3)
    shaded(c, rrect(-6.5, -10, 6.5, -2, 2.4), 2, "bottom", 0.9, 0.35)
    c.fill(rrect(-9, 2, 9, 4, 0.6), zone=3)
    c.fill(rrect(-1.2, 0.8, 1.2, 5.2, 0.6), zone=2)


def album(i: Icon):
    c = i.layer("teal", "white", "sky")
    shaded(c, rrect(-11, -11, 11, 11, 2.2), 1, "right", 0.86, 0.22)
    c.fill(rrect(-11, -11, -8, 11, 1), zone=1, shade=0.72)
    c.fill(rrect(-5.5, -6, 8, 7, 1), zone=2)
    c.fill(smooth([(-4.5, -5), (7, -5), (7, 0), (3, 3), (0, 0), (-4.5, 2)]), zone=3)
    c.fill(circle(4, 4, 1.4), zone=1, shade=1.2)


def camera(i: Icon):
    c = i.layer("dark", "sky", "white")
    c.fill(rrect(-5, 6, 1, 9, 1), zone=1)
    shaded(c, rrect(-12, -8, 12, 7.5, 3), 1, "bottom", 0.84, 0.3)
    c.fill(circle(0, -0.5, 6.2), zone=3)
    c.fill(circle(0, -0.5, 4.2), zone=2)
    c.fill(circle(0, -0.5, 1.8), zone=0)
    gloss(c, -1.6, 1.3, 1, 0.7, zone=3)
    c.fill(rrect(7, 3.5, 10, 5.5, 0.6), zone=3)


def nametag(i: Icon):
    c = i.layer("yellow", "white")
    tag = smooth([(-12, 0, "s"), (-6, 7, "s"), (12, 7, "s"), (12, -7, "s"), (-6, -7, "s")], n=2)
    shaded(c, tag, 1, "bottom", 0.88, 0.3)
    c.erase(circle(-6.5, 0, 1.6))
    for y in (2.5, -2.5):
        c.fill(rrect(-1, y - 0.8, 9, y + 0.8, 0.6), zone=0, alpha=0.5)


def gift(i: Icon):
    c = i.layer("pink", "yellow")
    shaded(c, rrect(-10, -11, 10, 4, 1.5), 1, "right", 0.86)
    c.fill(rrect(-11.5, 3, 11.5, 7.5, 1.4), zone=1, shade=1.04)
    c.fill(rrect(-2, -11, 2, 7.5, 0.4), zone=2)
    for sx in (-1, 1):
        c.fill(smooth([(0, 7.5), (sx * 7, 12), (sx * 8, 8), (sx * 2, 7.5)]), zone=2)


def music(i: Icon):
    c = i.layer("lilac")
    for x, y in ((-7, -8), (6, -5)):
        c.fill(ell(x, y, 3.6, 2.8, 32), zone=1)
    c.fill(rrect(-4.2, -8, -2.4, 9, 0.6), zone=1)
    c.fill(rrect(8.8, -5, 10.6, 12, 0.6), zone=1)
    c.fill([(-4.2, 9), (10.6, 12), (10.6, 8), (-4.2, 5)], zone=1)


def sun(i: Icon):
    c = i.layer("orange", "yellow", "white")
    for k in range(10):
        a = 2 * math.pi * k / 10
        c.fill(band([(8.5 * math.cos(a), 8.5 * math.sin(a)), (12.5 * math.cos(a), 12.5 * math.sin(a))], 1.5), zone=1)
    shaded(c, circle(0, 0, 7.4), 2, "bottom", 0.9, 0.3)
    for sx in (-1, 1):
        c.fill(ell(sx * 2.6, 1.2, 0.8, 1.1, 16), zone=0)
    c.line(smooth([(-2.6, -2), (0, -3.6), (2.6, -2)], closed=False), 0.5, zone=0)


def moon(i: Icon):
    c = i.layer("yellow", "white")
    pts = circle(-1, 0, 11)
    c.fill(pts, zone=1)
    c.erase(circle(5, 4, 9.5))
    s = i.layer("yellow")
    for x, y, r in ((7, -6, 1.8), (10, 3, 1.2)):
        s.fill([(x, y + r * 2), (x + r * 0.5, y + r * 0.5), (x + r * 2, y), (x + r * 0.5, y - r * 0.5), (x, y - r * 2),
                (x - r * 0.5, y - r * 0.5), (x - r * 2, y), (x - r * 0.5, y + r * 0.5)], zone=1)


def wrench(i: Icon):
    c = i.layer("grey", "white")
    c.fill(band([(-8, -8), (5, 5)], 2.2), zone=1)
    head = circle(7, 7, 5.2)
    c.fill(head, zone=1)
    c.erase(smooth([(6, 6, "s"), (9, 13, "s"), (13, 9, "s")], n=2))
    c.fill(circle(-8, -8, 3), zone=1)
    c.erase(circle(-8, -8, 1.2))
    k = i.layer("orange", "white")
    k.fill(trap(-12, -2, -13, -8.6, -5.4, -3, 0.6), zone=1)
    k.fill(rrect(-11, -9.5, -3, -7.5, 0.4), zone=2)


def ball(i: Icon):
    c = i.layer("red", "white", "sky")
    circ = circle(0, 0, 11.5)
    c.fill(circ, zone=2)
    cl = c.mask(circ)
    for k, z in ((0, 1), (2, 3), (4, 1)):
        a0 = k * 60 - 10
        pts = [(0, 0)] + [(20 * math.cos(math.radians(a)), 20 * math.sin(math.radians(a))) for a in range(a0, a0 + 61, 10)]
        c.fill(pts, zone=z, clip=cl)
    c.fill(circ, zone=2, shade=0.85, clip=c.mask(smooth([(-12, -4), (0, -8), (12, -4), (12, -13), (-12, -13)])), alpha=0.5)
    c.line(circ, INNER_W, zone=0, closed=True)
    gloss(c, -5, 5, 2.4, 1.6)


INNER_W = 0.38


def bone(i: Icon):
    c = i.layer("cream", "white")
    pts = smooth([(-8, 3), (-11, 6.5), (-7.5, 9.5), (-5, 6), (5, 6), (7.5, 9.5), (11, 6.5), (8, 3), (8, -3), (11, -6.5),
                   (7.5, -9.5), (5, -6), (-5, -6), (-7.5, -9.5), (-11, -6.5), (-8, -3)])
    shaded(c, pts, 1, "bottom", 0.86, 0.35)


def peek(i: Icon):
    c = i.layer("wood", "brown")
    f = i.layer("skin", "white", "brown")
    f.fill(circle(0, 3, 8.5), zone=1)
    f.fill(smooth([(-8.6, 4), (-6, 11), (0, 12.5), (6, 11), (8.6, 4), (4, 8), (-4, 8)]), zone=3)
    for sx in (-1, 1):
        f.fill(ell(sx * 3.2, 2.5, 1.5, 2.1, 20), zone=0)
        f.fill(circle(sx * 3.2 - 0.4, 3.2, 0.5, 12), zone=2)
    shaded(c, rrect(-13, -12, 13, -0.5, 1.2), 1, "bottom", 0.86, 0.3)
    for x in (-6.5, 0, 6.5):
        c.line([(x, -12), (x, -0.5)], 0.35, zone=0)
    for sx in (-1, 1):
        f2 = i.layer("skin")
        f2.fill(ell(sx * 6, 0, 2.6, 2, 20), zone=1)
