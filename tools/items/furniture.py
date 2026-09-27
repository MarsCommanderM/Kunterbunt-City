"""
Möbel (P04b-T09): Sofas, Sessel, Stühle, Hocker, Tische, Betten, Schränke, Regale, Lampen, Fernseher.
Vorderansicht mit sichtbarer Oberkante (wie in der Stil-Vorlage). Maße kommen aus dem Katalog (cm).
Zonen: 1 = Bezug/Lack (umfärbbar) · 2 = Kissen/Akzent (umfärbbar) · 3 = Holz/Metall/Füße.
"""
from __future__ import annotations

import math

from .kit import (DEEP, LINE, SHADE, SOFT, Item, cushion, ell, grain, knob, leg, line, rrect, shaded,
                  smooth)


# ------------------------------------------------------------------ Sitzmöbel
def sofa(it: Item, style: str = "classic", seat_h: float = 42.0, seats: int = 3):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    foot = 6.0 if style != "modern" else 12.0
    arm_w = {"classic": W * 0.1, "round": W * 0.12, "modern": W * 0.07, "chesterfield": W * 0.1}.get(style, W * 0.1)
    arm_h = {"classic": seat_h + 18, "round": seat_h + 14, "modern": seat_h + 12, "chesterfield": H - 2}.get(style, seat_h + 16)
    # Füße
    for fx in (x0 + arm_w * 0.5, x1 - arm_w * 0.5) + ((0.0,) if W > 150 else ()):
        if style == "modern":
            leg(c, fx, 0, foot + 1, 2.2, 1.2)
        else:
            leg(c, fx, 0, foot + 1, 4.5, 3.2)
    # Rückenlehne
    if style == "round":
        back = smooth([(x0 + 4, seat_h), (x0 + 2, H * 0.8), (x0 + W * 0.2, H), (0, H + 0.5), (x1 - W * 0.2, H),
                       (x1 - 2, H * 0.8), (x1 - 4, seat_h)])
    else:
        back = rrect(x0 + arm_w * 0.6, seat_h - 4, x1 - arm_w * 0.6, H, 5 if style != "modern" else 2)
    shaded(c, back, 1, "bottom", SOFT, 0.35)
    # Sockel (Sitzfront)
    base = rrect(x0 + 1, foot, x1 - 1, seat_h - 8, 3 if style != "modern" else 1.5)
    shaded(c, base, 1, "bottom", SHADE, 0.3)
    # Rückenkissen
    n = seats
    inner0, inner1 = x0 + arm_w, x1 - arm_w
    cw = (inner1 - inner0) / n
    for i in range(n):
        a, b = inner0 + i * cw + 0.8, inner0 + (i + 1) * cw - 0.8
        if style == "chesterfield":
            continue
        cushion(c, a, seat_h + 2, b, H - (4 if style != "modern" else 3), zone=2 if style == "modern" else 1)
    # Sitzkissen
    for i in range(n):
        a, b = inner0 + i * cw + 0.5, inner0 + (i + 1) * cw - 0.5
        cl = cushion(c, a, seat_h - 9, b, seat_h + 1, zone=1, r=4 if style != "modern" else 2)
        line(c, [(a + 3, seat_h - 1.5), (b - 3, seat_h - 1.5)], clip=cl, shade=0.78)
    # Armlehnen
    for sx in (-1, 1):
        ax0 = x0 if sx < 0 else x1 - arm_w
        if style == "classic":
            arm = smooth([(ax0, foot + 2, "s"), (ax0 + arm_w, foot + 2, "s"), (ax0 + arm_w, arm_h - 4),
                          (ax0 + arm_w * 0.5, arm_h + 2), (ax0, arm_h - 4)])
        elif style == "round":
            arm = smooth([(ax0, foot + 2, "s"), (ax0 + arm_w, foot + 2, "s"), (ax0 + arm_w, arm_h - 6),
                          (ax0 + arm_w * 0.5, arm_h), (ax0, arm_h - 6)])
        else:
            arm = rrect(ax0, foot + 1, ax0 + arm_w, arm_h, 2.5 if style == "modern" else 5)
        cl = shaded(c, arm, 1, "right" if sx < 0 else "bottom", SHADE, 0.3)
        if style == "classic":
            c.ellipse(ax0 + arm_w * 0.5, arm_h - 6, arm_w * 0.3, 3.2, zone=1, shade=SOFT, clip=cl)
            line(c, smooth([(ax0 + arm_w * 0.25, arm_h - 6), (ax0 + arm_w * 0.5, arm_h - 3.4),
                            (ax0 + arm_w * 0.75, arm_h - 6)], closed=False), clip=cl)
    if style == "chesterfield":   # Knöpfe in der Lehne
        for r in range(2):
            for i in range(int(W / 16)):
                x = inner0 + 8 + i * 16 + (8 if r else 0)
                if x < inner1 - 6:
                    c.ellipse(x, seat_h + 12 + r * 12, 0.9, 0.9, zone=0)
        line(c, [(inner0 + 2, seat_h + 6), (inner1 - 2, seat_h + 6)], shade=0.78)
    # Zierkissen
    if style in ("classic", "round"):
        for sx in (-1, 1):
            px = sx * (W / 2 - arm_w - 14)
            pil = smooth([(px - 10, seat_h + 1), (px - 11, seat_h + 16), (px, seat_h + 19), (px + 11, seat_h + 16),
                          (px + 10, seat_h + 1)])
            cl = shaded(c, pil, 2, "bottom", SOFT, 0.35)
            line(c, [(px - 4, seat_h + 10), (px + 4, seat_h + 10)], zone=2, clip=cl)


def armchair(it: Item, style: str = "classic", seat_h: float = 42.0):
    sofa(it, style, seat_h, seats=1)


def chair(it: Item, style: str = "dining", seat_h: float = 45.0):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style in ("dining", "mint", "kids"):
        # Rückenlehne: zwei Pfosten + Querstreben
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 3), seat_h - 1, H, 3.4, 3.0, zone=3 if style == "dining" else 1)
        rail_z = 3 if style == "dining" else 1
        for yy in (H - 9, H - 20):
            shaded(c, rrect(x0 + 2, yy, x1 - 2, yy + 6, 2.5), rail_z, "bottom", SHADE, 0.35)
        # Beine
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 3.5), 0, seat_h - 2, 3.6, 2.8, zone=3 if style == "dining" else 1)
        line(c, [(x0 + 5, seat_h * 0.4), (x1 - 5, seat_h * 0.4)], zone=3 if style == "dining" else 1, shade=0.7, w=1.6)
        # Sitz
        seat = rrect(x0, seat_h - 5, x1, seat_h, 2)
        shaded(c, seat, 3 if style == "dining" else 1, "bottom", SHADE, 0.4)
        if style != "dining":
            cushion(c, x0 + 2, seat_h - 1, x1 - 2, seat_h + 4, zone=2, r=2.5)
    elif style == "stool":
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 5), 0, seat_h - 3, 3.6, 2.6)
        line(c, [(x0 + 6, seat_h * 0.35), (x1 - 6, seat_h * 0.35)], zone=3, shade=0.7, w=1.6)
        top = rrect(x0, seat_h - 5, x1, seat_h, 2.5)
        cl = shaded(c, top, 1, "bottom", SHADE, 0.4)
        c.fill(rrect(x0, seat_h - 1.5, x1, seat_h, 1), zone=1, shade=1.0, clip=cl)
    elif style == "bar":
        leg(c, 0, 4, seat_h - 3, 4.0, 3.4, zone=3)
        c.fill(rrect(-W * 0.35, 0, W * 0.35, 4, 2), zone=3)
        c.line([(-W * 0.3, seat_h * 0.35), (W * 0.3, seat_h * 0.35)], 1.6, zone=3, shade=0.75)
        cushion(c, x0, seat_h - 6, x1, seat_h, zone=1, r=3)
    elif style == "office":
        # Rollen, Säule, Sitz, Rücken
        for k in (-1, 0, 1):
            c.ellipse(k * W * 0.36, 2.2, 2.2, 2.2, zone=0)
        c.fill(rrect(-W * 0.42, 3, W * 0.42, 5.5, 1.2), zone=3, shade=0.7)
        c.fill(rrect(-1.6, 5, 1.6, seat_h - 5, 0.8), zone=3, shade=0.8)
        cushion(c, x0 + 1, seat_h - 7, x1 - 1, seat_h, zone=1, r=3)
        back = rrect(x0 + 4, seat_h + 3, x1 - 4, H, 6)
        shaded(c, back, 1, "bottom", SOFT, 0.35)
        c.fill(rrect(-2, seat_h - 1, 2, seat_h + 4, 0.8), zone=3, shade=0.7)
    elif style == "rocking":
        c.fill(smooth([(x0 - 6, 5), (0, 0), (x1 + 6, 5), (x1 + 6, 7.5), (0, 3), (x0 - 6, 7.5)]), zone=3)
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 3), 3, seat_h - 2, 3.2, 2.8)
            leg(c, sx * (W / 2 - 3), seat_h - 1, H, 3.2, 3.0)
        for yy in (H - 10, H - 22, H - 34):
            c.fill(rrect(x0 + 2, yy, x1 - 2, yy + 5, 2), zone=3, shade=0.9)
        shaded(c, rrect(x0, seat_h - 5, x1, seat_h, 2), 3, "bottom", SHADE, 0.4)
        cushion(c, x0 + 2, seat_h - 1, x1 - 2, seat_h + 4, zone=1, r=2.5)
    elif style == "beanbag":
        bag = smooth([(x0 + 4, 0.5), (x1 - 4, 0.5), (x1, H * 0.35), (x1 - W * 0.12, H * 0.8), (0, H),
                      (x0 + W * 0.12, H * 0.8), (x0, H * 0.35)])
        cl = shaded(c, bag, 1, "bottom", SHADE, 0.35)
        line(c, smooth([(x0 + W * 0.2, H * 0.6), (0, H * 0.5), (x1 - W * 0.2, H * 0.6)], closed=False), clip=cl)
        line(c, smooth([(-W * 0.1, H * 0.92), (0, H * 0.75), (W * 0.12, H * 0.9)], closed=False), clip=cl)
    elif style == "pouf":
        body = rrect(x0, 0.5, x1, H, H * 0.35)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.35)
        for k in range(-3, 4):
            line(c, [(k * W / 8, 2), (k * W / 8 * 0.9, H - 2)], clip=cl, shade=0.8)
        c.ellipse(0, H - 3, W * 0.12, 1.4, zone=2)


# ------------------------------------------------------------------ Tische
def table(it: Item, style: str = "dining"):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    top_t = {"dining": 5.0, "coffee": 5.0, "side": 4.0, "kids": 4.0, "desk": 4.5, "round": 5.0, "picnic": 5.0}.get(style, 5.0)
    if style == "round":
        leg(c, 0, 4, H - top_t, W * 0.12, W * 0.08)
        c.fill(ell(0, 3, W * 0.28, 3), zone=3, shade=0.9)
    elif style == "desk":
        dw = W * 0.34
        body = rrect(x1 - dw, 1, x1 - 1, H - top_t, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        for i in range(3):
            y = 3 + i * (H - top_t - 5) / 3
            line(c, [(x1 - dw + 1, y + (H - top_t - 5) / 3 - 1), (x1 - 2, y + (H - top_t - 5) / 3 - 1)], clip=cl)
            knob(c, x1 - dw / 2 - 0.5, y + (H - top_t - 5) / 6, 1.0)
        leg(c, x0 + 3.5, 0, H - top_t, 3.4, 3.0)
    elif style == "picnic":
        for sx in (-1, 1):
            c.line([(sx * W * 0.08, H - top_t), (sx * W * 0.4, 1)], 4.0, zone=3, shade=0.95)
        c.fill(rrect(x0 + W * 0.08, H * 0.42, x1 - W * 0.08, H * 0.42 + 4, 1.5), zone=3, shade=0.85)
    else:
        inset = {"dining": 5.0, "coffee": 7.0, "side": 3.5, "kids": 4.0}.get(style, 5.0)
        lw = {"dining": 4.5, "coffee": 4.0, "side": 3.0, "kids": 4.5}.get(style, 4.0)
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - inset), 0, H - top_t, lw, lw * 0.75)
        if style == "dining":
            c.fill(rrect(x0 + inset, H - top_t - 7, x1 - inset, H - top_t, 1), zone=3, shade=0.85)
        if style == "coffee":
            c.fill(rrect(x0 + inset, H * 0.22, x1 - inset, H * 0.22 + 3, 1), zone=3, shade=0.85)
    top = rrect(x0, H - top_t, x1, H, 1.8)
    cl = shaded(c, top, 3 if style in ("dining", "coffee", "picnic", "side") else 1, "bottom", SHADE, 0.4)
    c.fill(rrect(x0 + 1, H - 1.4, x1 - 1, H, 0.8), zone=3 if style in ("dining", "coffee", "picnic", "side") else 1,
           shade=1.0, clip=cl)
    if style in ("dining", "coffee", "picnic", "side"):
        grain(c, x0 + 3, x1 - 3, H - top_t, H - 1.5, cl, n=1)


# ------------------------------------------------------------------ Betten
def bed(it: Item, style: str = "kid", mattress_h: float = 45.0):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "crib":
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 2.5), 0, H, 4.0, 4.0)
        c.fill(rrect(x0 + 2, mattress_h - 12, x1 - 2, mattress_h - 2, 3), zone=2)
        c.fill(rrect(x0 + 2, H - 5, x1 - 2, H - 1, 1.5), zone=3)
        c.fill(rrect(x0 + 2, mattress_h - 16, x1 - 2, mattress_h - 12, 1.5), zone=3)
        n = int(W / 9)
        for i in range(1, n):
            x = x0 + 2 + i * (W - 4) / n
            c.fill(rrect(x - 1.1, mattress_h - 12, x + 1.1, H - 5, 1), zone=3)
        return
    head_h = H
    # Kopfteil (links) und Fußteil (rechts)
    hb = rrect(x0, 0, x0 + 7, head_h, 3)
    shaded(c, hb, 3 if style != "kid" else 1, "right", SHADE, 0.35)
    fb = rrect(x1 - 6, 0, x1, mattress_h + (6 if style != "double" else 4), 3)
    shaded(c, fb, 3 if style != "kid" else 1, "right", SHADE, 0.35)
    if style == "bunk":
        for yy in (mattress_h + 55,):
            shaded(c, rrect(x0 + 4, yy - 20, x1 - 4, yy - 12, 2), 3, "bottom", SHADE, 0.4)
            c.fill(rrect(x0 + 6, yy - 12, x1 - 6, yy - 2, 3), zone=2)
            c.fill(rrect(x0 + 8, yy - 3, x0 + 30, yy + 4, 3), zone=2, shade=1.0)
            cushion(c, x0 + 26, yy - 4, x1 - 6, yy + 1, zone=1, r=3)
        for i in range(6):   # Leiter
            c.line([(x1 - 22, 8 + i * 13), (x1 - 12, 8 + i * 13)], 1.6, zone=3)
        c.line([(x1 - 22, 2), (x1 - 22, mattress_h + 40)], 2.0, zone=3)
        c.line([(x1 - 12, 2), (x1 - 12, mattress_h + 40)], 2.0, zone=3)
    # Rahmen
    frame = rrect(x0 + 4, 8, x1 - 4, mattress_h - 10, 2)
    shaded(c, frame, 3 if style != "kid" else 1, "bottom", SHADE, 0.4)
    for sx in (-1, 1):
        leg(c, sx * (W / 2 - 9), 0, 9, 4, 3.4)
    # Matratze, Decke, Kissen
    c.fill(rrect(x0 + 6, mattress_h - 11, x1 - 6, mattress_h - 1, 3.5), zone=2, shade=1.0)
    pil = smooth([(x0 + 8, mattress_h - 2), (x0 + 7, mattress_h + 7), (x0 + 20, mattress_h + 10),
                  (x0 + 34, mattress_h + 7), (x0 + 33, mattress_h - 2)])
    cl = shaded(c, pil, 2, "bottom", SOFT, 0.35)
    line(c, [(x0 + 14, mattress_h + 4), (x0 + 26, mattress_h + 4)], zone=2, clip=cl)
    blanket = smooth([(x0 + 30, mattress_h + 1), (x0 + 36, mattress_h + 5), (x1 - 10, mattress_h + 4),
                      (x1 - 6, mattress_h - 2), (x1 - 6, mattress_h - 14, "s"), (x0 + 30, mattress_h - 14, "s")])
    cl = shaded(c, blanket, 1, "bottom", SHADE, 0.35)
    c.fill(rrect(x0 + 30, mattress_h - 1, x0 + 42, mattress_h + 5, 2), zone=1, shade=SOFT, clip=cl)
    for k in range(1, 4):
        line(c, [(x0 + 30 + k * (W - 40) / 4, mattress_h + 3), (x0 + 28 + k * (W - 40) / 4, mattress_h - 13)],
             clip=cl, shade=0.8)


# ------------------------------------------------------------------ Schränke & Regale
BOOK_COLS = [1, 2, 3]


def _books(c, x0: float, x1: float, y: float, hmax: float, seed: int):
    x = x0 + 1
    k = seed
    while x < x1 - 3:
        k = (k * 1103515245 + 12345) & 0x7FFFFFFF
        bw = 2.2 + (k % 5) * 0.6
        bh = hmax * (0.62 + (k % 7) * 0.05)
        if x + bw > x1 - 1:
            break
        tilt = (k % 11) == 0
        pts = [(x, y), (x + bw, y), (x + bw, y + bh), (x, y + bh)] if not tilt else \
            [(x, y), (x + bw, y), (x + bw + bh * 0.25, y + bh * 0.97), (x + bh * 0.25, y + bh)]
        z = [1, 2, 3][k % 3]
        c.fill(pts, zone=z, shade=0.9 + (k % 3) * 0.05)
        c.line([(x + bw * 0.2, y + bh * 0.75), (x + bw * 0.8, y + bh * 0.75)], 0.35, zone=z, shade=0.6)
        c.line(pts, 0.25, zone=0, closed=True)
        x += bw + (bh * 0.25 if tilt else 0.3)
        if (k % 13) == 0:
            x += 5


def storage(it: Item, style: str = "bookshelf", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style in ("bookshelf", "shelf_low", "cube"):
        body = rrect(x0, 2, x1, H, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.08)
        c.fill(rrect(x0 + 2.5, 4, x1 - 2.5, H - 2.5, 0.5), zone=1, shade=0.7, clip=cl)    # Rückwand (dunkel)
        rows = max(1, int(round((H - 6) / 36))) if style != "cube" else 2
        rh = (H - 6.5) / rows
        for r in range(rows):
            y = 4 + r * rh
            c.fill([(x0 + 2.5, y), (x1 - 2.5, y), (x1 - 2.5, y + 2), (x0 + 2.5, y + 2)], zone=1)
            if style == "cube":
                c.fill([(-1, 4), (1, 4), (1, H - 2.5), (-1, H - 2.5)], zone=1)
            _books(c, x0 + 2.5, x1 - 2.5 if style != "cube" else -1, y + 2, rh - 4, r * 7 + int(W))
        c.fill([(x0 + 2.5, H - 4.5), (x1 - 2.5, H - 4.5), (x1 - 2.5, H - 2.5), (x0 + 2.5, H - 2.5)], zone=1)
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 3), 0, 3, 3, 2.4)
    elif style in ("wardrobe", "cabinet") and state == "open":
        body = rrect(x0, 3, x1, H, 1.5)
        shaded(c, body, 1, "right", SHADE, 0.12)
        c.fill(rrect(x0 + 2.5, 5, x1 - 2.5, H - 5, 0.8), zone=1, shade=0.62)          # Innenraum
        c.line([(x0 + 4, H - 14), (x1 - 4, H - 14)], 1.2, zone=3)                      # Kleiderstange
        for k in range(5):                                                              # Kleidung
            x = x0 + 8 + k * (W - 16) / 5
            c.fill(rrect(x, H * 0.38 + (k % 2) * 8, x + (W - 16) / 5 - 2, H - 16, 3), zone=[2, 3, 2, 3, 2][k], shade=0.95)
            c.line(rrect(x, H * 0.38 + (k % 2) * 8, x + (W - 16) / 5 - 2, H - 16, 3), 0.3, zone=0, closed=True)
        c.fill(rrect(x0 + 4, 8, x1 - 4, 12, 0.5), zone=1, shade=0.8)
        for sx in (-1, 1):                                                              # offene Türen
            door = [(sx * W / 2, 4), (sx * W * 0.78, 10), (sx * W * 0.78, H - 8), (sx * W / 2, H - 2)]
            shaded(c, door, 1, "bottom", SHADE, 0.2)
            knob(c, sx * W * 0.72, H * 0.5, 1.2)
            leg(c, sx * (W / 2 - 4), 0, 4, 4, 3.2)
    elif style in ("wardrobe", "cabinet"):
        body = rrect(x0, 3, x1, H, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        c.fill(rrect(x0 - 1, H - 5, x1 + 1, H, 1), zone=1, shade=1.0)
        line(c, [(0, 6), (0, H - 6)], clip=cl)
        for sx in (-1, 1):
            c.line(rrect(sx * 2 if sx > 0 else x0 + 3, 7, x1 - 3 if sx > 0 else -2, H - 8, 1.5), 0.3, zone=1,
                   shade=0.75, closed=True)
            knob(c, sx * 4.5, H * 0.5, 1.3)
            leg(c, sx * (W / 2 - 4), 0, 4, 4, 3.2)
    elif style in ("dresser", "nightstand", "tv_bench"):
        top_h = H
        body = rrect(x0, 4, x1, top_h, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        c.fill(rrect(x0 - 1, top_h - 3, x1 + 1, top_h, 1), zone=3)
        n = {"dresser": 3, "nightstand": 2, "tv_bench": 1}[style]
        cols = 2 if style in ("dresser", "tv_bench") and W > 60 else 1
        dh = (top_h - 8) / n
        for r in range(n):
            for k in range(cols):
                a = x0 + 2 + k * (W - 4) / cols
                b = a + (W - 4) / cols - 1.5
                y = 5 + r * dh
                if state == "open" and r == n - 1 and k == 0:        # oberste Schublade gezogen
                    c.fill(rrect(a - 3, y - 2, b + 3, y + dh + 1, 1.2), zone=1, shade=0.62)
                    c.fill(rrect(a - 1, y + dh * 0.45, b + 1, y + dh + 3, 0.8), zone=2)   # Inhalt
                    front = rrect(a - 4, y - 5, b + 4, y + dh - 4, 1.2)
                    shaded(c, front, 1, "bottom", SHADE, 0.3)
                    knob(c, (a + b) / 2, y + dh / 2 - 4.5, 1.1)
                    continue
                c.line(rrect(a, y, b, y + dh - 1.5, 1.2), 0.3, zone=1, shade=0.72, closed=True)
                knob(c, (a + b) / 2, y + dh / 2 - 0.5, 1.1)
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 3), 0, 5, 3, 2.2, zone=3)
    elif style == "toybox":
        body = rrect(x0, 1, x1, H - 5, 2.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.12)
        if state == "open":
            c.fill(rrect(x0 + 2, H - 9, x1 - 2, H - 5, 1), zone=1, shade=0.55)
            lid = [(x0 - 1, H - 6), (x1 + 1, H - 6), (x1 - 4, H + 14), (x0 + 4, H + 14)]
            shaded(c, lid, 2, "bottom", SHADE, 0.3)
            c.ellipse(x0 + W * 0.3, H - 4, 5, 5, zone=3)
            c.ellipse(x0 + W * 0.55, H - 3, 4, 6, zone=2)
        else:
            lid = rrect(x0 - 1, H - 7, x1 + 1, H, 2.5)
            shaded(c, lid, 2, "bottom", SHADE, 0.4)
        for k, (cx, cy, r) in enumerate(((-W * 0.25, H * 0.45, H * 0.14), (W * 0.2, H * 0.4, H * 0.12))):
            c.ellipse(cx, cy, r, r, zone=2)
            c.ellipse(cx, cy, r * 0.45, r * 0.45, zone=3)
        line(c, [(x0 + 3, H * 0.2), (x1 - 3, H * 0.2)], clip=cl)


# ------------------------------------------------------------------ Lampen & Elektronik
def lamp(it: Item, style: str = "floor", state: str = ""):
    c, W, H = it.c, it.w, it.h
    if style in ("floor", "table"):
        sh = H * (0.28 if style == "floor" else 0.45)
        foot_r = W * 0.36
        c.fill(ell(0, 1.5, foot_r, 1.8 if style == "floor" else 1.4), zone=3)
        c.fill(rrect(-0.9, 2, 0.9, H - sh + 1, 0.6), zone=3, shade=0.85)
        if style == "table":
            c.fill(smooth([(-W * 0.22, 2), (W * 0.22, 2), (W * 0.26, H * 0.3), (0, H * 0.55 - sh * 0.3), (-W * 0.26, H * 0.3)]),
                   zone=2)
        shade_pts = [(-W * 0.28, H - sh), (W * 0.28, H - sh)]
        shade_pts = smooth([(-W * 0.5, H - sh, "s"), (W * 0.5, H - sh, "s"), (W * 0.32, H, "s"), (-W * 0.32, H, "s")], n=2)
        if state == "on":   # Lichtkegel unter dem Schirm
            c.glass(smooth([(-W * 0.46, H - sh, "s"), (W * 0.46, H - sh, "s"), (W * 0.9, H - sh * 2.2, "s"),
                            (-W * 0.9, H - sh * 2.2, "s")], n=2), zone=1, opacity=0.28)
        cl = shaded(c, shade_pts, 1, "right", 0.97 if state == "on" else SHADE, 0.25)
        line(c, [(-W * 0.46, H - sh + 2.2), (W * 0.46, H - sh + 2.2)], clip=cl, shade=0.8)
    elif style == "arc":
        c.fill(ell(-W * 0.3, 2, W * 0.16, 2), zone=3)
        c.line(smooth([(-W * 0.3, 2), (-W * 0.28, H * 0.7), (0, H * 0.98), (W * 0.35, H * 0.8)], closed=False), 1.4, zone=3)
        cl = shaded(c, smooth([(W * 0.2, H * 0.7), (W * 0.35, H * 0.86), (W * 0.5, H * 0.7), (W * 0.35, H * 0.66)]), 1,
                    "bottom", SHADE, 0.3)
    elif style == "desk":
        c.fill(ell(0, 1.2, W * 0.3, 1.4), zone=1)
        c.line([(0, 2), (-W * 0.15, H * 0.6), (W * 0.2, H * 0.85)], 1.4, zone=3)
        c.fill(smooth([(W * 0.05, H * 0.8), (W * 0.2, H), (W * 0.48, H * 0.78), (W * 0.3, H * 0.66)]), zone=1)
        c.ellipse(-W * 0.15, H * 0.6, 1.4, 1.4, zone=3)


def tv(it: Item, style: str = "flat", state: str = ""):
    c, W, H = it.c, it.w, it.h
    stand = 8.0
    c.fill(rrect(-W * 0.2, 0, W * 0.2, 2.2, 1), zone=1)
    c.fill(rrect(-2, 2, 2, stand, 0.8), zone=1, shade=0.85)
    body = rrect(-W / 2, stand - 1, W / 2, H, 2)
    c.fill(body, zone=1)
    scr = rrect(-W / 2 + 2.2, stand + 1.2, W / 2 - 2.2, H - 2.2, 1)
    c.fill(scr, zone=0, shade=1.0)
    if state == "on":        # buntes Bild: Himmel, Hügel, Sonne
        c.fill(scr, zone=2)
        c.fill(smooth([(-W / 2 + 2.2, stand + 1.2, "s"), (W / 2 - 2.2, stand + 1.2, "s"), (W / 2 - 2.2, H * 0.45),
                       (W * 0.1, H * 0.6), (-W * 0.2, H * 0.45), (-W / 2 + 2.2, H * 0.55)]), zone=3, clip=c.mask(scr))
        c.ellipse(W * 0.25, H * 0.72, H * 0.1, H * 0.1, zone=1, shade=1.0, clip=c.mask(scr))
    c.fill(smooth([(-W * 0.4, H - 4), (-W * 0.2, H - 4), (-W * 0.36, stand + 3), (-W * 0.44, stand + 3)]), zone=2, alpha=0.18)
