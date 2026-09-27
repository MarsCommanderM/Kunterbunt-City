"""
Pflanzen (P04b-T09): ~35 Arten × Topfformen × Farben → mehrere hundert Pflanzen.
Zonen: 1 = Blattgrün (umfärbbar: hell/dunkel/bunt) · 2 = Topf (umfärbbar) · 3 = Blüte/Frucht (umfärbbar).
Jede Art wird mit festem Zufalls-Samen gezeichnet → bit-genau reproduzierbar, Varianten unterscheiden sich.
"""
from __future__ import annotations

import math
import random

from .kit import DEEP, LINE, SHADE, SOFT, Item, ell, line, rrect, shaded, smooth

POTS = ["terracotta", "round", "cylinder", "bowl", "basket", "square", "stand", "bucket"]


# ------------------------------------------------------------------ Töpfe
def pot_top(style: str, pw: float, ph: float, y0: float = 0.0) -> float:
    """Oberkante des Topfes (ohne zu malen) – dort beginnt die Pflanze."""
    if style == "stand":
        y0 += ph * 0.4
        ph *= 0.6
    if style == "bowl":
        ph *= 0.7
    return y0 + ph


def pot(it: Item, style: str, pw: float, ph: float, y0: float = 0.0) -> float:
    """Topf malen (Zone 2, eigene Kontur), gibt die Erd-Oberkante (y) zurück."""
    c = it.c
    if style == "stand":
        for sx in (-1, 1):
            c.line([(sx * pw * 0.3, y0 + ph * 0.45), (sx * pw * 0.42, y0)], 1.2, zone=2, shade=0.7)
        y0 += ph * 0.4
        ph *= 0.6
    top = y0 + ph
    if style == "stand":          # Topf auf dem Ständer = schlanker Zylinder
        style = "cylinder"
    if style == "terracotta":
        body = [(-pw * 0.36, y0), (pw * 0.36, y0), (pw * 0.46, top - ph * 0.2), (-pw * 0.46, top - ph * 0.2)]
        cl = shaded(c, _r(body), 2, "right", SHADE, 0.3)
        c.line(_r(body), 0.4, zone=0, closed=True)
        rim = rrect(-pw * 0.52, top - ph * 0.24, pw * 0.52, top, 1.2)
        shaded(c, rim, 2, "bottom", SOFT, 0.4)
        c.line(rim, 0.4, zone=0, closed=True)
    elif style == "round":
        body = smooth([(-pw * 0.3, y0 + 0.2), (pw * 0.3, y0 + 0.2), (pw * 0.5, y0 + ph * 0.5), (pw * 0.4, top),
                       (-pw * 0.4, top), (-pw * 0.5, y0 + ph * 0.5)])
        shaded(c, body, 2, "right", SHADE, 0.3)
        c.fill(rrect(-pw * 0.42, top - ph * 0.1, pw * 0.42, top, 0.8), zone=2, shade=SOFT)
        c.line(body, 0.4, zone=0, closed=True)
    elif style == "cylinder":
        body = rrect(-pw * 0.42, y0, pw * 0.42, top, 1.5)
        cl = shaded(c, body, 2, "right", SHADE, 0.3)
        line(c, [(-pw * 0.42, y0 + ph * 0.25), (pw * 0.42, y0 + ph * 0.25)], zone=2, clip=cl, shade=0.8)
        c.line(body, 0.4, zone=0, closed=True)
    elif style == "bowl":
        ph *= 0.7
        top = y0 + ph
        body = smooth([(-pw * 0.25, y0 + 0.2, "s"), (pw * 0.25, y0 + 0.2, "s"), (pw * 0.55, top, "s"), (-pw * 0.55, top, "s")])
        shaded(c, body, 2, "right", SHADE, 0.3)
        c.line(body, 0.4, zone=0, closed=True)
    elif style == "basket":
        body = [(-pw * 0.4, y0), (pw * 0.4, y0), (pw * 0.48, top), (-pw * 0.48, top)]
        cl = shaded(c, _r(body), 2, "right", SHADE, 0.3)
        for k in range(1, 5):
            y = y0 + ph * k / 5
            line(c, [(-pw * 0.5, y), (pw * 0.5, y)], zone=2, clip=cl, shade=0.72)
        for k in range(-4, 5):
            x = k * pw / 10
            line(c, [(x, y0), (x * 1.15, top)], zone=2, clip=cl, shade=0.82)
        c.line(_r(body), 0.4, zone=0, closed=True)
    elif style == "square":
        body = rrect(-pw * 0.44, y0, pw * 0.44, top, 1.2)
        cl = shaded(c, body, 2, "right", SHADE, 0.3)
        c.fill(rrect(-pw * 0.44, top - 1.6, pw * 0.44, top, 0.6), zone=2, shade=1.0, clip=cl)
        c.line(body, 0.4, zone=0, closed=True)
    elif style == "bucket":
        body = [(-pw * 0.38, y0), (pw * 0.38, y0), (pw * 0.47, top), (-pw * 0.47, top)]
        cl = shaded(c, _r(body), 2, "right", SHADE, 0.3)
        for yy in (y0 + ph * 0.18, top - ph * 0.15):
            line(c, [(-pw * 0.5, yy), (pw * 0.5, yy)], zone=2, clip=cl, shade=0.7, w=0.5)
        for sx in (-1, 1):
            c.ellipse(sx * pw * 0.47, top - ph * 0.25, 0.9, 0.9, zone=2, shade=0.7)
        c.line(_r(body), 0.4, zone=0, closed=True)
    return top


def _r(pts):
    from .kit import _round_poly
    return _round_poly(pts, 1.0)


# ------------------------------------------------------------------ Blätter & Blüten
def leaf(c, x, y, length, width, ang, zone=1, shade=1.0, rib=True, split=False, clip=None):
    """Blatt mit Spitze: Ansatz (x,y), Länge, Breite, Winkel (Grad, 90 = nach oben)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (x + ux * length, y + uy * length)
    m1 = (x + ux * length * 0.45 + nx * width / 2, y + uy * length * 0.45 + ny * width / 2)
    m2 = (x + ux * length * 0.45 - nx * width / 2, y + uy * length * 0.45 - ny * width / 2)
    pts = smooth([(x, y, "s"), m1, tip + ("s",), m2], n=10)
    c.fill(pts, zone=zone, shade=shade, clip=clip)
    half = [(x, y), m2, tip]
    c.fill(smooth([(x, y, "s"), (x + ux * length * 0.5, y + uy * length * 0.5), tip + ("s",), m2], n=8), zone=zone,
           shade=shade * 0.9, clip=c.mask(pts))
    if rib:
        c.line([(x, y), (x + ux * length * 0.85, y + uy * length * 0.85)], 0.25, zone=zone, shade=0.6)
    c.line(pts, 0.26, zone=0, closed=True, clip=clip)
    if split:
        for k in (0.35, 0.55, 0.72):
            px, py = x + ux * length * k, y + uy * length * k
            for s in (-1, 1):
                c.erase([(px + nx * s * width * 0.08, py + ny * s * width * 0.08),
                         (px + nx * s * width * 0.6 + ux * 1.6, py + ny * s * width * 0.6 + uy * 1.6),
                         (px + nx * s * width * 0.6 + ux * 2.6, py + ny * s * width * 0.6 + uy * 2.6)])
    return pts


def stem(c, pts, w=0.7, zone=1, shade=0.72):
    c.line(smooth(pts, closed=False, n=10), w, zone=zone, shade=shade)


def flower(c, x, y, r, petals=6, zone=3, center_zone=2, round_=True):
    for k in range(petals):
        a = 2 * math.pi * k / petals
        px, py = x + math.cos(a) * r * 0.62, y + math.sin(a) * r * 0.62
        c.ellipse(px, py, r * 0.48, r * 0.48, zone=zone)
        c.line(ell(px, py, r * 0.48, r * 0.48, 24), 0.22, zone=0, closed=True)
    c.ellipse(x, y, r * 0.36, r * 0.36, zone=center_zone, shade=0.85)
    c.line(ell(x, y, r * 0.36, r * 0.36, 24), 0.22, zone=0, closed=True)


def tulip(c, x, y, r, zone=3):
    pts = smooth([(x - r * 0.8, y + r * 0.9), (x - r * 0.9, y + r * 0.2), (x, y - r * 0.2), (x + r * 0.9, y + r * 0.2),
                   (x + r * 0.8, y + r * 0.9, "s"), (x + r * 0.35, y + r * 0.55), (x, y + r * 1.0, "s"),
                   (x - r * 0.35, y + r * 0.55), (x - r * 0.8, y + r * 0.9, "s")])
    c.fill(pts, zone=zone)
    c.line([(x, y + r * 0.95), (x, y + r * 0.1)], 0.25, zone=zone, shade=0.7)


# ------------------------------------------------------------------ Arten
def plant(it: Item, species: str, pot_style: str = "terracotta", seed: int = 1):
    c, W, H = it.c, it.w, it.h
    rnd = random.Random(hash((species, pot_style, seed)) & 0xFFFFFFFF)
    big = H > 70
    pw = min(W * 0.62, 18 + H * 0.1) if big else W * 0.7
    ph = min(H * (0.3 if big else 0.4), pw * 1.0)
    if pot_style == "stand":
        ph = H * 0.42
    ground = pot_top(pot_style, pw, ph) - 0.6
    top = H
    avail = top - ground

    def fan_leaves(n, lmin, lmax, wfac, spread=70, zone=1, split=False, rib=True):
        for i in range(n):
            t = i / max(1, n - 1)
            ang = 90 + (t - 0.5) * 2 * spread + rnd.uniform(-8, 8)
            ln = rnd.uniform(lmin, lmax)
            leaf(c, rnd.uniform(-pw * 0.12, pw * 0.12), ground - 0.5, ln, ln * wfac, ang, zone=zone,
                 shade=rnd.choice([1.0, 0.94, 0.88]), split=split, rib=rib)

    if species == "monstera":
        for i in range(7):
            ang = 90 + (i - 3) * 22 + rnd.uniform(-6, 6)
            L = avail * rnd.uniform(0.55, 0.95)
            a = math.radians(ang)
            sx, sy = math.cos(a) * L * 0.55, ground + math.sin(a) * L * 0.55
            stem(c, [(0, ground - 1), (sx * 0.6, (ground + sy) / 2), (sx, sy)], 0.8)
            leaf(c, sx, sy, L * 0.5, L * 0.42, ang + rnd.uniform(-15, 15), split=True)
    elif species == "fern":
        for i in range(11):
            ang = 90 + (i - 5) * 15
            L = avail * rnd.uniform(0.7, 1.0)
            a = math.radians(ang)
            ex, ey = math.cos(a) * L, ground + math.sin(a) * L * 0.8
            pts = [(0, ground), (ex * 0.5, ground + (ey - ground) * 0.75), (ex, ey)]
            stem(c, pts, 0.4)
            for k in range(1, 9):
                t = k / 9
                px = ex * t * (1 - 0.1 * t)
                py = ground + (ey - ground) * (t * 1.5 - 0.5 * t * t)
                ll = L * 0.16 * (1 - t * 0.6)
                for s in (-1, 1):
                    leaf(c, px, py, ll, ll * 0.45, ang + s * 60, rib=False, shade=0.95)
    elif species == "snake_plant":
        for i in range(8):
            x = (i - 3.5) * pw * 0.09
            L = avail * rnd.uniform(0.6, 1.0)
            ang = 90 + (x / pw) * 30 + rnd.uniform(-5, 5)
            p = leaf(c, x, ground - 0.5, L, pw * 0.16, ang, rib=False, shade=rnd.choice([1.0, 0.9]))
            cl = c.mask(p)
            for k in range(3, 9):
                yy = ground + L * k / 10
                c.line([(x - 3, yy), (x + 3, yy + 1)], 0.5, zone=1, shade=0.62, clip=cl)
            c.line(p, 0.6, zone=3, closed=True, clip=cl)
    elif species in ("cactus_column", "cactus_ball", "cactus_paddle"):
        if species == "cactus_column":
            cw = pw * 0.32
            body = rrect(-cw / 2, ground - 1, cw / 2, top - 0.5, cw / 2)
            shaded(c, body, 1, "right", SHADE, 0.3)
            for sx, hy in ((-1, 0.45), (1, 0.6)):
                arm = smooth([(sx * cw * 0.4, ground + avail * (hy - 0.08), "s"), (sx * cw * 1.3, ground + avail * (hy - 0.06)),
                              (sx * cw * 1.3, ground + avail * (hy + 0.22)), (sx * cw * 0.95, ground + avail * (hy + 0.22)),
                              (sx * cw * 0.95, ground + avail * (hy + 0.05)), (sx * cw * 0.4, ground + avail * (hy + 0.04), "s")])
                shaded(c, arm, 1, "right", SHADE, 0.3)
            for k in (-0.2, 0.2):
                c.line([(k * cw, ground + 2), (k * cw, top - 3)], 0.3, zone=1, shade=0.65)
            flower(c, 0, top - 1.5, cw * 0.3, 5)
        elif species == "cactus_ball":
            r = min(pw * 0.42, avail * 0.52)
            body = ell(0, ground + r * 0.9, r, r * 0.95)
            cl = shaded(c, body, 1, "right", SHADE, 0.3)
            for k in (-0.55, -0.2, 0.2, 0.55):
                c.line(smooth([(k * r * 0.6, ground + 1), (k * r, ground + r), (k * r * 0.6, ground + r * 1.8)], closed=False),
                       0.3, zone=1, shade=0.65, clip=cl)
            flower(c, 0, ground + r * 1.85, r * 0.35, 6)
        else:
            for (x, y, rx, ry, ang) in ((0, ground + avail * 0.32, pw * 0.3, avail * 0.3, 0),
                                        (-pw * 0.28, ground + avail * 0.68, pw * 0.22, avail * 0.22, 20),
                                        (pw * 0.25, ground + avail * 0.72, pw * 0.2, avail * 0.2, -15)):
                p = ell(x, y, rx, ry)
                shaded(c, p, 1, "right", SHADE, 0.3)
                for k in range(5):
                    c.ellipse(x + rnd.uniform(-rx, rx) * 0.6, y + rnd.uniform(-ry, ry) * 0.6, 0.35, 0.35, zone=3)
    elif species in ("succulent", "aloe"):
        n = 9 if species == "succulent" else 10
        for i in range(n):
            ang = 90 + (i - (n - 1) / 2) * (16 if species == "succulent" else 17)
            L = avail * (0.75 if species == "succulent" else 0.95) * (1 - abs(i - (n - 1) / 2) / n * 0.6)
            leaf(c, 0, ground - 0.5, L, L * (0.55 if species == "succulent" else 0.28), ang,
                 shade=0.85 + 0.15 * (i % 2), rib=False)
    elif species in ("ficus", "lemon_tree", "olive", "tree_small", "bonsai"):
        trunk_top = ground + avail * (0.45 if species != "bonsai" else 0.35)
        tw = pw * (0.1 if species != "bonsai" else 0.14)
        tr = smooth([(-tw, ground, "s"), (tw, ground, "s"), (tw * 0.6, trunk_top), (tw * 1.8, trunk_top + 3),
                     (-tw * 1.5, trunk_top + 3), (-tw * 0.6, trunk_top)]) if species != "bonsai" else \
            smooth([(-tw, ground, "s"), (tw, ground, "s"), (tw * 2.5, trunk_top * 0.9), (tw * 0.8, trunk_top + 2),
                    (-tw * 0.5, trunk_top + 2), (tw * 1.2, trunk_top * 0.85)])
        c.fill(tr, zone=3 if species in ("lemon_tree",) else 3, shade=0.55)
        cw = W * 0.46
        blobs = 7 if species != "bonsai" else 4
        for k in range(blobs):
            a = 2 * math.pi * k / blobs
            bx = math.cos(a) * cw * 0.55
            by = (trunk_top + top) / 2 + math.sin(a) * (top - trunk_top) * 0.3
            r = cw * rnd.uniform(0.42, 0.55)
            c.ellipse(bx, by, r, r * 0.85, zone=1, shade=rnd.choice([1.0, 0.92, 0.86]))
        c.ellipse(0, (trunk_top + top) / 2, cw * 0.8, (top - trunk_top) * 0.42, zone=1)
        for k in range(14):   # Blattstriche
            bx = rnd.uniform(-cw * 0.8, cw * 0.8)
            by = rnd.uniform(trunk_top + 4, top - 4)
            c.line([(bx, by), (bx + 1.5, by + 1.5)], 0.35, zone=1, shade=0.68)
        if species == "lemon_tree":
            for k in range(7):
                c.ellipse(rnd.uniform(-cw * 0.7, cw * 0.7), rnd.uniform(trunk_top + 5, top - 5), 2.2, 1.8, zone=3)
        if species == "olive":
            for k in range(6):
                c.ellipse(rnd.uniform(-cw * 0.7, cw * 0.7), rnd.uniform(trunk_top + 5, top - 5), 0.9, 1.2, zone=3)
    elif species == "palm":
        for i in range(7):
            ang = 90 + (i - 3) * 24
            L = avail * rnd.uniform(0.75, 1.0)
            a = math.radians(ang)
            ex, ey = math.cos(a) * L, ground + math.sin(a) * L * 0.85
            stem(c, [(0, ground), (ex * 0.4, ground + (ey - ground) * 0.7), (ex, ey)], 0.6)
            for k in range(2, 12):
                t = k / 12
                px, py = ex * t, ground + (ey - ground) * (t * 1.4 - 0.4 * t * t)
                for s in (-1, 1):
                    leaf(c, px, py, L * 0.2 * (1 - t * 0.5), 1.4, ang + s * 50 - 10, rib=False)
    elif species in ("tulips", "roses", "sunflower", "daisies", "lavender", "hydrangea", "poinsettia"):
        n = {"tulips": 6, "roses": 5, "sunflower": 3, "daisies": 9, "lavender": 9, "hydrangea": 3, "poinsettia": 1}[species]
        heads = []
        for i in range(n):
            x = (i - (n - 1) / 2) * pw * (0.14 if n > 3 else 0.28)
            hy = ground + avail * rnd.uniform(0.62, 0.9)
            bend = rnd.uniform(-3, 3)
            if species != "poinsettia":
                stem(c, [(x * 0.3, ground), (x + bend * 0.5, (ground + hy) / 2), (x + bend, hy)], 0.6)
            heads.append((x + bend, hy))
        for (x, y) in heads[: max(1, n // 2)]:
            leaf(c, x * 0.3, ground + avail * 0.2, avail * 0.3, avail * 0.12, 90 + x * 3 + rnd.uniform(20, 40))
            leaf(c, x * 0.3, ground + avail * 0.2, avail * 0.3, avail * 0.12, 90 + x * 3 - rnd.uniform(20, 40))
        for (x, y) in heads:
            if species == "tulips":
                tulip(c, x, y, pw * 0.1)
            elif species == "roses":
                c.ellipse(x, y, pw * 0.11, pw * 0.1, zone=3)
                c.line(smooth([(x - pw * 0.05, y), (x, y + pw * 0.04), (x + pw * 0.05, y), (x, y - pw * 0.04)],
                              closed=True), 0.3, zone=3, shade=0.65, closed=True)
            elif species == "sunflower":
                flower(c, x, y, pw * 0.22, 12, zone=3, center_zone=3)
                c.ellipse(x, y, pw * 0.1, pw * 0.1, zone=0, alpha=0.8)
            elif species == "daisies":
                flower(c, x, y, pw * 0.08, 8, zone=3, center_zone=3)
            elif species == "lavender":
                for k in range(6):
                    c.ellipse(x, y - k * 1.5, 0.9, 1.1, zone=3, shade=0.9 + (k % 2) * 0.1)
            elif species == "hydrangea":
                for k in range(12):
                    flower(c, x + rnd.uniform(-pw * 0.14, pw * 0.14), y + rnd.uniform(-pw * 0.12, pw * 0.12), pw * 0.05, 4)
        if species == "poinsettia":
            for i in range(8):
                leaf(c, 0, ground + avail * 0.35, avail * 0.5, avail * 0.26, 90 + (i - 3.5) * 22, zone=1)
            for i in range(9):
                leaf(c, 0, ground + avail * 0.55, avail * 0.42, avail * 0.2, 90 + (i - 4) * 32, zone=3)
            flower(c, 0, ground + avail * 0.6, 1.8, 5, zone=2, center_zone=2)
    elif species in ("orchid", "peace_lily", "bird_paradise", "calathea", "rubber_plant", "zz_plant", "spider_plant",
                     "herbs", "bamboo", "grass", "strawberry", "tomato", "ivy"):
        if species == "orchid":
            fan_leaves(4, avail * 0.3, avail * 0.38, 0.4, 50)
            stem(c, [(0, ground), (-pw * 0.05, ground + avail * 0.8), (pw * 0.2, top - 2)], 0.45)
            for k in range(5):
                t = k / 4
                flower(c, -pw * 0.05 + t * pw * 0.28, ground + avail * (0.7 + t * 0.26), pw * 0.1, 5)
        elif species == "peace_lily":
            fan_leaves(9, avail * 0.55, avail * 0.8, 0.42, 60)
            for k in (-1, 1):
                x = k * pw * 0.12
                stem(c, [(0, ground), (x, top - avail * 0.2)], 0.5)
                leaf(c, x, top - avail * 0.22, avail * 0.22, avail * 0.12, 90 + k * 10, zone=3, rib=False)
        elif species == "bird_paradise":
            fan_leaves(6, avail * 0.7, avail * 0.98, 0.3, 40)
            fx, fy = pw * 0.15, top - avail * 0.3
            leaf(c, fx, fy, avail * 0.2, avail * 0.07, 10, zone=3, rib=False)
            leaf(c, fx + 2, fy + 1, avail * 0.16, avail * 0.06, 50, zone=3, rib=False)
        elif species == "calathea":
            for i in range(7):
                ang = 90 + (i - 3) * 20
                L = avail * rnd.uniform(0.7, 0.95)
                a = math.radians(ang)
                sx, sy = math.cos(a) * L * 0.5, ground + math.sin(a) * L * 0.5
                stem(c, [(0, ground), (sx, sy)], 0.5)
                p = leaf(c, sx, sy, L * 0.5, L * 0.3, ang, rib=True)
                cl = c.mask(p)
                for k in range(3):
                    c.line([(sx, sy), (sx + math.cos(a) * L * 0.4, sy + math.sin(a) * L * 0.4)], 1.6 - k * 0.5, zone=3,
                           clip=cl, alpha=0.6)
        elif species == "rubber_plant":
            stem(c, [(0, ground), (0.5, top - 3)], 1.0, zone=3, shade=0.6)
            for k in range(8):
                y = ground + avail * (0.2 + k * 0.1)
                s = 1 if k % 2 else -1
                leaf(c, 0, y, avail * 0.26, avail * 0.14, 90 + s * rnd.uniform(35, 60), shade=0.85 + 0.15 * (k % 2))
        elif species == "zz_plant":
            for i in range(5):
                x = (i - 2) * pw * 0.08
                ang = 90 + (i - 2) * 12
                a = math.radians(ang)
                L = avail * rnd.uniform(0.75, 0.98)
                stem(c, [(x, ground), (x + math.cos(a) * L, ground + math.sin(a) * L)], 0.5)
                for k in range(3, 10):
                    t = k / 10
                    px, py = x + math.cos(a) * L * t, ground + math.sin(a) * L * t
                    for s in (-1, 1):
                        leaf(c, px, py, L * 0.12, L * 0.06, ang + s * 45, rib=False, shade=0.95)
        elif species == "spider_plant":
            for i in range(16):
                ang = 90 + (i - 7.5) * 11
                L = avail * rnd.uniform(0.7, 1.0)
                a = math.radians(ang)
                pts = [(0, ground), (math.cos(a) * L * 0.6, ground + math.sin(a) * L * 0.8),
                       (math.cos(a) * L * 1.1, ground + math.sin(a) * L * 0.5)]
                c.line(smooth(pts, closed=False), 1.3, zone=1, shade=0.9 + 0.1 * (i % 2))
                c.line(smooth(pts, closed=False), 0.35, zone=3, alpha=0.7)
        elif species == "herbs":
            for k in range(26):
                x = rnd.uniform(-pw * 0.38, pw * 0.38)
                y = ground + rnd.uniform(avail * 0.1, avail * 0.85)
                leaf(c, x, y, avail * 0.2, avail * 0.14, rnd.uniform(40, 140), shade=rnd.choice([1.0, 0.9, 0.84]), rib=False)
        elif species == "bamboo":
            for i in range(4):
                x = (i - 1.5) * pw * 0.12
                L = avail * rnd.uniform(0.7, 1.0)
                c.fill(rrect(x - 1.1, ground, x + 1.1, ground + L, 0.8), zone=1, shade=0.85)
                for k in range(1, 5):
                    c.line([(x - 1.2, ground + L * k / 5), (x + 1.2, ground + L * k / 5)], 0.35, zone=1, shade=0.6)
                leaf(c, x, ground + L - 1, L * 0.25, L * 0.1, 60 + i * 20, rib=False)
        elif species == "grass":
            for i in range(28):
                ang = 90 + (i - 13.5) * 3.2 + rnd.uniform(-3, 3)
                L = avail * rnd.uniform(0.6, 1.0)
                a = math.radians(ang)
                c.line(smooth([(rnd.uniform(-pw * 0.2, pw * 0.2), ground), (math.cos(a) * L * 0.5, ground + math.sin(a) * L * 0.6),
                               (math.cos(a) * L * 1.2, ground + math.sin(a) * L)], closed=False), 0.7, zone=1,
                       shade=rnd.choice([1.0, 0.9, 0.8]))
        elif species in ("strawberry", "tomato"):
            if species == "tomato":
                c.line([(0, ground), (0, top - 2)], 0.8, zone=3, shade=0.5)
            for k in range(12 if species == "strawberry" else 16):
                x = rnd.uniform(-pw * 0.4, pw * 0.4)
                y = ground + rnd.uniform(avail * 0.1, avail * (0.55 if species == "strawberry" else 0.95))
                leaf(c, x, y, avail * 0.18, avail * 0.14, rnd.uniform(30, 150), shade=rnd.choice([1.0, 0.9]), rib=False)
            for k in range(5 if species == "strawberry" else 6):
                x = rnd.uniform(-pw * 0.4, pw * 0.45)
                y = ground + rnd.uniform(avail * 0.1, avail * (0.5 if species == "strawberry" else 0.85))
                r = 1.6 if species == "strawberry" else 2.4
                c.ellipse(x, y, r, r * (1.2 if species == "strawberry" else 0.95), zone=3)
                c.ellipse(x - r * 0.3, y + r * 0.35, r * 0.25, r * 0.2, zone=2, alpha=0.5)
        elif species == "ivy":
            for i in range(5):
                x0 = (i - 2) * pw * 0.12
                pts = [(x0, ground), (x0 * 1.8 + (6 if i % 2 else -6), ground - avail * 0.1),
                       (x0 * 2.5, ground - rnd.uniform(0.1, 0.35) * H)]
                c.line(smooth(pts, closed=False), 0.4, zone=1, shade=0.6)
                for k in range(6):
                    t = k / 5
                    px = pts[0][0] + (pts[2][0] - pts[0][0]) * t
                    py = pts[0][1] + (pts[2][1] - pts[0][1]) * t
                    leaf(c, px, py, 3.2, 2.6, rnd.uniform(-160, -20), rib=False, shade=rnd.choice([1.0, 0.9]))
            fan_leaves(6, avail * 0.3, avail * 0.5, 0.6, 60)
    else:
        fan_leaves(7, avail * 0.6, avail * 0.95, 0.35, 60)
    # Topf VOR die Stiele malen: die Pflanze wächst aus der Erde im Topf
    pot(it, pot_style, pw, ph)
    c.fill(ell(0, ground - 0.3, pw * 0.38, max(0.8, ph * 0.06)), zone=0, alpha=0.55)


SPECIES = {
    # Art: (Höhe cm, Breite cm, Topfformen, Blattfarben-Varianten, Blüten-/Fruchtfarben)
    "monstera": (110, 90, ["terracotta", "basket", "cylinder", "stand"]),
    "fern": (60, 70, ["round", "basket", "stand", "bowl"]),
    "snake_plant": (80, 40, ["cylinder", "square", "terracotta"]),
    "cactus_column": (45, 24, ["terracotta", "cylinder", "square"]),
    "cactus_ball": (22, 18, ["terracotta", "bowl", "round"]),
    "cactus_paddle": (40, 34, ["terracotta", "bowl"]),
    "succulent": (16, 18, ["bowl", "round", "terracotta", "square"]),
    "aloe": (35, 34, ["terracotta", "cylinder", "round"]),
    "ficus": (150, 70, ["terracotta", "basket", "cylinder"]),
    "lemon_tree": (130, 70, ["terracotta", "square", "bucket"]),
    "olive": (140, 64, ["terracotta", "square", "cylinder"]),
    "tree_small": (120, 64, ["cylinder", "basket", "bucket"]),
    "bonsai": (28, 34, ["bowl", "square"]),
    "palm": (150, 100, ["basket", "cylinder", "terracotta"]),
    "tulips": (40, 24, ["round", "cylinder", "bucket"]),
    "roses": (45, 30, ["terracotta", "round", "bucket"]),
    "sunflower": (70, 34, ["terracotta", "bucket"]),
    "daisies": (30, 28, ["bowl", "round", "basket"]),
    "lavender": (40, 30, ["terracotta", "bucket", "square"]),
    "hydrangea": (55, 50, ["round", "terracotta", "bucket"]),
    "poinsettia": (35, 36, ["round", "terracotta"]),
    "orchid": (50, 28, ["cylinder", "round"]),
    "peace_lily": (60, 50, ["round", "cylinder", "basket"]),
    "bird_paradise": (150, 80, ["cylinder", "terracotta", "basket"]),
    "calathea": (55, 50, ["round", "cylinder", "basket"]),
    "rubber_plant": (110, 50, ["cylinder", "terracotta", "square"]),
    "zz_plant": (60, 40, ["square", "cylinder", "round"]),
    "spider_plant": (35, 50, ["round", "basket", "stand"]),
    "herbs": (28, 24, ["terracotta", "square", "bucket"]),
    "bamboo": (45, 20, ["square", "bowl"]),
    "grass": (60, 50, ["cylinder", "basket", "square"]),
    "strawberry": (25, 30, ["terracotta", "bucket"]),
    "tomato": (80, 44, ["bucket", "terracotta"]),
    "ivy": (30, 40, ["round", "stand", "basket"]),
}
