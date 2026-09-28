"""Item-IDs sind sauber (nur a–z, 0–9, _) – keine Farbcodes wie „_#b8b2a7" in IDs. Umbenennungen stehen in
data/item_aliases.json und zeigen auf existierende Items (R-11)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _ids() -> set[str]:
    out: set[str] = set()
    for p in (ROOT / "data" / "items").glob("*.json"):
        out.update(it["id"] for it in json.loads(p.read_text(encoding="utf-8"))["items"])
    return out


def test_item_ids_are_clean():
    bad = sorted(i for i in _ids() if not re.fullmatch(r"[a-z0-9_]+", i))
    assert not bad, f"unsaubere IDs: {bad[:10]}"


def test_aliases_point_to_existing_items():
    ids = _ids()
    aliases = json.loads((ROOT / "data" / "item_aliases.json").read_text(encoding="utf-8"))["aliases"]
    for old, new in aliases.items():
        assert new in ids, f"{old} → {new} fehlt"
        assert old not in ids, f"{old} existiert noch"
