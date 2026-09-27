"""P06-T06/T11 – atlas.py & figure_parts.py: Packen ≤4096², Differenz-Teile, parts.json.

Beweise:
  * Atlas: alle Regionen drin, keine Überlappung, Pixel am richtigen Ort,
    Limit erzwingbar (Fehler statt Überlauf).
  * Differenz: nur geänderte Pixel werden Teil-Ebene; Rauschen < Threshold bleibt.
  * Freistell-Modus ohne Schablone; Anker von unten-links wie im Rig.
  * save_part: PNG + parts.json-Upsert (kein Dublikat, Fremd-Felder bleiben).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "asset_pipeline"))

from atlas import AtlasError, build_area, pack  # noqa: E402
from figure_parts import (  # noqa: E402
    PartError,
    diff_layer,
    extract_part,
    save_part,
)


def _sprites():
    return {
        "a": Image.new("RGBA", (120, 300), (200, 30, 30, 255)),
        "b": Image.new("RGBA", (90, 90), (30, 200, 30, 255)),
        "c": Image.new("RGBA", (400, 60), (30, 30, 200, 255)),
        "d": Image.new("RGBA", (64, 64), (200, 200, 30, 255)),
    }


# ------------------------------------------------------------------ atlas
def test_pack_regions_valid_nonoverlap():
    atlas, regions = pack(_sprites(), max_size=1024)
    assert atlas.size == (1024, 1024)
    assert set(regions) == {"a", "b", "c", "d"}
    boxes = {k: (v["x"], v["y"], v["x"] + v["w"], v["y"] + v["h"])
             for k, v in regions.items()}
    for k, (x0, y0, x1, y1) in boxes.items():
        assert 0 <= x0 < x1 <= 1024 and 0 <= y0 < y1 <= 1024, k
    keys = list(boxes)
    for i, k1 in enumerate(keys):
        for k2 in keys[i + 1:]:
            a, b = boxes[k1], boxes[k2]
            overlap = not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
            assert not overlap, f"{k1} überlappt {k2}"
    px = atlas.load()
    for name, im in _sprites().items():
        r = regions[name]
        assert px[r["x"] + 1, r["y"] + 1] == im.getpixel((0, 0)), name


def test_pack_limit_raises():
    try:
        pack(_sprites(), max_size=200)
        raise AssertionError("AtlasError erwartet")
    except AtlasError as e:
        assert "Limit" in str(e) or "größer" in str(e)


def test_build_area_writes_png_and_json(tmp_path):
    src = tmp_path / "home"
    src.mkdir()
    for name, im in _sprites().items():
        im.save(src / f"{name}.png")
    png, js = build_area("home", sprites_root=tmp_path)
    assert png.exists() and js.exists()
    data = json.loads(js.read_text(encoding="utf-8"))
    assert data["area"] == "home"
    assert len(data["regions"]) == 4
    assert Image.open(png).size == tuple(data["size"])


def test_pack_empty_raises():
    try:
        pack({})
        raise AssertionError("AtlasError erwartet")
    except AtlasError:
        pass


# ---------------------------------------------------------- figure_parts
def _figure(color, square=None) -> Image.Image:
    im = Image.new("RGBA", (200, 200), color)
    if square:
        ImageDraw.Draw(im).rectangle(square, fill=(255, 255, 0, 255))
    return im


def test_diff_layer_keeps_only_change():
    base = _figure((30, 160, 60, 255))
    neu = _figure((30, 160, 60, 255), square=(40, 40, 80, 80))
    layer = diff_layer(neu, base)
    px = layer.load()
    assert px[60, 60][3] == 255, "geänderte Pixel bleiben"
    assert px[150, 150][3] == 0, "unverändert wird transparent"
    assert px[10, 10][3] == 0


def test_diff_threshold_filters_noise():
    base = _figure((30, 160, 60, 255))
    neu = _figure((38, 160, 60, 255))   # Distanz 8 < 24
    layer = diff_layer(neu, base, threshold=24)
    assert layer.getchannel("A").getbbox() is None, "Rauschen unter Threshold"


def test_diff_new_content_on_transparent_base_is_kept():
    base = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    neu = _figure((30, 160, 60, 255), square=(10, 10, 60, 60))
    layer = diff_layer(neu, base)
    assert layer.getpixel((30, 30))[3] == 255


def test_diff_size_mismatch_raises():
    try:
        diff_layer(Image.new("RGBA", (10, 10)), Image.new("RGBA", (11, 10)))
        raise AssertionError("PartError erwartet")
    except PartError:
        pass


def test_extract_without_base_uses_cutout():
    im = Image.new("RGBA", (300, 300), (255, 255, 255, 255))
    ImageDraw.Draw(im).ellipse([100, 60, 220, 180], fill=(200, 40, 40, 255))
    layer, meta = extract_part(im)
    # Weichzeichner der Kanten-Entmischung: Box max. +3 px größer als Inhalt
    assert 117 <= layer.width <= 124 and 117 <= layer.height <= 124
    assert abs(meta["w_cm"] - layer.width / 8) < 0.001, "cm = px / 8"
    assert 14.5 <= meta["w_cm"] <= 15.5
    assert abs(meta["anchor_cm"][0] - meta["w_cm"] / 2) < 0.01, "Default-Anker = Mitte"
    assert abs(meta["anchor_cm"][1] - meta["h_cm"] / 2) < 0.01


def test_extract_explicit_anchor_from_bottom_left():
    im = Image.new("RGBA", (300, 300), (255, 255, 255, 255))
    ImageDraw.Draw(im).rectangle([0, 0, 79, 159], fill=(40, 40, 200, 255))
    layer, meta = extract_part(im, anchor_cm=[5.0, 20.0])
    assert meta["anchor_cm"] == [5.0, 20.0], "Anker bleibt exakt wie übergeben"
    assert 78 <= layer.width <= 84 and 157 <= layer.height <= 164
    assert abs(meta["w_cm"] - layer.width / 8) < 0.001


def test_extract_identical_to_base_raises():
    base = _figure((30, 160, 60, 255))
    try:
        extract_part(base, base)
        raise AssertionError("PartError erwartet (leere Differenz)")
    except PartError as e:
        assert "leer" in str(e)


def test_save_part_upserts_and_keeps_foreign_fields(tmp_path):
    (tmp_path / "kid").mkdir()
    jp = tmp_path / "parts.json"
    jp.write_text(json.dumps({"kid": {"old_part": {"w_cm": 1, "h_cm": 1,
                                                   "anchor_cm": [0.5, 0.5],
                                                   "note": "Bewahrtes"}},
                              "adult": {"x": {"w_cm": 2, "h_cm": 2,
                                              "anchor_cm": [1, 1]}}}, indent=1),
                  encoding="utf-8")
    layer = Image.new("RGBA", (80, 80), (90, 90, 200, 255))
    meta = {"w_cm": 10.0, "h_cm": 10.0, "anchor_cm": [5.0, 10.0]}
    save_part("hair_front_test", layer, meta, "kid",
              parts_root=tmp_path, parts_json=jp)
    save_part("hair_front_test", layer, {**meta, "w_cm": 12.0}, "kid",
              parts_root=tmp_path, parts_json=jp)
    data = json.loads(jp.read_text(encoding="utf-8"))
    assert list(data["kid"]) == ["old_part", "hair_front_test"], "kein Dublikat"
    assert data["kid"]["hair_front_test"]["w_cm"] == 12.0, "zweite Ablage aktualisiert"
    assert data["kid"]["old_part"]["note"] == "Bewahrtes", "Fremd-Feld bleibt"
    assert data["adult"]["x"]["w_cm"] == 2, "andere Schablone unberührt"
    assert (tmp_path / "kid" / "hair_front_test.png").exists()
