#!/usr/bin/env python3
"""Haustier-Sprites für den Haustier-Editor (P04-T09) – Stil C, 0 EUR, reproduzierbar.

Gleiches Prinzip wie die Editor-Teile (tools/make_editor_parts.py): Das PNG speichert
ZONEN-GEWICHTE in R/G/B + Deckung in A.  Der Shader assets/shaders/zone_tint.gdshader
mischt daraus die Fellfarben:   Farbe = R*zone1 + G*zone2 + B*zone3.

  Zone 1 (R) = Fell / Körper        Zone 2 (G) = Bauch, Schnauze, Muster
  Zone 3 (B) = Halsband, Horn, Flügel, Sattel  (Zubehör)
Augen/Nase sind dunkle Werte der Fell-Zone (kein Schwarz, Stil C).

Groesse: aus data/scale_table.json (1 Einheit = 1 cm). 8 px/cm, maximal 512 px lange Seite.

Aufruf:  python3 tools/make_pet_sprites.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from make_editor_parts import ZCanvas  # noqa: E402

PPC = 16.0
MAX_SIDE = 512
OUT = ROOT / "assets" / "sprites" / "pets"

#                        id                 label        icon     Zone1-Fell  Zone2   Zone3    Stimme
SPECIES = [
    ("pet_dog_small",    "Hund · klein",    "dog",     "#c98a4b", "#f2e0c8", "#e2574c", "pet_dog_bark"),
    ("pet_dog_medium",   "Hund · mittel",   "dog",     "#b8763f", "#f0dcbe", "#4f9bd8", "pet_dog_bark"),
    ("pet_dog_large",    "Hund · groß",     "dog",     "#8f6a4a", "#e9d7bd", "#6cbf6b", "pet_dog_bark"),
    ("pet_cat",          "Katze",           "cat",     "#b9b3c4", "#f6f0f6", "#e2574c", "pet_cat_meow"),
    ("pet_rabbit",       "Kaninchen",       "bunny",   "#e8e2e6", "#fdf7fb", "#8fd3c1", "pet_rabbit_squeak"),
    ("pet_bird",         "Vogel",           "bird",    "#6fc3e8", "#ffe6a8", "#e2574c", "pet_bird_chirp"),
    ("pet_hamster",      "Hamster",         "hamster", "#e0b071", "#fbeed7", "#e2574c", "pet_hamster_squeak"),
    ("pet_guinea_pig",   "Meerschweinchen", "hamster", "#d8a15f", "#f7e6c8", "#8fd3c1", "pet_guinea_pig_wheek"),
    ("pet_fish",         "Fisch",           "fish",    "#f0a24b", "#ffd98a", "#6fc3e8", "pet_fish_bubble"),
    ("pet_turtle",       "Schildkröte",     "hamster", "#7fbf6a", "#e8dcae", "#e2574c", "pet_turtle_hiss"),
    ("pet_pony",         "Pony",            "bunny",   "#f0dcc0", "#f7efe0", "#c98ad8", "pet_pony_whinny"),
    ("pet_mini_dragon",  "Mini-Drache",     "dog",     "#8fd3c1", "#e8f6ef", "#f0a24b", "pet_dragon_roar"),
    ("pet_mini_unicorn", "Mini-Einhorn",    "bunny",   "#fdf3f7", "#ffffff", "#f5c8e8", "pet_unicorn_sparkle"),
]


def table() -> dict:
    return {e["id"]: e for e in json.loads((ROOT / "data" / "scale_table.json").read_text(encoding="utf-8"))["entries"]}


# ------------------------------------------------------------------ Zeichenbausteine
def eyes(c: ZCanvas, cx: float, cy: float, dx: float, r: float) -> None:
    """Augen als dunkle Werte der Fell-Zone (kein Schwarz)."""
    for sx in (-dx, dx):
        c.shape("ellipse", c.box(cx + sx - r, cy - r, cx + sx + r, cy + r), fill=(70, 45), zone=0)
        c.shape("ellipse", c.box(cx + sx - r * 0.45, cy + r * 0.25, cx + sx + r * 0.45, cy + r * 0.9),
                fill=(255, 240), zone=1)


def collar(c: ZCanvas, cx: float, cy: float, w: float, h: float) -> None:
    c.shape("rounded", c.box(cx - w / 2, cy, cx + w / 2, cy + h), radius_cm=h * 0.45, fill=(255, 205), zone=2)
    c.shape("ellipse", c.box(cx - h * 0.7, cy - h * 0.5, cx + h * 0.7, cy + h * 1.4), fill=(255, 220), zone=2)


def sitting(c: ZCanvas, w: float, h: float, *, ear: str = "dog", tail: str = "curl",
            muzzle: bool = True, wings: bool = False, horn: bool = False, mane: bool = False) -> None:
    """Sitzendes Tier: Körper unten, Kopf oben (Hund, Katze, Hase, Drache …)."""
    body_h = h * 0.58
    c.shape("rounded", c.box(w * 0.10, 0.0, w * 0.90, body_h), radius_cm=w * 0.34,
            outline_cm=0.35, fill=(255, 195), zone=0)                       # Körper
    c.shape("ellipse", c.box(w * 0.30, body_h * 0.05, w * 0.70, body_h * 0.85), fill=(255, 225), zone=1)
    for sx in (-1.0, 1.0):                                                  # Vorderpfoten
        c.shape("ellipse", c.box(w * 0.5 + sx * w * 0.17 - w * 0.09, 0.0,
                                 w * 0.5 + sx * w * 0.17 + w * 0.09, h * 0.17), fill=(255, 230), zone=1)
    hy = body_h + h * 0.20                                                  # Kopf
    hr = min(w * 0.34, h * 0.26)
    if mane:
        c.shape("ellipse", c.box(w * 0.5 - hr * 1.5, hy - hr * 1.2, w * 0.5 + hr * 1.5, hy + hr * 1.2),
                fill=(255, 210), zone=1)
    c.shape("ellipse", c.box(w * 0.5 - hr, hy - hr, w * 0.5 + hr, hy + hr), outline_cm=0.3,
            fill=(255, 210), zone=0)
    if ear == "dog":
        for sx in (-1.0, 1.0):
            c.shape("ellipse", c.box(w * 0.5 + sx * hr * 0.95 - w * 0.09, hy - hr * 0.55,
                                     w * 0.5 + sx * hr * 0.95 + w * 0.09, hy + hr * 0.85),
                    fill=(210, 150), zone=0)
    elif ear == "cat":
        for sx in (-1.0, 1.0):
            c.shape("poly", [(w * 0.5 + sx * hr * 0.35, hy + hr * 0.55),
                             (w * 0.5 + sx * hr * 1.15, hy + hr * 1.35),
                             (w * 0.5 + sx * hr * 0.98, hy - hr * 0.05)], fill=(235, 180), zone=0)
    elif ear == "long":
        for sx in (-1.0, 1.0):
            c.shape("rounded", c.box(w * 0.5 + sx * hr * 0.5 - w * 0.06, hy + hr * 0.4,
                                     w * 0.5 + sx * hr * 0.5 + w * 0.06, hy + hr * 2.0),
                    radius_cm=w * 0.06, fill=(255, 220), zone=0)
            c.shape("rounded", c.box(w * 0.5 + sx * hr * 0.5 - w * 0.03, hy + hr * 0.5,
                                     w * 0.5 + sx * hr * 0.5 + w * 0.03, hy + hr * 1.85),
                    radius_cm=w * 0.03, fill=(255, 245), zone=1)
    elif ear == "dragon":
        for sx in (-1.0, 1.0):
            c.shape("poly", [(w * 0.5 + sx * hr * 0.55, hy + hr * 0.4),
                             (w * 0.5 + sx * hr * 1.5, hy + hr * 1.05),
                             (w * 0.5 + sx * hr * 0.75, hy - hr * 0.35)], fill=(255, 200), zone=1)
    if horn:
        c.shape("poly", [(w * 0.5 - hr * 0.16, hy + hr * 0.9), (w * 0.5 + hr * 0.16, hy + hr * 0.9),
                         (w * 0.5, hy + hr * 1.9)], fill=(255, 215), zone=2)
    if wings:
        for sx in (-1.0, 1.0):
            c.shape("poly", [(w * 0.5 + sx * w * 0.30, body_h * 0.85),
                             (w * 0.5 + sx * w * 0.48, body_h * 0.35),
                             (w * 0.5 + sx * w * 0.44, body_h * 0.95)], fill=(255, 205), zone=1)
    if muzzle:
        c.shape("ellipse", c.box(w * 0.5 - hr * 0.55, hy - hr * 0.55, w * 0.5 + hr * 0.55, hy + hr * 0.28),
                fill=(255, 240), zone=1)
        c.shape("ellipse", c.box(w * 0.5 - hr * 0.16, hy - hr * 0.28, w * 0.5 + hr * 0.16, hy + hr * 0.02),
                fill=(80, 50), zone=0)
    eyes(c, w * 0.5, hy + hr * 0.32, hr * 0.46, hr * 0.13)
    collar(c, w * 0.5, body_h * 0.92, w * 0.52, h * 0.07)
    if tail == "curl":
        c.shape("ellipse", c.box(w * 0.78, body_h * 0.18, w * 1.02, body_h * 0.62), fill=(255, 200), zone=0)
    elif tail == "long":
        c.shape("rounded", c.box(w * 0.72, body_h * 0.05, w * 0.95, body_h * 0.75),
                radius_cm=w * 0.09, fill=(255, 205), zone=1)


def standing(c: ZCanvas, w: float, h: float, *, horn: bool = False, mane: bool = False) -> None:
    """Stehendes Tier von der Seite (Pony, Einhorn)."""
    body_h, body_y = h * 0.46, h * 0.42
    for sx, lw in ((0.16, 0.075), (0.30, 0.075), (0.70, 0.075), (0.84, 0.075)):   # Beine
        c.shape("rounded", c.box(w * (sx - lw), 0.0, w * (sx + lw), body_y + h * 0.04),
                radius_cm=w * 0.05, fill=(240, 185), zone=0)
    c.shape("rounded", c.box(w * 0.16, body_y, w * 0.90, body_y + body_h), radius_cm=w * 0.14,
            outline_cm=0.35, fill=(255, 200), zone=0)                              # Rumpf
    c.shape("ellipse", c.box(w * 0.30, body_y + body_h * 0.08, w * 0.72, body_y + body_h * 0.75),
            fill=(255, 230), zone=1)
    c.shape("poly", [(w * 0.70, body_y + body_h * 0.55), (w * 0.92, body_y + body_h * 0.95),
                     (w * 0.86, body_y + h * 0.02), (w * 0.70, body_y + body_h * 0.15)],
            fill=(255, 200), zone=0)                                               # Hals
    hx, hy = w * 0.90, body_y + body_h * 1.05
    c.shape("ellipse", c.box(hx - w * 0.14, hy - h * 0.09, hx + w * 0.14, hy + h * 0.09),
            outline_cm=0.3, fill=(255, 215), zone=0)                               # Kopf
    c.shape("ellipse", c.box(hx + w * 0.02, hy - h * 0.04, hx + w * 0.14, hy + h * 0.02),
            fill=(255, 240), zone=1)                                               # Schnauze
    if mane:
        c.shape("poly", [(w * 0.66, hy + h * 0.02), (w * 0.74, body_y + body_h * 0.9),
                         (w * 0.86, body_y + body_h * 0.2), (w * 0.80, hy + h * 0.01)],
                fill=(255, 215), zone=1)
    if horn:
        c.shape("poly", [(hx - w * 0.03, hy + h * 0.07), (hx + w * 0.03, hy + h * 0.07),
                         (hx + w * 0.005, hy + h * 0.20)], fill=(255, 220), zone=2)
    c.shape("poly", [(w * 0.60, body_y + body_h * 0.80), (w * 0.66, body_y + body_h * 0.20),
                     (w * 0.74, body_y + body_h * 0.85)], fill=(255, 205), zone=1)  # Schweifansatz
    eye_y = hy + h * 0.01
    c.shape("ellipse", c.box(hx - w * 0.02, eye_y - h * 0.012, hx + w * 0.02, eye_y + h * 0.012),
            fill=(70, 45), zone=0)
    collar(c, w * 0.80, body_y + body_h * 0.72, w * 0.20, h * 0.05)


def bird(c: ZCanvas, w: float, h: float) -> None:
    c.shape("ellipse", c.box(w * 0.18, 0.0, w * 0.82, h * 0.92), outline_cm=0.25,
            fill=(255, 195), zone=0)
    c.shape("ellipse", c.box(w * 0.34, h * 0.10, w * 0.72, h * 0.72), fill=(255, 230), zone=1)
    c.shape("ellipse", c.box(w * 0.30, h * 0.28, w * 0.70, h * 0.80), fill=(255, 210), zone=0)   # Flügel
    c.shape("poly", [(w * 0.18, h * 0.55), (w * 0.02, h * 0.78), (w * 0.18, h * 0.72)],
            fill=(255, 205), zone=2)                                                             # Schnabel
    c.shape("poly", [(w * 0.82, h * 0.30), (w * 1.00, h * 0.16), (w * 0.84, h * 0.46)],
            fill=(255, 195), zone=0)                                                             # Schwanz
    for sx in (-1.0, 1.0):
        c.line((w * (0.5 + sx * 0.10), 0.0), (w * (0.5 + sx * 0.10), h * 0.10), 0.35, 150, zone=2)
    c.shape("ellipse", c.box(w * 0.58, h * 0.66, w * 0.72, h * 0.78), fill=(70, 45), zone=0)
    c.shape("ellipse", c.box(w * 0.63, h * 0.70, w * 0.68, h * 0.75), fill=(255, 245), zone=1)


def fish(c: ZCanvas, w: float, h: float) -> None:
    c.shape("ellipse", c.box(w * 0.22, h * 0.06, w * 0.86, h * 0.94), outline_cm=0.2,
            fill=(255, 195), zone=0)
    c.shape("ellipse", c.box(w * 0.30, h * 0.16, w * 0.80, h * 0.60), fill=(255, 235), zone=1)
    c.shape("poly", [(w * 0.84, h * 0.5), (w * 1.00, h * 0.14), (w * 1.00, h * 0.86)],
            fill=(255, 210), zone=2)
    c.shape("poly", [(w * 0.46, h * 0.94), (w * 0.62, h * 1.00), (w * 0.60, h * 0.80)],
            fill=(255, 220), zone=2)
    c.shape("ellipse", c.box(w * 0.32, h * 0.56, w * 0.42, h * 0.74), fill=(255, 245), zone=1)
    c.shape("ellipse", c.box(w * 0.34, h * 0.60, w * 0.40, h * 0.70), fill=(70, 45), zone=0)


def turtle(c: ZCanvas, w: float, h: float) -> None:
    c.shape("ellipse", c.box(w * 0.10, h * 0.18, w * 0.90, h * 0.98), outline_cm=0.2,
            fill=(255, 200), zone=0)                                     # Panzer
    for i in range(3):
        x0 = w * (0.24 + i * 0.22)
        c.shape("ellipse", c.box(x0, h * 0.36, x0 + w * 0.18, h * 0.80), fill=(255, 235), zone=1)
    c.shape("ellipse", c.box(w * 0.80, h * 0.24, w * 1.00, h * 0.66), fill=(255, 220), zone=0)   # Kopf
    c.shape("ellipse", c.box(w * 0.94, h * 0.36, w * 0.99, h * 0.46), fill=(70, 45), zone=0)
    for x0 in (w * 0.14, w * 0.30, w * 0.58, w * 0.70):
        c.shape("rounded", c.box(x0, 0.0, x0 + w * 0.12, h * 0.28), radius_cm=h * 0.12,
                fill=(250, 210), zone=0)
    collar(c, w * 0.88, h * 0.24, w * 0.14, h * 0.10)


def rodent(c: ZCanvas, w: float, h: float, *, ears: float = 0.30) -> None:
    c.shape("ellipse", c.box(w * 0.04, 0.0, w * 0.96, h * 0.94), outline_cm=0.25,
            fill=(255, 195), zone=0)
    c.shape("ellipse", c.box(w * 0.24, h * 0.06, w * 0.80, h * 0.66), fill=(255, 235), zone=1)
    for sx in (-1.0, 1.0):
        c.shape("ellipse", c.box(w * (0.5 + sx * 0.30) - w * ears * 0.5, h * 0.62,
                                 w * (0.5 + sx * 0.30) + w * ears * 0.5, h * (0.62 + ears)),
                fill=(245, 190), zone=0)
        c.shape("ellipse", c.box(w * (0.5 + sx * 0.30) - w * ears * 0.28, h * 0.68,
                                 w * (0.5 + sx * 0.30) + w * ears * 0.28, h * (0.68 + ears * 0.7)),
                fill=(255, 240), zone=1)
    c.shape("ellipse", c.box(w * 0.66, h * 0.30, w * 0.82, h * 0.46), fill=(255, 245), zone=1)   # Schnauze
    c.shape("ellipse", c.box(w * 0.71, h * 0.34, w * 0.78, h * 0.41), fill=(80, 50), zone=0)
    eyes(c, w * 0.52, h * 0.52, w * 0.13, w * 0.045)
    collar(c, w * 0.42, h * 0.22, w * 0.34, h * 0.10)


DRAW = {
    "pet_dog_small": lambda c, w, h: sitting(c, w, h, ear="dog"),
    "pet_dog_medium": lambda c, w, h: sitting(c, w, h, ear="dog", tail="long"),
    "pet_dog_large": lambda c, w, h: sitting(c, w, h, ear="dog", tail="long"),
    "pet_cat": lambda c, w, h: sitting(c, w, h, ear="cat", tail="long"),
    "pet_rabbit": lambda c, w, h: sitting(c, w, h, ear="long", tail="curl"),
    "pet_mini_dragon": lambda c, w, h: sitting(c, w, h, ear="dragon", wings=True, tail="long"),
    "pet_bird": bird,
    "pet_fish": fish,
    "pet_turtle": turtle,
    "pet_hamster": lambda c, w, h: rodent(c, w, h, ears=0.34),
    "pet_guinea_pig": lambda c, w, h: rodent(c, w, h, ears=0.22),
    "pet_pony": lambda c, w, h: standing(c, w, h),
    "pet_mini_unicorn": lambda c, w, h: standing(c, w, h, horn=True, mane=True),
}


def main() -> int:
    T = table()
    OUT.mkdir(parents=True, exist_ok=True)
    index = {}
    for pid, label, icon, fur1, fur2, fur3, voice in SPECIES:
        e = T[pid]
        w_cm, h_cm = float(e["w_cm"]), float(e["h_cm"])
        ppc = min(PPC, MAX_SIDE / max(w_cm, h_cm))
        c = ZCanvas(w_cm, h_cm, ppc)
        DRAW[pid](c, w_cm, h_cm)
        img = c.finish()
        img.save(OUT / f"{pid}.png", optimize=True)
        index[pid] = {"label": label, "icon": icon, "w_cm": w_cm, "h_cm": h_cm,
                      "size_px": list(img.size), "colors": [fur1, fur2, fur3], "voice": voice,
                      "sprite": f"assets/sprites/pets/{pid}.png"}
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✅ {len(SPECIES)} Haustier-Sprites → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
