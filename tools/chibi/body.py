"""
Körper, Kopf und Gesicht der Figuren (Phase 04b · Stil „großer Kopf“).

Alle Maße kommen aus data/characters/templates.json (cm, Ursprung zwischen den Füßen, y nach oben).
Jede Funktion malt EIN Teil in Figuren-Koordinaten und gibt (Bild, Info) zurück – Info = parts.json-Format.

Farbzonen je Ebene (siehe CharacterLook.colors_for):
    Kopf/Haut: 1 = Haut · 2 = Wangenrot (aus der Haut abgeleitet)
    Augen:     1 = Augenfarbe · 2 = Glanz (weiß) · 3 = Augenbrauen (= Haarfarbe)
    Mund:      1 = Mundinneres · 2 = Zunge
    Beine/Schuhe: 1, 2 = Stoff · 3 = Haut (nackte Beine, Zehen)
"""
from __future__ import annotations

import math

from .vec import ZCanvas, blob, path

SHADE = 0.86        # Schattenseite einer Fläche (Richtung Tinte)
DEEP = 0.72         # dunkle Linien in der Fläche (Falten, Strähnen)


# ------------------------------------------------------------------ Hilfen
def head_box(t: dict, extra: float = 12.0) -> tuple[float, float, float, float]:
    hd = t["head"]
    return (-hd["w"] / 2 - extra, hd["cy"] - hd["h"] / 2 - extra, hd["w"] / 2 + extra, t["hair_top"] + extra)


def head_outline(t: dict, grow: float = 0.0) -> list:
    """Kopfform: oben rund, Wangen breit, Kinn weich."""
    hd = t["head"]
    return blob(0, hd["cy"], hd["w"] / 2 + grow, hd["h"] / 2 + grow, n=96, squish=0.35, top=1.0)


def eye_pos(t: dict) -> tuple[float, float, float]:
    """Augen-Mittelpunkte (±x, y) und Augenradius (cm)."""
    hd = t["head"]
    return hd["w"] * 0.2, hd["cy"] - hd["h"] * 0.06, hd["w"] * 0.055


# ------------------------------------------------------------------ Kopf
def draw_head(t: dict, ppc: float):
    hd = t["head"]
    c = ZCanvas(head_box(t, 8), ppc)
    ex = hd["w"] / 2
    ey = hd["cy"] - hd["h"] * 0.05
    for sx in (-1, 1):                                   # Ohren
        c.ellipse(sx * (ex + hd["w"] * 0.015), ey, hd["w"] * 0.1, hd["h"] * 0.12, zone=1)
    c.outline_under()
    head = head_outline(t)
    c.fill(head, zone=1)
    clip = c.mask(head)
    # weicher Schatten unten (Kinn) – liegt nur im Kopf
    c.fill(blob(0, hd["cy"] - hd["h"] * 0.55, hd["w"] * 0.62, hd["h"] * 0.22), zone=1, shade=0.93, clip=clip)
    # Wangen
    for sx in (-1, 1):
        c.ellipse(sx * hd["w"] * 0.3, hd["cy"] - hd["h"] * 0.2, hd["w"] * 0.085, hd["h"] * 0.05, zone=2, clip=clip)
    # Ohr-Innenlinie
    for sx in (-1, 1):
        x = sx * (ex + hd["w"] * 0.02)
        c.line([(x - sx * hd["w"] * 0.035, ey + hd["h"] * 0.06), (x + sx * hd["w"] * 0.02, ey + hd["h"] * 0.02),
                (x + sx * hd["w"] * 0.02, ey - hd["h"] * 0.03), (x - sx * hd["w"] * 0.03, ey - hd["h"] * 0.06)],
               w_cm=0.55, zone=1, shade=0.62)
    c.outline_under()
    return c.render_part((0, hd["cy"]))


def draw_nose_into(c: ZCanvas, t: dict):
    hd = t["head"]
    y = hd["cy"] - hd["h"] * 0.14
    c.ellipse(0, y, hd["w"] * 0.022, hd["h"] * 0.016, zone=0)


# ------------------------------------------------------------------ Augen (Ebene „Eyes“)
EYE_STYLES = ["dot", "round", "big", "lash", "sleepy", "wink", "star", "happy_closed"]
EMO_EYES = {"laugh": "happy_closed", "sad": "sad", "love": "love", "tired": "sleepy", "surprised": "big"}


def _brows(c: ZCanvas, t: dict, mood: str = "calm"):
    hd = t["head"]
    x0, y0, r = eye_pos(t)
    for sx in (-1, 1):
        cx = sx * x0
        by = y0 + r * 3.1
        tilt = {"calm": 0.0, "sad": 0.9, "up": -0.3}[mood] * sx
        c.line([(cx - hd["w"] * 0.06, by - r * 0.1 + tilt * r * 0.6), (cx, by + r * 0.35),
                (cx + hd["w"] * 0.06, by - r * 0.1 - tilt * r * 0.6)], w_cm=hd["w"] * 0.022, zone=3)


def draw_eyes(t: dict, style: str, ppc: float):
    hd = t["head"]
    c = ZCanvas(head_box(t, 2), ppc, outline_cm=0)
    x0, y0, r = eye_pos(t)
    mood = "sad" if style == "sad" else ("up" if style in ("big", "star") else "calm")
    _brows(c, t, mood)
    for sx in (-1, 1):
        x = sx * x0
        if style in ("dot", "sad"):
            c.ellipse(x, y0, r * 0.95, r * 1.2, zone=0)
            c.ellipse(x + r * 0.3, y0 + r * 0.45, r * 0.3, r * 0.3, zone=2)
        elif style == "round":
            c.ellipse(x, y0, r * 1.2, r * 1.35, zone=0)
            c.ellipse(x, y0 - r * 0.1, r * 0.85, r * 1.0, zone=1)
            c.ellipse(x, y0 - r * 0.1, r * 0.5, r * 0.6, zone=0)
            c.ellipse(x + r * 0.35, y0 + r * 0.45, r * 0.32, r * 0.32, zone=2)
        elif style in ("big",):
            c.ellipse(x, y0, r * 1.45, r * 1.7, zone=0)
            c.ellipse(x, y0 - r * 0.15, r * 1.1, r * 1.3, zone=1)
            c.ellipse(x, y0 - r * 0.25, r * 0.6, r * 0.75, zone=0)
            c.ellipse(x + r * 0.45, y0 + r * 0.55, r * 0.42, r * 0.42, zone=2)
            c.ellipse(x - r * 0.4, y0 - r * 0.6, r * 0.2, r * 0.2, zone=2)
        elif style == "lash":
            c.ellipse(x, y0, r * 1.0, r * 1.25, zone=0)
            c.ellipse(x + r * 0.3, y0 + r * 0.45, r * 0.3, r * 0.3, zone=2)
            c.line([(x + sx * r * 0.7, y0 + r * 0.9), (x + sx * r * 1.5, y0 + r * 1.35)], w_cm=r * 0.35, zone=0)
            c.line([(x + sx * r * 0.95, y0 + r * 0.45), (x + sx * r * 1.7, y0 + r * 0.7)], w_cm=r * 0.32, zone=0)
        elif style == "sleepy":
            c.line([(x - r * 1.2, y0 + r * 0.1), (x - r * 0.4, y0 - r * 0.45), (x + r * 0.4, y0 - r * 0.45),
                    (x + r * 1.2, y0 + r * 0.1)], w_cm=r * 0.45, zone=0)
        elif style == "happy_closed":
            c.line([(x - r * 1.2, y0 - r * 0.3), (x - r * 0.45, y0 + r * 0.55), (x + r * 0.45, y0 + r * 0.55),
                    (x + r * 1.2, y0 - r * 0.3)], w_cm=r * 0.5, zone=0)
        elif style == "wink":
            if sx < 0:
                c.ellipse(x, y0, r * 0.95, r * 1.2, zone=0)
                c.ellipse(x + r * 0.3, y0 + r * 0.45, r * 0.3, r * 0.3, zone=2)
            else:
                c.line([(x - r * 1.2, y0 + r * 0.2), (x, y0 - r * 0.2), (x + r * 1.2, y0 + r * 0.2)], w_cm=r * 0.45, zone=0)
                c.line([(x - r * 1.1, y0 - r * 0.2), (x, y0 + r * 0.25)], w_cm=r * 0.4, zone=0)
        elif style == "star":
            pts = []
            for i in range(10):
                a = math.pi / 2 + i * math.pi / 5
                rr = r * (1.45 if i % 2 == 0 else 0.62)
                pts.append((x + math.cos(a) * rr, y0 + math.sin(a) * rr))
            c.fill(pts, zone=0)
            c.ellipse(x + r * 0.2, y0 + r * 0.25, r * 0.22, r * 0.22, zone=2)
        elif style == "love":
            _heart(c, x, y0, r * 1.45, zone=0)
            _heart(c, x, y0 + r * 0.1, r * 1.05, zone=1)
    return c.render_part((0, hd["cy"]))


def _heart(c: ZCanvas, x: float, y: float, r: float, zone: int):
    pts = path((x, y - r), ((x - r * 0.4, y - r * 0.55), (x - r * 1.1, y - r * 0.1), (x - r * 1.0, y + r * 0.4)),
               ((x - r * 0.9, y + r * 0.95), (x - r * 0.15, y + r * 0.95), (x, y + r * 0.45)),
               ((x + r * 0.15, y + r * 0.95), (x + r * 0.9, y + r * 0.95), (x + r * 1.0, y + r * 0.4)),
               ((x + r * 1.1, y - r * 0.1), (x + r * 0.4, y - r * 0.55), (x, y - r)))
    c.fill(pts, zone=zone)


# ------------------------------------------------------------------ Mund (Ebene „Mouth“, mit Nase)
MOUTH_STYLES = ["smile", "grin", "oh", "tongue", "neutral", "happy", "laugh", "surprised", "sad", "tired", "love",
                "eat_open", "eat_closed"]


def draw_mouth(t: dict, style: str, ppc: float):
    hd = t["head"]
    c = ZCanvas(head_box(t, 2), ppc, outline_cm=0)
    draw_nose_into(c, t)
    y = hd["cy"] - hd["h"] * 0.235
    w = hd["w"] * 0.07
    lw = hd["w"] * 0.02
    if style in ("smile", "happy", "love"):
        c.line([(-w, y + w * 0.25), (-w * 0.4, y - w * 0.3), (w * 0.4, y - w * 0.3), (w, y + w * 0.25)], lw)
    elif style == "neutral" or style == "tired":
        c.line([(-w * 0.6, y), (w * 0.6, y)], lw)
    elif style == "sad":
        c.line([(-w, y - w * 0.3), (-w * 0.4, y + w * 0.2), (w * 0.4, y + w * 0.2), (w, y - w * 0.3)], lw)
    elif style in ("grin", "laugh", "eat_open"):
        big = 1.35 if style == "laugh" else 1.1
        pts = path((-w * big, y + w * 0.3), ((-w * big, y - w * 1.3 * big), (w * big, y - w * 1.3 * big), (w * big, y + w * 0.3)),
                   ((0, y + w * 0.3),))
        c.fill(pts, zone=0)
        inner = path((-w * big + lw, y + w * 0.3 - lw * 0.6),
                     ((-w * big + lw, y - w * 1.2 * big + lw), (w * big - lw, y - w * 1.2 * big + lw), (w * big - lw, y + w * 0.3 - lw * 0.6)),
                     ((0, y + w * 0.3 - lw * 0.6),))
        c.fill(inner, zone=1)
        c.ellipse(0, y - w * 0.75 * big, w * 0.55 * big, w * 0.35 * big, zone=2, clip=c.mask(inner))
    elif style in ("oh", "surprised"):
        c.ellipse(0, y - w * 0.2, w * 0.5, w * 0.62, zone=0)
        c.ellipse(0, y - w * 0.2, w * 0.5 - lw, w * 0.62 - lw, zone=1)
    elif style == "tongue":
        c.line([(-w, y + w * 0.25), (-w * 0.4, y - w * 0.3), (w * 0.4, y - w * 0.3), (w, y + w * 0.25)], lw)
        c.ellipse(w * 0.25, y - w * 0.6, w * 0.38, w * 0.45, zone=0)
        c.ellipse(w * 0.25, y - w * 0.62, w * 0.38 - lw * 0.8, w * 0.45 - lw * 0.8, zone=2)
    elif style == "eat_closed":
        c.ellipse(0, y - w * 0.1, w * 0.75, w * 0.45, zone=0)
        c.ellipse(0, y - w * 0.1, w * 0.75 - lw, w * 0.45 - lw, zone=2)
    return c.render_part((0, hd["cy"]))


# ------------------------------------------------------------------ Arme, Hände, Beine (Haut)
def draw_arm_skin(t: dict, ppc: float):
    """Arm senkrecht nach unten, Anker = Schulter (0, 0) in Arm-Koordinaten."""
    ar = t["arm"]
    c = ZCanvas((-ar["w"], -ar["len"] - 2, ar["w"], ar["w"]), ppc)
    L, w = ar["len"], ar["w"]
    pts = path((-w / 2, w * 0.3), ((-w / 2, w * 0.9), (w / 2, w * 0.9), (w / 2, w * 0.3)),
               ((w * 0.42, -L + 1),), ((-w * 0.42, -L + 1),))
    c.fill(pts, zone=1)
    c.fill([(0, w), (w, w), (w, -L), (w * 0.15, -L)], zone=1, shade=SHADE, clip=c.mask(pts))
    c.outline_under()
    return c.render_part((0, 0))


def draw_hand(t: dict, ppc: float, front: bool):
    """Handfläche (hinter dem Item) bzw. Fingerkappe (vor dem Item). Anker = Griffpunkt."""
    r = t["hand_r"]
    c = ZCanvas((-r * 2, -r * 2, r * 2, r * 2), ppc)
    if not front:
        c.ellipse(0, 0, r, r * 1.02, zone=1)
        c.ellipse(r * 0.25, -r * 0.3, r * 0.7, r * 0.65, zone=1, shade=0.93, clip=c.mask(blob(0, 0, r, r)))
        c.outline_under()
    else:
        # Faust von vorn: drei Fingerbögen vor dem Item (Item schaut oben und unten heraus)
        band = path((-r * 0.2, r * 0.55), ((r * 0.6, r * 0.62), (r * 1.1, r * 0.3), (r * 1.1, 0)),
                    ((r * 1.1, -r * 0.3), (r * 0.6, -r * 0.62), (-r * 0.2, -r * 0.55)),
                    ((-r * 0.5, -r * 0.1), (-r * 0.5, r * 0.1), (-r * 0.2, r * 0.55)))
        c.fill(band, zone=1)
        for k in (-1, 1):
            c.line([(r * 0.25, k * r * 0.18), (r * 0.95, k * r * 0.2)], w_cm=0.45, zone=1, shade=0.6)
        c.outline_under(0.7)
    return c.render_part((0, 0))


def _leg_pts(t: dict, sx: int, top: float, bottom: float, wmul: float = 1.0) -> list:
    hip, lg = t["hip"], t["leg"]
    x = sx * hip["x"]
    w = lg["w"] * wmul
    return path((x - w / 2, top), ((x - w / 2, bottom + 0.5),), ((x + w / 2, bottom + 0.5),), ((x + w / 2, top),))


def legs_box(t: dict) -> tuple:
    return (-t["hip"]["x"] - t["leg"]["w"] * 2, -3, t["hip"]["x"] + t["leg"]["w"] * 2, t["hip"]["y"] + 10)


def draw_legs_skin_into(c: ZCanvas, t: dict, from_y: float | None = None):
    """Nackte Beine in Zone 3 (= Haut) – liegen unter Hosen/Röcken."""
    top = t["hip"]["y"] + 2 if from_y is None else from_y
    for sx in (-1, 1):
        pts = _leg_pts(t, sx, top, t["shoe"]["h"] * 0.5, 0.86)
        c.fill(pts, zone=3)
        c.fill([(sx * t["hip"]["x"], top), (sx * 99, top), (sx * 99, 0), (sx * t["hip"]["x"], 0)],
               zone=3, shade=0.9, clip=c.mask(pts))
