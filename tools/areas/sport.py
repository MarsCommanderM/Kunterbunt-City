"""Sportzentrum (P10e, Welt-Doku §8): Empfang, Fitness, Sporthalle, Fußballplatz mit Tribüne, Tennis, Kletterwand,
Ballettraum. Ball antippen = schießen (Ball-Physik), Tor-Erkennung zählt auf der Anzeigetafel, Trainer jubelt."""
from __future__ import annotations

from .common import F, ON, W, deco, outdoor, shop

A = "sports"
WOOD = ["#e3c79a", "#d4b07c", "#8a6a4a"]
GRASS = ["#9fc98a", "#8bbb78", "#6f9a5e"]


def room(rid: str, label: str, icon: str, wall: list, items: list, width: float = 900, floor: str = "planks",
         fcols: list | None = None, height: float = 260.0, cam: dict | None = None, pattern: str = "") -> dict:
    return shop(rid, label, icon, deco(wall, pattern, "#ffffff", floor, fcols or WOOD), items, width=width, area=A,
                height=height, cam=cam)


def area() -> dict:
    rooms = [
        room("reception", "Empfang", "sport_trophy_butter", ["#eef3f8", "#ffffff", "#6f8fb8"], [
            F("shop_counter_oak", 300, 15), ON("sport_trophy_butter", "shop_counter_oak", -0.3), F("swim_lockers_sky", 560, 0),
            F("swim_lockers_coral", 690, 0), F("furn_bench_kitchen_white", 620, 55), F("spc_football_white", 450, 62),
            F("plant_monstera_basket_oak", 820, 20)], floor="tiles", fcols=["#eef0f2", "#d9dde2", "#9aa6b4"]),
        room("fitness", "Fitness", "sport_dumbbell_coral", ["#fdf0ee", "#ffffff", "#e07a7a"], [
            F("spc_treadmill_black", 200, 10), F("spc_treadmill_grey", 420, 10), F("spc_bike_coral", 620, 25),
            F("spc_bench_black", 800, 40), F("sport_dumbbell_coral", 870, 62), F("spc_yoga_ball_sky", 980, 55),
            F("sport_mat_teal", 1100, 60), W("spc_mirror_white", 600, -220)], width=1200),
        room("hall", "Sporthalle", "sport_basket_hoop_coral", ["#f3f6fa", "#ffffff", "#a9c3dd"], [
            F("sport_basket_hoop_coral", 150, 5), F("edu_vault_box_oak", 450, 25), F("edu_balance_beam_sky", 750, 25),
            F("edu_ball_cart_coral", 1050, 15), F("toy_ball_coral", 600, 60), F("sport_mat_sky", 1000, 60), F("sport_cone_orange", 300, 62),
            W("spc_scoreboard_navy", 700, -380)], width=1400, height=450, cam={"default_h_cm": 380, "min_h_cm": 220, "max_h_cm": 460}),
        room("climbing", "Kletterwand", "spc_climbing_wall_sand", ["#eef0f8", "#ffffff", "#b9a6d6"], [
            F("spc_climbing_wall_sand", 450, 0), F("sport_mat_coral", 450, 40), F("furn_bench_kitchen_oak", 800, 55),
            F("spc_climbing_wall_grey", 1050, 0)], width=1300, height=700, floor="concrete", fcols=["#c8c8c8", "#b8b8b8", "#8a8a8a"],
             cam={"default_h_cm": 480, "min_h_cm": 240, "max_h_cm": 700}),
        room("ballet", "Ballett", "spc_tutu_rose", ["#fdf0f3", "#ffffff", "#f0b6c2"], [
            F("spc_barre_oak", 400, 5), W("spc_mirror_oak", 400, -225), F("furn_piano_black", 820, 5),
            F("spc_tutu_rose", 250, 62), F("spc_tutu_lilac", 300, 64), F("spc_ballet_shoes_rose", 560, 64),
            F("spc_ballet_shoes_white", 600, 66)], pattern="dots"),
    ]
    rooms.append(outdoor(A, "football", "Fußballplatz", "spc_football_white", 2400, [
        F("spc_pitch_green", 1300, 40), F("spc_goal_white", 520, 10), F("spc_goal_white", 2080, 10),
        F("spc_bleachers_sky", 1300, 0), F("spc_corner_flag_coral", 480, 70), F("spc_corner_flag_coral", 2120, 70),
        F("spc_football_white", 1300, 45), F("sport_cone_orange", 1000, 60), F("sport_cone_butter", 1100, 55)], "grass", GRASS, 41))
    rooms.append(outdoor(A, "tennis", "Tennis", "sport_racket_coral", 1500, [
        F("spc_court_terracotta", 750, 40), F("spc_tennis_net_white", 750, 30), F("sport_racket_coral", 450, 60),
        F("sport_racket_sky", 1050, 60), F("spc_tennis_ball_butter", 600, 55), F("street_park_bench_green", 1400, 20)],
        "sand", ["#e3b48c", "#d4a078", "#a87a58"], 42))
    return {"id": A, "name": "Sportzentrum", "name_key": "AREA_SPORT",
            "_doc": "P10e: 7 Räume. Erzeugt von tools/make_areas.py (tools/areas/sport.py) – dort ändern.",
            "spawn": {"room": "reception", "x_cm": 440, "y_cm": 55}, "default_items": [], "music": "music_sport", "rooms": rooms}


def npcs() -> dict:
    n = [("receptionist", "reception", 300, 2), ("coach", "fitness", 520, 50), ("coach", "hall", 700, 45),
         ("supervisor", "climbing", 700, 45), ("ballet_teacher", "ballet", 700, 40), ("coach", "football", 1300, 62)]
    return {"_doc": "Feste Figuren im Sportzentrum (P10e). Erzeugt von tools/make_areas.py.", "area": A,
            "npcs": [{"id": f"npc_{r}_{rid}", "role": r, "room": rid, "x_cm": x, "y_cm": y} for r, rid, x, y in n]}
