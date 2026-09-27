"""
Katalog, P07-Inventar 4 – Essen & Geschirr (Wunsch 👤: „Obst, Gemüse, Pasta, Suppen, Becher, Tassen, Teller, alles was
dazu gehört … in mehrfacher Ausführung“). Pflichtliste: data/inventory.json.
Kategorie food: 2–35 cm, kitchen: 1,5–45 cm (Maßstab-Regeln).
"""
from __future__ import annotations

from . import pantry as PA
from . import produce as PR
from . import tableware as TW
from .catalog import TEMPLATES, S, cols

# ------------------------------------------------------------------ Obst & Gemüse (echte Größen in cm)
PRODUCE = (
    # Stil, Breite, Höhe, [(Name, Zone1, Zone2, Zone3)]
    ("grapes", 12, 16, [("green", "leaf_light", "cream", "leaf"), ("blue", "plum", "cream", "leaf")]),
    ("strawberry", 3.5, 4.5, [("red", "coral", "butter", "leaf")]),
    ("cherry", 5, 7, [("red", "rust", "cream", "leaf")]),
    ("pineapple", 12, 30, [("gold", "yellow", "orange", "leaf")]),
    ("kiwi", 6, 5.5, [("brown", "oak", "leaf_light", "leaf")]),
    ("plum", 5, 5.5, [("purple", "plum", "rose", "leaf")]),
    ("mango", 9, 11, [("orange", "orange", "coral", "leaf")]),
    ("melon", 16, 14, [("honey", "butter", "leaf_light", "leaf")]),
    ("apricot", 5, 4.8, [("orange", "orange", "coral", "leaf")]),
    ("blueberries", 10, 7, [("blue", "denim", "cream", "leaf")]),
    ("coconut", 12, 12, [("brown", "walnut", "cream", "leaf")]),
    ("cucumber", 22, 5, [("green", "leaf", "leaf_light", "leaf_dark")]),
    ("potato", 8, 6, [("yellow", "sand", "cream", "leaf")]),
    ("onion", 7, 8, [("brown", "oak", "butter", "leaf")]),
    ("pepper", 8, 10, [("red", "coral", "cream", "leaf"), ("yellow", "yellow", "cream", "leaf"), ("green", "leaf_light", "cream", "leaf_dark")]),
    ("broccoli", 14, 16, [("green", "leaf", "cream", "leaf_light")]),
    ("lettuce", 18, 14, [("green", "leaf_light", "cream", "leaf_light")]),
    ("corn", 7, 22, [("yellow", "yellow", "cream", "leaf")]),
    ("pumpkin", 28, 24, [("orange", "orange", "cream", "leaf"), ("green", "leaf", "cream", "walnut")]),
    ("eggplant", 20, 9, [("purple", "plum", "cream", "leaf")]),
    ("peas", 10, 4, [("green", "leaf_light", "cream", "leaf")]),
    ("radish", 4, 5, [("red", "coral", "white", "leaf")]),
    ("mushroom", 6, 6, [("brown", "oak", "cream", "leaf"), ("white", "cream", "linen", "leaf")]),
    ("garlic", 5, 5.5, [("white", "cream", "linen", "leaf")]),
    ("zucchini", 22, 5, [("green", "leaf_dark", "leaf_light", "leaf")]),
    ("cauliflower", 16, 14, [("white", "leaf", "cream", "leaf_light")]),
    ("leek", 30, 4, [("green", "leaf", "white", "leaf_light")]),
)
for style, w, h, vs in PRODUCE:
    S(f"food_{style}", PR.produce, style, w, h, "food", "food", [v[0] for v in vs])
    # Farben je Variante genau setzen (S() verteilt sonst Zweit-/Drittfarbe gleich)
    TEMPLATES[-1]["variants"] = [(n, cols(a, b, c)) for n, a, b, c in vs]

# ------------------------------------------------------------------ Vorrat, Frühstück, Süßes, Gerichte
PANTRY = (
    ("spaghetti", 26, 12, [("tomato", "butter", "coral", "cream"), ("pesto", "butter", "leaf", "sky")]),
    ("pasta_spaghetti", 8, 28, [("blue", "sky", "butter", "coral")]),
    ("pasta_penne", 12, 20, [("red", "coral", "butter", "cream")]),
    ("pasta_farfalle", 12, 20, [("green", "leaf_light", "butter", "cream")]),
    ("rice", 12, 18, [("white", "cream", "sky", "cream")]),
    ("roll", 9, 6, [("light", "oak", "cream", "cream"), ("dark", "walnut", "cream", "cream")]),
    ("pretzel", 14, 12, [("brown", "walnut", "white", "cream")]),
    ("baguette", 34, 6, [("gold", "oak", "cream", "cream")]),
    ("croissant", 14, 7, [("gold", "oak", "cream", "cream")]),
    ("milk", 7, 22, [("white", "white", "sky", "sky"), ("choco", "white", "walnut", "walnut")]),
    ("juice", 7, 22, [("orange", "orange", "yellow", "leaf"), ("apple", "leaf_light", "coral", "leaf"), ("red", "plum", "rose", "leaf")]),
    ("water", 7, 24, [("blue", "sky", "blue", "blue"), ("green", "leaf_light", "leaf", "leaf")]),
    ("yogurt", 7, 7, [("strawberry", "white", "rose", "coral"), ("vanilla", "white", "butter", "sky"), ("berry", "white", "plum", "lilac")]),
    ("butter", 10, 4, [("gold", "butter", "sky", "cream")]),
    ("cereal", 20, 28, [("red", "coral", "butter", "cream"), ("blue", "sky", "butter", "cream"), ("green", "leaf_light", "oak", "cream")]),
    ("jam", 7, 9, [("strawberry", "coral", "cream", "rose"), ("apricot", "orange", "cream", "leaf_light"), ("cherry", "plum", "cream", "coral")]),
    ("honey", 7, 9, [("gold", "yellow", "orange", "oak")]),
    ("cookie", 6, 3, [("choc", "oak", "walnut", "cream"), ("plain", "butter", "oak", "cream"), ("dark", "walnut", "cream", "cream")]),
    ("chocolate", 16, 8, [("milk", "sky", "walnut", "cream"), ("dark", "navy", "dark_wood", "cream"), ("white", "rose", "cream", "cream")]),
    ("candy", 10, 6, [("mix", "coral", "sky", "butter"), ("sour", "leaf_light", "yellow", "orange"), ("berry", "plum", "rose", "coral")]),
    ("donut", 9, 4.5, [("pink", "oak", "rose", "sky"), ("choc", "oak", "walnut", "butter"), ("white", "oak", "cream", "coral")]),
    ("lollipop", 7, 16, [("rainbow", "coral", "butter", "white"), ("blue", "sky", "white", "white"), ("green", "leaf_light", "yellow", "white")]),
    ("burger", 12, 10, [("classic", "oak", "yellow", "leaf")]),
    ("fries", 10, 14, [("red", "coral", "butter", "white")]),
    ("hotdog", 16, 6, [("classic", "pine", "yellow", "rust")]),
    ("sandwich", 12, 11, [("cheese", "pine", "butter", "leaf"), ("ham", "pine", "rose", "leaf")]),
    ("salad", 20, 10, [("green", "cream", "coral", "leaf_light"), ("mixed", "sky", "yellow", "leaf")]),
)
for style, w, h, vs in PANTRY:
    gid = "food_pasta_" + style.split("_")[1] if style.startswith("pasta_") else f"food_{style}"
    S(gid, PA.pantry, style, w, h, "food", "food", [v[0] for v in vs])
    TEMPLATES[-1]["variants"] = [(n, cols(a, b, c)) for n, a, b, c in vs]

# ------------------------------------------------------------------ Geschirr & Tischzubehör
DISHES = (
    ("teacup", 14, 8, ["cream", "rose", "sky", "mint", "white"], "coral", "cream"),
    ("plate_deep", 22, 5, ["white", "cream", "sky", "sage"], "coral", "metal"),
    ("plate_kids", 22, 3, ["butter", "sky", "rose"], "coral", "metal"),
    ("glass_wine", 8, 20, ["sky", "rose"], "rust", "metal"),
    ("glass_tumbler", 7, 10, ["sky", "mint", "rose"], "orange", "metal"),
    ("teaspoon", 3, 13, ["metal", "#e0b84a"], "cream", "metal"),
    ("jug", 16, 22, ["cream", "sky", "coral"], "sky", "metal"),
    ("carafe", 12, 26, ["sky", "mint"], "sky", "metal"),
    ("thermos", 9, 30, ["navy", "coral", "metal"], "cream", "black"),
    ("egg_cup", 5, 8, ["coral", "sky", "butter", "mint", "white"], "cream", "metal"),
    ("sugar_bowl", 10, 10, ["cream", "sky"], "white", "metal"),
    ("butter_dish", 18, 8, ["cream", "white", "sky"], "butter", "metal"),
    ("cake_stand", 30, 30, ["white", "sky"], "rose", "cream"),
    ("salad_bowl", 28, 12, ["oak", "white", "sky"], "leaf_light", "metal"),
    ("lunchbox", 18, 8, ["coral", "sky", "mint", "butter"], "white", "metal"),
    ("drink_bottle", 7, 22, ["coral", "sky", "mint", "plum"], "white", "grey"),
    ("napkins", 16, 4, ["coral", "sky", "butter"], "white", "metal"),
    ("placemat", 40, 3, ["oak", "coral", "sky", "sage"], "cream", "metal"),
)
for style, w, h, names, second, third in DISHES:
    gid = "kit_glass_" + style.split("_")[1] if style.startswith("glass_") else f"kit_{style}"
    S(gid, TW.tableware, style, w, h, "kitchen", "kitchen", names, second=second, third=third,
      tags=["stackable"] if style in ("plate_deep", "plate_kids") else None)
