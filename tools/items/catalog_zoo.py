"""
Katalog, Teil P10g (Zoo, Welt-Doku §10): 21 Tierarten in echter Größe (Giraffe 4,8 m → Kamera zoomt raus),
Gehege-Einrichtung und Futter. Tiere sind Haustier-Knoten mit Tag „zoo“: bleiben in ihrem Gehege, melden sich,
fressen NUR ihr Futter (Tags „eats:<ID-Präfix>“ – Daten, nicht Code). Kleine Streichelzoo-Tiere sind ✋ tragbar,
Affen („steals“) klauen ab und zu ein kleines Ding und legen es woanders hin.
"""
from __future__ import annotations

from . import zoo_animals as ZA
from . import zoo_props as ZP
from .catalog import T, cols

LEAVES, HAY, MEAT, FISH, SEEDS = "zoo_food_leaves", "zoo_food_hay", "zoo_food_meat", "zoo_food_fish", "zoo_food_seeds"
BANANA, APPLE, CARROT = "food_banana", "food_apple", "food_carrot"

# Art: Breite, Höhe (cm, echt), Farben (Fell, hell, Akzent), Stimme, Futter, tragbar, Extra-Tags
ANIMALS = {
    "giraffe": (360, 480, ("butter", "cream", "rust"), "pet_hamster_squeak", [LEAVES], False, []),
    "zebra": (230, 145, ("white", "cream", "black"), "pet_pony_whinny", [HAY, CARROT, APPLE], False, []),
    "lion": (200, 120, ("oak", "cream", "rust"), "roar", [MEAT], False, []),
    "lion_cub": (70, 45, ("oak", "cream", "walnut"), "roar", [MEAT], True, ["baby"]),
    "elephant": (450, 300, ("grey", "linen", "rose"), "trumpet", [HAY, BANANA, APPLE], False, []),
    "elephant_baby": (150, 100, ("metal", "linen", "rose"), "trumpet", [HAY, BANANA, APPLE], False, ["baby"]),
    "goat": (70, 55, ("white", "linen", "grey"), "bleat", [HAY, CARROT], True, ["pettable"]),
    "lamb": (70, 55, ("cream", "white", "taupe"), "bleat", [HAY, CARROT], True, ["pettable"]),
    "pig": (55, 38, ("rose", "cream", "coral"), "oink", [APPLE, CARROT], True, ["pettable"]),
    "penguin": (40, 70, ("navy", "white", "orange"), "penguin", [FISH], False, []),
    "penguin_chick": (30, 38, ("grey", "linen", "black"), "penguin", [FISH], True, ["baby"]),
    "flamingo": (90, 130, ("rose", "cream", "coral"), "duck_quack", [SEEDS], False, []),
    "parrot": (40, 55, ("coral", "butter", "sky"), "pet_bird_chirp", [SEEDS, BANANA], True, []),
    "chick": (12, 12, ("butter", "cream", "orange"), "pet_bird_chirp", [SEEDS], True, ["pettable"]),
    "monkey": (70, 80, ("walnut", "sand", "taupe"), "monkey", [BANANA, APPLE], False, ["steals"]),
    "gorilla": (120, 150, ("black", "grey", "taupe"), "monkey", [BANANA, LEAVES], False, []),
    "meerkat": (20, 32, ("sand", "cream", "navy"), "pet_guinea_pig_wheek", [SEEDS], True, []),
    "rabbit": (30, 26, ("linen", "white", "rose"), "pet_rabbit_squeak", [CARROT, HAY], True, ["pettable"]),
    "crocodile": (350, 50, ("green", "sage", "leaf_dark"), "pet_turtle_hiss", [FISH, MEAT], False, []),
    "tortoise": (130, 70, ("oak", "sage", "walnut"), "pet_turtle_hiss", [LEAVES, APPLE], False, []),
    "snake": (60, 30, ("leaf_light", "butter", "coral"), "pet_turtle_hiss", [MEAT], False, []),
}
for sp, (w, h, (z1, z2, z3), voice, food, carry, extra) in ANIMALS.items():
    T(id=f"zoo_{sp}", fn=ZA.zoo_animal, w=w, h=h, kw={"style": sp}, group="animals", category="animal", placement="floor",
      hold=("one_hand" if h <= 20 else "two_hands") if carry else "none", grip=[0.5, 0.5],
      tags=["zoo"] + [f"eats:{f}" for f in food] + extra, sfx={"voice": voice}, variants=[(z1, cols(z1, z2, z3))])

for st, w, h, names, second, third, extra in (
        ("rock", 300, 150, ["stone", "sand"], "sage", "grey", {}),
        ("acacia", 600, 560, ["leaf"], "cream", "walnut", {}),
        ("ice_floe", 400, 110, ["white"], "sky", "white", {}),
        ("terrarium", 200, 160, ["oak", "dark_wood"], "sand", "white", {}),
        ("tank", 420, 240, ["navy", "dark_wood"], "#7cc6e0", "coral", {"states": {"feed": {"state": "feed"}}, "state0": "calm",
                                                                        "sfx": {"feed": "pet_fish_bubble"}}),
        ("climb_frame", 420, 420, ["oak"], "sand", "coral", {"seat": {"h": 220, "pose": "sit", "slots": 2}}),
        ("hay_rack", 120, 140, ["oak"], "butter", "sand", {}),
        ("sign", 80, 140, ["oak", "green"], "cream", "walnut", {})):
    T(id=f"zoo_{st}", fn=ZP.zoo_prop, w=w, h=h, kw={"style": st}, group="animals", category="furniture", placement="floor",
      variants=[(n, cols(n, second, third)) for n in names], **extra)
T(id="zoo_pond", fn=ZP.zoo_prop, w=500, h=70, kw={"style": "pond"}, group="animals", category="deco", placement="rug",
  variants=[("stone", cols("stone", "#7cc6e0", "white"))])
for st, w, h, names, second in (("meat", 22, 12, ["coral"], "cream"), ("fish", 24, 10, ["sky"], "white"),
                                ("leaves", 40, 30, ["leaf"], "leaf"), ("hay", 30, 22, ["butter"], "butter"),
                                ("seeds", 14, 7, ["oak"], "oak")):
    T(id=f"zoo_food_{st}", fn=ZP.zoo_prop, w=w, h=h, kw={"style": st if st != "fish" else "fish_food"}, group="animals",
      category="item", placement="table", hold="one_hand", grip=[0.5, 0.5], tags=["zoo_food"],
      variants=[(n, cols(n, second, "walnut")) for n in names])
T(id="zoo_bucket", fn=ZP.zoo_prop, w=30, h=30, kw={"style": "bucket"}, group="animals", category="item", placement="table",
  hold="one_hand", grip=[0.5, 0.95], container={"slots": 3, "max_item_h_cm": 25},
  variants=[(n, cols(n, "sand", "metal")) for n in ["sky", "coral"]])
