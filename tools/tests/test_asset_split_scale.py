"""P06-T02/T03 – split.py & scale.py: Lesereihenfolge, Anzahl-Prüfung, Maßstabs-Rechnung.

Beweise (synthetische Blätter, reproduzierbar):
  * Zeilen werden über die vertikale Mitte gebildet – Reihenfolge ro→gr→bl→ge.
  * Kleinstflöhe (< min_area) werden ignoriert.
  * Anzahl ≠ YAML → SplitError mit nummeriertem Vorschaubild.
  * size_cm = Tabellen-Höhe × scale_mul, Breite aus dem Seitenverhältnis.
  * > 30 % Abweichung (tolerance_aspect) → Warnung; unbekanntes scale_ref → Fehler.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "asset_pipeline"))

from scale import ScaleError, load_table, resolve  # noqa: E402
from split import SplitError, split, split_sheet, trim  # noqa: E402

RED = (200, 40, 40)
GREEN = (40, 180, 60)
BLUE = (40, 80, 200)
YELLOW = (230, 200, 40)


def _sheet(shapes, size=(700, 500)) -> Image.Image:
    im = Image.new("RGB", size, "white")
    d = ImageDraw.Draw(im)
    for kind, box, color in shapes:
        if kind == "circle":
            d.ellipse(box, fill=color)
        else:
            d.rectangle(box, fill=color)
    return im


def _color_name(img: Image.Image) -> str:
    r, g, b = img.getpixel((img.width // 2, img.height // 2))[:3]
    if r > 150 and g < 120 and b < 120:
        return "red"
    if g > 150 and r < 120:
        return "green"
    if b > 150 and r < 120:
        return "blue"
    if r > 180 and g > 150 and b < 120:
        return "yellow"
    return f"?{r},{g},{b}"


# --------------------------------------------------------------- split (T02)
def _two_rows(extra_junk=False):
    shapes = [
        ("circle", [55, 55, 145, 145], RED),      # Zeile 1 links
        ("rect", [260, 60, 340, 140], GREEN),      # Zeile 1 rechts
        ("circle", [55, 255, 145, 345], BLUE),     # Zeile 2 links
        ("rect", [260, 260, 340, 340], YELLOW),    # Zeile 2 rechts
    ]
    if extra_junk:
        shapes.append(("circle", [560, 420, 576, 436], (120, 120, 120)))  # ~80 px
    return _sheet(shapes)


def test_reading_order_rows_then_left_to_right():
    from cutout import cutout
    rgba, fg = cutout(_two_rows())
    parts = [trim(p) for p in split(rgba, fg)]
    assert [_color_name(p) for p in parts] == ["red", "green", "blue", "yellow"]


def test_junk_below_min_area_ignored():
    from cutout import cutout
    rgba, fg = cutout(_two_rows(extra_junk=True))
    parts = split(rgba, fg)
    assert len(parts) == 4, "Kleinstfläche darf nicht als Objekt durchgehen"


def test_split_sheet_ok_returns_trimmed(tmp_path):
    p = tmp_path / "blatt.png"
    _two_rows().save(p)
    parts = split_sheet(p, ["a", "b", "c", "d"], tmp_path)
    assert len(parts) == 4
    for img in parts:
        assert img.mode == "RGBA"
        # trimmbar: keine transparenten Ränder mehr
        a = img.getchannel("A")
        assert a.getpixel((0, 0)) > 10 or a.getbbox() == (0, 0, img.width, img.height)


def test_count_mismatch_raises_with_preview(tmp_path):
    p = tmp_path / "blatt.png"
    _two_rows().save(p)
    try:
        split_sheet(p, ["a", "b", "c"], tmp_path)
        raise AssertionError("SplitError erwartet")
    except SplitError as e:
        assert "4 Objekte gefunden, 3 erwartet" in str(e)
        assert e.preview is not None and Path(e.preview).exists()
        prev = Image.open(e.preview)
        assert prev.size[0] > 100  # Vorschaubild ist da und nicht leer


# --------------------------------------------------------------- scale (T03)
def _table(tol=0.3):
    return {"apple": {"id": "apple", "h_cm": 8, "w_cm": 4}}, tol


def test_size_from_table_and_aspect():
    r = resolve({"scale_ref": "apple"}, 40, 80, _table())  # aspect 0.5 = Tabellen-Seite
    assert r["size_cm"] == [4.0, 8.0]
    assert r["warnings"] == []


def test_scale_mul_scales_height():
    r = resolve({"scale_ref": "apple", "scale_mul": 0.9}, 40, 80, _table())
    assert r["size_cm"][1] == 7.2
    assert r["size_cm"][0] == 3.6


def test_wide_sprite_warns_over_30_percent():
    r = resolve({"scale_ref": "apple"}, 80, 80, _table())  # w_cm 8 statt 4 → +100 %
    assert r["size_cm"] == [8.0, 8.0]
    assert len(r["warnings"]) == 1 and "apple" in r["warnings"][0]


def test_slightly_off_sprite_stays_quiet():
    r = resolve({"scale_ref": "apple"}, 44, 80, _table())  # w_cm 4.4 → +10 % < 30 %
    assert r["warnings"] == []


def test_unknown_scale_ref_raises():
    try:
        resolve({"scale_ref": "unicorn_horn"}, 40, 80, _table())
        raise AssertionError("ScaleError erwartet")
    except ScaleError as e:
        assert "unicorn_horn" in str(e)


def test_real_repo_table():
    table, tol = load_table()
    assert tol == 0.3
    r = resolve({"scale_ref": "char_child"}, 600, 1250, (table, tol))
    assert r["size_cm"] == [60.0, 125.0], "Kind = 125 cm, 60 cm breit (Tabelle)"
    assert r["warnings"] == []
