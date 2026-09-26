"""P06-T04/T05 – points.py & export.py: Grip-Defaults, Hand-Grip, 8 px/cm, Upsert.

Beweise:
  * Kategorie-Defaults (Tasse → Henkel rechts 45 %), YAML-Override gewinnt.
  * Figuren-Hand-Grip über Hautfarbe; Vorschaubild mit blau/roten Markern.
  * Zielmaß 8 px/cm, kleine Items ≥ 64 px Kantenlänge, 4 px Padding.
  * Upsert: bestehende ID ersetzt an Ort und Stelle, neue angehängt – kein Duplikat.
  * Record-Format == Referenz-Format (data/items/home_kitchen_demo.json).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "asset_pipeline"))

from export import (  # noqa: E402
    build_record,
    export_sprite,
    sprite_res_path,
    target_px,
    upsert_items,
)
from points import find_hand_grip, points, preview  # noqa: E402

MUG = {"category": "kitchen", "hold": "one_hand", "h_cm": 10, "w_cm": 8, "placement": "table"}
CHAIR = {"category": "furniture", "hold": "none", "h_cm": 90, "w_cm": 45, "placement": "floor"}


# ------------------------------------------------------------------ points
def test_furniture_has_pivot_but_no_grip():
    p = points({}, CHAIR)
    assert p["pivot"] == [0.5, 1.0]
    assert p["grip"] is None and p["hold"] == "none"


def test_kitchen_grip_is_handle_right_45():
    p = points({}, MUG)
    assert p["grip"] == [0.9, 0.45]
    assert p["hold"] == "one_hand"


def test_yaml_override_wins():
    p = points({"grip": [0.1, 0.5], "pivot": [0.5, 0.9],
                "hold": "two_hands", "hold_angle": -20}, MUG)
    assert p == {"pivot": [0.5, 0.9], "grip": [0.1, 0.5],
                 "hold": "two_hands", "hold_angle": -20}


def test_find_hand_grip_top_right_skin():
    im = Image.new("RGBA", (400, 800), (40, 40, 60, 255))          # Körper dunkel
    d = ImageDraw.Draw(im)
    d.ellipse([300, 60, 360, 120], fill=(230, 180, 150, 255))       # Faust oben rechts
    gx, gy = find_hand_grip(im)
    assert 0.62 < gx < 1.0 and 0.0 < gy < 0.62


def test_preview_marks_pivot_and_grip(tmp_path):
    im = Image.new("RGBA", (200, 200), (60, 160, 60, 255))
    out = preview(im, {"pivot": [0.5, 1.0], "grip": [0.9, 0.45]}, tmp_path / "p.png")
    assert out.exists()
    px = Image.open(out).load()
    red = any(px[x, y][0] > 180 and px[x, y][1] < 90 and px[x, y][2] < 90
              for x in range(165, 196) for y in range(73, 108))
    blue = any(px[x, y][2] > 180 and px[x, y][0] < 90
               for x in range(87, 114) for y in range(185, 200))
    assert red, "roter Grip-Marker (Ring)"
    assert blue, "blaues Pivot-Kreuz"


# ------------------------------------------------------------------ export
def test_target_px_density():
    assert target_px([10, 10]) == (80, 80, 8.0)


def test_target_px_small_item_gets_64px_edge():
    w, h, density = target_px([6, 6])
    assert min(w, h) >= 64
    assert density > 8


def test_export_sprite_padding_and_size(tmp_path):
    im = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([10, 10, 90, 90], fill=(200, 40, 40, 255))
    out = export_sprite(im, [10, 10], "test_apple", "test_area", sprites_root=tmp_path)
    got = Image.open(out)
    assert got.size == (80 + 8, 80 + 8), "8 px/cm + 2×4 px Padding"
    assert got.getpixel((0, 0))[3] == 0, "Ecke transparent"
    assert got.getpixel((got.width // 2, got.height // 2))[3] == 255


def test_sprite_res_path():
    assert sprite_res_path("home", "food_carrot") == "res://assets/sprites/home/food_carrot.png"


def test_build_record_matches_reference_format():
    spec = {"id": "home_cup_orange_dots", "scale_ref": "kitchen_mug",
            "scale_mul": 0.9, "placement": "table"}
    rec = build_record(spec, [8.1, 9.0], points({"grip": [0.5, 0.55]}, MUG), "home")
    ref = json.loads((ROOT / "data" / "items" / "home_kitchen_demo.json")
                     .read_text(encoding="utf-8"))
    ref_rec = next(r for r in ref["items"] if r["id"] == "home_cup_orange_dots")
    assert set(rec) - {"pad_px"} == set(ref_rec) - {"pad_px"}, \
        "Schlüssel entsprechen der Referenz"
    assert rec["pad_px"] == 4, "4 px Padding werden im JSON gemeldet"
    assert {k: v for k, v in rec.items() if k != "pad_px"} == \
           {k: v for k, v in ref_rec.items() if k != "pad_px"}, \
        "Record identisch zur Referenz (inkl. size_cm & scale_mul)"


def test_upsert_replaces_in_place_and_appends(tmp_path):
    p = tmp_path / "items.json"
    p.write_text(json.dumps({"area": "home", "room": "kitchen", "items": [
        {"id": "a", "size_cm": [1, 1]},
        {"id": "b", "size_cm": [2, 2]},
    ]}), encoding="utf-8")
    changed = upsert_items(
        [{"id": "b", "size_cm": [9, 9]}, {"id": "c", "size_cm": [3, 3]}],
        area="home", room="kitchen", items_path=p)
    data = json.loads(p.read_text(encoding="utf-8"))
    assert changed == ["b", "c"]
    assert [r["id"] for r in data["items"]] == ["a", "b", "c"], "Reihenfolge bleibt"
    assert data["items"][1]["size_cm"] == [9, 9], "b ersetzt an Ort und Stelle"
    assert len({r["id"] for r in data["items"]}) == 3, "keine Dubletten"


def test_upsert_creates_new_file(tmp_path):
    p = tmp_path / "neu.json"
    upsert_items([{"id": "x", "size_cm": [1, 2]}], area="zoo", room="savanne",
                 items_path=p)
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["area"] == "zoo" and len(data["items"]) == 1
