"""
Katalog, Teil P09 (Einkaufsstraße + Spielplatz): Ladeneinrichtung, Straßenmöbel, Spielgeräte, Wildtiere im Park.
Welt-Doku §2/§3. Größen: echte Maße (Regal 170 cm, Theke 95 cm, Laterne 380 cm, Ente 35 cm …).
"""
from __future__ import annotations

from . import park as PK
from . import shopfit as SF
from .catalog import T, cols

OPEN = {"states": {"open": {"state": "open"}}, "state0": "closed"}
ON = {"states": {"on": {"state": "on"}}, "state0": "off"}


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second if n != second else "cream", third)) for n in names]


# ------------------------------------------------------------------ Ladeneinrichtung (fest im Laden, aber verschiebbar)
for st, w, h, names, second, third, extra in (
        ("shelf_market", 120, 170, ["cream", "sky", "mint", "white"], "coral", "metal", {}),
        ("shelf_toys", 130, 170, ["butter", "sky", "rose"], "coral", "oak", {}),
        ("shelf_electro", 130, 170, ["black", "grey", "white"], "sky", "metal", {}),
        ("shelf_pets", 120, 160, ["mint", "oak"], "butter", "metal", {}),
        ("shelf_bread", 130, 170, ["oak", "walnut", "cream"], "orange", "oak", {}),
        ("shelf_books", 110, 180, ["oak", "walnut", "white"], "coral", "oak", {}),
        ("fridge_shelf", 130, 195, ["white", "sky", "grey"], "coral", "metal", {}),
        ("checkout", 170, 90, ["coral", "sky", "white", "mint"], "butter", "black", {"surface_h": 90}),
        ("counter", 150, 95, ["oak", "cream", "mint", "coral", "sky"], "butter", "walnut", {"surface_h": 95}),
        ("counter_glass", 150, 110, ["cream", "oak", "rose"], "butter", "metal", {"surface_h": 110}),
        ("produce_stand", 150, 110, ["oak", "walnut"], "coral", "oak", {}),
        ("flower_stand", 130, 110, ["oak", "white"], "rose", "sage", {}),
        ("icecream_counter", 160, 115, ["sky", "rose", "mint"], "butter", "metal", {"surface_h": 80}),
        ("fitting_room", 110, 215, ["oak", "white", "black"], "coral", "oak", OPEN),
        ("hair_sink", 110, 110, ["black", "coral", "sky"], "cream", "white", {"seat": {"h": 52, "pose": "sit", "slots": 1}}),
        ("dryer_hood", 60, 150, ["rose", "sky", "white"], "butter", "metal", {}),
        ("magazine_rack", 60, 150, ["metal", "coral"], "coral", "metal", {}),
        ("tank_shelf", 110, 160, ["black", "oak"], "coral", "sky", {}),
        ("coffee_machine", 55, 45, ["coral", "black", "cream"], "cream", "metal", {})):
    T(id=f"shop_{st}", fn=SF.shopfit, w=w, h=h, kw={"style": st}, group="shopfit",
      category="shop" if st == "coffee_machine" else "furniture", placement="table" if st == "coffee_machine" else "floor",
      hold="two_hands" if st == "coffee_machine" else "none", grip=[0.5, 0.5] if st == "coffee_machine" else None,
      variants=V(names, second, third), **extra)

# ------------------------------------------------------------------ Straße
for st, w, h, names, second, third, extra in (
        ("bus_stop", 280, 250, ["sky", "green", "butter"], "coral", "metal", {"seat": {"h": 45, "pose": "sit", "slots": 3}}),
        ("street_lamp", 60, 380, ["black", "green", "navy"], "butter", "metal", ON),
        ("park_bench", 160, 85, ["oak", "green", "walnut"], "cream", "black", {"seat": {"h": 45, "pose": "sit", "slots": 3}}),
        ("bin_street", 50, 100, ["green", "coral", "grey"], "butter", "metal", {}),
        ("bike_stand", 200, 80, ["metal", "coral"], "cream", "metal", {}),
        ("advert_column", 110, 300, ["green", "cream"], "coral", "metal", {}),
        ("icecream_cart", 170, 200, ["cream", "rose", "sky"], "coral", "metal", {}),
        ("bus", 500, 260, ["butter", "sky", "coral"], "white", "metal", {})):   # Kleinbus (Textur ≤ 4096 px)
    T(id=f"street_{st}", fn=PK.street, w=w, h=h, kw={"style": st}, group="street", category="item", variants=V(names, second, third),
      **extra)
T(id="street_awning", fn=PK.street, w=240, h=90, kw={"style": "awning"}, group="street", category="item", placement="wall",
  variants=V(["coral", "sky", "mint", "butter", "rose"], "white", "metal"))
for motif, second in (("cart", "coral"), ("bread", "orange"), ("flower", "rose"), ("shirt", "sky"), ("scissors", "plum"),
                      ("teddy", "walnut"), ("paw", "navy"), ("icecream", "rose"), ("note", "navy")):
    T(id=f"street_sign_{motif}", fn=PK.street, w=90, h=60, kw={"style": "shop_sign", "motif": motif}, group="street",
      category="item", placement="wall", variants=[(n, cols(n, second, "oak")) for n in ["oak", "cream", "mint"]])

# ------------------------------------------------------------------ Spielplatz
for st, w, h, names, second, third, extra in (
        ("climber", 300, 260, ["coral", "sky", "butter"], "mint", "oak", {"surface_h": 115}),
        ("roundabout", 180, 90, ["coral", "sky", "butter"], "mint", "metal", {**ON, "seat": {"h": 30, "pose": "sit", "slots": 4},
                                                                             "anim": {"on": "wiggle"}}),
        ("spring_rider", 80, 95, ["butter", "coral", "sky", "mint"], "orange", "metal", {"seat": {"h": 60, "pose": "sit", "slots": 1},
                                                                                        "states": {"on": {"state": "on"}},
                                                                                        "state0": "off", "anim": {"on": "wiggle"}}),
        ("swing_double", 300, 230, ["coral", "sky", "butter"], "mint", "oak", {"seat": {"h": 40, "pose": "sit", "slots": 2}}),
        ("tower_slide", 360, 240, ["coral", "sky", "mint"], "butter", "oak", {"surface_h": 120})):
    T(id=f"play_{st}", fn=PK.play, w=w, h=h, kw={"style": st}, group="park", category="item", variants=V(names, second, third),
      **extra)
T(id="play_sand_mold", fn=PK.play, w=14, h=12, kw={"style": "sand_mold"}, group="park", category="toy", placement="floor",
  hold="one_hand", grip=[0.5, 0.5], states={"fish": {"state": "fish"}, "castle": {"state": "castle"}}, state0="star",
  variants=V(["coral", "sky", "butter", "mint"], "cream", "metal"))
for shp in ("star", "fish", "castle"):                             # Sand-Figur (kommt aus dem Förmchen)
    T(id=f"play_sand_shape_{shp}", fn=PK.play, w=16 if shp != "castle" else 18, h=12, kw={"style": "sand_mold", "shape": shp},
      group="park", category="toy", placement="floor", hold="one_hand", grip=[0.5, 0.5], tags=["sand_shape"],
      variants=[("sand", cols("butter", "sand", "oak"))])
T(id="play_bubble_wand", fn=PK.play, w=10, h=16, kw={"style": "bubble_wand"}, group="park", category="toy", placement="floor",
  hold="one_hand", grip=[0.3, 0.3], variants=V(["sky", "rose", "mint"], "coral", "sky"))

# ------------------------------------------------------------------ Wildtiere im Park (laufen/schwimmen selbst, fliehen)
for st, w, h, names, second, third in (("duck", 36, 30, ["green", "sand", "white"], "orange", "orange"),
                                       ("pigeon", 30, 26, ["grey"], "teal", "rose"),
                                       ("squirrel", 30, 32, ["rust"], "cream", "walnut")):
    T(id=f"wild_{st}", fn=PK.critter, w=w, h=h, kw={"style": st}, group="critters", category="pet", placement="floor",
      hold="two_hands", grip=[0.5, 0.5], tags=["wild"], sfx={"voice": {"duck": "duck_quack", "pigeon": "pigeon_coo",
                                                                        "squirrel": "pet_hamster_squeak"}[st]},
      variants=[(n, cols(n, second, third)) for n in names])

# ------------------------------------------------------------------ Blumen (einzeln) + Strauß (Floristin bindet 3 Blumen)
for kind, names in (("rose", ["coral", "rose", "white", "butter"]), ("tulip", ["coral", "butter", "rose", "plum"]),
                    ("sunflower", ["butter"]), ("gerbera", ["orange", "rose", "coral"])):
    T(id=f"flower_{kind}", fn=SF.flowers, w=10 if kind != "sunflower" else 16, h=45 if kind != "sunflower" else 60,
      kw={"style": "stem", "kind": kind}, group="plants", category="item", placement="table", hold="one_hand", grip=[0.5, 0.3],
      tags=["flower"], variants=[(n, cols(n, "butter", "leaf")) for n in names])
T(id="flower_bouquet", fn=SF.flowers, w=34, h=55, kw={"style": "bouquet"}, group="plants", category="item", placement="table",
  hold="one_hand", grip=[0.5, 0.2], tags=["bouquet"], variants=[(n, cols(n, "butter", "cream")) for n in ["rose", "coral", "plum", "sky"]])
