#!/usr/bin/env python3
"""
Item-Bibliothek erzeugen (P04b-T09) – Vektor-Zeichnung im Stil der Figuren, 0 €, bit-genau reproduzierbar.

Liest den Katalog (tools/items/catalog.py) und schreibt:
    assets/sprites/items/<vorlage>.png     1 Sprite je Vorlage (Farbzonen in R/G/B, Rest = Tinte)
    data/items/catalog_<gruppe>.json      1 Item je Farbvariante (gleiches Sprite, andere "colors")
    data/scale_table.json                 Maßstab-Einträge der Vorlagen (Upsert, gemessen aus der Zeichnung)
    data/catalog.json                     Katalog-Reiter (Gruppe → Symbol → Items) für das Spiel
Bestehende Items mit `legacy`-ID behalten ID + Maßstab-Eintrag und bekommen nur Sprite + Farben.

Aufruf: python3 tools/make_items.py [--jobs 4] [--only plants] [--sheet out.png]
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from items.catalog import TEMPLATES  # noqa: E402
from items.kit import Item  # noqa: E402

PPC = 8.0
PAD_PX = 1
SPRITE_DIR = ROOT / "assets" / "sprites" / "items"
ITEMS_DIR = ROOT / "data" / "items"
GROUPS = {  # Reihenfolge + Symbol im Katalog
    "sofas": "cat_sofas", "chairs": "cat_chairs", "tables": "cat_tables", "beds": "cat_beds",
    "storage": "cat_storage", "lamps": "cat_lamps", "electronics": "cat_electronics", "plants": "cat_plants",
    "kitchen": "cat_kitchen", "food": "cat_food", "bath": "cat_bath", "deco": "cat_deco", "toys": "cat_toys",
    "pool": "cat_pool", "garden": "cat_garden", "camping": "cat_camping", "playground": "cat_playground",
    "bikes": "cat_bikes", "school": "cat_school", "sport": "cat_sport", "health": "cat_health",
    "workshop": "cat_workshop", "shop": "cat_shop", "hairdresser": "cat_hairdresser", "fair": "cat_fair", "winter": "cat_winter", "animals": "cat_animals",
}


def _render(i: int):
    t = TEMPLATES[i]
    it = Item(float(t["w"]), float(t["h"]), PPC)
    t["fn"](it, **t["kw"])
    img, info = it.finish()
    return t["id"], img, info


def scale_ref(t: dict) -> str:
    """Maßstab-ID: bestehende (legacy) behalten, sonst eigener Namensraum „c_“ – nie handgepflegte Einträge treffen."""
    return t.get("legacy") or "c_" + t["id"]


def _scale_entry(t: dict, w_cm: float, h_cm: float) -> dict:
    e = {"id": scale_ref(t), "category": t["category"], "h_cm": round(h_cm, 1), "w_cm": round(w_cm, 1),
         "hold": t["hold"], "placement": t["placement"], "src": "catalog"}
    if t.get("seat"):
        e["seat_h_cm"] = t["seat"]["h"]
    if t.get("surface_h"):
        e["surface_h_cm"] = round(min(float(t["surface_h"]), h_cm), 1)
    return e


def _item(t: dict, iid: str, ref: str, colors: list, size: tuple, sprite: str) -> dict:
    d = {"id": iid, "scale_ref": ref, "size_cm": [round(size[0], 1), round(size[1], 1)], "pivot": [0.5, 1.0],
         "hold": t["hold"], "placement": t["placement"], "movable": True, "sprite": sprite, "pad_px": PAD_PX,
         "colors": colors, "catalog": t["group"]}
    if t.get("grip"):
        d["grip"] = t["grip"]
    if t.get("seat"):
        d["seat"] = {"pose": t["seat"]["pose"], "slots": t["seat"].get("slots", 1)}
    if t.get("container"):
        d["container"] = t["container"]
    if t.get("tags"):
        d["tags"] = t["tags"]
    return d


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="", help="nur diese Gruppe(n), Komma-getrennt")
    a = ap.parse_args(argv)
    only = [s for s in a.only.split(",") if s]
    todo = [i for i, t in enumerate(TEMPLATES) if not only or t["group"] in only]
    SPRITE_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.jobs) as pool:
        rendered = {tid: (img, info) for tid, img, info in pool.map(_render, todo, chunksize=4)}
    print(f"  {len(rendered)} Vorlagen gezeichnet ({time.time() - t0:.0f} s)")

    table_path = ROOT / "data" / "scale_table.json"
    table = json.loads(table_path.read_text(encoding="utf-8"))
    entries = {e["id"]: e for e in table["entries"]}
    by_group: dict[str, list] = {}
    legacy_updates: dict[str, dict] = {}
    for i in todo:
        t = TEMPLATES[i]
        img, info = rendered[t["id"]]
        img.save(SPRITE_DIR / f"{t['id']}.png", optimize=True)
        pad = PAD_PX / PPC
        w_cm, h_cm = info["w_cm"] - 2 * pad, info["h_cm"] - 2 * pad
        ref = scale_ref(t)
        old = entries.get(ref)
        if old is None or old.get("src") == "catalog" or abs(old["h_cm"] - h_cm) / old["h_cm"] > 0.05:
            ne = _scale_entry(t, w_cm, h_cm)
            if old is not None and old.get("src") != "catalog":   # Hand-Einträge: Notizen, Sitz-/Flächenhöhe behalten (Notizen, Sitz-/Flächenhöhe der Tabelle)
                keep = {k: v for k, v in old.items() if k not in ("h_cm", "w_cm")}
                ne = {**ne, **keep, "h_cm": ne["h_cm"], "w_cm": ne["w_cm"]}
            entries[ref] = ne
        h_tab = entries[ref]["h_cm"]
        sprite = f"res://assets/sprites/items/{t['id']}.png"
        for suffix, colors in t["variants"]:
            iid = f"{t['id']}_{suffix}"
            by_group.setdefault(t["group"], []).append(_item(t, iid, ref, colors, (w_cm * h_tab / h_cm, h_tab), sprite))
        if t.get("legacy"):
            legacy_updates[t["legacy"]] = {"sprite": sprite, "pad_px": PAD_PX, "colors": t["variants"][0][1],
                                           "size_cm": [round(w_cm * h_tab / h_cm, 1), h_tab], "catalog": t["group"]}
    if not only:   # Voll-Lauf: veraltete Katalog-Einträge entfernen
        produced = {scale_ref(TEMPLATES[i]) for i in todo}
        entries = {k: e for k, e in entries.items() if e.get("src") != "catalog" or k in produced}
    table["entries"] = list(entries.values())
    table_path.write_text(json.dumps(table, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    n_items = 0
    for g, items in by_group.items():
        path = ITEMS_DIR / f"catalog_{g}.json"
        doc = {"area": "catalog", "room": g, "note": "erzeugt von tools/make_items.py – nicht von Hand ändern",
               "items": items}
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        n_items += len(items)
    # Bestehende Items (Tests, Räume) bekommen die neue Grafik – ID und Maßstab bleiben
    for path in sorted(glob.glob(str(ITEMS_DIR / "*.json"))):
        if Path(path).name.startswith("catalog_"):
            continue
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
        changed = False
        for it in doc.get("items", []):
            if it.get("id") in legacy_updates:
                it.update(legacy_updates[it["id"]])
                changed = True
        if changed:
            Path(path).write_text(json.dumps(doc, ensure_ascii=False) + "\n", encoding="utf-8")
    # Katalog-Reiter (alle Gruppen, auch von früheren Läufen)
    groups = []
    for g, icon in GROUPS.items():
        path = ITEMS_DIR / f"catalog_{g}.json"
        if not path.exists():
            continue
        ids = [it["id"] for it in json.loads(path.read_text(encoding="utf-8"))["items"]]
        groups.append({"id": g, "icon": icon, "items": ids})
    (ROOT / "data" / "catalog.json").write_text(json.dumps(
        {"_doc": "Katalog-Reiter (P04b-T09): jedes Item ist in jedem Raum einsetzbar. Erzeugt von tools/make_items.py.",
         "groups": groups}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(len(g["items"]) for g in groups)
    print(f"✅ {len(todo)} Vorlagen · {n_items} Items in diesem Lauf · Katalog gesamt {total} Items in {len(groups)} Gruppen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
