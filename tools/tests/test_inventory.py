"""Ist wirklich alles da? Jeder Eintrag in data/inventory.json braucht genug Varianten im Katalog."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def catalog_ids() -> list[str]:
    ids: list[str] = []
    for g in json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))["groups"]:
        ids += g["items"]
    return ids


def missing() -> list[str]:
    ids = catalog_ids()
    out = []
    inv = json.loads((ROOT / "data/inventory.json").read_text(encoding="utf-8"))
    for area, rooms in inv["areas"].items():
        for room, entries in rooms.items():
            for e in entries:
                n = sum(1 for i in ids if i.startswith(e["prefix"]))
                if n < e["min"]:
                    out.append(f"{area}/{room}: {e['label']} ({e['prefix']}) {n}/{e['min']}")
    return out


def test_inventory_is_complete():
    m = missing()
    assert m == [], f"{len(m)} fehlen:\n" + "\n".join(m)


if __name__ == "__main__":
    m = missing()
    print("\n".join(m) or "✅ alles da")
    print(f"{len(m)} fehlen")
