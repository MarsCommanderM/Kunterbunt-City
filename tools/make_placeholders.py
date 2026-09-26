#!/usr/bin/env python3
"""
Platzhalter-Sprites für JEDEN Eintrag in data/scale_table.json (Phase 02, P02-T01).

- 8 px pro cm (Referenz-Auflösung), längste Seite max. 2048 px (sehr große Dinge
  wie Bus/Giraffe bekommen dann weniger px/cm – die Welt-Größe bleibt exakt, weil
  ItemNode immer über die cm-Höhe skaliert).
- Randlos zugeschnitten (kein Padding): Bildhöhe = Objekthöhe.
- Kategorie-Farbe mit weichem Verlauf, dunklere farbige Kontur (Stil-C-nah, nicht schwarz),
  Beschriftung „Name + cm“, runde Form für runde Dinge (Bälle, Obst …).
- Schreibt assets/placeholders/<id>.png und assets/placeholders/index.json.

Aufruf:  python3 tools/make_placeholders.py [--only id1,id2] [--out DIR]
Reproduzierbar: gleiche Tabelle → identische Bilder (keine Zufallswerte).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PX_PER_CM = 8.0
MAX_SIDE = 2048
MIN_SIDE = 6

CATEGORY_COLORS = {
    "character": (250, 184, 160), "pet": (214, 170, 120), "zoo_animal": (190, 170, 120),
    "fixture": (200, 205, 215), "furniture": (214, 172, 128), "food": (240, 128, 110),
    "kitchen": (150, 200, 220), "toy": (130, 190, 240), "item": (180, 160, 230),
    "school": (120, 200, 170), "health": (240, 150, 170), "pool": (110, 200, 235),
    "shop": (250, 200, 110), "sport": (160, 210, 120), "fair": (250, 150, 210),
    "garage": (170, 170, 185),
}
ROUND_IDS = ("ball", "apple", "tomato", "orange", "watermelon", "balloon", "globe", "egg", "puck", "cupcake")


def is_round(entry: dict) -> bool:
    w, h = entry.get("w_cm", entry["h_cm"]), entry["h_cm"]
    near_square = abs(w - h) / max(w, h) < 0.25
    return near_square and any(k in entry["id"] for k in ROUND_IDS)


def size_px(entry: dict) -> tuple[int, int, float]:
    w_cm, h_cm = float(entry.get("w_cm") or entry["h_cm"]), float(entry["h_cm"])
    ppc = PX_PER_CM
    if max(w_cm, h_cm) * ppc > MAX_SIDE:
        ppc = MAX_SIDE / max(w_cm, h_cm)
    return max(MIN_SIDE, round(w_cm * ppc)), max(MIN_SIDE, round(h_cm * ppc)), ppc


def font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=size)
    except TypeError:                      # sehr alte Pillow-Versionen
        return ImageFont.load_default()


def short_name(entry_id: str) -> str:
    parts = entry_id.split("_")
    return " ".join(parts[1:] if len(parts) > 1 else parts)


def render(entry: dict) -> tuple[Image.Image, float]:
    w, h, ppc = size_px(entry)
    base = CATEGORY_COLORS.get(entry.get("category", ""), (200, 200, 200))
    ss = 4 if max(w, h) <= 1024 else 2          # Supersampling für glatte Kanten
    W, H = w * ss, h * ss
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # vertikaler Verlauf: oben heller, unten dunkler
    grad = Image.new("RGBA", (1, H))
    for y in range(H):
        t = y / max(1, H - 1)
        k = 1.12 - 0.24 * t
        grad.putpixel((0, y), tuple(min(255, int(c * k)) for c in base) + (255,))
    grad = grad.resize((W, H))
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    outline_w = max(ss, min(round(min(W, H) * 0.035), 10 * ss))   # max. ~1,2 cm Kontur
    if is_round(entry):
        md.ellipse([0, 0, W - 1, H - 1], fill=255)
    else:
        r = round(min(W, H) * 0.16)
        md.rounded_rectangle([0, 0, W - 1, H - 1], radius=r, fill=255)
    img.paste(grad, (0, 0), mask)
    # Kontur: dunklere Variante der Grundfarbe (nicht schwarz, Stil C)
    edge = mask.point(lambda v: 255 if v > 0 else 0)
    inner = Image.new("L", (W, H), 0)
    idraw = ImageDraw.Draw(inner)
    if is_round(entry):
        idraw.ellipse([outline_w, outline_w, W - 1 - outline_w, H - 1 - outline_w], fill=255)
    else:
        r2 = max(0, round(min(W, H) * 0.16) - outline_w)
        idraw.rounded_rectangle([outline_w, outline_w, W - 1 - outline_w, H - 1 - outline_w], radius=r2, fill=255)
    ring = Image.eval(Image.merge("L", [edge]), lambda v: v)
    ring.paste(0, (0, 0), inner)
    dark = tuple(int(c * 0.55) for c in base) + (255,)
    img.paste(Image.new("RGBA", (W, H), dark), (0, 0), ring)
    # Glanzlicht oben links
    hl = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hl).ellipse([W * 0.12, H * 0.06, W * 0.55, H * 0.28], fill=70)
    hl.paste(0, (0, 0), Image.eval(inner, lambda v: 255 - v))
    img.paste(Image.new("RGBA", (W, H), (255, 255, 255, 255)), (0, 0), hl)
    img = img.resize((w, h), Image.LANCZOS)
    # Beschriftung (nur wenn sie passt)
    d = ImageDraw.Draw(img)
    label_cm = f"{entry['h_cm']:g} cm"
    for text in (f"{short_name(entry['id'])}\n{label_cm}", label_cm):
        fs = int(max(9, min(64, min(w, h) * 0.16)))
        f = font(fs)
        bb = d.multiline_textbbox((0, 0), text, font=f, align="center", spacing=2)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if tw <= w * 0.9 and th <= h * 0.8:
            pos = ((w - tw) / 2 - bb[0], (h - th) / 2 - bb[1])
            d.multiline_text(pos, text, font=f, fill=tuple(int(c * 0.35) for c in base) + (255,),
                             align="center", spacing=2, stroke_width=max(1, fs // 10),
                             stroke_fill=(255, 255, 255, 200))
            break
    return img, ppc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="kommagetrennte IDs")
    ap.add_argument("--out", default=str(ROOT / "assets" / "placeholders"))
    a = ap.parse_args(argv)
    table = json.loads((ROOT / "data" / "scale_table.json").read_text(encoding="utf-8"))
    only = set(a.only.split(",")) if a.only else None
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    index = {}
    for e in table["entries"]:
        if only and e["id"] not in only:
            continue
        if not e.get("w_cm") and not e.get("h_cm"):
            continue
        img, ppc = render(e)
        img.save(out / f"{e['id']}.png", optimize=True)
        index[e["id"]] = {"size_px": list(img.size), "px_per_cm": round(ppc, 4),
                          "h_cm": e["h_cm"], "w_cm": e.get("w_cm", e["h_cm"])}
    (out / "index.json").write_text(json.dumps(index, indent=1, sort_keys=True), encoding="utf-8")
    print(f"✅ {len(index)} Platzhalter → {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
