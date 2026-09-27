"""
Draußen (P04b-T09): Garten, Grill, Camping (Zelte, Lagerfeuer), Wald, Spielplatz, Fahrräder & Verleih,
Sport, Eishalle. Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Holz/Metall/Detail.
"""
from __future__ import annotations

import math
import random

from .kit import SHADE, SOFT, Item, ell, knob, leg, line, rrect, shaded, smooth, trap
from .plants import leaf


# ------------------------------------------------------------------ Garten & Grill
def garden(it: Item, style: str = "grill"):
    c, W, H = it.c, it.w, it.h
    if style == "grill":
        for sx in (-1, 1):
            c.line([(sx * W * 0.1, H * 0.55), (sx * W * 0.4, 0)], 1.4, zone=3)
        c.fill(ell(0, 1.5, W * 0.1, 1.5), zone=3)
        bowl = smooth([(-W / 2, H * 0.72, "s"), (W / 2, H * 0.72, "s"), (W * 0.3, H * 0.45), (-W * 0.3, H * 0.45)])
        shaded(c, bowl, 1, "bottom", SHADE, 0.4)
        c.fill(rrect(-W / 2, H * 0.7, W / 2, H * 0.76, 0.3), zone=3)
        lid = smooth([(-W * 0.48, H * 0.78, "s"), (W * 0.48, H * 0.78, "s"), (W * 0.3, H * 0.95), (0, H), (-W * 0.3, H * 0.95)])
        shaded(c, lid, 1, "bottom", SOFT, 0.3)
        c.ellipse(0, H, 1.2, 1.0, zone=3)
    elif style == "bbq_food":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.3, 1), zone=3)
        for k, x in enumerate((-W * 0.3, 0, W * 0.3)):
            c.fill(rrect(x - W * 0.12, H * 0.3, x + W * 0.12, H, W * 0.1), zone=1 if k != 1 else 2)
    elif style == "watering_can":
        c.fill(smooth([(W * 0.2, H * 0.4, "s"), (W / 2, H * 0.9, "s"), (W / 2 + 1, H * 0.85, "s"), (W * 0.24, H * 0.3, "s")]), zone=1)
        body = rrect(-W * 0.4, 0, W * 0.25, H * 0.7, 2)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.line(smooth([(-W * 0.3, H * 0.7), (-W * 0.1, H), (W * 0.15, H * 0.7)], closed=False), 1.0, zone=1)
        c.ellipse(-W * 0.08, H * 0.35, W * 0.12, W * 0.12, zone=2, clip=cl)
    elif style == "wheelbarrow":
        c.fill(ell(W * 0.3, H * 0.2, H * 0.2, H * 0.2), zone=0)
        c.fill(ell(W * 0.3, H * 0.2, H * 0.09, H * 0.09), zone=3)
        c.line([(-W / 2, H * 0.65), (W * 0.3, H * 0.2)], 1.2, zone=3)
        c.line([(-W * 0.2, H * 0.5), (-W * 0.25, 0)], 1.2, zone=3)
        tub = smooth([(-W * 0.35, H, "s"), (W * 0.45, H, "s"), (W * 0.25, H * 0.45), (-W * 0.2, H * 0.45)])
        shaded(c, tub, 1, "bottom", SHADE, 0.35)
    elif style == "gnome":
        c.fill(trap(-W * 0.4, W * 0.4, 0, -W * 0.3, W * 0.3, H * 0.45, 1), zone=2)
        c.fill(ell(0, H * 0.5, W * 0.22, H * 0.12), zone=3, shade=1.0)
        c.fill(smooth([(-W * 0.25, H * 0.5), (0, H * 0.3), (W * 0.25, H * 0.5)]), zone=3, shade=1.0)
        c.fill([(-W * 0.3, H * 0.55), (W * 0.3, H * 0.55), (0, H)], zone=1)
        c.ellipse(0, H * 0.47, 1.0, 0.8, zone=1, shade=0.9)
    elif style == "birdhouse":
        c.fill(rrect(-1, 0, 1, H * 0.5, 0.5), zone=3)
        body = rrect(-W * 0.35, H * 0.5, W * 0.35, H * 0.85, 0.8)
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill([(-W / 2, H * 0.82), (W / 2, H * 0.82), (0, H)], zone=2)
        c.fill(ell(0, H * 0.68, W * 0.1, W * 0.1), zone=0)
    elif style == "fence":
        for k in range(5):
            x = -W / 2 + W * (k + 0.5) / 5
            c.fill([(x - W * 0.07, 0), (x + W * 0.07, 0), (x + W * 0.07, H * 0.85), (x, H), (x - W * 0.07, H * 0.85)], zone=1)
            c.line([(x - W * 0.07, 0), (x - W * 0.07, H * 0.85), (x, H), (x + W * 0.07, H * 0.85), (x + W * 0.07, 0)], 0.3, zone=0)
        for y in (H * 0.25, H * 0.65):
            c.fill(rrect(-W / 2, y, W / 2, y + H * 0.08, 0.4), zone=1, shade=0.88)
    elif style == "bench":
        for sx in (-1, 1):
            leg(c, sx * W * 0.4, 0, H * 0.5, 3, 3, zone=3)
        c.fill(rrect(-W / 2, H * 0.45, W / 2, H * 0.52, 0.8), zone=1)
        for y in (H * 0.7, H * 0.86):
            c.fill(rrect(-W / 2, y, W / 2, y + H * 0.08, 0.8), zone=1)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.4 - 1, H * 0.5, sx * W * 0.4 + 1, H, 0.5), zone=3)
    elif style == "pool_kids":
        body = smooth([(-W / 2, H * 0.2), (0, 0), (W / 2, H * 0.2), (W / 2, H * 0.8), (0, H), (-W / 2, H * 0.8)])
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(ell(0, H * 0.8, W * 0.44, H * 0.18), zone=2)
        for k in (-1, 1):
            line(c, [(-W / 2, H * (0.5 + k * 0.12)), (W / 2, H * (0.5 + k * 0.12))], shade=0.8)
    elif style == "sandbox_toys":
        c.fill(smooth([(-W / 2, 0), (W / 2, 0), (W * 0.35, H * 0.5), (-W * 0.35, H * 0.5)]), zone=3)
        for k, x in enumerate((-W * 0.25, W * 0.15)):
            c.fill(trap(x - W * 0.12, x + W * 0.12, H * 0.3, x - W * 0.16, x + W * 0.16, H * 0.8, 0.6), zone=1 + k)
    elif style == "hose":
        for r in range(4):
            c.line(ell(0, H * 0.5, W * (0.5 - r * 0.08), H * (0.5 - r * 0.08), 48), 1.6, zone=1, closed=True)
        c.fill(rrect(W * 0.3, H * 0.1, W * 0.5, H * 0.25, 0.6), zone=2)


# ------------------------------------------------------------------ Camping & Wald
def camping(it: Item, style: str = "tent"):
    c, W, H = it.c, it.w, it.h
    if style == "tent":
        body = smooth([(-W / 2, 0, "s"), (W / 2, 0, "s"), (W * 0.08, H, "s"), (-W * 0.08, H, "s")])
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        door = [(-W * 0.18, 0), (W * 0.18, 0), (0, H * 0.7)]
        c.fill(door, zone=0, alpha=0.8)
        c.fill([(W * 0.02, 0), (W * 0.18, 0), (0.5, H * 0.66)], zone=2)
        line(c, [(0, H), (0, H * 0.7)], zone=1, clip=cl)
        for sx in (-1, 1):
            c.line([(sx * W * 0.06, H * 0.98), (sx * W * 0.2, H + 3)], 0.4, zone=3)
    elif style == "dome_tent":
        body = smooth([(-W / 2, 0, "s"), (W / 2, 0, "s"), (W * 0.35, H * 0.75), (0, H), (-W * 0.35, H * 0.75)])
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        c.fill(smooth([(-W * 0.2, 0, "s"), (W * 0.2, 0, "s"), (W * 0.12, H * 0.55), (0, H * 0.62), (-W * 0.12, H * 0.55)]), zone=2)
        for k in (-0.25, 0.25):
            c.line(smooth([(k * W * 1.8, 0), (k * W, H * 0.8), (0, H)], closed=False), 0.35, zone=1, shade=0.7, clip=cl)
    elif style == "campfire":
        for k, a in enumerate((-25, 25, -10, 10)):
            c.line([(-W * 0.4 + k * 2, 1), (W * 0.4 - k * 2, H * 0.12)], 2.2, zone=3, shade=0.9 - k * 0.05)
        c.fill(smooth([(0, H), (W * 0.3, H * 0.4), (W * 0.2, H * 0.12), (-W * 0.2, H * 0.12), (-W * 0.3, H * 0.4)]), zone=1)
        c.fill(smooth([(0, H * 0.7), (W * 0.15, H * 0.3), (0, H * 0.15), (-W * 0.15, H * 0.3)]), zone=2)
        for k in range(4):
            a = math.radians(200 + k * 45)
            c.fill(ell(math.cos(a) * W * 0.42, 1.5 + abs(math.sin(a)) * 1, 2.2, 1.6), zone=3, shade=0.55)
    elif style == "sleeping_bag":
        body = rrect(-W / 2, 0, W / 2, H, H * 0.45)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(rrect(-W / 2, 0, -W * 0.3, H, H * 0.45), zone=2, clip=cl)
        line(c, [(-W * 0.28, H * 0.5), (W * 0.45, H * 0.5)], clip=cl, shade=0.75)
    elif style == "lantern":
        c.line(smooth([(-W * 0.3, H * 0.85), (0, H), (W * 0.3, H * 0.85)], closed=False), 0.6, zone=3)
        c.fill(rrect(-W * 0.4, 0, W * 0.4, H * 0.12, 0.6), zone=1)
        c.glass(rrect(-W * 0.32, H * 0.12, W * 0.32, H * 0.72, 1), zone=2, opacity=0.75)
        c.line(rrect(-W * 0.32, H * 0.12, W * 0.32, H * 0.72, 1), 0.3, zone=0, closed=True)
        c.fill(trap(-W * 0.4, W * 0.4, H * 0.7, -W * 0.2, W * 0.2, H * 0.86, 0.6), zone=1)
    elif style == "camp_chair":
        c.line([(-W * 0.4, 0), (W * 0.35, H * 0.55)], 1.2, zone=3)
        c.line([(W * 0.4, 0), (-W * 0.35, H * 0.55)], 1.2, zone=3)
        c.fill(smooth([(-W * 0.42, H * 0.5), (W * 0.42, H * 0.5), (W * 0.36, H), (-W * 0.36, H)]), zone=1)
        c.fill(smooth([(-W * 0.44, H * 0.4), (W * 0.44, H * 0.4), (W * 0.4, H * 0.55), (-W * 0.4, H * 0.55)]), zone=2)
    elif style == "backpack_hiking":
        body = rrect(-W / 2, 0, W / 2, H * 0.9, W * 0.3)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W * 0.35, H * 0.08, W * 0.35, H * 0.4, 1.5), zone=2)
        c.fill(rrect(-W * 0.45, H * 0.66, W * 0.45, H * 0.9, W * 0.2), zone=2)
        c.fill(rrect(-W * 0.4, H * 0.9, W * 0.4, H, 1.5), zone=3)
    elif style == "log":
        body = rrect(-W / 2, 0, W / 2, H, H * 0.45)
        cl = shaded(c, body, 3, "bottom", SHADE, 0.35)
        c.fill(ell(W / 2 - H * 0.3, H / 2, H * 0.3, H * 0.48), zone=2)
        c.line(ell(W / 2 - H * 0.3, H / 2, H * 0.16, H * 0.25), 0.3, zone=3, closed=True)
        for k in range(3):
            line(c, [(-W * 0.4 + k * W * 0.2, H * 0.35), (-W * 0.25 + k * W * 0.2, H * 0.4)], zone=3, clip=cl, shade=0.6)
    elif style == "stump":
        body = trap(-W / 2, W / 2, 0, -W * 0.42, W * 0.42, H * 0.85, 1)
        shaded(c, body, 3, "right", SHADE, 0.3)
        c.fill(ell(0, H * 0.86, W * 0.42, H * 0.14), zone=2)
        c.line(ell(0, H * 0.86, W * 0.22, H * 0.07), 0.3, zone=3, closed=True)
    elif style == "mushroom":
        c.fill(rrect(-W * 0.15, 0, W * 0.15, H * 0.55, W * 0.1), zone=2)
        cap = smooth([(-W / 2, H * 0.5, "s"), (W / 2, H * 0.5, "s"), (W * 0.35, H * 0.9), (0, H), (-W * 0.35, H * 0.9)])
        cl = shaded(c, cap, 1, "bottom", SHADE, 0.3)
        for (x, y, r) in ((-W * 0.2, H * 0.72, W * 0.08), (W * 0.15, H * 0.8, W * 0.06), (W * 0.3, H * 0.6, W * 0.05)):
            c.fill(ell(x, y, r, r), zone=2, clip=cl)
    elif style == "tree":
        rnd = random.Random(int(W * 13 + H))
        c.fill(trap(-W * 0.08, W * 0.08, 0, -W * 0.05, W * 0.05, H * 0.5, 0.6), zone=3, shade=0.6)
        for k in range(8):
            a = 2 * math.pi * k / 8
            c.fill(ell(math.cos(a) * W * 0.28, H * 0.68 + math.sin(a) * H * 0.16, W * 0.26, W * 0.24), zone=1,
                   shade=rnd.choice([1.0, 0.9, 0.84]))
        c.fill(ell(0, H * 0.68, W * 0.38, H * 0.25), zone=1)
    elif style == "fir":
        c.fill(rrect(-W * 0.06, 0, W * 0.06, H * 0.2, 0.4), zone=3, shade=0.6)
        for k in range(4):
            y0 = H * (0.12 + k * 0.2)
            w = W * (0.5 - k * 0.1)
            c.fill(smooth([(-w, y0, "s"), (w, y0, "s"), (0, y0 + H * 0.34, "s")], n=2), zone=1, shade=1.0 - k * 0.04)
            c.line(smooth([(-w, y0, "s"), (w, y0, "s"), (0, y0 + H * 0.34, "s")], n=2), 0.3, zone=0, closed=True)
    elif style == "bush":
        for k in range(6):
            a = math.pi * (0.1 + 0.8 * k / 5)
            c.fill(ell(math.cos(a) * W * 0.3, H * 0.35 + math.sin(a) * H * 0.3, W * 0.24, H * 0.3), zone=1,
                   shade=[1.0, 0.9, 0.86][k % 3])
        c.fill(ell(0, H * 0.4, W * 0.45, H * 0.38), zone=1)
        for k in range(5):
            c.ellipse(-W * 0.3 + k * W * 0.15, H * (0.3 + (k % 2) * 0.3), 1.0, 1.0, zone=2)
    elif style == "rock":
        body = smooth([(-W / 2, 0, "s"), (W / 2, 0, "s"), (W * 0.42, H * 0.6), (W * 0.1, H), (-W * 0.35, H * 0.8)])
        cl = shaded(c, body, 1, "right", SHADE, 0.35)
        line(c, [(-W * 0.1, H * 0.7), (W * 0.1, H * 0.4)], clip=cl, shade=0.72)
    elif style == "signpost":
        c.fill(rrect(-1.2, 0, 1.2, H, 0.6), zone=3)
        for k, (y, d) in enumerate(((H * 0.78, 1), (H * 0.58, -1))):
            pts = [(0, y), (d * W * 0.4, y), (d * W / 2, y + H * 0.06), (d * W * 0.4, y + H * 0.12), (0, y + H * 0.12)]
            c.fill(pts, zone=1 + k)
            c.line(pts, 0.3, zone=0, closed=True)
    elif style == "binoculars":
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.25 - W * 0.2, 0, sx * W * 0.25 + W * 0.2, H * 0.8, W * 0.12), zone=1)
            c.fill(ell(sx * W * 0.25, H * 0.8, W * 0.18, H * 0.12), zone=2)
        c.fill(rrect(-W * 0.1, H * 0.4, W * 0.1, H * 0.6, 0.5), zone=3)


# ------------------------------------------------------------------ Spielplatz & Fahrräder
def playground(it: Item, style: str = "slide"):
    c, W, H = it.c, it.w, it.h
    if style == "slide":
        c.line([(-W * 0.4, 0), (-W * 0.4, H)], 1.6, zone=3)
        c.line([(-W * 0.2, 0), (-W * 0.2, H)], 1.6, zone=3)
        for k in range(1, 7):
            c.line([(-W * 0.4, H * k / 7), (-W * 0.2, H * k / 7)], 1.0, zone=3)
        c.fill(smooth([(-W * 0.22, H * 0.92, "s"), (-W * 0.1, H * 0.92), (W * 0.3, H * 0.2), (W / 2, H * 0.1, "s"), (W / 2, 0, "s"),
                       (W * 0.25, H * 0.08), (-W * 0.2, H * 0.8, "s")]), zone=1)
        c.fill(rrect(-W * 0.45, H * 0.9, -W * 0.1, H * 0.96, 0.6), zone=2)
    elif style == "swing":
        c.line([(-W / 2, 0), (-W * 0.35, H)], 1.6, zone=3)
        c.line([(W / 2, 0), (W * 0.35, H)], 1.6, zone=3)
        c.fill(rrect(-W * 0.4, H * 0.95, W * 0.4, H, 0.5), zone=3)
        for sx in (-1, 1):
            c.line([(sx * W * 0.12, H * 0.96), (sx * W * 0.12, H * 0.28)], 0.3, zone=0)
        c.fill(rrect(-W * 0.16, H * 0.25, W * 0.16, H * 0.3, 0.6), zone=1)
    elif style == "seesaw":
        c.fill(trap(-W * 0.08, W * 0.08, 0, -W * 0.03, W * 0.03, H * 0.6, 0.6), zone=3)
        c.fill(rrect(-W / 2, H * 0.55, W / 2, H * 0.7, 1), zone=1)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.4 - 0.6, H * 0.7, sx * W * 0.4 + 0.6, H, 0.4), zone=2)
    elif style == "bicycle":
        for sx in (-1, 1):
            c.line(ell(sx * W * 0.3, H * 0.3, H * 0.3, H * 0.3, 40), 1.2, zone=0, closed=True)
            c.ellipse(sx * W * 0.3, H * 0.3, 0.8, 0.8, zone=3)
            for k in range(6):
                a = math.radians(k * 30)
                c.line([(sx * W * 0.3 - math.cos(a) * H * 0.27, H * 0.3 - math.sin(a) * H * 0.27),
                        (sx * W * 0.3 + math.cos(a) * H * 0.27, H * 0.3 + math.sin(a) * H * 0.27)], 0.15, zone=3)
        c.line([(-W * 0.3, H * 0.3), (-W * 0.02, H * 0.3), (W * 0.18, H * 0.7), (-W * 0.12, H * 0.7), (-W * 0.02, H * 0.3)], 1.1,
               zone=1)
        c.line([(-W * 0.3, H * 0.3), (-W * 0.12, H * 0.7)], 1.1, zone=1)
        c.line([(W * 0.3, H * 0.3), (W * 0.16, H * 0.82)], 1.1, zone=1)
        c.line([(W * 0.1, H * 0.86), (W * 0.24, H * 0.86)], 1.0, zone=3)
        c.fill(rrect(-W * 0.2, H * 0.74, -W * 0.04, H * 0.8, 0.5), zone=2)
        c.fill(ell(-W * 0.02, H * 0.3, 1.4, 1.4), zone=3)
    elif style == "tricycle":
        c.line(ell(W * 0.3, H * 0.35, H * 0.35, H * 0.35, 40), 1.4, zone=0, closed=True)
        for sx in (-1,):
            c.line(ell(-W * 0.3, H * 0.2, H * 0.2, H * 0.2, 32), 1.2, zone=0, closed=True)
        c.fill(rrect(-W * 0.4, H * 0.3, W * 0.1, H * 0.4, 0.6), zone=1)
        c.line([(W * 0.3, H * 0.35), (W * 0.15, H * 0.9)], 1.2, zone=1)
        c.line([(W * 0.05, H * 0.9), (W * 0.25, H * 0.9)], 1.0, zone=3)
        c.fill(rrect(-W * 0.2, H * 0.45, 0, H * 0.52, 0.5), zone=2)
    elif style == "scooter":
        c.line(ell(-W * 0.4, H * 0.08, H * 0.08, H * 0.08, 24), 0.8, zone=0, closed=True)
        c.line(ell(W * 0.4, H * 0.08, H * 0.08, H * 0.08, 24), 0.8, zone=0, closed=True)
        c.fill(rrect(-W * 0.4, H * 0.1, W * 0.35, H * 0.16, 0.5), zone=1)
        c.line([(W * 0.4, H * 0.1), (W * 0.32, H)], 1.2, zone=1)
        c.line([(W * 0.2, H), (W * 0.45, H)], 1.0, zone=2)
    elif style == "helmet":
        body = smooth([(-W / 2, 0, "s"), (W / 2, 0, "s"), (W * 0.45, H * 0.6), (0, H), (-W * 0.45, H * 0.6)])
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        for k in (-0.2, 0.1):
            c.fill(rrect(k * W, H * 0.5, k * W + W * 0.12, H * 0.85, 1), zone=2, clip=cl)
    elif style == "bike_rack":
        for k in range(4):
            x = -W / 2 + W * (k + 0.5) / 4
            c.line(smooth([(x - W * 0.08, 0), (x - W * 0.08, H * 0.7), (x, H), (x + W * 0.08, H * 0.7), (x + W * 0.08, 0)],
                          closed=False), 1.2, zone=1)
    elif style == "sandpit":
        body = rrect(-W / 2, 0, W / 2, H, 1)
        c.fill(body, zone=3)
        c.fill(smooth([(-W / 2 + 3, H - 2), (-W * 0.2, H + 3), (W * 0.2, H + 1), (W / 2 - 3, H - 2)]), zone=1)


# ------------------------------------------------------------------ Sport & Eishalle
def sport(it: Item, style: str = "goal"):
    c, W, H = it.c, it.w, it.h
    if style == "goal":
        c.line([(-W / 2, 0), (-W / 2, H), (W / 2, H), (W / 2, 0)], 2.0, zone=1)
        for k in range(1, 8):
            c.line([(-W / 2 + W * k / 8, 0), (-W / 2 + W * k / 8, H)], 0.25, zone=2)
        for k in range(1, 5):
            c.line([(-W / 2, H * k / 5), (W / 2, H * k / 5)], 0.25, zone=2)
    elif style == "basket_hoop":
        c.fill(rrect(-1.5, 0, 1.5, H * 0.75, 0.6), zone=3)
        c.fill(rrect(-W / 2, H * 0.72, W / 2, H, 1), zone=2)
        c.line(rrect(-W * 0.2, H * 0.76, W * 0.2, H * 0.9, 0.5), 0.4, zone=1, closed=True)
        c.line([(-W * 0.2, H * 0.72), (W * 0.2, H * 0.72)], 0.9, zone=1)
        for k in range(-2, 3):
            c.line([(k * W * 0.08, H * 0.72), (k * W * 0.05, H * 0.6)], 0.2, zone=2)
    elif style == "racket":
        c.fill(rrect(-W * 0.08, 0, W * 0.08, H * 0.4, W * 0.08), zone=3)
        head = ell(0, H * 0.68, W / 2, H * 0.3)
        c.line(head, 1.2, zone=1, closed=True)
        for k in range(-3, 4):
            c.line([(k * W * 0.12, H * 0.42), (k * W * 0.12, H * 0.94)], 0.15, zone=2, clip=c.mask(head))
            c.line([(-W / 2, H * 0.68 + k * H * 0.07), (W / 2, H * 0.68 + k * H * 0.07)], 0.15, zone=2, clip=c.mask(head))
    elif style == "bat":
        c.fill(trap(-W * 0.2, W * 0.2, 0, -W / 2, W / 2, H, W * 0.4), zone=1)
        c.fill(rrect(-W * 0.25, 0, W * 0.25, H * 0.22, W * 0.2), zone=2)
    elif style == "dumbbell":
        c.fill(rrect(-W * 0.3, H * 0.4, W * 0.3, H * 0.6, 0.5), zone=3)
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.3 - (W * 0.2 if sx < 0 else 0), 0, sx * W * 0.3 + (0 if sx < 0 else W * 0.2), H, 1), zone=1)
    elif style == "mat":
        body = rrect(-W / 2, 0, W / 2, H, H * 0.4)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.35)
        line(c, [(-W / 2, H / 2), (W / 2, H / 2)], zone=2, clip=cl, w=0.6, shade=1.0)
    elif style == "cone":
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.1, 0.4), zone=1)
        body = trap(-W * 0.38, W * 0.38, H * 0.08, -W * 0.08, W * 0.08, H, 0.4)
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        c.fill(rrect(-W / 2, H * 0.4, W / 2, H * 0.55, 0.2), zone=2, clip=cl)
    elif style == "trophy":
        c.fill(rrect(-W * 0.35, 0, W * 0.35, H * 0.14, 0.6), zone=3)
        c.fill(rrect(-W * 0.08, H * 0.14, W * 0.08, H * 0.4, 0.5), zone=1)
        cup = smooth([(-W * 0.4, H, "s"), (W * 0.4, H, "s"), (W * 0.3, H * 0.6), (0, H * 0.4), (-W * 0.3, H * 0.6)])
        shaded(c, cup, 1, "right", SHADE, 0.3)
        for sx in (-1, 1):
            c.line(smooth([(sx * W * 0.38, H * 0.9), (sx * W / 2, H * 0.75), (sx * W * 0.3, H * 0.6)], closed=False), 0.8, zone=1)
    elif style == "skates":
        for sx in (-1, 1):
            x = sx * W * 0.25
            boot = smooth([(x - W * 0.2, H * 0.2, "s"), (x + W * 0.22, H * 0.2, "s"), (x + W * 0.24, H * 0.4), (x + W * 0.02, H * 0.5),
                           (x + W * 0.04, H), (x - W * 0.18, H)])
            shaded(c, boot, 1, "bottom", SHADE, 0.3)
            c.fill(rrect(x - W * 0.22, 0, x + W * 0.24, H * 0.06, 0.3), zone=3)
            c.line([(x - W * 0.12, H * 0.06), (x - W * 0.12, H * 0.2)], 0.6, zone=3)
            c.line([(x + W * 0.14, H * 0.06), (x + W * 0.14, H * 0.2)], 0.6, zone=3)
            for k in range(3):
                c.line([(x - W * 0.08, H * (0.55 + k * 0.12)), (x + W * 0.0, H * (0.55 + k * 0.12))], 0.3, zone=2)
    elif style == "hockey_stick":
        c.line([(W * 0.3, H), (-W * 0.2, H * 0.1)], 1.6, zone=1)
        c.fill(smooth([(-W * 0.25, H * 0.12, "s"), (-W / 2, 0.5), (-W / 2, 0, "s"), (-W * 0.15, 0, "s")]), zone=1)
        c.fill(rrect(W * 0.2, H * 0.82, W * 0.35, H, 0.4), zone=2)
    elif style == "puck":
        c.fill(rrect(-W / 2, 0, W / 2, H, H * 0.3), zone=1)
        c.fill(ell(0, H * 0.8, W * 0.45, H * 0.2), zone=1, shade=0.8)
    elif style == "sled":
        for sx in (-1, 1):
            c.line([(sx * W * 0.3, H * 0.2), (sx * W * 0.3, H * 0.6)], 1.2, zone=3)
        c.line(smooth([(-W / 2, H * 0.1), (W * 0.4, H * 0.1), (W / 2, H * 0.4)], closed=False), 1.0, zone=3)
        c.fill(rrect(-W * 0.45, H * 0.55, W * 0.42, H * 0.7, 1), zone=1)
        c.fill(rrect(-W * 0.45, H * 0.7, -W * 0.3, H, 0.8), zone=1)
    elif style == "snowman":
        for (y, r) in ((H * 0.22, W * 0.5), (H * 0.58, W * 0.36), (H * 0.84, W * 0.25)):
            c.fill(ell(0, y, r, r), zone=2)
            c.line(ell(0, y, r, r), 0.3, zone=0, closed=True)
        c.fill([(0, H * 0.84), (W * 0.35, H * 0.82), (0, H * 0.8)], zone=1)
        for sx in (-1, 1):
            c.ellipse(sx * W * 0.1, H * 0.88, 0.8, 0.8, zone=0)
        c.fill(rrect(-W * 0.3, H * 0.66, W * 0.3, H * 0.72, 0.6), zone=3)
        c.fill(rrect(-W * 0.18, H * 0.95, W * 0.18, H, 0.4), zone=0)
