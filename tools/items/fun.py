"""
Spielzeug, Schwimmbad/Strand, Essen & Trinken (P04b-T09).
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Drittfarbe/Detail.
"""
from __future__ import annotations

import math

from .household import _band
from .kit import SHADE, SOFT, Item, ell, knob, line, rrect, shaded, smooth, trap


# ------------------------------------------------------------------ Spielzeug
def toy(it: Item, style: str = "ball"):
    c, W, H = it.c, it.w, it.h
    if style in ("ball", "beachball", "football", "basketball"):
        r = min(W, H) / 2
        body = ell(0, r, r, r)
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        if style == "beachball":
            for k, z in enumerate((2, 3)):
                c.fill(smooth([(0, 2 * r), (-r * 0.9 + k * r * 0.9, r), (0, 0), (-r * 0.4 + k * r * 0.9, r)]), zone=z, clip=cl)
        elif style == "football":
            c.fill(ell(0, r, r * 0.28, r * 0.28), zone=2, clip=cl)
            for k in range(5):
                a = math.radians(90 + k * 72)
                c.fill(ell(math.cos(a) * r * 0.8, r + math.sin(a) * r * 0.8, r * 0.22, r * 0.22), zone=2, clip=cl)
        elif style == "basketball":
            for pts in ([(0, 0), (0, 2 * r)], [(-r, r), (r, r)]):
                c.line(pts, 0.4, zone=0, clip=cl)
            c.line(smooth([(-r * 0.7, 2 * r), (-r * 0.35, r), (-r * 0.7, 0)], closed=False), 0.4, zone=0, clip=cl)
            c.line(smooth([(r * 0.7, 2 * r), (r * 0.35, r), (r * 0.7, 0)], closed=False), 0.4, zone=0, clip=cl)
        else:
            c.line(smooth([(-r, r), (0, r * 1.25), (r, r)], closed=False), 1.2, zone=2, clip=cl)
    elif style == "teddy":
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.3, H * 0.15, W * 0.18, H * 0.14), zone=1)     # Füße
            c.fill(ell(sx * W * 0.4, H * 0.45, W * 0.14, H * 0.16), zone=1)     # Arme
            c.fill(ell(sx * W * 0.28, H * 0.92, W * 0.14, W * 0.14), zone=1)    # Ohren
            c.fill(ell(sx * W * 0.28, H * 0.92, W * 0.07, W * 0.07), zone=2)
        c.fill(ell(0, H * 0.38, W * 0.34, H * 0.3), zone=1)
        c.fill(ell(0, H * 0.35, W * 0.2, H * 0.18), zone=2)
        c.fill(ell(0, H * 0.72, W * 0.32, H * 0.22), zone=1)
        c.fill(ell(0, H * 0.66, W * 0.13, H * 0.08), zone=2)
        c.ellipse(0, H * 0.69, 0.9, 0.7, zone=0)
        for sx in (-1, 1):
            c.ellipse(sx * W * 0.12, H * 0.76, 0.7, 0.8, zone=0)
        c.fill(smooth([(-W * 0.12, H * 0.54), (W * 0.12, H * 0.54), (W * 0.2, H * 0.5), (0, H * 0.46), (-W * 0.2, H * 0.5)]), zone=3)
    elif style == "blocks":
        for k, (x, y, z) in enumerate(((-W * 0.25, 0, 1), (W * 0.25, 0, 2), (0, H / 2, 3))):
            b = rrect(x - W * 0.24, y, x + W * 0.24, y + H / 2 - 0.3, 0.8)
            cl = shaded(c, b, z, "right", SHADE, 0.25)
            c.ellipse(x, y + H / 4, W * 0.1, W * 0.1, zone=z, shade=0.7, clip=cl)
    elif style == "car":
        body = smooth([(-W / 2, H * 0.25, "s"), (W / 2, H * 0.25, "s"), (W / 2, H * 0.55), (W * 0.25, H * 0.6), (W * 0.1, H),
                       (-W * 0.25, H), (-W * 0.35, H * 0.6), (-W / 2, H * 0.55)])
        cl = shaded(c, body, 1, "bottom", SHADE, 0.35)
        c.fill(trap(-W * 0.22, W * 0.18, H * 0.62, -W * 0.18, W * 0.06, H * 0.92, 0.5), zone=2, clip=cl)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.3, H * 0.22, H * 0.22, H * 0.22), zone=0)
            c.fill(ell(sx * W * 0.3, H * 0.22, H * 0.1, H * 0.1), zone=3)
    elif style == "train":
        for k, x in enumerate((-W * 0.25, W * 0.2)):
            cl = shaded(c, rrect(x - W * 0.22, H * 0.2, x + W * 0.22, H * (0.75 if k else 0.6), 1), 1 + k, "bottom", SHADE, 0.3)
        c.fill(rrect(W * 0.06, H * 0.75, W * 0.34, H, 0.6), zone=2)
        c.fill(rrect(-W * 0.4, H * 0.6, -W * 0.3, H * 0.85, 0.4), zone=3)
        for x in (-W * 0.35, -W * 0.15, W * 0.08, W * 0.3):
            c.fill(ell(x, H * 0.18, H * 0.17, H * 0.17), zone=3)
            c.ellipse(x, H * 0.18, 0.6, 0.6, zone=0)
    elif style == "robot":
        c.fill(rrect(-W * 0.3, 0, -W * 0.08, H * 0.25, 0.6), zone=3)
        c.fill(rrect(W * 0.08, 0, W * 0.3, H * 0.25, 0.6), zone=3)
        cl = shaded(c, rrect(-W * 0.4, H * 0.22, W * 0.4, H * 0.62, 1.2), 1, "right", SHADE, 0.25)
        c.fill(rrect(-W * 0.2, H * 0.3, W * 0.2, H * 0.5, 0.6), zone=2)
        cl = shaded(c, rrect(-W * 0.34, H * 0.62, W * 0.34, H * 0.9, 1.5), 1, "right", SHADE, 0.25)
        for sx in (-1, 1):
            c.ellipse(sx * W * 0.14, H * 0.77, W * 0.07, W * 0.07, zone=2)
        c.line([(0, H * 0.9), (0, H)], 0.5, zone=3)
        c.ellipse(0, H - 0.8, 1.0, 1.0, zone=2)
    elif style == "doll":
        # Puppe im Figuren-Stil: großer Kopf, Pony, Wangen, Kleid mit Kragen, Ärmchen, Schuhe
        hr = W * 0.36
        hy = H - hr
        for sx in (-1, 1):
            c.fill(rrect(sx * W * 0.1 - 1.0, H * 0.04, sx * W * 0.1 + 1.0, H * 0.3, 0.8), zone=3)
            c.fill(rrect(sx * W * 0.1 - 1.4, 0, sx * W * 0.1 + 1.4, H * 0.06, 0.8), zone=2, shade=0.7)
            c.line([(sx * W * 0.2, H * 0.52), (sx * W * 0.36, H * 0.3)], 1.6, zone=3)
        dress = smooth([(-W * 0.36, H * 0.22, "s"), (W * 0.36, H * 0.22, "s"), (W * 0.18, H * 0.56), (-W * 0.18, H * 0.56)])
        cl = shaded(c, dress, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W * 0.4, H * 0.2, W * 0.4, H * 0.26, 0.5), zone=1, shade=0.8, clip=cl)
        c.fill(smooth([(-W * 0.16, H * 0.56), (0, H * 0.5), (W * 0.16, H * 0.56), (0, H * 0.6)]), zone=1, shade=1.15)
        c.fill(ell(0, hy + 1, hr * 1.12, hr * 1.1), zone=2)                      # Haare hinten
        c.fill(ell(0, hy, hr, hr * 0.95), zone=3, shade=1.0)                     # Gesicht
        c.fill(smooth([(-hr * 1.05, hy), (-hr * 0.9, hy + hr * 0.8), (0, hy + hr * 1.08), (hr * 0.9, hy + hr * 0.8), (hr * 1.05, hy),
                       (hr * 0.5, hy + hr * 0.45), (0, hy + hr * 0.5), (-hr * 0.5, hy + hr * 0.45)]), zone=2)
        for sx in (-1, 1):
            c.ellipse(sx * hr * 0.4, hy - hr * 0.05, hr * 0.13, hr * 0.17, zone=0)
            c.ellipse(sx * hr * 0.4 + hr * 0.04, hy + hr * 0.02, hr * 0.04, hr * 0.05, zone=3, shade=1.2)
            c.ellipse(sx * hr * 0.62, hy - hr * 0.35, hr * 0.12, hr * 0.07, zone=1, alpha=0.5)
        c.line(smooth([(-hr * 0.15, hy - hr * 0.45), (0, hy - hr * 0.55), (hr * 0.15, hy - hr * 0.45)], closed=False), 0.3, zone=0)
    elif style == "drum":
        body = rrect(-W / 2, 0, W / 2, H * 0.8, 2)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        for k in range(-3, 4):
            line(c, [(k * W * 0.14, 1), (k * W * 0.14 + W * 0.07, H * 0.79)], zone=2, clip=cl, w=0.5, shade=1.0)
        c.fill(ell(0, H * 0.8, W / 2, H * 0.1), zone=3)
        for sx in (-1, 1):
            c.line([(sx * W * 0.1, H * 0.9), (sx * W * 0.35, H)], 0.7, zone=3, shade=0.7)
    elif style == "xylophone":
        for k in range(6):
            x = -W / 2 + W * (k + 0.5) / 6
            h = H * (0.9 - k * 0.1)
            c.fill(rrect(x - W / 14, H * 0.2, x + W / 14, H * 0.2 + h * 0.7, 0.6), zone=[1, 2, 3][k % 3])
        c.fill(rrect(-W / 2, 0, W / 2, H * 0.22, 1), zone=3, shade=0.7)
    elif style == "puzzle":
        for k, (x, y) in enumerate(((-W * 0.25, H * 0.25), (W * 0.25, H * 0.25), (-W * 0.25, H * 0.75), (W * 0.25, H * 0.75))):
            c.fill(rrect(x - W * 0.24, y - H * 0.24, x + W * 0.24, y + H * 0.24, 0.5), zone=[1, 2, 3, 1][k])
            c.fill(ell(x + (W * 0.25 if k % 2 == 0 else 0), y, W * 0.07, W * 0.07), zone=[1, 2, 3, 1][k])
    elif style == "kite":
        c.fill([(0, H), (W / 2, H * 0.6), (0, H * 0.25), (-W / 2, H * 0.6)], zone=1)
        c.fill([(0, H), (W / 2, H * 0.6), (0, H * 0.6)], zone=2)
        c.fill([(0, H * 0.25), (-W / 2, H * 0.6), (0, H * 0.6)], zone=2)
        c.line(smooth([(0, H * 0.25), (W * 0.1, H * 0.12), (-W * 0.05, 0)], closed=False), 0.4, zone=3)
        for k in range(3):
            c.fill(ell(W * 0.05 - k * 0.8, H * (0.2 - k * 0.07), 1.2, 0.7), zone=3)
    elif style == "rocking_horse":
        c.fill(smooth([(-W / 2, H * 0.15), (0, 0), (W / 2, H * 0.15), (W / 2, H * 0.2), (0, H * 0.06), (-W / 2, H * 0.2)]), zone=3)
        for sx in (-1, 1):
            c.line([(sx * W * 0.22, H * 0.12), (sx * W * 0.2, H * 0.45)], 2.0, zone=1, shade=0.9)
        body = ell(0, H * 0.52, W * 0.34, H * 0.13)
        shaded(c, body, 1, "bottom", SHADE, 0.35)
        head = smooth([(W * 0.2, H * 0.55), (W * 0.36, H * 0.95), (W * 0.5, H * 0.85), (W * 0.36, H * 0.55)])
        shaded(c, head, 1, "right", SHADE, 0.3)
        c.fill(smooth([(W * 0.22, H * 0.62), (W * 0.3, H), (W * 0.36, H * 0.9), (W * 0.28, H * 0.6)]), zone=2)
        c.ellipse(W * 0.4, H * 0.85, 0.6, 0.6, zone=0)
        c.fill(smooth([(-W * 0.34, H * 0.55), (-W * 0.5, H * 0.45), (-W * 0.42, H * 0.3)]), zone=2)
    elif style == "balloon":
        c.line(smooth([(0, 0), (-W * 0.1, H * 0.2), (W * 0.05, H * 0.4)], closed=False), 0.3, zone=3)
        body = ell(0, H * 0.7, W / 2, H * 0.3)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill([(0, H * 0.38), (1.2, H * 0.36), (-1.2, H * 0.36)], zone=1)
        c.fill(ell(-W * 0.2, H * 0.82, W * 0.08, H * 0.06), zone=2, alpha=0.5, clip=cl)
    elif style == "skateboard":
        c.fill(smooth([(-W / 2, H * 0.7), (-W * 0.45, H * 0.45, "s"), (W * 0.45, H * 0.45, "s"), (W / 2, H * 0.7), (W * 0.42, H * 0.55),
                       (-W * 0.42, H * 0.55)]), zone=1)
        for sx in (-1, 1):
            c.fill(ell(sx * W * 0.3, H * 0.2, H * 0.2, H * 0.2), zone=2)
    elif style == "bucket_spade":
        body = trap(-W * 0.3, W * 0.2, 0, -W * 0.4, W * 0.3, H * 0.6, 1)
        shaded(c, body, 1, "right", SHADE, 0.25)
        c.line(smooth([(-W * 0.4, H * 0.6), (-W * 0.05, H * 0.85), (W * 0.3, H * 0.6)], closed=False), 0.5, zone=3)
        c.fill(rrect(W * 0.3, H * 0.3, W * 0.36, H, 0.3), zone=3)
        c.fill(smooth([(W * 0.2, H * 0.3), (W / 2, H * 0.3), (W * 0.46, 0), (W * 0.24, 0)]), zone=2)


# ------------------------------------------------------------------ Schwimmbad & Strand
def pool(it: Item, style: str = "air_mattress", state: str = ""):
    c, W, H = it.c, it.w, it.h
    if style == "air_mattress":
        # Seitenansicht mit leichter Aufsicht: Kopfkissen-Wulst links, 6 prall gewölbte Kammern, Ventil, Glanz
        pil = W * 0.2
        top = [(-W / 2 + 1.5, H * 0.5), (-W / 2 + pil * 0.2, H), (-W / 2 + pil * 0.8, H), (-W / 2 + pil, H * 0.8)]
        n = 6
        for k in range(n):
            x0 = -W / 2 + pil + (W - pil) * k / n
            x1 = -W / 2 + pil + (W - pil) * (k + 1) / n
            top += [((x0 * 0.7 + x1 * 0.3), H * 0.84), ((x0 + x1) / 2, H * 0.86), ((x0 * 0.3 + x1 * 0.7), H * 0.84),
                    (x1, H * 0.74 if k < n - 1 else H * 0.6)]
        body = [(W / 2, H * 0.3), (W / 2 - 2, 0, "s"), (-W / 2 + 2, 0, "s")] + top
        cl = shaded(c, smooth(body), 1, "bottom", SHADE, 0.35)
        for k in range(n + 1):
            x = -W / 2 + pil + (W - pil) * k / n
            line(c, [(x, H * 0.08), (x, H * 0.72)], clip=cl, shade=0.78)
        c.fill(smooth([(-W / 2 + 3, H * 0.62), (-W / 2 + pil * 0.3, H * 0.9), (-W / 2 + pil * 0.85, H * 0.86),
                       (-W / 2 + pil * 0.9, H * 0.55), (-W / 2 + pil * 0.4, H * 0.45)]), zone=2, clip=cl)
        c.fill(rrect(-W / 2 + pil + 3, H * 0.64, W / 2 - 6, H * 0.71, H * 0.035), zone=2, alpha=0.6)
        c.fill(rrect(W / 2 - 5, H * 0.3, W / 2 - 2, H * 0.5, 0.6), zone=3)
    elif style == "swim_ring":
        # echter Reifen: Loch in der Mitte, 8 Streifen, Glanzbogen
        R, r = W / 2, W * 0.2
        ring = ell(0, H / 2, R, H / 2, 64)
        cl = shaded(c, ring, 1, "bottom", SHADE, 0.3)
        for k in range(0, 8, 2):
            a0 = k * 45 + 22
            pts = [(0, H / 2)] + [(math.cos(math.radians(a)) * W, H / 2 + math.sin(math.radians(a)) * W)
                                  for a in range(a0, a0 + 46, 5)]
            c.fill(pts, zone=2, clip=cl)
        c.line(ell(0, H / 2, (R + r) / 2, (H / 2 + r) / 2 * 1.0, 64), 0.25, zone=1, shade=0.7, closed=True)
        c.fill(_band(smooth([(-R * 0.75, H * 0.62), (-R * 0.45, H * 0.9), (0, H * 0.97)], closed=False, n=10), 1.1),
               zone=2, alpha=0.8)
        c.line(ell(0, H / 2, r, r, 48), 0.4, zone=0, closed=True)
        c.erase(ell(0, H / 2, r - 0.2, r - 0.2, 48))
    elif style == "noodle":
        body = rrect(-W / 2, 0, W / 2, H, H / 2)
        cl = shaded(c, body, 1, "bottom", SHADE, 0.35)
        for k in range(1, 8):
            line(c, [(-W / 2 + W * k / 8, 0), (-W / 2 + W * k / 8, H)], clip=cl, shade=0.88)
    elif style == "flippers":
        # zwei Flossen hintereinander: Fußtasche + lange, gerippte Flosse
        for dx, sh in ((W * 0.08, 0.82), (-W * 0.02, 1.0)):
            fin = smooth([(-W / 2 + dx, H * 0.1, "s"), (W * 0.1 + dx, H * 0.1), (W / 2 + dx - 2, H * 0.05, "s"),
                          (W / 2 + dx - 1, H * 0.3, "s"), (W * 0.1 + dx, H * 0.5), (-W * 0.2 + dx, H * 0.9),
                          (-W * 0.42 + dx, H, "s"), (-W / 2 + dx, H * 0.7)])
            cl = shaded(c, fin, 1, "bottom", SHADE * sh, 0.3)
            c.fill(smooth([(-W * 0.44 + dx, H * 0.3), (-W * 0.2 + dx, H * 0.32), (-W * 0.26 + dx, H * 0.75),
                           (-W * 0.42 + dx, H * 0.8)]), zone=2, shade=sh, clip=cl)
            for k in range(3):
                x = W * (0.05 + k * 0.13) + dx
                line(c, [(x, H * 0.22), (x + W * 0.1, H * 0.18)], clip=cl, shade=0.75)
    elif style == "goggles":
        for sx in (-1, 1):
            c.glass(ell(sx * W * 0.22, H / 2, W * 0.22, H * 0.4), zone=2, opacity=0.5)
            c.line(ell(sx * W * 0.22, H / 2, W * 0.22, H * 0.4), 1.0, zone=1, closed=True)
        c.line([(-W / 2, H / 2), (-W * 0.44, H / 2)], 0.8, zone=1)
        c.line([(W / 2, H / 2), (W * 0.44, H / 2)], 0.8, zone=1)
    elif style == "umbrella":
        c.fill(rrect(-0.8, 0, 0.8, H * 0.85, 0.6), zone=3)
        can = smooth([(-W / 2, H * 0.62, "s"), (0, H), (W / 2, H * 0.62, "s"), (W * 0.3, H * 0.66), (0, H * 0.62),
                      (-W * 0.3, H * 0.66)])
        cl = shaded(c, can, 1, "bottom", SOFT, 0.25)
        for k in (-0.3, 0.3):
            c.fill(smooth([(0, H), (k * W, H * 0.64), (k * W * 1.6, H * 0.62)]), zone=2, clip=cl)
    elif style == "deck_chair":
        # Klappliegestuhl (vorne = rechts): Rückenrahmen lehnt nach hinten, Stoffbahn hängt vom oberen zum vorderen Holm
        c.line([(W * 0.18, 0), (-W * 0.4, H)], 2.2, zone=3)                     # Rückenrahmen
        c.line([(W * 0.45, 0), (W * 0.3, H * 0.52)], 2.2, zone=3)                # Vorderbein
        c.line([(-W * 0.3, 0), (W * 0.3, H * 0.52)], 2.0, zone=3, shade=0.85)    # Sitzrahmen
        curve = smooth([(-W * 0.38, H * 0.95), (-W * 0.2, H * 0.55), (-W * 0.02, H * 0.3), (W * 0.18, H * 0.36),
                        (W * 0.3, H * 0.52)], closed=False, n=10)
        sling = _band(curve, 2.4)
        cl = shaded(c, sling, 1, "bottom", SHADE, 0.3)
        c.fill(_band(curve, 0.9), zone=2, clip=cl)
        for x, y in ((-W * 0.4, H), (W * 0.3, H * 0.52)):
            c.ellipse(x, y, 1.5, 1.5, zone=3, shade=0.8)
    elif style == "towel_beach":
        # ausgebreitetes Strandtuch, leicht gewellt, Streifen + Fransen an den Enden
        body = smooth([(-W / 2, 0, "s"), (W / 2, 0, "s"), (W / 2, H * 0.8), (W * 0.2, H), (-W * 0.2, H * 0.75), (-W / 2, H)])
        cl = shaded(c, body, 1, "bottom", SOFT, 0.3)
        for k in range(1, 6, 2):
            c.fill([(-W / 2 + W * k / 6, 0), (-W / 2 + W * (k + 1) / 6, 0), (-W / 2 + W * (k + 1) / 6, H * 2),
                    (-W / 2 + W * k / 6, H * 2)], zone=2, clip=cl)
        for sx in (-1, 1):
            for k in range(4):
                c.line([(sx * W / 2, H * (0.2 + k * 0.2)), (sx * (W / 2 + 2), H * (0.15 + k * 0.2))], 0.4, zone=2)
    elif style == "cooler":
        body = rrect(-W / 2, 0, W / 2, H * 0.8, 2)
        shaded(c, body, 1, "right", SHADE, 0.2)
        if state == "open":  # Deckel nach hinten geklappt, Eis-Inneres sichtbar
            c.fill(smooth([(-W / 2 - 0.5, H * 0.78, "s"), (W / 2 + 0.5, H * 0.78, "s"), (W * 0.46, H * 1.25, "s"),
                           (-W * 0.46, H * 1.25, "s")], n=2), zone=2, shade=0.85)
            c.fill(rrect(-W * 0.44, H * 0.6, W * 0.44, H * 0.78, 1), zone=0, alpha=0.35)
            for x in (-W * 0.25, W * 0.05, W * 0.28):
                c.glass(rrect(x - 2, H * 0.62, x + 2, H * 0.8, 0.6), zone=2, opacity=0.6)
        else:
            c.fill(rrect(-W / 2 - 0.5, H * 0.72, W / 2 + 0.5, H * 0.86, 1), zone=2)
            c.line(smooth([(-W * 0.3, H * 0.86), (0, H), (W * 0.3, H * 0.86)], closed=False), 0.8, zone=3)
    elif style == "sunscreen":
        body = rrect(-W / 2, 0, W / 2, H * 0.82, W * 0.3)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(ell(0, H * 0.45, W * 0.3, W * 0.3), zone=2, clip=cl)
        c.fill(rrect(-W * 0.3, H * 0.8, W * 0.3, H, 0.8), zone=3)
    elif style == "water_gun":
        body = smooth([(-W / 2, H * 0.55), (W * 0.3, H * 0.65), (W / 2, H * 0.75), (W / 2, H), (-W / 2, H * 0.9)])
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(trap(-W * 0.35, -W * 0.1, 0, -W * 0.3, -W * 0.05, H * 0.6, 1), zone=1)
        c.fill(ell(-W * 0.05, H, W * 0.18, H * 0.2), zone=2)
    elif style == "inflatable_animal":
        body = smooth([(-W / 2, H * 0.1), (W * 0.2, 0), (W * 0.45, H * 0.2), (W * 0.35, H * 0.55), (W * 0.45, H), (W * 0.2, H * 0.95),
                       (W * 0.1, H * 0.5), (-W * 0.4, H * 0.45)])
        cl = shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.ellipse(W * 0.32, H * 0.85, 0.8, 0.8, zone=0)
        c.fill(smooth([(W * 0.42, H * 0.92), (W / 2 + 2, H * 0.9), (W * 0.44, H * 0.84)]), zone=2)


# ------------------------------------------------------------------ Essen & Trinken
def food(it: Item, style: str = "apple"):
    c, W, H = it.c, it.w, it.h
    if style in ("apple", "orange", "tomato", "lemon", "peach"):
        body = ell(0, H * 0.45, W / 2, H * 0.45)
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        c.fill(ell(-W * 0.18, H * 0.62, W * 0.1, H * 0.08), zone=2, alpha=0.45, clip=cl)
        c.line([(0, H * 0.85), (W * 0.05, H)], 0.6, zone=3, shade=0.5)
        if style in ("apple", "orange", "tomato"):
            c.fill(smooth([(W * 0.05, H * 0.9), (W * 0.35, H * 1.0), (W * 0.1, H * 0.85)]), zone=3)
    elif style == "banana":
        body = smooth([(-W / 2, H * 0.8, "s"), (-W * 0.2, H * 0.1), (W * 0.3, 0), (W / 2, H * 0.4, "s"), (W * 0.2, H * 0.3),
                       (-W * 0.15, H * 0.45)])
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill(ell(-W * 0.48, H * 0.8, 0.8, 0.8), zone=3)
    elif style == "pear":
        body = smooth([(0, H * 0.85), (W * 0.2, H * 0.7), (W / 2, H * 0.25), (0, 0), (-W / 2, H * 0.25), (-W * 0.2, H * 0.7)])
        shaded(c, body, 1, "right", SHADE, 0.3)
        c.line([(0, H * 0.82), (W * 0.05, H)], 0.6, zone=3, shade=0.5)
    elif style == "carrot":
        body = smooth([(0, 0, "s"), (W * 0.35, H * 0.72), (0, H * 0.78), (-W * 0.35, H * 0.72)])
        cl = shaded(c, body, 1, "right", SHADE, 0.3)
        for k in range(3):
            line(c, [(-W * 0.2, H * (0.3 + k * 0.14)), (-W * 0.05, H * (0.28 + k * 0.14))], clip=cl, shade=0.7)
        for k in (-1, 0, 1):
            c.fill(smooth([(0, H * 0.75, "s"), (k * W * 0.3, H), (k * W * 0.1, H * 0.78, "s")]), zone=2)
    elif style == "bread":
        body = smooth([(-W / 2, 0.2, "s"), (W / 2, 0.2, "s"), (W / 2, H * 0.6), (W * 0.25, H), (-W * 0.25, H), (-W / 2, H * 0.6)])
        cl = shaded(c, body, 1, "bottom", SHADE, 0.35)
        for k in (-0.25, 0.0, 0.25):
            line(c, [(k * W - 2, H * 0.55), (k * W + 2, H * 0.85)], clip=cl, shade=0.72, w=0.6)
    elif style == "cake":
        body = rrect(-W / 2, 0, W / 2, H * 0.72, 1.2)
        cl = shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W / 2, H * 0.3, W / 2, H * 0.4, 0.5), zone=2, clip=cl)
        c.fill(smooth([(-W / 2, H * 0.72), (-W / 2, H * 0.55), (-W * 0.3, H * 0.6), (-W * 0.1, H * 0.5), (W * 0.1, H * 0.6),
                       (W * 0.3, H * 0.5), (W / 2, H * 0.6), (W / 2, H * 0.72)]), zone=2)
        c.fill(ell(0, H * 0.85, W * 0.08, H * 0.12), zone=3)
    elif style == "cupcake":
        c.fill(trap(-W * 0.35, W * 0.35, 0, -W * 0.45, W * 0.45, H * 0.45, 0.6), zone=2)
        for k in range(-2, 3):
            line(c, [(k * W * 0.14, 0.5), (k * W * 0.18, H * 0.44)], zone=2, shade=0.75)
        c.fill(smooth([(-W / 2, H * 0.45), (-W * 0.35, H * 0.75), (0, H * 0.9), (W * 0.35, H * 0.75), (W / 2, H * 0.45)]), zone=1)
        c.fill(ell(0, H * 0.93, W * 0.1, W * 0.1), zone=3)
    elif style == "pizza":
        body = smooth([(-W / 2, H * 0.1), (W / 2, H * 0.1), (0, H)])
        body = [(-W / 2, 0), (W / 2, 0), (0, H)]
        c.fill(body, zone=2)
        c.fill([(-W * 0.4, H * 0.12), (W * 0.4, H * 0.12), (0, H * 0.9)], zone=1)
        for (x, y) in ((-W * 0.15, H * 0.3), (W * 0.12, H * 0.25), (0, H * 0.55)):
            c.ellipse(x, y, W * 0.07, W * 0.07, zone=3)
    elif style == "icecream":
        c.fill([(-W * 0.3, H * 0.5), (W * 0.3, H * 0.5), (0, 0)], zone=3)
        for k in range(2):
            line(c, [(-W * 0.2 + k * W * 0.2, H * 0.5), (W * 0.1 + k * W * 0.1, H * 0.15)], zone=3, shade=0.7)
        c.fill(ell(0, H * 0.6, W * 0.38, H * 0.16), zone=1)
        c.fill(ell(0, H * 0.82, W * 0.32, H * 0.16), zone=2)
    elif style == "drink":
        body = trap(-W * 0.38, W * 0.38, 0, -W / 2, W / 2, H * 0.85, 0.8)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(rrect(-W / 2, H * 0.35, W / 2, H * 0.55, 0.3), zone=2, clip=cl)
        c.line([(W * 0.1, H * 0.8), (W * 0.2, H)], 0.8, zone=3)
    elif style == "carton":
        c.fill([(-W / 2, H * 0.8), (0, H), (W / 2, H * 0.8)], zone=1)
        body = rrect(-W / 2, 0, W / 2, H * 0.82, 0.5)
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        c.fill(ell(0, H * 0.4, W * 0.3, H * 0.15), zone=2, clip=cl)
    elif style == "cheese":
        body = [(-W / 2, 0), (W / 2, 0), (W / 2, H * 0.55), (-W / 2, H)]
        cl = shaded(c, body, 1, "right", SHADE, 0.25)
        for (x, y, r) in ((-W * 0.2, H * 0.3, 1.2), (W * 0.2, H * 0.2, 0.8), (0, H * 0.55, 0.9)):
            c.fill(ell(x, y, r, r), zone=1, shade=0.78, clip=cl)
    elif style == "egg":
        body = smooth([(0, H), (W / 2, H * 0.4), (0, 0), (-W / 2, H * 0.4)])
        shaded(c, body, 1, "right", SHADE, 0.25)
    elif style == "watermelon":
        c.fill(smooth([(-W / 2, H * 0.4), (0, 0), (W / 2, H * 0.4)]), zone=2)
        c.fill([(-W / 2, H * 0.4), (W / 2, H * 0.4), (0, H * 0.05)], zone=1)
        body = smooth([(-W / 2, H * 0.4, "s"), (W / 2, H * 0.4, "s"), (W * 0.3, H * 0.9), (0, H), (-W * 0.3, H * 0.9)])
        c.fill(body, zone=1)
        for (x, y) in ((-W * 0.2, H * 0.6), (0, H * 0.75), (W * 0.2, H * 0.6), (-W * 0.05, H * 0.5)):
            c.fill(ell(x, y, 0.7, 1.0), zone=0)
