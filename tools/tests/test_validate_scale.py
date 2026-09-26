"""Tests für den Maßstab-Prüfer: grün mit Originaldaten, rot bei falschen Größen."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _copy_project(tmp: Path) -> Path:
    shutil.copytree(ROOT / "data", tmp / "data")
    (tmp / "tools").mkdir()
    shutil.copy(ROOT / "tools" / "validate_scale.py", tmp / "tools")
    return tmp


def _run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(root / "tools" / "validate_scale.py")],
                          capture_output=True, text=True, encoding="utf-8")


def _edit_entry(root: Path, entry_id: str, **changes) -> None:
    p = root / "data" / "scale_table.json"
    table = json.loads(p.read_text(encoding="utf-8"))
    for e in table["entries"]:
        if e["id"] == entry_id:
            e.update(changes)
    p.write_text(json.dumps(table, ensure_ascii=False), encoding="utf-8")


def test_original_data_is_green():
    r = _run(ROOT)
    assert r.returncode == 0, r.stdout + r.stderr


def test_dog_bigger_than_table_is_red(tmp_path):
    root = _copy_project(tmp_path)
    _edit_entry(root, "pet_dog_medium", h_cm=90)
    r = _run(root)
    assert r.returncode == 1
    assert "pet_dog_medium" in r.stdout


def test_apple_as_big_as_football_is_red(tmp_path):
    root = _copy_project(tmp_path)
    _edit_entry(root, "food_apple", h_cm=30)
    r = _run(root)
    assert r.returncode == 1


def test_item_with_unknown_scale_ref_is_red(tmp_path):
    root = _copy_project(tmp_path)
    p = root / "data" / "items" / "home_kitchen_demo.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["items"][0]["scale_ref"] = "gibt_es_nicht"
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    assert _run(root).returncode == 1


def test_item_height_must_match_table(tmp_path):
    root = _copy_project(tmp_path)
    p = root / "data" / "items" / "home_kitchen_demo.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    item = data["items"][0]
    item["size_cm"] = [item["size_cm"][0], item["size_cm"][1] * 2]
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    assert _run(root).returncode == 1
