"""Bereichs-Symbole für die Stadtkarte (Gebäude/Szenen als kleine Embleme) im Stil C."""
from __future__ import annotations

import math

from .base import Icon, band, circle, ell, gloss, rrect, shaded, smooth, trap


def _house(i: Icon, wall: str, roof: str, door: str = "wood", w: float = 10, h: float = 8, roof_h: float = 7):
    c = i.layer(wall, roof, door)
    shaded(c, rrect(-w, -12, w, -12 + h * 2, 0.8), 1, "right", 0.86, 0.25)
    c.fill(smooth([(-w - 2.5, -12 + h * 2 - 0.5, "s"), (w + 2.5, -12 + h * 2 - 0.5, "s"), (0, -12 + h * 2 + roof_h, "s")], n=2),
           zone=2)
    c.line(smooth([(-w - 2.5, -12 + h * 2 - 0.5, "s"), (w + 2.5, -12 + h * 2 - 0.5, "s"), (0, -12 + h * 2 + roof_h, "s")], n=2),
           0.38, zone=0, closed=True)
    return c


def area_home(i: Icon):
    c = _house(i, "cream", "red", "wood")
    c.fill(rrect(-3, -12, 3, -3, 2.6), zone=3)
    c.fill(circle(1.6, -7.5, 0.5, 12), zone=0)
    for x in (-7.5, 5):
        c.fill(rrect(x, -5, x + 3.2, -1.8, 0.6), zone=2, shade=0.5)
    c.fill(rrect(5, 6, 8, 11, 0.4), zone=2, shade=0.8)


def area_hospital(i: Icon):
    c = _house(i, "white", "sky", "sky", w=11, h=9, roof_h=4)
    x = i.layer("red")
    x.fill(rrect(-1.8, -4.5, 1.8, 4.5, 0.6), zone=1)
    x.fill(rrect(-4.5, -1.8, 4.5, 1.8, 0.6), zone=1)
    c.fill(rrect(-2.5, -12, 2.5, -7, 1), zone=3)


def area_school(i: Icon):
    c = _house(i, "yellow", "red", "wood", w=11, h=7.5, roof_h=5)
    c.fill(rrect(-2.5, 3, 2.5, 8, 0.6), zone=1, shade=1.05)
    c.fill(circle(0, 5.5, 1.8), zone=3)
    c.fill(rrect(-2.5, -12, 2.5, -5, 1.4), zone=3)
    for x in (-8.5, 5):
        c.fill(rrect(x, -6, x + 3.5, -2, 0.6), zone=2, shade=0.5)


def area_pool(i: Icon):
    w = i.layer("water", "white")
    shaded(w, rrect(-13, -12, 13, -2, 2.5), 1, "bottom", 0.86, 0.35)
    for y in (-5.5, -9):
        w.fill(band(smooth([(-10, y), (-5, y + 1), (0, y), (5, y + 1), (10, y)], closed=False, n=8), 0.5), zone=2, alpha=0.8)
    r = i.layer("red", "white")
    ring = circle(1, 4.5, 7.2)
    r.fill(ring, zone=2)
    cl = r.mask(ring)
    for k in range(0, 8, 2):
        a0 = k * 45 + 22
        r.fill([(1, 4.5)] + [(1 + 12 * math.cos(math.radians(a)), 4.5 + 12 * math.sin(math.radians(a))) for a in range(a0, a0 + 46, 5)],
               zone=1, clip=cl)
    r.line(ring, 0.38, zone=0, closed=True)
    r.erase(circle(1, 4.5, 3.4))
    r.line(circle(1, 4.5, 3.6), 0.35, zone=0, closed=True)


def area_playground(i: Icon):
    c = i.layer("grey", "orange", "sky")
    for x in (-10, -5):
        c.fill(rrect(x - 0.8, -12, x + 0.8, 8, 0.4), zone=1)
    for y in (-8, -4, 0, 4):
        c.fill(rrect(-10, y - 0.5, -5, y + 0.5, 0.3), zone=1, shade=0.85)
    c.fill(rrect(-11, 7, -4, 9, 0.6), zone=3)
    slide = smooth([(-5, 8), (0, 4), (6, -7), (12, -11), (12, -13.5), (5, -10), (-1, 1), (-5, 5)])
    shaded(c, slide, 2, "bottom", 0.88, 0.3)


def area_fair(i: Icon):
    c = i.layer("grey", "pink", "yellow")
    for sx in (-1, 1):
        c.fill(band([(0, 1), (sx * 7, -13)], 1.0), zone=1)
    c.line(circle(0, 1, 10.5, 64), 1.1, zone=1, closed=True)
    for k in range(8):
        a = 2 * math.pi * k / 8
        c.line([(0, 1), (10.5 * math.cos(a), 1 + 10.5 * math.sin(a))], 0.5, zone=1)
    for k in range(8):
        a = 2 * math.pi * k / 8 + 0.2
        x, y = 10.5 * math.cos(a), 1 + 10.5 * math.sin(a)
        g = i.layer("pink" if k % 2 else "sky", "white")
        g.fill(rrect(x - 2, y - 2.8, x + 2, y, 1), zone=1)
    c.fill(circle(0, 1, 2.2), zone=3)


def area_shop(i: Icon):
    c = i.layer("cream", "wood", "sky")
    shaded(c, rrect(-11, -12, 11, 4, 0.8), 1, "right", 0.86, 0.25)
    c.fill(rrect(-8.5, -9, 1.5, 1, 0.8), zone=3, alpha=0.9)
    c.fill(rrect(4, -12, 8.5, -1, 0.8), zone=2)
    a = i.layer("red", "white")
    for k in range(6):
        x0 = -12.5 + k * 25 / 6
        a.fill(smooth([(x0, 3.5, "s"), (x0 + 25 / 6, 3.5, "s"), (x0 + 25 / 6, 9, "s"), (x0, 9, "s")], n=2),
               zone=1 if k % 2 == 0 else 2)
        a.fill(ell(x0 + 25 / 12, 3.5, 25 / 12, 1.6, 20), zone=1 if k % 2 == 0 else 2)
    a.fill(rrect(-12.5, 9, 12.5, 11, 0.6), zone=1, shade=0.85)


def area_sports(i: Icon):
    c = i.layer("white", "black")
    ball = circle(0, 0, 11.5)
    shaded(c, ball, 1, "bottom", 0.88, 0.3)
    cl = c.mask(ball)
    pent = [(3.6 * math.cos(math.pi / 2 + k * 2 * math.pi / 5), 3.6 * math.sin(math.pi / 2 + k * 2 * math.pi / 5)) for k in range(5)]
    c.fill(pent, zone=2)
    for k in range(5):
        a = math.pi / 2 + k * 2 * math.pi / 5
        cx, cy = 10.5 * math.cos(a), 10.5 * math.sin(a)
        c.fill([(cx + 3.4 * math.cos(a + j * 2 * math.pi / 5), cy + 3.4 * math.sin(a + j * 2 * math.pi / 5)) for j in range(5)],
               zone=2, clip=cl)
        c.line([pent[k], (7.2 * math.cos(a), 7.2 * math.sin(a))], 0.4, zone=0)
    gloss(c, -5, 5.5, 2.2, 1.4, zone=1)


def area_ice(i: Icon):
    c = i.layer("white", "sky", "grey")
    boot = smooth([(-8, -5, "s"), (9, -5, "s"), (10, -1), (5, 1), (3, 11, "s"), (-7, 11, "s")])
    shaded(c, boot, 1, "right", 0.86, 0.28)
    c.fill(rrect(-7.5, 8.5, 3.5, 11, 0.8), zone=2)
    for k in range(3):
        c.fill(band([(-4 + k * 0.2, 6.5 - k * 3), (1 + k * 0.4, 6.8 - k * 3)], 0.45), zone=2)
    c.fill(rrect(-10, -11, 12, -9, 1), zone=3)
    for x in (-5, 5):
        c.fill(rrect(x - 0.8, -9.5, x + 0.8, -5, 0.3), zone=3)


def area_flower(i: Icon):
    pot = i.layer("coral", "brown")
    shaded(pot, trap(-5.5, 5.5, -12, -7, 7, -4, 0.8), 1, "right", 0.86, 0.3)
    pot.fill(rrect(-7.8, -5, 7.8, -2.5, 0.8), zone=1, shade=1.05)
    st = i.layer("leaf")
    st.fill(band([(0, -3), (0, 4)], 0.8), zone=1)
    for sx in (-1, 1):
        st.fill(smooth([(0, -1), (sx * 5, 1.5), (sx * 6.5, -1), (sx * 3, -2.5)]), zone=1)
    f = i.layer("pink", "yellow")
    for k in range(6):
        a = 2 * math.pi * k / 6
        f.fill(circle(3.8 * math.cos(a), 7 + 3.8 * math.sin(a), 2.9), zone=1)
    f.fill(circle(0, 7, 2.4), zone=2)


def area_zoo(i: Icon):
    c = i.layer("yellow", "wood", "brown")
    c.fill(band(smooth([(-1, -13), (0, -2), (2, 5)], closed=False), 3.2), zone=1)
    head = smooth([(-2, 3), (4, 9), (12, 7.5), (12.5, 4), (6, 2), (1, -1)])
    shaded(c, head, 1, "bottom", 0.9, 0.3)
    for x, y in ((-1.5, -9), (1, -4), (-0.5, 0.5), (4, 5.5), (8, 5.5)):
        c.fill(ell(x, y, 1.3, 1.0, 16), zone=2)
    for x in (2.5, 5):
        c.fill(rrect(x - 0.5, 8.5, x + 0.5, 12, 0.4), zone=3)
        c.fill(circle(x, 12, 1), zone=3)
    c.fill(circle(6.5, 6.8, 0.8), zone=0)
    c.fill(band(smooth([(-2.5, 2), (-4, -4), (-3, -11)], closed=False), 0.9), zone=3)


def area_workshop(i: Icon):
    h = i.layer("wood", "grey")
    h.fill(band([(-9, -10), (3, 5)], 1.5), zone=1)
    h.fill(smooth([(0, 3, "s"), (7, 10, "s"), (9.5, 7.5, "s"), (3, 0, "s")], n=2), zone=2)
    w = i.layer("grey", "white")
    w.fill(band([(9, -10), (-3, 2)], 1.9), zone=1)
    w.fill(circle(-5, 4, 4.4), zone=1)
    w.erase(smooth([(-6, 3, "s"), (-9, 9, "s"), (-11, 6, "s")], n=2))


def car(i: Icon):
    c = i.layer("red", "sky", "dark")
    body = smooth([(-13, -5, "s"), (13, -5, "s"), (13, 1), (8, 2.5), (5, 8, "s"), (-6, 8, "s"), (-9, 2.5), (-13, 1)])
    shaded(c, body, 1, "bottom", 0.86, 0.3)
    c.fill(smooth([(-5.5, 2.5, "s"), (4.5, 2.5, "s"), (3.5, 6.8, "s"), (-4.5, 6.8, "s")], n=2), zone=2)
    for x in (-7, 7):
        c.fill(circle(x, -5, 3.3), zone=3)
        c.fill(circle(x, -5, 1.3), zone=2, shade=0.5)


def area_forest(i: Icon):
    for x, h, s in ((-6, 22, 0.85), (5, 26, 1.0)):
        t = i.layer("green", "brown")
        t.fill(rrect(x - 1.2, -13, x + 1.2, -8, 0.4), zone=2)
        for k in range(3):
            y0 = -9 + k * h * 0.22
            w = 8 - k * 2.2
            t.fill(smooth([(x - w, y0, "s"), (x + w, y0, "s"), (x, y0 + h * 0.34, "s")], n=2), zone=1, shade=s - k * 0.03)
            t.line(smooth([(x - w, y0, "s"), (x + w, y0, "s"), (x, y0 + h * 0.34, "s")], n=2), 0.35, zone=0, closed=True)
    m = i.layer("red", "white", "cream")
    m.fill(rrect(-1.2, -13, 1.2, -9, 0.8), zone=3)
    m.fill(smooth([(-4.5, -9.2, "s"), (4.5, -9.2, "s"), (3, -6.5), (0, -5.3), (-3, -6.5)]), zone=1)
    for x, y in ((-2, -7.4), (1.6, -6.6), (3, -8.4)):
        m.fill(circle(x, y, 0.7, 12), zone=2)


def area_camping(i: Icon):
    c = i.layer("orange", "cream", "brown")
    tent = smooth([(-13, -11, "s"), (13, -11, "s"), (0, 10, "s")], n=2)
    shaded(c, tent, 1, "right", 0.86, 0.35)
    c.fill([(-4, -11), (4, -11), (0, 1)], zone=0, alpha=0.8)
    c.fill([(0.5, -11), (4, -11), (0.5, 0.6)], zone=2)
    c.line([(0, 10), (0, 13)], 0.5, zone=3)
    c.fill([(0, 13), (4, 12), (0, 11)], zone=1)


def area_hair(i: Icon):
    s = i.layer("grey", "pink")
    for sx, ang in ((-1, 35), (1, -35)):
        a = math.radians(90 + ang)
        s.fill(band([(0, 0), (sx * 9, 11)], 1.2), zone=1)
        s.fill(circle(-sx * 5.5, -7.5, 3.6), zone=2)
        s.erase(circle(-sx * 5.5, -7.5, 1.8))
        s.fill(band([(0, 0), (-sx * 3.8, -4.8)], 1.1), zone=2)
    s.fill(circle(0, 0, 1), zone=1, shade=0.7)


def area_bike(i: Icon):
    c = i.layer("teal", "dark", "grey")
    for x in (-7.5, 7.5):
        c.line(circle(x, -4, 5, 40), 1.1, zone=2, closed=True)
        c.fill(circle(x, -4, 1), zone=3)
    frame = [(-7.5, -4), (-1, -4), (5, 4), (-3.5, 4), (-7.5, -4)]
    c.line(frame, 1.1, zone=1)
    c.line([(-1, -4), (-3.5, 6)], 1.1, zone=1)
    c.line([(5, 4), (7.5, -4)], 1.1, zone=1)
    c.line([(5, 4), (6, 8)], 1.0, zone=1)
    c.fill(rrect(4, 7.4, 9, 9, 0.6), zone=2)
    c.fill(rrect(-6, 6, -1.5, 7.6, 0.8), zone=2)
