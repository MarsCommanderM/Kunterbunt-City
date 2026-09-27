"""
Blick-Check aller Katalog-Vorlagen (P04b): färbt jede Vorlage wie der Shader im Spiel ein
(Farbe = R·z1 + G·z2 + B·z3 + Rest·Tinte) und legt sie als Kontaktbogen je Gruppe ab.
Optional maßstabsgetreu (alle Items einer Seite im selben px/cm) – damit man Größen vergleicht.

Aufruf: python3 tools/items/review_sheet.py <out_dir> [--scale] [--states]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
INK = np.array([0x3B, 0x2A, 0x2A], np.float32) / 255.0
BG = (246, 240, 230, 255)


def _hex(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


def tint(path: Path, colors: list[str]) -> Image.Image:
    """Genau die Shader-Formel – so sieht das Kind das Item."""
    a = np.asarray(Image.open(path).convert("RGBA"), np.float32) / 255.0
    z = [_hex(c) for c in (colors + ["#ffffff"] * 3)[:3]] if colors else None
    if z is None:
        return Image.open(path).convert("RGBA")
    r, g, b = a[..., 0:1], a[..., 1:2], a[..., 2:3]
    rest = np.clip(1.0 - r - g - b, 0.0, 1.0)
    col = r * z[0] + g * z[1] + b * z[2] + rest * INK
    out = np.concatenate([np.clip(col, 0, 1), a[..., 3:4]], axis=-1)
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def _items_by_group() -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    seen: set[str] = set()
    for f in sorted((ROOT / "data/items").glob("catalog_*.json")):
        for it in json.loads(f.read_text())["items"]:
            spr = it["sprite"]
            if spr in seen:        # je Vorlage nur die erste Farbvariante
                continue
            seen.add(spr)
            groups.setdefault(it.get("catalog", f.stem[8:]), []).append(it)
    return groups


def sheet(items: list[dict], cell: int = 200, cols: int = 8, scale: bool = False, states: bool = False) -> Image.Image:
    tiles: list[Image.Image] = []
    max_cm = max(max(it["size_cm"]) for it in items) if scale else 0.0
    for it in items:
        paths = [ROOT / it["sprite"].replace("res://", "")]
        if states:
            paths += [ROOT / p.replace("res://", "") for p in it.get("state_sprites", {}).values()]
        for p in paths:
            im = tint(p, it.get("colors", []))
            if scale:
                f = (cell - 16) / max_cm * max(it["size_cm"]) / max(im.size)
                im = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
            else:
                im.thumbnail((cell - 16, cell - 30), Image.LANCZOS)
            t = Image.new("RGBA", (cell, cell), BG)
            t.alpha_composite(im, ((cell - im.width) // 2, cell - 22 - im.height))
            ImageDraw.Draw(t).text((4, cell - 16), it["id"][:30], fill=(90, 70, 70, 255))
            tiles.append(t)
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGBA", (cols * cell, rows * cell), (255, 255, 255, 255))
    for i, t in enumerate(tiles):
        out.paste(t, ((i % cols) * cell, (i // cols) * cell))
    return out.convert("RGB")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--scale", action="store_true")
    ap.add_argument("--states", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    only = {s for s in a.only.split(",") if s}
    for g, items in _items_by_group().items():
        if only and g not in only:
            continue
        sheet(items, scale=a.scale, states=a.states).save(out / f"{g}.jpg", quality=85)
        print(f"{g}: {len(items)} Vorlagen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
