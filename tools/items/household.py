"""
Haushalt (P04b-T09): Küche, Bad, Deko, kleine Elektronik, Wäsche, Putzen.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe/Muster · 3 = Metall/Holz/Inhalt.
"""
from __future__ import annotations

import math

from .kit import DEEP, SHADE, SOFT, Item, ell, knob, line, rrect, shaded, smooth, trap


# ------------------------------------------------------------------ Küche
def mug(it: Item, style: str = "mug"):
    c, W, H = it.c, it.w, it.h
    bw = W * (0.72 if style == "mug" else 1.0)
    x0 = -W / 2
    if style == "mug":
        c.line(smooth([(x0 + bw - 1, H * 0.75), (W / 2, H * 0.65), (W / 2, H * 0.35), (x0 + bw - 1, H * 0.25)], closed=False),
               1.3, zone=1, shade=0.9)
    body = rrect(x0, 0, x0 + bw, H, 1.2)
    cl = shaded(c, body, 1, "right", SHADE, 0.25)
    c.ellipse(x0 + bw / 2, H * 0.5, bw * 0.16, bw * 0.16, zone=2, clip=cl)
    c.fill(rrect(x0, H - 1.2, x0 + bw, H, 0.5), zone=1, shade=SOFT, clip=cl)


def glass(it: Item, style: str = "water"):
    c, W, H = it.c, it.w, it.h
    body = trap(-W * 0.4, W * 0.4, 0, -W / 2, W / 2, H, 0.5)
    c.glass(body, zone=1, opacity=0.35)
    c.fill(trap(-W * 0.38, W * 0.38, 0.5, -W * 0.46, W * 0.46, H * 0.6, 0.4), zone=2, alpha=0.8)
    c.line(body, 0.3, zone=0, closed=True)
    c.line([(-W * 0.28, H * 0.85), (-W * 0.24, H * 0.2)], 0.5, zone=1, alpha=0.9)


def plate(it: Item, style: str = "plate"):
    c, W, H = it.c, it.w, it.h
    if style == "bowl":
        body = smooth([(-W * 0.3, 0.2, "s"), (W * 0.3, 0.2, "s"), (W / 2, H, "s"), (-W / 2, H, "s")])
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        line(c, [(-W * 0.46, H * 0.75), (W * 0.46, H * 0.75)], zone=2, clip=cl, w=0.8, shade=1.0)
        return
    body = smooth([(-W * 0.3, 0.2, "s"), (W * 0.3, 0.2, "s"), (W / 2, H, "s"), (-W / 2, H, "s")])
    shaded(c, body, 1, "bottom", SOFT, 0.5)
    line(c, [(-W * 0.4, H * 0.7), (W * 0.4, H * 0.7)], zone=2, w=0.6, shade=1.0)


def cookware(it: Item, style: str = "pot", state: str = ""):
    on = state == "on"
    c, W, H = it.c, it.w, it.h
    if style == "pot":
        bw = W * 0.72
        for sx in (-1, 1):
            c.fill(rrect(sx * bw / 2 - (2.5 if sx < 0 else 0), H * 0.62, sx * bw / 2 + (0 if sx < 0 else 2.5), H * 0.74, 1), zone=3)
        body = rrect(-bw / 2, 0, bw / 2, H * 0.82, 2)
        shaded(c, body, 1, "right", SHADE, 0.25)
        lid = smooth([(-bw / 2 - 0.6, H * 0.8, "s"), (bw / 2 + 0.6, H * 0.8, "s"), (bw * 0.35, H * 0.94), (-bw * 0.35, H * 0.94)])
        shaded(c, lid, 1, "bottom", SOFT, 0.4)
        c.fill(rrect(-2, H * 0.92, 2, H, 1), zone=3)
        if on:
            _steam(c, 0, H, W * 0.5)
    elif style == "pan":
        c.fill(rrect(W * 0.1, H * 0.55, W / 2, H * 0.8, 1), zone=3, shade=0.7)
        body = smooth([(-W * 0.45, H * 0.9, "s"), (W * 0.12, H * 0.9, "s"), (W * 0.06, 0.2), (-W * 0.39, 0.2)])
        shaded(c, body, 1, "bottom", SHADE, 0.4)
    elif style == "kettle":
        c.line(smooth([(-W * 0.3, H * 0.7), (-W * 0.05, H * 1.0), (W * 0.25, H * 0.7)], closed=False), 1.4, zone=3)
        c.fill(smooth([(W * 0.25, H * 0.35, "s"), (W / 2, H * 0.62, "s"), (W * 0.45, H * 0.66, "s"), (W * 0.22, H * 0.5, "s")]), zone=1)
        body = smooth([(-W * 0.38, 0.2, "s"), (W * 0.32, 0.2, "s"), (W * 0.3, H * 0.6), (0, H * 0.78), (-W * 0.36, H * 0.6)])
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        c.ellipse(-W * 0.03, H * 0.8, 1.5, 1.3, zone=3)
        line(c, [(-W * 0.36, H * 0.15), (W * 0.32, H * 0.15)], zone=3, clip=cl, w=1.4, shade=1.0)
        if on:
            c.ellipse(-W * 0.25, H * 0.3, 1.0, 1.0, zone=2)
            _steam(c, W * 0.48, H * 0.66, W * 0.3)
    elif style == "toaster":
        body = rrect(-W / 2, 0, W / 2, H, 3.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        for x in (-W * 0.18, W * 0.14):
            c.fill(rrect(x - W * 0.12, H - 1.4, x + W * 0.12, H + 0.1, 0.6), zone=0)
        c.fill(rrect(W / 2 - 1, H * (0.25 if on else 0.45), W / 2 + 1.5, H * (0.38 if on else 0.58), 0.5), zone=3)
        if on:
            for x in (-W * 0.18, W * 0.14):
                c.glass(ell(x, H + 1.5, W * 0.14, 2.5), zone=2, opacity=0.5)
        line(c, [(-W / 2 + 2, H * 0.2), (W / 2 - 2, H * 0.2)], zone=3, clip=cl, w=0.8, shade=1.0)
    elif style == "blender":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.28, 2), zone=1)
        knob(c, 0, H * 0.14, 1.4)
        jar = trap(-W * 0.36, W * 0.36, H * 0.28, -W * 0.45, W * 0.45, H * 0.93, 0.8)
        c.glass(jar, zone=2, opacity=0.4)
        if on:   # wirbelnder Inhalt
            c.fill(smooth([(-W * 0.34, H * 0.29), (W * 0.34, H * 0.29), (W * 0.42, H * 0.8), (W * 0.1, H * 0.66),
                           (-W * 0.2, H * 0.84), (-W * 0.42, H * 0.7)]), zone=2, alpha=0.9)
            c.line(smooth([(-W * 0.2, H * 0.4), (W * 0.15, H * 0.55), (-W * 0.1, H * 0.7)], closed=False), 0.5, zone=0, alpha=0.4)
        else:
            c.fill(trap(-W * 0.34, W * 0.34, H * 0.29, -W * 0.4, W * 0.4, H * 0.6, 0.6), zone=2, alpha=0.85)
        c.line(jar, 0.3, zone=0, closed=True)
        c.fill(rrect(-W * 0.47, H * 0.92, W * 0.47, H, 1), zone=1)
    elif style == "microwave":
        body = rrect(-W / 2, 0, W / 2, H, 2)
        cl = shaded(c, body, 1, "right", SHADE, 0.15)
        win = rrect(-W / 2 + 3, 3, W * 0.2, H - 3, 1.5)
        c.fill(win, zone=0, alpha=0.9)
        if on:
            c.fill(win, zone=2, alpha=0.55)
            c.fill(ell(-W * 0.12, 5.5, W * 0.18, 2), zone=3, alpha=0.8)
        c.fill(smooth([(-W * 0.4, H - 5), (-W * 0.25, H - 5), (-W * 0.36, 5), (-W * 0.46, 5)]), zone=2, alpha=0.2)
        for k in range(4):
            c.fill(rrect(W * 0.28, H - 7 - k * 4.5, W * 0.44, H - 4 - k * 4.5, 0.6), zone=3)
    elif style == "coffee":
        body = rrect(-W / 2, 0, W / 2, H, 2)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.3, 2, W * 0.3, H * 0.55, 1), zone=0, alpha=0.85)
        c.fill(rrect(-W * 0.12, 2, W * 0.12, H * 0.2, 0.8), zone=2)
        knob(c, W * 0.3, H * 0.8, 1.3)
        if on:
            c.line([(0, H * 0.5), (0, H * 0.22)], 0.6, zone=3)
            _steam(c, 0, H * 0.24, W * 0.3)
            c.ellipse(W * 0.3, H * 0.65, 0.8, 0.8, zone=2)
    elif style == "board":
        c.fill(rrect(-W / 2, 0, W / 2, H, H * 0.45), zone=3)
        c.ellipse(W / 2 - 3, H / 2, 0.9, 0.5, zone=0)


def _steam(c, x: float, y: float, w: float):
    """Dampf-Kringel (weiß-transparent) über heißen Dingen."""
    for k, dx in enumerate((-0.3, 0.05, 0.35)):
        pts = smooth([(x + dx * w, y + 1), (x + dx * w + w * 0.12, y + w * 0.35), (x + dx * w - w * 0.08, y + w * 0.7),
                      (x + dx * w + w * 0.06, y + w * 0.95)], closed=False, n=8)
        c.glass(_band(pts, max(0.5, w * 0.06)), zone=1, opacity=0.45)


def _band(pts, r):
    """Kurve → schmale Fläche (für halbdurchsichtige Striche)."""
    import math as _m
    left, right = [], []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = _m.hypot(dx, dy) or 1.0
        nx, ny = -dy / n * r, dx / n * r
        left.append((pts[i][0] + nx, pts[i][1] + ny))
        right.append((pts[i][0] - nx, pts[i][1] - ny))
    return left + right[::-1]


def utensil(it: Item, style: str = "spoon"):
    c, W, H = it.c, it.w, it.h
    if style in ("spoon", "ladle", "spatula", "whisk", "fork"):
        c.fill(rrect(-W * 0.14, 0, W * 0.14, H * 0.68, W * 0.14), zone=3 if style != "spatula" else 1)
        head_y = H * 0.66
        if style == "spoon":
            c.fill(ell(0, head_y + H * 0.15, W / 2, H * 0.18), zone=1)
        elif style == "ladle":
            c.fill(ell(0, head_y + H * 0.14, W / 2, H * 0.16), zone=1)
            c.fill(ell(0, head_y + H * 0.1, W * 0.42, H * 0.08), zone=0, alpha=0.4)
        elif style == "spatula":
            c.fill(rrect(-W / 2, head_y, W / 2, H, 1), zone=3)
            for k in (-0.2, 0.0, 0.2):
                c.fill(rrect(k * W - 0.3, head_y + 2, k * W + 0.3, H - 2, 0.2), zone=0)
        elif style == "whisk":
            for k in range(-2, 3):
                c.line(smooth([(0, head_y), (k * W * 0.18, head_y + H * 0.2), (0, H)], closed=False), 0.35, zone=3, shade=0.8)
        elif style == "fork":
            c.fill(rrect(-W * 0.35, head_y, W * 0.35, head_y + H * 0.1, 0.6), zone=1)
            for k in (-0.28, -0.1, 0.1, 0.28):
                c.fill(rrect(k * W - 0.35, head_y + H * 0.08, k * W + 0.35, H, 0.35), zone=1)


def bottle(it: Item, style: str = "bottle"):
    c, W, H = it.c, it.w, it.h
    if style == "jar":
        body = rrect(-W / 2, 0, W / 2, H * 0.85, 2)
        c.glass(body, zone=1, opacity=0.35)
        c.fill(rrect(-W * 0.46, 0.4, W * 0.46, H * 0.6, 1.5), zone=2, alpha=0.85)
        c.line(body, 0.3, zone=0, closed=True)
        c.fill(rrect(-W * 0.44, H * 0.83, W * 0.44, H, 1), zone=3)
        c.fill(rrect(-W * 0.3, H * 0.25, W * 0.3, H * 0.45, 0.8), zone=1, shade=1.0)
        return
    neck = W * 0.3
    body = smooth([(-W / 2, 0.2, "s"), (W / 2, 0.2, "s"), (W / 2, H * 0.55), (neck / 2, H * 0.72), (neck / 2, H * 0.9, "s"),
                   (-neck / 2, H * 0.9, "s"), (-neck / 2, H * 0.72), (-W / 2, H * 0.55)])
    cl = shaded(c, body, 1, "right", SHADE, 0.25)
    c.fill(rrect(-W / 2, H * 0.18, W / 2, H * 0.45, 0.4), zone=2, clip=cl)
    c.fill(rrect(-neck * 0.6, H * 0.88, neck * 0.6, H, 0.6), zone=3)


# ------------------------------------------------------------------ Bad
def bath(it: Item, style: str = "towel", state: str = ""):
    c, W, H = it.c, it.w, it.h
    if style == "towel":
        body = rrect(-W / 2, 0, W / 2, H, 2)
        cl = shaded(c, body, 1, "bottom", SOFT, 0.3)
        for y in (H * 0.25, H * 0.33):
            line(c, [(-W / 2, y), (W / 2, y)], zone=2, clip=cl, w=1.0, shade=1.0)
        for k in range(1, 4):
            line(c, [(-W / 2 + 1, H * k / 4 + 2), (W / 2 - 1, H * k / 4 + 2)], clip=cl, shade=0.85)
    elif style == "duck":
        c.fill(ell(0, H * 0.3, W * 0.48, H * 0.3), zone=1)
        c.fill(ell(W * 0.12, H * 0.7, W * 0.26, H * 0.28), zone=1)
        c.fill(smooth([(W * 0.34, H * 0.7, "s"), (W / 2, H * 0.64), (W * 0.34, H * 0.6, "s")]), zone=2)
        c.ellipse(W * 0.2, H * 0.78, 0.8, 0.8, zone=0)
        c.fill(smooth([(-W * 0.3, H * 0.4), (-W * 0.05, H * 0.5), (-W * 0.1, H * 0.25)]), zone=1, shade=SHADE)
    elif style == "toothbrush":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.8, W * 0.4), zone=1)
        c.fill(rrect(-W * 0.45, H * 0.8, W * 0.45, H, 0.3), zone=2)
        for k in range(4):
            line(c, [(-W * 0.3 + k * W * 0.2, H * 0.82), (-W * 0.3 + k * W * 0.2, H)], zone=2, shade=0.8)
    elif style == "soap":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.55, 1.2), zone=2)
        c.fill(ell(0, H * 0.6, W * 0.38, H * 0.18), zone=1)
        for (x, y, r) in ((-W * 0.2, H * 0.85, 1.2), (W * 0.1, H * 0.92, 0.9), (W * 0.3, H * 0.8, 0.7)):
            c.glass(ell(x, y, r, r), zone=3, opacity=0.5)
            c.line(ell(x, y, r, r, 24), 0.2, zone=0, closed=True)
    elif style == "shampoo":
        body = smooth([(-W / 2, 0.2, "s"), (W / 2, 0.2, "s"), (W * 0.46, H * 0.72), (W * 0.3, H * 0.82), (-W * 0.3, H * 0.82),
                       (-W * 0.46, H * 0.72)])
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.ellipse(0, H * 0.4, W * 0.25, W * 0.25, zone=2, clip=cl)
        c.fill(rrect(-W * 0.18, H * 0.8, W * 0.18, H, 0.8), zone=3)
    elif style == "tp":
        body = rrect(-W / 2, 0, W / 2, H, 2)
        cl = shaded(c, body, 1, "right", SOFT, 0.25)
        c.fill(ell(0, H - 0.5, W * 0.2, 1.2), zone=3, shade=0.8)
        for k in range(1, 4):
            line(c, [(-W / 2, H * k / 4), (W / 2, H * k / 4)], clip=cl, shade=0.88)
    elif style == "hairdryer":
        c.fill(rrect(-W * 0.1, 0, W * 0.12, H * 0.55, 1.2), zone=1)
        body = smooth([(-W / 2, H * 0.55), (-W * 0.35, H), (W * 0.3, H * 0.95), (W / 2, H * 0.8), (W / 2, H * 0.62),
                       (W * 0.1, H * 0.55)])
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(W / 2 - 1.2, H * 0.62, W / 2 + 0.6, H * 0.8, 0.5), zone=3)
        c.ellipse(-W * 0.25, H * 0.8, 1.6, 1.6, zone=2)
        if state == "on":
            for k in range(3):
                c.line([(W / 2 + 2, H * (0.64 + k * 0.07)), (W / 2 + 7, H * (0.6 + k * 0.1))], 0.4, zone=0, alpha=0.5)
    elif style == "basket":
        body = trap(-W * 0.42, W * 0.42, 0, -W / 2, W / 2, H * 0.8, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        for k in range(1, 4):
            line(c, [(-W / 2, H * 0.8 * k / 4), (W / 2, H * 0.8 * k / 4)], clip=cl, shade=0.75)
        c.fill(rrect(-W * 0.3, H * 0.75, W * 0.3, H, 2), zone=2)


# ------------------------------------------------------------------ Deko & Elektronik (klein)
def deco(it: Item, style: str = "vase", state: str = ""):
    on = state == "on"
    c, W, H = it.c, it.w, it.h
    if style == "vase":
        body = smooth([(-W * 0.3, 0.2, "s"), (W * 0.3, 0.2, "s"), (W / 2, H * 0.45), (W * 0.2, H * 0.85), (W * 0.26, H, "s"),
                       (-W * 0.26, H, "s"), (-W * 0.2, H * 0.85), (-W / 2, H * 0.45)])
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        line(c, [(-W / 2, H * 0.42), (W / 2, H * 0.42)], zone=2, clip=cl, w=1.2, shade=1.0)
    elif style == "candle":
        body = rrect(-W / 2, 0, W / 2, H * 0.8, 1)
        shaded(c, body, 1, "right", SOFT, 0.25)
        c.line([(0, H * 0.8), (0, H * 0.86)], 0.4, zone=0)
        c.fill(smooth([(0, H), (W * 0.2, H * 0.9), (0, H * 0.84), (-W * 0.2, H * 0.9)]), zone=2)
    elif style == "clock":
        c.fill(ell(0, H / 2, W / 2, H / 2), zone=1)
        c.fill(ell(0, H / 2, W * 0.4, H * 0.4), zone=2)
        for k in range(12):
            a = math.radians(k * 30)
            c.ellipse(math.cos(a) * W * 0.33, H / 2 + math.sin(a) * H * 0.33, 0.45, 0.45, zone=0)
        c.line([(0, H / 2), (0, H * 0.8)], 0.6, zone=0)
        c.line([(0, H / 2), (W * 0.2, H / 2)], 0.6, zone=0)
    elif style == "frame":
        body = rrect(-W / 2, 0, W / 2, H, 1)
        c.fill(body, zone=3)
        c.fill(rrect(-W / 2 + 2, 2, W / 2 - 2, H - 2, 0.5), zone=2)
        c.fill(smooth([(-W / 2 + 2, 2, "s"), (-W * 0.1, H * 0.5), (W * 0.1, H * 0.3), (W / 2 - 2, H * 0.6), (W / 2 - 2, 2, "s")]),
               zone=1)
        c.ellipse(W * 0.2, H * 0.72, W * 0.1, W * 0.1, zone=1, shade=1.0)
    elif style == "cushion":
        body = smooth([(-W / 2, H * 0.1), (0, 0), (W / 2, H * 0.1), (W * 0.46, H * 0.9), (0, H), (-W * 0.46, H * 0.9)])
        cl = shaded(c, body, 1, "bottom", SOFT, 0.35)
        c.ellipse(0, H / 2, W * 0.12, H * 0.12, zone=2, clip=cl)
    elif style == "rug":
        body = ell(0, H / 2, W / 2, H / 2)
        cl = shaded(c, body, 1, "bottom", SOFT, 0.4)
        c.line(ell(0, H / 2, W * 0.38, H * 0.3), 1.2, zone=2, closed=True, clip=cl)
    elif style == "radio":
        body = rrect(-W / 2, 0, W / 2, H * 0.8, 2)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.ellipse(-W * 0.22, H * 0.4, H * 0.24, H * 0.24, zone=2)
        for k in range(3):
            line(c, [(W * 0.05, H * (0.25 + k * 0.13)), (W * 0.4, H * (0.25 + k * 0.13))], clip=cl, shade=0.7)
        c.line([(W * 0.3, H * 0.8), (W * 0.45, H)], 0.5, zone=3)
        if on:   # Musiknoten
            for k, (nx, ny) in enumerate(((-W * 0.35, H * 1.05), (W * 0.05, H * 1.2), (W * 0.4, H * 1.1))):
                c.ellipse(nx, ny, 1.3, 1.0, zone=0)
                c.line([(nx + 1.1, ny), (nx + 1.1, ny + 4)], 0.4, zone=0)
    elif style == "laptop":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.14, 0.8), zone=1)
        scr = trap(-W * 0.42, W * 0.42, H * 0.12, -W * 0.46, W * 0.46, H, 0.8)
        c.fill(scr, zone=1)
        c.fill(trap(-W * 0.38, W * 0.38, H * 0.2, -W * 0.41, W * 0.41, H * 0.92, 0.5), zone=2 if on else 0, shade=1.0)
        if on:
            for k in range(3):
                c.fill(rrect(-W * 0.3, H * (0.7 - k * 0.14), W * (0.1 + k * 0.08), H * (0.75 - k * 0.14), 0.4), zone=1, alpha=0.6)
    elif style == "phone":
        body = rrect(-W / 2, 0, W / 2, H, W * 0.18)
        c.fill(body, zone=1)
        c.fill(rrect(-W * 0.4, H * 0.08, W * 0.4, H * 0.9, W * 0.1), zone=2 if on else 0, shade=1.0)
        if on:
            for k in range(3):
                c.fill(rrect(-W * 0.3, H * (0.7 - k * 0.2), W * 0.3, H * (0.82 - k * 0.2), 0.8), zone=1, alpha=0.5)
    elif style == "books":
        from .furniture import _books
        _books(c, -W / 2, W / 2, 0, H, int(W * 7))
    elif style == "globe":
        c.fill(rrect(-W * 0.3, 0, W * 0.3, H * 0.08, 0.6), zone=3)
        c.line([(0, H * 0.08), (0, H * 0.2)], 1.0, zone=3)
        c.fill(ell(0, H * 0.58, W * 0.42, H * 0.4), zone=2)
        c.fill(smooth([(-W * 0.2, H * 0.8), (W * 0.1, H * 0.85), (W * 0.2, H * 0.6), (0, H * 0.45), (-W * 0.25, H * 0.55)]),
               zone=1)
        c.line(smooth([(W * 0.46, H * 0.3), (W * 0.5, H * 0.6), (W * 0.3, H * 0.95)], closed=False), 0.6, zone=3)
    elif style == "basket_laundry":
        body = trap(-W * 0.42, W * 0.42, 0, -W / 2, W / 2, H * 0.85, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        for r in range(3):
            for k in range(-3, 4):
                c.ellipse(k * W * 0.13, H * (0.2 + r * 0.22), W * 0.035, H * 0.05, zone=0, clip=cl, alpha=0.6)
        c.fill(smooth([(-W * 0.4, H * 0.8), (-W * 0.1, H), (W * 0.3, H * 0.92), (W * 0.42, H * 0.8)]), zone=2)
    elif style == "broom":
        c.fill(rrect(-0.9, H * 0.28, 0.9, H, 0.8), zone=3)
        c.fill(trap(-W / 2, W / 2, 0, -W * 0.25, W * 0.25, H * 0.3, 1), zone=1)
        for k in range(-3, 4):
            line(c, [(k * W * 0.12, 0.5), (k * W * 0.07, H * 0.26)], shade=0.7)
    elif style == "bucket_mop":
        body = trap(-W * 0.38, W * 0.38, 0, -W / 2, W / 2, H * 0.6, 1)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.line(smooth([(-W / 2, H * 0.6), (0, H * 0.85), (W / 2, H * 0.6)], closed=False), 0.6, zone=3)
        c.fill(rrect(W * 0.1, H * 0.5, W * 0.18, H, 0.4), zone=3)
