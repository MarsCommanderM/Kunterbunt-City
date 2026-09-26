"""Platzhalter (P02-T01): einer pro Tabellen-Eintrag, Größe = cm × 8 px, randlos, reproduzierbar."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PH = ROOT / "assets" / "placeholders"
TABLE = json.loads((ROOT / "data" / "scale_table.json").read_text(encoding="utf-8"))["entries"]


def test_one_placeholder_per_entry():
    ids = {e["id"] for e in TABLE}
    files = {p.stem for p in PH.glob("*.png")}
    assert ids == files


def test_size_is_8px_per_cm_or_capped():
    for e in TABLE:
        w_cm, h_cm = float(e.get("w_cm") or e["h_cm"]), float(e["h_cm"])
        img = Image.open(PH / f"{e['id']}.png")
        ppc = min(8.0, 2048 / max(w_cm, h_cm))
        assert abs(img.height - max(6, round(h_cm * ppc))) <= 1, e["id"]
        assert abs(img.width - max(6, round(w_cm * ppc))) <= 1, e["id"]
        # Seitenverhältnis bleibt exakt → Welt-Breite stimmt, wenn über die Höhe skaliert wird
        assert abs(img.width / img.height - w_cm / h_cm) < 0.1 or min(img.size) <= 6, e["id"]


def test_borderless_content_touches_edges():
    for name in ["food_apple", "home_table_dining", "kitchen_plate"]:
        img = Image.open(PH / f"{name}.png").convert("RGBA")
        bbox = img.getchannel("A").getbbox()
        assert bbox == (0, 0, img.width, img.height), name


def test_reproducible(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "tools" / "make_placeholders.py"),
                    "--only", "food_apple,kitchen_plate,pet_dog_medium", "--out", str(tmp_path)], check=True)
    for name in ["food_apple", "kitchen_plate", "pet_dog_medium"]:
        a = hashlib.md5((tmp_path / f"{name}.png").read_bytes()).hexdigest()
        b = hashlib.md5((PH / f"{name}.png").read_bytes()).hexdigest()
        assert a == b, f"{name}: Platzhalter nicht reproduzierbar – tools/make_placeholders.py neu ausführen"
