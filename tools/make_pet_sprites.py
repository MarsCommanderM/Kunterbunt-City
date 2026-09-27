#!/usr/bin/env python3
"""Haustier-Sprites (P04b-T07) im Stil C: Vektor, weiche Schattierung, braune Tinte, großer Kopf.

Zeichnungen in tools/pets/draw.py (Entwurfs-Einheiten: Höhe 100). Das PNG speichert Zonen-Gewichte in R/G/B
(Rest = Tinte) wie Figuren und Items; der Shader assets/shaders/zone_tint.gdshader färbt ein:
  Zone 1 = Fell / Körper · Zone 2 = Bauch, Schnauze, Pfoten, Glanz · Zone 3 = Halsband, Mähne, Flügel, Schnabel.
Größe im Spiel kommt aus data/scale_table.json (Seitenverhältnis = Tabelle).

Aufruf:  python3 tools/make_pet_sprites.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pets import draw as D  # noqa: E402

PPC = 8.0          # px je Entwurfs-Einheit → Tiere ~800 px hoch (scharf auch groß im Editor)
OUT = ROOT / "assets" / "sprites" / "pets"

#                        id                 label        icon     Zone1-Fell  Zone2   Zone3    Stimme
SPECIES = [
    ("pet_dog_small",    "Hund · klein",    "dog",     "#d9a066", "#fbeed7", "#e2574c", "pet_dog_bark"),
    ("pet_dog_medium",   "Hund · mittel",   "dog",     "#b8763f", "#f6e6cc", "#4f9bd8", "pet_dog_bark"),
    ("pet_dog_large",    "Hund · groß",     "dog",     "#8f6a4a", "#efdcc2", "#6cbf6b", "pet_dog_bark"),
    ("pet_cat",          "Katze",           "cat",     "#f0a24b", "#fbeedc", "#e2574c", "pet_cat_meow"),
    ("pet_rabbit",       "Kaninchen",       "bunny",   "#e8e2e6", "#fdf2f6", "#f28fb1", "pet_rabbit_squeak"),
    ("pet_bird",         "Vogel",           "bird",    "#6fc3e8", "#fff1c4", "#f0a24b", "pet_bird_chirp"),
    ("pet_hamster",      "Hamster",         "hamster", "#e0b071", "#fdf1dc", "#f28fb1", "pet_hamster_squeak"),
    ("pet_guinea_pig",   "Meerschweinchen", "hamster", "#c98a4b", "#fbeedc", "#f28fb1", "pet_guinea_pig_wheek"),
    ("pet_fish",         "Fisch",           "fish",    "#f0a24b", "#fff4e0", "#e2574c", "pet_fish_bubble"),
    ("pet_turtle",       "Schildkröte",     "hamster", "#7fbf6a", "#e8dcae", "#c98a4b", "pet_turtle_hiss"),
    ("pet_pony",         "Pony",            "bunny",   "#e0b98a", "#f7efe0", "#8a5a3c", "pet_pony_whinny"),
    ("pet_mini_dragon",  "Mini-Drache",     "dog",     "#8fd3c1", "#fff4dc", "#f0a24b", "pet_dragon_roar"),
    ("pet_mini_unicorn", "Mini-Einhorn",    "bunny",   "#fdf3f7", "#fff8e0", "#c98ad8", "pet_unicorn_sparkle"),
]

DRAW = {
    "pet_dog_small": lambda p: D.sitting(p, ears="point", tail="wag"),
    "pet_dog_medium": lambda p: D.sitting(p, ears="flop", tail="wag"),
    "pet_dog_large": lambda p: D.sitting(p, ears="flop", tail="long"),
    "pet_cat": lambda p: D.sitting(p, ears="point", tail="long", whiskers=True),
    "pet_rabbit": lambda p: D.sitting(p, ears="long", tail="puff", whiskers=True),
    "pet_mini_dragon": lambda p: D.sitting(p, ears="horns", tail="dragon", wings=True),
    "pet_bird": D.bird,
    "pet_fish": D.fish,
    "pet_turtle": D.turtle,
    "pet_hamster": lambda p: D.rodent(p),
    "pet_guinea_pig": lambda p: D.rodent(p, long=True),
    "pet_pony": lambda p: D.standing(p),
    "pet_mini_unicorn": lambda p: D.standing(p, horn=True),
}


def table() -> dict:
    return {e["id"]: e for e in json.loads((ROOT / "data" / "scale_table.json").read_text(encoding="utf-8"))["entries"]}


def main() -> int:
    T = table()
    OUT.mkdir(parents=True, exist_ok=True)
    index = {}
    for pid, label, icon, fur1, fur2, fur3, voice in SPECIES:
        e = T[pid]
        w_cm, h_cm = float(e["w_cm"]), float(e["h_cm"])
        p = D.Pet(100.0 * w_cm / h_cm, 100.0, PPC)
        DRAW[pid](p)
        img, _info = p.finish()
        img.save(OUT / f"{pid}.png", optimize=True)
        index[pid] = {"label": label, "icon": icon, "w_cm": w_cm, "h_cm": h_cm,
                      "size_px": list(img.size), "colors": [fur1, fur2, fur3], "voice": voice,
                      "sprite": f"assets/sprites/pets/{pid}.png"}
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✅ {len(SPECIES)} Haustier-Sprites → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
