#!/usr/bin/env python3
"""P06-T08 – Lineup: alle Items eines Bereichs + Kind + Hund + Tisch am cm-Lineal.

Portiert aus reference/pipeline_demo_kueche.py lineup(), aber dynamisch:
Reihenfolge nach Höhe, Zahlen kommen aus size_cm der Item-JSON bzw. der
Maßstab-Tabelle, Bereichs- und Legendennamen sind frei wählbar.

Ausgabe: ``<out_dir>/lineup_<bereich>.png`` (Standard: docs/tests/).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]

PX_CM = 3.0        # Lineal-Auflösung wie Demo
PAD = 60
GROUND = 470       # Bodenlinie

# Legende: End-Segment des IDs → deutscher Kurzname
_NAME_DE = {
    "egg": "Ei", "apple": "Apfel", "red": "rot", "green": "grün", "mug": "Tasse",
    "cup": "Becher", "carrot": "Karotte", "book": "Buch", "ball": "Ball",
    "teddy": "Teddy", "tulip": "Tulpe", "table": "Tisch", "chair": "Stuhl",
    "dog": "Hund", "girl": "Kind", "child": "Kind", "pot": "Topf",
    "chocolate": "Schoko", "icecream": "Eis", "star": "Stern", "beachball": "Strandball",
    "wood": "", "mint": "", "brown": "", "b": "", "pink": "", "dots": "",
    "orange": "", "blue": "", "yellow": "gelb", "boy": "Junge", "cat": "Katze",
    "sofa": "Sofa", "bed": "Bett", "armchair": "Sessel", "kid": "Kind",
}


def _name(item_id: str) -> str:
    parts = item_id.split("_")[1:]           # Kategorie-Präfix weg
    words = [_NAME_DE.get(p, p.replace("-", " ")) for p in parts if not p.isdigit()]
    words = [w for w in words if w]
    return " ".join(words) if words else item_id


def _font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _load_sprite(rec: dict, fallback_cm: tuple[float, float]) -> Image.Image:
    """Sprite aus res://-/Pfad; ohne Datei: graue Platzhalter-Fläche (exakte cm)."""
    sp = rec.get("sprite", "")
    if sp.startswith("res://"):
        p = ROOT / sp[len("res://"):]
    else:
        p = Path(sp)
    if p.exists():
        return Image.open(p).convert("RGBA")
    w_cm, h_cm = rec["size_cm"]
    w = max(4, round(w_cm * PX_CM)); h = max(4, round(h_cm * PX_CM))
    return Image.new("RGBA", (w, h), (150, 150, 160, 255))


def render(items_json: Path, out_path: Path, *, extra: list[str] | None = None,
           table_path: Path | None = None) -> Path:
    """Lineup-Bild bauen und nach ``out_path`` schreiben."""
    data = json.loads(Path(items_json).read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in data["items"]}
    table = json.loads((table_path or ROOT / "data" / "scale_table.json")
                       .read_text(encoding="utf-8"))
    T = {e["id"]: e for e in table["entries"]}

    # Kind + Hund + Tisch sind Pflicht-Anker (Kind immer, Hund/Tisch aus dem
    # Bereich oder als Tabellen-Platzhalter) – niemals doppelt in der Reihe.
    items = data["items"]
    picks: list[dict] = []
    char_path = ROOT / "assets" / "characters" / "sprite" / "char_girl_01.png"
    kid_rec: dict = {"id": "char_girl_01",
                     "size_cm": [T["char_child"]["w_cm"], T["char_child"]["h_cm"]],
                     "sprite": "res://assets/characters/sprite/char_girl_01.png"}
    if char_path.exists():
        im = Image.open(char_path)
        kid_rec["size_cm"] = [round(T["char_child"]["h_cm"] * im.width / im.height, 1),
                              T["char_child"]["h_cm"]]
    picks.append(kid_rec)

    def _anchor(match_prefix: str, table_ids: list[str]) -> dict:
        for r in items:
            if r["id"].startswith(match_prefix):
                return r
        tid = table_ids[0]
        return {"id": tid, "size_cm": [T[tid]["w_cm"], T[tid]["h_cm"]], "sprite": ""}

    picks.append(_anchor("pet_dog", ["pet_dog_medium"]))
    picks.append(_anchor("home_table", ["home_table_dining"]))
    anchor_ids = {r["id"] for r in picks}
    for r in items:
        if r["id"] not in anchor_ids:
            picks.append(r)

    max_cm = max(r["size_cm"][1] for r in picks)
    top_cm = max(140, int(math.ceil(max_cm / 50.0) * 50))
    gy = GROUND
    # Höhe des Lineals an das höchste Objekt anpassen (Boden bleibt)
    scale = PX_CM
    h_needed = top_cm * scale
    canvas_h = gy + 90
    if h_needed > gy - 20:
        scale = (gy - 20) / top_cm

    W = PAD * 2 + 40 + sum(max(round(r["size_cm"][0] * scale), 70) + 28 for r in picks)
    c = Image.new("RGBA", (W, canvas_h), (255, 248, 236, 255))
    d = ImageDraw.Draw(c)
    fb, fn = _font(17), _font(15)
    for cm in range(0, top_cm + 1, 10):
        y = gy - cm * scale
        d.line([(PAD, y), (W - 20, y)], fill=(210, 200, 185) if cm % 50 else (180, 170, 155), width=1)
        if cm % 50 == 0:
            d.text((12, y - 9), f"{cm}", fill=(130, 130, 140), font=fn)
    d.rectangle([0, gy, W, gy + 90], fill=(232, 199, 154))

    x = PAD + 40
    for r in picks:
        w_cm, h_cm = r["size_cm"]
        img = _load_sprite(r, (w_cm, h_cm))
        tw, th = max(1, round(w_cm * scale)), max(1, round(h_cm * scale))
        if (img.width, img.height) != (tw, th):
            img = img.resize((tw, th), Image.LANCZOS)
        slot = max(img.width, 70)
        cx = x + slot / 2
        c.alpha_composite(img, (int(cx - img.width / 2), int(gy - img.height)))
        t = _name(r["id"]) or r["id"]
        d.text((cx - d.textlength(t, font=fb) / 2, gy + 14), t, fill=(58, 63, 88), font=fb)
        tt = f"{h_cm:g} cm"
        d.text((cx - d.textlength(tt, font=fn) / 2, gy + 38), tt, fill=(110, 110, 125), font=fn)
        x += slot + 28

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c.convert("RGB").save(out_path)
    return out_path


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("items_json")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args(argv)
    src = Path(a.items_json)
    area = json.loads(src.read_text(encoding="utf-8")).get("area", src.stem)
    out = Path(a.out) if a.out else ROOT / "docs" / "tests" / f"lineup_{area}.png"
    p = render(src, out)
    print(f"Lineup → {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
