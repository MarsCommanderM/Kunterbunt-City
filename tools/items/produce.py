"""
Obst & Gemüse (P07-Inventar): Trauben, Erdbeere, Kirschen, Ananas, Kiwi, Pflaume, Mango, Honigmelone, Aprikose,
Heidelbeeren, Kokosnuss; Gurke, Kartoffel, Zwiebel, Paprika, Brokkoli, Salat, Mais, Kürbis, Aubergine, Erbsen,
Radieschen, Pilz, Knoblauch, Zucchini, Blumenkohl, Lauch.
Zonen: 1 = Frucht · 2 = Zweitfarbe (Fruchtfleisch, Kappe, Punkte) · 3 = Grün (Stiel, Blätter).
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, ell, line, rrect, shaded, smooth, trap


def _stem(c, x: float, y: float, h: float, lean: float = 0.3):
    c.line([(x, y), (x + lean * h, y + h)], max(0.4, h * 0.12), zone=3, shade=0.8)


def _leafy(c, x: float, y: float, w: float, h: float, n: int = 3, zone: int = 3):
    for k in range(n):
        a = -0.6 + 1.2 * k / max(1, n - 1)
        pts = smooth([(x, y, "s"), (x + math.sin(a) * w * 0.6 - w * 0.12, y + h * 0.6), (x + math.sin(a) * w, y + h, "s"),
                      (x + math.sin(a) * w * 0.6 + w * 0.12, y + h * 0.6)])
        c.fill(pts, zone=zone, shade=1.0 - abs(a) * 0.1)
        c.line(pts, INNER * 0.7, zone=0, closed=True)


def produce(it: Item, style: str = "grapes"):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    # ---------------------------------------------------------------- Obst
    if style == "grapes":
        _stem(c, 0, H * 0.85, H * 0.15, 0.2)
        rows = [3, 3, 2, 2, 1]
        r = W * 0.15
        for j, n in enumerate(rows):
            for i in range(n):
                x = (i - (n - 1) / 2) * r * 1.8
                y = H * 0.82 - j * r * 1.6 - r
                c.fill(ell(x, y, r, r, 16), zone=1, shade=1.0 - 0.04 * j)
                c.line(ell(x, y, r, r, 16), INNER * 0.7, zone=0, closed=True)
                c.fill(ell(x - r * 0.35, y + r * 0.35, r * 0.25, r * 0.2, 10), zone=1, shade=1.35)
    elif style == "strawberry":
        body = smooth([(x0, H * 0.72, "s"), (x1, H * 0.72, "s"), (W * 0.3, H * 0.25), (0, 0), (-W * 0.3, H * 0.25)])
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        for k in range(8):
            c.ellipse(-W * 0.3 + (k % 4) * W * 0.2, H * (0.25 + (k // 4) * 0.25) + (k % 2), 0.4, 0.6, zone=2, clip=cl)
        _leafy(c, 0, H * 0.7, W * 0.45, H * 0.3, 4)
    elif style == "cherry":
        for dx, lean in ((-W * 0.25, 0.4), (W * 0.2, -0.3)):
            c.line(smooth([(dx, H * 0.35), (dx + lean * W * 0.3, H * 0.75), (0, H)], closed=False), 0.5, zone=3)
            b = ell(dx, H * 0.2, W * 0.24, H * 0.2, 20)
            shaded(c, b, 1, "right", SHADE, 0.3)
            c.fill(ell(dx - W * 0.08, H * 0.26, W * 0.06, H * 0.05, 8), zone=1, shade=1.4)
        _leafy(c, 0, H * 0.95, W * 0.3, H * 0.2, 1)
    elif style == "pineapple":
        _leafy(c, 0, H * 0.6, W * 0.5, H * 0.4, 5)
        body = ell(0, H * 0.32, W / 2, H * 0.32, 32)
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        for k in range(-4, 5):
            line(c, [(k * W * 0.14 - W * 0.2, 0), (k * W * 0.14 + W * 0.2, H * 0.64)], zone=1, clip=cl, shade=0.72)
            line(c, [(k * W * 0.14 + W * 0.2, 0), (k * W * 0.14 - W * 0.2, H * 0.64)], zone=1, clip=cl, shade=0.72)
    elif style in ("kiwi", "plum", "apricot", "mango", "coconut", "melon"):
        rx, ry = {"kiwi": (0.5, 0.42), "plum": (0.44, 0.5), "apricot": (0.5, 0.48), "mango": (0.5, 0.4), "coconut": (0.5, 0.48),
                  "melon": (0.5, 0.44)}[style]
        body = ell(0, H * 0.48, W * rx, H * ry, 36) if style != "mango" else \
            smooth([(x0, H * 0.4), (-W * 0.2, 0), (W * 0.4, H * 0.1), (x1, H * 0.6), (W * 0.2, H * 0.95), (-W * 0.3, H * 0.8)])
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        if style == "kiwi":                                          # halbe Kiwi daneben: grünes Fruchtfleisch
            c.fill(ell(W * 0.1, H * 0.45, W * 0.3, H * 0.34, 28), zone=2, clip=cl)
            c.fill(ell(W * 0.1, H * 0.45, W * 0.1, H * 0.1, 16), zone=2, shade=1.4, clip=cl)
            for k in range(10):
                a = k * math.pi / 5
                c.ellipse(W * 0.1 + math.cos(a) * W * 0.18, H * 0.45 + math.sin(a) * H * 0.2, 0.3, 0.4, zone=0, clip=cl)
        elif style == "coconut":
            for k in range(3):
                c.ellipse(-W * 0.12 + k * W * 0.12, H * 0.7, W * 0.05, W * 0.05, zone=2, shade=0.6)
            for k in range(8):
                line(c, [(x0 + k * W / 7, H * 0.1), (x0 + k * W / 7 + 2, H * 0.9)], zone=1, clip=cl, shade=0.8)
        elif style == "melon":
            for k in range(-3, 4):
                line(c, [(k * W * 0.13, 0), (k * W * 0.11, H * 0.92)], zone=2, clip=cl, shade=1.0)
        else:
            c.fill(ell(-W * 0.18, H * 0.66, W * 0.1, H * 0.07, 12), zone=2, alpha=0.5, clip=cl)
            if style != "mango":
                _stem(c, 0, H * 0.94, H * 0.1)
    elif style == "blueberries":                                     # Schälchen voller Heidelbeeren
        for k in range(9):
            x = x0 + W * 0.18 + (k % 5) * W * 0.16
            y = H * (0.6 + (k // 5) * 0.2)
            c.fill(ell(x, y, W * 0.1, W * 0.1, 12), zone=1, shade=1.0 - 0.05 * (k % 3))
            c.line(ell(x, y, W * 0.1, W * 0.1, 12), INNER * 0.6, zone=0, closed=True)
        bowl = trap(-W * 0.36, W * 0.36, 0, x0, x1, H * 0.62, 0.8)
        shaded(c, bowl, 2, "right", SHADE, 0.25)
    # ---------------------------------------------------------------- Gemüse
    elif style in ("cucumber", "zucchini", "eggplant", "leek"):
        body = rrect(x0, 0, x1 - (W * 0.08 if style != "leek" else 0), H, H * 0.48)
        if style == "eggplant":
            body = smooth([(x0, H * 0.5), (x0 + W * 0.2, 0), (W * 0.3, 0), (W * 0.4, H * 0.5), (W * 0.3, H), (x0 + W * 0.2, H * 0.95)])
        cl = shaded(c, body, 1 if style != "leek" else 2, "bottom", SHADE, 0.35)
        if style == "cucumber":
            for k in range(8):
                c.ellipse(x0 + 4 + k * W * 0.11, H * (0.35 + 0.3 * (k % 2)), 0.3, 0.3, zone=2, clip=cl)
        if style == "leek":
            c.fill(rrect(-W * 0.05, 0, x1, H, H * 0.4), zone=3, clip=cl)
            for k in range(3):
                c.line([(x1 - 2, H * (0.2 + k * 0.3)), (x1 + W * 0.1, H * (0.1 + k * 0.4))], H * 0.28, zone=3, shade=0.9)
        else:
            c.fill(rrect(x1 - W * 0.1, H * 0.3, x1, H * 0.7, 1), zone=3)
    elif style in ("potato", "onion", "garlic", "radish"):
        if style == "potato":
            body = smooth([(x0, H * 0.4), (-W * 0.2, 0), (W * 0.35, H * 0.05), (x1, H * 0.55), (W * 0.2, H), (-W * 0.35, H * 0.85)])
            cl = shaded(c, body, 1, "right", SHADE, 0.3)
            for (x, y) in ((-W * 0.2, H * 0.5), (W * 0.15, H * 0.3), (W * 0.1, H * 0.7)):
                c.ellipse(x, y, 0.5, 0.4, zone=1, shade=0.6, clip=cl)
        else:
            body = smooth([(0, 0), (x1, H * 0.35), (W * 0.2, H * 0.72), (0, H * 0.8), (-W * 0.2, H * 0.72), (x0, H * 0.35)])
            cl = shaded(c, body, 1, "right", SHADE, 0.3)
            for k in (-1, 0, 1):
                line(c, [(k * W * 0.25, H * 0.08), (k * W * 0.12, H * 0.75)], zone=1, clip=cl, shade=0.8)
            if style == "radish":
                _leafy(c, 0, H * 0.78, W * 0.4, H * 0.3, 3)
            else:
                c.fill(trap(-W * 0.08, W * 0.08, H * 0.75, -W * 0.03, W * 0.03, H, 0.3), zone=2 if style == "onion" else 1)
            c.line([(0, 0), (0, -1.2)], 0.4, zone=2)
    elif style == "pepper":
        body = smooth([(x0, H * 0.75, "s"), (x1, H * 0.75, "s"), (W * 0.4, H * 0.1), (W * 0.1, 0), (0, H * 0.08), (-W * 0.1, 0),
                       (-W * 0.4, H * 0.1)])
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        line(c, [(0, H * 0.08), (0, H * 0.7)], zone=1, clip=cl, shade=0.75)
        c.fill(rrect(-W * 0.12, H * 0.72, W * 0.12, H * 0.82, 1), zone=3)
        _stem(c, 0, H * 0.82, H * 0.18, 0.2)
    elif style in ("broccoli", "cauliflower"):
        c.fill(trap(-W * 0.14, W * 0.14, 0, -W * 0.22, W * 0.22, H * 0.5, 1), zone=3, shade=0.9)
        if style == "cauliflower":
            for sx in (-1, 1):
                _leafy(c, sx * W * 0.3, H * 0.1, W * 0.25, H * 0.5, 1)
        for k in range(7):
            a = math.pi * (0.1 + 0.8 * k / 6)
            x, y = math.cos(a) * W * 0.3, H * 0.55 + math.sin(a) * H * 0.28
            c.fill(ell(x, y, W * 0.2, H * 0.17, 16), zone=1 if style == "broccoli" else 2, shade=1.0 + (k % 2) * 0.08)
            c.line(ell(x, y, W * 0.2, H * 0.17, 16), INNER * 0.7, zone=0, closed=True)
    elif style == "lettuce":
        for k in range(5):
            a = math.pi * k / 4
            leaf = ell(math.cos(a) * W * 0.25, H * 0.45 + math.sin(a) * H * 0.1, W * 0.3, H * 0.4, 24)
            shaded(c, leaf, 3, "bottom", 0.9, 0.3)
        c.fill(ell(0, H * 0.48, W * 0.25, H * 0.3, 24), zone=3, shade=1.15)
        c.line(ell(0, H * 0.48, W * 0.25, H * 0.3, 24), INNER * 0.7, zone=0, closed=True)
    elif style == "corn":
        for sx in (-1, 1):
            c.fill(smooth([(0, 0), (sx * W * 0.5, H * 0.2), (sx * W * 0.2, H * 0.7)]), zone=3)
        cob = rrect(-W * 0.25, H * 0.05, W * 0.25, H, W * 0.24)
        cl = c.mask(cob)
        c.fill(cob, zone=1)
        for j in range(int(H / 1.6)):
            for i in range(4):
                c.ellipse(-W * 0.18 + i * W * 0.12, H * 0.08 + j * 1.6, W * 0.055, 0.7, zone=1, shade=0.9 + (i + j) % 2 * 0.15, clip=cl)
        c.line(cob, INNER, zone=0, closed=True)
    elif style == "pumpkin":
        for k, (x, r) in enumerate(((-W * 0.24, 0.3), (W * 0.24, 0.3), (0, 0.32))):
            lobe = ell(x, H * 0.42, W * r, H * 0.42, 28)
            shaded(c, lobe, 1, "right", SHADE, 0.3)
        c.fill(rrect(-1.2, H * 0.8, 1.2, H, 0.6), zone=3)
    elif style == "peas":                                             # offene Schote
        pod = smooth([(x0, H * 0.5), (0, 0), (x1, H * 0.5), (W * 0.3, H * 0.9), (-W * 0.3, H * 0.9)])
        shaded(c, pod, 3, "bottom", SHADE, 0.3)
        for k in range(5):
            c.fill(ell(x0 + W * (0.2 + k * 0.15), H * 0.55, W * 0.08, H * 0.24, 12), zone=1)
            c.line(ell(x0 + W * (0.2 + k * 0.15), H * 0.55, W * 0.08, H * 0.24, 12), INNER * 0.6, zone=0, closed=True)
    elif style == "mushroom":
        c.fill(trap(-W * 0.14, W * 0.14, 0, -W * 0.12, W * 0.12, H * 0.55, 1), zone=2)
        cap = smooth([(x0, H * 0.5, "s"), (x1, H * 0.5, "s"), (W * 0.3, H * 0.9), (0, H), (-W * 0.3, H * 0.9)])
        shaded(c, cap, 1, "bottom", SHADE, 0.3)
