"""Eishalle (P10f, Welt-Doku §9): Kasse & Verleih, Eisfläche (Gleiten, Eismaschine alle 3 Min., Eishockey, Disco),
Tribüne, Imbiss."""
from __future__ import annotations

from .common import F, ON, W, deco, shop

A = "ice"
HALL = {"default_h_cm": 380, "min_h_cm": 220, "max_h_cm": 460}
RUBBER = ["#5a6a7a", "#4a5a6a", "#2e3a48"]


def room(rid: str, label: str, icon: str, wall: list, items: list, width: float = 1000, floor: str = "tiles",
         fcols: list | None = None, height: float = 260.0, cam: dict | None = None, pattern: str = "") -> dict:
    return shop(rid, label, icon, deco(wall, pattern, "#ffffff", floor, fcols or RUBBER), items, width=width, area=A,
                height=height, cam=cam)


def area() -> dict:
    rooms = [
        room("entrance", "Kasse & Verleih", "sport_skates_cream", ["#eaf4fa", "#ffffff", "#6f8fb8"], [
            F("ice_rental_sky", 330, 10), ON("sport_skates_cream", "ice_rental_sky", -0.25), ON("sport_skates_rose", "ice_rental_sky", 0.0),
            ON("shop_cash_register_cream", "ice_rental_sky", 0.3), F("furn_bench_kitchen_white", 650, 50), F("sport_skates_sky", 600, 62),
            F("ice_penguin_navy", 820, 40), F("swim_lockers_sky", 950, 0)], floor="concrete"),
        room("rink", "Eisfläche", "ice_resurfacer_white", ["#eef6fb", "#ffffff", "#a9c3dd"], [
            F("ice_boards_white", 600, 0), F("ice_boards_white", 1200, 0), F("ice_boards_white", 1800, 0),
            F("ice_surface_white", 1200, 40), F("ice_resurfacer_white", 150, 20), F("ice_hockey_goal_coral", 450, 38),
            F("ice_hockey_goal_coral", 1950, 38), F("sport_puck_black", 1200, 45), F("sport_hockey_stick_black", 1100, 55),
            F("ice_penguin_sky", 800, 55), W("ice_disco_ball_lilac", 1200, -420), W("spc_scoreboard_navy", 700, -400)],
             width=2300, height=450, cam=HALL),
        room("stands", "Tribüne", "spc_bleachers_sky", ["#f1f4f8", "#ffffff", "#6f8fb8"], [
            F("spc_bleachers_sky", 380, 0), F("spc_bleachers_coral", 1050, 0), W("spc_scoreboard_navy", 700, -380),
            F("ice_cocoa_coral", 700, 64), F("fair_balloon_sky", 1300, 55)], width=1400, height=450, cam=HALL),
        room("snack", "Imbiss", "ice_pretzel_oak", ["#fdf3e1", "#ffffff", "#f6d98a"], [
            F("shop_counter_glass_cream", 260, 15), ON("shop_cash_register_cream", "shop_counter_glass_cream", 0.3),
            ON("ice_cocoa_coral", "shop_counter_glass_cream", -0.3), ON("ice_pretzel_oak", "shop_counter_glass_cream", -0.1),
            ON("ice_fries_coral", "shop_counter_glass_cream", 0.1), F("furn_table_bistro_white", 560, 40),
            F("furn_chair_dining_cream", 500, 46), F("furn_chair_dining_cream", 620, 46), ON("ice_cocoa_sky", "furn_table_bistro_white", 0.0),
            F("furn_table_bistro_sage", 780, 55)], width=900, floor="planks", fcols=["#e3c79a", "#d4b07c", "#8a6a4a"]),
    ]
    return {"id": A, "name": "Eishalle", "name_key": "AREA_ICE",
            "_doc": "P10f: 4 Räume. Erzeugt von tools/make_areas.py (tools/areas/ice.py) – dort ändern.",
            "spawn": {"room": "entrance", "x_cm": 520, "y_cm": 55}, "default_items": [], "music": "music_ice", "rooms": rooms}


def npcs() -> dict:
    n = [("cashier", "entrance", 330, 2), ("skate_coach", "rink", 1200, 45), ("ice_driver", "rink", 320, 30),
         ("cashier", "snack", 260, 2)]
    return {"_doc": "Feste Figuren in der Eishalle (P10f). Erzeugt von tools/make_areas.py.", "area": A,
            "npcs": [{"id": f"npc_{r}_{rid}", "role": r, "room": rid, "x_cm": x, "y_cm": y} for r, rid, x, y in n]}
