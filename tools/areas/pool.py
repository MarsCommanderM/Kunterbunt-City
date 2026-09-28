"""Freizeitbad (P10c, Welt-Doku §6): Kasse & Umkleiden, Schwimmhalle (Schwimmerbecken), Babybecken, Whirlpool,
Freibad mit Sprungturm (1/3/5 m) und Wasserrutsche, Liegewiese mit Kiosk. Schwimmen = in einem Becken sitzen;
der Bademeister zählt die Figuren im Wasser (Rolle lifeguard, `water`)."""
from __future__ import annotations

from .common import F, ON, W, deco, outdoor, shop

A = "pool"
TILES = ["#e9f5f8", "#cfe6ee", "#7cb4c8"]


def room(rid: str, label: str, icon: str, wall: list, items: list, width: float = 800, pattern: str = "",
         pcol: str = "#ffffff") -> dict:
    return shop(rid, label, icon, deco(wall, pattern, pcol, "tiles", TILES), items, width=width, area=A, amb="amb_bath")


def area() -> dict:
    rooms = [
        room("entrance", "Kasse & Umkleiden", "swim_turnstile_metal", ["#eaf6f8", "#ffffff", "#7cc6e0"], [
            F("shop_counter_oak", 260, 15), ON("shop_cash_register_cream", "shop_counter_oak", 0.3),
            ON("swim_dive_rings_coral", "shop_counter_oak", -0.3), F("swim_turnstile_metal", 420, 30),
            F("swim_lockers_sky", 560, 0), F("swim_lockers_coral", 690, 0), F("swim_cabin_white", 820, 5),
            F("swim_cabin_white", 940, 5), F("swim_bench_tiled_white", 620, 55), F("pool_towel_beach_sky", 600, 58),
            F("pool_goggles_coral", 660, 60), F("swim_shower_metal", 1050, 10)], width=1150),
        room("hall", "Schwimmhalle", "swim_basin_sky", ["#e6f2f8", "#ffffff", "#6f8fb8"], [
            F("swim_basin_sky", 620, 30), F("swim_start_block_white", 230, 8), F("swim_start_block_white", 330, 8),
            F("swim_start_block_white", 430, 8), F("swim_guard_chair_coral", 1180, 15), F("swim_lifebuoy_coral", 1110, 60),
            F("swim_kickboard_sky", 140, 60), F("swim_kickboard_butter", 180, 62), F("pool_noodle_coral", 90, 64),
            W("swim_wave_sign_navy", 620, -200), F("swim_bench_tiled_sky", 1000, 62)], width=1300),
        room("babies", "Babybecken", "swim_baby_pool_butter", ["#fff6e0", "#ffffff", "#f6d98a"], [
            F("swim_baby_pool_butter", 400, 30), F("pool_inflatable_animal_butter", 240, 62), F("swim_beach_ball_coral", 560, 62),
            F("pool_swim_ring_mint", 620, 64), F("swim_bench_tiled_white", 700, 15), F("swim_shower_metal", 120, 10),
            F("bath_duck_yellow", 470, 64)], pattern="dots", pcol="#fbe8b0"),
        room("whirl", "Whirlpool", "swim_whirlpool_sky", ["#eef0f8", "#ffffff", "#b9a6d6"], [
            F("swim_whirlpool_sky", 300, 25), F("swim_whirlpool_sand", 580, 35), F("pool_deck_chair_teal", 760, 55),
            F("pool_towel_beach_coral", 700, 62), F("plant_monstera_basket_oak", 100, 20)], width=880),
    ]
    rooms.append(outdoor(A, "outside", "Freibad", "swim_diving_tower_sky", 2600, [
        F("swim_basin_sky", 900, 35), F("swim_diving_tower_sky", 620, 5), F("swim_water_slide_butter", 1500, 5),
        F("swim_basin_white", 1780, 40), F("swim_guard_chair_white", 1250, 20), F("swim_lifebuoy_orange", 1320, 60),
        F("pool_umbrella_butter", 2200, 20), F("pool_deck_chair_coral", 2250, 45), F("swim_shower_metal", 200, 15),
        F("swim_beach_ball_sky", 2050, 62)], "tiles", TILES, 21, height=800,
        cam={"default_h_cm": 450, "min_h_cm": 240, "max_h_cm": 700}))
    rooms.append(outdoor(A, "lawn", "Liegewiese", "swim_kiosk_butter", 1800, [
        F("swim_kiosk_butter", 400, 10), ON("shop_cash_register_cream", "swim_kiosk_butter", 0.3),
        ON("food_icecream_butter", "swim_kiosk_butter", -0.3), F("pool_umbrella_coral", 800, 20), F("pool_deck_chair_sky", 850, 45),
        F("pool_towel_beach_butter", 1000, 60), F("pool_cooler_coral", 1100, 58), F("pool_umbrella_butter", 1300, 25),
        F("pool_deck_chair_butter", 1350, 50), F("swim_beach_ball_butter", 1500, 62), F("pool_sunscreen_orange", 1040, 64),
        F("camp_tree_leaf", 1650, 5)], "grass", ["#9fc98a", "#8bbb78", "#6f9a5e"], 22))
    return {"id": A, "name": "Freizeitbad", "name_key": "AREA_POOL",
            "_doc": "P10c: 6 Räume. Erzeugt von tools/make_areas.py (tools/areas/pool.py) – dort ändern.",
            "spawn": {"room": "entrance", "x_cm": 350, "y_cm": 55}, "default_items": [], "music": "music_pool", "rooms": rooms}


def npcs() -> dict:
    n = [("cashier", "entrance", 260, 2), ("lifeguard", "hall", 900, 60), ("swim_teacher", "babies", 560, 40),
         ("lifeguard", "outside", 1100, 62), ("vendor", "lawn", 400, 2)]
    return {"_doc": "Feste Figuren im Freizeitbad (P10c). Erzeugt von tools/make_areas.py.", "area": A,
            "npcs": [{"id": f"npc_{r}_{rid}", "role": r, "room": rid, "x_cm": x, "y_cm": y} for r, rid, x, y in n]}
