"""Schule & Pausenhof (P10a, Welt-Doku §4): Eingangshalle mit Spinden, 2 Klassenzimmer, Musik, Kunst, NaWi,
Turnhalle, Mensa, Lehrerzimmer, Pausenhof. Schulglocke startet die Pause (Kinder jubeln), Tafel mit Kreide-Bildern."""
from __future__ import annotations

from .common import DOOR_TOP, F, ON, W, deco, outdoor, shop

A = "school"


def room(rid: str, label: str, icon: str, decor: dict, items: list, **kw) -> dict:
    return shop(rid, label, icon, decor, items, area=A, **kw)


def classroom(rid: str, label: str, wall: list, desk: str) -> dict:
    items = [W("edu_blackboard_green", 400, -230), W("edu_world_map_sea", 690, -200), W("deco_clock_cream", 180, -215),
             F("edu_teacher_desk_oak", 240, 10), ON("school_pencil_cup_sky", "edu_teacher_desk_oak", 0.3),
             F("furn_bookshelf_oak", 720, 2)]
    for k, x in enumerate((300, 480, 660)):
        items += [F(desk, x, 45), F("furn_chair_kids_sky" if k % 2 else "furn_chair_kids_coral", x - 25, 52),
                  F("furn_chair_kids_mint", x + 25, 52), ON("school_school_bag_coral" if k % 2 else "school_school_bag_sky", desk, 0.2)]
    items += [F("deco_globe_sky", 130, 60)]
    return room(rid, label, "edu_blackboard_green", deco(wall, "", "#ffffff", "planks", ["#e8c49a", "#d9ae7e", "#8a5a3c"]), items)


def area() -> dict:
    tiles = ["#f5f3ee", "#dfe6ea", "#a9b3bd"]
    rooms = [
        room("hall", "Eingangshalle", "edu_locker_sky", deco(["#eef3f8", "#ffffff", "#a9c3dd"], "", "#ffffff", "tiles", tiles), [
            F("edu_locker_sky", 220, 0), F("edu_locker_coral", 340, 0), F("edu_locker_mint", 460, 0), W("edu_bell_butter", 600, -240),
            F("street_park_bench_oak", 640, 40), F("plant_monstera_basket_oak", 760, 30), F("furn_coat_rack_sage", 140, 30),
            F("school_school_bag_plum", 520, 64), W("door_double_white", 720, -217.0)]),
        classroom("class1", "Klasse 1", ["#fdf3e1", "#ffffff", "#f6d98a"], "edu_desk_oak"),
        classroom("class2", "Klasse 2", ["#eaf4ee", "#ffffff", "#9fc3a0"], "edu_desk_mint"),
        room("music", "Musikraum", "music_drums_coral", deco(["#f1ecfa", "#ffffff", "#b9a6d6"], "stars", "#e2d9f3", "planks",
                                                             ["#d9a066", "#c98a4b", "#8a5a3c"]), [
            F("furn_piano_walnut", 230, 0), F("music_drums_coral", 440, 20), F("edu_music_stand_black", 560, 30),
            F("music_keyboard_black", 680, 20), F("toy_xylophone_coral", 330, 62), F("edu_triangle_metal", 420, 66),
            F("edu_tambourine_oak", 480, 64), F("toy_guitar_oak", 600, 62), F("music_violin_oak", 720, 64), F("music_flute_sky", 380, 68)]),
        room("art", "Kunstraum", "school_easel_cream", deco(["#fff4e8", "#ffffff", "#f09a55"], "dots", "#fbe0c6", "concrete",
                                                             ["#c9c0b0", "#b8ae9c", "#8a8070"]), [
            F("school_easel_cream", 200, 20), F("school_easel_cream", 320, 25), F("edu_art_table_cream", 540, 40),
            ON("edu_palette_oak", "edu_art_table_cream", -0.3), ON("edu_clay_pot_terracotta", "edu_art_table_cream", 0.0),
            ON("toy_paints_coral", "edu_art_table_cream", 0.3), F("furn_chair_kids_coral", 490, 55), F("furn_chair_kids_sky", 590, 55),
            F("toy_crayons_coral", 700, 64), W("poster_rainbow_sky", 420, -200)]),
        room("science", "NaWi-Raum", "edu_volcano_oak", deco(["#e9f4f5", "#ffffff", "#7cc6e0"], "", "#ffffff", "tiles", tiles), [
            F("edu_lab_table_white", 300, 30), ON("edu_volcano_oak", "edu_lab_table_white", -0.25),
            ON("edu_flask_mint", "edu_lab_table_white", 0.1), ON("school_microscope_cream", "edu_lab_table_white", 0.3),
            F("edu_skeleton_cream", 560, 10), F("edu_lab_table_grey", 640, 50), ON("edu_flask_rose", "edu_lab_table_grey", -0.2),
            ON("edu_flask_sky", "edu_lab_table_grey", 0.1), F("plant_cactus_ball_bowl_cream_rose", 150, 60), W("edu_world_map_sea", 430, -220)]),
        room("gym", "Turnhalle", "edu_vault_box_oak", deco(["#fbf3e3", "#ffffff", "#f4c95d"], "", "#ffffff", "planks",
                                                            ["#e3c79a", "#d4b07c", "#8a6a4a"]), [
            F("edu_vault_box_oak", 220, 20), F("edu_balance_beam_oak", 450, 45), F("sport_mat_sky", 660, 40),
            F("edu_ball_cart_metal", 760, 15), F("sport_basket_hoop_coral", 120, 5), F("toy_ball_coral", 330, 64),
            F("sport_cone_orange", 560, 66), F("sport_jump_rope_coral", 620, 68), F("sport_hoop_teal", 700, 64)], width=900),
        room("cafeteria", "Mensa", "edu_tray_coral", deco(["#fdf0e6", "#ffffff", "#e07a7a"], "pinstripes", "#f6ddd0", "tiles",
                                                           ["#f6d98a", "#f5f3ee", "#b89a55"]), [
            F("edu_serving_counter_white", 240, 10), ON("edu_tray_coral", "edu_serving_counter_white", -0.35),
            ON("edu_tray_sky", "edu_serving_counter_white", -0.2), ON("food_spaghetti_tomato", "edu_serving_counter_white", 0.05),
            ON("food_apple_green", "edu_serving_counter_white", 0.3), F("furn_table_dining_oak", 560, 40),
            F("furn_chair_kids_coral", 480, 48), F("furn_chair_kids_mint", 640, 48), ON("food_milk_carton", "furn_table_dining_oak", -0.2),
            ON("kit_plate_kids_sky", "furn_table_dining_oak", 0.15), F("kit_trash_mint", 760, 30)]),
        room("staff", "Lehrerzimmer", "edu_copier_grey", deco(["#f3efe8", "#ffffff", "#a1887f"], "", "#ffffff", "carpet",
                                                             ["#d8cfc2", "#cabfb0", "#a1887f"]), [
            F("furn_table_dining_walnut", 360, 30), F("furn_chair_dining_walnut", 290, 38), F("furn_chair_dining_walnut", 430, 38),
            ON("kit_mug_navy", "furn_table_dining_walnut", -0.2), ON("kit_coffee_black", "furn_table_dining_walnut", 0.25),
            F("edu_copier_grey", 600, 5), W("edu_cubbies_oak", 180, -200), F("furn_bookshelf_walnut", 740, 2),
            F("plant_ficus_basket_oak", 120, 30)]),
    ]
    yard = [F("play_climber_coral", 380, 8), F("sport_table_tennis_green", 900, 40), F("edu_hopscotch_coral", 1250, 45),
            F("garden_raised_bed_m_carrot_oak", 1600, 20), F("garden_raised_bed_m_tomato_oak", 1760, 22),
            F("garden_watering_can_sky", 1680, 62), F("street_park_bench_green", 1450, 20), F("street_bin_street_green", 1350, 30),
            F("street_bike_stand_metal", 2100, 20), F("sport_goal_small_white", 700, 30), F("toy_ball_sky", 780, 60),
            F("sport_jump_rope_butter", 1150, 66), F("camp_tree_leaf", 120, 2), F("camp_tree_leaf_light", 2300, 4)]
    rooms.append(outdoor(A, "yard", "Pausenhof", "edu_hopscotch_coral", 2400, yard, "pavement", ["#d8cfc2", "#c9bfb0", "#9a8f80"], 12))
    return {"id": A, "name": "Schule & Pausenhof", "name_key": "AREA_SCHOOL",
            "_doc": "P10a: Halle mit Spinden, 2 Klassen, Musik, Kunst, NaWi, Turnhalle, Mensa, Lehrerzimmer, Pausenhof. "
                    "Erzeugt von tools/make_areas.py (tools/areas/school.py) – dort ändern.",
            "spawn": {"room": "hall", "x_cm": 400, "y_cm": 45}, "default_items": [], "music": "music_school", "rooms": rooms}


def npcs() -> dict:
    n = [{"id": "npc_teacher1", "role": "teacher", "room": "class1", "x_cm": 330, "y_cm": 8},
         {"id": "npc_teacher2", "role": "teacher", "room": "class2", "x_cm": 330, "y_cm": 8},
         {"id": "npc_musicteacher", "role": "music_teacher", "room": "music", "x_cm": 150, "y_cm": 30},
         {"id": "npc_artteacher", "role": "art_teacher", "room": "art", "x_cm": 420, "y_cm": 15},
         {"id": "npc_janitor", "role": "janitor", "room": "hall", "x_cm": 560, "y_cm": 50},
         {"id": "npc_cook", "role": "cook", "room": "cafeteria", "x_cm": 240, "y_cm": 2},
         {"id": "npc_principal", "role": "principal", "room": "staff", "x_cm": 520, "y_cm": 30},
         {"id": "npc_yardwatch", "role": "supervisor", "room": "yard", "x_cm": 1300, "y_cm": 40}]
    for i, (rid, x) in enumerate((("yard", 500), ("yard", 950), ("yard", 1300), ("yard", 1900), ("class1", 400), ("class1", 580),
                                  ("class2", 420), ("gym", 380))):
        n.append({"id": f"npc_pupil{i + 1}", "role": "pupil" if i % 2 else "pupil2", "room": rid, "x_cm": x, "y_cm": 55 + (i % 3) * 4})
    return {"_doc": "Feste Figuren der Schule (P10a): 7 Erwachsene + 8 Schulkinder. Erzeugt von tools/make_areas.py.",
            "area": A, "npcs": n}
