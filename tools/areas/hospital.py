"""Gesundheitszentrum (P10b, Welt-Doku §5): Empfang/Wartezimmer, Hausarzt, Zahnarzt, Kinderarzt, Tierarzt, Röntgen,
Notaufnahme, Babystation, Patientenzimmer, Cafeteria, Apotheke, Dach mit Hubschrauber. Nie gruselig, kein Blut."""
from __future__ import annotations

from .common import F, ON, W, deco, outdoor, shop

A = "hospital"
TILES = ["#f5f3ee", "#dfe6ea", "#a9b3bd"]


def room(rid: str, label: str, icon: str, wall: list, items: list, floor: str = "tiles", fcols: list | None = None,
         pattern: str = "", pcol: str = "#ffffff") -> dict:
    return shop(rid, label, icon, deco(wall, pattern, pcol, floor, fcols or TILES), items, area=A)


def praxis(rid: str, label: str, wall: list, extra: list) -> list:
    return [F("edu_teacher_desk_oak", 600, 10), ON("health_stethoscope_black", "edu_teacher_desk_oak", -0.2),
            ON("health_thermometer_sky", "edu_teacher_desk_oak", 0.2), F("furn_chair_office_grey", 640, 30),
            F("med_exam_couch_mint", 280, 20), W("med_eye_chart_white", 450, -190), F("health_first_aid_coral", 760, 60)] + extra


def area() -> dict:
    rooms = [
        room("reception", "Empfang", "med_reception_white", ["#eef6f3", "#ffffff", "#9fc3a0"], [
            F("med_reception_white", 280, 15), ON("shop_cash_register_cream", "med_reception_white", 0.3),
            F("med_waiting_chairs_sky", 560, 30), F("med_waiting_chairs_coral", 740, 50), F("toy_blocks_mint", 460, 64),
            F("toy_teddy_cream", 420, 62), F("plant_monstera_basket_oak", 120, 30), F("shop_magazine_rack_metal", 660, 64)]),
        room("gp", "Hausarzt", "health_stethoscope_black", ["#eef3f8", "#ffffff", "#a9c3dd"], praxis("gp", "Hausarzt",
             ["#eef3f8", "#ffffff", "#a9c3dd"], [F("health_bandage_cream", 360, 64), F("med_sling_sky", 420, 66)])),
        room("dentist", "Zahnarzt", "med_teeth_model_rose", ["#eaf7f6", "#ffffff", "#7cc6e0"], [
            F("med_dentist_chair_sky", 330, 25), F("med_heart_monitor_white", 520, 10), F("edu_lab_table_white", 600, 10),
            ON("med_teeth_model_rose", "edu_lab_table_white", -0.2), ON("med_big_toothbrush_sky", "edu_lab_table_white", 0.15),
            ON("bath_cup_sky", "edu_lab_table_white", 0.35), F("toy_plush_unicorn_white", 740, 64)]),
        room("pediatric", "Kinderarzt", "toy_teddy_rose", ["#fdf0f3", "#ffffff", "#f0b6c2"], praxis("pediatric", "Kinderarzt",
             ["#fdf0f3", "#ffffff", "#f0b6c2"], [F("med_baby_scale_white", 150, 45), F("toy_ball_pit_sky", 420, 55),
                                                   F("toy_teddy_rose", 360, 64)]), pattern="stars", pcol="#f8d4de"),
        room("vet", "Tierarzt", "med_pet_carrier_sky", ["#f1f6ea", "#ffffff", "#9fc3a0"], [
            F("edu_lab_table_white", 320, 20), F("med_pet_carrier_sky", 520, 60), F("pet_cat", 560, 50), F("pet_dog_small", 200, 55),
            F("petgear_bowl_mint", 640, 62), F("petgear_basket_oak", 740, 45), F("health_bandage_cream", 420, 64),
            F("shop_tank_shelf_black", 130, 0)], pattern="dots", pcol="#dfecd4"),
        room("xray", "Röntgen", "med_xray_white", ["#e8eaf2", "#ffffff", "#6f8fb8"], [
            F("med_xray_white", 400, 10), F("med_gurney_sky", 600, 40), F("toy_car_coral", 300, 64), F("food_apple_red", 250, 66)]),
        room("er", "Notaufnahme", "med_gurney_sky", ["#fdeeee", "#ffffff", "#e07a7a"], [
            F("med_gurney_mint", 280, 30), F("med_iv_stand_sky", 170, 20), F("med_heart_monitor_white", 420, 12),
            F("med_crutches_metal", 560, 30), F("health_wheelchair_sky", 680, 45), F("health_first_aid_coral", 760, 62),
            F("med_sling_coral", 420, 66), F("med_eye_patch_sand", 480, 66)]),
        room("babies", "Babystation", "med_incubator_white", ["#fff4f6", "#ffffff", "#f0b6c2"], [
            F("med_incubator_white", 250, 20), F("med_incubator_sky", 420, 20), F("med_baby_scale_sky", 620, 50),
            F("furn_crib_sky", 740, 10), F("furn_chair_rocking_cream", 120, 45), F("baby_bottle_sky", 540, 66),
            F("baby_rattle_rose", 580, 66), F("toy_plush_bunny_cream", 330, 64)], pattern="dots", pcol="#fbe0e6"),
        room("patient", "Patientenzimmer", "med_hospital_bed_sky", ["#eef3f8", "#ffffff", "#a9c3dd"], [
            F("med_hospital_bed_sky", 300, 15), F("med_iv_stand_mint", 170, 10), F("furn_nightstand_cream", 450, 10),
            F("med_heart_monitor_grey", 450, 12), F("med_hospital_bed_rose", 640, 45), F("flower_bouquet_rose", 540, 64),
            F("toy_teddy_brown", 720, 64)]),
        room("cafe", "Cafeteria", "kit_mug_coral", ["#fdf3e1", "#ffffff", "#f6d98a"], [
            F("shop_counter_glass_cream", 240, 15), ON("shop_coffee_machine_coral", "shop_counter_glass_cream", -0.2),
            ON("shop_cash_register_cream", "shop_counter_glass_cream", 0.3), F("furn_table_bistro_white", 520, 40),
            F("furn_chair_dining_cream", 460, 46), F("furn_chair_dining_cream", 580, 46), ON("food_cake_coral", "furn_table_bistro_white", 0),
            F("furn_table_bistro_sage", 720, 55)], floor="planks", fcols=["#e3c79a", "#d4b07c", "#8a6a4a"]),
        room("pharmacy", "Apotheke", "med_syrup_coral", ["#eef7ee", "#ffffff", "#5f8f6a"], [
            F("med_medicine_shelf_white", 180, 0), F("med_medicine_shelf_mint", 330, 0), F("shop_counter_oak", 560, 25),
            ON("shop_cash_register_cream", "shop_counter_oak", 0.3), ON("med_medicine_coral", "shop_counter_oak", -0.3),
            ON("med_syrup_plum", "shop_counter_oak", -0.1), F("med_medicine_sky", 450, 66), F("med_syrup_orange", 480, 66)],
             pattern="dots", pcol="#d9ecd9"),
    ]
    roof = [F("med_helipad_grey", 900, 40), F("med_helicopter_coral", 900, 38), F("med_ambulance_white", 1700, 30),
            F("street_street_lamp_black", 200, 2), F("street_park_bench_green", 1350, 20)]
    rooms.append(outdoor(A, "roof", "Dach", "med_helicopter_coral", 2100, roof, "concrete", ["#b8b8b8", "#a8a8a8", "#7a7a7a"], 14,
                         cam={"default_h_cm": 450, "min_h_cm": 240, "max_h_cm": 600}))
    return {"id": A, "name": "Gesundheitszentrum", "name_key": "AREA_HOSPITAL",
            "_doc": "P10b: 12 Räume. Erzeugt von tools/make_areas.py (tools/areas/hospital.py) – dort ändern.",
            "spawn": {"room": "reception", "x_cm": 430, "y_cm": 55}, "default_items": [], "music": "music_clinic", "rooms": rooms}


def npcs() -> dict:
    n = [("receptionist", "reception", 280, 2), ("doctor", "gp", 620, 5), ("dentist", "dentist", 460, 10), ("doctor", "pediatric", 620, 5),
         ("vet", "vet", 420, 5), ("nurse", "xray", 250, 30), ("nurse", "er", 360, 45), ("midwife", "babies", 340, 45),
         ("nurse", "patient", 540, 50), ("pharmacist", "pharmacy", 640, 5), ("cashier", "cafe", 320, 2), ("paramedic", "roof", 1500, 40)]
    return {"_doc": "Feste Figuren im Gesundheitszentrum (P10b). Erzeugt von tools/make_areas.py.", "area": A,
            "npcs": [{"id": f"npc_{r}_{rid}", "role": r, "room": rid, "x_cm": x, "y_cm": y} for r, rid, x, y in n]}
