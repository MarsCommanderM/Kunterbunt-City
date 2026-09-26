"""Tests für calibrate_bg.py: Arbeitsplatte = 90 cm, Kacheln ≤ 2048 px, Ursprung korrekt."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
pytest.importorskip("PIL")


@pytest.fixture(scope="module")
def calibrated(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("cal")
    for d in ("data", "reference"):
        shutil.copytree(ROOT / d, tmp_path / d)
    (tmp_path / "tools" / "asset_pipeline").mkdir(parents=True)
    shutil.copy(ROOT / "tools/asset_pipeline/calibrate_bg.py", tmp_path / "tools/asset_pipeline")
    r = subprocess.run([sys.executable, str(tmp_path / "tools/asset_pipeline/calibrate_bg.py"),
                        "data/areas/test_kitchen.json"], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stdout + r.stderr
    area = json.loads((tmp_path / "data/areas/test_kitchen.json").read_text(encoding="utf-8"))
    return tmp_path, area["rooms"][0]


def test_counter_is_90cm(calibrated):
    _, room = calibrated
    counter = next(s for s in room["surfaces"] if s["id"] == "counter_top")
    assert abs(counter["h_cm"] - 90) <= 2


def test_floor_band_and_size(calibrated):
    _, room = calibrated
    assert room["floor"]["back_y_cm"] == 0
    assert 50 <= room["floor"]["front_y_cm"] <= 120      # Bodenband-Tiefe laut Maßstab-Bibel §4
    assert room["floor"]["depth_scale_max"] <= 1.12
    assert room["width_cm"] > 600


def test_tiles_within_limit(calibrated):
    from PIL import Image
    root, room = calibrated
    meta = json.loads((root / "assets/backgrounds/test/kitchen.bg.json").read_text(encoding="utf-8"))
    assert meta["tiles"]
    for t in meta["tiles"]:
        w, h = Image.open(root / t["file"].replace("res://", "")).size
        assert w <= 2048 and h <= 2048


def test_counter_pixel_maps_to_minus_90(calibrated):
    root, room = calibrated
    meta = json.loads((root / "assets/backgrounds/test/kitchen.bg.json").read_text(encoding="utf-8"))
    c = room["calibration"]
    k = meta["px_per_cm"] / meta["source_px_per_cm"]
    out_y = (c["px_top"] - c["crop_px"][1]) * k
    world_y = (out_y - meta["origin_px"][1]) / meta["px_per_cm"]
    assert abs(world_y - (-90)) <= 2
