#!/usr/bin/env python3
"""
Figuren-Teile im Stil „großer Kopf“ (Phase 04b) – ersetzt make_rig_parts.py + make_editor_parts.py.

Erzeugt für jede Schablone aus data/characters/templates.json ALLE Teile als Vektor-Zeichnung
(tools/chibi/), 8 px/cm, bit-genau reproduzierbar, 0 €:
    assets/characters/parts/<schablone>/<teil>.png
    assets/characters/parts/parts.json          Körper, Hände, Haare, Rückfall-Teile + _geometry
    assets/characters/parts/editor_parts.json   Teile aus dem Editor-Katalog (+ Zonen-Anzahl)
    data/character_parts/<slot>.json            Katalog (8 Slots, Varianten, Zonen, Aliase)

Teilnamen und Anker sind dieselben wie bisher → CharacterRig/CharacterLook bleiben gleich.
Farbkodierung: R/G/B = Farbzone 1/2/3, Rest = Tinte (siehe assets/shaders/zone_tint.gdshader).

Aufruf: python3 tools/make_chibi_parts.py [--only kid] [--jobs 4]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from chibi import accessories, body, hair, wardrobe  # noqa: E402

PARTS_DIR = ROOT / "assets" / "characters" / "parts"
CATALOG_DIR = ROOT / "data" / "character_parts"

# Gefühle → Augenform (set_emotion nimmt „eyes_<gefühl>“, falls vorhanden; „happy“ behält die Editor-Wahl)
EMO_EYES = {"laugh": "happy_closed", "sad": "sad", "love": "love", "tired": "sleepy", "surprised": "big"}

# ------------------------------------------------------------------ Katalog (Slots, Varianten, Zonen)
LABELS = {
    "hair": ("Frisur", "💇", 2), "eyes": ("Augen", "👀", 1), "mouth": ("Mund", "👄", 1),
    "top": ("Oberteil", "👕", 2), "bottom": ("Hose/Rock", "👖", 2), "shoes": ("Schuhe", "👟", 2),
    "accessory": ("Accessoire", "🎀", 3), "aid": ("Hilfsmittel", "🦻", 2),
}
GERMAN = {
    # Frisuren
    "short": "kurz", "spiky": "stachelig", "side_part": "Seitenscheitel", "curly": "Locken", "afro": "Afro",
    "bob": "Bob", "long": "lang", "pigtails": "Zöpfchen", "ponytail": "Pferdeschwanz", "bun": "Dutt",
    "space_buns": "zwei Dutts", "braids": "Zöpfe", "wavy": "wellig", "pixie": "Pixie", "buzz": "raspelkurz",
    "bald": "Glatze",
    # Augen / Mund
    "dot": "Punkte", "freckles": "Sommersprossen", "round": "rund", "big": "groß", "lash": "Wimpern",
    "sleepy": "müde", "wink": "zwinkern", "star": "Sterne", "smile": "Lächeln", "grin": "Grinsen", "oh": "Oh",
    "tongue": "Zunge", "neutral": "ruhig",
    # Kleidung
    "tee": "T-Shirt", "raglan": "Raglan", "tee_star": "Stern-Shirt", "longsleeve": "Langarm", "tank": "Top",
    "hoodie": "Kapuzenpulli", "sweater": "Pulli", "shirt": "Hemd", "jacket": "Jacke", "dress": "Kleid",
    "sundress": "Sommerkleid", "overalls": "Latzhose", "polo": "Polo", "raincoat": "Regenmantel",
    "trousers": "Hose", "jeans": "Jeans", "shorts": "kurze Hose", "skirt": "Rock", "leggings": "Leggings",
    "dungarees": "Latzhose", "tutu": "Tüllrock", "joggers": "Jogginghose",
    "sneaker_socks": "Turnschuhe + Socken", "sneaker": "Turnschuhe", "boot": "Stiefel", "sandal": "Sandalen",
    "slipper": "Hausschuhe", "rainboot": "Gummistiefel", "ballet": "Ballerinas", "hightop": "hohe Turnschuhe",
    "barefoot": "barfuß",
    # Accessoires / Hilfsmittel
    "none": "ohne", "glasses": "Brille", "glasses_square": "eckige Brille", "sunglasses": "Sonnenbrille",
    "headband": "Haarreif", "bow": "Schleife", "hairclip": "Spangen", "cap": "Kappe", "beanie": "Mütze",
    "sunhat": "Sonnenhut", "flowers": "Blumenkranz", "headphones": "Kopfhörer", "hearing_aid": "Hörgerät",
    "cochlear": "Cochlea-Implantat", "eye_patch": "Augenpflaster", "plaster": "Pflaster", "arm_sling": "Armschlinge",
}
# Reihenfolge = Reihenfolge im Editor; die erste Variante ohne „none“ ist der Startwert.
CATALOG = {
    "hair": ["long", "short", "pigtails", "bob", "curly", "afro", "ponytail", "bun", "space_buns", "braids", "wavy",
             "side_part", "pixie", "spiky", "buzz", "bald"],
    "eyes": ["dot", "freckles", "round", "big", "lash", "sleepy", "wink", "star"],
    "mouth": ["smile", "grin", "oh", "tongue", "neutral"],
    "top": ["tee", "shirt", "raglan", "tee_star", "longsleeve", "polo", "tank", "hoodie", "sweater", "jacket",
            "raincoat", "dress", "sundress", "overalls"],
    "bottom": ["trousers", "jeans", "shorts", "skirt", "leggings", "dungarees", "tutu", "joggers"],
    "shoes": ["sneaker", "sneaker_socks", "hightop", "boot", "rainboot", "sandal", "ballet", "slipper", "barefoot"],
    "accessory": ["none", "glasses", "glasses_square", "sunglasses", "headband", "bow", "hairclip", "cap", "beanie",
                  "sunhat", "flowers", "headphones"],
    "aid": ["none", "hearing_aid", "cochlear", "eye_patch", "plaster", "arm_sling"],
}
# Alte Varianten-IDs aus Speicherständen (Phase 04) → neue ID (R-11: alte Figuren laden weiter)
ALIASES = {"aid": {"knee_bandage": "plaster"}}
ZONES = {  # Farbzonen, die das Kind wählt (Rest ist Haut, Glanz oder fest)
    "hair": {s: (2 if s in ("pigtails", "ponytail", "braids") else 1) for s in CATALOG["hair"]},
    "accessory": {"none": 1, "glasses": 1, "glasses_square": 1, "sunglasses": 1, "headband": 1, "hairclip": 2,
                  "bow": 2, "cap": 2, "beanie": 2, "sunhat": 2, "flowers": 3, "headphones": 2},
    "aid": {"none": 1, "hearing_aid": 2, "cochlear": 2, "eye_patch": 1, "plaster": 2, "arm_sling": 1},
    "shoes": {s: (1 if s in ("barefoot",) else 2) for s in CATALOG["shoes"]},
}


# ------------------------------------------------------------------ Aufträge
def jobs_for(t: dict) -> dict[str, tuple]:
    """Teilname → (Art, Argumente). Gleiche Zeichnungen werden nur einmal gerechnet (Aliase)."""
    J: dict[str, tuple] = {"head": ("head", ()), "arm_skin": ("arm_skin", ()), "hand": ("hand", (False,)),
                           "hand_front": ("hand", (True,))}
    for st in hair.HAIR_STYLES:
        J["hair_front_" + st] = ("hair_front", (st,))
        J["hair_back_" + st] = ("hair_back", (st,))
    for st in body.EYE_STYLES:
        J["eyes_" + st] = ("eyes", (st,))
    for emo, st in EMO_EYES.items():
        J["eyes_" + emo] = ("eyes", (st,))
    for st in body.MOUTH_STYLES:
        J["mouth_" + st] = ("mouth", (st,))
    for st in wardrobe.TOP_STYLES:
        J["top_" + st] = ("top", (st,))
        J["sleeve_" + st] = ("sleeve", (wardrobe.SLEEVE_OF.get(st, "short"),))
    for st in wardrobe.BOTTOM_STYLES:
        J["bottom_" + st] = ("bottom", (st, False))
        J["bottom_sit_" + st] = ("bottom", (st, True))
    for st in wardrobe.SHOE_STYLES:
        J["shoes_" + st] = ("shoes", (st,))
    for st in accessories.ACC_STYLES:
        J["acc_" + st] = ("acc", (st,))
    for st in accessories.AID_STYLES:
        J["aid_" + st] = ("aid", (st,))
    # Rückfall-Teile (Figuren ohne Editor-Auswahl, Phase-03-Namen)
    J["torso"] = J["top_tee"]
    J["arm_sleeve"] = J["sleeve_tee"]
    J["legs_stand"] = J["bottom_trousers"]
    J["legs_sit"] = J["bottom_sit_trousers"]
    J["shoes_stand"] = J["shoes_sneaker"]
    return J


def _draw(args: tuple):
    t, kind, a, ppc = args
    fn = {
        "head": lambda: body.draw_head(t, ppc), "arm_skin": lambda: body.draw_arm_skin(t, ppc),
        "hand": lambda: body.draw_hand(t, ppc, *a), "hair_front": lambda: hair.draw_hair_front(t, *a, ppc),
        "hair_back": lambda: hair.draw_hair_back(t, *a, ppc), "eyes": lambda: body.draw_eyes(t, *a, ppc),
        "mouth": lambda: body.draw_mouth(t, *a, ppc), "top": lambda: wardrobe.draw_top(t, *a, ppc),
        "sleeve": lambda: wardrobe.draw_sleeve(t, *a, ppc),
        "bottom": lambda: wardrobe.draw_bottom(t, a[0], ppc, sit=a[1]),
        "shoes": lambda: wardrobe.draw_shoes(t, *a, ppc), "acc": lambda: accessories.draw_accessory(t, *a, ppc),
        "aid": lambda: accessories.draw_aid(t, *a, ppc),
    }[kind]
    img, info = fn()
    return img, info


EDITOR_PREFIX = ("top_", "sleeve_", "bottom_", "shoes_", "eyes_", "mouth_", "acc_", "aid_")


def build_template(tid: str, t: dict, ppc: float, pool: ProcessPoolExecutor, out: Path) -> tuple[dict, dict]:
    out.mkdir(parents=True, exist_ok=True)
    J = jobs_for(t)
    uniq = sorted({v for v in J.values()}, key=repr)
    results = dict(zip(uniq, pool.map(_draw, [(t, k, a, ppc) for k, a in uniq])))
    rig: dict[str, dict] = {}
    editor: dict[str, dict] = {}
    for name in sorted(J):
        img, info = results[J[name]]
        img.save(out / f"{name}.png", optimize=True)
        entry = dict(info)
        entry["note"] = f"P04b · {J[name][0]}"
        (editor if name.startswith(EDITOR_PREFIX) and name not in ("shoes_stand",) else rig)[name] = entry
    # Alte Dateien entfernen, die es nicht mehr gibt (samt .import) – sonst lädt Godot Leichen
    keep = {f"{n}.png" for n in J}
    for f in out.glob("*.png"):
        if f.name not in keep:
            f.unlink()
            imp = f.with_name(f.name + ".import")
            if imp.exists():
                imp.unlink()
    lg, sh = t["leg"], t["shoe"]
    rig["_geometry"] = {"sit_drop_cm": round(lg["shin"] + 2.0, 2), "shoe_h_cm": sh["h"], "sit_thigh_cm": lg["sit_thigh"]}
    return rig, editor


def write_catalog(dirpath: Path) -> int:
    n = 0
    for slot, ids in CATALOG.items():
        label, icon, max_z = LABELS[slot]
        variants = []
        for vid in ids:
            v = {"id": vid, "label": GERMAN.get(vid, vid), "zones": ZONES.get(slot, {}).get(vid, max_z), "tags": [slot]}
            if vid == "none":
                v["tags"] = ["none"]
            if slot == "hair":
                v["part"], v["part_back"] = "hair_front_" + vid, "hair_back_" + vid
                if vid == "bald":
                    v["tags"] = ["hair", "bald"]
            elif slot == "top":
                v["part"], v["part_back"] = "top_" + vid, "sleeve_" + vid
            elif slot == "bottom":
                v["part"], v["part_back"] = "bottom_" + vid, "bottom_sit_" + vid
            else:
                v["part"] = {"eyes": "eyes_", "mouth": "mouth_", "shoes": "shoes_", "accessory": "acc_",
                             "aid": "aid_"}[slot] + vid
            variants.append(v)
            n += 1
        doc = {"slot": slot, "label": label, "icon": icon, "max_zones": max_z, "variants": variants}
        if slot in ALIASES:
            doc["aliases"] = ALIASES[slot]
        (dirpath / f"{slot}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="nur diese Schablone(n), Komma-getrennt")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", default=str(PARTS_DIR))
    ap.add_argument("--catalog", default=str(CATALOG_DIR))
    a = ap.parse_args(argv)
    data = json.loads((ROOT / "data" / "characters" / "templates.json").read_text(encoding="utf-8"))
    ppc = float(data["px_per_cm"])
    out = Path(a.out)
    only = [s for s in a.only.split(",") if s]
    rig_all = json.loads((out / "parts.json").read_text(encoding="utf-8")) if only and (out / "parts.json").exists() else {}
    ed_all = json.loads((out / "editor_parts.json").read_text(encoding="utf-8")) if only and (out / "editor_parts.json").exists() else {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.jobs) as pool:
        for tid, t in data["templates"].items():
            if only and tid not in only:
                continue
            rig_all[tid], ed_all[tid] = build_template(tid, t, ppc, pool, out / tid)
            print(f"  {tid}: {len(rig_all[tid]) - 1 + len(ed_all[tid])} Teile ({time.time() - t0:.0f} s)")
    for stale in set(rig_all) - set(data["templates"]):
        rig_all.pop(stale, None)
        ed_all.pop(stale, None)
    (out / "parts.json").write_text(json.dumps(rig_all, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (out / "editor_parts.json").write_text(json.dumps(ed_all, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    n = write_catalog(Path(a.catalog))
    print(f"✅ Figuren-Teile für {len(rig_all)} Schablonen · Katalog {n} Varianten → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
