"""
Zoo-Tiere (P10g, Welt-Doku §10) in echter Größe, Stil wie die Haustiere: großer Kopf, Kulleraugen, weiche Schatten.
Alle schauen nach rechts (das Spiel spiegelt beim Laufen). Zonen: 1 = Fell · 2 = hell (Bauch, Glanzpunkte) · 3 = Akzent.
Vierbeiner werden aus einer Bauform mit Maßen je Art gezeichnet, dazu Vögel, Affen, Reptilien und kleine Tiere.
"""
from __future__ import annotations

import math

from pets.draw import blush, eye, smile

from .kit import INNER, SHADE, SOFT, Item, ell, rrect, shaded, smooth, trap

# Vierbeiner: Beinlänge, Körper (Breite, Höhe) als Anteil von W/H, Hals (Länge, Dicke), Kopf-Radius (Anteil H), Extras
QUAD = {
    "giraffe": dict(leg=0.36, bw=0.62, bh=0.2, neck=0.3, nw=0.08, head=0.09, ears=True, horns="ossicones", spots=True, tail=True),
    "zebra": dict(leg=0.42, bw=0.66, bh=0.33, neck=0.12, nw=0.1, head=0.2, ears=True, stripes=True, mane=True, tail=True),
    "lion": dict(leg=0.34, bw=0.6, bh=0.36, neck=0.05, nw=0.12, head=0.26, ears=True, mane=True, tail=True),
    "lion_cub": dict(leg=0.28, bw=0.56, bh=0.34, neck=0.04, nw=0.12, head=0.34, ears=True, tail=True),
    "elephant": dict(leg=0.34, bw=0.66, bh=0.46, neck=0.02, nw=0.2, head=0.26, ears="big", trunk=True, tail=True),
    "elephant_baby": dict(leg=0.3, bw=0.62, bh=0.44, neck=0.02, nw=0.2, head=0.32, ears="big", trunk=True, tail=True),
    "goat": dict(leg=0.4, bw=0.6, bh=0.3, neck=0.1, nw=0.1, head=0.24, ears=True, horns="small", beard=True, tail=True),
    "lamb": dict(leg=0.34, bw=0.62, bh=0.38, neck=0.06, nw=0.12, head=0.26, ears=True, wool=True, tail=True),
    "pig": dict(leg=0.2, bw=0.7, bh=0.46, neck=0.02, nw=0.16, head=0.3, ears=True, snout=True, tail=True),
}


def _leg(c, x: float, top: float, w: float, zone: int = 1, shade: float = 1.0, hoof: bool = True):
    leg = rrect(x - w / 2, 0, x + w / 2, top, w * 0.45)
    c.fill(leg, zone=zone, shade=shade)
    if hoof:
        c.fill(rrect(x - w / 2, 0, x + w / 2, max(2.0, w * 0.35), w * 0.3), zone=3, shade=shade * 0.9)
    c.line(leg, INNER, zone=0, closed=True)


def quadruped(c, W: float, H: float, kind: str):
    p = QUAD[kind]
    lh = H * p["leg"]
    bw, bh = W * p["bw"], H * p["bh"]
    bx, by = -W * 0.1, lh + bh * 0.42
    hr = H * p["head"]
    hoof = kind in ("giraffe", "zebra", "goat", "lamb", "pig")
    lw = max(4.0, bw * 0.12)
    for x in (bx + bw * 0.34 + lw * 0.4, bx - bw * 0.34 + lw * 0.4):         # hintere Beine (dunkler)
        _leg(c, x, by, lw, shade=0.82, hoof=hoof)
    if p.get("tail"):
        tx = bx - bw * 0.5
        c.line(smooth([(tx + 2, by + bh * 0.2), (tx - W * 0.06, by - bh * 0.1), (tx - W * 0.07, by - bh * 0.5)], closed=False),
               max(1.2, lw * 0.28), zone=1, shade=0.9)
        c.fill(ell(tx - W * 0.07, by - bh * 0.55, lw * 0.35, lw * 0.5, 12), zone=3 if kind != "pig" else 1)
    body = ell(bx, by, bw / 2, bh / 2, 40)
    shaded(c, body, 1, "bottom", SHADE, 0.3)
    cl = c.mask(body)
    c.fill(ell(bx + bw * 0.05, by - bh * 0.3, bw * 0.34, bh * 0.2, 28), zone=2, clip=cl, alpha=0.8)
    if p.get("stripes"):
        for k in range(7):
            x = bx - bw * 0.42 + k * bw * 0.13
            c.line(smooth([(x, by + bh * 0.5), (x + bw * 0.03, by), (x - bw * 0.02, by - bh * 0.4)], closed=False), bw * 0.035,
                   zone=3, clip=cl)
    if p.get("spots"):
        for k in range(9):
            x = bx - bw * 0.38 + (k % 5) * bw * 0.18 + (k // 5) * bw * 0.09
            y = by + bh * (0.18 - (k // 5) * 0.32)
            c.fill(smooth([(x - 5, y - 4), (x + 1, y - 6), (x + 6, y - 1), (x + 4, y + 5), (x - 4, y + 4)]), zone=3, clip=cl)
    if p.get("wool"):
        for k in range(10):
            a = 2 * math.pi * k / 10
            c.fill(ell(bx + math.cos(a) * bw * 0.42, by + math.sin(a) * bh * 0.4, bh * 0.2, bh * 0.2, 16), zone=2)
    c.line(body, INNER, zone=0, closed=True)
    for x in (bx + bw * 0.34, bx - bw * 0.34):                              # vordere Beine
        _leg(c, x, by, lw, hoof=hoof)
    # Hals + Kopf
    nx0, ny0 = bx + bw * 0.38, by + bh * 0.15
    hx = min(W / 2 - hr * 1.05, nx0 + W * 0.08 + H * p["neck"] * 0.25)
    hy = min(H - hr * (1.25 if p.get("horns") == "ossicones" else 1.05), ny0 + H * p["neck"])
    if p["neck"] > 0.03:
        neck = [(nx0 - W * p["nw"] * 0.5, ny0 - bh * 0.1), (nx0 + W * p["nw"] * 0.5, ny0 - bh * 0.15), (hx + hr * 0.3, hy - hr * 0.2),
                (hx - hr * 0.5, hy)]
        c.fill(smooth(neck), zone=1)
        if p.get("spots"):
            for k in range(4):
                t = (k + 0.5) / 4
                c.fill(ell(nx0 + (hx - nx0) * t, ny0 + (hy - ny0) * t, W * 0.02, W * 0.02, 10), zone=3)
        if p.get("mane") and kind == "zebra":
            c.line(smooth([(nx0 - W * 0.02, ny0 + bh * 0.1), (hx - hr * 0.6, hy + hr * 0.4)], closed=False), W * 0.03, zone=3)
    if p.get("mane") and kind == "lion":
        mane = ell(hx - hr * 0.1, hy, hr * 1.45, hr * 1.4, 36)
        c.fill(mane, zone=3)
        for k in range(14):
            a = 2 * math.pi * k / 14
            c.fill(ell(hx - hr * 0.1 + math.cos(a) * hr * 1.35, hy + math.sin(a) * hr * 1.3, hr * 0.3, hr * 0.3, 12), zone=3, shade=0.92)
    ears = p.get("ears")
    if ears == "big":
        ear = smooth([(hx - hr * 0.3, hy + hr * 0.6), (hx - hr * 1.5, hy + hr * 0.5), (hx - hr * 1.6, hy - hr * 0.6),
                      (hx - hr * 0.6, hy - hr * 0.9)])
        c.fill(ear, zone=1, shade=0.9)
        c.fill(ell(hx - hr * 1.0, hy, hr * 0.4, hr * 0.55, 20), zone=3, alpha=0.5)
        c.line(ear, INNER, zone=0, closed=True)
    head = ell(hx, hy, hr * (1.25 if kind in ("zebra", "goat", "giraffe") else 1.0), hr, 36)
    shaded(c, head, 1, "bottom", SOFT, 0.2)
    if ears is True:
        for dx, sh in ((-0.45, 0.85), (0.1, 1.0)):
            e = smooth([(hx + hr * dx - hr * 0.2, hy + hr * 0.7), (hx + hr * dx, hy + hr * 1.3), (hx + hr * dx + hr * 0.25, hy + hr * 0.75)])
            c.fill(e, zone=1, shade=sh)
            c.line(e, INNER, zone=0, closed=True)
    horns = p.get("horns")
    if horns == "ossicones":
        for dx in (-0.25, 0.15):
            c.line([(hx + hr * dx, hy + hr * 0.8), (hx + hr * dx, hy + hr * 1.2)], hr * 0.16, zone=1)
            c.fill(ell(hx + hr * dx, hy + hr * 1.22, hr * 0.13, hr * 0.13, 10), zone=3)
    elif horns == "small":
        c.line(smooth([(hx - hr * 0.1, hy + hr * 0.8), (hx - hr * 0.3, hy + hr * 1.2), (hx - hr * 0.6, hy + hr * 1.25)], closed=False),
               hr * 0.14, zone=3)
    if p.get("wool"):
        c.fill(ell(hx - hr * 0.1, hy + hr * 0.7, hr * 0.6, hr * 0.35, 20), zone=2)
    if p.get("trunk"):
        c.line(smooth([(hx + hr * 0.7, hy - hr * 0.2), (hx + hr * 1.05, hy - hr * 0.9), (hx + hr * 0.95, hy - hr * 1.7),
                       (hx + hr * 1.2, hy - hr * 1.9)], closed=False), hr * 0.42, zone=1)
    elif p.get("snout"):
        sn = ell(hx + hr * 0.85, hy - hr * 0.2, hr * 0.32, hr * 0.28, 20)
        c.fill(sn, zone=3)
        for dy in (-0.08, 0.08):
            c.fill(ell(hx + hr * 0.95, hy - hr * 0.2 + hr * dy * 2, hr * 0.05, hr * 0.06, 8), zone=0)
    else:
        muz = ell(hx + hr * 0.6, hy - hr * 0.35, hr * 0.5, hr * 0.38, 24)
        c.fill(muz, zone=2)
        c.fill(ell(hx + hr * 0.95, hy - hr * 0.2, hr * 0.14, hr * 0.1, 12), zone=0)
        smile(c, hx + hr * 0.62, hy - hr * 0.5, hr * 0.16)
    if p.get("beard"):
        c.fill([(hx + hr * 0.3, hy - hr * 0.7), (hx + hr * 0.55, hy - hr * 0.7), (hx + hr * 0.4, hy - hr * 1.2)], zone=2)
    eye(c, hx + hr * 0.2, hy + hr * 0.18, hr * 0.26)
    blush(c, hx + hr * 0.1, hy - hr * 0.3, hr * 0.2)
    c.line(head, INNER, zone=0, closed=True)


def zoo_animal(it: Item, style: str = "giraffe", state: str = ""):
    c, W, H = it.c, it.w, it.h
    if style in QUAD:
        quadruped(c, W, H, style)
    elif style in ("penguin", "penguin_chick"):                       # Pinguin (Küken: flauschig grau)
        body = ell(0, H * 0.45, W * 0.42, H * 0.45, 36)
        shaded(c, body, 1, "right", SOFT, 0.25)
        c.fill(ell(W * 0.08, H * 0.4, W * 0.28, H * 0.36, 32), zone=2)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.12, H * 0.02, W * 0.14, H * 0.03, 12), zone=3)
        c.fill(smooth([(-W * 0.4, H * 0.62), (-W * 0.52, H * 0.3), (-W * 0.34, H * 0.4)]), zone=1, shade=0.85)
        eye(c, W * 0.14, H * 0.74, H * 0.07)
        c.fill([(W * 0.3, H * 0.68), (W * 0.52, H * 0.64), (W * 0.3, H * 0.6)], zone=3)
        blush(c, W * 0.08, H * 0.64, H * 0.05)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "flamingo":                                         # Flamingo auf einem Bein
        c.line([(0, 0), (0, H * 0.45)], W * 0.05, zone=3)
        c.line(smooth([(0, H * 0.45), (W * 0.1, H * 0.3), (-W * 0.05, H * 0.25)], closed=False), W * 0.05, zone=3)
        body = ell(-W * 0.08, H * 0.52, W * 0.34, H * 0.12, 28)
        shaded(c, body, 1, "bottom", SOFT, 0.3)
        c.line(smooth([(W * 0.18, H * 0.56), (W * 0.26, H * 0.8), (W * 0.1, H * 0.88), (W * 0.2, H * 0.94)], closed=False), W * 0.07, zone=1)
        head = ell(W * 0.26, H * 0.93, W * 0.1, H * 0.05, 20)
        c.fill(head, zone=1)
        c.fill(smooth([(W * 0.34, H * 0.94), (W * 0.48, H * 0.9), (W * 0.44, H * 0.84)]), zone=3)
        eye(c, W * 0.27, H * 0.94, H * 0.022)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "parrot":                                           # Papagei auf einer Stange
        c.fill(rrect(-W * 0.45, H * 0.02, W * 0.45, H * 0.07, 1), zone=3, shade=0.7)
        c.fill(smooth([(-W * 0.1, H * 0.4), (-W * 0.2, 0), (0, H * 0.2)]), zone=3)
        body = ell(0, H * 0.45, W * 0.3, H * 0.3, 28)
        shaded(c, body, 1, "right", SOFT, 0.3)
        c.fill(ell(-W * 0.06, H * 0.42, W * 0.18, H * 0.22, 20), zone=3, shade=0.95)
        head = ell(W * 0.08, H * 0.78, W * 0.26, H * 0.2, 28)
        c.fill(head, zone=1)
        c.fill(ell(W * 0.12, H * 0.76, W * 0.12, H * 0.1, 16), zone=2)
        c.fill(smooth([(W * 0.28, H * 0.8), (W * 0.44, H * 0.7), (W * 0.3, H * 0.62)]), zone=0, shade=0.6)
        eye(c, W * 0.12, H * 0.8, H * 0.05)
        c.line(body, INNER, zone=0, closed=True)
        c.line(head, INNER, zone=0, closed=True)
    elif style == "chick":                                            # Küken
        body = ell(0, H * 0.42, W * 0.46, H * 0.4, 28)
        shaded(c, body, 1, "right", SOFT, 0.25)
        c.fill(ell(W * 0.14, H * 0.8, W * 0.3, H * 0.22, 24), zone=1)
        eye(c, W * 0.2, H * 0.84, H * 0.08)
        c.fill([(W * 0.38, H * 0.8), (W * 0.54, H * 0.76), (W * 0.38, H * 0.72)], zone=3)
        for sx in (-0.1, 0.1):
            c.line([(W * sx, H * 0.05), (W * sx, 0)], 0.6, zone=3)
        c.line(body, INNER, zone=0, closed=True)
    elif style in ("monkey", "gorilla"):                              # sitzender Affe (Gorilla: groß, dunkel)
        big = style == "gorilla"
        body = ell(0, H * 0.34, W * 0.36, H * 0.3, 36)
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(ell(W * 0.05, H * 0.3, W * 0.22, H * 0.2, 24), zone=2)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.26, H * 0.08, W * 0.14, H * 0.08, 16), zone=1, shade=0.9)
            c.line(smooth([(sx * W * 0.3, H * 0.5), (sx * W * 0.44, H * 0.3), (sx * W * 0.36, H * 0.08)], closed=False), W * 0.1, zone=1)
        if not big:
            c.line(smooth([(-W * 0.3, H * 0.15), (-W * 0.5, H * 0.3), (-W * 0.44, H * 0.6), (-W * 0.34, H * 0.55)], closed=False), W * 0.04, zone=1)
        head = ell(0, H * 0.74, W * 0.3, H * 0.22, 32)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.3, H * 0.76, W * 0.1, H * 0.08, 16), zone=2 if not big else 1)
        shaded(c, head, 1, "bottom", SOFT, 0.2)
        c.fill(smooth([(-W * 0.18, H * 0.66), (-W * 0.2, H * 0.84), (0, H * 0.9), (W * 0.2, H * 0.84), (W * 0.18, H * 0.66),
                       (0, H * 0.58)]), zone=2)
        for sx in (-1, 1):
            eye(c, sx * W * 0.08, H * 0.78, H * 0.045)
        smile(c, 0, H * 0.64, W * 0.05)
        c.line(body, INNER, zone=0, closed=True)
        c.line(head, INNER, zone=0, closed=True)
    elif style == "meerkat":                                          # Erdmännchen aufrecht
        body = smooth([(-W * 0.2, 0, "s"), (W * 0.2, 0, "s"), (W * 0.22, H * 0.5), (W * 0.12, H * 0.72), (-W * 0.12, H * 0.72),
                       (-W * 0.24, H * 0.5)])
        shaded(c, body, 1, "right", SOFT, 0.3)
        c.fill(ell(W * 0.04, H * 0.38, W * 0.12, H * 0.26, 20), zone=2)
        c.line(smooth([(-W * 0.2, H * 0.05), (-W * 0.45, H * 0.1), (-W * 0.48, H * 0.3)], closed=False), W * 0.08, zone=1)
        head = ell(W * 0.06, H * 0.82, W * 0.2, H * 0.14, 24)
        c.fill(head, zone=1)
        c.fill(ell(W * 0.24, H * 0.8, W * 0.08, H * 0.05, 12), zone=0)
        eye(c, W * 0.1, H * 0.86, H * 0.045)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "rabbit":                                           # Kaninchen (sitzt)
        body = ell(-W * 0.1, H * 0.3, W * 0.34, H * 0.3, 28)
        shaded(c, body, 1, "right", SOFT, 0.3)
        c.fill(ell(-W * 0.44, H * 0.3, W * 0.1, H * 0.1, 12), zone=2)
        for dx, sh in ((-0.04, 0.85), (0.1, 1.0)):
            c.fill(ell(W * (0.14 + dx), H * 0.86, W * 0.07, H * 0.16, 16), zone=1, shade=sh)
        head = ell(W * 0.2, H * 0.58, W * 0.24, H * 0.2, 28)
        c.fill(head, zone=1)
        eye(c, W * 0.26, H * 0.62, H * 0.07)
        c.fill(ell(W * 0.42, H * 0.54, W * 0.03, H * 0.025, 8), zone=3)
        c.line(body, INNER, zone=0, closed=True)
        c.line(head, INNER, zone=0, closed=True)
    elif style == "crocodile":                                        # Krokodil (freundlich, flach)
        body = smooth([(-W * 0.5, H * 0.3), (-W * 0.2, H * 0.1, "s"), (W * 0.2, H * 0.1, "s"), (W * 0.5, H * 0.3), (W * 0.2, H * 0.75),
                       (-W * 0.15, H * 0.7)])
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        for k in range(8):
            c.fill([(-W * 0.35 + k * W * 0.08, H * 0.66), (-W * 0.31 + k * W * 0.08, H * 0.82), (-W * 0.27 + k * W * 0.08, H * 0.66)], zone=1,
                   shade=0.85)
        for x in (-W * 0.15, W * 0.12):
            c.fill(ell(x, H * 0.08, W * 0.05, H * 0.1, 12), zone=1, shade=0.9)
        c.fill(ell(W * 0.28, H * 0.66, W * 0.07, H * 0.2, 20), zone=1)
        eye(c, W * 0.3, H * 0.72, H * 0.12)
        c.line(smooth([(W * 0.32, H * 0.4), (W * 0.48, H * 0.36)], closed=False), INNER * 1.3, zone=0)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "tortoise":                                         # Riesenschildkröte
        c.fill(ell(W * 0.36, H * 0.4, W * 0.14, H * 0.18, 20), zone=2)
        for x in (-W * 0.25, W * 0.2):
            c.fill(rrect(x - W * 0.06, 0, x + W * 0.06, H * 0.3, W * 0.03), zone=2, shade=0.9)
        shell = smooth([(-W * 0.42, H * 0.2, "s"), (W * 0.32, H * 0.2, "s"), (W * 0.2, H * 0.9), (-W * 0.05, H), (-W * 0.3, H * 0.9)])
        shaded(c, shell, 1, "right", SHADE, 0.25)
        cl = c.mask(shell)
        for k in range(5):
            c.line(ell(-W * 0.3 + k * W * 0.15, H * 0.55, W * 0.07, H * 0.16, 6), INNER, zone=0, closed=True, clip=cl)
        eye(c, W * 0.4, H * 0.46, H * 0.06)
        c.line(shell, INNER, zone=0, closed=True)
    elif style == "snake":                                            # zusammengerollte Schlange
        for k, r in enumerate((0.46, 0.34, 0.22)):
            ring = ell(0, H * 0.22 + k * H * 0.12, W * r, H * 0.16, 28)
            shaded(c, ring, 1, "bottom", SOFT, 0.3)
            c.line(ring, INNER, zone=0, closed=True)
        head = ell(W * 0.1, H * 0.78, W * 0.18, H * 0.16, 24)
        c.fill(head, zone=1)
        c.line(smooth([(0, H * 0.5), (W * 0.05, H * 0.65)], closed=False), W * 0.1, zone=1)
        eye(c, W * 0.16, H * 0.82, H * 0.06)
        c.line([(W * 0.26, H * 0.74), (W * 0.36, H * 0.72), (W * 0.4, H * 0.76)], 0.5, zone=3)
        c.line(head, INNER, zone=0, closed=True)
    else:
        raise ValueError(style)
