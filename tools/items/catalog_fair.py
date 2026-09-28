"""
Katalog, Teil P10d (Rummelplatz, Welt-Doku §7): Fahrgeschäfte (Figur hineinsetzen → Fahrt), Buden, Bühne,
Gewinne zum Mitnehmen. Fahrgeschäfte bewegen sich über PlayMotion (Daten: Präfix → Bewegungsart).
"""
from __future__ import annotations

from . import funfair as FF
from .catalog import T, cols


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second if second != n else "cream", third)) for n in names]


for st, w, h, names, second, third, extra in (
        ("ferris_wheel", 600, 640, ["sky", "coral"], "butter", "white", {"seat": {"h": 40, "pose": "sit", "slots": 2}}),
        ("carousel", 620, 460, ["coral", "sky", "mint"], "butter", "white", {"seat": {"h": 150, "pose": "sit", "slots": 3}}),
        ("bumper_car", 160, 100, ["coral", "sky", "butter", "mint", "lilac"], "butter", "metal",
         {"seat": {"h": 40, "pose": "sit", "slots": 1}}),
        ("coaster_track", 1100, 340, ["coral", "sky"], "butter", "metal", {}),
        ("coaster_car", 170, 100, ["coral", "butter"], "sky", "metal", {"seat": {"h": 45, "pose": "sit", "slots": 2}}),
        ("ghost_house", 720, 440, ["lilac", "navy"], "plum", "white", {"states": {"boo": {"state": "boo"}}, "state0": "calm",
                                                                      "sfx": {"boo": "boo"}, "anim": {"boo": "wiggle"}}),
        ("ghost_car", 150, 95, ["lilac", "mint"], "plum", "white", {"seat": {"h": 42, "pose": "sit", "slots": 1}}),
        ("booth", 320, 260, ["coral", "sky", "butter", "mint"], "butter", "white", {"surface_h": 98}),
        ("duck_pond", 220, 70, ["sky", "coral"], "butter", "white", {}),
        ("high_striker", 90, 460, ["coral"], "butter", "white", {"states": {"ring": {"state": "ring"}}, "state0": "off",
                                                                 "sfx": {"ring": "fair_bell"}, "anim": {"ring": "bounce"}}),
        ("stage", 640, 320, ["plum", "coral"], "coral", "white", {"states": {"open": {"state": "open"}}, "state0": "closed",
                                                                  "surface_h": 108, "sfx": {"open": "tada"}}),
        ("candy_stand", 200, 230, ["rose", "sky"], "rose", "white", {"surface_h": 104}),
        ("gate", 560, 480, ["coral", "sky"], "butter", "white", {})):
    T(id=f"fair_{st}", fn=FF.funfair, w=w, h=h, kw={"style": st}, group="fair", category="furniture", placement="floor",
      variants=V(names, second, third), **extra)
T(id="fair_bumper_floor", fn=FF.funfair, w=900, h=60, kw={"style": "bumper_floor"}, group="fair", category="deco",
  placement="rug", variants=V(["navy"], "coral", "grey"))
for st, w, h, names, second, third, hold, extra in (
        ("cans", 30, 36, ["coral"], "sky", "metal", "one_hand", {"states": {"fallen": {"state": "fallen"}}, "state0": "standing",
                                                                   "sfx": {"fallen": "drop_metal"}}),
        ("lottery", 50, 54, ["coral", "sky"], "butter", "metal", "none", {"states": {"spin": {"state": "spin"}}, "state0": "still",
                                                                          "sfx": {"spin": "dice_roll"}, "anim": {"spin": "shake"}}),
        ("magic_hat", 30, 28, ["black"], "coral", "white", "one_hand", {"states": {"rabbit": {"state": "rabbit"}}, "state0": "empty",
                                                                        "sfx": {"rabbit": "tada"}, "anim": {"rabbit": "bounce"}}),
        ("juggling", 24, 8, ["coral"], "butter", "sky", "one_hand", {}),
        ("prize", 42, 54, ["rose", "sky", "butter", "mint", "lilac"], "coral", "black", "two_hands", {}),
        ("candy_apple", 9, 20, ["coral"], "coral", "oak", "one_hand", {})):
    T(id=f"fair_{st}", fn=FF.funfair, w=w, h=h, kw={"style": st}, group="fair", category="toy" if st != "candy_apple" else "food",
      placement="table", hold=hold, grip=[0.5, 0.5] if hold != "none" else None, variants=V(names, second, third), **extra)
T(id="fair_balloon", fn=FF.funfair, w=34, h=110, kw={"style": "balloon"}, group="fair", category="toy", placement="floor",
  hold="one_hand", grip=[0.5, 0.02], variants=V(["coral", "sky", "butter", "mint", "lilac", "rose"], "coral", "white"))
