"""
Figur aus Teilen zusammensetzen – CPU-Nachbau des CharacterRig (für Vorschau, Katalog-Bilder und Tests).
Reihenfolge wie in src/characters/character_rig.gd.
"""
from __future__ import annotations

import math

from PIL import Image

from .vec import hexcol, tint

SKIN_BLUSH = (1.0, 0.55, 0.55)


def blush(skin: tuple) -> tuple:
    return tuple(min(1.0, s * 0.62 + b * 0.38) for s, b in zip(skin, SKIN_BLUSH))


def _paste(canvas: Image.Image, img: Image.Image, info: dict, at_cm: tuple, ppc: float, origin_px: tuple, rot: float = 0.0):
    """Teil so einfügen, dass sein Anker auf at_cm (Figuren-cm) liegt; rot in rad (positiv = gegen Uhrzeiger)."""
    ax = info["anchor_cm"][0] * ppc
    ay = (info["h_cm"] - info["anchor_cm"][1]) * ppc
    if rot:
        # um den Anker drehen: Bild so erweitern, dass der Anker in der Mitte liegt
        w, h = img.size
        R = int(math.ceil(math.hypot(max(ax, w - ax), max(ay, h - ay)))) + 2
        big = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
        big.paste(img, (int(round(R - ax)), int(round(R - ay))))
        img = big.rotate(math.degrees(rot), resample=Image.BICUBIC, center=(R, R))
        ax, ay = R, R
    x = origin_px[0] + at_cm[0] * ppc - ax
    y = origin_px[1] - at_cm[1] * ppc - ay
    canvas.alpha_composite(img, (int(round(x)), int(round(y))))


def compose(t: dict, parts: dict, look: dict, ppc: float = 8.0, pad_cm: float = 20.0, arm_out: float = 0.12) -> Image.Image:
    """parts: name → (img, info). look: skin, hair, eye, top[3], bottom[2], shoes[2]."""
    W = int((t["torso"]["w_bot"] + t["head"]["w"] + 2 * pad_cm) * ppc)
    Hh = int((t["hair_top"] + 2 * pad_cm) * ppc)
    img = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    org = (W / 2, Hh - pad_cm * ppc)
    skin = hexcol(look["skin"])
    hair = hexcol(look["hair"])
    cols = {
        "skin": [skin, blush(skin)],
        "eyes": [hexcol(look.get("eye", "#4a3020")), (1, 1, 1), hair],
        "mouth": [hexcol("#b0424f"), hexcol("#ff8fa3")],
        "hair": [hair, tuple(min(1.0, h * 0.55 + 0.45 * 0.75) for h in hair), hexcol(look.get("hair2", "#ff6f91"))],
        "top": [hexcol(x) for x in look["top"][:2]] + [skin],
        "bottom": [hexcol(x) for x in look["bottom"]] + [skin],
        "shoes": [hexcol(x) for x in look["shoes"]] + [skin],
    }
    sh = t["shoulder"]
    hand = (0, -t["arm"]["len"])

    def put(name, group, at, rot=0.0):
        if name not in parts:
            return
        im, info = parts[name]
        _paste(img, tint(im, cols[group]), info, at, ppc, org, rot)

    def arm(side):
        sx = sh["x"] * side
        rot = arm_out * side
        at = (sx, sh["y"])
        put("arm_skin", "skin", at, rot)
        put(look.get("sleeve", "sleeve_tee"), "top", at, rot)
        hx = sx + math.sin(rot) * t["arm"]["len"]
        hy = sh["y"] - math.cos(rot) * t["arm"]["len"]
        put("hand", "skin", (hx, hy))

    # weicher Bodenschatten
    from PIL import ImageDraw
    sh_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rw = t["torso"]["w_bot"] * 0.95 * ppc
    ImageDraw.Draw(sh_img).ellipse([org[0] - rw, org[1] - rw * 0.16, org[0] + rw, org[1] + rw * 0.16], fill=(60, 40, 60, 60))
    img.alpha_composite(sh_img)
    put("hair_back_" + look.get("hair_style", "short"), "hair", (0, t["hair_top"]))
    arm(-1)
    put(look.get("bottom_part", "bottom_trousers"), "bottom", (0, 0))
    put(look.get("shoes_part", "shoes_sneaker"), "shoes", (0, 0))
    put(look.get("top_part", "top_tee"), "top", (0, t["torso"]["bot"]))
    cy = t["head"]["cy"]
    put("head", "skin", (0, cy))
    put("eyes_" + look.get("eyes", "dot"), "eyes", (0, cy))
    put("mouth_" + look.get("mouth", "smile"), "mouth", (0, cy))
    put("hair_front_" + look.get("hair_style", "short"), "hair", (0, t["hair_top"]))
    arm(1)
    return img
