#!/usr/bin/env python3
"""Erzeugt data/items/test_kitchen_placeholders.json – 43 Platzhalter-Items für die Test-Küche (P02-T10).
Größen/Seitenverhältnis exakt aus scale_table.json → validate_scale.py bleibt grün. Reproduzierbar."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
T = {e["id"]: e for e in json.loads((ROOT / "data/scale_table.json").read_text(encoding="utf-8"))["entries"]}

SPEC = [  # (item_id, scale_ref, extra)
    *[(f"food_{n}", f"food_{n}", {}) for n in
      ["banana", "tomato", "bread_loaf", "toast", "cheese", "milk_carton", "juice_bottle", "pizza", "cake", "cupcake", "watermelon"]],
    *[(f"kitchen_plate_{i}", "kitchen_plate", {"tags": ["stackable"]}) for i in range(1, 5)],
    *[(f"kitchen_bowl_{i}", "kitchen_bowl", {"tags": ["stackable"]}) for i in range(1, 3)],
    *[(f"kitchen_{n}", f"kitchen_{n}", {}) for n in
      ["mug", "glass", "pan", "pot", "cutting_board", "spoon", "toaster", "kettle", "microwave"]],
    *[(f"toy_block_{i}", "toy_block", {"tags": ["stackable"]}) for i in range(1, 5)],
    ("toy_car_small", "toy_car_small", {}), ("toy_basketball", "toy_basketball", {}), ("toy_doll", "toy_doll", {}),
    *[(f"item_book_{i}", "item_book", {"tags": ["stackable"]}) for i in range(1, 3)],
    ("item_crayon", "item_crayon", {}),
    ("item_backpack", "item_backpack", {"container": {"slots": 6, "max_item_h_cm": 25}}),
    ("item_watering_can", "item_watering_can", {}),
    ("item_bucket", "item_bucket", {"container": {"slots": 4, "max_item_h_cm": 20}}),
    ("item_vase_bouquet", "item_vase_bouquet", {}),
    ("fix_fridge", "fix_fridge", {"movable": False, "container": {"slots": 12, "max_item_h_cm": 40},
                                  "sfx": {"open": "open", "close": "close"}}),
    ("home_stool", "home_stool", {"surface_h_cm": 45}),
    ("home_table_coffee", "home_table_coffee", {}),
    # Phase 03: Sitz-/Liegeplätze und ein zweites Tier
    ("home_sofa", "home_sofa", {"seat": {"pose": "sit", "slots": 3}}),
    ("home_armchair", "home_armchair", {"seat": {"pose": "sit", "slots": 1}}),
    ("home_bed_kid", "home_bed_kid", {"seat": {"pose": "lie", "slots": 1}}),
    ("pet_cat", "pet_cat", {"grip": [0.5, 0.45], "sfx": {"voice": "pet_cat_meow"}}),
]

items = []
for iid, ref, extra in SPEC:
    e = T[ref]
    it = {"id": iid, "scale_ref": ref, "size_cm": [e.get("w_cm", e["h_cm"]), e["h_cm"]],
          "pivot": [0.5, 1.0], "hold": e["hold"], "placement": e["placement"]}
    if e["hold"] != "none":
        it["grip"] = [0.5, 0.5]
    it.update(extra)
    items.append(it)
out = {"area": "test", "room": "kitchen", "note": "Platzhalter – erzeugt von tools/dev/make_test_items.py", "items": items}
(ROOT / "data/items/test_kitchen_placeholders.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"✅ {len(items)} Test-Items")
