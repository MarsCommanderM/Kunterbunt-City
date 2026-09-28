"""
Katalog, Teil P10a (Schule & Pausenhof, Welt-Doku §4): Klassenzimmer, Musik, Kunst, NaWi, Turnhalle, Mensa,
Lehrerzimmer, Pausenhof. Dazu: Instrumente klingen beim Antippen (auch die schon vorhandenen).
"""
from __future__ import annotations

from . import schoolroom as SR
from .catalog import TEMPLATES, T, cols


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second if n != second else "cream", third)) for n in names]


for st, w, h, names, second, third, extra in (
        ("desk", 120, 72, ["oak", "cream", "mint", "sky"], "cream", "metal", {"surface_h": 72}),
        ("teacher_desk", 150, 76, ["oak", "walnut", "cream"], "sky", "metal", {"surface_h": 76}),
        ("locker", 105, 180, ["sky", "coral", "mint", "butter", "grey"], "navy", "metal",
         {"states": {"open": {"state": "open"}}, "state0": "closed"}),
        ("music_stand", 50, 120, ["black", "metal"], "cream", "black", {}),
        ("art_table", 140, 70, ["cream", "oak", "white"], "coral", "metal", {"surface_h": 70}),
        ("lab_table", 160, 90, ["white", "grey", "mint"], "sky", "metal", {"surface_h": 90}),
        ("skeleton", 45, 150, ["cream"], "cream", "metal", {}),
        ("vault_box", 90, 100, ["oak"], "coral", "oak", {"surface_h": 100}),
        ("balance_beam", 300, 60, ["oak", "sky"], "cream", "metal", {"seat": {"h": 60, "pose": "sit", "slots": 3}}),
        ("ball_cart", 100, 110, ["metal", "coral"], "coral", "metal", {}),
        ("serving_counter", 220, 95, ["white", "grey", "mint"], "orange", "metal", {"surface_h": 95}),
        ("copier", 80, 110, ["grey", "white"], "sky", "metal", {})):
    T(id=f"edu_{st}", fn=SR.school, w=w, h=h, kw={"style": st}, group="school", category="furniture", placement="floor",
      variants=V(names, second, third), **extra)
# Wand
T(id="edu_blackboard", fn=SR.school, w=240, h=120, kw={"style": "blackboard"}, group="school", category="item",
  placement="wall", states={"sun": {"state": "sun"}, "house": {"state": "house"}, "cat": {"state": "cat"},
                             "shapes": {"state": "shapes"}}, state0="empty", sfx={"sun": "chalk", "house": "chalk", "cat": "chalk",
                                                                                  "shapes": "chalk", "empty": "sponge"},
  variants=[("green", cols("#2f5a45", "white", "oak")), ("black", cols("#2e3140", "white", "oak"))])
T(id="edu_bell", fn=SR.school, w=30, h=34, kw={"style": "bell"}, group="school", category="item", placement="wall",
  states={"ring": {"state": "ring"}}, state0="quiet", sfx={"ring": "school_bell"}, anim={"ring": "shake"},
  variants=V(["butter", "coral"], "cream", "metal"))
T(id="edu_world_map", fn=SR.school, w=160, h=100, kw={"style": "world_map"}, group="school", category="item", placement="wall",
  variants=[("sea", cols("sky", "leaf_light", "oak"))])
T(id="edu_cubbies", fn=SR.school, w=100, h=80, kw={"style": "cubbies"}, group="school", category="item", placement="wall",
  variants=V(["oak", "white"], "cream", "metal"))
# Kleinkram (tragbar)
for st, w, h, names, second, third, extra in (
        ("triangle", 18, 22, ["metal"], "cream", "oak", {"sfx": {"tap": "triangle"}}),
        ("tambourine", 25, 25, ["oak", "coral"], "cream", "metal", {"sfx": {"tap": "tambourine"}}),
        ("palette", 30, 22, ["oak"], "sky", "oak", {}),
        ("clay_pot", 16, 18, ["terracotta", "sky", "butter"], "cream", "metal", {}),
        ("flask", 12, 18, ["mint", "rose", "sky"], "cream", "white", {"states": {"bubble": {"state": "bubble"}}, "state0": "still",
                                                                     "sfx": {"bubble": "pet_fish_bubble"}, "anim": {"bubble": "shake"}}),
        ("volcano", 36, 30, ["oak"], "orange", "grey", {"states": {"erupt": {"state": "erupt"}}, "state0": "calm",
                                                     "sfx": {"erupt": "fizz"}, "anim": {"erupt": "shake"}}),
        ("tray", 40, 3, ["coral", "sky", "mint", "grey"], "cream", "metal", {"tags": ["stackable"]})):
    T(id=f"edu_{st}", fn=SR.school, w=w, h=h, kw={"style": st}, group="school", category="school", placement="table",
      hold="one_hand" if h <= 50 else "two_hands", grip=[0.5, 0.5], variants=V(names, second, third), **extra)
T(id="edu_hopscotch", fn=SR.school, w=300, h=46, kw={"style": "hopscotch"}, group="school", category="item", placement="rug",
  variants=V(["coral", "sky", "butter"], "mint", "white"))

# ------------------------------------------------------------------ Instrumente klingen beim Antippen (alle, auch alte)
TAP = {"music_drums": "drum_hit", "toy_drum": "drum_hit", "music_keyboard": "piano_note", "furn_piano": "piano_note",
       "toy_xylophone": "xylophone", "toy_guitar": "guitar", "music_violin": "violin", "music_flute": "flute"}
for t in TEMPLATES:
    if t["id"] in TAP and not t.get("sfx"):
        t["sfx"] = {"tap": TAP[t["id"]]}
