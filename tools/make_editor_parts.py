#!/usr/bin/env python3
"""
ABGELÖST in P04b durch tools/make_chibi_parts.py (Figuren-Teile). Nur noch ZCanvas wird von
tools/make_pet_sprites.py benutzt – NICHT mehr für Figuren ausführen (würde die neuen Teile überschreiben).

Editor-Teile für den Charakter-Editor (P04-T01/T04/T10) – Platzhalter in Stil-C-Nähe, 0 €, reproduzierbar.

Farbzonen: Jedes Teil speichert seine **Farbgewichte** in R/G/B (Zone 1/2/3, mit eingebackenem
Hell-Dunkel-Verlauf) und die Deckung in A. Der Shader `zone_tint.gdshader` mischt daraus die drei
Palettenfarben:  Farbe = R·c1 + G·c2 + B·c3.  Ein Teil mit nur einer Zone nutzt nur R.

Ausgabe: assets/characters/parts/<schablone>/<teil>.png  (gleicher Ordner wie die Rig-Teile)
         assets/characters/parts/editor_parts.json        (Größe + Anker in cm, Zonen je Teil)
         data/character_parts/<slot>.json                 (Katalog: 5 Varianten je Slot)

Aufruf: python3 tools/make_editor_parts.py [--out DIR]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SS = 4                       # Überabtastung
PPC = 8.0                    # px pro cm
M = 2.3                      # Rand in cm

# ------------------------------------------------------------------ Zeichenfläche mit 3 Zonen
class ZCanvas:
    """cm-Koordinaten (y nach oben), 3 Graustufen-Ebenen (R/G/B) + Deckung."""

    def __init__(self, w_cm: float, h_cm: float, ppc: float = PPC):
        self.w_cm, self.h_cm, self.ppc = w_cm, h_cm, ppc
        self.s = ppc * SS
        self.size = (max(1, round(w_cm * self.s)), max(1, round(h_cm * self.s)))
        self.z = [Image.new("L", self.size, 0) for _ in range(3)]
        self.alpha = Image.new("L", self.size, 0)
        self.zone = 0

    def p(self, x: float, y: float) -> tuple[float, float]:
        return x * self.s, (self.h_cm - y) * self.s

    def box(self, x0, y0, x1, y1):
        a, b = self.p(x0, y1), self.p(x1, y0)
        return [a[0], a[1], b[0], b[1]]

    def lw(self, cm: float) -> int:
        return max(1, round(cm * self.s))

    def _mask(self, kind: str, box, radius_cm: float) -> Image.Image:
        m = Image.new("L", self.size, 0)
        d = ImageDraw.Draw(m)
        if kind == "ellipse":
            d.ellipse(box, fill=255)
        elif kind == "poly":
            d.polygon([self.p(*pt) for pt in box], fill=255)
        else:
            d.rounded_rectangle(box, radius=max(1.0, radius_cm * self.s), fill=255)
        return m

    def _grad(self, hi: int, lo: int) -> Image.Image:
        col = Image.linear_gradient("L").resize((1, self.size[1]))
        col = col.point(lambda v: round(hi + (lo - hi) * v / 255))
        return col.resize(self.size)

    def shape(self, kind: str, box, radius_cm: float = 0.0, outline_cm: float = 0.0,
              fill=(255, 205), outline: int = 150, zone: int = -1):
        """Form in die Zone zeichnen: erst Kontur (dunkler), dann Fläche (Verlauf)."""
        zi = self.zone if zone < 0 else zone
        big = box
        if outline_cm > 0.0:
            o = outline_cm * self.s
            if kind == "poly":                     # Polygon um seinen Schwerpunkt weiten
                cx = sum(p[0] for p in box) / len(box)
                cy = sum(p[1] for p in box) / len(box)
                big = [(cx + (p[0] - cx) * 1.14 + (1 if p[0] >= cx else -1) * 0.35 * o,
                        cy + (p[1] - cy) * 1.14 + (1 if p[1] >= cy else -1) * 0.35 * o) for p in box]
            else:
                big = [box[0] - o, box[1] - o, box[2] + o, box[3] + o]
            self._put(self._mask(kind, big, radius_cm), Image.new("L", self.size, outline), zi)
        m = self._mask(kind, box, radius_cm)
        self._put(m, self._grad(fill[0], fill[1]), zi)
        self.alpha = ImageChops.lighter(self.alpha,
                                        m if outline_cm <= 0 else self._mask(kind, big, radius_cm))

    def _put(self, mask: Image.Image, value: Image.Image, zi: int) -> None:
        layer = ImageChops.multiply(mask, value)
        self.z[zi] = ImageChops.lighter(self.z[zi], layer)

    def line(self, a, b, cm: float, value: int = 90, zone: int = -1) -> None:
        zi = self.zone if zone < 0 else zone
        m = Image.new("L", self.size, 0)
        ImageDraw.Draw(m).line([self.p(*a), self.p(*b)], fill=255, width=max(1, round(cm * self.s)))
        self._put(m, Image.new("L", self.size, value), zi)
        self.alpha = ImageChops.lighter(self.alpha, m)

    def finish(self) -> Image.Image:
        r, g, b = self.z
        a = ImageChops.lighter(ImageChops.lighter(r, g), b)
        return Image.merge("RGBA", (r, g, b, ImageChops.lighter(a, self.alpha))).resize(
            (max(1, round(self.w_cm * self.ppc)), max(1, round(self.h_cm * self.ppc))), Image.LANCZOS)


# ------------------------------------------------------------------ Varianten je Slot
TOPS = ["shirt", "tee", "sweater", "dress", "overalls"]          # + passender Ärmel
BOTTOMS = ["trousers", "shorts", "skirt", "leggings", "dungarees"]
SHOES = ["sneaker", "boot", "sandal", "slipper", "rainboot"]
HAIRS = ["short", "pigtails", "curly", "bob", "bald"]
EYES = ["round", "big", "sleepy", "wink", "star"]
MOUTHS = ["smile", "grin", "oh", "tongue", "neutral"]
ACCESSORIES = ["none", "glasses", "bow", "headphones", "cap"]
AIDS = ["none", "hearing_aid", "eye_patch", "arm_sling", "knee_bandage"]
EMOTIONS = ["happy", "laugh", "surprised", "sad", "tired", "love"]


def build(tid: str, t: dict, out: Path) -> dict:
    """Erzeugt alle Editor-Teile einer Schablone. Rückgabe: {teilname: {w_cm,h_cm,anchor_cm,zones}}."""
    (out).mkdir(parents=True, exist_ok=True)
    parts: dict[str, dict] = {}
    head, torso, hip = t["head"], t["torso"], t["hip"]
    leg, shoe, arm = t["leg"], t["shoe"], t["arm"]
    top_y, bot_y = torso["top"], torso["bot"]
    tw = max(torso["w_top"], torso["w_bot"])

    def save(name: str, c: ZCanvas, anchor: tuple[float, float], zones: int, note: str) -> None:
        c.finish().save(out / f"{name}.png", optimize=True)
        parts[name] = {"w_cm": round(c.w_cm, 3), "h_cm": round(c.h_cm, 3),
                       "anchor_cm": [round(anchor[0], 3), round(anchor[1], 3)],
                       "zones": zones, "note": note}

    # ---------------- Oberteil (Torso) + Ärmel
    for v in TOPS:
        th = top_y - bot_y + 2 * M
        c = ZCanvas(tw + 2 * M, th, PPC)
        if v == "dress":                      # Kleid: länger, Zone 2 = Saum
            c.shape("rounded", c.box(M, M, c.w_cm - M, th - M - 4), radius_cm=tw * 0.18,
                    outline_cm=0.55, fill=(255, 200), zone=0)
            c.shape("rounded", c.box(M, M, c.w_cm - M, M + 5), radius_cm=2, fill=(255, 215), zone=1)
        elif v == "overalls":                 # Latz: Zone 1 Stoff, Zone 2 Latz + Träger
            c.shape("rounded", c.box(M, M, c.w_cm - M, th - M - 2), radius_cm=tw * 0.16,
                    outline_cm=0.55, fill=(255, 205), zone=0)
            c.shape("rounded", c.box(c.w_cm * 0.28, th - M - 16, c.w_cm * 0.72, th - M - 2),
                    radius_cm=2, fill=(255, 210), zone=1)
        elif v == "sweater":                  # Pullover: Zone 2 = Bündchen
            c.shape("rounded", c.box(M, M, c.w_cm - M, th - M - 3), radius_cm=tw * 0.22,
                    outline_cm=0.55, fill=(255, 195), zone=0)
            c.shape("rounded", c.box(M, M, c.w_cm - M, M + 3), radius_cm=2, fill=(255, 215), zone=1)
        elif v == "tee":                      # T-Shirt mit Streifen in Zone 2
            c.shape("rounded", c.box(M, M, c.w_cm - M, th - M - 2), radius_cm=tw * 0.16,
                    outline_cm=0.55, fill=(255, 202), zone=0)
            for i in range(3):
                y0 = M + 8 + i * (th - 2 * M - 12) / 3
                c.shape("rounded", c.box(M + 1, y0, c.w_cm - M - 1, y0 + 2.4), radius_cm=1,
                        fill=(255, 225), zone=1)
        else:                                 # Hemd: Zone 2 = Kragen, Zone 3 = Knöpfe
            c.shape("rounded", c.box(M, M, c.w_cm - M, th - M - 2), radius_cm=tw * 0.14,
                    outline_cm=0.55, fill=(255, 205), zone=0)
            c.shape("ellipse", c.box(c.w_cm / 2 - tw * 0.18, th - M - tw * 0.14,
                                     c.w_cm / 2 + tw * 0.18, th - M + 0.4), fill=(255, 230), zone=1)
            for i in range(3):
                y0 = th - M - 8 - i * 7
                c.shape("ellipse", c.box(c.w_cm / 2 - 1, y0, c.w_cm / 2 + 1, y0 + 2), fill=(255, 240), zone=2)
        save(f"top_{v}", c, (c.w_cm / 2, M), 3 if v == "shirt" else 2, f"Oberteil {v}")

        aw, ah = arm["w"] + 2 * M, arm["sleeve"] + 2 * M
        c = ZCanvas(aw, ah, PPC)
        c.shape("rounded", c.box(M, M, aw - M, ah - M), radius_cm=arm["w"] * 0.45,
                outline_cm=0.5, fill=(255, 205))
        save(f"sleeve_{v}", c, (aw / 2, ah - M), 1, f"Ärmel {v} (Anker = Schulter)")

    # ---------------- Unterteil (Beine stehend + sitzend)
    for v in BOTTOMS:
        lw_, lh = hip["x"] * 2 + leg["w"] + 2 * M, hip["y"] + 2 + M
        c = ZCanvas(lw_, lh, PPC)
        if v == "shorts":
            for sx in (-1, 1):
                x = lw_ / 2 + sx * hip["x"]
                c.shape("rounded", c.box(x - leg["w"] * 0.6, lh - M - 16, x + leg["w"] * 0.6, lh - M - 3),
                        radius_cm=leg["w"] * 0.35, outline_cm=0.5, fill=(255, 205))
            c.shape("rounded", c.box(M, lh - M - 11, lw_ - M, lh - M - 3), radius_cm=3,
                    outline_cm=0.5, fill=(255, 205))
        elif v == "skirt":
            c.shape("poly", [c.p(M, lh - M - 3), c.p(lw_ - M, lh - M - 3),
                             c.p(lw_ - M - 3, lh - M - 20), c.p(M + 3, lh - M - 20)],
                    outline_cm=0.5, fill=(255, 200))
            for sx in (-1, 1):
                x = lw_ / 2 + sx * hip["x"]
                c.shape("rounded", c.box(x - leg["w"] * 0.4, M, x + leg["w"] * 0.4, lh - M - 18),
                        radius_cm=leg["w"] * 0.3, outline_cm=0.45, fill=(250, 200))
        elif v == "leggings":
            c.shape("rounded", c.box(M, lh - M - 8, lw_ - M, lh - M), radius_cm=4,
                    outline_cm=0.5, fill=(255, 205))
            for sx in (-1, 1):
                x = lw_ / 2 + sx * hip["x"]
                c.shape("rounded", c.box(x - leg["w"] / 2, so_h(shoe), x + leg["w"] / 2, lh - M - 3),
                        radius_cm=leg["w"] * 0.35, outline_cm=0.45, fill=(255, 200))
        elif v == "dungarees":
            c.shape("rounded", c.box(M, lh - M - 8, lw_ - M, lh - M), radius_cm=4,
                    outline_cm=0.5, fill=(255, 200))
            for sx in (-1, 1):
                x = lw_ / 2 + sx * hip["x"]
                c.shape("rounded", c.box(x - leg["w"] / 2, so_h(shoe), x + leg["w"] / 2, lh - M - 3),
                        radius_cm=leg["w"] * 0.35, outline_cm=0.45, fill=(255, 195))
                c.shape("rounded", c.box(x - leg["w"] * 0.55, lh - M - 14, x + leg["w"] * 0.55, lh - M - 11),
                        radius_cm=1, fill=(255, 230), zone=1)
        else:                                  # trousers
            c.shape("rounded", c.box(M, lh - M - 8, lw_ - M, lh - M), radius_cm=4,
                    outline_cm=0.5, fill=(255, 205))
            for sx in (-1, 1):
                x = lw_ / 2 + sx * hip["x"]
                c.shape("rounded", c.box(x - leg["w"] / 2, so_h(shoe), x + leg["w"] / 2, lh - M - 3),
                        radius_cm=leg["w"] * 0.35, outline_cm=0.45, fill=(255, 200))
        save(f"bottom_{v}", c, (lw_ / 2, 0), 2 if v == "dungarees" else 1, f"Unterteil {v}")

        sit_h = leg["shin"] + 2 * M + 2
        c = ZCanvas(lw_, sit_h, PPC)
        for sx in (-1, 1):
            x = lw_ / 2 + sx * hip["x"]
            h0 = sit_h - M - (16 if v == "shorts" else leg["shin"])
            c.shape("rounded", c.box(x - leg["w"] * (0.6 if v == "shorts" else 0.45), maxf(M, h0),
                                     x + leg["w"] * (0.6 if v == "shorts" else 0.45), sit_h - M),
                    radius_cm=leg["w"] * 0.35, outline_cm=0.45, fill=(255, 202))
        c.shape("rounded", c.box(M, sit_h - M - leg["sit_thigh"] * 0.85, lw_ - M, sit_h - M),
                radius_cm=leg["sit_thigh"] * 0.5, outline_cm=0.5, fill=(255, 205))
        save(f"bottom_sit_{v}", c, (lw_ / 2, sit_h - M), 1, f"Unterteil {v} sitzend (Anker = Hüfte)")

    # ---------------- Schuhe
    for v in SHOES:
        sw = hip["x"] * 2 + shoe["w"] + 2 * M + 2
        BOT = 0.2                              ## Sohle sitzt auf der Unterkante (kein Rand unten!)
        hh = shoe["h"] * (1.9 if v == "boot" else 1.0)
        c = ZCanvas(sw, hh + BOT + M, PPC)
        for sx in (-1, 1):
            x = sw / 2 + sx * hip["x"] + sx * 0.8
            if v == "sandal":
                c.shape("rounded", c.box(x - shoe["w"] / 2, BOT, x + shoe["w"] / 2, BOT + shoe["h"] * 0.45),
                        radius_cm=shoe["h"] * 0.3, outline_cm=0.4, fill=(255, 210))
                c.shape("rounded", c.box(x - shoe["w"] * 0.42, BOT + shoe["h"] * 0.35,
                                         x + shoe["w"] * 0.42, BOT + shoe["h"] * 0.62),
                        radius_cm=1.2, fill=(255, 225), zone=1)
            else:
                c.shape("rounded", c.box(x - shoe["w"] / 2, BOT, x + shoe["w"] / 2, BOT + hh),
                        radius_cm=shoe["h"] * 0.5, outline_cm=0.45, fill=(255, 205))
                c.shape("rounded", c.box(x - shoe["w"] / 2, BOT, x + shoe["w"] / 2, BOT + shoe["h"] * 0.4),
                        radius_cm=shoe["h"] * 0.35, fill=(255, 235), zone=1)   # Sohle
                if v in ("sneaker", "slipper"):
                    c.shape("rounded", c.box(x - shoe["w"] * 0.34, BOT + shoe["h"] * 0.55,
                                             x + shoe["w"] * 0.34, BOT + shoe["h"] * 0.95),
                            radius_cm=1, fill=(255, 240), zone=1)               # Klett/Streifen
        save(f"shoes_{v}", c, (sw / 2, BOT), 2, f"Schuhe {v}")

    # ---------------- Frisuren (vorne + hinten)
    for v in HAIRS:
        hw = head["w"] * (2.1 if v == "pigtails" else 1.7 if v == "curly" else 1.35)
        hh = head["h"] * (0.95 if v in ("pigtails", "curly") else 0.8)
        c = ZCanvas(hw, hh, PPC)
        if v == "bald":
            pass                                # leeres Bild = kahl (kein Teil gezeichnet)
        elif v == "pigtails":
            c.shape("ellipse", c.box(M, hh - M - head["h"] * 0.7, hw - M, hh - M), outline_cm=0.5,
                    fill=(255, 205))
            for sx in (-1, 1):
                x = hw / 2 + sx * head["w"] * 0.72
                c.shape("ellipse", c.box(x - head["w"] * 0.22, M, x + head["w"] * 0.22, hh - M - head["h"] * 0.5),
                        outline_cm=0.5, fill=(255, 200))
        elif v == "curly":
            for i in range(7):
                a = -0.9 + i * 0.3
                x = hw / 2 + math.cos(a) * head["w"] * 0.62
                y = hh - M - head["h"] * 0.42 + math.sin(a) * head["h"] * 0.34
                c.shape("ellipse", c.box(x - head["w"] * 0.2, y - head["h"] * 0.2,
                                         x + head["w"] * 0.2, y + head["h"] * 0.2),
                        outline_cm=0.45, fill=(255, 200))
        elif v == "bob":
            c.shape("rounded", c.box(M + head["w"] * 0.12, M, hw - M - head["w"] * 0.12, hh - M - head["h"] * 0.35),
                    radius_cm=head["h"] * 0.3, outline_cm=0.5, fill=(255, 200))
            c.shape("rounded", c.box(M, hh - M - head["h"] * 0.75, hw - M, hh - M),
                    radius_cm=head["h"] * 0.3, outline_cm=0.5, fill=(255, 205))
        else:                                   # short
            c.shape("rounded", c.box(M, hh - M - head["h"] * 0.72, hw - M, hh - M),
                    radius_cm=head["h"] * 0.32, outline_cm=0.5, fill=(255, 205))
        save(f"hair_back_{v}", c, (hw / 2, hh - M), 1, f"Haar hinten {v}")

        c = ZCanvas(hw, hh, PPC)
        if v == "bald":
            pass
        elif v == "pigtails":
            c.shape("rounded", c.box(hw / 2 - head["w"] * 0.5, hh - M - head["h"] * 0.34,
                                     hw / 2 + head["w"] * 0.5, hh - M), radius_cm=head["h"] * 0.16,
                    outline_cm=0.5, fill=(255, 205))
        elif v == "curly":
            for i in range(5):
                x = hw / 2 + (-1 + i * 0.5) * head["w"] * 0.52
                y = hh - M - head["h"] * 0.06
                c.shape("ellipse", c.box(x - head["w"] * 0.19, y - head["h"] * 0.17,
                                         x + head["w"] * 0.19, y + head["h"] * 0.17),
                        outline_cm=0.45, fill=(255, 200))
        elif v == "bob":
            c.shape("rounded", c.box(hw / 2 - head["w"] * 0.58, hh - M - head["h"] * 0.55,
                                     hw / 2 + head["w"] * 0.58, hh - M), radius_cm=head["h"] * 0.26,
                    outline_cm=0.5, fill=(255, 210))
        else:
            c.shape("rounded", c.box(hw / 2 - head["w"] * 0.46, hh - M - head["h"] * 0.3,
                                     hw / 2 + head["w"] * 0.46, hh - M), radius_cm=head["h"] * 0.18,
                    outline_cm=0.5, fill=(255, 215))
        save(f"hair_front_{v}", c, (hw / 2, hh - M), 1, f"Haar vorne {v}")

    # ---------------- Augen, Mund, Accessoire, Hilfsmittel:
    # kopfgroße Fläche, Anker = Kopfmitte → der Rig hängt sie genau wie die alte Gesichts-Ebene ein.
    hw_, hh_ = head["w"], head["h"]
    ey, my0 = hh_ * 0.47, hh_ * 0.23
    er, mw = hw_ * 0.085, hw_ * 0.16
    for v in EYES + EMOTIONS:
        c = ZCanvas(hw_, hh_, PPC)
        v = {"happy": "round", "laugh": "laugh", "surprised": "big", "sad": "sad",
             "tired": "sleepy", "love": "love"}.get(v, v)
        for sx in (-1, 1):
            x = hw_ / 2 + sx * hw_ * 0.19
            r = er * (1.35 if v == "big" else 1.0)
            if v == "sleepy":
                c.shape("ellipse", c.box(x - r * 1.1, ey - r * 0.35, x + r * 1.1, ey + r * 0.35),
                        fill=(70, 45), zone=0)
                c.line((x - r, ey + r * 0.5), (x + r, ey + r * 0.5), 0.35, 60)
            elif v == "wink" and sx < 0:
                c.line((x - r, ey), (x + r, ey), 0.5, 60)
                c.line((x - r * 0.6, ey - r * 0.45), (x + r * 0.6, ey - r * 0.45), 0.3, 60)
            elif v == "star":
                star(c, x, ey, r * 1.25, 80)
            elif v == "laugh":                      # zugekniffene Augenbögen
                c.line((x - r, ey + r * 0.3), (x + r, ey + r * 0.3), 0.5, 70)
                for k in (-1, 0, 1):
                    c.line((x + k * r * 0.6, ey + r * 0.75), (x + k * r * 0.6 - r * 0.25, ey + r * 0.25), 0.25, 70)
            elif v == "sad":                        # nach unten gezogene Augen
                c.shape("ellipse", c.box(x - r * 0.86, ey - r * 0.85, x + r * 0.86, ey + r * 0.95),
                        fill=(70, 45), zone=0)
                c.shape("rounded", c.box(x - r * 1.1, ey + r * 0.75, x + r * 1.1, ey + r * 1.05),
                        radius_cm=0.3, fill=(90, 60), zone=0)
            elif v == "love":                       # Herzen
                heart_eye(c, x, ey, r * 1.3)
            else:
                c.shape("ellipse", c.box(x - r * 0.86, ey - r, x + r * 0.86, ey + r), fill=(70, 45), zone=0)
                c.shape("ellipse", c.box(x - r * 0.3, ey + r * 0.1, x + r * 0.2, ey + r * 0.6),
                        fill=(255, 255), zone=1)                       # Glanz (Zone 2)
        save(f"eyes_{v}", c, (hw_ / 2, hh_ / 2), 2, f"Augen {v}")

    for v in MOUTHS + EMOTIONS + ["eat_closed", "eat_open"]:
        c = ZCanvas(hw_, hh_, PPC)
        cx = hw_ / 2
        if v in ("smile", "happy", "love", "tongue"):
            c.shape("poly", arc_poly(cx, my0, mw, 200, 340, 16), fill=(190, 120), zone=0)
        elif v in ("grin", "laugh", "eat_open"):
            c.shape("ellipse", c.box(cx - mw, my0 - mw * 0.5, cx + mw, my0 + mw * 0.8),
                    fill=(180, 110), zone=0)
            c.shape("ellipse", c.box(cx - mw * 0.6, my0 - mw * 0.5, cx + mw * 0.6, my0 + mw * 0.1),
                    fill=(255, 190), zone=1)                           # Zunge/Gaumen
        elif v in ("oh", "surprised"):
            c.shape("ellipse", c.box(cx - mw * 0.5, my0 - mw * 0.5, cx + mw * 0.5, my0 + mw * 0.5),
                    fill=(190, 120), zone=0)
        elif v == "sad":
            c.shape("poly", arc_poly(cx, my0 + mw * 0.3, mw * 0.8, 20, 160, 16), fill=(190, 120), zone=0)
        elif v == "tired":
            c.shape("rounded", c.box(cx - mw * 0.7, my0 - mw * 0.1, cx + mw * 0.7, my0 + mw * 0.1),
                    radius_cm=0.4, fill=(190, 120), zone=0)
        elif v == "eat_closed":
            c.shape("ellipse", c.box(cx - mw * 0.8, my0 - mw * 0.3, cx + mw * 0.8, my0 + mw * 0.3),
                    fill=(200, 140), zone=0)
        else:                                   # neutral
            c.shape("rounded", c.box(cx - mw * 0.8, my0 - mw * 0.08, cx + mw * 0.8, my0 + mw * 0.08),
                    radius_cm=0.3, fill=(190, 120), zone=0)
        if v == "tongue":
            c.shape("ellipse", c.box(cx - mw * 0.35, my0 - mw * 0.75, cx + mw * 0.35, my0 - mw * 0.1),
                    fill=(255, 190), zone=1)
        save(f"mouth_{v}", c, (hw_ / 2, hh_ / 2), 2, f"Mund {v}")

    for v in ACCESSORIES:
        c = ZCanvas(hw_, hh_, PPC)
        if v == "glasses":
            for sx in (-1, 1):
                x = hw_ / 2 + sx * hw_ * 0.19
                c.shape("ellipse", c.box(x - hw_ * 0.16, ey - hw_ * 0.13, x + hw_ * 0.16, ey + hw_ * 0.13),
                        outline_cm=0.35, fill=(255, 225), zone=0)
            c.shape("rounded", c.box(hw_ / 2 - hw_ * 0.05, ey - hw_ * 0.02, hw_ / 2 + hw_ * 0.05, ey + hw_ * 0.02),
                    radius_cm=0.3, fill=(255, 235), zone=0)
        elif v == "bow":
            bx = hw_ / 2 - hw_ * 0.36
            by = hh_ * 0.86
            for sx in (-1, 1):
                c.shape("poly", [c.p(bx, by), c.p(bx - sx * hw_ * 0.17, by + hh_ * 0.09),
                                 c.p(bx - sx * hw_ * 0.17, by - hh_ * 0.09)], fill=(255, 200), zone=0)
            c.shape("ellipse", c.box(bx - hw_ * 0.05, by - hh_ * 0.05, bx + hw_ * 0.05, by + hh_ * 0.05),
                    fill=(255, 220), zone=1)
        elif v == "headphones":
            c.shape("poly", arc_poly(hw_ / 2, hh_ * 0.55, hw_ * 0.52, 20, 160, 18), fill=(255, 200), zone=0)
            for sx in (-1, 1):
                x = hw_ / 2 + sx * hw_ * 0.5
                c.shape("rounded", c.box(x - hw_ * 0.1, ey - hh_ * 0.13, x + hw_ * 0.1, ey + hh_ * 0.11),
                        radius_cm=hh_ * 0.06, outline_cm=0.35, fill=(255, 215), zone=1)
        elif v == "cap":
            c.shape("poly", arc_poly(hw_ / 2, hh_ * 0.62, hw_ * 0.58, 0, 180, 20), fill=(255, 205), zone=0)
            c.shape("rounded", c.box(hw_ / 2 - hw_ * 0.6, hh_ * 0.58, hw_ / 2 + hw_ * 0.1, hh_ * 0.66),
                    radius_cm=hh_ * 0.03, fill=(255, 225), zone=1)
        save(f"acc_{v}", c, (hw_ / 2, hh_ / 2), 2, f"Accessoire {v}")

    for v in AIDS:
        c = ZCanvas(hw_, hh_, PPC)
        if v == "hearing_aid":
            for sx in (-1, 1):
                x = hw_ / 2 + sx * hw_ * 0.42
                c.shape("poly", arc_poly(x, ey, hw_ * 0.1, 250, 430, 14), fill=(255, 200), zone=0)
        elif v == "eye_patch":
            c.shape("ellipse", c.box(hw_ / 2 - hw_ * 0.36, ey - hh_ * 0.11, hw_ / 2 + hw_ * 0.02, ey + hh_ * 0.09),
                    outline_cm=0.3, fill=(255, 195), zone=0)
            c.line((hw_ / 2 - hw_ * 0.5, ey + hh_ * 0.05), (hw_ / 2 + hw_ * 0.18, ey - hh_ * 0.07), 0.3, 120)
        elif v == "arm_sling":
            c.shape("poly", [c.p(hw_ / 2 - hw_ * 0.3, hh_ * 0.2), c.p(hw_ / 2 + hw_ * 0.3, hh_ * 0.2),
                             c.p(hw_ / 2, hh_ * 0.42)], fill=(255, 215), zone=0)
        elif v == "knee_bandage":
            c.shape("rounded", c.box(hw_ / 2 - hw_ * 0.22, hh_ * 0.1, hw_ / 2 + hw_ * 0.22, hh_ * 0.26),
                    radius_cm=hh_ * 0.04, fill=(255, 225), zone=0)
        save(f"aid_{v}", c, (hw_ / 2, hh_ / 2), 1, f"Hilfsmittel {v}")

    return parts


# ------------------------------------------------------------------ kleine Helfer
import math

def maxf(a: float, b: float) -> float:
    return a if a > b else b


def so_h(shoe: dict) -> float:
    return shoe["h"] * 0.6


def arc_poly(cx: float, cy: float, r: float, a0: float, a1: float, steps: int) -> list:
    pts = []
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    for i in range(steps, -1, -1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62))
    return pts


def heart_eye(c: ZCanvas, x: float, y: float, r: float) -> None:
    c.shape("ellipse", c.box(x - r * 0.62, y - r * 0.05, x, y + r * 0.55), fill=(210, 60), zone=1)
    c.shape("ellipse", c.box(x, y - r * 0.05, x + r * 0.62, y + r * 0.55), fill=(210, 60), zone=1)
    c.shape("poly", [c.p(x - r * 0.62, y + r * 0.2), c.p(x + r * 0.62, y + r * 0.2), c.p(x, y - r * 0.62)],
            fill=(210, 60), zone=1)


def star(c: ZCanvas, x: float, y: float, r: float, value: int) -> None:
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r * (1.0 if i % 2 == 0 else 0.45)
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))     # cm, ZCanvas rechnet um
    c.shape("poly", pts, fill=(value, int(value * 0.7)), zone=0)


# ------------------------------------------------------------------ Katalog (data/character_parts)
CATALOG = [
    ("top", TOPS, "Oberteil", "top_{v}", "sleeve_{v}", 3),
    ("bottom", BOTTOMS, "Hose/Rock", "bottom_{v}", "bottom_sit_{v}", 2),
    ("shoes", SHOES, "Schuhe", "shoes_{v}", "", 2),
    ("hair", HAIRS, "Frisur", "hair_front_{v}", "hair_back_{v}", 1),
    ("eyes", EYES, "Augen", "eyes_{v}", "", 2),
    ("mouth", MOUTHS, "Mund", "mouth_{v}", "", 2),
    ("accessory", ACCESSORIES, "Accessoire", "acc_{v}", "", 2),
    ("aid", AIDS, "Hilfsmittel", "aid_{v}", "", 1),
]

SLOT_ICON = {"top": "👕", "bottom": "👖", "shoes": "👟", "hair": "💇", "eyes": "👀",
             "mouth": "👄", "accessory": "🎀", "aid": "🦻"}


def write_catalog(cat_dir: Path) -> None:
    cat_dir.mkdir(parents=True, exist_ok=True)
    for slot, variants, label, front, back, zones in CATALOG:
        doc = {
            "slot": slot,
            "label": label,
            "icon": SLOT_ICON[slot],
            "max_zones": zones,
            "variants": [
                {
                    "id": v,
                    "label": v.replace("_", " "),
                    "part": front.format(v=v),
                    "part_back": back.format(v=v) if back else None,
                    "zones": 1 if v in ("none", "bald") else (3 if slot == "top" and v == "shirt" else (2 if zones > 1 else 1)),
                    "tags": (["none"] if v == "none" else []) + ([slot] if v != "none" else []),
                }
                for v in variants
            ],
        }
        (cat_dir / f"{slot}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "assets" / "characters" / "parts"))
    ap.add_argument("--catalog", default=str(ROOT / "data" / "character_parts"))
    a = ap.parse_args()
    out = Path(a.out)
    data = json.loads((ROOT / "data" / "characters" / "templates.json").read_text(encoding="utf-8"))
    index: dict = {}
    n = 0
    for tid, t in data["templates"].items():
        index[tid] = build(tid, t, out / tid)
        n += len(index[tid])
    (out / "editor_parts.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    write_catalog(Path(a.catalog))
    print(f"✅ {n} Editor-Teile ({len(data['templates'])} Schablonen) + Katalog → {out}")


if __name__ == "__main__":
    main()
