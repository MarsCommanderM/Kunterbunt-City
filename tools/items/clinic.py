"""
Gesundheitszentrum (P10b, Welt-Doku §5 – nie gruselig, kein Blut): Empfangstheke, Wartestühle, Untersuchungsliege,
Zahnarztstuhl, Röntgengerät (zeigt lustige Dinge), Rolltrage, Krankenbett, Infusionsständer, Herzmonitor, Brutkasten,
Babywaage, Sehtafel (Bilder statt Buchstaben), Medizinregal, Medizin, Gips/Armschlinge, Augenpflaster, Krücken,
Tiertransportbox, Tierarzt-Tisch, Zahnmodell, Riesen-Zahnbürste, Krankenwagen, Hubschrauber, Landeplatz.
Zonen: 1 = Hauptfarbe · 2 = Zweitfarbe · 3 = Metall/Weiß.
"""
from __future__ import annotations

import math

from .kit import INNER, SHADE, SOFT, Item, cushion, ell, leg, line, rrect, shaded, smooth, trap


def _wheel(c, x: float, y: float, r: float):
    c.fill(ell(x, y, r, r, 16), zone=0)
    c.fill(ell(x, y, r * 0.45, r * 0.45, 12), zone=3, shade=1.2)


def _cross(c, x: float, y: float, s: float, zone: int = 2):
    c.fill(rrect(x - s * 0.18, y - s * 0.5, x + s * 0.18, y + s * 0.5, s * 0.06), zone=zone)
    c.fill(rrect(x - s * 0.5, y - s * 0.18, x + s * 0.5, y + s * 0.18, s * 0.06), zone=zone)


def clinic(it: Item, style: str = "reception", state: str = ""):
    c, W, H = it.c, it.w, it.h
    x0, x1 = -W / 2, W / 2
    if style == "reception":                                        # Empfangstheke mit Aufsatz und Kreuz
        body = rrect(x0, 0, x1, H * 0.8, 1.2)
        shaded(c, body, 1, "right", SHADE, 0.15)
        c.fill(rrect(x0 - 2, H * 0.8, x1 + 2, H * 0.86, 0.8), zone=3)
        c.fill(rrect(x0 + W * 0.1, H * 0.86, x1 - W * 0.1, H, 0.8), zone=1, shade=0.9)
        c.fill(ell(0, H * 0.45, H * 0.18, H * 0.18, 24), zone=3, shade=1.3)
        _cross(c, 0, H * 0.45, H * 0.22)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "waiting_chairs":                                 # 3 Wartestühle auf Traverse
        c.fill(rrect(x0 + 4, H * 0.45, x1 - 4, H * 0.5, 0.5), zone=3)
        for x in (x0 + 10, x1 - 10):
            c.fill(rrect(x - 1.5, 0, x + 1.5, H * 0.45, 0.4), zone=3)
        for k in range(3):
            cx = x0 + (k + 0.5) * W / 3
            cushion(c, cx - W / 6 + 2, H * 0.5, cx + W / 6 - 2, H * 0.56, zone=1)
            back = rrect(cx - W / 6 + 3, H * 0.6, cx + W / 6 - 3, H, 3.0)
            shaded(c, back, 1, "right", SOFT, 0.2)
            c.line(back, INNER, zone=0, closed=True)
    elif style == "exam_couch":                                     # Untersuchungsliege mit Papierrolle
        for x in (x0 + 12, x1 - 12):
            leg(c, x, 0, H * 0.75, 4, 3, zone=3)
        cushion(c, x0, H * 0.72, x1, H * 0.9, zone=1)
        head = [(x0, H * 0.88), (x0 + W * 0.25, H * 0.88), (x0 + W * 0.2, H), (x0 + 2, H)]
        c.fill(head, zone=1, shade=0.95)
        c.fill(rrect(x0 + W * 0.15, H * 0.9, x1 - 6, H * 0.92, 0.3), zone=3, shade=1.6)
        c.fill(ell(x1 - 4, H * 0.84, 4, 4, 16), zone=3, shade=1.5)
        c.line(head, INNER, zone=0, closed=True)
    elif style == "dentist_chair":                                  # Behandlungsstuhl mit Lampe (Zustand: Lampe an)
        c.fill(trap(-10, 10, 0, -6, 6, H * 0.35, 0.6), zone=3)
        seat = smooth([(x0 + W * 0.15, H * 0.35, "s"), (x1 - 4, H * 0.35, "s"), (x1 - 2, H * 0.45), (x0 + W * 0.2, H * 0.48),
                       (x0 + 4, H * 0.8), (x0 + 2, H * 0.72)])
        shaded(c, seat, 1, "bottom", SHADE, 0.3)
        c.fill(ell(x0 + 6, H * 0.8, 8, 6, 16), zone=1, shade=0.95)
        c.line([(x1 - 10, H * 0.35), (x1 - 12, H * 0.95), (x0 + W * 0.3, H)], 1.6, zone=3)
        lamp = smooth([(x0 + W * 0.2, H * 0.95, "s"), (x0 + W * 0.4, H * 0.95, "s"), (x0 + W * 0.36, H * 0.87), (x0 + W * 0.24, H * 0.87)])
        c.fill(lamp, zone=2)
        if state == "on":
            c.fill([(x0 + W * 0.24, H * 0.87), (x0 + W * 0.36, H * 0.87), (x0 + W * 0.4, H * 0.6), (x0 + W * 0.1, H * 0.6)], zone=2,
                   shade=1.6, alpha=0.35)
        c.line(seat, INNER, zone=0, closed=True)
    elif style == "xray":                                           # Röntgenbildschirm auf Rollständer: lustige Dinge
        _wheel(c, x0 + 10, 4, 4)
        _wheel(c, x1 - 10, 4, 4)
        c.fill(rrect(x0 + 6, 6, x1 - 6, 10, 0.5), zone=3)
        c.fill(rrect(-2, 10, 2, H * 0.45, 0.5), zone=3)
        frame = rrect(x0, H * 0.45, x1, H, 1.5)
        c.fill(frame, zone=1)
        scr = rrect(x0 + 5, H * 0.49, x1 - 5, H - 4, 0.8)
        c.fill(scr, zone=3, shade=0.25)
        cl = c.mask(scr)
        cx, cy, r = 0.0, H * 0.72, min(W, H * 0.5) * 0.32
        glow = 1.8
        if state in ("", "off"):
            pass
        elif state == "fish":                                       # Fischgräte im Bauch
            c.line([(cx - r, cy), (cx + r * 0.8, cy)], 1.2, zone=3, shade=glow, clip=cl)
            for k in range(6):
                x = cx - r * 0.7 + k * r * 0.25
                c.line([(x - r * 0.12, cy + r * 0.35), (x, cy), (x - r * 0.12, cy - r * 0.35)], 0.8, zone=3, shade=glow, clip=cl)
            c.line(ell(cx + r * 0.95, cy, r * 0.22, r * 0.2, 16), 1.0, zone=3, shade=glow, closed=True, clip=cl)
            c.line([(cx - r, cy), (cx - r * 1.3, cy + r * 0.3), (cx - r * 1.3, cy - r * 0.3), (cx - r, cy)], 1.0, zone=3, shade=glow,
                   clip=cl)
        elif state == "car":                                        # Spielzeugauto verschluckt (lacht)
            c.line(rrect(cx - r, cy - r * 0.3, cx + r, cy + r * 0.2, 1.5), 1.0, zone=3, shade=glow, closed=True, clip=cl)
            c.line(rrect(cx - r * 0.5, cy + r * 0.2, cx + r * 0.5, cy + r * 0.6, 1.5), 1.0, zone=3, shade=glow, closed=True, clip=cl)
            for sx in (-0.6, 0.6):
                c.line(ell(cx + sx * r, cy - r * 0.35, r * 0.2, r * 0.2, 14), 1.0, zone=3, shade=glow, closed=True, clip=cl)
        elif state == "ribs":                                       # freundliche Rippen + Herz
            c.line([(cx, cy - r), (cx, cy + r)], 1.0, zone=3, shade=glow, clip=cl)
            for k in range(4):
                y = cy + r * 0.7 - k * r * 0.4
                c.line(smooth([(cx - r, y - r * 0.15), (cx, y + r * 0.05), (cx + r, y - r * 0.15)], closed=False), 0.9, zone=3,
                       shade=glow, clip=cl)
            c.fill(ell(cx - r * 0.2, cy, r * 0.12, r * 0.12, 12), zone=2, clip=cl)
            c.fill(ell(cx - r * 0.05, cy, r * 0.12, r * 0.12, 12), zone=2, clip=cl)
            c.fill([(cx - r * 0.32, cy - 0.5), (cx + r * 0.07, cy - 0.5), (cx - r * 0.12, cy - r * 0.25)], zone=2, clip=cl)
        c.line(frame, INNER, zone=0, closed=True)
    elif style == "gurney":                                         # Rolltrage
        for x in (x0 + 16, x1 - 16):
            c.line([(x, 8), (x, H * 0.8)], 1.6, zone=3)
            _wheel(c, x, 4, 4)
        c.fill(rrect(x0 + 6, H * 0.35, x1 - 6, H * 0.4, 0.5), zone=3)
        cushion(c, x0, H * 0.8, x1, H, zone=1)
        c.fill(ell(x0 + 18, H * 0.98, 14, 4, 16), zone=3, shade=1.6)
    elif style == "hospital_bed":                                   # Krankenbett mit Kopfteil + Decke
        for x in (x0 + 14, x1 - 14):
            c.line([(x, 8), (x, H * 0.5)], 1.8, zone=3)
            _wheel(c, x, 4, 4.5)
        c.fill(rrect(x0 + 4, H * 0.45, x1 - 4, H * 0.52, 0.6), zone=3)
        c.fill(rrect(x0, H * 0.5, x0 + 5, H, 1.5), zone=3)
        c.fill(rrect(x1 - 5, H * 0.5, x1, H * 0.8, 1.5), zone=3)
        cushion(c, x0 + 5, H * 0.52, x1 - 5, H * 0.62, zone=3)
        c.fill(ell(x0 + 22, H * 0.66, 14, 5, 20), zone=3, shade=1.5)
        blanket = rrect(x0 + W * 0.28, H * 0.54, x1 - 5, H * 0.66, 2.0)
        shaded(c, blanket, 1, "bottom", SHADE, 0.35)
        c.line(blanket, INNER, zone=0, closed=True)
    elif style == "iv_stand":
        for sx in (-1, 0, 1):
            c.line([(0, 6), (sx * W * 0.4, 2)], 1.2, zone=3)
        c.line([(0, 4), (0, H * 0.92)], 1.2, zone=3)
        c.line([(-W * 0.3, H * 0.92), (W * 0.3, H * 0.92)], 1.0, zone=3)
        bag = rrect(W * 0.08, H * 0.6, W * 0.4, H * 0.9, 2.0)
        c.fill(bag, zone=1, shade=1.3)
        c.fill(rrect(W * 0.08, H * 0.6, W * 0.4, H * 0.72, 2.0), zone=1)
        c.line([(W * 0.24, H * 0.6), (W * 0.3, H * 0.3), (W * 0.35, H * 0.1)], 0.4, zone=3, shade=0.9)
        c.line(bag, INNER, zone=0, closed=True)
    elif style == "heart_monitor":                                  # Herzmonitor (Zustand: piept – Linie hüpft)
        body = rrect(x0, 0, x1, H, 2.0)
        shaded(c, body, 1, "right", SHADE, 0.2)
        scr = rrect(x0 + 3, H * 0.25, x1 - 3, H - 3, 1.0)
        c.fill(scr, zone=3, shade=0.2)
        pts = []
        amp = 0.28 if state == "beep" else 0.1
        for k in range(21):
            x = x0 + 5 + k * (W - 10) / 20
            y = H * 0.6 + (math.sin(k * 1.9) * amp * H if k in (8, 9, 10, 17) else 0.0)
            pts.append((x, y))
        c.line(pts, 0.7, zone=2, clip=c.mask(scr))
        c.fill(ell(x1 - 7, H * 0.12, 2.2, 2.2, 12), zone=2 if state == "beep" else 3)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "incubator":                                      # Wärmebett für Babys mit Haube
        for x in (x0 + 8, x1 - 8):
            c.line([(x, 6), (x, H * 0.5)], 1.6, zone=3)
            _wheel(c, x, 4, 3.5)
        base = rrect(x0, H * 0.45, x1, H * 0.6, 1.5)
        shaded(c, base, 1, "right", SHADE, 0.2)
        cushion(c, x0 + 6, H * 0.6, x1 - 6, H * 0.66, zone=2)
        hood = smooth([(x0 + 2, H * 0.6, "s"), (x0 + 4, H * 0.92), (x0 + 12, H, "s"), (x1 - 12, H, "s"), (x1 - 4, H * 0.92),
                       (x1 - 2, H * 0.6, "s")])
        c.fill(hood, zone=3, shade=1.6, alpha=0.4)
        c.line(hood, 0.5, zone=3, shade=0.8, closed=True)
        for sx in (-1, 1):
            c.line(ell(sx * W * 0.22, H * 0.78, 5, 5, 16), 0.6, zone=3, shade=0.7, closed=True)
        c.line(base, INNER, zone=0, closed=True)
    elif style == "baby_scale":                                     # Babywaage mit Schale und Anzeige
        body = rrect(x0 + 4, 0, x1 - 4, H * 0.45, 1.5)
        shaded(c, body, 1, "right", SHADE, 0.2)
        c.fill(rrect(-W * 0.18, H * 0.12, W * 0.18, H * 0.32, 0.6), zone=3, shade=0.3)
        c.fill(ell(0, H * 0.22, W * 0.06, H * 0.06, 10), zone=2)
        tray = smooth([(x0, H * 0.7, "s"), (x0 + 6, H * 0.45, "s"), (x1 - 6, H * 0.45, "s"), (x1, H * 0.7, "s"), (x1 - 3, H, "s"),
                       (x0 + 3, H, "s")])
        c.fill(tray, zone=2, shade=1.2)
        c.line(tray, INNER, zone=0, closed=True)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "eye_chart":                                      # Sehtafel mit Bildern (Haus, Stern, Apfel …) statt Buchstaben
        board = rrect(x0, 0, x1, H, 1.0)
        c.fill(board, zone=3, shade=1.5)
        rows = [(1, 0.14), (2, 0.1), (3, 0.075), (4, 0.055), (5, 0.04)]
        y = H * 0.88
        for n, s in rows:
            for k in range(n):
                x = x0 + (k + 0.5) * W / n
                r = s * W * 1.2
                shape = (k + n) % 3
                if shape == 0:
                    c.fill(ell(x, y, r, r, 14), zone=1)
                elif shape == 1:
                    c.fill([(x - r, y - r), (x + r, y - r), (x, y + r)], zone=2)
                else:
                    c.fill(rrect(x - r, y - r, x + r, y + r, r * 0.2), zone=1, shade=0.8)
            y -= H * (s * 2.6 + 0.06)
        c.line(board, INNER, zone=0, closed=True)
    elif style == "medicine_shelf":                                 # Apothekenregal: Schubladen unten, Packungen oben
        body = rrect(x0, 0, x1, H, 1.0)
        shaded(c, body, 1, "right", SHADE, 0.12)
        for i in range(4):
            for j in range(2):
                d = rrect(x0 + 3 + i * (W - 6) / 4 + 0.6, 3 + j * H * 0.18, x0 + 3 + (i + 1) * (W - 6) / 4 - 0.6,
                          3 + (j + 1) * H * 0.18 - 0.8, 0.4)
                c.fill(d, zone=1, shade=0.94)
                c.fill(ell(x0 + 3 + (i + 0.5) * (W - 6) / 4, 3 + (j + 0.5) * H * 0.18, 1.6, 1.6, 10), zone=3)
                c.line(d, INNER, zone=0, closed=True)
        for row in range(3):
            y = H * 0.4 + row * H * 0.19
            c.fill(rrect(x0 + 2, y - 1.5, x1 - 2, y, 0.3), zone=3)
            x = x0 + 5
            k = 0
            while x < x1 - 10:
                bw = [8, 6, 10, 7][k % 4]
                bh = H * [0.1, 0.13, 0.08, 0.12][k % 4]
                box = rrect(x, y, x + bw, y + bh, 0.6 if k % 2 else 2.5)
                c.fill(box, zone=2, shade=[0.8, 1.0, 1.25, 1.4][k % 4])
                c.line(box, INNER, zone=0, closed=True)
                x += bw + 2
                k += 1
        c.line(body, INNER, zone=0, closed=True)
    elif style == "medicine":                                       # Medizinpackung mit Kreuz / Sirup-Flasche
        if state == "syrup":
            b = smooth([(x0 + 1, 0, "s"), (x1 - 1, 0, "s"), (x1 - 1, H * 0.6), (W * 0.2, H * 0.75), (W * 0.2, H, "s"),
                        (-W * 0.2, H, "s"), (-W * 0.2, H * 0.75), (x0 + 1, H * 0.6)])
            c.fill(b, zone=1)
            c.fill(rrect(x0 + 1.5, H * 0.2, x1 - 1.5, H * 0.45, 0.4), zone=3, shade=1.5)
            c.line(b, INNER, zone=0, closed=True)
        else:
            box = rrect(x0, 0, x1, H, 0.6)
            c.fill(box, zone=3, shade=1.5)
            c.fill(rrect(x0, H * 0.65, x1, H, 0.6), zone=1)
            _cross(c, 0, H * 0.35, min(W, H) * 0.35, zone=2)
            c.line(box, INNER, zone=0, closed=True)
    elif style == "sling":                                          # Armschlinge / Gips (geht an die Figur)
        c.fill(smooth([(x0, H * 0.9, "s"), (x1, H, "s"), (x1 - 2, H * 0.6), (0, 0, "s"), (x0 + 2, H * 0.4)]), zone=1)
        c.fill(rrect(-W * 0.3, H * 0.25, W * 0.3, H * 0.55, 3.0), zone=3, shade=1.5)
    elif style == "eye_patch":
        c.fill(ell(0, H * 0.5, W * 0.4, H * 0.45, 20), zone=1)
        c.fill(ell(-W * 0.1, H * 0.6, W * 0.12, H * 0.1, 12), zone=2, shade=1.2)
        c.line([(x0, H * 0.7), (x1, H * 0.75)], 0.5, zone=3)
    elif style == "crutches":
        for sx in (-1, 1):
            x = sx * W * 0.25
            c.line([(x, 0), (x, H * 0.85)], 1.4, zone=3)
            c.fill(rrect(x - 5, H * 0.85, x + 5, H * 0.9, 1.5), zone=1)
            c.fill(rrect(x - 3, H * 0.5, x + 3, H * 0.54, 1.0), zone=1)
            c.fill(ell(x, 1, 2, 1.5, 10), zone=0)
    elif style == "pet_carrier":                                    # Transportbox mit Gittertür
        box = rrect(x0, 0, x1, H * 0.85, 4.0)
        shaded(c, box, 1, "right", SHADE, 0.2)
        door = rrect(x0 + W * 0.15, H * 0.12, x1 - W * 0.15, H * 0.72, 3.0)
        c.fill(door, zone=3, shade=0.4)
        for k in range(1, 6):
            line(c, [(x0 + W * 0.15 + k * W * 0.7 / 6, H * 0.12), (x0 + W * 0.15 + k * W * 0.7 / 6, H * 0.72)], zone=3, shade=1.4, w=0.6)
        c.fill(smooth([(-W * 0.25, H * 0.85), (0, H), (W * 0.25, H * 0.85)], closed=False), zone=2)
        c.line(box, INNER, zone=0, closed=True)
    elif style == "teeth_model":                                    # Zahnmodell (Kiefer mit Zähnen)
        c.fill(smooth([(x0, H * 0.3, "s"), (0, 0, "s"), (x1, H * 0.3, "s"), (x1 - 2, H * 0.6), (x0 + 2, H * 0.6)]), zone=1)
        for k in range(6):
            x = x0 + 3 + k * (W - 6) / 5
            c.fill(rrect(x - 1.6, H * 0.5, x + 1.6, H * 0.95, 1.2), zone=3, shade=1.6)
    elif style == "big_toothbrush":
        c.fill(rrect(-W * 0.2, 0, W * 0.2, H * 0.7, W * 0.2), zone=1)
        c.fill(rrect(-W * 0.35, H * 0.72, W * 0.35, H * 0.8, 0.5), zone=1, shade=0.85)
        for k in range(5):
            c.fill(rrect(-W * 0.3 + k * W * 0.13, H * 0.8, -W * 0.3 + k * W * 0.13 + W * 0.08, H, 0.4), zone=2)
    elif style == "ambulance":                                      # Krankenwagen (Zustand: Blaulicht an)
        body = rrect(x0, 16, x1 - W * 0.22, H * 0.9, 4.0)
        shaded(c, body, 1, "bottom", SHADE, 0.2)
        cab = smooth([(x1 - W * 0.24, 16, "s"), (x1, 16, "s"), (x1, H * 0.45), (x1 - W * 0.08, H * 0.7), (x1 - W * 0.24, H * 0.72, "s")])
        shaded(c, cab, 1, "bottom", SHADE, 0.2)
        c.fill([(x1 - W * 0.2, H * 0.44), (x1 - W * 0.07, H * 0.44), (x1 - W * 0.1, H * 0.66), (x1 - W * 0.2, H * 0.66)], zone=3,
               shade=1.5)
        c.fill(rrect(x0, H * 0.4, x1, H * 0.48, 0.5), zone=2)
        _cross(c, x0 + W * 0.3, H * 0.65, H * 0.22, zone=2)
        c.fill(rrect(x0 + W * 0.52, 20, x0 + W * 0.7, H * 0.8, 1.5), zone=1, shade=0.94)
        for k, x in enumerate((x0 + W * 0.15, x0 + W * 0.3)):
            c.fill(rrect(x - 3, H * 0.9, x + 3, H * 0.97, 1.0), zone=2 if (state == "on" and k == 0) or state != "on" else 3,
                   shade=1.4 if state == "on" else 0.9)
        if state == "on":
            for sx in (-1, 1):
                c.line(smooth([(x0 + W * 0.15 + sx * 8, H), (x0 + W * 0.15 + sx * 14, H * 1.08)], closed=False), 0.8, zone=2)
        for wx in (x0 + W * 0.18, x1 - W * 0.16):
            c.fill(ell(wx, 14, 14, 14, 28), zone=0)
            c.fill(ell(wx, 14, 6, 6, 16), zone=3, shade=1.2)
        c.line(body, INNER, zone=0, closed=True)
        c.line(cab, INNER, zone=0, closed=True)
    elif style == "helicopter":                                     # Rettungshubschrauber (Zustand: Rotor dreht)
        c.line([(x0 + W * 0.2, 4), (x1 - W * 0.2, 4)], 2.0, zone=3)
        for x in (x0 + W * 0.3, x1 - W * 0.3):
            c.line([(x, 4), (x, H * 0.18)], 1.4, zone=3)
        body = smooth([(x0 + W * 0.25, H * 0.2, "s"), (x1 - W * 0.12, H * 0.2, "s"), (x1, H * 0.4), (x1 - W * 0.1, H * 0.7),
                       (x0 + W * 0.3, H * 0.72, "s"), (x0 + W * 0.2, H * 0.45)])
        shaded(c, body, 1, "bottom", SHADE, 0.3)
        c.fill([(x0 + W * 0.25, H * 0.45), (x0, H * 0.55), (x0, H * 0.62), (x0 + W * 0.3, H * 0.6)], zone=1, shade=0.9)
        c.fill(ell(x0 + 4, H * 0.62, 6, 8, 16), zone=3)
        c.fill(smooth([(x1 - W * 0.22, H * 0.42, "s"), (x1 - W * 0.03, H * 0.42), (x1 - W * 0.1, H * 0.64), (x1 - W * 0.22, H * 0.64, "s")]),
               zone=3, shade=1.5)
        _cross(c, x0 + W * 0.5, H * 0.45, H * 0.16, zone=2)
        c.fill(rrect(-3, H * 0.72, 3, H * 0.8, 0.5), zone=3)
        if state == "on":                                           # Rotor verwischt
            c.fill(ell(0, H * 0.82, W * 0.5, H * 0.03, 40), zone=3, shade=0.8, alpha=0.45)
        else:
            c.fill(rrect(x0 + 2, H * 0.8, x1 - 2, H * 0.84, 0.6), zone=3, shade=0.7)
        c.line(body, INNER, zone=0, closed=True)
    elif style == "helipad":                                        # Landeplatz (flach, wie Teppich)
        pad = ell(0, H / 2, W / 2, H / 2, 48)
        c.fill(pad, zone=1)
        c.line(ell(0, H / 2, W * 0.42, H * 0.42, 48), 1.6, zone=2, closed=True)
        c.fill(rrect(-W * 0.2, H * 0.2, -W * 0.12, H * 0.8, 0.5), zone=2)
        c.fill(rrect(W * 0.12, H * 0.2, W * 0.2, H * 0.8, 0.5), zone=2)
        c.fill(rrect(-W * 0.12, H * 0.44, W * 0.12, H * 0.56, 0.5), zone=2)
