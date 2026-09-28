"""
Item-Katalog (P04b-T09): WAS es gibt – echte Größe (cm), Zeichnung, Farbvarianten, Spielregeln.

Jede Vorlage = eine Zeichnung (Sprite mit Farbzonen). Jede Farbvariante = ein eigenes Item im Spiel
(gleiches Sprite, andere Zonen-Farben) → hunderte Items ohne hunderte Bilder.
Gruppen (`group`) = Reiter im Katalog; jedes Item ist in JEDEM Raum einsetzbar.
Bestehende IDs (Phase 02/03, `legacy`) behalten ID und Maßstab-Eintrag und bekommen nur die neue Grafik.
"""
from __future__ import annotations

from . import furniture as F
from . import plants as P

# ------------------------------------------------------------------ Farben (Namen → Hex)
C = {
    "cream": "#f5f3ee", "linen": "#e8e2d8", "sand": "#d8cfc2", "taupe": "#a1887f", "grey": "#6d6f78", "navy": "#2e3140",
    "mint": "#9fc3a0", "sage": "#dbe8d9", "green": "#5f8f6a", "sky": "#a9c3dd", "blue": "#6f8fb8", "denim": "#3c4f7a",
    "butter": "#f6d98a", "yellow": "#f4c95d", "rose": "#f0b6c2", "coral": "#e07a7a", "rust": "#b8452f", "lilac": "#b9a6d6",
    "plum": "#7a5ea8", "teal": "#48b0a0", "orange": "#f09a55", "white": "#fbfaf7", "black": "#2a2a30",
    "oak": "#d4a86e", "walnut": "#8a5e3f", "pine": "#e3c79a", "dark_wood": "#5a463a", "metal": "#9aa6b4",
    "terracotta": "#c96a4a", "leaf": "#5f8f6a", "leaf_light": "#7fae6a", "leaf_dark": "#3f6a4f",
    "gold": "#e0b84a", "stone": "#b8b2a7", "brick": "#c0664f",
}


def cols(*names: str) -> list[str]:
    return [C.get(n, n) for n in names]


# ------------------------------------------------------------------ Vorlagen
# Felder: id, fn, w, h, kw, group, category, hold, placement, grip, seat {h, pose, slots}, surface_h,
#         container {slots, max_item_h_cm}, tags, variants [(suffix, [z1, z2, z3])], legacy (bestehende ID)
TEMPLATES: list[dict] = []


def T(**kw):
    kw.setdefault("hold", "none")
    kw.setdefault("placement", "floor")
    kw.setdefault("kw", {})
    TEMPLATES.append(kw)


WOOD = ["oak", "walnut", "pine", "cream", "dark_wood"]
SOFT_COLS = ["mint", "rose", "sky", "butter", "grey", "coral", "linen", "denim", "plum", "teal"]

# --- Sofas & Sessel
for style, w, h, names in (("classic", 200, 85, ["mint", "rose", "sky", "butter", "grey", "coral", "linen"]),
                           ("round", 190, 80, ["rose", "lilac", "butter", "sky", "cream", "teal"]),
                           ("modern", 210, 78, ["grey", "navy", "sand", "green", "rust"]),
                           ("chesterfield", 200, 82, ["walnut", "navy", "green", "rust"])):
    T(id=f"furn_sofa_{style}", fn=F.sofa, w=w, h=h, kw={"style": style}, group="sofas", category="furniture",
      seat={"h": 42, "pose": "sit", "slots": 3}, legacy="home_sofa" if style == "classic" else None,
      variants=[(n, cols(n, "cream" if n not in ("cream", "linen") else "coral", "walnut" if style != "modern" else "black"))
                for n in names])
T(id="furn_loveseat", fn=F.sofa, w=140, h=82, kw={"style": "round", "seats": 2}, group="sofas", category="furniture",
  seat={"h": 42, "pose": "sit", "slots": 2}, variants=[(n, cols(n, "butter", "oak")) for n in ["sage", "rose", "sky", "grey"]])
for style, names in (("classic", ["sky", "mint", "rose", "butter", "grey", "coral"]),
                     ("round", ["lilac", "rose", "teal", "cream"]), ("modern", ["grey", "navy", "rust", "green"])):
    T(id=f"furn_armchair_{style}", fn=F.armchair, w=85, h=90, kw={"style": style}, group="sofas", category="furniture",
      seat={"h": 42, "pose": "sit", "slots": 1}, legacy="home_armchair" if style == "classic" else None,
      variants=[(n, cols(n, "butter" if n != "butter" else "cream", "walnut")) for n in names])

# --- Stühle & Hocker
for style, w, h, names, seat in (("dining", 45, 90, WOOD, 45), ("mint", 45, 90, ["mint", "rose", "sky", "butter", "coral", "cream"], 45),
                                 ("kids", 34, 62, ["coral", "sky", "butter", "mint"], 32), ("office", 55, 100, ["navy", "grey", "coral"], 48),
                                 ("rocking", 55, 95, ["oak", "walnut", "cream"], 42), ("bar", 38, 75, ["grey", "coral", "mint"], 72),
                                 ("beanbag", 70, 60, ["yellow", "coral", "sky", "mint", "plum", "grey"], 38),
                                 ("pouf", 50, 42, ["rose", "sand", "teal", "butter"], 42)):
    zone3 = "oak" if style in ("mint", "kids", "rocking") else "metal" if style in ("office", "bar") else "walnut"
    T(id=f"furn_chair_{style}", fn=F.chair, w=w, h=h, kw={"style": style, "seat_h": seat}, group="chairs",
      category="furniture", seat={"h": seat, "pose": "sit", "slots": 1},
      variants=[(n, cols(n, "cream", zone3 if style != "dining" else n)) for n in names])
T(id="furn_stool", fn=F.chair, w=35, h=45, kw={"style": "stool", "seat_h": 45}, group="chairs", category="furniture",
  seat={"h": 45, "pose": "sit", "slots": 1}, legacy="home_stool",
  variants=[(n, cols(n, "cream", "oak")) for n in ["oak", "coral", "mint", "sky", "butter"]])

# --- Tische
for style, w, h, names in (("dining", 140, 75, WOOD), ("round", 90, 75, ["cream", "oak", "mint"]),
                           ("coffee", 100, 45, WOOD), ("side", 45, 55, ["oak", "cream", "walnut"]),
                           ("desk", 120, 75, ["sky", "cream", "mint", "rose"]), ("kids", 70, 50, ["butter", "sky", "coral"]),
                           ("picnic", 150, 75, ["oak", "walnut"])):
    T(id=f"furn_table_{style}", fn=F.table, w=w, h=h, kw={"style": style}, group="tables", category="furniture",
      surface_h=h, legacy="home_table_coffee" if style == "coffee" else None,
      variants=[(n, cols(n, "cream", n if style in ("dining", "coffee", "side", "picnic") else "oak")) for n in names])

# --- Betten
T(id="furn_bed_kid", fn=F.bed, w=180, h=90, kw={"style": "kid", "mattress_h": 45}, group="beds", category="furniture",
  seat={"h": 45, "pose": "lie", "slots": 1}, legacy="home_bed_kid",
  variants=[(n, cols(n, "cream", "oak")) for n in ["sky", "rose", "mint", "butter", "coral", "lilac"]])
T(id="furn_bed_double", fn=F.bed, w=200, h=100, kw={"style": "double", "mattress_h": 50}, group="beds",
  category="furniture", seat={"h": 50, "pose": "lie", "slots": 2},
  variants=[(n, cols(n, "cream", w)) for n, w in (("linen", "oak"), ("sage", "walnut"), ("grey", "dark_wood"), ("rose", "oak"))])
T(id="furn_bed_bunk", fn=F.bed, w=190, h=160, kw={"style": "bunk", "mattress_h": 45}, group="beds", category="furniture",
  seat={"h": 45, "pose": "lie", "slots": 1}, variants=[(n, cols(n, "cream", "oak")) for n in ["coral", "blue", "mint"]])
T(id="furn_crib", fn=F.bed, w=120, h=100, kw={"style": "crib", "mattress_h": 55}, group="beds", category="furniture",
  seat={"h": 45, "pose": "lie", "slots": 1}, variants=[(n, cols(n, "cream", w)) for n, w in (("rose", "cream"), ("sky", "cream"), ("sage", "oak"))])

# --- Schränke & Regale
for style, w, h, names, extra in (("bookshelf", 80, 180, WOOD, {}), ("shelf_low", 100, 80, ["cream", "oak", "mint"], {}),
                                  ("cube", 80, 80, ["cream", "oak"], {}), ("wardrobe", 100, 200, ["cream", "oak", "sky", "mint"], {}),
                                  ("dresser", 100, 85, ["mint", "cream", "rose", "oak"], {"surface_h": 85}),
                                  ("nightstand", 45, 55, ["cream", "oak", "sky"], {"surface_h": 55}),
                                  ("tv_bench", 140, 50, ["cream", "walnut", "grey"], {"surface_h": 50}),
                                  ("toybox", 70, 50, ["butter", "sky", "coral"], {"container": {"slots": 8, "max_item_h_cm": 40}})):
    T(id=f"furn_{style}", fn=F.storage, w=w, h=h, kw={"style": style}, group="storage", category="furniture",
      variants=[(n, cols(n, "coral" if style == "bookshelf" else "cream", "sky" if style == "bookshelf" else "oak"))
                for n in names], **extra)

# --- Lampen & Elektronik
for style, w, h, place in (("floor", 45, 160, "floor"), ("table", 28, 45, "table"), ("arc", 80, 180, "floor"), ("desk", 30, 45, "table")):
    T(id=f"deco_lamp_{style}", fn=F.lamp, w=w, h=h, kw={"style": style}, group="lamps", category="furniture",
      placement=place, hold="one_hand" if place == "table" else "none", grip=[0.5, 0.5] if place == "table" else None,
      variants=[(n, cols(n, "sage", "walnut" if style != "arc" else "black")) for n in ["butter", "cream", "rose", "sky", "mint"]])
T(id="elec_tv", fn=F.tv, w=100, h=62, group="electronics", category="furniture", placement="floor",
  variants=[(n, cols(n, "sky", "leaf_light")) for n in ["black", "cream", "sky"]])

# --- Pflanzen: Art × Topf × Farbe
POT_COLORS = {
    "terracotta": ["terracotta", "cream"], "round": ["cream", "rose", "blue"], "cylinder": ["cream", "navy", "sage"],
    "bowl": ["cream", "butter", "coral"], "basket": ["oak", "walnut"], "square": ["cream", "grey", "mint"],
    "stand": ["cream", "navy"], "bucket": ["metal", "butter", "coral"],
}
BLOOM = {
    "tulips": ["coral", "butter", "rose", "lilac"], "roses": ["rust", "rose", "cream"], "sunflower": ["yellow"],
    "daisies": ["white", "butter"], "lavender": ["lilac", "plum"], "hydrangea": ["sky", "rose", "lilac"],
    "poinsettia": ["rust"], "orchid": ["rose", "white", "plum"], "lemon_tree": ["butter"], "tomato": ["coral"],
    "strawberry": ["coral"], "cactus_column": ["rose"], "cactus_ball": ["rose", "yellow"], "cactus_paddle": ["yellow"],
    "peace_lily": ["white"], "bird_paradise": ["orange"], "calathea": ["rose"], "spider_plant": ["cream"],
    "snake_plant": ["butter"], "olive": ["dark_wood"], "bonsai": ["walnut"],
}
for sp, (h, w, pots) in P.SPECIES.items():
    small = h <= 50
    for pot_style in pots:
        vs = []
        for pc in POT_COLORS[pot_style][:3]:
            for bloom in BLOOM.get(sp, ["walnut"])[:3 if len(pots) <= 2 else 2]:
                leafc = "leaf_light" if sp in ("herbs", "bamboo", "grass", "succulent", "cactus_ball") else "leaf"
                suffix = pc if len(BLOOM.get(sp, [])) <= 1 else f"{pc}_{bloom}"
                vs.append((suffix, cols(leafc, pc, bloom)))
        T(id=f"plant_{sp}_{pot_style}", fn=P.plant, w=w, h=h, kw={"species": sp, "pot_style": pot_style}, group="plants",
          category="plant", placement="table" if small else "floor", hold="one_hand" if h <= 50 else "none",
          grip=[0.5, 0.85] if h <= 50 else None, tags=["plant"], variants=vs)


# ================================================================== P04b: alle Bereiche (lieber zu viel als zu wenig)
from . import fun as FU  # noqa: E402
from . import household as HH  # noqa: E402
from . import outdoor as OD  # noqa: E402
from . import town as TW  # noqa: E402

BRIGHT = ["coral", "sky", "butter", "mint", "plum", "orange", "teal", "rose"]
KITCH = ["cream", "coral", "sky", "mint", "butter", "navy"]


def S(id: str, fn, style: str, w: float, h: float, group: str, category: str, names: list, second: str = "cream",
      third: str = "metal", hold: str | None = None, placement: str | None = None, grip=None, **extra):
    extra = {k: v for k, v in extra.items() if v is not None}
    """Kurzform: kleine Dinge (≤ 60 cm) sind tragbar und stehen auf Tischen, große stehen auf dem Boden."""
    small = h <= 50
    if hold is None:
        hold = "one_hand" if h <= 50 else ("two_hands" if h <= 56 else "none")   # Zeichnung + Kontur ≤ 60 cm
    if placement is None:
        placement = "table" if small and category not in ("toy", "pool", "sport", "garage") else "floor"
    if hold != "none" and grip is None:
        grip = [0.5, 0.5]
    T(id=id, fn=fn, w=w, h=h, kw={"style": style}, group=group, category=category, hold=hold, placement=placement,
      grip=grip, variants=[(n, cols(n, second if n != second else "coral", third)) for n in names], **extra)


# --- Küche (Kategorie kitchen: 1,5–45 cm)
S("kit_mug", HH.mug, "mug", 11, 10, "kitchen", "kitchen", KITCH, grip=[0.9, 0.45])
S("kit_cup", HH.mug, "cup", 8, 9, "kitchen", "kitchen", KITCH)
S("kit_glass", HH.glass, "water", 7, 12, "kitchen", "kitchen", ["sky", "orange", "coral", "mint"], second="sky")
S("kit_plate", HH.plate, "plate", 26, 3, "kitchen", "kitchen", KITCH, tags=["stackable"])
S("kit_bowl", HH.plate, "bowl", 15, 7, "kitchen", "kitchen", KITCH, tags=["stackable"])
S("kit_pot", HH.cookware, "pot", 30, 20, "kitchen", "kitchen", ["coral", "navy", "mint", "cream"], third="metal")
S("kit_pan", HH.cookware, "pan", 46, 8, "kitchen", "kitchen", ["black", "coral", "navy"], third="dark_wood", grip=[0.85, 0.7])
S("kit_kettle", HH.cookware, "kettle", 24, 26, "kitchen", "kitchen", ["cream", "coral", "sky", "mint", "black"], third="dark_wood")
S("kit_toaster", HH.cookware, "toaster", 28, 20, "kitchen", "kitchen", ["cream", "coral", "sky", "mint"], third="metal")
S("kit_blender", HH.cookware, "blender", 16, 40, "kitchen", "kitchen", ["cream", "black", "coral"], second="rose")
S("kit_microwave", HH.cookware, "microwave", 50, 30, "kitchen", "kitchen", ["cream", "black", "grey"], second="sky",
  hold="two_hands")
S("kit_coffee", HH.cookware, "coffee", 25, 35, "kitchen", "kitchen", ["black", "cream", "coral"], second="walnut",
  hold="two_hands")
S("kit_board", HH.cookware, "board", 35, 2.5, "kitchen", "kitchen", ["oak", "walnut", "pine"], third="oak")
for u in ("spoon", "ladle", "spatula", "whisk", "fork"):
    S(f"kit_{u}", HH.utensil, u, 5 if u != "whisk" else 7, 20 if u != "ladle" else 28, "kitchen", "kitchen",
      ["metal", "coral", "mint"], third="oak")
S("kit_bottle", HH.bottle, "bottle", 8, 28, "kitchen", "kitchen", ["green", "sky", "coral", "cream"], second="butter", third="navy")
S("kit_jar", HH.bottle, "jar", 10, 14, "kitchen", "kitchen", ["coral", "butter", "orange", "plum"], second="coral", third="rose")
# --- Essen (food: 2–35 cm)
for st, w, h, names in (("apple", 8, 8, ["coral", "leaf_light", "butter"]), ("orange", 8, 8, ["orange"]),
                        ("lemon", 7, 6, ["butter"]), ("peach", 7, 7, ["rose"]), ("tomato", 7, 6, ["rust"]),
                        ("banana", 18, 6, ["butter"]), ("pear", 7, 10, ["leaf_light", "butter"]), ("carrot", 5, 22, ["orange"]),
                        ("bread", 30, 12, ["oak"]), ("cake", 24, 16, ["cream", "coral", "walnut"]), ("cupcake", 7, 8, ["rose", "sky", "butter"]),
                        ("pizza", 18, 20, ["butter"]), ("icecream", 6, 16, ["rose", "butter", "walnut", "mint"]),
                        ("drink", 8, 16, ["coral", "orange", "sky"]), ("carton", 7, 20, ["cream", "butter"]),
                        ("cheese", 10, 8, ["butter"]), ("egg", 4.5, 6, ["cream", "oak"]), ("watermelon", 22, 16, ["coral"])):
    second = {"cake": "rose", "cupcake": "cream", "pizza": "oak", "icecream": "cream", "drink": "cream", "carton": "sky",
              "carrot": "leaf", "apple": "cream", "tomato": "cream", "watermelon": "leaf"}.get(st, "cream")
    third = {"apple": "leaf", "orange": "leaf", "tomato": "leaf", "icecream": "oak", "cake": "coral", "cupcake": "coral",
             "pizza": "rust", "drink": "coral", "carton": "sky"}.get(st, "walnut")
    S(f"food_{st}", FU.food, st, w, h, "food", "food", names, second=second, third=third)
# --- Bad
for st, w, h, names, cat in (("towel", 40, 30, ["sky", "rose", "mint", "butter", "cream"], "item"),
                             ("duck", 10, 10, ["yellow", "sky", "rose"], "toy"),
                             ("toothbrush", 3, 19, ["sky", "coral", "mint", "butter"], "item"),
                             ("soap", 10, 8, ["rose", "mint", "cream"], "item"), ("shampoo", 7, 20, ["plum", "teal", "coral"], "item"),
                             ("tp", 11, 10, ["cream"], "item"), ("hairdryer", 22, 20, ["rose", "black", "sky"], "item"),
                             ("basket", 30, 25, ["oak", "cream"], "item")):
    S(f"bath_{st}", HH.bath, st, w, h, "bath", cat, names, second="coral" if st != "duck" else "orange", third="sky")
# --- Deko, Elektronik, Putzen
for st, w, h, names, place in (("vase", 16, 30, ["cream", "sky", "coral", "sage", "navy"], "table"),
                               ("candle", 7, 14, ["cream", "rose", "butter"], "table"),
                               ("clock", 30, 30, ["cream", "walnut", "sky"], "wall"),
                               ("frame", 40, 30, ["oak", "walnut", "cream"], "wall"),
                               ("cushion", 40, 40, ["rose", "sky", "butter", "mint", "coral", "plum"], "floor"),
                               ("radio", 30, 22, ["coral", "sky", "cream"], "table"),
                               ("laptop", 34, 24, ["grey", "cream", "rose"], "table"),
                               ("phone", 7, 15, ["black", "coral", "sky"], "table"),
                               ("books", 30, 24, ["coral"], "table"), ("globe", 26, 36, ["sky"], "table"),
                               ("basket_laundry", 45, 45, ["cream", "oak", "sky"], "floor"),
                               ("broom", 30, 130, ["butter", "coral"], "floor"), ("bucket_mop", 34, 60, ["sky", "coral"], "floor")):
    hold = "none" if st in ("rug",) else None
    S(f"deco_{st}", HH.deco, st, w, h, "deco" if st not in ("radio", "laptop", "phone") else "electronics",
      "item", names, second="orange" if st == "candle" else "sky", third="oak" if st != "globe" else "metal",
      placement=place, hold=hold if hold else ("one_hand" if h <= 150 and st != "cushion" else "two_hands"))
# --- Spielzeug
for st, w, h, names in (("ball", 22, 22, BRIGHT[:5]), ("beachball", 30, 30, ["cream"]), ("football", 22, 22, ["white"]),
                        ("basketball", 24, 24, ["orange"]), ("teddy", 25, 30, ["oak", "walnut", "rose", "cream"]),
                        ("blocks", 12, 12, ["coral", "mint", "plum"]), ("car", 16, 9, ["coral", "sky", "butter", "mint"]),
                        ("train", 30, 14, ["coral", "navy"]), ("robot", 16, 26, ["sky", "grey", "coral"]),
                        ("doll", 15, 35, ["rose", "sky", "butter"]), ("drum", 26, 22, ["coral", "sky"]),
                        ("xylophone", 36, 14, ["coral"]), ("puzzle", 24, 24, ["coral"]), ("kite", 60, 80, ["coral", "sky", "butter"]),
                        ("rocking_horse", 80, 70, ["cream", "oak", "rose"]), ("balloon", 25, 60, BRIGHT[:6]),
                        ("skateboard", 80, 10, ["coral", "teal", "navy"]), ("bucket_spade", 26, 24, ["coral", "sky", "butter"])):
    second = {"beachball": "coral", "football": "black", "teddy": "sand", "blocks": "sky", "train": "sky", "robot": "butter",
              "doll": "walnut", "puzzle": "sky"}.get(st, "cream")
    third = {"beachball": "sky", "blocks": "butter", "teddy": "coral", "car": "metal", "train": "butter", "doll": "sand",
             "xylophone": "sky", "puzzle": "butter", "kite": "coral", "rocking_horse": "walnut", "balloon": "cream"}.get(st, "walnut")
    extra = {}
    if st == "rocking_horse":
        extra["seat"] = {"h": 40, "pose": "sit", "slots": 1}
    S(f"toy_{st}", FU.toy, st, w, h, "toys", "toy", names, second=second, third=third,
      hold="two_hands" if st in ("ball", "beachball", "football", "basketball") else ("one_hand" if st == "balloon" else None),
      grip=[0.5, 0.02] if st == "balloon" else None, **extra)
# --- Schwimmbad & Strand (die Luftmatratze taugt auch als Bett/Sofa – überall!)
for st, w, h, names, extra in (("air_mattress", 180, 15, ["coral", "sky", "butter", "mint"], {"seat": {"h": 15, "pose": "lie", "slots": 1}}),
                               ("swim_ring", 56, 56, ["coral", "sky", "butter", "mint"], {}), ("noodle", 150, 8, ["coral", "butter", "sky", "mint"], {}),
                               ("flippers", 50, 8, ["sky", "coral", "black"], {}), ("goggles", 18, 6, ["sky", "coral", "butter"], {}),
                               ("umbrella", 180, 200, ["coral", "sky", "butter", "teal"], {}),
                               ("deck_chair", 70, 90, ["coral", "sky", "teal", "butter"], {"seat": {"h": 35, "pose": "sit", "slots": 1}}),
                               ("towel_beach", 160, 6, ["sky", "coral", "butter"], {"seat": {"h": 6, "pose": "lie", "slots": 1}}),
                               ("cooler", 45, 35, ["sky", "coral", "cream"], {"container": {"slots": 6, "max_item_h_cm": 30}}),
                               ("sunscreen", 7, 16, ["butter", "orange"], {}), ("water_gun", 30, 15, ["butter", "coral", "teal"], {}),
                               ("inflatable_animal", 90, 70, ["butter", "rose", "mint"], {"seat": {"h": 25, "pose": "sit", "slots": 1}})):
    second = "cream" if st not in ("air_mattress", "swim_ring") else "cream"
    S(f"pool_{st}", FU.pool, st, w, h, "pool", "pool", names, second=second if st != "goggles" else "sky",
      third="oak" if st in ("umbrella", "deck_chair") else "metal",
      hold="two_hands" if st in ("air_mattress", "swim_ring", "noodle", "towel_beach", "inflatable_animal") and h <= 60 else None,
      **extra)
# --- Garten & Grill
for st, w, h, names, extra in (("grill", 60, 95, ["black", "coral", "navy"], {}), ("bbq_food", 24, 10, ["rust"], {}),
                               ("watering_can", 40, 30, ["mint", "sky", "coral", "metal"], {}),
                               ("wheelbarrow", 120, 70, ["coral", "green", "sky"], {}), ("gnome", 22, 40, ["coral", "sky"], {}),
                               ("birdhouse", 30, 120, ["coral", "sky", "mint"], {}), ("fence", 120, 90, ["cream", "oak", "sage"], {}),
                               ("bench", 150, 85, ["oak", "green", "coral"], {"seat": {"h": 45, "pose": "sit", "slots": 3}}),
                               ("pool_kids", 150, 30, ["sky", "rose", "mint"], {}), ("sandbox_toys", 30, 20, ["coral"], {}),
                               ("hose", 40, 40, ["green", "coral"], {})):
    second = {"grill": "orange", "gnome": "cream", "bbq_food": "rust", "birdhouse": "rust", "pool_kids": "sky", "sandbox_toys": "sky",
              "watering_can": "cream"}.get(st, "cream")
    third = {"grill": "metal", "gnome": "rose", "bbq_food": "metal", "bench": "dark_wood", "sandbox_toys": "sand",
             "birdhouse": "oak"}.get(st, "metal")
    S(f"garden_{st}", OD.garden, st, w, h, "garden", "item", names, second=second, third=third, **extra)
# --- Camping & Wald
for st, w, h, names, extra in (("tent", 200, 140, ["coral", "sage", "sky", "butter"], {"seat": {"h": 5, "pose": "lie", "slots": 2}}),
                               ("dome_tent", 220, 130, ["teal", "orange", "plum"], {"seat": {"h": 5, "pose": "lie", "slots": 2}}),
                               ("campfire", 60, 50, ["orange"], {}), ("sleeping_bag", 180, 18, ["navy", "coral", "green"],
                                                                     {"seat": {"h": 18, "pose": "lie", "slots": 1}}),
                               ("lantern", 16, 26, ["green", "coral", "navy"], {}), ("camp_chair", 60, 80, ["navy", "green", "coral"],
                                                                                    {"seat": {"h": 42, "pose": "sit", "slots": 1}}),
                               ("backpack_hiking", 35, 60, ["coral", "green", "navy"], {"container": {"slots": 6, "max_item_h_cm": 30}}),
                               ("log", 120, 30, ["oak"], {"seat": {"h": 30, "pose": "sit", "slots": 2}}),
                               ("stump", 50, 40, ["oak"], {"seat": {"h": 40, "pose": "sit", "slots": 1}}),
                               ("mushroom", 20, 22, ["rust", "oak"], {}), ("tree", 180, 300, ["leaf", "leaf_light"], {}),
                               ("fir", 160, 320, ["leaf_dark", "leaf"], {}), ("bush", 120, 80, ["leaf", "leaf_light"], {}),
                               ("rock", 80, 50, ["grey", "sand"], {"seat": {"h": 50, "pose": "sit", "slots": 1}}),
                               ("signpost", 60, 160, ["oak"], {}), ("binoculars", 14, 12, ["black", "green"], {})):
    second = {"tent": "cream", "campfire": "butter", "lantern": "butter", "log": "pine", "stump": "pine", "mushroom": "cream",
              "bush": "coral", "signpost": "pine", "sleeping_bag": "butter", "rock": "leaf"}.get(st, "cream")
    third = {"tent": "oak", "campfire": "walnut", "log": "walnut", "stump": "walnut", "tree": "walnut", "fir": "walnut",
             "lantern": "metal", "backpack_hiking": "metal"}.get(st, "metal")
    S(f"camp_{st}", OD.camping, st, w, h,
      group="garden" if st in ("tree", "fir", "bush", "rock", "mushroom", "stump") else "camping",
      category="item", names=names, second=second, third=third,
      hold="one_hand" if st == "backpack_hiking" else None, **extra)
# --- Spielplatz & Fahrräder (Verleih)
for st, w, h, names, extra in (("slide", 200, 180, ["coral", "sky", "butter"], {}), ("swing", 160, 200, ["coral", "sky", "mint"], {}),
                               ("seesaw", 250, 70, ["butter", "coral", "sky"], {}),
                               ("bicycle", 150, 90, ["coral", "sky", "mint", "butter", "navy", "plum"], {}),
                               ("tricycle", 70, 55, ["coral", "sky", "butter"], {}),
                               ("scooter", 60, 80, ["teal", "coral", "sky"], {}), ("helmet", 25, 18, ["coral", "sky", "butter", "mint"], {}),
                               ("bike_rack", 150, 70, ["metal"], {}), ("sandpit", 180, 30, ["butter"], {})):
    S(f"play_{st}", OD.playground, st, w, h, "playground" if st in ("slide", "swing", "seesaw", "sandpit") else "bikes",
      "toy" if st not in ("slide", "swing", "seesaw", "sandpit", "bike_rack") else "item", names,
      second="cream" if st != "sandpit" else "coral", third="metal" if st != "sandpit" else "oak", **extra)
# --- Sport & Eishalle
for st, w, h, names, grp in (("goal", 300, 200, ["cream"], "sport"), ("basket_hoop", 120, 300, ["coral"], "sport"),
                             ("racket", 27, 68, ["coral", "sky", "mint"], "sport"), ("bat", 8, 80, ["oak", "coral"], "sport"),
                             ("dumbbell", 30, 12, ["coral", "sky", "black"], "sport"), ("mat", 180, 8, ["sky", "coral", "teal"], "sport"),
                             ("cone", 20, 30, ["orange", "butter"], "sport"), ("trophy", 20, 32, ["butter"], "sport"),
                             ("skates", 36, 28, ["cream", "sky", "rose"], "winter"), ("hockey_stick", 40, 150, ["black", "coral"], "winter"),
                             ("puck", 8, 2.5, ["black"], "winter"), ("sled", 90, 35, ["coral", "sky", "oak"], "winter"),
                             ("snowman", 60, 120, ["coral"], "winter")):
    second = {"goal": "cream", "basket_hoop": "cream", "racket": "cream", "bat": "black", "skates": "coral", "hockey_stick": "cream",
              "snowman": "white", "mat": "cream", "cone": "cream"}.get(st, "cream")
    extra = {"seat": {"h": 8, "pose": "lie", "slots": 1}} if st == "mat" else {}
    extra.update({"seat": {"h": 30, "pose": "sit", "slots": 1}} if st == "sled" else {})
    S(f"sport_{st}", OD.sport, st, w, h, grp, "sport", names, second=second, third="metal" if st != "snowman" else "coral",
      **extra)
# --- Werkstatt
for st, w, h, names in (("hammer", 12, 30, ["black", "coral"]), ("wrench", 7, 25, ["metal"]), ("screwdriver", 3, 22, ["coral", "butter"]),
                        ("saw", 50, 16, ["coral"]), ("drill", 26, 24, ["coral", "teal", "butter"]), ("toolbox", 45, 30, ["coral", "navy", "green"]),
                        ("tire", 56, 56, ["metal"]), ("jerrycan", 30, 40, ["coral", "green"]), ("workbench", 150, 90, ["oak"]),
                        ("ladder", 50, 200, ["metal", "oak"]), ("paint_can", 18, 20, BRIGHT[:5]), ("cone_traffic", 30, 50, ["orange"])):
    S(f"work_{st}", TW.tool, st, w, h, "workshop", "garage", names,
      second={"toolbox": "metal", "workbench": "coral", "cone_traffic": "white", "drill": "black"}.get(st, "cream"),
      third={"hammer": "oak", "workbench": "walnut", "paint_can": "metal"}.get(st, "metal"),
      surface_h=90 if st == "workbench" else None)
# --- Läden, Kasse, Friseur, Modeladen
for st, w, h, names, grp, extra in (("cart", 60, 100, ["coral", "sky", "metal"], "shop", {"container": {"slots": 10, "max_item_h_cm": 40}}),
                                    ("basket_shop", 40, 28, ["coral", "sky", "mint"], "shop", {"container": {"slots": 6, "max_item_h_cm": 25}}),
                                    ("bag", 30, 36, ["cream", "coral", "sky", "oak"], "shop", {"container": {"slots": 5, "max_item_h_cm": 25}}),
                                    ("box", 40, 30, ["oak", "sand"], "shop", {"container": {"slots": 6, "max_item_h_cm": 25}}),
                                    ("cash_register", 45, 35, ["cream", "black", "sky"], "shop", {}),
                                    ("price_sign", 30, 40, ["coral", "butter"], "shop", {}),
                                    ("mannequin", 50, 175, ["cream", "sand"], "shop", {}),
                                    ("hanger_rack", 120, 160, ["metal"], "shop", {}),
                                    ("barber_chair", 65, 110, ["coral", "black", "sky"], "hairdresser", {"seat": {"h": 55, "pose": "sit", "slots": 1}}),
                                    ("hair_tools", 30, 24, ["black", "coral"], "hairdresser", {}),
                                    ("mirror_stand", 60, 170, ["oak", "cream", "black"], "hairdresser", {})):
    S(f"shop_{st}", TW.shop, st, w, h, grp, "shop", names,
      second={"cart": "coral", "cash_register": "sky", "price_sign": "cream", "hanger_rack": "coral", "mirror_stand": "sky",
              "bag": "coral"}.get(st, "cream"), third="metal", **extra)
# --- Rummelplatz
for st, w, h, names in (("cotton_candy", 20, 40, ["rose", "sky"]), ("popcorn", 16, 22, ["coral"]), ("ticket_booth", 150, 220, ["coral", "sky"]),
                        ("balloon_bunch", 50, 120, ["coral"]), ("target", 60, 150, ["coral"]), ("carousel_horse", 100, 180, ["cream", "rose", "sky"])):
    S(f"fair_{st}", TW.fair, st, w, h, "fair", "fair" if st != "popcorn" else "food", names,
      second={"popcorn": "butter", "ticket_booth": "butter", "balloon_bunch": "sky", "target": "cream", "carousel_horse": "butter"}.get(st, "cream"),
      third={"balloon_bunch": "butter", "popcorn": "white", "carousel_horse": "butter"}.get(st, "oak"),
      **({"seat": {"h": 90, "pose": "sit", "slots": 1}} if st == "carousel_horse" else {}))
# --- Schule & Gesundheit
for st, w, h, names, grp, cat in (("school_desk", 70, 75, ["sky", "oak", "mint"], "school", "school"),
                                  ("blackboard", 150, 180, ["green", "navy"], "school", "school"),
                                  ("school_bag", 30, 38, ["coral", "sky", "mint", "plum"], "school", "school"),
                                  ("pencil_cup", 10, 20, ["sky", "coral"], "school", "school"),
                                  ("microscope", 20, 35, ["cream", "black"], "school", "school"),
                                  ("easel", 70, 150, ["cream"], "school", "school"),
                                  ("first_aid", 30, 26, ["coral", "cream"], "health", "health"),
                                  ("stethoscope", 20, 40, ["black", "sky"], "health", "health"),
                                  ("wheelchair", 70, 90, ["sky", "coral", "black"], "health", "health"),
                                  ("bandage", 10, 5, ["cream"], "health", "health"), ("thermometer", 3, 14, ["sky"], "health", "health")):
    extra = {"surface_h": 75} if st == "school_desk" else {}
    if st == "wheelchair":
        extra["seat"] = {"h": 48, "pose": "sit", "slots": 1}
    S(f"{grp}_{st}", TW.school, st, w, h, grp, cat, names,
      second={"blackboard": "cream", "school_bag": "butter", "pencil_cup": "coral", "first_aid": "white", "easel": "cream",
              "microscope": "sky", "thermometer": "coral", "bandage": "rose"}.get(st, "cream"),
      third={"school_desk": "metal", "blackboard": "oak", "pencil_cup": "butter", "easel": "oak", "school_bag": "metal"}.get(st, "metal"),
      **extra)
# --- Zoo & Tierbedarf
for st, w, h, names in (("feed_bucket", 30, 32, ["coral", "sky"]), ("hay", 80, 45, ["butter"]), ("bowl_pet", 18, 7, ["coral", "sky", "mint"]),
                        ("zoo_sign", 60, 150, ["oak", "green"]), ("pet_bed", 70, 25, ["coral", "sky", "rose", "oak"]),
                        ("cage", 60, 70, ["mint", "sky", "coral"]), ("aquarium", 80, 50, ["black", "oak"])):
    extra = {"seat": {"h": 20, "pose": "lie", "slots": 1}} if st == "pet_bed" else {}
    S(f"zoo_{st}", TW.zoo, st, w, h, "animals", "item", names,
      second={"feed_bucket": "butter", "hay": "oak", "bowl_pet": "walnut", "zoo_sign": "cream", "pet_bed": "cream",
              "aquarium": "sky"}.get(st, "cream"),
      third={"aquarium": "sand", "cage": "metal"}.get(st, "metal"), **extra)


# ================================================================== P04b-T10: Zustände (auf/zu, an/aus) + Geräte + Gekochtes
from . import appliances as AP  # noqa: E402

OPEN = {"states": {"open": {"state": "open"}}, "state0": "closed"}
ON = {"states": {"on": {"state": "on"}}, "state0": "off"}
STATEFUL = {
    "furn_wardrobe": OPEN, "furn_dresser": OPEN, "furn_nightstand": OPEN, "furn_tv_bench": OPEN, "furn_toybox": OPEN,
    "deco_lamp_floor": ON, "deco_lamp_table": ON, "deco_lamp_arc": ON, "deco_lamp_desk": ON, "elec_tv": ON,
    "kit_kettle": {**ON, "anim": {"on": "pulse"}}, "kit_toaster": ON, "kit_blender": {**ON, "anim": {"on": "shake"}},
    "kit_microwave": {**ON, "anim": {"on": "pulse"}}, "kit_coffee": ON, "kit_pot": {**ON, "anim": {"on": "pulse"}},
    "deco_radio": {**ON, "anim": {"on": "bounce"}}, "deco_laptop": ON, "deco_phone": ON,
    "bath_hairdryer": {**ON, "anim": {"on": "shake"}},
    # T11: draußen, Werkstatt, Laden
    "garden_grill": {**ON, "anim": {"on": "pulse"}}, "camp_campfire": {**ON, "anim": {"on": "pulse"}},
    "camp_lantern": ON, "camp_tent": OPEN, "pool_cooler": OPEN,
    "work_drill": {**ON, "anim": {"on": "shake"}}, "work_toolbox": OPEN,
    "shop_cash_register": {**OPEN, "anim": {"open": "bounce"}},
}
# Kochen: Geräte nehmen Zutaten auf (Inhalt immer sichtbar) – Rezepte in data/recipes/
COOK_HOSTS = {"kit_toaster": 2, "kit_blender": 4, "kit_microwave": 2, "kit_pot": 4, "kit_pan": 2, "kit_coffee": 1,
              "garden_grill": 4, "camp_campfire": 3}
for t in TEMPLATES:
    for key, cfg in STATEFUL.items():
        if t["id"] == key:
            t.update({k: v for k, v in cfg.items()})
    if t["id"] in COOK_HOSTS:
        t["container"] = {"slots": COOK_HOSTS[t["id"]], "max_item_h_cm": 30}
        t["tags"] = list(t.get("tags", [])) + ["open_top", "cook_host"]

for st, w, h, names, extra in (
        ("fridge", 70, 180, ["cream", "sky", "mint", "coral", "grey"], {**OPEN, "container": {"slots": 12, "max_item_h_cm": 40}}),
        ("stove", 60, 90, ["cream", "black", "sky"], {**ON, "anim": {"on": "pulse"}, "surface_h": 90,
                                                      "container": {"slots": 2, "max_item_h_cm": 35},
                                                      "tags": ["open_top", "cook_host"]}),
        ("oven", 60, 90, ["cream", "black", "coral"], {**ON, "container": {"slots": 3, "max_item_h_cm": 35},
                                                       "tags": ["open_top", "cook_host"]}),
        ("washer", 60, 85, ["cream", "sky", "grey"], {**ON, "anim": {"on": "shake"}, "container": {"slots": 6, "max_item_h_cm": 40},
                                                      "tags": ["open_top"]}),
        ("sink", 80, 110, ["cream", "sky", "mint"], {**ON}),
        ("fan", 40, 100, ["cream", "sky", "mint"], {**ON, "anim": {"on": "pulse"}}),
        ("computer", 55, 50, ["cream", "black", "grey"], {**ON}),
        ("console", 36, 20, ["black", "cream", "coral"], {**ON})):
    S(f"app_{st}", AP.appliance, st, w, h, "kitchen" if st in ("fridge", "stove", "oven", "sink") else "electronics",
      "furniture" if h > 45 else "item", names,
      second={"fridge": "butter", "stove": "orange", "oven": "orange", "washer": "sky", "sink": "sky", "fan": "sky",
              "computer": "sky", "console": "coral"}[st], third="metal", **extra)
for st, w, h, names in (("toast", 11, 11, ["oak"]), ("bread_slice", 11, 11, ["pine"]), ("fried_egg", 12, 3, ["white"]),
                        ("smoothie", 8, 16, ["rose", "orange", "mint", "plum"]), ("soup", 16, 9, ["orange", "leaf_light", "coral"]),
                        ("pancakes", 16, 10, ["oak"]), ("sausage", 14, 5, ["rust"]), ("hot_drink", 10, 11, ["walnut", "cream"]),
                        ("popcorn_bowl", 18, 12, ["butter"]), ("cake_baked", 24, 16, ["cream", "walnut"])):
    second = {"toast": "walnut", "bread_slice": "oak", "fried_egg": "yellow", "smoothie": "cream", "pancakes": "coral",
              "cake_baked": "rose"}.get(st, "cream")
    third = {"smoothie": "sky", "soup": "cream", "hot_drink": "coral", "popcorn_bowl": "coral", "pancakes": "cream",
             "cake_baked": "coral"}.get(st, "metal")
    S(f"cook_{st}", AP.cooked, st, w, h, "food", "food", names, second=second, third=third)


# ================================================================== P07: Bauteile – Räume sind leer, das Kind baut (Wunsch 👤)
# Fenster, Türen, Vorhänge hängen an der Wand (placement "wall", Aufhängepunkt oben Mitte); Teppiche liegen
# flach unter allem (placement "rug"). Türen und bodentiefe Fenster rasten unten am Boden ein (tag "to_floor").
from . import building as BU  # noqa: E402

SKY, HILL = "#a8dcf2", "#8cc47a"
FRAMES = ["white", "oak", "walnut", "grey", "sky", "mint", "coral"]
for style, sizes in (("single", (("s", 60, 72), ("m", 90, 110), ("l", 120, 140))), ("double", (("m", 120, 120), ("l", 160, 140))),
                     ("triple", (("l", 210, 130),)), ("floor", (("l", 100, 212),)), ("tilt", (("m", 80, 100),)),
                     ("small", (("s", 50, 50),)), ("basement", (("m", 100, 52),)), ("shop", (("xl", 260, 190),)),
                     ("round", (("s", 50, 50), ("m", 72, 72))), ("porthole", (("s", 56, 56),)), ("arch", (("m", 90, 150), ("l", 120, 185))),
                     ("gable", (("m", 90, 115),)), ("stained", (("m", 70, 140),))):
    for size, w, h in sizes:
        T(id=f"win_{style}_{size}", fn=BU.window, w=w, h=h, kw={"style": style}, group="windows", category="deco",
          placement="wall", tags=["to_floor"] if style == "floor" else [],
          variants=[(n, cols(n, SKY, HILL if style != "stained" else "rose")) for n in FRAMES])
for style, w, h, names in (("wood", 95, 205, ["oak", "walnut", "white", "sky", "mint", "coral", "navy"]),
                           ("glass", 95, 205, ["white", "oak", "grey", "sky"]), ("arch", 100, 220, ["oak", "walnut", "coral", "mint"]),
                           ("barn", 110, 210, ["oak", "walnut", "rust", "grey"]), ("double", 165, 215, ["white", "oak", "grey"]),
                           ("garage", 260, 215, ["cream", "grey", "sky", "coral"])):
    T(id=f"door_{style}", fn=BU.door, w=w, h=h, kw={"style": style}, group="doors", category="deco", placement="wall",
      tags=["to_floor"], variants=[(n, cols(n, "white" if n != "white" else "cream", "gold" if style != "garage" else "metal"))
                                   for n in names])
CURTAIN = ["coral", "sky", "mint", "butter", "rose", "navy", "sage", "plum", "cream"]
for style, w, h in (("long", 170, 235), ("short", 130, 80), ("sheer", 170, 235), ("blind", 110, 150)):
    for pattern in (("plain", "dots", "stripes", "stars") if style in ("long", "short") else ("plain",)):
        T(id=f"curtain_{style}" + ("" if pattern == "plain" else f"_{pattern}"), fn=BU.curtain, w=w, h=h,
          kw={"style": style, "pattern": pattern}, group="curtains", category="deco", placement="wall",
          variants=[(n, cols(n if style != "sheer" else "cream", "cream" if n != "cream" else "coral",
                             "oak" if style != "blind" else "metal")) for n in (CURTAIN if style != "sheer" else ["cream"])])
for style, w, h, names in (("rect", 220, 60, ["coral", "sky", "sage", "butter", "navy", "rust", "plum"]),
                           ("rect", 160, 45, ["rose", "teal", "mint", "sand", "grey"]),
                           ("round", 150, 42, ["rose", "sky", "butter", "mint", "lilac"]),
                           ("runner", 280, 24, ["rust", "navy", "sage", "coral"]),
                           ("doormat", 75, 20, ["oak", "pine", "grey"]), ("bathmat", 80, 24, ["sky", "mint", "rose", "cream"]),
                           ("roads", 200, 56, ["green"]), ("sheepskin", 110, 32, ["cream", "sand", "grey"]),
                           ("flower", 130, 40, ["rose", "butter", "sky", "mint"])):
    rid = f"rug_{style}" + ("_s" if (style == "rect" and w < 200) else "")
    third = {"rect": "cream", "runner": "cream", "doormat": "walnut", "roads": "white", "bathmat": "cream"}.get(style, "cream")
    second = {"roads": "grey", "doormat": "coral", "flower": "butter", "round": "cream"}.get(style, "butter")
    T(id=rid, fn=BU.rug, w=w, h=h, kw={"style": style}, group="rugs", category="deco", placement="rug",
      variants=[(n, cols(n, second if n != second else "coral", third)) for n in names])
for motif, names in (("rocket", ["navy", "sky"]), ("rainbow", ["sky", "cream"]), ("dino", ["butter", "mint"]), ("sun", ["sky", "rose"])):
    T(id=f"poster_{motif}", fn=BU.poster, w=50, h=70, kw={"motif": motif}, group="walldeco", category="deco", placement="wall",
      variants=[(n, cols(n, {"rocket": "coral", "rainbow": "coral", "dino": "green", "sun": "yellow"}[motif],
                         {"rocket": "cream", "rainbow": "butter", "dino": "oak", "sun": "leaf"}[motif])) for n in names])
T(id="wall_sconce", fn=BU.sconce, w=30, h=45, group="walldeco", category="deco", placement="wall",
  states={"on": {"state": "on"}}, state0="off",
  variants=[(n, cols(n, "butter", "metal")) for n in ["cream", "sky", "mint", "coral"]])
T(id="home_radiator", fn=BU.radiator, w=100, h=60, group="walldeco", category="furniture",
  variants=[(n, cols(n, "grey", "metal")) for n in ["white", "cream", "grey"]])

# P07-Inventar (Pflichtliste data/inventory.json) – eigene Datei, damit keine Datei über 400 Zeilen wächst
from . import catalog_food, catalog_home, catalog_living, catalog_more, catalog_town  # noqa: E402,F401
