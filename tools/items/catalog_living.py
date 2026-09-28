"""
Katalog, P07-Inventar 3 – Wohnen & Garage (Wunsch 👤: „Bett, Doppelbett, Himmelbett, Tische in allen möglichen Formen,
Sessel, Schaukelstuhl für Oma/Opa, Hocker, Stühle, Gardinen, Gardinenstange … Garage: Autoreifen, alles Mögliche“).
Pflichtliste: data/inventory.json.
"""
from __future__ import annotations

from . import cellar as CE
from . import furniture as F
from . import furniture2 as F2
from .catalog import S, T, cols

WOOD = ["oak", "walnut", "pine", "cream", "dark_wood"]
SOFT = ["sage", "rose", "sky", "butter", "grey", "coral", "linen", "navy"]

# ------------------------------------------------------------------ Betten
T(id="furn_bed_single", fn=F.bed, w=200, h=85, kw={"style": "double", "mattress_h": 45}, group="beds", category="furniture",
  seat={"h": 45, "pose": "lie", "slots": 1}, variants=[(n, cols(n, "cream", w)) for n, w in
                                                       (("sky", "oak"), ("mint", "pine"), ("rose", "cream"), ("grey", "walnut"), ("butter", "oak"))])
T(id="furn_bed_double_box", fn=F.bed, w=210, h=115, kw={"style": "double", "mattress_h": 62}, group="beds", category="furniture",
  seat={"h": 62, "pose": "lie", "slots": 2}, variants=[(n, cols(n, "cream", w)) for n, w in (("navy", "grey"), ("linen", "sand"), ("sage", "grey"))])
for style, w, h, mh, names, slots in (("canopy", 210, 210, 50, ["rose", "cream", "sky", "lilac", "sage"], 2),
                                      ("loft", 200, 190, 160, ["sky", "mint", "coral"], 1),
                                      ("sofa_bed", 200, 80, 22, ["grey", "navy", "sage"], 2),
                                      ("daybed", 200, 90, 45, ["cream", "rose", "sky"], 1)):
    T(id="furn_sofa_bed" if style == "sofa_bed" else ("furn_daybed" if style == "daybed" else f"furn_bed_{style}"),
      fn=F2.bed2, w=w, h=h, kw={"style": style, "mattress_h": mh}, group="beds", category="furniture",
      seat={"h": mh, "pose": "lie", "slots": slots},
      variants=[(n, cols(n, "cream" if n != "cream" else "rose", "oak" if style != "canopy" else "white")) for n in names])

# ------------------------------------------------------------------ Tische in allen Formen
T(id="furn_table_round_big", fn=F.table, w=120, h=75, kw={"style": "round"}, group="tables", category="furniture", surface_h=75,
  variants=[(n, cols(n, "cream", n)) for n in ["oak", "walnut", "white"]])
for style, w, h, names in (("oval", 160, 75, WOOD[:4]), ("square", 90, 75, ["oak", "white", "walnut", "sage"]),
                           ("long", 240, 76, ["oak", "walnut", "dark_wood"]), ("extend", 180, 75, ["oak", "white", "walnut"]),
                           ("folding", 120, 72, ["white", "grey", "sky"]), ("bistro", 60, 72, ["white", "black", "sage"]),
                           ("bar", 70, 105, ["black", "oak", "white"]), ("console", 110, 80, ["walnut", "white", "oak"]),
                           ("coffee_round", 80, 42, ["oak", "white", "walnut", "black"]), ("nesting", 70, 50, ["oak", "walnut", "white"])):
    T(id=f"furn_table_{style}", fn=F2.table2, w=w, h=h, kw={"style": style}, group="tables", category="furniture",
      **({"surface_h": h} if style != "nesting" else {}), variants=[(n, cols(n, "cream" if n != "cream" else "coral", n)) for n in names])

# ------------------------------------------------------------------ Sessel, Stühle, Hocker, Bänke
for style, w, h, sh, names, slots in (("wing", 85, 115, 45, ["sage", "rust", "navy", "rose", "butter"], 1),
                                      ("recliner", 110, 105, 45, ["walnut", "grey", "navy"], 1)):
    T(id=f"furn_armchair_{style}", fn=F2.seat2, w=w, h=h, kw={"style": style, "seat_h": sh}, group="sofas", category="furniture",
      seat={"h": sh, "pose": "sit", "slots": slots}, variants=[(n, cols(n, "cream", "walnut")) for n in names])
T(id="furn_chair_rocking_granny", fn=F.chair, w=60, h=105, kw={"style": "rocking", "seat_h": 44}, group="chairs", category="furniture",
  seat={"h": 44, "pose": "sit", "slots": 1}, variants=[(n, cols(n, "cream", w)) for n, w in (("rose", "walnut"), ("sage", "oak"), ("navy", "dark_wood"))])
T(id="furn_chair_padded", fn=F.chair, w=46, h=92, kw={"style": "mint", "seat_h": 46}, group="chairs", category="furniture",
  seat={"h": 46, "pose": "sit", "slots": 1}, variants=[(n, cols(n, "cream", "walnut")) for n in ["grey", "navy", "rust", "sage", "linen"]])
for style, w, h, sh, names, gid, slots in (
        ("folding", 44, 82, 45, ["white", "grey", "coral", "sky"], "furn_chair_folding", 1),
        ("bench_kitchen", 180, 90, 46, ["oak", "white", "pine"], "furn_bench_kitchen", 3),
        ("step", 45, 45, 45, ["white", "sky", "coral"], "furn_stool_step", 1),
        ("piano", 45, 50, 50, ["black", "walnut"], "furn_stool_piano", 1),
        ("milk", 32, 30, 30, ["oak", "pine"], "furn_stool_milk", 1),
        ("footstool", 50, 38, 38, ["sage", "rose", "grey", "rust"], "furn_footstool", 1)):
    T(id=gid, fn=F2.seat2, w=w, h=h, kw={"style": style, "seat_h": sh}, group="chairs", category="furniture",
      seat={"h": sh, "pose": "sit", "slots": slots},
      variants=[(n, cols(n, "coral" if style == "bench_kitchen" else "cream", "oak" if style != "folding" else "metal")) for n in names])

# ------------------------------------------------------------------ Gardinenstangen, Raffrollo, Jalousie (Wand)
for style, w, h, names in (("rod", 180, 12, ["black", "white", "oak", "gold"]), ("rod_rings", 240, 12, ["black", "oak", "white"]),
                           ("roman", 110, 70, ["cream", "sage", "sky", "rose"]), ("venetian", 110, 130, ["white", "grey", "oak", "sky"])):
    gid = {"rod": "curtain_rod", "rod_rings": "curtain_rod_rings", "roman": "curtain_roman", "venetian": "curtain_venetian"}[style]
    T(id=gid, fn=F2.window_deco, w=w, h=h, kw={"style": style}, group="curtains", category="deco", placement="wall",
      variants=[(n, cols(n, "gold" if style.startswith("rod") else "cream", "metal")) for n in names])

# ------------------------------------------------------------------ Garage
for style, w, h, names in (("tire_summer", 62, 62, ["black"]), ("tire_winter", 62, 62, ["black"]), ("tire_sport", 66, 66, ["black"]),
                           ("tire_steel", 60, 60, ["black"])):
    T(id=f"work_{style}", fn=CE.garage, w=w, h=h, kw={"style": style}, group="workshop", category="garage",
      hold="two_hands" if h <= 56 else "none", variants=[(n, cols("#34343a", c2, c3)) for n, c2, c3 in
                                                          (("silver", "metal", "#c9d0d8"), ("black", "black", "#6d6f78"))])
T(id="work_tire_stack", fn=CE.garage, w=62, h=90, kw={"style": "tire_stack"}, group="workshop", category="garage",
  variants=[("black", cols("#34343a", "metal", "metal")), ("grey", cols("#4a4a52", "metal", "metal"))])
for style, w, h, names in (("car_jack", 40, 30, ["coral", "black"]), ("oil_can", 24, 30, ["coral", "sky", "green"]),
                           ("bike_pump", 22, 60, ["black", "coral", "sky"]), ("car_wash", 34, 36, ["sky", "coral"]),
                           ("tool_cart", 70, 95, ["coral", "navy", "black"]), ("snow_shovel", 45, 130, ["coral", "sky", "black"]),
                           ("cable_reel", 30, 34, ["coral", "black"])):
    S(f"work_{style}", CE.garage, style, w, h, "workshop", "garage", names,
      second={"car_jack": "metal", "oil_can": "butter", "bike_pump": "butter", "car_wash": "white", "tool_cart": "metal",
              "snow_shovel": "black", "cable_reel": "orange"}[style], third={"car_wash": "butter"}.get(style, "metal"),
      hold="one_hand" if style in ("snow_shovel", "bike_pump") else None, grip=[0.5, 0.95] if style in ("snow_shovel", "bike_pump") else None)
