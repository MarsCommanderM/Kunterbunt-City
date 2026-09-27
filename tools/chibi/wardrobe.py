"""
Kleidung (Oberteile, Ärmel, Unterteile, Schuhe) im Stil „großer Kopf“ – Phase 04b.

Zonen: 1 = Hauptstoff · 2 = Zweitfarbe (Kragen, Bündchen, Träger) · 3 = je nach Ebene
(Top: Drittfarbe, Beine/Schuhe: Haut). Muster kommen NICHT ins Sprite, sondern per Shader
über Zone 1 (siehe patterns.py) – so ergibt jede Form × jedes Muster ein eigenes Teil ohne neue Bilder.
"""
from __future__ import annotations

import math

from .body import DEEP, SHADE, draw_legs_skin_into, legs_box
from .vec import ZCanvas, blob, path


# ------------------------------------------------------------------ Oberteile
def torso_pts(t: dict, hem: float = 0.0, flare: float = 0.0, grow: float = 0.0) -> list:
    """Rumpf: runde Schultern, leicht ausgestellt. hem = Saum unter torso.bot, flare = Zusatzbreite unten."""
    to = t["torso"]
    wt, wb = to["w_top"] / 2 + grow, to["w_bot"] / 2 + flare + grow
    top, bot = to["top"] + grow, to["bot"] - hem - grow
    r = wt * 0.45
    return path((-wt + r * 0.2, top), ((-wt - r * 0.15, top), (-wt - r * 0.1, top - r * 1.1), (-wt, top - r * 1.4)),
                ((-wb, bot + 1.5),), ((-wb, bot), (-wb + 1, bot - 0.4), (-wb + 2, bot - 0.4)),
                ((wb - 2, bot - 0.4),), ((wb - 1, bot - 0.4), (wb, bot), (wb, bot + 1.5)),
                ((wt, top - r * 1.4),), ((wt + r * 0.1, top - r * 1.1), (wt + r * 0.15, top), (wt - r * 0.2, top)))


def torso_box(t: dict, extra: float = 14) -> tuple:
    to = t["torso"]
    w = max(to["w_top"], to["w_bot"]) / 2 + extra
    return (-w, to["bot"] - extra - 30, w, to["top"] + extra)


def _neck(t: dict, depth: float = 0.12, width: float = 0.3) -> list:
    to = t["torso"]
    w = to["w_top"] * width
    top = to["top"] + 2
    return blob(0, top, w, to["w_top"] * depth + 2, n=48)


def _side_shade(c: ZCanvas, t: dict, clip, zone: int = 1):
    to = t["torso"]
    c.fill([(to["w_top"] * 0.18, to["top"] + 5), (60, to["top"] + 5), (60, to["bot"] - 40), (to["w_bot"] * 0.22, to["bot"] - 40)],
           zone=zone, shade=SHADE, clip=clip)


TOP_STYLES = ["tee", "raglan", "tee_star", "longsleeve", "tank", "hoodie", "sweater", "shirt", "jacket", "dress", "sundress", "overalls",
              "polo", "raincoat"]
SLEEVE_OF = {"raglan": "raglan", "tee_star": "short", "tee": "short", "polo": "short", "tank": "none", "sundress": "none", "overalls": "short",
             "longsleeve": "long", "hoodie": "long", "sweater": "long", "shirt": "long", "jacket": "long",
             "dress": "short", "raincoat": "long"}


def draw_top(t: dict, style: str, ppc: float):
    to = t["torso"]
    c = ZCanvas(torso_box(t), ppc)
    hem = {"dress": to["top"] - to["bot"] - 4, "sundress": to["top"] - to["bot"] - 4, "raincoat": 10,
           "jacket": 3, "hoodie": 3, "sweater": 2}.get(style, 1.0)
    flare = {"dress": 9, "sundress": 11, "raincoat": 4}.get(style, 0.0)
    body = torso_pts(t, hem=0 if style not in ("dress", "sundress") else 0, flare=0)
    if style in ("dress", "sundress"):
        # Kleid: Oberteil + Glockenrock bis zum Knie
        bot = to["bot"] - hem
        wb = to["w_bot"] / 2 + flare
        skirt = path((-to["w_bot"] / 2 + 1, to["bot"] + 4), ((-wb, bot + 2),), ((-wb + 1, bot - 1), (wb - 1, bot - 1), (wb, bot + 2)),
                     ((to["w_bot"] / 2 - 1, to["bot"] + 4),))
        c.fill(skirt, zone=1)
        cm = c.mask(skirt)
        for k in (-0.5, 0.0, 0.5):   # Falten
            x = k * wb
            c.line([(x * 0.6, to["bot"] + 2), (x, bot + 2)], w_cm=0.5, zone=1, shade=DEEP, clip=cm)
        c.fill([(wb * 0.25, to["bot"] + 6), (60, to["bot"] + 6), (60, bot - 5), (wb * 0.35, bot - 5)], zone=1, shade=SHADE, clip=cm)
        c.fill(skirt[:0] or path((-wb, bot + 2.8), ((wb, bot + 2.8),), ((wb, bot - 2),), ((-wb, bot - 2),)), zone=2, clip=cm)
    else:
        body = torso_pts(t, hem=hem, flare=flare)
    c.fill(body, zone=1)
    clip = c.mask(body)
    _side_shade(c, t, clip)
    if style in ("tank", "sundress"):
        # Träger + Haut-Ausschnitt: Ausschnitt ist transparent (Haut vom Kopf/Hals verdeckt)
        c.fill(_neck(t, 0.32, 0.36), zone=3, clip=clip)
    elif style in ("raglan", "tee_star"):
        c.fill(_neck(t, 0.14, 0.3), zone=2, clip=clip)
        c.fill(_neck(t, 0.09, 0.24), zone=3, clip=clip)
        if style == "raglan":   # schräge Ärmelnaht bis zum Kragen in Zone 2
            for sx in (-1, 1):
                c.fill([(sx * to["w_top"] * 0.26, to["top"] + 2), (sx * 40, to["top"] + 2), (sx * 40, to["top"] - to["w_top"] * 0.62),
                        (sx * to["w_top"] * 0.5, to["top"] - to["w_top"] * 0.62)], zone=2, clip=clip)
        # Brustbild: Kreis (Zone 2) mit Stern (Zone 1)
        py = to["top"] - (to["top"] - to["bot"]) * 0.45
        pr = to["w_top"] * 0.17
        c.ellipse(0, py, pr, pr, zone=2, clip=clip)
        c.line(blob(0, py, pr, pr), 0.45, zone=0, closed=True, clip=clip)
        star = []
        for i in range(10):
            a = math.pi / 2 + i * math.pi / 5
            rr = pr * (0.75 if i % 2 == 0 else 0.32)
            star.append((math.cos(a) * rr, py + math.sin(a) * rr))
        c.fill(star, zone=1 if style == "tee_star" else 3)
        c.line(star, 0.4, zone=0, closed=True)
    elif style == "tee" or style == "dress":
        c.fill(_neck(t, 0.14, 0.3), zone=2, clip=clip)
        c.fill(_neck(t, 0.09, 0.24), zone=3, clip=clip)
    elif style == "longsleeve":
        c.fill(_neck(t, 0.11, 0.28), zone=2, clip=clip)
        c.fill(_neck(t, 0.06, 0.22), zone=3, clip=clip)
    elif style == "polo":
        c.fill(_neck(t, 0.12, 0.26), zone=3, clip=clip)
        for sx in (-1, 1):
            c.fill([(0, to["top"] - to["w_top"] * 0.18), (sx * to["w_top"] * 0.32, to["top"] + 1),
                    (sx * to["w_top"] * 0.36, to["top"] - to["w_top"] * 0.14)], zone=2)
        c.line([(0, to["top"] - to["w_top"] * 0.16), (0, to["top"] - to["w_top"] * 0.45)], 0.5, zone=2, shade=DEEP)
    elif style == "shirt":
        c.fill(_neck(t, 0.1, 0.22), zone=3, clip=clip)
        for sx in (-1, 1):
            c.fill([(0, to["top"] - to["w_top"] * 0.2), (sx * to["w_top"] * 0.3, to["top"] + 1),
                    (sx * to["w_top"] * 0.34, to["top"] - to["w_top"] * 0.18)], zone=2)
        c.line([(0, to["top"] - to["w_top"] * 0.2), (0, to["bot"] - hem + 1)], 0.45, zone=1, shade=DEEP, clip=clip)
        for i in range(3):
            y = to["top"] - (to["top"] - to["bot"]) * (0.32 + i * 0.22)
            c.ellipse(1.3, y, 0.7, 0.7, zone=2)
    elif style in ("hoodie", "sweater"):
        c.fill(_neck(t, 0.1, 0.27), zone=3, clip=clip)
        # Bündchen unten
        c.fill([(-60, to["bot"] - hem + 3), (60, to["bot"] - hem + 3), (60, to["bot"] - hem - 5), (-60, to["bot"] - hem - 5)],
               zone=1, shade=0.92, clip=clip)
        if style == "hoodie":
            # Kapuze hinter dem Nacken (sichtbar an den Schultern), Bauchtasche, Kordeln
            for sx in (-1, 1):
                c.line([(sx * to["w_top"] * 0.12, to["top"] - 1), (sx * to["w_top"] * 0.14, to["top"] - to["w_top"] * 0.45)],
                       0.55, zone=2)
            py = to["bot"] - hem + (to["top"] - to["bot"]) * 0.42
            pocket = path((-to["w_bot"] * 0.3, py), ((to["w_bot"] * 0.3, py),), ((to["w_bot"] * 0.36, to["bot"] - hem + 4),),
                          ((-to["w_bot"] * 0.36, to["bot"] - hem + 4),))
            c.fill(pocket, zone=1, shade=0.93, clip=clip)
            c.line(pocket, 0.45, zone=1, shade=DEEP, closed=True, clip=clip)
        else:
            c.fill(_neck(t, 0.13, 0.31), zone=2, clip=clip)
            c.fill(_neck(t, 0.1, 0.27), zone=3, clip=clip)
    elif style in ("jacket", "raincoat"):
        # offene Jacke über einem Shirt (Zone 2)
        inner = path((-to["w_top"] * 0.2, to["top"] + 1), ((to["w_top"] * 0.2, to["top"] + 1),),
                     ((to["w_bot"] * 0.12, to["bot"] - hem),), ((-to["w_bot"] * 0.12, to["bot"] - hem),))
        if style == "jacket":
            c.fill(inner, zone=2, clip=clip)
            c.fill(_neck(t, 0.08, 0.2), zone=3, clip=clip)
            for sx in (-1, 1):
                c.line([(sx * to["w_top"] * 0.2, to["top"]), (sx * to["w_bot"] * 0.12, to["bot"] - hem)], 0.55, zone=1, shade=DEEP, clip=clip)
        else:
            c.fill(_neck(t, 0.1, 0.24), zone=3, clip=clip)
            c.line([(0, to["top"] - to["w_top"] * 0.2), (0, to["bot"] - hem + 1)], 0.5, zone=1, shade=DEEP, clip=clip)
            for i in range(4):
                y = to["top"] - (to["top"] - to["bot"] + hem) * (0.25 + i * 0.2)
                c.ellipse(2.0, y, 0.9, 0.9, zone=2)
        for sx in (-1, 1):   # Taschen
            x = sx * to["w_bot"] * 0.3
            c.line([(x - 3, to["bot"] - hem + 9), (x + 3, to["bot"] - hem + 9)], 0.6, zone=1, shade=DEEP, clip=clip)
    elif style == "overalls":
        # Latz (Zone 1) über T-Shirt (Zone 2) – Hosenteil kommt vom Unterteil
        c.fill(body, zone=2)
        _side_shade(c, t, clip, zone=2)
        c.fill(_neck(t, 0.12, 0.28), zone=3, clip=clip)
        bib = path((-to["w_top"] * 0.3, to["top"] - (to["top"] - to["bot"]) * 0.35), ((to["w_top"] * 0.3, to["top"] - (to["top"] - to["bot"]) * 0.35),),
                   ((to["w_bot"] * 0.5 + 1, to["bot"] - 2),), ((-to["w_bot"] * 0.5 - 1, to["bot"] - 2),))
        c.fill(bib, zone=1, clip=clip)
        for sx in (-1, 1):
            c.line([(sx * to["w_top"] * 0.26, to["top"] - (to["top"] - to["bot"]) * 0.35), (sx * to["w_top"] * 0.34, to["top"] + 1)],
                   to["w_top"] * 0.09, zone=1, clip=clip)
            c.ellipse(sx * to["w_top"] * 0.24, to["top"] - (to["top"] - to["bot"]) * 0.38, 0.9, 0.9, zone=0)
        py = to["top"] - (to["top"] - to["bot"]) * 0.55
        c.line(path((-to["w_top"] * 0.16, py), ((to["w_top"] * 0.16, py),), ((to["w_top"] * 0.14, py - 6),), ((-to["w_top"] * 0.14, py - 6),)),
               0.45, zone=1, shade=DEEP, closed=True)
    c.outline_under()
    return c.render_part((0, to["bot"]))


def draw_sleeve(t: dict, kind: str, ppc: float):
    """Ärmel auf dem Arm (senkrecht, Anker = Schulter)."""
    ar = t["arm"]
    L, w = ar["len"], ar["w"]
    c = ZCanvas((-w * 1.5, -L - 4, w * 1.5, w * 1.5), ppc)
    if kind == "none":
        c.ellipse(0, 0, 0.01, 0.01, zone=1)
        return c.render_part((0, 0))
    z = 2 if kind == "raglan" else 1
    kind = "long" if kind == "raglan" else kind
    ln = L * (0.42 if kind == "short" else 0.93) - (0 if kind == "short" else t["hand_r"] * 0.6)
    ww = w * (0.68 if kind == "short" else 0.6)
    pts = path((-w * 0.62, w * 0.35), ((-w * 0.62, w * 1.05), (w * 0.62, w * 1.05), (w * 0.62, w * 0.35)),
               ((ww, -ln),), ((ww * 0.3, -ln - 0.8), (-ww * 0.3, -ln - 0.8), (-ww, -ln)))
    c.fill(pts, zone=z)
    cl = c.mask(pts)
    c.fill([(w * 0.1, w * 2), (w * 2, w * 2), (w * 2, -L - 4), (w * 0.1, -L - 4)], zone=z, shade=SHADE, clip=cl)
    if kind == "long":
        c.fill([(-w, -ln + 3), (w, -ln + 3), (w, -ln - 2), (-w, -ln - 2)], zone=z, shade=0.93, clip=cl)
    c.outline_under()
    return c.render_part((0, 0))


# ------------------------------------------------------------------ Unterteile (Anker = Boden)
BOTTOM_STYLES = ["trousers", "jeans", "shorts", "skirt", "leggings", "dungarees", "tutu", "joggers"]


def _pants_pts(t: dict, leg_bottom: float, flare: float = 0.0, extra_top: float = 3.0) -> list:
    hip, lg, to = t["hip"], t["leg"], t["torso"]
    wb = to["w_bot"] / 2 - 0.5
    top = hip["y"] + extra_top
    x = hip["x"]
    w = lg["w"] / 2 + flare
    return path((-wb, top), ((-x - w, leg_bottom + 4),), ((-x - w, leg_bottom),), ((-x + w, leg_bottom),),
                ((-x + w * 0.9, hip["y"] - 3),), ((-0.6, hip["y"] - 5), (0.6, hip["y"] - 5), (x - w * 0.9, hip["y"] - 3)),
                ((x - w, leg_bottom),), ((x + w, leg_bottom),), ((x + w, leg_bottom + 4),), ((wb, top),))


def draw_bottom(t: dict, style: str, ppc: float, sit: bool = False):
    hip, lg, sh = t["hip"], t["leg"], t["shoe"]
    if sit:
        return draw_bottom_sit(t, style, ppc)
    c = ZCanvas(legs_box(t), ppc)
    draw_legs_skin_into(c, t)
    sole = sh["h"] * 0.55
    if style in ("trousers", "jeans", "leggings", "joggers", "dungarees"):
        pts = _pants_pts(t, sole, flare=0.4 if style != "leggings" else -0.8)
        c.fill(pts, zone=1)
        cl = c.mask(pts)
        for sx in (-1, 1):
            x = sx * hip["x"]
            c.fill([(x + lg["w"] * 0.1 * sx, hip["y"]), (x + sx * 20, hip["y"]), (x + sx * 20, -5), (x + lg["w"] * 0.1 * sx, -5)],
                   zone=1, shade=SHADE, clip=cl)
            if style == "jeans":
                c.line([(x + sx * lg["w"] * 0.2, hip["y"] - 4), (x + sx * lg["w"] * 0.2, sole + 2)], 0.35, zone=2, clip=cl)
            if style == "joggers":
                c.fill([(x - 20, sole + 3.5), (x + 20, sole + 3.5), (x + 20, sole - 2), (x - 20, sole - 2)], zone=2, clip=cl)
            if style in ("trousers", "jeans"):
                c.fill([(x - 20, sole + 1.6), (x + 20, sole + 1.6), (x + 20, sole - 2), (x - 20, sole - 2)], zone=1, shade=0.9, clip=cl)
        c.fill([(-40, hip["y"] + 3.2), (40, hip["y"] + 3.2), (40, hip["y"] + 0.8), (-40, hip["y"] + 0.8)],
               zone=2 if style in ("jeans", "joggers") else 1, shade=0.92, clip=cl)
    elif style == "shorts":
        knee = hip["y"] * 0.5
        pts = _pants_pts(t, knee, flare=1.2)
        c.fill(pts, zone=1)
        cl = c.mask(pts)
        c.fill([(0, 99), (40, 99), (40, -5), (hip["x"] * 1.1, -5)], zone=1, shade=SHADE, clip=cl)
        c.fill([(-40, knee + 2.2), (40, knee + 2.2), (40, knee - 2), (-40, knee - 2)], zone=2, clip=cl)
    elif style in ("skirt", "tutu"):
        top = hip["y"] + 3
        bot = hip["y"] * (0.5 if style == "skirt" else 0.6)
        wb = t["torso"]["w_bot"] / 2 + (4 if style == "skirt" else 9)
        pts = path((-t["torso"]["w_bot"] / 2, top), ((-wb, bot + 1),), ((-wb * 0.6, bot - 1.5), (wb * 0.6, bot - 1.5), (wb, bot + 1)),
                   ((t["torso"]["w_bot"] / 2, top),))
        c.fill(pts, zone=1)
        cl = c.mask(pts)
        if style == "tutu":
            for i in range(9):
                x = -wb + wb * 2 * (i + 0.5) / 9
                c.ellipse(x, bot + 0.5, wb / 9 * 1.2, 2.2, zone=1)
            c.fill(pts, zone=1)
            c.fill([(-40, top + 1), (40, top + 1), (40, top - 3), (-40, top - 3)], zone=2, clip=cl)
        else:
            for k in (-0.55, 0.0, 0.55):
                c.line([(k * t["torso"]["w_bot"] * 0.45, top - 3), (k * wb, bot + 1)], 0.45, zone=1, shade=DEEP, clip=cl)
            c.fill([(wb * 0.3, top), (40, top), (40, bot - 5), (wb * 0.45, bot - 5)], zone=1, shade=SHADE, clip=cl)
            c.fill([(-40, bot + 2.5), (40, bot + 2.5), (40, bot - 3), (-40, bot - 3)], zone=2, clip=cl)
    if style == "dungarees":
        # Latzhose: Taschen vorn, Träger gehören zum Oberteil „overalls“
        for sx in (-1, 1):
            x = sx * hip["x"] * 1.2
            c.line([(x - 2, hip["y"] - 1), (x + 2, hip["y"] - 1)], 0.5, zone=1, shade=DEEP)
    c.outline_under()
    return c.render_part((0, 0))


def draw_bottom_sit(t: dict, style: str, ppc: float):
    """Sitzend von vorn: Schoß (verkürzter Oberschenkel) + Unterschenkel ab Hüfte. Anker = Hüfte."""
    hip, lg, sh = t["hip"], t["leg"], t["shoe"]
    drop = lg["shin"] + 2.0
    c = ZCanvas((-hip["x"] - lg["w"] * 2, hip["y"] - drop - 3, hip["x"] + lg["w"] * 2, hip["y"] + 6), ppc)
    y0 = hip["y"]
    # nackte Unterschenkel
    for sx in (-1, 1):
        x = sx * hip["x"]
        c.fill(path((x - lg["w"] * 0.43, y0), ((x - lg["w"] * 0.43, y0 - drop + 1),), ((x + lg["w"] * 0.43, y0 - drop + 1),),
                    ((x + lg["w"] * 0.43, y0),)), zone=3)
    covered = {"trousers": 1.0, "jeans": 1.0, "leggings": 1.0, "joggers": 1.0, "dungarees": 1.0,
               "shorts": 0.0, "skirt": 0.0, "tutu": 0.0}.get(style, 0.0)
    wb = t["torso"]["w_bot"] / 2
    lap = path((-wb, y0 + 3), ((-wb - 1, y0 - lg["sit_thigh"] * 0.9),), ((wb + 1, y0 - lg["sit_thigh"] * 0.9),), ((wb, y0 + 3),))
    if style in ("skirt", "tutu"):
        lap = path((-wb, y0 + 3), ((-wb - 5, y0 - lg["sit_thigh"] * 1.1),), ((wb + 5, y0 - lg["sit_thigh"] * 1.1),), ((wb, y0 + 3),))
    c.fill(lap, zone=1)
    if covered:
        for sx in (-1, 1):
            x = sx * hip["x"]
            c.fill(path((x - lg["w"] * 0.5, y0 - 2), ((x - lg["w"] * 0.5, y0 - drop + sh["h"] * 0.6),),
                        ((x + lg["w"] * 0.5, y0 - drop + sh["h"] * 0.6),), ((x + lg["w"] * 0.5, y0 - 2),)), zone=1)
    c.fill([(0, y0 + 10), (40, y0 + 10), (40, y0 - drop - 5), (hip["x"] * 1.05, y0 - drop - 5)], zone=1, shade=SHADE,
           clip=c.mask(lap))
    c.outline_under()
    return c.render_part((0, y0))


# ------------------------------------------------------------------ Schuhe (Anker = Boden)
SHOE_STYLES = ["sneaker_socks", "sneaker", "boot", "sandal", "slipper", "rainboot", "ballet", "hightop", "barefoot"]


def draw_shoes(t: dict, style: str, ppc: float):
    hip, sh = t["hip"], t["shoe"]
    c = ZCanvas((-hip["x"] - sh["w"] * 1.5, -2, hip["x"] + sh["w"] * 1.5, sh["h"] * 3 + 6), ppc)
    for sx in (-1, 1):
        x = sx * hip["x"] + sx * 0.6
        w, h = sh["w"] / 2, sh["h"]
        if style == "sneaker_socks":
            up = t["leg"]["shin"] * 0.55
            sock = path((x - w * 0.5, up), ((x - w * 0.52, h * 0.5),), ((x + w * 0.52, h * 0.5),), ((x + w * 0.5, up),))
            c.fill(sock, zone=2)
            sc = c.mask(sock)
            for k in (0.78, 0.6):
                c.fill([(x - w, up * k + 0.9), (x + w, up * k + 0.9), (x + w, up * k - 0.9), (x - w, up * k - 0.9)], zone=1, clip=sc)
            c.fill([(x + sx * w * 0.05, up), (x + sx * w, up), (x + sx * w, 0), (x + sx * w * 0.05, 0)], zone=2, shade=SHADE, clip=sc)
        if style == "barefoot":
            c.ellipse(x, h * 0.35, w * 0.8, h * 0.45, zone=3)
            continue
        if style in ("boot", "rainboot", "hightop"):
            up = h * (2.2 if style != "hightop" else 1.5)
            shaft = path((x - w * 0.62, up), ((x - w * 0.7, h * 0.5),), ((x + w * 0.7, h * 0.5),), ((x + w * 0.62, up),))
            c.fill(shaft, zone=1)
            c.fill([(x - w * 0.8, up + 0.2), (x + w * 0.8, up + 0.2), (x + w * 0.8, up - 1.6), (x - w * 0.8, up - 1.6)],
                   zone=2, clip=c.mask(shaft))
        body = blob(x + sx * w * 0.1, h * 0.6, w * 1.05, h * 0.66, n=48, top=1.1)
        if style == "sandal":
            c.ellipse(x + sx * w * 0.05, h * 0.55, w * 0.85, h * 0.5, zone=3)
            c.fill([(x - w, h * 0.22), (x + w, h * 0.22), (x + w, 0), (x - w, 0)], zone=1)
            c.line([(x - w * 0.7, h * 0.75), (x + w * 0.7, h * 0.75)], h * 0.25, zone=1)
            continue
        c.fill(body, zone=1)
        cl = c.mask(body)
        c.fill([(x - w * 2, h * 0.34), (x + w * 2, h * 0.34), (x + w * 2, -1), (x - w * 2, -1)],
               zone=2 if style in ("sneaker", "sneaker_socks", "hightop", "rainboot") else 1, shade=1.0 if style != "boot" else 0.8, clip=cl)
        if style in ("sneaker", "sneaker_socks", "hightop"):
            c.line([(x - w * 0.35, h * 0.8), (x + w * 0.2, h * 0.9)], 0.45, zone=2, clip=cl)
            c.line([(x - w * 0.3, h * 0.62), (x + w * 0.25, h * 0.72)], 0.45, zone=2, clip=cl)
        if style == "ballet":
            c.line([(x - w * 0.2, h * 0.95), (x + w * 0.2, h * 0.95)], 0.8, zone=2)
    c.outline_under()
    # Sohle (samt Kontur) steht genau auf dem Boden: Anker = unterste bemalte Stelle
    return c.render_part((0, c.content_bottom_cm()))
