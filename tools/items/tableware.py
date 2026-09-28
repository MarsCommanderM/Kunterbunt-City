"""
Geschirr & Tischzubehör (P07-Inventar): Teetasse mit Untertasse, tiefer Teller, Kinderteller, Weinglas, Saftglas,
Teelöffel, Kanne, Karaffe, Eierbecher, Zuckerdose, Butterdose, Tortenplatte, Salatschüssel, Brotdose, Trinkflasche,
Thermoskanne, Servietten, Tischset.
Zonen: 1 = Hauptfarbe · 2 = Muster/Inhalt · 3 = Metall/Holz/Deckel.
"""
from __future__ import annotations

from .kit import INNER, SHADE, SOFT, Item, ell, knob, line, rrect, shaded, smooth, trap


def tableware(it: Item, style: str = "teacup"):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "teacup":
        c.fill(ell(0, H * 0.1, W / 2, H * 0.1, 28), zone=1, shade=0.9)
        c.line(ell(0, H * 0.1, W / 2, H * 0.1, 28), INNER, zone=0, closed=True)
        c.line(smooth([(W * 0.28, H * 0.75), (W * 0.46, H * 0.65), (W * 0.3, H * 0.4)], closed=False), 1.0, zone=1)
        cup = smooth([(-W * 0.34, H, "s"), (W * 0.34, H, "s"), (W * 0.22, H * 0.2, "s"), (-W * 0.22, H * 0.2, "s")])
        cl = shaded(c, cup, 1, "right", SHADE, 0.25)
        for k in range(4):
            c.ellipse(-W * 0.18 + k * W * 0.12, H * 0.6, 0.6, 0.6, zone=2, clip=cl)
        c.fill(ell(0, H, W * 0.32, H * 0.05, 20), zone=2, shade=0.6)
    elif style in ("plate_deep", "plate_kids"):
        dish = smooth([(x0, H, "s"), (x1, H, "s"), (W * 0.3, 0, "s"), (-W * 0.3, 0, "s")]) if style == "plate_deep" else \
            smooth([(x0, H, "s"), (x1, H, "s"), (W * 0.4, 0, "s"), (-W * 0.4, 0, "s")])
        shaded(c, dish, 1, "bottom", SHADE, 0.35)
        c.fill(rrect(x0 - 0.5, H * 0.75, x1 + 0.5, H, H * 0.12), zone=2 if style == "plate_kids" else 1, shade=1.05)
        if style == "plate_kids":
            for k in range(3):
                c.fill(ell(-W * 0.25 + k * W * 0.25, H * 0.45, W * 0.06, W * 0.06, 12), zone=2)
    elif style in ("glass_wine", "glass_tumbler"):
        if style == "glass_wine":
            c.fill(ell(0, H * 0.02, W * 0.4, H * 0.02, 16), zone=1, alpha=0.8)
            c.line([(0, 0), (0, H * 0.45)], 0.6, zone=1)
            bowl = smooth([(x0, H, "s"), (x1, H, "s"), (W * 0.35, H * 0.55), (0, H * 0.45), (-W * 0.35, H * 0.55)])
            c.glass(bowl, zone=1, opacity=0.4)
            c.fill(smooth([(-W * 0.42, H * 0.7), (W * 0.42, H * 0.7), (W * 0.35, H * 0.55), (0, H * 0.46), (-W * 0.35, H * 0.55)]), zone=2,
                   clip=c.mask(bowl))
            c.line(bowl, INNER * 0.8, zone=0, closed=True)
        else:
            body = trap(-W * 0.4, W * 0.4, 0, x0, x1, H, 0.6)
            c.glass(body, zone=1, opacity=0.45)
            c.fill(trap(-W * 0.4, W * 0.4, 0, -W * 0.45, W * 0.45, H * 0.65, 0.5), zone=2, clip=c.mask(body))
            c.line(body, INNER * 0.8, zone=0, closed=True)
    elif style == "teaspoon":
        c.fill(rrect(-W * 0.12, 0, W * 0.12, H * 0.7, W * 0.1), zone=3)
        c.fill(ell(0, H * 0.84, W * 0.45, H * 0.16, 20), zone=3)
        c.fill(ell(0, H * 0.85, W * 0.3, H * 0.1, 16), zone=3, shade=0.85)
    elif style in ("jug", "carafe", "thermos"):
        if style == "jug":
            c.line(smooth([(W * 0.3, H * 0.8), (W * 0.52, H * 0.7), (W * 0.35, H * 0.3)], closed=False), 1.4, zone=1)
            body = smooth([(-W * 0.36, 0, "s"), (W * 0.36, 0, "s"), (W * 0.36, H * 0.75), (W * 0.3, H), (-W * 0.42, H), (-W * 0.3, H * 0.75)])
            cl = shaded(c, body, 1, "right", SHADE, 0.25)
            c.fill(rrect(-W * 0.36, H * 0.35, W * 0.36, H * 0.45, 0.3), zone=2, clip=cl)
        elif style == "carafe":
            body = smooth([(-W * 0.45, 0, "s"), (W * 0.45, 0, "s"), (W * 0.45, H * 0.4), (W * 0.15, H * 0.7), (W * 0.16, H, "s"),
                           (-W * 0.16, H, "s"), (-W * 0.15, H * 0.7), (-W * 0.45, H * 0.4)])
            c.glass(body, zone=1, opacity=0.45)
            c.fill(rrect(-W * 0.5, 0, W * 0.5, H * 0.38, 2), zone=2, clip=c.mask(body))
            c.line(body, INNER * 0.8, zone=0, closed=True)
        else:
            c.fill(rrect(-W * 0.36, H * 0.86, W * 0.36, H, 1.5), zone=3)
            body = rrect(x0, 0, x1, H * 0.87, W * 0.2)
            cl = shaded(c, body, 1, "right", SHADE, 0.25)
            c.fill(rrect(x0, H * 0.3, x1, H * 0.36, 0.3), zone=2, clip=cl)
    elif style == "egg_cup":
        c.fill(trap(-W * 0.4, W * 0.4, 0, -W * 0.15, W * 0.15, H * 0.3, 0.5), zone=1)
        c.fill(smooth([(0, H), (W * 0.36, H * 0.72), (0, H * 0.35), (-W * 0.36, H * 0.72)]), zone=2)
        cup = smooth([(x0, H * 0.72, "s"), (x1, H * 0.72, "s"), (W * 0.2, H * 0.3), (-W * 0.2, H * 0.3)])
        shaded(c, cup, 1, "right", SHADE, 0.3)
    elif style in ("sugar_bowl", "butter_dish"):
        if style == "sugar_bowl":
            body = smooth([(x0, H * 0.7, "s"), (x1, H * 0.7, "s"), (W * 0.36, 0, "s"), (-W * 0.36, 0, "s")])
            cl = shaded(c, body, 1, "right", SHADE, 0.25)
            for k in range(3):
                c.ellipse(-W * 0.2 + k * W * 0.2, H * 0.4, 0.8, 0.8, zone=2, clip=cl)
            lid = smooth([(x0 + 1, H * 0.7, "s"), (x1 - 1, H * 0.7, "s"), (W * 0.2, H * 0.9), (-W * 0.2, H * 0.9)])
            shaded(c, lid, 1, "bottom", SOFT, 0.3)
            knob(c, 0, H * 0.95, W * 0.08, zone=2)
        else:
            c.fill(rrect(x0, 0, x1, H * 0.2, H * 0.1), zone=1, shade=0.9)
            lid = smooth([(-W * 0.44, H * 0.2, "s"), (W * 0.44, H * 0.2, "s"), (W * 0.4, H * 0.8), (-W * 0.4, H * 0.8)])
            shaded(c, lid, 1, "right", SHADE, 0.25)
            c.fill(rrect(-W * 0.12, H * 0.8, W * 0.12, H, 1), zone=2)
    elif style == "cake_stand":
        c.fill(trap(-W * 0.2, W * 0.2, 0, -W * 0.05, W * 0.05, H * 0.3, 0.5), zone=1)
        c.fill(rrect(-W * 0.04, H * 0.3, W * 0.04, H * 0.5, 0.4), zone=1)
        plate = ell(0, H * 0.52, W / 2, H * 0.05, 32)
        shaded(c, plate, 1, "bottom", SHADE, 0.4)
        cake = rrect(-W * 0.34, H * 0.55, W * 0.34, H * 0.9, 1)
        cl = shaded(c, cake, 2, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.34, H * 0.7, W * 0.34, H * 0.75, 0.3), zone=3, clip=cl)
        c.fill(smooth([(-W * 0.34, H * 0.9), (-W * 0.34, H * 0.82), (-W * 0.2, H * 0.86), (0, H * 0.8), (W * 0.2, H * 0.86),
                       (W * 0.34, H * 0.82), (W * 0.34, H * 0.9)]), zone=3)
        c.fill(ell(0, H * 0.96, W * 0.06, W * 0.06, 12), zone=2, shade=0.7)
    elif style == "salad_bowl":
        bowl = smooth([(x0, H, "s"), (x1, H, "s"), (W * 0.32, H * 0.1), (0, 0), (-W * 0.32, H * 0.1)])
        cl = shaded(c, bowl, 1, "bottom", SHADE, 0.35)
        c.fill(rrect(x0, H * 0.55, x1, H * 0.66, 0.4), zone=2, clip=cl)
        c.fill(rrect(x0 - 0.5, H * 0.92, x1 + 0.5, H, 1), zone=1, shade=1.05)
    elif style == "lunchbox":
        body = rrect(x0, 0, x1, H * 0.75, 2)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(x0 - 0.5, H * 0.62, x1 + 0.5, H, 2), zone=2)
        c.line(rrect(x0 - 0.5, H * 0.62, x1 + 0.5, H, 2), INNER, zone=0, closed=True)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.3 - 1.5, H * 0.55, sx * W * 0.3 + 1.5, H * 0.75, 0.5), zone=3)
        c.fill(ell(0, H * 0.3, W * 0.14, H * 0.14, 16), zone=2, clip=cl)
    elif style == "drink_bottle":
        c.fill(rrect(-W * 0.26, H * 0.85, W * 0.26, H, 1), zone=3)
        c.line(smooth([(W * 0.2, H * 0.95), (W * 0.46, H * 0.92), (W * 0.3, H * 0.84)], closed=False), 0.6, zone=3)
        body = rrect(x0, 0, x1, H * 0.86, W * 0.3)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        for k in range(3):
            c.fill(ell(-W * 0.1 + k * W * 0.1, H * (0.3 + k * 0.15), W * 0.12, W * 0.12, 12), zone=2, clip=cl)
    elif style == "napkins":
        for k in range(4):
            c.fill(rrect(x0 + (k % 2), k * H / 4, x1 - (k % 2), (k + 1) * H / 4 - 0.2, 0.3), zone=[1, 2][k % 2])
            c.line(rrect(x0 + (k % 2), k * H / 4, x1 - (k % 2), (k + 1) * H / 4 - 0.2, 0.3), INNER * 0.6, zone=0, closed=True)
    elif style == "placemat":                                         # flach auf dem Tisch
        body = rrect(x0, 0, x1, H, H * 0.3)
        cl = shaded(c, body, 1, "bottom", SOFT, 0.3)
        for k in range(int(W / 4)):
            line(c, [(x0 + k * 4, 0), (x0 + k * 4, H)], zone=2, clip=cl, shade=1.0)
