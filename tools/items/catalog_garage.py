"""
Katalog, Teil P10h (Werkstatt, Welt-Doku §11): Hebebühne, Zapfsäule, Waschanlage, Lackierkabine + Sprühpistole,
Fahrrad-Montageständer, Schrottplatz mit Schatz. Mechanik: src/areas/workshop_actions.gd.
"""
from __future__ import annotations

from . import garage as GA
from .catalog import T, cols


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second if second != n else "cream", third)) for n in names]


for st, w, h, names, second, third, extra in (
        ("car_lift", 480, 220, ["coral", "sky"], "butter", "metal", {"states": {"up": {"state": "up"}}, "state0": "down",
                                                                     "sfx": {"up": "drop_metal"}}),
        ("gas_pump", 90, 190, ["coral", "sky", "green"], "white", "black", {"states": {"fuel": {"state": "fuel"}}, "state0": "idle",
                                                                            "sfx": {"fuel": "water_pour"}, "anim": {"fuel": "pulse"}}),
        ("wash_tunnel", 620, 330, ["sky", "butter"], "coral", "white", {"states": {"on": {"state": "on"}}, "state0": "off",
                                                                         "sfx": {"on": "water_pour"}, "anim": {"on": "shake"}}),
        ("paint_booth", 640, 300, ["grey", "white"], "sky", "white", {}),
        ("bike_stand", 90, 130, ["coral", "black"], "grey", "metal", {}),
        ("scrap_pile", 320, 190, ["rust", "grey"], "metal", "black", {"states": {"found": {"state": "found"}}, "state0": "junk",
                                                                      "sfx": {"found": "tada"}}),
        ("scrap_car", 380, 130, ["rust", "sky"], "grey", "terracotta", {"seat": {"h": 60, "pose": "sit", "slots": 2}}),
        ("oil_drum", 60, 90, ["blue", "coral", "green"], "white", "black", {})):
    T(id=f"garage_{st}", fn=GA.garage, w=w, h=h, kw={"style": st}, group="workshop", category="furniture", placement="floor",
      variants=V(names, second, third), **extra)
T(id="garage_spray_gun", fn=GA.garage, w=24, h=22, kw={"style": "spray_gun"}, group="workshop", category="item", placement="table",
  hold="one_hand", grip=[0.5, 0.3], variants=[(n, cols("metal", n, "grey")) for n in ["coral", "sky", "butter", "mint", "plum", "black"]])
T(id="garage_hubcap", fn=GA.garage, w=40, h=40, kw={"style": "hubcap"}, group="workshop", category="item", placement="table",
  hold="one_hand", grip=[0.5, 0.5], variants=V(["gold"], "butter", "metal"))
