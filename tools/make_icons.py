#!/usr/bin/env python3
"""
P04b-T08: alle UI-, Editor-, Tier- und Bereichs-Symbole im Stil C (ersetzt make_ui_icons.py).

Jedes Icon wird als Vektor mit Farbzonen + Tinte gezeichnet, fertig eingefärbt („gebacken“) und als
256×256-PNG nach assets/ui/icons/ geschrieben. Die Symbole brauchen kein `modulate` mehr.

Aufruf: python3 tools/make_icons.py [--only name,name] [--sheet out.png] [--jobs 4]
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from icons import area_set as A  # noqa: E402
from icons import editor_set as E  # noqa: E402
from icons import ui_set as U  # noqa: E402
from icons.base import SIZE, Icon  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/ui/icons"

ICONS = {
    # Aktionen
    "check": U.check, "close": U.close, "back": U.back, "forward": U.forward, "undo": U.undo, "plus": U.plus,
    "trash": U.trash, "copy": U.copy, "folder": U.folder, "gear": U.gear, "map": U.map_, "heart": U.heart,
    "star": U.star, "speaker": U.speaker, "mute": U.mute, "palette": U.palette, "dice": U.dice,
    "magnifier": U.magnifier, "lock": U.lock, "home": U.home, "brush": U.brush, "pencil": U.pencil,
    "backpack": U.backpack, "album": U.album, "camera": U.camera, "nametag": U.nametag, "gift": U.gift,
    "music": U.music, "sun": U.sun, "moon": U.moon, "wrench": U.wrench, "ball": U.ball, "bone": U.bone,
    "peek": U.peek,
    # Editor + Tiere
    "shirt": E.shirt, "pants": E.pants, "shoe": E.shoe, "hair": E.hair, "eye": E.eye, "mouth": E.mouth,
    "bow": E.bow, "glasses": E.glasses, "person": E.person, "hand": E.hand, "paw": E.paw,
    "dog": E.dog, "cat": E.cat, "bunny": E.bunny, "hamster": E.hamster, "bird": E.bird, "fish": E.fish,
    # Bereiche
    "area_home": A.area_home, "area_hospital": A.area_hospital, "area_school": A.area_school,
    "area_pool": A.area_pool, "area_playground": A.area_playground, "area_fair": A.area_fair,
    "area_shop": A.area_shop, "area_sports": A.area_sports, "area_ice": A.area_ice, "area_flower": A.area_flower,
    "area_zoo": A.area_zoo, "area_workshop": A.area_workshop, "car": A.car, "area_forest": A.area_forest,
    "area_camping": A.area_camping, "area_hair": A.area_hair, "area_bike": A.area_bike,
}


def render(name: str):
    ic = Icon()
    ICONS[name](ic)
    return name, ic.bake()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--sheet", default="")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args(argv)
    names = [n for n in a.only.split(",") if n] or list(ICONS)
    OUT.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(a.jobs) as ex:
        done = list(ex.map(render, names))
    for name, img in done:
        img.save(OUT / f"{name}.png", optimize=True)
    if a.sheet:
        from PIL import Image, ImageDraw
        cols = 10
        cell = SIZE // 2 + 30
        sheet = Image.new("RGBA", (cols * cell, -(-len(done) // cols) * cell), (255, 248, 238, 255))
        for k, (name, img) in enumerate(done):
            x, y = (k % cols) * cell, (k // cols) * cell
            sheet.alpha_composite(img.resize((SIZE // 2, SIZE // 2), Image.LANCZOS), (x + 15, y + 4))
            ImageDraw.Draw(sheet).text((x + 6, y + cell - 22), name, fill=(80, 60, 60, 255))
        sheet.convert("RGB").save(a.sheet)
    print(f"✅ {len(done)} Symbole → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
