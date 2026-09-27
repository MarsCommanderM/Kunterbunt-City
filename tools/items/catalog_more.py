"""
Katalog, Teil P07-Inventar 2 (Wunsch 👤: „Inliner, Skateboard-Ausrüstung, Kindersitz, Schal, Mütze, Handschuhe …
Gartenzaun groß/klein, Fahrrad, Roller, Tischtennisplatte, Schwerlastregale, Weinkeller, Insektenhaus,
Schildkröten-Gehege, Gartenlaube …“). Pflichtliste: data/inventory.json.
"""
from __future__ import annotations

from . import cellar as CE
from . import garden_extra as GE
from . import leisure as LE
from . import outdoor as OD
from . import playroom as PR
from .catalog import S, T, cols

OPEN = {"states": {"open": {"state": "open"}}, "state0": "closed"}
ON = {"states": {"on": {"state": "on"}}, "state0": "off"}
BRIGHT = ["coral", "sky", "butter", "mint", "plum", "orange", "teal", "rose"]


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second if n != second else "cream", third)) for n in names]


# ------------------------------------------------------------------ Sport & Freizeit
for st, w, h, names, grp, extra in (
        ("inline_skates", 36, 34, ["coral", "sky", "mint", "black", "rose"], "sport", {}),
        ("roller_skates", 34, 30, ["rose", "white", "sky"], "sport", {}),
        ("pads", 36, 22, ["black", "coral", "sky"], "sport", {}),
        ("table_tennis", 274, 76, ["green", "navy"], "sport", {"surface_h": 76, "hold": "none"}),
        ("tt_paddle", 16, 26, ["coral", "black", "sky"], "sport", {}),
        ("badminton", 22, 66, ["sky", "coral", "mint"], "sport", {"hold": "one_hand", "grip": [0.5, 0.1]}),
        ("goal_small", 120, 80, ["white", "coral"], "sport", {"hold": "none"}),
        ("skis", 30, 145, ["coral", "sky", "black"], "winter", {"hold": "one_hand", "grip": [0.5, 0.45]}),
        ("snowboard", 28, 140, ["teal", "coral", "plum"], "winter", {"hold": "one_hand", "grip": [0.5, 0.5]}),
        ("fishing_rod", 60, 145, ["green", "navy"], "sport", {"hold": "one_hand", "grip": [0.1, 0.08]}),
        ("jump_rope", 40, 30, ["coral", "sky", "butter"], "sport", {}),
        ("hoop", 70, 70, ["coral", "teal", "plum", "butter"], "sport", {"hold": "none"}),
        ("frisbee", 25, 5, ["coral", "sky", "butter", "mint"], "sport", {})):
    second = {"inline_skates": "black", "roller_skates": "coral", "pads": "grey", "table_tennis": "white", "tt_paddle": "black",
              "badminton": "cream", "goal_small": "white", "skis": "cream", "snowboard": "cream", "fishing_rod": "coral",
              "jump_rope": "oak", "hoop": "butter", "frisbee": "cream"}[st]
    S(f"sport_{st}", LE.sporty, st, w, h, grp, "sport", names, second=second, third="metal", **extra)
for st, w, h, names, grp, cat, extra in (
        ("bike_seat", 40, 60, ["navy", "coral", "grey"], "vehicles", "item", {"seat": {"h": 25, "pose": "sit", "slots": 1}}),
        ("car_seat", 45, 65, ["navy", "grey", "rose", "sky"], "baby", "item", {"seat": {"h": 20, "pose": "sit", "slots": 1}}),
        ("balance_bike", 85, 55, ["coral", "sky", "mint", "butter"], "bikes", "toy", {"seat": {"h": 36, "pose": "sit", "slots": 1}}),
        ("bike_trailer", 140, 90, ["coral", "sky", "butter"], "bikes", "item", {"seat": {"h": 25, "pose": "sit", "slots": 2}})):
    prefix = {"bike_seat": "veh", "car_seat": "baby", "balance_bike": "play", "bike_trailer": "veh"}[st]
    S(f"{prefix}_{st}", LE.sporty, st, w, h, grp, cat, names, second="butter" if st != "car_seat" else "grey",
      third="metal", hold="two_hands" if h <= 56 else "none", **extra)
S("play_kids_bike", OD.playground, "bicycle", 110, 65, "bikes", "toy", ["coral", "sky", "mint", "rose", "butter"],
  second="cream", third="metal", hold="none", seat={"h": 50, "pose": "sit", "slots": 1})
S("play_scooter_mini", OD.playground, "scooter", 45, 65, "bikes", "toy", ["rose", "butter", "mint"], second="cream",
  third="metal", hold="none")

# ------------------------------------------------------------------ Kleidung & Zubehör
for st, w, h, names in (("scarf", 34, 20, ["coral", "sky", "butter", "mint", "plum", "navy", "rust"]),
                        ("beanie", 24, 22, ["coral", "sky", "butter", "mint", "plum", "navy", "grey"]),
                        ("gloves", 26, 20, ["coral", "sky", "butter", "mint", "navy", "grey"]),
                        ("mittens", 26, 20, ["rose", "teal", "orange"]),
                        ("cap", 30, 16, ["coral", "sky", "navy", "green", "black"]),
                        ("raincoat", 50, 70, ["yellow", "coral", "sky", "green"]),
                        ("sunglasses", 16, 6, ["black", "coral", "sky", "rose"]),
                        ("backpack", 30, 38, ["coral", "sky", "mint", "plum", "butter"]),
                        ("handbag", 30, 28, ["walnut", "coral", "navy"])):
    gid = "cloth_gloves_mittens" if st == "mittens" else f"cloth_{st}"
    S(gid, LE.outfit, st, w, h, "clothes", "item", names,
      second={"scarf": "cream", "beanie": "cream", "gloves": "cream", "mittens": "cream", "cap": "white", "raincoat": "navy",
              "sunglasses": "black", "backpack": "butter", "handbag": "butter"}[st], third="butter",
      hold="one_hand" if st == "raincoat" else None, grip=[0.5, 0.95] if st == "raincoat" else None,
      **({"container": {"slots": 4, "max_item_h_cm": 25}} if st in ("backpack", "handbag") else {}))

# ------------------------------------------------------------------ Musik
for st, w, h, names, extra in (("drums", 120, 110, ["coral", "navy", "black"], {}),
                               ("keyboard", 100, 90, ["black", "white"], {"surface_h": 90}),
                               ("violin", 20, 60, ["walnut", "oak"], {"hold": "one_hand", "grip": [0.5, 0.85]}),
                               ("flute", 4, 32, ["oak", "cream", "sky"], {})):
    S(f"music_{st}", LE.music, st, w, h, "toys", "toy", names, second={"drums": "cream", "keyboard": "cream", "violin": "black",
                                                                    "flute": "walnut"}[st], third="metal", **extra)

# ------------------------------------------------------------------ Keller & Haushalt
for st, w, h, names, grp, extra in (
        ("heavy_shelf", 120, 180, ["oak", "grey", "black"], "storage", {"hold": "none"}),
        ("wine_rack", 80, 100, ["walnut", "oak", "black"], "storage", {"hold": "none"}),
        ("barrel", 90, 70, ["oak", "walnut"], "storage", {"hold": "none"}),
        ("crate", 40, 30, ["coral", "sky", "green", "butter"], "storage", {}),
        ("box", 50, 32, ["sky", "cream", "coral", "mint", "grey", "oak"], "storage",
         {"container": {"slots": 6, "max_item_h_cm": 28}}),
        ("jars", 30, 20, ["coral", "orange", "plum"], "kitchen", {}),
        ("sack", 40, 55, ["sand", "oak"], "storage", {}),
        ("boiler", 60, 150, ["white", "grey"], "household", {**ON, "hold": "none"}),
        ("wine", 8, 32, ["green", "walnut", "rose"], "kitchen", {})):
    S(f"cellar_{st}", CE.cellar, st, w, h, grp, "item" if st not in ("jars", "wine") else "kitchen", names,
      second={"heavy_shelf": "sand", "wine_rack": "green", "barrel": "metal", "crate": "green", "box": "cream", "jars": "white",
              "sack": "walnut", "boiler": "sky", "wine": "butter"}[st],
      third={"barrel": "metal", "jars": "white", "sack": "oak", "wine": "cream"}.get(st, "metal"), **extra)
for st, w, h, names, grp, place, extra in (("flashlight", 22, 7, ["black", "coral", "sky"], "household", "table", ON),
                                           ("bucket", 30, 30, ["coral", "sky", "mint", "grey"], "household", "floor", {}),
                                           ("dustpan", 30, 40, ["coral", "sky"], "household", "floor", {}),
                                           ("pinboard", 60, 45, ["oak", "white", "black"], "deco", "wall", {}),
                                           ("calendar", 30, 42, ["sky", "rose", "mint"], "deco", "wall", {})):
    prefix = "deco" if st in ("pinboard", "calendar") else "home"
    S(f"{prefix}_{st}", CE.cellar, st, w, h, grp, "item", names, second={"flashlight": "butter", "bucket": "cream",
                                                                        "dustpan": "black", "pinboard": "coral",
                                                                        "calendar": "coral"}[st],
      third={"pinboard": "oak", "calendar": "white"}.get(st, "metal"), placement=place, **extra)

# ------------------------------------------------------------------ Kinderzimmer & Baby
for st, w, h, names, grp, extra in (
        ("play_kitchen", 90, 100, ["cream", "mint", "rose"], "toys", {"surface_h": 55, "hold": "none"}),
        ("workbench", 80, 90, ["sky", "coral"], "toys", {"surface_h": 55, "hold": "none"}),
        ("board_game", 40, 18, ["coral", "sky", "mint", "butter", "plum"], "toys", {}),
        ("crayons", 12, 16, ["coral", "sky", "butter"], "toys", {}),
        ("paints", 26, 14, ["sky", "coral", "black"], "toys", {}),
        ("stacker", 16, 24, ["cream", "oak", "sky"], "baby", {}),
        ("play_mat", 120, 40, ["mint", "sky", "rose"], "baby", {"placement": "rug", "hold": "none"}),
        ("bouncer", 70, 60, ["sky", "rose", "grey"], "baby", {"seat": {"h": 12, "pose": "lie", "slots": 1}, "hold": "none"}),
        ("baby_monitor", 8, 14, ["white", "sky"], "baby", {**ON}),
        ("diapers", 30, 26, ["sky", "rose"], "baby", {}),
        ("baby_bath", 80, 80, ["sky", "rose", "mint"], "baby", {**ON, "hold": "none"})):
    gid = st if st.startswith("baby_") else (f"baby_{st}" if st in ("stacker", "play_mat", "bouncer", "diapers") else f"toy_{st}")
    S(gid, PR.playroom, st, w, h, grp, "toy" if grp == "toys" else "item", names,
      second={"play_kitchen": "sky", "workbench": "butter", "board_game": "butter", "crayons": "sky", "paints": "sky",
              "stacker": "coral", "play_mat": "butter", "bouncer": "cream", "baby_monitor": "sky", "diapers": "cream",
              "baby_bath": "cream"}[st], third={"play_kitchen": "oak", "workbench": "oak", "paints": "cream"}.get(st, "butter"),
      **extra)

# ------------------------------------------------------------------ Zäune – jede Art in klein, mittel und groß
FENCES = {"picket": ["white", "oak", "sage", "sky"], "wire": ["green", "grey"], "metal": ["black", "white", "green"],
          "privacy": ["oak", "grey", "walnut"], "bamboo": ["sand"], "rail": ["oak", "white"]}
for style, names in FENCES.items():
    for size, w, h in (("s", 100, 50), ("m", 150, 100), ("l", 200, 180)):
        if style == "rail" and size == "l":
            continue
        T(id=f"garden_fence_{style}_{size}", fn=GE.fence, w=w, h=h, kw={"style": style}, group="fences", category="item",
          variants=V(names, "coral", "walnut" if style != "bamboo" else "leaf"))
T(id="garden_edging", fn=GE.fence, w=100, h=16, kw={"style": "edging"}, group="fences", category="item",
  variants=V(["oak", "grey", "terracotta"], "walnut", "leaf"))

# ------------------------------------------------------------------ Garten-Extras
for st, w, h, names, grp, extra in (
        ("insect_hotel", 50, 110, ["oak", "sage", "coral"], "yard", {}),
        ("tortoise_pen", 200, 70, ["leaf_light", "leaf", "sage"], "yard", {}),
        ("arbor", 300, 280, ["sage", "sky", "rose", "oak"], "yard", {}),
        ("hutch", 120, 100, ["oak", "white", "sage"], "yard", {"container": {"slots": 2, "max_item_h_cm": 40}}),
        ("coop", 140, 130, ["rust", "oak"], "yard", {}),
        ("bird_bath", 50, 80, ["#b8b2a7", "sand"], "yard", {}),
        ("bird_feeder", 40, 140, ["oak", "white", "sky"], "yard", {}),
        ("parasol", 250, 240, ["coral", "sky", "butter", "sage", "cream"], "patio",
         {"states": {"closed": {"state": "closed"}}, "state0": "open"}),
        ("sun_sail", 300, 250, ["cream", "sky", "coral"], "patio", {}),
        ("torch", 16, 150, ["walnut", "black", "oak"], "patio", {**ON, "anim": {"on": "pulse"}}),
        ("picnic_blanket", 180, 60, ["coral", "sky", "mint", "butter"], "patio", {"placement": "rug",
                                                                                  "seat": {"h": 1, "pose": "sit", "slots": 3}}),
        ("picnic_basket", 40, 34, ["oak", "walnut"], "patio", {"container": {"slots": 5, "max_item_h_cm": 25}}),
        ("hose_reel", 60, 90, ["green", "coral"], "yard", {}),
        ("swing_set", 300, 210, ["oak", "sky", "coral"], "patio", {"seat": {"h": 42, "pose": "sit", "slots": 2}}),
        ("playhouse", 150, 200, ["butter", "rose", "sky"], "patio", {"seat": {"h": 8, "pose": "sit", "slots": 2}})):
    base = {"planter": "garden_planter"}.get(st, f"garden_{st}")
    second = {"insect_hotel": "rust", "tortoise_pen": "butter", "arbor": "rust", "hutch": "rust", "coop": "rust", "bird_bath": "sky",
              "bird_feeder": "butter", "parasol": "cream", "sun_sail": "cream", "torch": "orange", "picnic_blanket": "white",
              "picnic_basket": "coral", "hose_reel": "coral", "swing_set": "coral", "playhouse": "coral"}[st]
    third = {"tortoise_pen": "oak", "arbor": "oak", "hutch": "oak", "coop": "oak", "bird_feeder": "walnut", "bird_bath": "walnut",
             "insect_hotel": "oak", "swing_set": "oak", "playhouse": "oak", "torch": "walnut", "parasol": "oak"}.get(st, "metal")
    T(id=base, fn=GE.garden_extra, w=w, h=h, kw={"style": st}, group=grp, category="item",
      placement=extra.pop("placement", "floor"), hold="one_hand" if st == "picnic_basket" else "none",
      grip=[0.5, 0.95] if st == "picnic_basket" else None,
      variants=[(n, cols(n, second if n != second else "cream", third)) for n in names], **extra)
for kind, w, h, names in (("box", 80, 60, ["terracotta", "grey", "white"]), ("round", 50, 70, ["terracotta", "cream", "sky"]),
                          ("trough", 120, 50, ["grey", "oak"]), ("tall", 40, 90, ["grey", "white", "navy"]),
                          ("basket", 50, 55, ["oak", "walnut"]), ("tub", 60, 55, ["oak", "walnut"])):
    T(id=f"garden_planter_{kind}", fn=GE.garden_extra, w=w, h=h, kw={"style": f"planter_{kind}", "seed": w + h}, group="yard",
      category="item", tags=["needs_water"], variants=[(n, cols(n, {"box": "rose", "round": "butter", "trough": "lilac", "tall": "coral",
                                                                     "basket": "rose", "tub": "butter"}[kind], "leaf")) for n in names])
S("garden_slide", OD.playground, "slide", 240, 150, "patio", "item", ["coral", "sky", "butter"], second="cream", third="oak",
  hold="none")
S("garden_sandbox", OD.playground, "sandpit", 150, 30, "patio", "item", ["butter"], second="coral", third="oak", hold="none",
  seat={"h": 16, "pose": "sit", "slots": 3})
S("garden_sandbox_big", OD.playground, "sandpit", 220, 36, "patio", "item", ["butter"], second="sky", third="walnut", hold="none",
  seat={"h": 20, "pose": "sit", "slots": 4})
