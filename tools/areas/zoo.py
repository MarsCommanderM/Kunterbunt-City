"""Zoo (P10g, Welt-Doku §10): Eingang, Savanne (Giraffe, Zebras, Löwe, Flamingos, Erdmännchen), Affenhaus,
Elefanten, Pinguine, Reptilien, Aquarium, Streichelzoo, Tierbaby-Station. Tiere in echter Größe (Giraffe 4,8 m →
Kamera bis 7 m). Richtiges Futter → Freude, Pfleger/innen füttern alle 90 s, Affen „leihen“ sich Dinge aus."""
from __future__ import annotations

from .common import F, ON, W, deco, outdoor, shop

A = "zoo"
GRASS = ["#9fc98a", "#8bbb78", "#6f9a5e"]
SAVANNA = ["#e3c98c", "#d4b878", "#a88c58"]
TALL = {"default_h_cm": 480, "min_h_cm": 240, "max_h_cm": 700}


def out(rid: str, label: str, icon: str, width: float, items: list, seed: int, floor: str = "grass", cols: list | None = None) -> dict:
    return outdoor(A, rid, label, icon, width, items, floor, cols or GRASS, seed, height=800, cam=TALL)


def room(rid: str, label: str, icon: str, wall: list, items: list, width: float = 1100, floor: str = "tiles",
         fcols: list | None = None, height: float = 260.0, pattern: str = "") -> dict:
    cam = {"default_h_cm": 380, "min_h_cm": 220, "max_h_cm": min(700.0, height)} if height > 260 else None
    return shop(rid, label, icon, deco(wall, pattern, "#ffffff", floor, fcols or ["#e3dcc8", "#d4cbb4", "#9a8f78"]), items,
                width=width, area=A, height=height, cam=cam)


def area() -> dict:
    rooms = [
        out("entrance", "Eingang", "zoo_sign_green", 1400, [
            F("fair_gate_coral", 700, 5), F("fair_ticket_booth_sky", 300, 10), F("zoo_sign_green", 1050, 30),
            F("zoo_sign_oak", 1150, 30), F("zoo_parrot_coral", 480, 60), F("street_park_bench_green", 1250, 20),
            F("fair_balloon_mint", 420, 58)], 51, floor="pavement", cols=["#d8cfc2", "#c9bfb0", "#9a8f80"]),
        out("savanna", "Savanne", "zoo_giraffe_butter", 2800, [
            F("zoo_acacia_leaf", 500, 0), F("zoo_giraffe_butter", 700, 15), F("zoo_zebra_white", 1150, 30), F("zoo_zebra_white", 1400, 50),
            F("zoo_rock_sand", 2200, 5), F("zoo_lion_oak", 2150, 40), F("zoo_pond_stone", 1750, 45), F("zoo_flamingo_rose", 1700, 40),
            F("zoo_flamingo_rose", 1820, 50), F("zoo_meerkat_sand", 2500, 55), F("zoo_meerkat_sand", 2550, 60),
            F("zoo_food_leaves_leaf", 1300, 64), F("zoo_sign_oak", 2650, 20)], 52, floor="sand", cols=SAVANNA),
        room("monkeys", "Affenhaus", "zoo_monkey_walnut", ["#eef6e8", "#ffffff", "#7fae6a"], [
            F("zoo_climb_frame_oak", 400, 5), F("zoo_monkey_walnut", 350, 40), F("zoo_monkey_walnut", 650, 55),
            F("zoo_gorilla_black", 950, 20), F("zoo_parrot_coral", 100, 50), F("food_banana_butter", 1250, 64),
            F("plant_monstera_basket_oak", 200, 20), F("zoo_rock_stone", 1350, 5)], width=1450, height=500,
             floor="grass", fcols=GRASS, pattern="dots"),
        out("elephants", "Elefanten", "zoo_elephant_grey", 2200, [
            F("zoo_pond_stone", 1500, 45), F("zoo_elephant_grey", 800, 20), F("zoo_elephant_baby_metal", 1250, 50),
            F("zoo_hay_rack_oak", 300, 10), F("zoo_acacia_leaf", 1900, 0), F("zoo_food_hay_butter", 400, 64)], 53, floor="sand",
            cols=SAVANNA),
        out("penguins", "Pinguine", "zoo_penguin_navy", 1500, [
            F("zoo_ice_floe_white", 450, 10), F("zoo_pond_stone", 1000, 45), F("zoo_penguin_navy", 400, 40),
            F("zoo_penguin_navy", 600, 50), F("zoo_penguin_navy", 950, 45), F("zoo_penguin_chick_grey", 700, 60),
            F("zoo_bucket_sky", 1300, 62)], 54, floor="concrete", cols=["#e8f0f4", "#d8e4ea", "#a9b8c2"]),
        room("reptiles", "Reptilien", "zoo_crocodile_green", ["#eef3e4", "#ffffff", "#5f8f6a"], [
            F("zoo_terrarium_oak", 250, 5), F("zoo_snake_leaf_light", 250, 55), F("zoo_pond_stone", 700, 40),
            F("zoo_crocodile_green", 700, 45), F("zoo_tortoise_oak", 1050, 50), F("zoo_terrarium_dark_wood", 1200, 5)], width=1400,
             floor="grass", fcols=["#b8b87a", "#a8a86a", "#7a7a4a"]),
        room("aquarium", "Aquarium", "zoo_tank_navy", ["#1f3552", "#2e4a6e", "#162840"], [
            F("zoo_tank_navy", 330, 5), F("zoo_tank_dark_wood", 800, 5), F("zoo_tank_navy", 1250, 5),
            F("street_park_bench_green", 600, 55), F("street_park_bench_green", 1050, 55)], width=1500, floor="tiles",
             fcols=["#3a4a60", "#2e3c50", "#1a2636"]),
        out("petting", "Streichelzoo", "zoo_goat_white", 1700, [
            F("garden_fence_rustic_oak", 200, 5), F("garden_fence_rustic_oak", 600, 5), F("garden_fence_rustic_oak", 1000, 5),
            F("zoo_hay_rack_oak", 1300, 10), F("zoo_goat_white", 350, 40), F("zoo_goat_white", 520, 55), F("zoo_lamb_cream", 750, 45),
            F("zoo_pig_rose", 950, 55), F("zoo_rabbit_linen", 1150, 60), F("zoo_rabbit_linen", 1200, 64), F("zoo_chick_butter", 1400, 62),
            F("zoo_chick_butter", 1430, 66), F("zoo_chick_butter", 1460, 60), F("zoo_bucket_coral", 1550, 62),
            F("food_carrot_orange", 1580, 66), F("zoo_food_seeds_oak", 1660, 66)], 55),
        room("nursery", "Tierbabys", "zoo_lion_cub_oak", ["#fff4e8", "#ffffff", "#f6d98a"], [
            F("zoo_lion_cub_oak", 300, 50), F("zoo_penguin_chick_grey", 520, 55), F("med_incubator_white", 720, 10),
            F("med_baby_scale_white", 900, 40), F("baby_bottle_sky", 420, 64), F("zoo_food_fish_sky", 960, 66),
            F("petgear_basket_oak", 150, 30)], width=1050, floor="planks", fcols=["#e3c79a", "#d4b07c", "#8a6a4a"], pattern="dots"),
    ]
    return {"id": A, "name": "Zoo", "name_key": "AREA_ZOO",
            "_doc": "P10g: 9 Bereiche. Erzeugt von tools/make_areas.py (tools/areas/zoo.py) – dort ändern.",
            "spawn": {"room": "entrance", "x_cm": 560, "y_cm": 55}, "default_items": [], "music": "music_zoo", "rooms": rooms}


def npcs() -> dict:
    n = [("cashier", "entrance", 300, 5), ("zoo_director", "entrance", 950, 40), ("zookeeper", "savanna", 1000, 60),
         ("guide", "savanna", 1500, 62), ("zookeeper", "petting", 800, 62), ("vet", "nursery", 820, 50)]
    return {"_doc": "Feste Figuren im Zoo (P10g). Erzeugt von tools/make_areas.py.", "area": A,
            "npcs": [{"id": f"npc_{r}_{rid}", "role": r, "room": rid, "x_cm": x, "y_cm": y} for r, rid, x, y in n]}
