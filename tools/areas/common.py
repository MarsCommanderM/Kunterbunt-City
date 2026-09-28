"""Gemeinsame Bausteine für die Bereichs-Dateien (tools/make_areas.py): Item-Einträge, Räume, Prüfung."""
from __future__ import annotations

import glob
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FLOOR = {"depth_scale_max": 1.12, "back_y_cm": 0.0, "front_y_cm": 70.0}
CAM_IN = {"default_h_cm": 300, "min_h_cm": 220, "max_h_cm": 420}
DOOR_TOP = -206.8                       # Wand-Items: y = Oberkante (Tür 206,8 cm hoch steht auf dem Boden)


def F(id_: str, x: float, y: float = 20.0, **kw) -> dict:
    return {"id": id_, "x_cm": x, "y_cm": y, **kw}


def W(id_: str, x: float, top: float) -> dict:
    return {"id": id_, "x_cm": x, "y_cm": top}


def ON(id_: str, host: str, x_rel: float = 0.0) -> dict:
    return {"id": id_, "on": host, "x_rel": x_rel}


def shop(rid: str, label: str, icon: str, decor: dict, items: list, width: float = 800, area: str = "shopping",
         door: bool = True, amb: str = "amb_indoor", height: float = 260.0, cam: dict | None = None) -> dict:
    return {"id": rid, "label": label, "icon": icon, "width_cm": width, "height_cm": height, "floor": FLOOR, "camera": cam or CAM_IN,
            "background": f"res://assets/backgrounds/{area}/{rid}.bg.json",
            "scene": {"kind": "indoor", "wainscot": True, "extras": [], "decor": decor},
            "default_items": ([W("door_glass_white", 70, DOOR_TOP)] if door else []) + items, "ambience": amb}


def outdoor(area: str, rid: str, label: str, icon: str, width: float, items: list, floor: str, cols: list, seed: int,
            town: list | None = None, height: float = 560.0, cam: dict | None = None, amb: str = "amb_garden") -> dict:
    sc = {"kind": "outdoor", "seed": seed, "decor": {"floor": floor, "floor_cols": cols}}
    if town:
        sc["town"] = town
    return {"id": rid, "label": label, "icon": icon, "width_cm": width, "height_cm": height, "floor": FLOOR,
            "camera": cam or {"default_h_cm": 400, "min_h_cm": 220, "max_h_cm": 600},
            "background": f"res://assets/backgrounds/{area}/{rid}.bg.json", "scene": sc, "default_items": items, "ambience": amb}


def deco(wall: list, pattern: str, pcol: str, floor: str, fcols: list) -> dict:
    return {"wall": wall, "pattern": pattern, "pattern_col": pcol, "floor": floor, "floor_cols": fcols}


def check(area: dict, npcs: dict) -> list[str]:
    ids = set()
    for f in glob.glob(str(ROOT / "data/items/*.json")):
        ids.update(i["id"] for i in json.loads(Path(f).read_text(encoding="utf-8"))["items"])
    roles = {Path(p).stem for p in glob.glob(str(ROOT / "data/npc_roles/*.json"))}
    bad = []
    for r in area["rooms"]:
        for e in r["default_items"]:
            if e["id"] not in ids:
                bad.append(f"{r['id']}: Item {e['id']}")
        if r.get("icon") not in ids:
            bad.append(f"{r['id']}: Symbol {r.get('icon')}")
    rids = {r["id"] for r in area["rooms"]}
    for n in npcs["npcs"]:
        if n["role"] not in roles:
            bad.append(f"NPC {n['id']}: Rolle {n['role']}")
        if n["room"] not in rids:
            bad.append(f"NPC {n['id']}: Raum {n['room']}")
    return bad
