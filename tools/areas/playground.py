"""Spielplatz & Park (P09): Spielplatz, Teich, Wiese."""
from __future__ import annotations

from .common import CAM_IN, DOOR_TOP, FLOOR, F, ON, W, deco, outdoor, shop  # noqa: F401


# ------------------------------------------------------------------ Spielplatz & Park
GRASS = ["#8cc47a", "#7fb36e", "#5f8f4a"]


def area() -> dict:
    trees = lambda xs: [F("camp_tree_leaf", x, 2) if k % 2 else F("camp_tree_leaf_light", x, 4) for k, x in enumerate(xs)]  # noqa: E731
    play = [F("play_tower_slide_coral", 420, 10), F("play_swing_double_sky", 880, 12), F("play_roundabout_coral", 1260, 40),
            F("play_spring_rider_butter", 1480, 50), F("play_spring_rider_mint", 1580, 58), F("play_climber_butter", 1900, 8),
            F("garden_sandbox_big_butter", 1250, 62), F("play_sand_mold_coral", 1180, 66), F("play_sand_mold_sky", 1320, 66),
            F("toy_bucket_spade_butter", 1270, 68), F("play_seesaw_coral", 2180, 45), F("street_park_bench_green", 700, 30),
            F("street_bin_street_green", 1060, 40), F("play_bubble_wand_sky", 1500, 66)] + trees([90, 2330])
    pond = [F("garden_pond_l_stone", 700, 40), F("garden_pond_m_stone", 1300, 50), F("wild_duck_green", 640, 44),
            F("wild_duck_sand", 760, 46), F("wild_duck_white", 1300, 54), F("wild_duck_green", 1360, 52),
            F("street_park_bench_oak", 1000, 20), F("wild_squirrel_rust", 1650, 30), F("wild_pigeon_grey", 980, 60),
            F("camp_bush_leaf", 250, 10), F("camp_bush_leaf_light", 1800, 12)] + trees([80, 420, 1550, 1920])
    meadow = [F("street_icecream_cart_rose", 1500, 20), F("garden_picnic_blanket_coral", 500, 50),
              F("garden_picnic_basket_oak", 560, 52), F("food_apple_red", 460, 56), F("toy_kite_coral", 800, 60),
              F("toy_ball_sky", 1000, 62), F("garden_picnic_blanket_sky", 1100, 40), F("street_park_bench_oak", 1800, 25),
              F("street_bin_street_green", 1920, 40), F("petgear_ball_coral", 1250, 64)] + trees([120, 320, 1680, 1950])
    rooms = [outdoor("playground", "playground", "Spielplatz", "play_tower_slide_coral", 2400, play, "grass", GRASS, 7),
             outdoor("playground", "pond", "Teich", "wild_duck_green", 2000, pond, "grass", ["#a6cf7c", "#94c06c", "#6f9a4a"], 8),
             outdoor("playground", "meadow", "Wiese", "garden_picnic_blanket_coral", 2000, meadow, "grass", GRASS, 9)]
    return {"id": "playground", "name": "Spielplatz & Park", "name_key": "AREA_PLAYGROUND",
            "_doc": "P09: Spielplatz (Schaukel, Rutsche, Karussell, Federwippe, Klettergerüst, Sandkasten), Teich mit Enten, "
                    "Wiese mit Eiswagen. Erzeugt von tools/make_areas.py – dort ändern.",
            "spawn": {"room": "playground", "x_cm": 1000, "y_cm": 55}, "default_items": [], "music": "music_park", "rooms": rooms}


def npcs() -> dict:
    return {"_doc": "Feste Figuren im Park (P09). Erzeugt von tools/make_areas.py.", "area": "playground", "npcs": [
        {"id": "npc_ranger", "role": "supervisor", "room": "playground", "x_cm": 1700, "y_cm": 30},
        {"id": "npc_granny", "role": "duck_feeder", "room": "pond", "x_cm": 1000, "y_cm": 30},
        {"id": "npc_icevendor", "role": "vendor", "room": "meadow", "x_cm": 1580, "y_cm": 14},
        {"id": "npc_jogger", "role": "jogger", "room": "meadow", "x_cm": 900, "y_cm": 62}]}
