"""P06-Abnahme – run.py auf der Referenz: dieselben 18 Sprites + JSON wie die Demo.

Beweise (alles in tmp, das Repo bleibt unangetastet):
  * JSON nach dem Lauf **semantisch identisch** mit data/items/home_kitchen_demo.json
    (Gröhen, Griffe, Winkel, Pfade – die 18 Referenz-Einträge).
  * 18 Item-Sprites unter assets/sprites/home-Struktur, Seitenverhältnis ≈ size_cm.
  * Figuren-Sprite + .sprite.json mit hand_grip (0..1).
  * Lineup- und Testszene werden erzeugt (Kamera 1920×1080, Inhalt nicht leer).
  * Falsche Objektanzahl → Exit-Code 1 + Vorschaubild (SplitError-Prüfung).
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "asset_pipeline"))

import run as run_mod  # noqa: E402

REF = ROOT / "reference"
GOLDEN = json.loads((ROOT / "data" / "items" / "home_kitchen_demo.json")
                    .read_text(encoding="utf-8"))
ITEM_IDS = [r["id"] for r in GOLDEN["items"]]


def _roots(tmp: Path) -> dict:
    items = tmp / "items"
    items.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "data" / "items" / "home_kitchen_demo.json", items)
    return dict(items_root=items, sprites_root=tmp / "sprites",
                characters_root=tmp / "chars", lineup_dir=tmp / "lineup",
                scene_dir=tmp / "scene")


def _args(tmp: Path) -> list[str]:
    r = _roots(tmp)
    return ["reference/", "--items-root", str(r["items_root"]),
            "--sprites-root", str(r["sprites_root"]),
            "--characters-root", str(r["characters_root"]),
            "--lineup-dir", str(r["lineup_dir"]),
            "--scene-dir", str(r["scene_dir"])]


def test_full_reference_run(tmp_path):
    rc = run_mod.main(_args(tmp_path))
    assert rc == 0, "run.py reference/ muss durchlaufen"


def test_json_identical_to_reference(tmp_path):
    assert run_mod.main(_args(tmp_path)) == 0
    got = json.loads((_roots(tmp_path)["items_root"] / "home_kitchen_demo.json")
                     .read_text(encoding="utf-8"))
    assert [r["id"] for r in got["items"]] == ITEM_IDS, "Reihenfolge bleibt"

    def strip(recs):   # pad_px ist die einzige Zulage der Pipeline (Vergleich
        return [{k: v for k, v in r.items() if k != "pad_px"}   # darunter)
                for r in recs]
    assert strip(got["items"]) == strip(GOLDEN["items"]), \
        "JSON exakt wie die Referenz (tags/sfx/seat bleiben erhalten)"
    extras = [k for k in ("tags", "sfx", "seat", "surface_frac_y")
              if any(k in r for r in GOLDEN["items"])]
    for key in extras:
        assert any(key in r for r in got["items"]), f"Metadatum '{key}' durfte nicht verloren gehen"
    assert all(r.get("pad_px") == 4 for r in got["items"]), "pad_px: 4 überall"


def test_eighteen_sprites_with_reference_aspect(tmp_path):
    assert run_mod.main(_args(tmp_path)) == 0
    sp = _roots(tmp_path)["sprites_root"] / "home"
    files = sorted(p.stem for p in sp.glob("*.png"))
    assert files == sorted(ITEM_IDS), "genau die 18 Referenz-Items"
    for rec in GOLDEN["items"]:
        img = Image.open(sp / f"{rec['id']}.png")
        want = rec["size_cm"][0] / rec["size_cm"][1]
        got = (img.width - 8) / (img.height - 8)   # 4 px Padding je Seite
        assert abs(got - want) / want < 0.02, \
            f"{rec['id']}: Seitenverhältnis {got:.3f} ≠ {want:.3f}"


def test_character_export_with_hand_grip(tmp_path):
    assert run_mod.main(_args(tmp_path)) == 0
    r = _roots(tmp_path)
    png = r["characters_root"] / "char_girl_01.png"
    side = r["characters_root"] / "char_girl_01.sprite.json"
    assert png.exists() and side.exists()
    rec = json.loads(side.read_text(encoding="utf-8"))
    assert rec["size_cm"][1] == 125, "Kind = 125 cm (char_child)"
    gx, gy = rec["hand_grip"]
    assert 0.0 <= gx <= 1.0 and 0.0 <= gy <= 1.0
    assert (png.exists()), "Figuren-Sprite geschrieben"


def test_lineup_and_scene_generated(tmp_path):
    assert run_mod.main(_args(tmp_path)) == 0
    r = _roots(tmp_path)
    lineup = r["lineup_dir"] / "lineup_home.png"
    assert lineup.exists() and Image.open(lineup).width > 800
    scene = r["scene_dir"] / "scene_test.png"
    cam = r["scene_dir"] / "scene_test_kamera.png"
    assert scene.exists() and cam.exists()
    assert Image.open(cam).size == (1920, 1080)
    px = Image.open(scene).convert("RGB")
    colors = set()
    for x in range(0, px.width, 17):
        for y in range(0, px.height, 17):
            colors.add(px.getpixel((x, y)))
    assert len(colors) > 200, "Szene ist nicht leer/farblos"


def test_wrong_object_count_fails(tmp_path):
    # Blatt mit EINEM Item weniger → Anzahl ≠ YAML → Fehler + Vorschau
    dst = tmp_path / "blätter"
    dst.mkdir()
    shutil.copy(REF / "raw_items.png", dst)
    spec = (REF / "raw_items.yaml").read_text(encoding="utf-8")
    lines = [l for l in spec.splitlines()
             if "flower_tulip_yellow_pot" not in l]
    (dst / "raw_items.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    r = _roots(tmp_path)
    rc = run_mod.main([str(dst), "--items-root", str(r["items_root"]),
                       "--sprites-root", str(r["sprites_root"]),
                       "--characters-root", str(r["characters_root"]),
                       "--no-lineup", "--no-scene"])
    assert rc == 1
    previews = list(dst.glob("*_split_preview.png"))
    assert previews, "Vorschaubild der gefundenen Objekte wird erzeugt"
