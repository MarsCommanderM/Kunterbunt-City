#!/usr/bin/env python3
"""
Hintergründe einmessen (Maßstab-Bibel §6, Regel S-10) – erste Version (Phase 01).

Liest den Block "calibration" eines Raums aus data/areas/<bereich>.json:
    source            Quellbild (relativ zum Repo)
    ref               ID in data/scale_table.json, deren Höhe das Referenzmaß ist (z. B. fix_counter = 90 cm)
    px_top/px_bottom  obere/untere Kante des Referenzmaßes im Quellbild (px)
    floor_back_px     hintere Bodenlinie (Wand trifft Boden) im Quellbild
    floor_front_px    vordere Bodenlinie
    origin_x_px       x-Position, die 0 cm entspricht
    crop_px           [x0, y0, x1, y1] – nutzbarer Bildbereich
    surfaces_px       [{id, type, x_px:[a,b], top_px, depth_px}]
    out_px_per_cm     Ziel-Auflösung (Standard 8; bei kleinen Quellen max. 2× Hochskalierung sinnvoll)

Schreibt:
    assets/backgrounds/<bereich>/<raum>_<i>.png   Kacheln (≤ 2048 px)
    assets/backgrounds/<bereich>/<raum>.bg.json   Kachel-Liste + Ursprung
und trägt im Raum ein: background, width_cm, height_cm, floor.back_y_cm/front_y_cm, surfaces (cm).

Koordinaten (1 Einheit = 1 cm): x nach rechts; y = 0 auf der hinteren Bodenlinie,
negativ = nach oben (Wand), positiv = nach vorne/unten (Bodenband).

Aufruf:  python3 tools/asset_pipeline/calibrate_bg.py data/areas/test_kitchen.json [--room kitchen]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MAX_TILE = 2048


def scale_height(ref: str) -> float:
    table = json.loads((ROOT / "data" / "scale_table.json").read_text(encoding="utf-8"))
    for e in table["entries"]:
        if e["id"] == ref:
            return float(e.get("surface_h_cm", e["h_cm"]))
    raise SystemExit(f"❌ calibration.ref '{ref}' fehlt in scale_table.json")


def calibrate_room(area: dict, room: dict, out_dir: Path, res_prefix: str) -> dict:
    c = room["calibration"]
    ref_h = scale_height(c["ref"])
    src_ppc = (c["px_bottom"] - c["px_top"]) / ref_h          # Quell-px pro cm
    if src_ppc <= 0:
        raise SystemExit("❌ px_bottom muss größer als px_top sein")
    out_ppc = float(c.get("out_px_per_cm", 8))
    up = out_ppc / src_ppc
    if up > 2.2:
        print(f"⚠️  {room['id']}: Hochskalierung ×{up:.1f} (Quelle nur {src_ppc:.2f} px/cm) – "
              f"out_px_per_cm senken oder Hintergrund größer generieren")

    img = Image.open(ROOT / c["source"]).convert("RGBA")
    x0, y0, x1, y1 = c.get("crop_px", [0, 0, img.width, img.height])
    img = img.crop((x0, y0, x1, y1))
    k = out_ppc / src_ppc
    out = img.resize((max(1, round(img.width * k)), max(1, round(img.height * k))), Image.LANCZOS)

    # Ursprung (0 cm | hintere Bodenlinie) in Ausgabe-Pixeln
    origin = [(c["origin_x_px"] - x0) * k, (c["floor_back_px"] - y0) * k]

    out_dir.mkdir(parents=True, exist_ok=True)
    tiles = []
    nx, ny = math.ceil(out.width / MAX_TILE), math.ceil(out.height / MAX_TILE)
    for j in range(ny):
        for i in range(nx):
            box = (i * MAX_TILE, j * MAX_TILE, min(out.width, (i + 1) * MAX_TILE), min(out.height, (j + 1) * MAX_TILE))
            name = f"{room['id']}_{j}_{i}.png"
            out.crop(box).save(out_dir / name, optimize=True)
            tiles.append({"file": f"{res_prefix}/{name}", "x_px": box[0], "y_px": box[1]})
    meta = {
        "px_per_cm": out_ppc, "size_px": [out.width, out.height], "origin_px": [round(v, 2) for v in origin],
        "source": c["source"], "source_px_per_cm": round(src_ppc, 4), "tiles": tiles,
    }
    (out_dir / f"{room['id']}.bg.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    to_cm_x = lambda px: round((px - c["origin_x_px"]) / src_ppc, 1)
    to_cm_y = lambda px: round((px - c["floor_back_px"]) / src_ppc, 1)
    room["background"] = f"{res_prefix}/{room['id']}.bg.json"
    room["width_cm"] = round((x1 - c["origin_x_px"]) / src_ppc, 1)
    room["height_cm"] = round((c["floor_back_px"] - y0) / src_ppc, 1)
    room.setdefault("floor", {})
    room["floor"]["back_y_cm"] = 0.0
    room["floor"]["front_y_cm"] = to_cm_y(c["floor_front_px"])
    room["floor"].setdefault("depth_scale_max", 1.12)
    room["surfaces"] = [{
        "id": s["id"], "type": s["type"],
        "x_cm": [to_cm_x(s["x_px"][0]), to_cm_x(s["x_px"][1])],
        "h_cm": round((s["depth_px"] - s["top_px"]) / src_ppc, 1),
        "depth_y_cm": to_cm_y(s["depth_px"]),
    } for s in c.get("surfaces_px", [])]
    print(f"✅ {area['id']}/{room['id']}: {src_ppc:.3f} px/cm → {out_ppc} px/cm, "
          f"{out.width}×{out.height} px in {len(tiles)} Kachel(n), Raum {room['width_cm']}×{room['height_cm']} cm, "
          f"Bodenband 0…{room['floor']['front_y_cm']} cm")
    return room


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("area_json")
    ap.add_argument("--room", help="nur diesen Raum")
    a = ap.parse_args(argv)
    path = (ROOT / a.area_json) if not Path(a.area_json).is_absolute() else Path(a.area_json)
    area = json.loads(path.read_text(encoding="utf-8"))
    done = 0
    for room in area["rooms"]:
        if "calibration" not in room or (a.room and room["id"] != a.room):
            continue
        out_dir = ROOT / "assets" / "backgrounds" / area["id"]
        calibrate_room(area, room, out_dir, f"res://assets/backgrounds/{area['id']}")
        done += 1
    if not done:
        print("⚠️  kein Raum mit 'calibration' gefunden")
        return 1
    path.write_text(json.dumps(area, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
