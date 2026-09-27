"""
Katalog, Teil P07-Inventar (Wunsch 👤: „wirklich alles vom Löffel bis zur Wohnwand, in Varianten“).
Die Pflichtliste steht in data/inventory.json, der Test tools/tests/test_inventory.py prüft sie gegen den Katalog.

Wird am Ende von catalog.py geladen und hängt seine Vorlagen an TEMPLATES an (gleiche Felder wie dort).
"""
from __future__ import annotations

from . import cabinets as CB
from . import home_big as HB
from . import home_small as HS
from . import kids as KI
from . import patio as PA
from . import yard as YA
from .catalog import S, T, cols

OPEN = {"states": {"open": {"state": "open"}}, "state0": "closed"}
ON = {"states": {"on": {"state": "on"}}, "state0": "off"}
GROW = {"states": {"sprout": {"state": "sprout"}, "grown": {"state": "grown"}, "ripe": {"state": "ripe"}}, "state0": "empty"}
DRY = {"states": {"dry": {"state": "dry"}}, "state0": "fresh"}
MIRROR, WATER, CHROME, BRICK = "#d4e9f2", "#7cc6e0", "#c9d0d8", "#c0664f"
FRONTS = ["cream", "sage", "sky", "navy", "coral", "oak", "grey"]


def cab(id: str, w: float, h: float, layout: str, group: str, names: list, body: str | None = None, third: str = "oak",
        top: str = "flat", legs: str = "short", plinth: bool = False, placement: str = "floor", state: bool = True, **extra):
    """Schrank aus dem Baukasten: Zone 1 Korpus, 2 Fronten, 3 Griffe/Platte."""
    T(id=id, fn=CB.cabinet, w=w, h=h, kw={"layout": layout, "top": top, "legs": legs, "plinth": plinth}, group=group,
      category="furniture", placement=placement,
      variants=[(n, cols(body or n, n, third)) for n in names], **({**OPEN} if state and ("D" in layout or "G" in layout) else {}),
      **extra)


# ------------------------------------------------------------------ Schränke (Wohnen, Flur, Büro, Keller)
cab("furn_sideboard", 160, 80, "D|W/W/W|D", "storage", ["oak", "walnut", "cream", "sage", "navy", "white"], legs="tall",
    surface_h=80)
cab("furn_sideboard_low", 180, 55, "D|D|D", "storage", ["walnut", "cream", "grey"], legs="tall", surface_h=55)
cab("furn_vitrine", 90, 190, "D/G/G/G", "storage", ["oak", "walnut", "white", "sage"], top="crown", body=None)
cab("furn_vitrine_wide", 140, 180, "W/G/G|W/G/G", "storage", ["cream", "walnut"], top="crown")
cab("furn_wall_unit", 280, 190, "D/G/G/G|W/T/O|D/O/O/O|D/G/G/G", "storage", ["oak", "walnut", "white", "grey"], top="crown",
    legs="none", plinth=True)
cab("furn_shoe_cabinet", 80, 100, "S/S/W", "storage", ["white", "oak", "grey", "sky"], surface_h=100)
cab("furn_shoe_cabinet_bench", 100, 48, "S|S", "storage", ["oak", "cream"], legs="none", state=False,
    seat={"h": 48, "pose": "sit", "slots": 2})
cab("furn_file_cabinet", 45, 130, "F/F/F/F", "storage", ["grey", "navy", "cream"], third="metal", legs="none", state=False)
cab("furn_metal_shelf", 90, 180, "O/O/O/O", "storage", ["metal", "grey", "black"], body=None, third="metal", legs="short",
    top="flat", state=False)
T(id="furn_chest", fn=KI.toy_big, w=90, h=55, kw={"style": "chest"}, group="storage", category="furniture", **OPEN,
  container={"slots": 6, "max_item_h_cm": 40}, variants=[(n, cols(n, "coral", "#e0b84a")) for n in ["walnut", "oak", "sky", "rose"]])
T(id="furn_dresser_tall", fn=CB.cabinet, w=80, h=120, kw={"layout": "W/W/W/W/W", "legs": "short"}, group="storage",
  category="furniture", surface_h=120, variants=[(n, cols(n, n, "oak")) for n in ["white", "oak", "sage"]])

# ------------------------------------------------------------------ Küche (Möbel & Geräte)
for kid, w, layout in (("door", 60, "D"), ("drawers", 60, "W/W/W"), ("double", 90, "D|D"), ("mixed", 80, "D|W/W/W")):
    cab(f"kit_cabinet_base_{kid}", w, 90, layout, "kitchen_furn", FRONTS[:5], body="white", third="oak", top="counter",
        legs="none", plinth=True, surface_h=90, state=kid != "drawers")
for kid, w, h, layout in (("door", 60, 70, "D"), ("double", 90, 70, "D|D"), ("glass", 80, 70, "G|G"), ("flat", 90, 40, "D|D")):
    cab(f"kit_cabinet_wall_{kid}", w, h, layout, "kitchen_furn", FRONTS[:5], body="white", third="oak", top="none", legs="none",
        placement="wall")
for kid, w, layout in (("long", 180, "D|W/W/W|D|D"), ("short", 120, "D|W/W/W")):
    cab(f"kit_counter_{kid}", w, 90, layout, "kitchen_furn", FRONTS[:5], body="white", third="oak", top="counter", legs="none",
        plinth=True, surface_h=90)
for kid in ("sink", "hob"):
    T(id=f"kit_counter_{kid}", fn=CB.counter_extra, w=120, h=90, kw={"kind": kid}, group="kitchen_furn", category="furniture",
      surface_h=90, **OPEN, variants=[(n, cols("white", n, "oak")) for n in FRONTS[:5]])
cab("kit_island", 160, 92, "D|W/W|D|D", "kitchen_furn", ["white", "navy", "sage", "oak"], body=None, third="walnut",
    top="counter", legs="none", plinth=True, surface_h=92)
T(id="app_dishwasher", fn=HB.big, w=60, h=85, kw={"style": "dishwasher"}, group="kitchen_furn", category="furniture",
  surface_h=85, **ON, variants=[(n, cols(n, "sky", "metal")) for n in ["white", "metal", "black"]])
T(id="kit_hood", fn=HB.big, w=90, h=60, kw={"style": "hood"}, group="kitchen_furn", category="furniture", placement="wall",
  **ON, variants=[(n, cols(n, "butter", "grey")) for n in ["metal", "white", "black"]])
T(id="furn_highchair", fn=HB.big, w=55, h=105, kw={"style": "highchair"}, group="baby", category="furniture",
  seat={"h": 58, "pose": "sit", "slots": 1}, variants=[(n, cols(n, "cream", "oak")) for n in ["white", "mint", "coral", "oak"]])
for st, w, h, names, extra in (("knife", 3, 24, ["black", "oak", "coral"], {}), ("woodspoon", 6, 30, ["oak", "pine"], {}),
                               ("rolling_pin", 40, 6, ["pine", "oak"], {}), ("teapot", 24, 18, ["cream", "coral", "sky", "mint"], {}),
                               ("tray", 45, 5, ["oak", "cream", "sky"], {}), ("breadbox", 36, 20, ["cream", "oak", "coral", "mint"], OPEN),
                               ("fruit_bowl", 28, 14, ["cream", "sky", "oak"], {}), ("spice_rack", 34, 26, ["oak", "white"], {}),
                               ("trash", 30, 40, ["metal", "cream", "coral", "mint"], {}), ("dish_rack", 44, 24, ["metal", "white"], {}),
                               ("baking_tray", 42, 3, ["metal"], {}), ("scale", 22, 12, ["cream", "coral", "mint"], {}),
                               ("salt_pepper", 9, 10, ["cream", "oak"], {}), ("canister", 12, 18, ["cream", "sky", "coral", "mint"], {}),
                               ("paper_roll", 14, 30, ["oak", "metal"], {}), ("sieve", 26, 10, ["metal", "coral"], {})):
    S(f"kit_{st}", HS.small, st, w, h, "kitchen", "kitchen", names,
      second={"teapot": "rose", "fruit_bowl": "coral", "canister": "cream", "salt_pepper": "black", "spice_rack": "coral",
              "dish_rack": "cream", "baking_tray": "oak", "tray": "cream", "sieve": "metal", "breadbox": "oak"}.get(st, "cream"),
      third={"fruit_bowl": "butter", "scale": "metal", "trash": "black", "rolling_pin": "coral", "baking_tray": "oak",
             "salt_pepper": "metal", "paper_roll": "metal", "sieve": "black", "spice_rack": "butter", "knife": "metal"}.get(st, "metal"),
      **extra)

# ------------------------------------------------------------------ Wohnen & Schlafen
T(id="furn_sofa_corner", fn=HB.big, w=260, h=85, kw={"style": "sofa_corner"}, group="sofas", category="furniture",
  seat={"h": 42, "pose": "sit", "slots": 4}, variants=[(n, cols(n, "cream" if n != "cream" else "coral", "black"))
                                                        for n in ["grey", "sage", "navy", "sand", "rust"]])
T(id="furn_fireplace", fn=HB.big, w=140, h=120, kw={"style": "fireplace"}, group="storage", category="furniture", surface_h=120,
  **{**ON, "anim": {"on": "pulse"}}, variants=[(n, cols(n, "orange", "walnut")) for n in ["cream", BRICK, "grey", "white"]])
T(id="furn_piano", fn=HB.big, w=150, h=125, kw={"style": "piano"}, group="storage", category="furniture",
  variants=[(n, cols(n, "white", "black")) for n in ["black", "walnut", "white"]])
T(id="furn_vanity", fn=HB.big, w=100, h=150, kw={"style": "vanity"}, group="beds", category="furniture",
  variants=[(n, cols(n, MIRROR, "#e0b84a")) for n in ["white", "rose", "oak", "sky"]])
T(id="furn_clothes_rack", fn=HB.big, w=120, h=160, kw={"style": "clothes_rack"}, group="clothes", category="furniture",
  variants=[(n, cols(n, "sky" if n != "sky" else "butter", "metal")) for n in ["coral", "mint", "rose", "sky"]])
T(id="furn_coat_rack", fn=HB.big, w=55, h=180, kw={"style": "coat_rack"}, group="clothes", category="furniture",
  variants=[(n, cols(n, "coral", w)) for n, w in (("navy", "oak"), ("sage", "walnut"), ("rust", "black"))])
T(id="furn_stairs", fn=HB.big, w=220, h=250, kw={"style": "stairs"}, group="storage", category="furniture",
  variants=[(n, cols(n, "cream", "walnut" if n != "walnut" else "oak")) for n in ["oak", "walnut", "white"]])
T(id="furn_stroller", fn=HB.big, w=70, h=105, kw={"style": "stroller"}, group="baby", category="furniture",
  variants=[(n, cols(n, n, "black")) for n in ["navy", "sage", "rose", "grey"]])
T(id="furn_mattress", fn=HB.big, w=190, h=20, kw={"style": "mattress"}, group="beds", category="furniture",
  seat={"h": 20, "pose": "lie", "slots": 1}, variants=[(n, cols(n, "sky", "cream")) for n in ["cream", "sky", "rose", "mint"]])
T(id="pet_cat_tree", fn=HB.big, w=60, h=150, kw={"style": "cat_tree"}, group="animals", category="furniture",
  variants=[(n, cols(n, n, "sand")) for n in ["grey", "cream", "rose"]])
T(id="deco_gramophone", fn=HB.big, w=40, h=50, kw={"style": "gramophone"}, group="deco", category="item", placement="table",
  hold="two_hands", grip=[0.5, 0.2], variants=[(n, cols(n, "#e0b84a", "metal")) for n in ["walnut", "oak"]])
T(id="elec_printer", fn=HB.big, w=45, h=25, kw={"style": "printer"}, group="electronics", category="item", placement="table",
  hold="two_hands", grip=[0.5, 0.5], **ON, variants=[(n, cols(n, "white", "sky")) for n in ["grey", "white", "black"]])
for st, w, h, names, place, grp in (("duvet", 60, 22, ["sky", "rose", "mint", "butter", "cream", "lilac", "navy"], "floor", "beds"),
                                    ("pillow", 60, 30, ["cream", "sky", "rose", "mint", "butter", "lilac"], "floor", "beds"),
                                    ("throw", 50, 18, ["coral", "sage", "grey", "rust", "sky"], "floor", "beds"),
                                    ("magazines", 30, 8, ["coral", "sky"], "table", "deco"),
                                    ("speaker", 20, 32, ["black", "cream", "sky"], "table", "electronics"),
                                    ("remote", 5, 17, ["black", "grey", "cream"], "table", "electronics"),
                                    ("alarm", 14, 16, ["coral", "sky", "mint", "butter"], "table", "deco"),
                                    ("nightlight", 14, 16, ["butter", "sky", "rose", "mint"], "table", "deco"),
                                    ("key_board", 40, 18, ["oak", "white", "sky"], "wall", "deco"),
                                    ("suitcase", 48, 50, ["coral", "navy", "butter", "walnut", "mint"], "floor", "deco"),
                                    ("umbrella", 16, 80, ["coral", "sky", "butter", "navy", "plum"], "floor", "clothes"),
                                    ("umbrella_stand", 26, 55, ["metal", "coral", "navy"], "floor", "clothes"),
                                    ("mirror", 50, 80, ["oak", "white", "#e0b84a", "black"], "wall", "deco"),
                                    ("mirror_stand", 50, 160, ["oak", "white", "black", "rose"], "floor", "deco")):
    extra = {"states": {"on": {"state": "on"}}, "state0": "off"} if st in ("speaker", "nightlight") else {}
    prefix = {"duvet": "bed", "pillow": "bed", "umbrella_stand": "furn", "speaker": "elec", "remote": "elec"}.get(st, "deco")
    S(f"{prefix}_{st}", HS.small, st, w, h, grp,
      "item", names, second={"duvet": "cream", "pillow": "coral", "throw": "cream", "speaker": "grey", "suitcase": "cream",
                             "umbrella": "cream", "mirror": MIRROR, "mirror_stand": MIRROR, "nightlight": "rose",
                             "alarm": "cream", "key_board": "coral"}.get(st, "cream"),
      third={"remote": "coral", "speaker": "black", "alarm": "metal", "key_board": "metal"}.get(st, "metal"),
      placement=place, hold="two_hands" if st in ("duvet", "pillow", "throw", "suitcase") else ("one_hand" if st == "umbrella" else None),
      grip=[0.5, 0.95] if st == "umbrella" else None, **extra)

# ------------------------------------------------------------------ Kleidung
for st, w, h, names in (("shirt", 40, 38, ["coral", "sky", "mint", "butter", "white", "navy", "rose"]),
                        ("pants", 34, 60, ["denim", "grey", "sand", "black"]), ("dress", 44, 70, ["rose", "sky", "butter", "lilac", "coral"]),
                        ("jacket", 50, 55, ["navy", "rust", "sage", "butter"]), ("shoes", 28, 12, ["coral", "sky", "white", "black", "rose", "mint"]),
                        ("slippers", 28, 10, ["rose", "sky", "grey"]), ("boots", 28, 30, ["yellow", "coral", "green", "navy"]),
                        ("hat", 30, 18, ["coral", "sky", "butter", "navy", "sage"])):
    S(f"cloth_{st}", HS.small, st, w, h, "clothes", "item", names, second={"shirt": "white", "pants": "black", "dress": "white",
                                                                          "jacket": "butter", "shoes": "white", "boots": "black"}.get(st, "cream"),
      third="metal", hold="one_hand" if h > 50 else None)

# ------------------------------------------------------------------ Kinderzimmer & Baby
for animal, names in (("bunny", ["cream", "rose"]), ("bear", ["oak", "walnut"]), ("elephant", ["grey", "sky"]),
                      ("unicorn", ["white", "lilac"]), ("dino", ["mint", "green"]), ("cat", ["orange", "grey"])):
    T(id=f"toy_plush_{animal}", fn=KI.plush, w=28, h=34, kw={"animal": animal}, group="toys", category="toy", placement="table",
      hold="one_hand", grip=[0.5, 0.5], variants=[(n, cols(n, "rose" if animal != "dino" else "butter",
                                                         "butter" if animal == "unicorn" else "walnut")) for n in names])
for st, w, h, names, extra in (("dollhouse", 80, 95, ["rose", "sky", "mint"], {"container": {"slots": 6, "max_item_h_cm": 30}}),
                               ("shop_stand", 100, 125, ["coral", "sky", "mint"], {"surface_h": 62}),
                               ("tipi", 120, 170, ["cream", "sky", "rose"], {"seat": {"h": 4, "pose": "sit", "slots": 2}}),
                               ("ball_pit", 130, 40, ["sky", "rose"], {"seat": {"h": 25, "pose": "sit", "slots": 2}}),
                               ("pram", 46, 50, ["rose", "sky", "lilac"], {}), ("guitar", 30, 80, ["coral", "oak", "sky"], {})):
    T(id=f"toy_{st}", fn=KI.toy_big, w=w, h=h, kw={"style": st}, group="toys", category="toy",
      hold="one_hand" if st == "guitar" else ("two_hands" if st == "pram" else "none"), grip=[0.5, 0.9] if st in ("guitar", "pram") else None,
      variants=[(n, cols(n, {"dollhouse": "cream", "shop_stand": "cream", "tipi": "coral", "ball_pit": "coral", "pram": "cream",
                             "guitar": "cream"}[st], {"dollhouse": "coral", "shop_stand": "oak", "tipi": "butter", "ball_pit": "butter",
                                                      "pram": "metal", "guitar": "walnut"}[st])) for n in names], **extra)
T(id="furn_changing", fn=KI.toy_big, w=90, h=95, kw={"style": "changing"}, group="baby", category="furniture", **OPEN,
  seat={"h": 97, "pose": "lie", "slots": 1}, variants=[(n, cols("white", n, "oak")) for n in ["white", "mint", "sky", "rose"]])
for st, w, h, names in (("rattle", 8, 16, ["butter", "sky", "rose"]), ("baby_bottle", 7, 17, ["sky", "rose", "mint"]),
                        ("pacifier", 6, 7, ["sky", "rose", "mint", "butter"])):
    S(f"baby_{st.replace('baby_', '')}", HS.small, st, w, h, "baby", "item", names, second="cream" if st != "baby_bottle" else "white", third="coral")

# ------------------------------------------------------------------ Bad
for st, w, h, names, extra in (("tub", 170, 60, ["white", "sky", "mint", "rose"], {**ON, "seat": {"h": 30, "pose": "sit", "slots": 2}}),
                               ("shower", 90, 210, ["white", "grey", "sky"], {**ON}),
                               ("toilet", 42, 80, ["white", "sky", "black"], {**ON, "seat": {"h": 42, "pose": "sit", "slots": 1}}),
                               ("washbasin", 60, 90, ["white", "sky", "mint"], {**ON})):
    T(id=f"bath_{st}", fn=HB.big, w=w, h=h, kw={"style": st}, group="bathroom", category="furniture",
      variants=[(n, cols(n, WATER if st != "shower" else MIRROR, CHROME)) for n in names], **extra)
cab("bath_cabinet", 40, 170, "D/W/O/D", "bathroom", ["white", "sky", "oak"], legs="short")
cab("bath_cabinet_low", 70, 60, "D|D", "bathroom", ["white", "sage"], legs="none", surface_h=60)
T(id="bath_mirror_cabinet", fn=CB.cabinet, w=60, h=65, kw={"layout": "D|D", "top": "none", "legs": "none"}, group="bathroom",
  category="furniture", placement="wall", **OPEN, variants=[(n, cols(n, MIRROR, CHROME)) for n in ["white", "oak", "grey"]])
T(id="bath_towel_rail", fn=KI.toy_big, w=60, h=55, kw={"style": "towel_rail"}, group="bathroom", category="furniture",
  placement="wall", variants=[(n, cols(n, "cream", CHROME)) for n in ["sky", "rose", "mint"]])
for st, w, h, names, place in (("cup", 8, 10, ["sky", "mint", "rose", "white"], "table"), ("bath_scale", 30, 5, ["white", "sky", "black"], "floor"),
                               ("potty", 30, 26, ["sky", "rose", "mint", "white"], "floor"), ("robe", 50, 110, ["white", "sky", "rose", "navy"], "floor"),
                               ("sponge", 12, 6, ["butter", "rose", "mint"], "table")):
    S(f"bath_{st.replace('bath_', '')}", HS.small, st, w, h, "bathroom", "item", names,
      second={"cup": "coral", "bath_scale": "grey", "potty": "white", "robe": "cream", "sponge": "mint"}.get(st, "cream"),
      third="butter", placement=place, hold="one_hand" if st == "robe" else None, grip=[0.5, 0.95] if st == "robe" else None)

# ------------------------------------------------------------------ Waschen, Putzen, Keller, Garage, Büro
for st, w, h, names, extra in (("dryer", 60, 85, ["white", "grey", "sky"], {**ON, "anim": {"on": "shake"}, "surface_h": 85}),
                               ("freezer", 100, 85, ["white", "grey"], {"surface_h": 85})):
    T(id=f"app_{st}", fn=HB.big, w=w, h=h, kw={"style": st}, group="household", category="furniture",
      variants=[(n, cols(n, "sky", "metal")) for n in names], **extra)
for st, w, h, names, extra in (("drying_rack", 110, 100, ["white", "sky"], {}), ("ironing_board", 120, 90, ["sky", "rose", "mint"], {}),
                               ("vacuum", 40, 100, ["coral", "sky", "grey", "mint"], {})):
    T(id=f"home_{st}", fn=HB.big, w=w, h=h, kw={"style": st}, group="household", category="furniture",
      variants=[(n, cols(n, "coral" if n != "coral" else "butter", "metal")) for n in names], **extra)
T(id="home_iron", fn=KI.toy_big, w=26, h=16, kw={"style": "iron"}, group="household", category="item", placement="table",
  hold="one_hand", grip=[0.45, 0.85], **ON, variants=[(n, cols(n, "grey", CHROME)) for n in ["sky", "coral", "white"]])
T(id="work_tool_wall", fn=KI.toy_big, w=120, h=80, kw={"style": "tool_wall"}, group="workshop", category="furniture",
  placement="wall", variants=[(n, cols(n, "coral", "metal")) for n in ["oak", "grey", "sky"]])
for st, w, h, names in (("mower", 60, 100, ["coral", "green", "sky"]), ("mower_ride", 180, 120, ["green", "coral"])):
    T(id=f"garden_{st}", fn=KI.toy_big, w=w, h=h, kw={"style": st}, group="vehicles", category="item",
      variants=[(n, cols(n, "black", "metal")) for n in names], **({"seat": {"h": 55, "pose": "sit", "slots": 1}} if st == "mower_ride" else {}))
for st, w, h, names in (("hatch", 380, 150, ["coral", "sky", "butter"]), ("sedan", 460, 145, ["navy", "grey", "white"]),
                        ("van", 480, 195, ["white", "mint", "sky"]), ("jeep", 420, 180, ["green", "sand", "black"]),
                        ("beetle", 400, 150, ["rose", "mint", "butter"]), ("pickup", 520, 185, ["rust", "navy", "white"])):
    T(id=f"veh_car_{st}", fn=HB.car, w=w, h=h, kw={"style": st}, group="vehicles", category="garage",
      seat={"h": 60, "pose": "sit", "slots": 2}, variants=[(n, cols(n, MIRROR, CHROME)) for n in names])

# ------------------------------------------------------------------ Garten (groß): säen, gießen, ernten
CROPS = {"carrot": "orange", "tomato": "coral", "lettuce": "leaf_light", "strawberry": "coral", "pumpkin": "orange", "sunflower": "yellow"}
for crop, fruit in CROPS.items():
    T(id=f"garden_seeds_{crop}", fn=YA.yard, w=9, h=13, kw={"style": "seeds", "crop": crop}, group="yard", category="item",
      placement="table", hold="one_hand", grip=[0.5, 0.5], tags=["seeds", f"crop_{crop}"],
      variants=[("pack", cols("leaf", fruit, "butter" if crop != "lettuce" else "sky"))])
for size, w, h in (("m", 120, 80), ("l", 180, 80)):
    for crop in ("carrot", "tomato", "lettuce"):
        T(id=f"garden_raised_bed_{size}_{crop}", fn=YA.yard, w=w, h=h, kw={"style": "raised_bed", "crop": crop}, group="yard",
          category="item", tags=["bed", "needs_water"], **GROW,
          variants=[(n, cols("leaf", CROPS[crop], n)) for n in (["oak", "walnut"] if size == "m" else ["grey"])])
for crop in ("carrot", "strawberry", "pumpkin", "sunflower"):
    T(id=f"garden_veg_bed_{crop}", fn=YA.yard, w=160, h=24, kw={"style": "veg_bed", "crop": crop}, group="yard", category="item",
      tags=["bed", "needs_water"], **GROW, variants=[("oak", cols("leaf", CROPS[crop], "oak"))])
for size, w in (("s", 100), ("m", 160), ("l", 240)):
    T(id=f"garden_flower_bed_{size}", fn=YA.yard, w=w, h=45, kw={"style": "flower_bed", "seed": w}, group="yard", category="item",
      tags=["bed", "needs_water"], **DRY, variants=[(n, cols("leaf", n, "#b8b2a7")) for n in ["rose", "butter", "lilac", "coral"][: 4 if size == "m" else 2]])
T(id="garden_sprinkler", fn=YA.yard, w=30, h=16, kw={"style": "sprinkler"}, group="yard", category="item", placement="floor",
  hold="one_hand", grip=[0.5, 0.5], **ON, variants=[(n, cols(n, WATER, "metal")) for n in ["green", "coral", "sky"]])
for st, w, h in (("spade", 20, 110), ("rake", 40, 145), ("shovel", 26, 110)):
    T(id=f"garden_{st}", fn=YA.yard, w=w, h=h, kw={"style": st}, group="yard", category="item", hold="one_hand", grip=[0.5, 0.8],
      variants=[(n, cols(n, "metal" if st != "rake" else "green", "oak")) for n in ["coral", "green", "sky"]])
for st, w, h, names in (("fence_rustic", 150, 90, ["oak", "walnut", "white"]), ("fence_lattice", 120, 150, ["white", "oak", "sage"])):
    T(id=f"garden_{st}", fn=YA.yard, w=w, h=h, kw={"style": st}, group="yard", category="item",
      variants=[(n, cols(n, "rose", "leaf")) for n in names])
for kid, w, h, flowers in (("box", 150, 110, False), ("low", 150, 60, True), ("tall", 120, 180, False)):
    T(id=f"garden_hedge_{kid}", fn=YA.yard, w=w, h=h, kw={"style": "hedge", "state": "" if flowers else "plain", "seed": w + h},
      group="yard", category="item", variants=[(n, cols(n, "rose", "walnut")) for n in (["leaf", "leaf_dark"] if not flowers else ["leaf_light"])])
T(id="garden_gate", fn=YA.yard, w=100, h=110, kw={"style": "gate"}, group="yard", category="item", **OPEN,
  variants=[(n, cols(n, "cream", "walnut" if n != "walnut" else "oak")) for n in ["white", "oak", "walnut", "sage"]])
for st, w, h, names in (("path_stones", 160, 34, ["grey", "sand"]), ("path_gravel", 200, 40, ["sand", "grey"]), ("path_deck", 200, 40, ["oak", "walnut"])):
    T(id=f"garden_{st}", fn=YA.yard, w=w, h=h, kw={"style": st}, group="yard", category="deco",
      placement="rug", variants=[(n, cols(n, "cream", "walnut")) for n in names])

# ------------------------------------------------------------------ Garten: sitzen, feiern, grillen
for st, w, h, names in (("table_bistro", 70, 74, ["white", "sage", "black"]), ("table_wood", 160, 75, ["oak", "walnut"]),
                        ("table_plastic", 120, 72, ["white", "green"])):
    T(id=f"garden_table_{st.split('_')[1]}", fn=PA.patio, w=w, h=h, kw={"style": st}, group="patio", category="furniture",
      surface_h=h, variants=[(n, cols(n, "coral", "metal" if st != "table_wood" else n)) for n in names])
for st, w, h, names, sh in (("chair_bistro", 45, 88, ["white", "sage", "black"], 45), ("chair_wood", 50, 90, ["oak", "walnut"], 45),
                            ("chair_plastic", 50, 85, ["white", "green", "coral"], 45), ("lounger", 190, 70, ["sky", "coral", "butter", "sage"], 32)):
    T(id=f"garden_chair_{st.split('_')[-1]}" if st != "lounger" else "garden_lounger", fn=PA.patio, w=w, h=h, kw={"style": st},
      group="patio", category="furniture", seat={"h": sh, "pose": "sit" if st != "lounger" else "lie", "slots": 1},
      variants=[(n, cols(n, "coral" if n != "coral" else "butter", "metal" if st in ("chair_bistro", "lounger") else n)) for n in names])
for st, w, h, names, extra in (("hammock", 230, 110, ["coral", "sky", "butter"], {"seat": {"h": 50, "pose": "lie", "slots": 1}}),
                               ("swing_bench", 200, 180, ["sky", "coral", "sage"], {"seat": {"h": 50, "pose": "sit", "slots": 3}}),
                               ("grill_gas", 130, 110, ["black", "coral", "metal"], {**ON, "anim": {"on": "pulse"},
                                                                                    "container": {"slots": 4, "max_item_h_cm": 30},
                                                                                    "tags": ["open_top", "cook_host"]}),
                               ("fire_bowl", 70, 45, ["black", "rust"], {**ON, "anim": {"on": "pulse"}}),
                               ("lights", 220, 40, ["butter", "coral", "sky", "mint"], {**ON, "placement": "wall"}),
                               ("bunting", 220, 40, ["coral", "sky", "butter", "mint"], {"placement": "wall"}),
                               ("pavilion", 300, 260, ["white", "sky", "coral"], {}), ("gazebo", 300, 300, ["white", "oak"], {})):
    gid = "garden_pavilion" + ("_wood" if st == "gazebo" else "") if st in ("pavilion", "gazebo") else f"garden_{st}"
    T(id=gid, fn=PA.patio, w=w, h=h, kw={"style": st}, group="patio", category="furniture" if st not in ("lights", "bunting") else "deco",
      variants=[(n, cols(n, {"hammock": "cream", "swing_bench": "cream", "grill_gas": "orange", "fire_bowl": "orange",
                             "lights": "rose", "bunting": "white", "pavilion": "cream" if n != "white" else "coral",
                             "gazebo": "rust" if n == "white" else "green"}[st], "metal" if st not in ("gazebo",) else "oak")) for n in names],
      **extra)

# ------------------------------------------------------------------ Garten: Wasser, Spielen, Bauten
for kid, w, h, names in (("s", 240, 70, ["sky", "coral"]), ("l", 360, 90, ["sky", "grey"])):
    T(id=f"garden_pool_frame_{kid}", fn=YA.yard, w=w, h=h, kw={"style": "pool_frame"}, group="water", category="furniture",
      seat={"h": 30, "pose": "sit", "slots": 3}, variants=[(n, cols(n, WATER, "white")) for n in names])
T(id="garden_pool_big", fn=YA.yard, w=500, h=60, kw={"style": "pool_big"}, group="water", category="furniture",
  seat={"h": 35, "pose": "sit", "slots": 4}, variants=[(n, cols(n, WATER, CHROME)) for n in ["white", "#b8b2a7"]])
for kid, w, h in (("s", 180, 50), ("m", 260, 70), ("l", 360, 90)):
    T(id=f"garden_pond_{kid}", fn=YA.yard, w=w, h=h, kw={"style": "pond", "seed": w}, group="water", category="deco",
      placement="rug", variants=[("stone", cols("#b8b2a7", WATER, "leaf_dark"))])
T(id="garden_lily", fn=YA.yard, w=30, h=10, kw={"style": "lily"}, group="water", category="item", placement="table",
  hold="one_hand", grip=[0.5, 0.3], variants=[(n, cols(n, "butter", "leaf")) for n in ["rose", "white", "butter"]])
T(id="garden_fountain", fn=YA.yard, w=100, h=130, kw={"style": "fountain"}, group="water", category="furniture",
  **{**ON, "anim": {"on": "pulse"}}, variants=[(n, cols(n, WATER, "grey")) for n in ["#b8b2a7", "sand", "white"]])
for st, w, h, names, extra in (("trampoline", 260, 230, ["green", "sky", "coral"], {"seat": {"h": 60, "pose": "sit", "slots": 3}}),
                               ("treehouse", 320, 420, ["leaf", "leaf_light"], {}), ("greenhouse", 250, 230, ["white", "green"], {}),
                               ("compost", 100, 90, ["oak", "green"], {}), ("bin", 60, 110, ["grey", "sky", "walnut", "butter"], OPEN),
                               ("mailbox", 40, 120, ["coral", "navy", "butter", "green"], OPEN),
                               ("doghouse", 100, 95, ["coral", "sky", "oak"], {}), ("shed", 250, 240, ["sage", "coral", "sky"], OPEN),
                               ("clothesline", 200, 180, ["metal", "white"], {}), ("rain_barrel", 60, 90, ["green", "walnut"], {})):
    T(id=f"garden_{st}", fn=PA.patio, w=w, h=h, kw={"style": st}, group="patio" if st in ("trampoline",) else "yard",
      category="furniture", variants=[(n, cols(n, {"trampoline": "sky", "treehouse": "coral", "greenhouse": "sky", "compost": "rust",
                                                   "bin": "black", "mailbox": "cream", "doghouse": "rust", "shed": "rust",
                                                   "clothesline": "coral", "rain_barrel": "sky"}[st],
                                                  {"trampoline": "metal", "treehouse": "walnut", "greenhouse": "leaf", "compost": "walnut",
                                                   "bin": "black", "mailbox": "metal", "doghouse": "oak", "shed": "oak",
                                                   "clothesline": "metal", "rain_barrel": "metal"}[st])) for n in names], **extra)
