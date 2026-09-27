#!/usr/bin/env python3
"""
P07: Raum-Hintergründe aus den Bereichs-Daten erzeugen (Stil C, Vektor). Entscheidung 👤: Räume starten LEER –
im Bild nur Boden und Wände (+ Dachschräge, Außen-Kulisse). Fenster, Türen, Teppiche … baut das Kind aus Items.

Für jeden Raum mit `scene` in data/areas/<bereich>.json:
  • Wand-Ebene (Zonen, geteilt je Breite/Variante)  → Tapete + Muster im Spiel wählbar (Shader)
  • Boden-Ebene (Zonen, geteilt je Breite/Art)      → Boden wählbar
  • Detail-Ebene (fest eingefärbt, je Raum)         → Dachschräge, Außen-Kulisse
  • <raum>.bg.json (px/cm, Ursprung, Kacheln ≤ 2048 px, Ebenen) + <raum>_thumb.png (Raum-Wahl im Spiel)

Aufruf: python3 tools/make_rooms.py [--area home] [--only raum,raum]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rooms import details as D  # noqa: E402
from rooms import layers as L  # noqa: E402
from rooms.base import BOTTOM, INK, PPC, WALL_H, Sheet, hexcol, tiles  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "assets/backgrounds/shared"


def _tint(img: Image.Image, cols: list[str], pattern: str = "", pattern_col: str = "", repeat_cm: float = 48.0) -> Image.Image:
    """Zonen-Ebene einfärben wie der Shader (für Vorschaubilder)."""
    a = np.asarray(img, np.float32) / 255.0
    r, g, b, al = a[..., 0:1], a[..., 1:2], a[..., 2:3], a[..., 3:4]
    z1 = np.broadcast_to(hexcol(cols[0]), a.shape[:2] + (3,)).copy()
    if pattern:
        tex = np.asarray(Image.open(ROOT / f"assets/shaders/wallpapers/{pattern}.png").getchannel("A"), np.float32) / 255.0
        rep = max(1, int(round(img.width / PPC / repeat_cm)))
        tw = max(1, img.width // rep)
        tile = np.asarray(Image.fromarray((tex * 255).astype(np.uint8)).resize((tw, tw)), np.float32) / 255.0
        ny, nx = -(-img.height // tw), -(-img.width // tw)
        p = np.tile(tile, (ny, nx))[: img.height, : img.width, None]
        z1 = z1 * (1 - p) + hexcol(pattern_col) * p
    rest = np.clip(1.0 - r - g - b, 0.0, 1.0)
    rgb = r * z1 + g * hexcol(cols[1]) + b * hexcol(cols[2]) + rest * INK
    return Image.fromarray(np.clip(np.concatenate([rgb, al], -1) * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")


def _shared_layer(name: str, make) -> tuple[Image.Image, list[dict]]:
    """Geteilte Zonen-Ebene: einmal zeichnen, für alle Räume gleicher Breite nutzen."""
    SHARED.mkdir(parents=True, exist_ok=True)
    img = make()
    return img, tiles(img, SHARED / name, ROOT)


def build_room(area_id: str, room: dict, cache: dict) -> dict:
    sc = room["scene"]
    width = float(room["width_cm"])
    outdoor = sc.get("kind") == "outdoor"
    top = float(room.get("height_cm", WALL_H))
    sheet = Sheet(width, top_cm=top, bottom_cm=BOTTOM)
    out_dir = ROOT / f"assets/backgrounds/{area_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    decor = dict(sc.get("decor", {}))
    layers = []
    wall_img = floor_img = None
    if not outdoor:
        variant = "panel" if sc.get("wainscot", True) else "plain"
        key = f"wall_{int(width)}_{variant}"
        if key not in cache:
            cache[key] = _shared_layer(key, lambda: L.wall(width, WALL_H, variant == "panel"))
        wall_img, wall_tiles = cache[key]
        layers.append({"kind": "wall", "y_px": round((top - WALL_H) * PPC), "tiles": wall_tiles})
    fkind = decor.get("floor", "planks")
    floors = {}
    for kind in L.FLOOR_KINDS:                          # jede Bodenart für jede Breite → im Spiel frei wählbar
        fkey = f"floor_{int(width)}_{kind}"
        if fkey not in cache:
            cache[fkey] = _shared_layer(fkey, lambda k=kind: L.floor(width, k))
        floors[kind] = {"y_px": round(top * PPC), "tiles": cache[fkey][1]}
    floor_img = cache[f"floor_{int(width)}_{fkind}"][0]
    # Details (fest)
    if outdoor:
        D.outdoor(sheet, width, seed=int(sc.get("seed", 5)))
    if "roof" in sc.get("extras", []):
        D.roof_slopes(sheet, width)
    detail_tiles = tiles(sheet.img, out_dir / f"{room['id']}_detail", ROOT)
    meta = {
        "px_per_cm": PPC, "size_px": [sheet.img.width, sheet.img.height], "origin_px": sheet.origin_px(),
        "source": "tools/make_rooms.py", "tiles": detail_tiles, "layers": layers, "floors": floors, "decor": decor,
        "note": "Ebene 'wall' und 'floors' (je Bodenart) sind Zonen-kodiert (Shader färbt nach decor), 'tiles' ist fest.",
    }
    (out_dir / f"{room['id']}.bg.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    # Vorschaubild für die Raum-Wahl (so, wie das Kind den Raum zuerst sieht)
    full = Image.new("RGBA", sheet.img.size, (0, 0, 0, 0))
    if wall_img is not None:
        full.alpha_composite(_tint(wall_img, decor.get("wall", ["#f3e6d0", "#ffffff", "#b9d7c0"]),
                                   decor.get("pattern", ""), decor.get("pattern_col", "#ffffff")), (0, round((top - WALL_H) * PPC)))
    full.alpha_composite(_tint(floor_img, decor.get("floor_cols", ["#d9a066", "#c98a4b", "#8a5a3c"])), (0, round(top * PPC)))
    full.alpha_composite(sheet.img)
    thumb = full.crop((0, 0, full.width, round((top + 70) * PPC)))
    thumb.thumbnail((360, 200), Image.LANCZOS)
    thumb.save(out_dir / f"{room['id']}_thumb.png", optimize=True)
    return meta


def thumb_from_bg(area_id: str, room: dict) -> None:
    """Vorschaubild für einen eingemessenen (gemalten) Raum aus seinen Kacheln – für die Raum-Wahl."""
    meta = json.loads((ROOT / room["background"].replace("res://", "")).read_text(encoding="utf-8"))
    img = Image.new("RGBA", tuple(meta["size_px"]), (0, 0, 0, 0))
    for t in meta["tiles"]:
        img.alpha_composite(Image.open(ROOT / t["file"].replace("res://", "")).convert("RGBA"), (int(t["x_px"]), int(t["y_px"])))
    ppc = float(meta["px_per_cm"])
    oy = float(meta["origin_px"][1])
    top = max(0, round(oy - float(room.get("height_cm", WALL_H)) * ppc))
    img = img.crop((0, top, img.width, min(img.height, round(oy + 70 * ppc))))
    img.thumbnail((360, 200), Image.LANCZOS)
    out = ROOT / f"assets/backgrounds/{area_id}"
    out.mkdir(parents=True, exist_ok=True)
    img.save(out / f"{room['id']}_thumb.png", optimize=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--area", default="home")
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    path = ROOT / f"data/areas/{a.area}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    only = {x for x in a.only.split(",") if x}
    cache: dict = {}
    n = 0
    for room in data["rooms"]:
        if only and room["id"] not in only:
            continue
        if "scene" not in room:
            if room.get("background"):
                thumb_from_bg(data["id"], room)
            continue
        build_room(data["id"], room, cache)
        n += 1
        print(f"  {room['id']}: {room['width_cm']:.0f} cm")
    print(f"✅ {n} Räume → assets/backgrounds/{data['id']}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
