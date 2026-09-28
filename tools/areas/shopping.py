"""Einkaufsstraße (P09): Straße + 9 Läden + Gewächshaus."""
from __future__ import annotations

from .common import CAM_IN, DOOR_TOP, FLOOR, F, ON, W, deco, outdoor, shop  # noqa: F401


# ------------------------------------------------------------------ Einkaufsstraße
SHOPS = [("market", "Supermarkt", "cart"), ("bakery", "Bäckerei & Café", "bread"), ("florist", "Blumenladen", "flower"),
         ("fashion", "Modeladen", "shirt"), ("hairdresser", "Friseur", "scissors"), ("toys", "Spielzeugladen", "teddy"),
         ("petshop", "Tierhandlung", "paw"), ("icecream", "Eisdiele", "icecream"), ("music", "Musikladen", "note")]
FRONT_W = 320.0


def front_x(i: int) -> float:
    return 330.0 + i * 360.0


def street() -> dict:
    items = []
    for i, (rid, _label, motif) in enumerate(SHOPS):
        cx = front_x(i)
        items += [W("door_glass_white", cx + FRONT_W / 2 - 55, DOOR_TOP),
                  W(f"street_sign_{motif}_oak", cx + FRONT_W / 2 - 55, -300),
                  W(["street_awning_coral", "street_awning_sky", "street_awning_mint", "street_awning_butter",
                     "street_awning_rose"][i % 5], cx - 60, -300)]
    items += [F("street_bus_stop_sky", 3500, 4), F("street_street_lamp_black", 150, 2), F("street_street_lamp_black", 1230, 2),
              F("street_street_lamp_black", 2310, 2), F("street_street_lamp_black", 3280, 2),
              F("street_park_bench_oak", 870, 30), F("street_park_bench_green", 2020, 30), F("street_bin_street_green", 1000, 40),
              F("street_bin_street_green", 2700, 40), F("street_bike_stand_metal", 1500, 50), F("street_advert_column_green", 2480, 14),
              F("garden_fountain_stone", 1760, 45), F("garden_planter_box_terracotta", 610, 55), F("garden_planter_box_white", 2860, 55),
              F("street_icecream_cart_cream", 3000, 58), F("wild_pigeon_grey", 1650, 62), F("wild_pigeon_grey", 1850, 66),
              F("play_scooter_mini_mint", 1420, 64)]
    town = [[front_x(i), FRONT_W] for i in range(len(SHOPS))]
    return outdoor("shopping", "street", "Straße", "street_bus_stop_sky", 3700, items, "pavement",
                   ["#c9c6c0", "#b9b5ae", "#8a8780"], 11, town=town, height=820.0,
                   cam={"default_h_cm": 420, "min_h_cm": 240, "max_h_cm": 760}, amb="amb_garden")


def area() -> dict:
    tiles = ["#f5f3ee", "#dfe6ea", "#a9b3bd"]
    rooms = [street(),
             shop("market", "Supermarkt", "shop_cart_coral", deco(["#e6f4ec", "#ffffff", "#9fc3a0"], "", "#ffffff", "tiles", tiles), [
                 F("shop_shelf_market_cream", 180, 0), F("shop_shelf_market_sky", 320, 0), F("shop_fridge_shelf_white", 470, 0),
                 F("shop_produce_stand_oak", 640, 8), F("shop_checkout_coral", 560, 52), ON("shop_cash_register_cream", "shop_checkout_coral", 0.25),
                 ON("food_apple_red", "shop_checkout_coral", -0.3), ON("food_milk_carton", "shop_checkout_coral", -0.1),
                 F("shop_cart_coral", 250, 55), F("shop_basket_shop_sky", 380, 62), F("shop_box_oak", 720, 60),
                 F("food_banana", 700, 62), F("food_bread_loaf", 330, 64)]),
             shop("bakery", "Bäckerei & Café", "food_croissant_gold", deco(["#fbeedd", "#ffffff", "#e3c79a"], "pinstripes", "#f1dcc0",
                                                                          "planks", ["#d9a066", "#c98a4b", "#8a5a3c"]), [
                 F("shop_shelf_bread_oak", 190, 0), F("shop_counter_glass_cream", 360, 22), ON("shop_cash_register_cream", "shop_counter_glass_cream", 0.3),
                 ON("shop_coffee_machine_coral", "shop_counter_glass_cream", -0.25), F("furn_table_round_cream", 590, 45),
                 ON("food_croissant_gold", "furn_table_round_cream", -0.2), ON("kit_mug_coral", "furn_table_round_cream", 0.2),
                 F("furn_chair_dining_cream", 520, 50), F("furn_chair_dining_oak", 660, 50), F("furn_table_bistro_white", 740, 30),
                 ON("food_cake_coral", "furn_table_bistro_white", 0.0)]),
             shop("florist", "Blumenladen", "flower_bouquet_rose", deco(["#f3f7ec", "#ffffff", "#b9d7a0"], "flowers", "#dfeccc",
                                                                         "tiles", ["#e9e2d6", "#c9b9a3", "#9a8a78"]), [
                 F("shop_flower_stand_oak", 220, 10), F("shop_flower_stand_white", 660, 10), F("shop_counter_oak", 440, 24),
                 ON("shop_cash_register_cream", "shop_counter_oak", 0.3), ON("flower_rose_coral", "shop_counter_oak", -0.3),
                 ON("flower_tulip_butter", "shop_counter_oak", -0.15), ON("flower_gerbera_orange", "shop_counter_oak", 0.0),
                 F("plant_roses_bucket_coral_rose", 120, 50), F("plant_tulips_bucket_butter_coral", 560, 60),
                 F("plant_monstera_basket_oak", 760, 40), F("flower_sunflower_butter", 330, 64),
                 W("door_glass_oak", 740, DOOR_TOP)]),
             shop("greenhouse", "Gewächshaus", "garden_greenhouse_white", deco(["#e3f2f7", "#ffffff", "#bfe0d0"], "", "#ffffff", "tiles",
                                                                             ["#d8cfc2", "#c9bfb0", "#9a8f80"]), [
                 F("garden_flower_bed_l_rose", 230, 20), F("garden_flower_bed_m_butter", 470, 20), F("garden_flower_bed_m_lilac", 650, 30),
                 F("garden_raised_bed_m_tomato_oak", 300, 55), F("garden_raised_bed_m_lettuce_oak", 560, 58),
                 F("garden_watering_can_mint", 420, 64), F("garden_seeds_carrot_pack", 160, 62), F("garden_seeds_sunflower_pack", 180, 64),
                 F("plant_lemon_tree_terracotta_terracotta", 750, 10)]),
             shop("fashion", "Modeladen", "cloth_dress_rose", deco(["#fdeef2", "#ffffff", "#f0b6c2"], "dots", "#f7d9e1", "planks",
                                                                     ["#e8c49a", "#d9ae7e", "#8a5a3c"]), [
                 F("shop_hanger_rack_metal", 200, 5), F("shop_mannequin_cream", 330, 5), F("shop_fitting_room_oak", 700, 0),
                 F("shop_counter_cream", 500, 30), ON("shop_cash_register_cream", "shop_counter_cream", 0.3),
                 ON("cloth_shirt_coral", "shop_counter_cream", -0.35), ON("cloth_hat_butter", "shop_counter_cream", -0.12),
                 ON("cloth_cap_navy", "shop_counter_cream", 0.08), F("shop_mirror_stand_oak", 600, 10),
                 F("cloth_dress_sky", 150, 62), F("cloth_shoes_rose", 250, 64), F("cloth_pants_denim", 380, 60),
                 F("cloth_shirt_mint", 430, 66), F("cloth_sunglasses_black", 300, 66)]),
             shop("hairdresser", "Friseur", "shop_barber_chair_coral", deco(["#eef0fb", "#ffffff", "#b9a6d6"], "pinstripes", "#dcd6ef",
                                                                            "tiles", ["#2e3140", "#f5f3ee", "#6d6f78"]), [
                 F("shop_mirror_stand_cream", 230, 4), F("shop_barber_chair_coral", 230, 30), F("shop_mirror_stand_cream", 420, 4),
                 F("shop_barber_chair_sky", 420, 30), F("shop_hair_sink_black", 610, 20), F("shop_dryer_hood_rose", 740, 15),
                 F("shop_counter_mint", 150, 60), ON("shop_cash_register_cream", "shop_counter_mint", 0.25),
                 ON("shop_hair_tools_black", "shop_counter_mint", -0.25), F("shop_magazine_rack_metal", 530, 64)]),
             shop("toys", "Spielzeugladen", "toy_teddy_oak", deco(["#fff4d6", "#ffffff", "#f6d98a"], "stars", "#fbe3a0", "carpet",
                                                                   ["#a9c3dd", "#8fb0d0", "#6f8fb8"]), [
                 F("shop_shelf_toys_butter", 180, 0), F("shop_shelf_toys_sky", 330, 0), F("shop_counter_coral", 560, 30),
                 ON("shop_cash_register_cream", "shop_counter_coral", 0.3), ON("toy_car_coral", "shop_counter_coral", -0.3),
                 F("toy_teddy_oak", 150, 60), F("toy_ball_coral", 260, 64), F("toy_kite_sky", 700, 40), F("toy_blocks_mint", 420, 64),
                 F("toy_dollhouse_rose", 720, 10), F("toy_rocking_horse_oak", 470, 55)]),
             shop("petshop", "Tierhandlung", "petgear_bowl_coral", deco(["#eef6ea", "#ffffff", "#9fc3a0"], "", "#ffffff", "tiles",
                                                                        ["#e9e2d6", "#c9b9a3", "#9a8a78"]), [
                 F("shop_tank_shelf_black", 190, 0), F("shop_shelf_pets_mint", 340, 0), F("zoo_cage_mint", 520, 10),
                 F("shop_counter_oak", 680, 30), ON("shop_cash_register_cream", "shop_counter_oak", 0.3),
                 ON("petgear_bone_cream", "shop_counter_oak", -0.25), F("petgear_bowl_coral", 250, 62), F("petgear_basket_oak", 420, 60),
                 F("petgear_ball_butter", 460, 66), F("petgear_food_bag_butter", 580, 60), F("petgear_leash_coral", 150, 64),
                 F("pet_rabbit", 330, 50), F("pet_guinea_pig", 620, 55)]),
             shop("icecream", "Eisdiele", "food_icecream_3", deco(["#fdeef2", "#ffffff", "#a9dcd0"], "dots", "#f7d9e1", "tiles",
                                                                   ["#f5f3ee", "#f0b6c2", "#b88090"]), [
                 F("shop_icecream_counter_sky", 300, 15), ON("shop_cash_register_cream", "shop_icecream_counter_sky", 0.35),
                 ON("food_icecream_rose", "shop_icecream_counter_sky", -0.3), ON("food_icecream_mint", "shop_icecream_counter_sky", -0.15),
                 F("furn_table_bistro_white", 560, 40), F("furn_chair_dining_cream", 500, 46), F("furn_chair_dining_cream", 620, 46),
                 ON("food_icecream_3", "furn_table_bistro_white", 0.0), F("furn_table_bistro_sage", 730, 58)]),
             shop("music", "Musikladen", "music_drums_coral", deco(["#2e3140", "#6d6f78", "#f4c95d"], "", "#ffffff", "planks",
                                                                    ["#8a5e3f", "#74492f", "#4a3024"]), [
                 F("shop_shelf_electro_black", 180, 0), F("music_drums_coral", 360, 30), F("music_keyboard_black", 520, 25),
                 F("toy_guitar_coral", 440, 60), F("music_violin_oak", 610, 62), F("elec_tv_black", 690, 64),
                 F("shop_counter_oak", 700, 20), ON("shop_cash_register_black", "shop_counter_oak", 0.3),
                 ON("deco_radio_coral", "shop_counter_oak", -0.25)]),
             ]
    return {"id": "shopping", "name": "Einkaufsstraße", "name_key": "AREA_SHOPPING",
            "_doc": "P09: Straße (Häuserzeile, Bushaltestelle = zurück zur Stadtkarte) + 9 Läden + Gewächshaus. Erzeugt von "
                    "tools/make_areas.py – dort ändern.",
            "spawn": {"room": "street", "x_cm": 3380, "y_cm": 45}, "default_items": [], "music": "music_town", "rooms": rooms}


def npcs() -> dict:
    n = [{"id": f"npc_cash_{rid}", "role": "cashier", "room": rid, "x_cm": x, "y_cm": 6, "name": ""}
         for rid, x in (("market", 660), ("bakery", 440), ("fashion", 580), ("toys", 640), ("petshop", 760), ("icecream", 390),
                        ("music", 760))]
    n += [{"id": "npc_stocker", "role": "shelf_stocker", "room": "market", "x_cm": 260, "y_cm": 40},
          {"id": "npc_florist", "role": "florist", "room": "florist", "x_cm": 520, "y_cm": 6},
          {"id": "npc_hair", "role": "hairdresser", "room": "hairdresser", "x_cm": 320, "y_cm": 20},
          {"id": "npc_icecart", "role": "vendor", "room": "street", "x_cm": 3080, "y_cm": 50},
          {"id": "npc_walker1", "role": "passerby", "room": "street", "x_cm": 700, "y_cm": 58},
          {"id": "npc_walker2", "role": "passerby", "room": "street", "x_cm": 2200, "y_cm": 48}]
    return {"_doc": "Feste Figuren der Einkaufsstraße (P09). Erzeugt von tools/make_areas.py.", "area": "shopping", "npcs": n}
