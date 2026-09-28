"""Werkstatt (P10h, Welt-Doku §11): Autowerkstatt mit Hebebühne, Waschanlage, Tankstelle mit Shop, Lackiererei,
Fahrradwerkstatt, Schrottplatz (Geheimnisse). Hupen, Reifenwechsel, Lackieren, Waschen, Tanken."""
from __future__ import annotations

from .common import F, ON, W, deco, outdoor, shop

A = "workshop"
CONCRETE = ["#c8c8c8", "#b8b8b8", "#8a8a8a"]
ASPHALT = ["#8a8f96", "#7a7f86", "#5a5f66"]


def room(rid: str, label: str, icon: str, wall: list, items: list, width: float = 1200, height: float = 260.0,
         fcols: list | None = None) -> dict:
    cam = {"default_h_cm": 380, "min_h_cm": 220, "max_h_cm": min(600.0, height)} if height > 260 else None
    return shop(rid, label, icon, deco(wall, "", "#ffffff", "concrete", fcols or CONCRETE), items, width=width, area=A,
                height=height, cam=cam)


def area() -> dict:
    rooms = [
        room("garage", "Autowerkstatt", "garage_car_lift_coral", ["#eef0f4", "#ffffff", "#e07a7a"], [
            F("garage_car_lift_coral", 500, 5), F("veh_car_hatch_sky", 500, 10), F("work_tool_wall_grey", 1000, 0),
            F("work_tool_cart_coral", 850, 40), F("work_tire_summer_black", 780, 62), F("work_tire_summer_black", 830, 64),
            F("work_car_jack_coral", 250, 60), F("work_toolbox_coral", 1100, 62), F("garage_oil_drum_blue", 120, 20)],
             width=1300, height=400),
        outdoor(A, "wash", "Waschanlage", "garage_wash_tunnel_sky", 1500, [
            F("garage_wash_tunnel_sky", 700, 10), F("veh_car_beetle_mint", 1250, 45), F("work_car_wash_sky", 300, 60),
            F("work_cone_traffic_orange", 200, 64)], "pavement", ASPHALT, 61, height=600),
        outdoor(A, "fuel", "Tankstelle", "garage_gas_pump_coral", 1600, [
            F("garage_gas_pump_coral", 500, 20), F("garage_gas_pump_sky", 750, 20), F("veh_car_sedan_navy", 500, 45),
            F("swim_kiosk_sky", 1250, 10), ON("shop_cash_register_cream", "swim_kiosk_sky", 0.3), ON("food_banana_butter", "swim_kiosk_sky", -0.3),
            F("work_jerrycan_coral", 900, 62), F("street_street_lamp_black", 100, 2)], "pavement", ASPHALT, 62, height=600),
        room("paint", "Lackiererei", "garage_spray_gun_coral", ["#f4f4f8", "#ffffff", "#a9c3dd"], [
            F("garage_paint_booth_white", 550, 0), F("veh_car_pickup_white", 550, 20), F("garage_spray_gun_coral", 950, 62),
            F("garage_spray_gun_sky", 1000, 64), F("garage_spray_gun_butter", 1050, 62), F("work_paint_can_mint", 1120, 64)],
             width=1200, height=360),
        room("bikes", "Fahrradwerkstatt", "garage_bike_stand_coral", ["#f3f8ee", "#ffffff", "#7fae6a"], [
            F("garage_bike_stand_coral", 350, 20), F("work_bike_pump_coral", 520, 62), F("work_tool_wall_oak", 800, 0),
            F("work_workbench_oak", 1000, 10), ON("work_wrench_metal", "work_workbench_oak", -0.2), F("work_tire_steel_silver", 650, 64)],
             width=1150),
        outdoor(A, "scrapyard", "garage_scrap_pile_rust", 1800, [
            F("garage_scrap_pile_rust", 500, 5), F("garage_scrap_car_rust", 950, 20), F("garage_scrap_pile_grey", 1450, 10),
            F("work_tire_stack_black", 1200, 50), F("garage_oil_drum_coral", 250, 50), F("work_tire_winter_black", 700, 64)],
            "sand", ["#c8b89a", "#b8a88a", "#8a7a5a"], 63, height=600),
    ]
    return {"id": A, "name": "Werkstatt", "name_key": "AREA_WORKSHOP",
            "_doc": "P10h: 6 Räume. Erzeugt von tools/make_areas.py (tools/areas/workshop.py) – dort ändern.",
            "spawn": {"room": "garage", "x_cm": 900, "y_cm": 55}, "default_items": [], "music": "music_workshop", "rooms": rooms}


def npcs() -> dict:
    n = [("mechanic", "garage", 750, 30), ("mechanic", "bikes", 500, 40), ("cashier", "fuel", 1250, 2), ("vendor", "wash", 250, 30),
         ("mechanic", "paint", 900, 45)]
    return {"_doc": "Feste Figuren in der Werkstatt (P10h). Erzeugt von tools/make_areas.py.", "area": A,
            "npcs": [{"id": f"npc_{r}_{rid}", "role": r, "room": rid, "x_cm": x, "y_cm": y} for r, rid, x, y in n]}
