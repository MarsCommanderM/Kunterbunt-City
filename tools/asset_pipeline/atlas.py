#!/usr/bin/env python3
"""P06-T06 – Atlas: pro Bereich ein Blatt (≤ 4096²), Godot-kompatibel.

Shelf-Packing: Items nach Höhe absteigend, in Reihen eingereiht.
Ausgabe:
  ``assets/sprites/<bereich>_atlas.png``      – gesammeltes Blatt
  ``assets/sprites/<bereich>_atlas.json``     – Regionen {id: {x, y, w, h}} + size

Die .import-Datei erzeugt Godot beim nächsten ``--headless --import`` mit den
Projekt-Standardeinstellungen (wie alle anderen Sprites auch).
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SPRITES_ROOT = ROOT / "assets" / "sprites"

MAX_SIZE = 4096
GUTTER = 2          # px Abstand zwischen Regionen (verhindert Sampler-Leaks)


class AtlasError(Exception):
    """Items passen nicht ins Atlas (oder sind leer)."""


def pack(sprites: dict[str, Image.Image], *, max_size: int = MAX_SIZE,
         gutter: int = GUTTER) -> tuple[Image.Image, dict[str, dict]]:
    """Sprites → ein Atlasbild + Regions-Map. Reihen-Packung nach Höhe."""
    if not sprites:
        raise AtlasError("keine Sprites zum Packen")
    order = sorted(sprites.items(), key=lambda kv: -kv[1].height)
    shelf_y, x, y, shelf_h = 0, gutter, gutter, 0
    regions: dict[str, dict] = {}
    for name, im in order:
        w, h = im.width, im.height
        if w + 2 * gutter > max_size or h + 2 * gutter > max_size:
            raise AtlasError(f"{name} ({w}×{h}) ist größer als das Atlas-Limit {max_size}")
        if x + w + gutter > max_size:            # neue Reihe
            x = gutter
            y += shelf_h + gutter
            shelf_h = 0
        if y + h + gutter > max_size:
            raise AtlasError(f"Atlas-Limit {max_size}² überschritten "
                             f"({len(sprites)} Sprites, {len(regions)} gepackt)")
        regions[name] = {"x": x, "y": y, "w": w, "h": h}
        x += w + gutter
        shelf_h = max(shelf_h, h)
        shelf_y = y
    atlas = Image.new("RGBA", (max_size, max_size), (0, 0, 0, 0))
    for name, im in order:
        r = regions[name]
        atlas.alpha_composite(im, (r["x"], r["y"]))
    return atlas, regions


def build_area(area: str, *, sprites_root: Path | None = None,
               max_size: int = MAX_SIZE) -> tuple[Path, Path]:
    """Alle Sprites eines Bereichs packen und ablegen."""
    root = Path(sprites_root) if sprites_root else SPRITES_ROOT
    src = root / area
    files = sorted(src.glob("*.png"))
    if not files:
        raise AtlasError(f"{src}: keine Sprites")
    sprites = {p.stem: Image.open(p).convert("RGBA") for p in files}
    atlas, regions = pack(sprites, max_size=max_size)
    png = root / f"{area}_atlas.png"
    js = root / f"{area}_atlas.json"
    atlas.save(png)
    js.write_text(json.dumps(
        {"area": area, "size": [atlas.width, atlas.height],
         "gutter": GUTTER, "regions": regions},
        indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return png, js


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("area", nargs="?", default="home")
    ap.add_argument("--sprites-root", type=Path, default=SPRITES_ROOT)
    a = ap.parse_args(argv)
    png, js = build_area(a.area, sprites_root=a.sprites_root)
    print(f"Atlas → {png.name} + {js.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
