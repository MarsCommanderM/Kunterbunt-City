"""
Stadt (P04b-T09): Werkstatt, Läden & Kasse-Waren, Friseur, Rummel, Schule, Gesundheit, Zoo-Zubehör.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Holz/Detail.
"""
from __future__ import annotations

import math

from .kit import SHADE, SOFT, Item, ell, knob, leg, line, rrect, shaded, smooth, trap


# ------------------------------------------------------------------ Werkstatt
def tool(it: Item, style: str = "hammer", state: str = ""):
    c, W, H = it.c, it.w, it.h
    if style == "hammer":
        c.fill(rrect(-W * 0.08, 0, W * 0.08, H * 0.8, W * 0.08), zone=3)
        c.fill(smooth([(-W / 2, H * 0.78, "s"), (W * 0.3, H * 0.78, "s"), (W / 2, H * 0.9), (W * 0.3, H, "s"), (-W / 2, H, "s")]),
               zone=1)
    elif style == "wrench":
        c.fill(rrect(-W * 0.1, 0, W * 0.1, H * 0.75, W * 0.1), zone=1)
        c.fill(ell(0, H * 0.82, W / 2, H * 0.18), zone=1)
        c.erase(rrect(-W * 0.14, H * 0.84, W * 0.14, H + 1, 0.3))
    elif style == "screwdriver":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.45, W * 0.3), zone=1)
        for k in (-0.2, 0.0, 0.2):
            c.line([(k * W, H * 0.05), (k * W, H * 0.4)], 0.3, zone=1, shade=0.7)
        c.fill(rrect(-W * 0.1, H * 0.45, W * 0.1, H, 0.2), zone=3)
    elif style == "saw":
        c.fill(smooth([(-W / 2, H * 0.3, "s"), (W / 2, H * 0.45, "s"), (W / 2, H * 0.6, "s"), (-W * 0.3, H * 0.7, "s")]), zone=3)
        for k in range(10):
            x = -W / 2 + W * k / 10
            c.fill([(x, H * 0.3 + k * H * 0.015), (x + W * 0.05, H * 0.24 + k * H * 0.015), (x + W * 0.1, H * 0.31 + k * H * 0.015)],
                   zone=3, shade=0.75)
        c.fill(smooth([(-W / 2, H * 0.25), (-W * 0.25, H * 0.3), (-W * 0.22, H), (-W / 2, H)]), zone=1)
        c.fill(ell(-W * 0.37, H * 0.65, W * 0.06, H * 0.12), zone=0, alpha=0.9)
    elif style == "drill":
        c.fill(rrect(-W * 0.1, 0, W * 0.2, H * 0.55, 1.2), zone=1)
        body = rrect(-W * 0.3, H * 0.5, W * 0.35, H, 2)
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(rrect(W * 0.35, H * 0.68, W / 2, H * 0.82, 0.3), zone=3)
        c.fill(rrect(-W * 0.18, 0, W * 0.25, H * 0.15, 1), zone=2)
        if state == "on":   # Drehbewegung an der Spitze
            for k in range(3):
                r = 1.2 + k * 0.9
                c.line(smooth([(W / 2 + 0.6, H * 0.75 + r), (W / 2 + 0.6 + r, H * 0.75), (W / 2 + 0.6, H * 0.75 - r)],
                              closed=False, n=6), 0.35, zone=2)
    elif style == "toolbox":
        if state == "open":  # Deckel hinten hoch, Werkzeug schaut heraus
            c.fill(rrect(-W / 2, H * 0.62, W / 2, H * 1.05, 1.5), zone=1, shade=0.72)
            c.fill(rrect(-W * 0.3, H * 0.55, -W * 0.22, H * 1.15, 0.4), zone=3)          # Schraubenzieher
            c.fill(rrect(-W * 0.33, H * 1.05, -W * 0.19, H * 1.3, 0.8), zone=2)
            c.fill(rrect(W * 0.05, H * 0.55, W * 0.12, H * 1.1, 0.4), zone=3, shade=0.8)  # Hammer
            c.fill(rrect(-W * 0.03, H * 1.05, W * 0.25, H * 1.2, 0.6), zone=3)
            c.line(smooth([(W * 0.3, H * 0.6), (W * 0.36, H * 1.1), (W * 0.42, H * 0.6)], closed=False), 0.8, zone=3)
        else:
            c.line(smooth([(-W * 0.2, H * 0.7), (0, H), (W * 0.2, H * 0.7)], closed=False), 1.2, zone=3)
        body = rrect(-W / 2, 0, W / 2, H * 0.72, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W / 2, H * 0.5, W / 2, H * 0.58, 0.3), zone=2, clip=cl)
        knob(c, 0, H * 0.54, 1.2, zone=3)
    elif style == "tire":
        c.fill(ell(0, H / 2, W / 2, H / 2), zone=0, shade=1.0)
        c.fill(ell(0, H / 2, W * 0.28, H * 0.28), zone=3)
        c.fill(ell(0, H / 2, W * 0.08, H * 0.08), zone=0)
        for k in range(12):
            a = math.radians(k * 30)
            c.line([(math.cos(a) * W * 0.4, H / 2 + math.sin(a) * H * 0.4), (math.cos(a) * W * 0.48, H / 2 + math.sin(a) * H * 0.48)],
                   0.6, zone=1, alpha=0.4)
    elif style == "jerrycan":
        body = rrect(-W / 2, 0, W / 2, H * 0.85, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.line([(-W * 0.4, H * 0.1), (W * 0.4, H * 0.75)], 0.8, zone=1, shade=0.75, clip=cl)
        c.fill(rrect(W * 0.1, H * 0.84, W * 0.35, H, 0.5), zone=2)
        c.fill(rrect(-W * 0.4, H * 0.78, -W * 0.05, H * 0.95, 0.8), zone=1)
    elif style == "workbench":
        for sx in (-1, 1):
            leg(c, sx * W * 0.42, 0, H * 0.9, 5, 5, zone=3)
        c.fill(rrect(-W * 0.44, H * 0.2, W * 0.44, H * 0.26, 0.5), zone=3, shade=0.85)
        top = rrect(-W / 2, H * 0.88, W / 2, H, 1)
        shaded(c, top, 1, "bottom", SHADE, 0.4)
        c.fill(rrect(W * 0.2, H * 0.72, W * 0.4, H * 0.88, 0.6), zone=2)
    elif style == "ladder":
        for sx in (-1, 1):
            c.line([(sx * W * 0.45, 0), (sx * W * 0.35, H)], 1.6, zone=1)
        for k in range(1, 8):
            y = H * k / 8
            c.line([(-W * 0.45 + W * 0.1 * k / 8, y), (W * 0.45 - W * 0.1 * k / 8, y)], 1.1, zone=1, shade=0.9)
    elif style == "paint_can":
        body = rrect(-W / 2, 0, W / 2, H * 0.9, 1)
        cl = shaded(c, body, 3, "right", SHADE, 0.2)
        c.fill(rrect(-W / 2, H * 0.2, W / 2, H * 0.62, 0.3), zone=1, clip=cl)
        c.fill(smooth([(-W / 2, H * 0.9), (-W * 0.3, H), (W * 0.1, H * 0.95), (W / 2, H * 0.9), (W / 2, H * 0.78), (-W * 0.2, H * 0.72)]),
               zone=1)
        c.line(smooth([(-W / 2, H * 0.8), (0, H * 1.05), (W / 2, H * 0.8)], closed=False), 0.4, zone=3)
    elif style == "cone_traffic":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.08, 0.3), zone=0)
        body = trap(-W * 0.35, W * 0.35, H * 0.07, -W * 0.06, W * 0.06, H, 0.4)
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        for y in (H * 0.35, H * 0.62):
            c.fill(rrect(-W / 2, y, W / 2, y + H * 0.1, 0.1), zone=2, clip=cl)


# ------------------------------------------------------------------ Läden, Kasse, Friseur
def shop(it: Item, style: str = "cart", state: str = ""):
    c, W, H = it.c, it.w, it.h
    if style == "cart":
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.32, H * 0.06, H * 0.06, H * 0.06), zone=0)
        c.line([(-W * 0.4, H * 0.12), (W * 0.35, H * 0.12)], 1.0, zone=3)
        basket = trap(-W * 0.36, W * 0.34, H * 0.3, -W * 0.46, W * 0.42, H * 0.82, 0.8)
        c.fill(basket, zone=1)
        cl = c.mask(basket)
        for k in range(1, 8):
            c.line([(-W / 2 + W * k / 8, H * 0.28), (-W / 2 + W * k / 8, H * 0.84)], 0.3, zone=1, shade=0.6, clip=cl)
        for k in range(1, 4):
            c.line([(-W / 2, H * (0.3 + k * 0.13)), (W / 2, H * (0.3 + k * 0.13))], 0.3, zone=1, shade=0.6, clip=cl)
        c.line([(W * 0.42, H * 0.82), (W / 2, H)], 1.0, zone=3)
        c.fill(rrect(W * 0.38, H * 0.96, W / 2 + 1, H, 0.4), zone=2)
    elif style == "basket_shop":
        body = trap(-W * 0.4, W * 0.4, 0, -W / 2, W / 2, H * 0.6, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        for k in range(1, 6):
            c.line([(-W / 2 + W * k / 6, 0), (-W / 2 + W * k / 6, H * 0.6)], 0.3, zone=1, shade=0.6, clip=cl)
        c.line(smooth([(-W * 0.35, H * 0.6), (0, H), (W * 0.35, H * 0.6)], closed=False), 0.9, zone=2)
    elif style == "bag":
        body = trap(-W * 0.45, W * 0.45, 0, -W / 2, W / 2, H * 0.8, 0.8)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.ellipse(0, H * 0.4, W * 0.15, W * 0.15, zone=2, clip=cl)
        c.line(smooth([(-W * 0.25, H * 0.78), (0, H), (W * 0.25, H * 0.78)], closed=False), 0.6, zone=2)
    elif style == "box":
        body = rrect(-W / 2, 0, W / 2, H, 0.8)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.08, 0, W * 0.08, H, 0.2), zone=2, clip=cl)
        line(c, [(-W / 2, H * 0.85), (W / 2, H * 0.85)], clip=cl)
    elif style == "cash_register":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.3, 1), zone=1)
        body = trap(-W * 0.45, W * 0.45, H * 0.3, -W * 0.35, W * 0.35, H * 0.62, 1)
        shaded(c, body, 1, "right", SHADE, 0.25)
        for r in range(3):
            for k in range(4):
                c.fill(rrect(-W * 0.3 + k * W * 0.15, H * (0.35 + r * 0.08), -W * 0.2 + k * W * 0.15, H * (0.4 + r * 0.08), 0.3), zone=2)
        c.fill(rrect(-W * 0.25, H * 0.68, W * 0.25, H, 1), zone=1)
        c.fill(rrect(-W * 0.2, H * 0.74, W * 0.2, H * 0.94, 0.5), zone=0, alpha=0.85)
        if state == "open":  # Geldschublade vorne raus, Münzen + Scheine, Anzeige leuchtet
            c.fill(rrect(-W * 0.14, H * 0.8, W * 0.14, H * 0.88, 0.3), zone=2)
            c.fill(rrect(-W * 0.52, H * 0.02, W * 0.52, H * 0.26, 0.8), zone=1, shade=0.85)
            for k in range(4):
                x = -W * 0.4 + k * W * 0.2
                c.fill(rrect(x, H * 0.12, x + W * 0.16, H * 0.24, 0.3), zone=2 if k % 2 else 3, shade=1.0)
            for x in (-W * 0.3, -W * 0.1, W * 0.15):
                c.ellipse(x, H * 0.26, 1.1, 0.6, zone=3, shade=1.0)
    elif style == "price_sign":
        c.fill(rrect(-0.8, 0, 0.8, H * 0.5, 0.4), zone=3)
        c.fill(rrect(-W / 2, H * 0.45, W / 2, H, 1), zone=1)
        c.fill(rrect(-W * 0.35, H * 0.58, W * 0.35, H * 0.88, 0.6), zone=2)
    elif style == "mannequin":
        c.fill(ell(0, H * 0.02, W * 0.3, H * 0.02), zone=3)
        c.fill(rrect(-0.8, 0, 0.8, H * 0.45, 0.4), zone=3)
        body = smooth([(-W * 0.3, H * 0.45), (W * 0.3, H * 0.45), (W * 0.35, H * 0.7), (W / 2, H * 0.82), (W * 0.2, H * 0.86),
                       (-W * 0.2, H * 0.86), (-W / 2, H * 0.82), (-W * 0.35, H * 0.7)])
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(ell(0, H * 0.94, W * 0.16, H * 0.07), zone=2)
    elif style == "hanger_rack":
        for sx in (-1, 1):
            c.line([(sx * W * 0.45, 0), (sx * W * 0.45, H)], 1.2, zone=3)
        c.line([(-W / 2, H), (W / 2, H)], 1.2, zone=3)
        for k in range(5):
            x = -W * 0.35 + k * W * 0.17
            c.fill(trap(x - W * 0.08, x + W * 0.08, H * 0.4, x - W * 0.06, x + W * 0.06, H * 0.95, 0.8), zone=[1, 2, 1, 2, 1][k])
    elif style == "barber_chair":
        c.fill(ell(0, 1, W * 0.35, 1.5), zone=3)
        c.fill(rrect(-2, 1, 2, H * 0.3, 0.8), zone=3)
        seat = rrect(-W * 0.4, H * 0.3, W * 0.4, H * 0.45, 2)
        shaded(c, seat, 1, "bottom", SHADE, 0.35)
        back = rrect(-W * 0.34, H * 0.45, W * 0.34, H * 0.9, 3)
        shaded(c, back, 1, "bottom", SOFT, 0.3)
        c.fill(rrect(-W * 0.18, H * 0.9, W * 0.18, H, 2), zone=1)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.5 - (W * 0.12 if sx < 0 else 0), H * 0.45, sx * W * 0.5 + (0 if sx < 0 else W * 0.12) - sx * 0.1,
                         H * 0.55, 1), zone=3)
    elif style == "hair_tools":
        c.fill(rrect(-W * 0.4, 0, -W * 0.28, H * 0.6, 0.6), zone=1)
        for k in range(8):
            c.line([(-W * 0.28, H * (0.6 + k * 0.05)), (-W * 0.1, H * (0.6 + k * 0.05))], 0.3, zone=1)
        c.fill(rrect(-W * 0.4, H * 0.58, -W * 0.28, H, 0.6), zone=1)
        for sx in (-1, 1):
            c.line(ell(W * 0.25 + sx * W * 0.1, H * 0.15, W * 0.08, H * 0.1, 24), 0.6, zone=2, closed=True)
        c.line([(W * 0.2, H * 0.25), (W * 0.4, H)], 0.7, zone=3)
        c.line([(W * 0.3, H * 0.25), (W * 0.1, H)], 0.7, zone=3)
    elif style == "mirror_stand":
        c.fill(rrect(-W * 0.3, 0, W * 0.3, H * 0.05, 0.5), zone=3)
        c.fill(rrect(-1, 0, 1, H * 0.35, 0.4), zone=3)
        c.fill(ell(0, H * 0.67, W / 2, H * 0.33), zone=1)
        c.fill(ell(0, H * 0.67, W * 0.42, H * 0.28), zone=2)
        c.line([(-W * 0.2, H * 0.55), (-W * 0.05, H * 0.85)], 0.8, zone=1, alpha=0.4)


# ------------------------------------------------------------------ Rummel
def fair(it: Item, style: str = "cotton_candy"):
    c, W, H = it.c, it.w, it.h
    if style == "cotton_candy":
        c.fill(rrect(-W * 0.06, 0, W * 0.06, H * 0.45, 0.3), zone=3)
        for k in range(7):
            a = math.pi * k / 6
            c.fill(ell(math.cos(a) * W * 0.3, H * 0.72 + math.sin(a) * H * 0.12, W * 0.22, H * 0.16), zone=1)
        c.fill(ell(0, H * 0.7, W * 0.45, H * 0.25), zone=1)
    elif style == "popcorn":
        for k in range(8):
            c.fill(ell(-W * 0.35 + k * W * 0.1, H * (0.82 + (k % 2) * 0.1), W * 0.12, H * 0.1), zone=2)
        body = trap(-W * 0.35, W * 0.35, 0, -W / 2, W / 2, H * 0.82, 0.6)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        for k in range(-2, 3):
            c.fill(trap(k * W * 0.18 - W * 0.04, k * W * 0.18 + W * 0.04, 0, k * W * 0.22 - W * 0.05, k * W * 0.22 + W * 0.05, H * 0.82,
                        0.1), zone=3, clip=cl)
    elif style == "prize_teddy":
        from .fun import toy
        toy(it, "teddy")
    elif style == "ticket_booth":
        body = rrect(-W / 2, 0, W / 2, H * 0.75, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.35, H * 0.35, W * 0.35, H * 0.65, 1), zone=0, alpha=0.8)
        c.fill(smooth([(-W * 0.6, H * 0.75, "s"), (W * 0.6, H * 0.75, "s"), (0, H, "s")], n=2), zone=2)
        for k in range(-2, 3):
            c.fill(ell(k * W * 0.22, H * 0.74, W * 0.1, H * 0.05), zone=1)
    elif style == "balloon_bunch":
        for k, (x, y) in enumerate(((-W * 0.25, H * 0.75), (W * 0.2, H * 0.8), (0, H * 0.9), (-W * 0.05, H * 0.66))):
            c.line([(0, 0), (x, y - H * 0.12)], 0.25, zone=3)
            c.fill(ell(x, y, W * 0.22, H * 0.12), zone=[1, 2, 3, 1][k])
            c.line(ell(x, y, W * 0.22, H * 0.12, 32), 0.3, zone=0, closed=True)
    elif style == "target":
        c.fill(rrect(-1, 0, 1, H * 0.4, 0.4), zone=3)
        for k, r in enumerate((0.5, 0.36, 0.22, 0.09)):
            c.fill(ell(0, H * 0.65, W * r, W * r), zone=1 if k % 2 == 0 else 2)
    elif style == "carousel_horse":
        c.fill(rrect(-0.8, 0, 0.8, H, 0.4), zone=3)
        from .fun import toy
        body = ell(0, H * 0.45, W * 0.4, H * 0.14)
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(smooth([(W * 0.25, H * 0.5), (W * 0.4, H * 0.82), (W / 2, H * 0.75), (W * 0.42, H * 0.5)]), zone=1)
        c.fill(smooth([(W * 0.27, H * 0.55), (W * 0.33, H * 0.85), (W * 0.4, H * 0.8), (W * 0.33, H * 0.52)]), zone=2)
        for sx in (-1, 1):
            c.line([(sx * W * 0.25, H * 0.35), (sx * W * 0.3, H * 0.15)], 1.4, zone=1)


# ------------------------------------------------------------------ Schule & Gesundheit
def school(it: Item, style: str = "school_desk"):
    c, W, H = it.c, it.w, it.h
    if style == "school_desk":
        for sx in (-1, 1):
            c.line([(sx * W * 0.4, 0), (sx * W * 0.4, H * 0.92)], 1.4, zone=3)
        c.fill(rrect(-W * 0.45, H * 0.6, W * 0.45, H * 0.7, 0.5), zone=1, shade=0.8)
        top = rrect(-W / 2, H * 0.92, W / 2, H, 0.8)
        shaded(c, top, 1, "bottom", SHADE, 0.4)
    elif style == "blackboard":
        for sx in (-1, 1):
            c.line([(sx * W * 0.35, 0), (sx * W * 0.4, H * 0.4)], 1.4, zone=3)
        c.fill(rrect(-W / 2, H * 0.3, W / 2, H, 1.2), zone=3)
        c.fill(rrect(-W * 0.46, H * 0.34, W * 0.46, H * 0.96, 0.8), zone=1)
        c.line(smooth([(-W * 0.3, H * 0.8), (-W * 0.2, H * 0.85), (-W * 0.1, H * 0.78)], closed=False), 0.4, zone=2)
        c.line([(-W * 0.3, H * 0.6), (W * 0.2, H * 0.6)], 0.4, zone=2)
    elif style == "school_bag":
        body = rrect(-W / 2, 0, W / 2, H * 0.85, W * 0.2)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W / 2, H * 0.45, W / 2, H * 0.85, W * 0.2), zone=2, clip=cl)
        c.fill(rrect(-W * 0.2, H * 0.35, W * 0.2, H * 0.52, 0.5), zone=3)
        c.line(smooth([(-W * 0.2, H * 0.85), (0, H), (W * 0.2, H * 0.85)], closed=False), 0.8, zone=3)
    elif style == "pencil_cup":
        for k, (x, z) in enumerate(((-W * 0.2, 1), (0, 2), (W * 0.2, 3))):
            c.fill(rrect(x - 0.6, H * 0.4, x + 0.6, H * (0.92 + k * 0.03), 0.3), zone=z)
            c.fill([(x - 0.6, H * (0.92 + k * 0.03)), (x + 0.6, H * (0.92 + k * 0.03)), (x, H * (1.0 + k * 0.03))], zone=z, shade=0.7)
        body = rrect(-W / 2, 0, W / 2, H * 0.55, 1)
        shaded(c, body, 1, "right", SHADE, 0.2)
    elif style == "microscope":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.1, 0.8), zone=1)
        c.line(smooth([(-W * 0.2, H * 0.1), (-W * 0.3, H * 0.5), (0, H * 0.8)], closed=False), 2.0, zone=1)
        c.fill(rrect(-W * 0.05, H * 0.35, W * 0.4, H * 0.42, 0.4), zone=3)
        c.line([(W * 0.05, H * 0.45), (W * 0.2, H)], 2.0, zone=2)
    elif style == "easel":
        c.line([(-W * 0.4, 0), (0, H)], 1.2, zone=3)
        c.line([(W * 0.4, 0), (0, H)], 1.2, zone=3)
        c.fill(rrect(-W * 0.35, H * 0.35, W * 0.35, H * 0.9, 0.5), zone=2)
        c.fill(ell(-W * 0.1, H * 0.65, W * 0.12, H * 0.08), zone=1)
        c.fill(ell(W * 0.12, H * 0.55, W * 0.1, H * 0.12), zone=3)
    elif style == "first_aid":
        body = rrect(-W / 2, 0, W / 2, H * 0.85, 1.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.07, H * 0.2, W * 0.07, H * 0.65, 0.3), zone=2)
        c.fill(rrect(-W * 0.2, H * 0.36, W * 0.2, H * 0.5, 0.3), zone=2)
        c.line(smooth([(-W * 0.2, H * 0.85), (0, H), (W * 0.2, H * 0.85)], closed=False), 0.8, zone=3)
    elif style == "stethoscope":
        c.line(smooth([(-W * 0.3, H), (-W * 0.4, H * 0.5), (0, H * 0.25), (W * 0.4, H * 0.5), (W * 0.3, H)], closed=False), 0.8,
               zone=1)
        c.line([(0, H * 0.25), (0, H * 0.1)], 0.8, zone=1)
        c.fill(ell(0, H * 0.08, W * 0.12, W * 0.12), zone=3)
    elif style == "wheelchair":
        c.line(ell(W * 0.1, H * 0.35, H * 0.35, H * 0.35, 40), 1.3, zone=0, closed=True)
        c.ellipse(W * 0.1, H * 0.35, 1.2, 1.2, zone=3)
        c.fill(ell(-W * 0.35, H * 0.08, H * 0.08, H * 0.08), zone=0)
        c.fill(rrect(-W * 0.35, H * 0.42, W * 0.25, H * 0.5, 1), zone=1)
        c.fill(rrect(W * 0.18, H * 0.48, W * 0.3, H, 1), zone=1)
        c.line([(-W * 0.3, H * 0.42), (-W * 0.35, H * 0.08)], 1.0, zone=3)
        c.line([(W * 0.3, H), (W * 0.45, H)], 1.0, zone=3)
    elif style == "hospital_bed":
        from .furniture import bed
        bed(it, "kid", H * 0.6)
    elif style == "bandage":
        c.fill(rrect(-W / 2, 0, W / 2, H, H * 0.4), zone=1)
        c.fill(rrect(-W * 0.15, H * 0.1, W * 0.15, H * 0.9, 0.5), zone=2)
    elif style == "thermometer":
        c.fill(rrect(-W / 2, 0, W / 2, H, W / 2), zone=1)
        c.fill(rrect(-W * 0.18, H * 0.1, W * 0.18, H * 0.6, W * 0.18), zone=2)


# ------------------------------------------------------------------ Zoo-Zubehör
def zoo(it: Item, style: str = "feed_bucket"):
    c, W, H = it.c, it.w, it.h
    if style == "feed_bucket":
        body = trap(-W * 0.38, W * 0.38, 0, -W / 2, W / 2, H * 0.7, 1)
        shaded(c, body, 1, "right", SHADE, 0.2)
        for k in range(-2, 3):
            c.fill(ell(k * W * 0.15, H * 0.72, W * 0.1, H * 0.08), zone=2)
        c.line(smooth([(-W / 2, H * 0.7), (0, H), (W / 2, H * 0.7)], closed=False), 0.6, zone=3)
    elif style == "hay":
        body = rrect(-W / 2, 0, W / 2, H, 1.5)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        for k in range(12):
            y = H * (k + 0.5) / 12
            c.line([(-W / 2, y), (W / 2, y + H * 0.04)], 0.3, zone=1, shade=0.7, clip=cl)
        for x in (-W * 0.25, W * 0.25):
            c.fill(rrect(x - 0.5, 0, x + 0.5, H, 0.2), zone=2, clip=cl)
    elif style == "bowl_pet":
        body = trap(-W * 0.38, W * 0.38, 0, -W / 2, W / 2, H * 0.8, 1)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(ell(0, H * 0.8, W * 0.42, H * 0.18), zone=2)
    elif style == "zoo_sign":
        c.fill(rrect(-1, 0, 1, H * 0.6, 0.4), zone=3)
        c.fill(rrect(-W / 2, H * 0.55, W / 2, H, 1.5), zone=1)
        c.fill(ell(-W * 0.25, H * 0.78, W * 0.14, H * 0.14), zone=2)
        c.line([(-W * 0.05, H * 0.84), (W * 0.35, H * 0.84)], 0.8, zone=2)
        c.line([(-W * 0.05, H * 0.7), (W * 0.25, H * 0.7)], 0.8, zone=2)
    elif style == "pet_bed":
        body = smooth([(-W / 2, H * 0.2), (0, 0), (W / 2, H * 0.2), (W / 2, H * 0.9), (W * 0.35, H), (-W * 0.35, H), (-W / 2, H * 0.9)])
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(ell(0, H * 0.7, W * 0.38, H * 0.22), zone=2)
    elif style == "cage":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.12, 0.8), zone=1)
        for k in range(9):
            x = -W / 2 + W * (k + 0.5) / 9
            c.line([(x, H * 0.12), (x, H * 0.85)], 0.35, zone=3)
        c.fill(smooth([(-W / 2, H * 0.85, "s"), (W / 2, H * 0.85, "s"), (0, H, "s")], n=2), zone=1)
    elif style == "aquarium":
        body = rrect(-W / 2, 0, W / 2, H, 1)
        c.glass(body, zone=2, opacity=0.6)
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.12, 0.5), zone=3)
        c.fill(smooth([(W * 0.1, H * 0.5), (W * 0.25, H * 0.6), (W * 0.35, H * 0.5), (W * 0.25, H * 0.42)]), zone=1)
        c.fill([(W * 0.08, H * 0.5), (0, H * 0.58), (0, H * 0.42)], zone=1)
        c.line(body, 0.4, zone=0, closed=True)
        c.fill(rrect(-W / 2, H * 0.9, W / 2, H, 0.5), zone=1)
