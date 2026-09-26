#!/usr/bin/env python3
"""P06-T09 – Test-Szene: Komposition wie die Referenz-Küche (reference/).

Nachbau von reference/pipeline_demo_kueche.py compose(): Kind hält Karotte,
Teddy sitzt auf dem Stuhl, Items stehen maßstabsgetreu auf Tisch/Arbeitsplatte,
Ball/Hund vorne. Die Raum-Kalibrierung gehört zum Hintergrund
``raw_kitchen_bg.png`` (Arbeitsplatte 90 cm = 165 px an der Rückwand, Regel S-07
Tiefe max. +12 %, Regel S-08 Kamera ≈ 300 cm Raumhöhe).

Ausgabe: ``<out_dir>/scene_test.png`` (Gesamtszene) und
``<out_dir>/scene_test_kamera.png`` (1920×1080 Spielkamera-Ausschnitt).
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]

# Kalibrierung raw_kitchen_bg.png (Demo-Werte, px bei SCALE_OUT=1)
SCALE_OUT = 2
_BASE_PX_CM = 1.83
_REF_Y, _REF_SPAN, DEPTH_MAX = 600, 135, 0.12

# Layout (Demo-Koordinaten bei SCALE_OUT=1)
_COUNTER_Y = 434
_COUNTER_ITEMS = [("school_book_blue_star", 640), ("home_cup_orange_dots", 692),
                  ("food_apple_green", 878)]
_CHAIR = (652, 850)
_TABLE = (664, 1010)
_TABLE_ITEMS = [("home_mug_pink_dots", -0.30), ("food_apple_red", -0.05),
                ("food_icecream_3", 0.12), ("flower_tulip_red_pot", 0.32)]
_BALL = (728, 1165)
_DOG = (712, 520)
_GIRL = (715, 370)
_CAM = {"y1": 744, "x0": 228, "height_cm": 300}


def px_per_cm(y: float) -> float:
    t = max(0.0, min(1.0, (y - _REF_Y) / _REF_SPAN))
    return _BASE_PX_CM * (1 + DEPTH_MAX * t) * SCALE_OUT


def _require(recs: dict, ids: list[str]) -> None:
    missing = [i for i in ids if i not in recs]
    if missing:
        raise KeyError(f"Test-Szene braucht fehlende Records: {', '.join(missing)}")


def _loader(recs: dict, sprites_root: Path | None):
    cache: dict[str, Image.Image] = {}

    def load(id_: str) -> Image.Image:
        if id_ not in cache:
            rec = recs[id_]
            p = rec.get("_path")
            if not p:
                sp = rec.get("sprite", "")
                p = (ROOT / sp[len("res://"):] if sp.startswith("res://") else Path(sp))
                if sprites_root and not Path(p).exists():
                    p = Path(sprites_root) / f"{id_}.png"
            cache[id_] = Image.open(p).convert("RGBA")
        return cache[id_]

    return load


def _scaled(rec: dict, y_floor: float, load) -> Image.Image:
    img = load(rec["id"])
    s = px_per_cm(y_floor)
    w, h = rec["size_cm"][0] * s, rec["size_cm"][1] * s
    return img.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)


def _drop_shadow(canvas: Image.Image, cx: float, y: float, w: float, strength=0.28):
    sh = Image.new("L", (int(w * 1.4) + 40, int(w * 0.35) + 40), 0)
    ImageDraw.Draw(sh).ellipse([20, 20, sh.width - 20, sh.height - 20],
                               fill=int(255 * strength))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    layer = Image.new("RGBA", sh.size, (60, 35, 20, 0))
    layer.putalpha(sh)
    canvas.alpha_composite(layer, (int(cx - sh.width / 2), int(y - sh.height / 2)))


def _put(canvas, img, cx, base_y, shadow=True):
    if shadow:
        _drop_shadow(canvas, cx, base_y, img.width * 0.8)
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(base_y - img.height)))


def render_reference_kitchen(recs: dict, bg_path, out_dir,
                             sprites_root: Path | None = None) -> list[Path]:
    """Szene rendern; gibt [Gesamtszene, Kamera-Ausschnitt] zurück."""
    need = ([i for i, _ in _COUNTER_ITEMS] + [i for i, _ in _TABLE_ITEMS] +
            ["home_chair_mint", "toy_teddy_brown", "home_table_wood",
             "toy_beachball", "pet_dog_brown", "char_girl_01", "food_carrot"])
    _require(recs, need)
    R = recs
    load = _loader(recs, sprites_root)
    bg = Image.open(bg_path).convert("RGBA")
    S = SCALE_OUT
    c = bg.resize((bg.width * S, bg.height * S), Image.LANCZOS)

    # Arbeitsplatte (hintere Ebene)
    counter_y = _COUNTER_Y * S
    s_back = px_per_cm(_REF_Y)
    for id_, x in _COUNTER_ITEMS:
        rec = R[id_]
        img = load(id_)
        img = img.resize((round(rec["size_cm"][0] * s_back), round(rec["size_cm"][1] * s_back)),
                         Image.LANCZOS)
        c.alpha_composite(img, (int(x * S - img.width / 2), int(counter_y - img.height)))

    # Stuhl (etwas weiter hinten), Teddy darauf, Tisch davor
    yc, xc = _CHAIR
    chair = _scaled(R["home_chair_mint"], yc, load)
    _put(c, chair, xc * S, yc * S)
    seat_y = yc * S - chair.height * 0.50
    _put(c, _scaled(R["toy_teddy_brown"], yc, load),
         xc * S + chair.width * 0.12, seat_y + 6, shadow=False)

    yt, xt = _TABLE
    table = _scaled(R["home_table_wood"], yt, load)
    tx = xt * S
    _put(c, table, tx, yt * S)
    top_y = yt * S - table.height + table.height * 0.085
    for id_, dx in _TABLE_ITEMS:
        _put(c, _scaled(R[id_], yt, load), tx + dx * table.width, top_y + 4, shadow=False)

    # Ball vorne rechts, Hund
    by, bx = _BALL
    _put(c, _scaled(R["toy_beachball"], by, load), bx * S, by * S)
    yd, xd = _DOG
    _put(c, _scaled(R["pet_dog_brown"], yd, load), xd * S, yd * S)

    # Figur mit Karotte in der Hand (Karotte HINTER der Faust)
    yg, xg = _GIRL
    girl = _scaled(R["char_girl_01"], yg, load)
    gx0 = int(xg * S - girl.width / 2)
    gy0 = int(yg * S - girl.height)
    fist = R["char_girl_01"].get("hand_grip") or [0.5, 0.5]
    hand = (gx0 + fist[0] * girl.width, gy0 + fist[1] * girl.height)
    car = R["food_carrot"]
    cimg = _scaled(car, yg, load)
    rot = cimg.rotate(-car.get("hold_angle", 0), resample=Image.BICUBIC, expand=True)
    grip = car.get("grip") or [0.5, 1.0]
    gxp = grip[0] * cimg.width - cimg.width / 2
    gyp = grip[1] * cimg.height - cimg.height / 2
    t = math.radians(car.get("hold_angle", 0))
    rx = gxp * math.cos(t) - gyp * math.sin(t)
    ry = gxp * math.sin(t) + gyp * math.cos(t)
    _drop_shadow(c, xg * S, yg * S, girl.width * 0.8)
    c.alpha_composite(rot, (int(hand[0] - (rot.width / 2 + rx)),
                            int(hand[1] - (rot.height / 2 + ry))))
    c.alpha_composite(girl, (gx0, gy0))

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    scene_path = out_dir / "scene_test.png"
    c.convert("RGB").save(scene_path)

    # Spielkamera: ~300 cm Raumhöhe, 16:9 (Regel S-08)
    vis_h = _CAM["height_cm"] * px_per_cm(640)
    y1 = _CAM["y1"] * S
    y0 = y1 - vis_h
    w = vis_h * 16 / 9
    x0 = _CAM["x0"] * S
    cam = c.crop((int(x0), int(y0), int(x0 + w), int(y1))).resize((1920, 1080), Image.LANCZOS)
    cam_path = out_dir / "scene_test_kamera.png"
    cam.convert("RGB").save(cam_path)
    return [scene_path, cam_path]
