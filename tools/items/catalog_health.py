"""
Katalog, Teil P10b (Gesundheitszentrum, Welt-Doku §5): Empfang, Praxen, Zahnarzt, Röntgen, Notaufnahme,
Babystation, Patientenzimmer, Apotheke, Dach mit Hubschrauber. Nie gruselig, kein Blut.
"""
from __future__ import annotations

from . import clinic as CL
from .catalog import T, cols


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second if n != second else "cream", third)) for n in names]


ON = {"states": {"on": {"state": "on"}}, "state0": "off"}
for st, w, h, names, second, third, extra in (
        ("reception", 220, 110, ["white", "sky", "mint"], "coral", "metal", {"surface_h": 88}),
        ("waiting_chairs", 180, 85, ["sky", "coral", "mint", "butter"], "cream", "metal", {"seat": {"h": 45, "pose": "sit", "slots": 3}}),
        ("exam_couch", 190, 90, ["mint", "sky", "coral"], "cream", "white", {"seat": {"h": 68, "pose": "lie", "slots": 1}}),
        ("dentist_chair", 160, 130, ["sky", "mint", "coral"], "butter", "white", {**ON, "seat": {"h": 55, "pose": "lie", "slots": 1},
                                                                                  "sfx": {"on": "ui_confirm"}}),
        ("xray", 110, 200, ["white", "grey"], "sky", "white", {"states": {"fish": {"state": "fish"}, "car": {"state": "car"},
                                                                          "ribs": {"state": "ribs"}}, "state0": "off",
                                                               "sfx": {"fish": "xray_beep", "car": "xray_beep", "ribs": "xray_beep"}}),
        ("gurney", 200, 95, ["sky", "mint", "white"], "white", "metal", {"seat": {"h": 85, "pose": "lie", "slots": 1}}),
        ("hospital_bed", 210, 110, ["sky", "mint", "rose", "butter"], "coral", "white", {"seat": {"h": 62, "pose": "lie", "slots": 1}}),
        ("iv_stand", 50, 180, ["sky", "mint"], "cream", "metal", {}),
        ("incubator", 90, 120, ["white", "sky"], "rose", "white", {"seat": {"h": 76, "pose": "lie", "slots": 1}}),
        ("medicine_shelf", 130, 200, ["white", "mint", "oak"], "coral", "metal", {}),
        ("ambulance", 480, 250, ["white"], "coral", "metal", {**ON, "sfx": {"on": "siren"}, "anim": {"on": "pulse"},
                                                           "seat": {"h": 60, "pose": "sit", "slots": 2}}),
        ("helicopter", 500, 250, ["coral", "butter", "white"], "white", "metal", {**ON, "sfx": {"on": "rotor"}, "anim": {"on": "shake"},
                                                                                  "seat": {"h": 90, "pose": "sit", "slots": 2}})):
    T(id=f"med_{st}", fn=CL.clinic, w=w, h=h, kw={"style": st}, group="health", category="furniture", placement="floor",
      variants=V(names, second, third), **extra)
T(id="med_eye_chart", fn=CL.clinic, w=60, h=90, kw={"style": "eye_chart"}, group="health", category="item", placement="wall",
  variants=V(["white"], "sky", "white"))
T(id="med_helipad", fn=CL.clinic, w=520, h=70, kw={"style": "helipad"}, group="health", category="item", placement="rug",
  variants=[("grey", cols("grey", "white", "white"))])
for st, w, h, names, second, third, extra in (
        ("heart_monitor", 40, 35, ["white", "grey"], "mint", "metal", {"states": {"beep": {"state": "beep"}}, "state0": "calm",
                                                                         "sfx": {"beep": "monitor_beep"}, "anim": {"beep": "pulse"}}),
        ("baby_scale", 55, 25, ["white", "sky"], "rose", "metal", {"seat": {"h": 22, "pose": "lie", "slots": 1}}),
        ("medicine", 8, 10, ["coral", "sky", "mint"], "coral", "white", {}),
        ("sling", 20, 30, ["sky", "white", "coral"], "cream", "white", {}),
        ("eye_patch", 8, 6, ["sand", "black"], "cream", "black", {}),
        ("crutches", 30, 120, ["metal", "sky"], "cream", "metal", {}),
        ("pet_carrier", 55, 40, ["sky", "coral", "grey"], "cream", "metal", {"container": {"slots": 1, "max_item_h_cm": 36}}),
        ("teeth_model", 20, 15, ["rose"], "cream", "white", {}),
        ("big_toothbrush", 8, 45, ["sky", "coral", "mint"], "white", "white", {})):
    T(id=f"med_{st}", fn=CL.clinic, w=w, h=h, kw={"style": st}, group="health", category="health" if h <= 50 else "item",
      placement="table" if h <= 60 else "floor", hold="one_hand" if h <= 150 and st != "baby_scale" else "none", grip=[0.5, 0.5],
      variants=V(names, second, third), **extra)
T(id="med_syrup", fn=CL.clinic, w=7, h=14, kw={"style": "medicine", "state": "syrup"}, group="health", category="health",
  placement="table", hold="one_hand", grip=[0.5, 0.4], variants=V(["coral", "plum", "orange"], "cream", "white"))
