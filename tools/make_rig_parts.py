#!/usr/bin/env python3
"""
Figuren-Teile für den CharacterRig (P03-T01) – Platzhalter in Stil-C-Nähe, 0 €, reproduzierbar.

- Liest data/characters/templates.json (Maße in cm), zeichnet jedes Teil 4× überabgetastet und
  verkleinert (weiche Kanten) auf 8 px/cm.
- Einfärbbare Teile sind HELL (weiß → leicht grau Verlauf) mit GRAUER Kontur: Godot färbt sie per
  modulate (Haut/Haare/Shirt/Hose/Schuhe) → Kontur wird automatisch eine dunklere Variante der Farbe
  (Stil C: farbige Kontur, nie schwarz). Gesichter sind fertig farbig (nicht eingefärbt).
- Ausgabe: assets/characters/parts/<schablone>/<teil>.png + parts.json (Teil → Größe/Anker in cm).

Aufruf: python3 tools/make_rig_parts.py [--out DIR]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SS = 4
OUTLINE = (112, 112, 118, 255)
EYE = (58, 38, 30, 255)
MOUTH = (150, 60, 60, 255)
CHEEK = (255, 130, 130, 90)
WHITE = (255, 255, 255, 255)


class Canvas:
    """Zeichenfläche in cm (y nach oben), intern px nach unten."""

    def __init__(self, w_cm: float, h_cm: float, ppc: float):
        self.w_cm, self.h_cm, self.ppc = w_cm, h_cm, ppc
        self.s = ppc * SS
        self.img = Image.new("RGBA", (max(1, round(w_cm * self.s)), max(1, round(h_cm * self.s))), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        self._grads: dict = {}

    def p(self, x: float, y: float) -> tuple[float, float]:
        """cm (x ab links, y ab unten) → px."""
        return x * self.s, (self.h_cm - y) * self.s

    def box(self, x0, y0, x1, y1):
        a, b = self.p(x0, y1), self.p(x1, y0)
        return [a[0], a[1], b[0], b[1]]

    def lw(self, cm: float) -> int:
        return max(1, round(cm * self.s))

    def _grad(self, grad) -> Image.Image:
        key = tuple(grad)
        if key not in self._grads:
            hi, lo = grad
            col = Image.linear_gradient("L").resize((1, self.img.size[1]))
            col = col.point(lambda v: round(hi + (lo - hi) * v / 255))
            self._grads[key] = col.resize(self.img.size)
        return self._grads[key]

    def shape(self, kind: str, box, radius_cm: float = 0.0, outline_cm: float = 0.55, grad=(255, 222)):
        """Gefüllte Form mit vertikalem Hell-Verlauf; Kontur = um outline_cm vergrößerte Form darunter."""
        o = outline_cm * self.s
        big = [box[0] - o, box[1] - o, box[2] + o, box[3] + o]
        if kind == "ellipse":
            self.d.ellipse(big, fill=OUTLINE)
        else:
            self.d.rounded_rectangle(big, radius=radius_cm * self.s + o, fill=OUTLINE)
        mask = Image.new("L", self.img.size, 0)
        md = ImageDraw.Draw(mask)
        if kind == "ellipse":
            md.ellipse(box, fill=255)
        else:
            md.rounded_rectangle(box, radius=radius_cm * self.s, fill=255)
        g = self._grad(grad)
        self.img.paste(Image.merge("RGBA", (g, g, g, Image.new("L", self.img.size, 255))), (0, 0), mask)

    def finish(self) -> Image.Image:
        return self.img.resize((max(1, round(self.w_cm * self.ppc)), max(1, round(self.h_cm * self.ppc))), Image.LANCZOS)


def face(c: Canvas, w: float, h: float, emotion: str):
    """Gesicht auf der Kopf-Fläche (w×h cm, Mitte = w/2,h/2)."""
    d, s = c.d, c.s
    cx, cy = w / 2, h * 0.47
    ex, er = w * 0.19, w * 0.085
    # Wangen
    for sx in (-1, 1):
        x, y = cx + sx * w * 0.27, cy - h * 0.12
        d.ellipse(c.box(x - w * 0.08, y - h * 0.045, x + w * 0.08, y + h * 0.045), fill=CHEEK)
    for sx in (-1, 1):
        x = cx + sx * ex
        if emotion in ("happy", "surprised", "love", "sad"):
            if emotion == "love":
                heart(c, x, cy, er * 1.25, (230, 70, 110, 255))
                continue
            r = er * (1.3 if emotion == "surprised" else 1.12)
            d.ellipse(c.box(x - r * 0.86, cy - r, x + r * 0.86, cy + r), fill=EYE)
            d.ellipse(c.box(x - r * 0.62, cy - r * 0.72, x + r * 0.62, cy + r * 0.5), fill=(110, 70, 45, 255))  # Iris
            d.ellipse(c.box(x - r * 0.1, cy + r * 0.12, x + r * 0.5, cy + r * 0.66), fill=WHITE)              # Glanz groß
            d.ellipse(c.box(x - r * 0.55, cy - r * 0.55, x - r * 0.25, cy - r * 0.25), fill=WHITE)            # Glanz klein
            d.line([c.p(x + sx * r * 0.7, cy + r * 0.72), c.p(x + sx * r * 1.15, cy + r * 1.05)], fill=EYE, width=c.lw(0.45))  # Wimper
            if emotion == "sad":
                d.line([c.p(x - er * 1.1, cy + er * 1.2 + sx * er * 0.35), c.p(x + er * 1.1, cy + er * 1.2 - sx * er * 0.35)],
                       fill=EYE, width=c.lw(0.5))
        elif emotion == "laugh":
            d.arc(c.box(x - er, cy - er * 0.9, x + er, cy + er * 0.9), 200, 340, fill=EYE, width=c.lw(0.6))
        elif emotion == "tired":
            d.arc(c.box(x - er, cy - er * 0.9, x + er, cy + er * 0.9), 20, 160, fill=EYE, width=c.lw(0.55))
        elif emotion.startswith("eat"):
            d.arc(c.box(x - er, cy - er * 0.9, x + er, cy + er * 0.9), 200, 340, fill=EYE, width=c.lw(0.6))
    d.arc(c.box(cx - w * 0.035, cy - h * 0.13, cx + w * 0.035, cy - h * 0.07), 20, 160, fill=(200, 120, 100, 255), width=c.lw(0.4))  # Nase
    my = cy - h * 0.24
    mw = w * 0.16
    if emotion in ("happy", "love"):
        d.arc(c.box(cx - mw, my - mw * 0.55, cx + mw, my + mw * 0.55), 20, 160, fill=MOUTH, width=c.lw(0.5))
    elif emotion in ("laugh", "eat_open"):
        d.chord(c.box(cx - mw, my - mw * 0.9, cx + mw, my + mw * 0.5), 0, 180, fill=MOUTH)
        d.chord(c.box(cx - mw * 0.55, my - mw * 0.85, cx + mw * 0.55, my - mw * 0.3), 0, 180, fill=(255, 140, 150, 255))
    elif emotion == "surprised":
        d.ellipse(c.box(cx - mw * 0.4, my - mw * 0.55, cx + mw * 0.4, my + mw * 0.3), fill=MOUTH)
    elif emotion == "sad":
        d.arc(c.box(cx - mw * 0.8, my - mw * 0.9, cx + mw * 0.8, my + mw * 0.2), 200, 340, fill=MOUTH, width=c.lw(0.5))
    elif emotion == "tired":
        d.line([c.p(cx - mw * 0.5, my), c.p(cx + mw * 0.5, my)], fill=MOUTH, width=c.lw(0.5))
    elif emotion == "eat_closed":
        d.ellipse(c.box(cx - mw * 0.7, my - mw * 0.3, cx + mw * 0.7, my + mw * 0.3), fill=(235, 150, 140, 255))
        d.arc(c.box(cx - mw * 0.7, my - mw * 0.3, cx + mw * 0.7, my + mw * 0.3), 0, 360, fill=MOUTH, width=c.lw(0.35))


def heart(c: Canvas, x: float, y: float, r: float, col):
    d = c.d
    d.ellipse(c.box(x - r, y - r * 0.1, x, y + r * 0.8), fill=col)
    d.ellipse(c.box(x, y - r * 0.1, x + r, y + r * 0.8), fill=col)
    d.polygon([c.p(x - r * 0.97, y + r * 0.25), c.p(x + r * 0.97, y + r * 0.25), c.p(x, y - r)], fill=col)


def build(tid: str, t: dict, ppc: float, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    parts: dict[str, dict] = {}

    def save(name: str, c: Canvas, anchor: tuple[float, float], note: str):
        c.finish().save(out / f"{name}.png", optimize=True)
        parts[name] = {"w_cm": c.w_cm, "h_cm": c.h_cm, "anchor_cm": [round(anchor[0], 3), round(anchor[1], 3)], "note": note}

    hd, to, sh, ar, hip, lg, so = t["head"], t["torso"], t["shoulder"], t["arm"], t["hip"], t["leg"], t["shoe"]
    hr = t["hand_r"]
    m = 0.8  # Rand für Kontur
    # Kopf (mit Ohren) – Anker = Mitte Kopf
    w, h = hd["w"] + 2 * m + hd["w"] * 0.16, hd["h"] + 2 * m
    c = Canvas(w, h, ppc)
    ex = hd["w"] * 0.08
    for sx in (-1, 1):
        x = w / 2 + sx * hd["w"] * 0.48
        c.shape("ellipse", c.box(x - ex * 1.3, h * 0.36, x + ex * 1.3, h * 0.56))
    c.shape("ellipse", c.box(m + ex, m, w - m - ex, h - m), grad=(255, 232))
    save("head", c, (w / 2, h / 2), "Haut · Anker = Kopfmitte")
    # Gesichter
    for emo in ["happy", "laugh", "surprised", "sad", "tired", "love", "eat_open", "eat_closed"]:
        c = Canvas(hd["w"], hd["h"], ppc)
        face(c, hd["w"], hd["h"], emo)
        save(f"face_{emo}", c, (hd["w"] / 2, hd["h"] / 2), "fertig farbig · Anker = Kopfmitte")
    # Haare
    top_gap = t["hair_top"] - (hd["cy"] + hd["h"] / 2)
    hw, hh = hd["w"] + 2 * m + 4, hd["h"] * 0.62 + top_gap + m
    for style in ["pigtails", "short"]:
        # vorne: Kappe bis zur Stirn, darunter runde Pony-Strähnen, seitlich spitz zulaufende Strähnen
        c = Canvas(hw, hh, ppc)
        brow = hh - top_gap - hd["h"] * 0.30          # Unterkante der Kappe (y in cm)
        cap = Canvas(hw, hh, ppc)
        cap.shape("ellipse", cap.box(m + 1, hh - hd["h"] * 0.95 - m, hw - m - 1, hh - m), grad=(255, 215))
        clip = Image.new("L", cap.img.size, 0)
        ImageDraw.Draw(clip).rectangle(cap.box(0, brow, hw, hh), fill=255)
        c.img.paste(cap.img, (0, 0), Image.composite(cap.img.getchannel("A"), clip, clip))
        n = 5 if style == "pigtails" else 4
        span = hd["w"] * 0.78
        for i in range(n):  # Pony: überlappende runde Strähnen
            x = hw / 2 - span / 2 + span * (i + 0.5) / n
            lh = hd["h"] * (0.16 if i % 2 == 0 else 0.12)
            c.shape("ellipse", c.box(x - span / n * 0.62, brow - lh, x + span / n * 0.62, brow + lh * 0.9),
                    outline_cm=0.45, grad=(250, 212))
        for sx in (-1, 1):  # Seitensträhnen, verjüngt (Ellipse, schmal)
            x = hw / 2 + sx * hd["w"] * 0.43
            c.shape("ellipse", c.box(x - hd["w"] * 0.075, hh - hd["h"] * (0.72 if style == "pigtails" else 0.6),
                                     x + hd["w"] * 0.075, brow + hd["h"] * 0.1), outline_cm=0.45, grad=(245, 205))
        save(f"hair_front_{style}", c, (hw / 2, hh), "Haare · Anker = oben Mitte (= hair_top)")
        # hinten
        bw = hd["w"] * (1.9 if style == "pigtails" else 1.12)
        bh = hd["h"] * (1.0 if style == "pigtails" else 0.9)
        c = Canvas(bw + 2 * m, bh + 2 * m, ppc)
        cx = (bw + 2 * m) / 2
        c.shape("ellipse", c.box(cx - hd["w"] * 0.54, bh * 0.2, cx + hd["w"] * 0.54, bh + m), grad=(235, 200))
        if style == "pigtails":
            for sx in (-1, 1):
                x = cx + sx * hd["w"] * 0.72
                c.shape("ellipse", c.box(x - hd["w"] * 0.2, m, x + hd["w"] * 0.2, bh * 0.52), grad=(245, 205))
        save(f"hair_back_{style}", c, (cx, bh + 2 * m), "Haare · Anker = oben Mitte (= hair_top)")
    # Oberkörper – Anker = Hüftmitte unten
    tw = max(to["w_top"], to["w_bot"]) + 2 * m
    th = to["top"] - to["bot"] + 2 * m
    c = Canvas(tw, th, ppc)
    c.shape("rounded", c.box(m + (tw - 2 * m - to["w_top"]) / 2, m, tw - m - (tw - 2 * m - to["w_top"]) / 2, th - m),
            radius_cm=to["w_top"] * 0.28)
    # Kragen
    c.shape("ellipse", c.box(tw / 2 - to["w_top"] * 0.18, th - m - to["w_top"] * 0.14, tw / 2 + to["w_top"] * 0.18, th - m + 0.4),
            grad=(245, 230))
    save("torso", c, (tw / 2, m), "Shirt · Anker = unten Mitte (Hüfthöhe torso.bot)")
    # Arm: Ärmel + Haut, senkrecht nach unten, Anker = Schulter (oben Mitte)
    aw, ah = ar["w"] + 2 * m, ar["len"] + 2 * m
    c = Canvas(aw, ah, ppc)
    c.shape("rounded", c.box(m + ar["w"] * 0.1, m, aw - m - ar["w"] * 0.1, ah - m - ar["sleeve"] * 0.6), radius_cm=ar["w"] * 0.45)
    save("arm_skin", c, (aw / 2, ah - m), "Haut · Anker = Schulter")
    c = Canvas(aw, ar["sleeve"] + 2 * m, ppc)
    c.shape("rounded", c.box(m, m, aw - m, ar["sleeve"] + m), radius_cm=ar["w"] * 0.45)
    save("arm_sleeve", c, (aw / 2, ar["sleeve"] + m), "Shirt · Anker = Schulter")
    # Hand (Handfläche, unter dem Item) und Finger (über dem Item)
    hs = hr * 2 + 2 * m
    c = Canvas(hs, hs, ppc)
    c.shape("ellipse", c.box(m, m, hs - m, hs - m), grad=(255, 230))
    save("hand", c, (hs / 2, hs / 2), "Haut · Anker = Griffpunkt (Handmitte)")
    c = Canvas(hs * 1.1, hs, ppc)
    # Fingerband wie eine echte Faust: 3 Finger über der MITTE der Hand (≈ 56 % der Höhe) –
    # das gehaltene Item schaut oben und unten heraus (Apfel, Karotte, Löffel bleiben sichtbar)
    x0, band_lo, band_hi = hs * 0.30, hs * 0.22, hs * 0.78
    for i in range(3):
        y0 = band_lo + i * (band_hi - band_lo) / 3
        y1 = y0 + (band_hi - band_lo) / 3
        c.shape("rounded", c.box(x0 - i * 0.25, y0 + 0.08, hs * 1.1 - m - i * 0.2, y1 - 0.08), radius_cm=(y1 - y0) * 0.5,
                outline_cm=0.35, grad=(255, 228))
    save("hand_front", c, (hs / 2, hs / 2), "Haut · Finger ÜBER dem Item · Anker = Griffpunkt")
    # Beine stehend – Anker = Boden Mitte
    lw_, lh = hip["x"] * 2 + lg["w"] + 2 * m, hip["y"] + 2 + m
    c = Canvas(lw_, lh, ppc)
    c.shape("rounded", c.box(m, lh - m - 8, lw_ - m, lh - m), radius_cm=4)
    for sx in (-1, 1):
        x = lw_ / 2 + sx * hip["x"]
        c.shape("rounded", c.box(x - lg["w"] / 2, so["h"] * 0.6, x + lg["w"] / 2, lh - m - 3), radius_cm=lg["w"] * 0.35)
    save("legs_stand", c, (lw_ / 2, 0), "Hose · Anker = Boden Mitte")
    # Schuhe stehend
    sw = hip["x"] * 2 + so["w"] + 2 * m + 2
    c = Canvas(sw, so["h"] + 2 * m, ppc)
    for sx in (-1, 1):
        x = sw / 2 + sx * hip["x"] + sx * 0.8
        c.shape("rounded", c.box(x - so["w"] / 2, m, x + so["w"] / 2, so["h"] + m), radius_cm=so["h"] * 0.5)
    save("shoes_stand", c, (sw / 2, m), "Schuhe · Anker = Boden Mitte")
    # Beine sitzend: Oberschenkel waagerecht → Knie auf Hüfthöhe, Unterschenkel hängt von dort herab.
    # Damit steht die Sohle genau „shin“ cm unter der Hüfte (Erwachsene 40 cm → Sitzhöhe 42 … 45 cm passt).
    sit_h = lg["shin"] + 2 * m + 2
    c = Canvas(lw_, sit_h, ppc)
    for sx in (-1, 1):                      # Unterschenkel ab der Hüfte (Anker) nach unten
        x = lw_ / 2 + sx * hip["x"]
        c.shape("rounded", c.box(x - lg["w"] * 0.45, m, x + lg["w"] * 0.45, sit_h - m), radius_cm=lg["w"] * 0.35)
    c.shape("rounded", c.box(m, sit_h - m - lg["sit_thigh"] * 0.85, lw_ - m, sit_h - m),   # Schoß (verkürzter Oberschenkel)
            radius_cm=lg["sit_thigh"] * 0.5)
    save("legs_sit", c, (lw_ / 2, sit_h - m), "Hose · Anker = Hüfte (Knie auf Sitzhöhe)")
    parts["_geometry"] = {"sit_drop_cm": round(lg["shin"] + 2.0, 2),   ## Hüfte → Sohle (sitzend)
                          "shoe_h_cm": so["h"], "sit_thigh_cm": lg["sit_thigh"]}
    return parts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "assets" / "characters" / "parts"))
    a = ap.parse_args(argv)
    data = json.loads((ROOT / "data" / "characters" / "templates.json").read_text(encoding="utf-8"))
    out = Path(a.out)
    index = {}
    for tid, t in data["templates"].items():
        index[tid] = build(tid, t, float(data["px_per_cm"]), out / tid)
    (out / "parts.json").write_text(json.dumps(index, indent=1, sort_keys=True), encoding="utf-8")
    n = sum(len([k for k in v if not k.startswith("_")]) for v in index.values())
    print(f"✅ {n} Figuren-Teile ({len(index)} Schablonen) → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
