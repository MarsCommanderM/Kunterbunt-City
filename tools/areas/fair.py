"""Rummelplatz (P10d, Welt-Doku §7): Eingang, Riesenrad, Autoscooter, Karussell, Achterbahn, Geisterbahn (lustig),
Buden (Dosenwerfen, Entenangeln, Losrad, Hau den Lukas, Zuckerwatte) und Bühne (Zauberer, Clown).
Figur ins Fahrgeschäft setzen → Fahrt startet. Gewinne sind ✋ und können im Rucksack mit nach Hause."""
from __future__ import annotations

from .common import F, ON, outdoor

A = "fair"
PAVE = ["#d8cfc2", "#c9bfb0", "#9a8f80"]
SAND = ["#e8d7b0", "#dcc89c", "#b8a37a"]
TALL = {"default_h_cm": 480, "min_h_cm": 240, "max_h_cm": 700}


def r(rid: str, label: str, icon: str, width: float, items: list, seed: int, floor: str = "pavement", cols: list | None = None,
      height: float = 760.0) -> dict:
    return outdoor(A, rid, label, icon, width, items, floor, cols or PAVE, seed, height=height, cam=TALL)


def area() -> dict:
    rooms = [
        r("entrance", "Eingang", "fair_gate_coral", 1400, [
            F("fair_gate_coral", 700, 5), F("fair_ticket_booth_coral", 300, 10), F("fair_balloon_bunch_coral", 420, 30),
            F("fair_balloon_sky", 470, 55), F("fair_balloon_butter", 500, 58), F("fair_popcorn_coral", 1080, 64),
            F("street_park_bench_green", 1100, 20), F("street_street_lamp_black", 1300, 2)], 31),
        r("ferris", "Riesenrad", "fair_ferris_wheel_sky", 1200, [
            F("fair_ferris_wheel_sky", 600, 5), F("fair_ticket_booth_sky", 150, 10), F("street_park_bench_green", 1000, 25),
            F("fair_balloon_rose", 950, 60)], 32),
        r("bumper", "Autoscooter", "fair_bumper_car_coral", 1400, [
            F("fair_bumper_floor_navy", 700, 35), F("fair_bumper_car_coral", 400, 30), F("fair_bumper_car_sky", 650, 55),
            F("fair_bumper_car_butter", 900, 35), F("fair_bumper_car_mint", 1100, 60), F("fair_ticket_booth_coral", 120, 5)], 33,
          floor="concrete", cols=["#b8b8b8", "#a8a8a8", "#7a7a7a"]),
        r("carousel", "Karussell", "fair_carousel_horse_cream", 1200, [
            F("fair_carousel_coral", 560, 10), F("fair_carousel_horse_rose", 1000, 40), F("fair_candy_stand_rose", 150, 10),
            ON("fair_cotton_candy_rose", "fair_candy_stand_rose", 0.36)], 34),
        r("coaster", "Achterbahn", "fair_coaster_car_coral", 1600, [
            F("fair_coaster_track_coral", 750, 5), F("fair_coaster_car_coral", 285, 12), F("fair_ticket_booth_sky", 1450, 20),
            F("street_park_bench_green", 1450, 55)], 35),
        r("ghost", "Geisterbahn", "fair_ghost_house_lilac", 1200, [
            F("fair_ghost_house_lilac", 600, 5), F("fair_ghost_car_lilac", 330, 30), F("fair_ghost_car_mint", 1050, 50),
            F("fair_ticket_booth_coral", 1080, 5)], 36, floor="sand", cols=SAND),
        r("booths", "Buden", "fair_booth_coral", 1900, [
            F("fair_booth_coral", 250, 5), ON("fair_cans_coral", "fair_booth_coral", -0.25), ON("fair_cans_coral", "fair_booth_coral", 0.2),
            F("fair_duck_pond_sky", 620, 30), F("fair_booth_sky", 950, 5), ON("fair_lottery_coral", "fair_booth_sky", 0.0),
            F("fair_high_striker_coral", 1250, 10), F("fair_candy_stand_sky", 1500, 8), ON("fair_candy_apple_coral", "fair_candy_stand_sky", -0.2),
            ON("fair_cotton_candy_sky", "fair_candy_stand_sky", 0.2), F("fair_booth_butter", 1750, 5),
            ON("fair_prize_mint", "fair_booth_butter", 0.0), F("fair_target_coral", 1850, 40)], 37),
        r("stage", "Bühne", "fair_magic_hat_black", 1400, [
            F("fair_stage_plum", 600, 5), ON("fair_magic_hat_black", "fair_stage_plum", 0.15), ON("fair_juggling_coral", "fair_stage_plum", -0.2),
            F("street_park_bench_green", 450, 50), F("street_park_bench_green", 750, 55), F("fair_balloon_lilac", 1100, 58),
            F("fair_popcorn_coral", 1150, 64)], 38),
    ]
    return {"id": A, "name": "Rummelplatz", "name_key": "AREA_FAIR",
            "_doc": "P10d: 8 Räume. Erzeugt von tools/make_areas.py (tools/areas/fair.py) – dort ändern.",
            "spawn": {"room": "entrance", "x_cm": 560, "y_cm": 55}, "default_items": [], "music": "music_fair", "rooms": rooms}


def npcs() -> dict:
    n = [("ride_operator", "ferris", 260, 30), ("ride_operator", "bumper", 180, 30), ("ride_operator", "carousel", 900, 20),
         ("ride_operator", "coaster", 1380, 5), ("ride_operator", "ghost", 1000, 10), ("vendor", "booths", 950, 2),
         ("vendor", "carousel", 150, 2), ("clown", "entrance", 900, 50), ("magician", "stage", 960, 30)]
    return {"_doc": "Feste Figuren auf dem Rummelplatz (P10d). Erzeugt von tools/make_areas.py.", "area": A,
            "npcs": [{"id": f"npc_{r}_{rid}_{i}", "role": r, "room": rid, "x_cm": x, "y_cm": y} for i, (r, rid, x, y) in enumerate(n)]}
