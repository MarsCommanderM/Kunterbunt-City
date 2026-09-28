"""
Katalog, Teil P10e (Sportzentrum, Welt-Doku §8): Fitness, Sporthalle, Fußballplatz mit Tribüne, Tennis, Kletterwand,
Ballett. Ball-Physik mit Tor-Erkennung: src/areas/sport_actions.gd.
"""
from __future__ import annotations

from . import sportcenter as SP
from .catalog import T, cols

ON = {"states": {"on": {"state": "on"}}, "state0": "off"}
SCORE = {"states": {f"s{k}": {"state": f"s{k}"} for k in range(1, 6)}, "state0": "s0"}


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second if second != n else "cream", third)) for n in names]


for st, w, h, names, second, third, extra in (
        ("treadmill", 180, 140, ["black", "grey"], "sky", "metal", {**ON, "anim": {"on": "shake"}, "sfx": {"on": "ui_confirm"}}),
        ("bike", 110, 120, ["coral", "black", "sky"], "grey", "metal", {"seat": {"h": 90, "pose": "sit", "slots": 1}}),
        ("bench", 150, 55, ["black", "coral"], "grey", "metal", {"seat": {"h": 42, "pose": "lie", "slots": 1}}),
        ("yoga_ball", 65, 65, ["coral", "sky", "mint", "lilac"], "white", "white", {"seat": {"h": 62, "pose": "sit", "slots": 1}}),
        ("bleachers", 640, 150, ["sky", "coral"], "butter", "cream", {"seat": {"h": 150, "pose": "sit", "slots": 6}}),
        ("climbing_wall", 420, 640, ["sand", "grey"], "coral", "sky", {"seat": {"h": 300, "pose": "sit", "slots": 3}}),
        ("barre", 320, 110, ["oak"], "oak", "metal", {}),
        ("tennis_net", 640, 107, ["white"], "white", "grey", {}),
        ("goal", 500, 200, ["white"], "white", "white", {}),
        ("corner_flag", 30, 150, ["coral", "butter"], "coral", "white", {})):
    T(id=f"spc_{st}", fn=SP.sportcenter, w=w, h=h, kw={"style": st}, group="sport", category="furniture", placement="floor",
      variants=V(names, second, third), **extra)
T(id="spc_scoreboard", fn=SP.sportcenter, w=200, h=100, kw={"style": "scoreboard"}, group="sport", category="item",
  placement="wall", **SCORE, sfx={f"s{k}": "fair_bell" for k in range(1, 6)}, variants=V(["navy"], "butter", "white"))
T(id="spc_mirror", fn=SP.sportcenter, w=320, h=180, kw={"style": "mirror"}, group="sport", category="item", placement="wall",
  variants=V(["oak", "white"], "oak", "white"))
for st, w, h, names in (("pitch", 1600, 60, ["green"]), ("court", 1100, 60, ["terracotta", "blue"])):
    T(id=f"spc_{st}", fn=SP.sportcenter, w=w, h=h, kw={"style": st}, group="sport", category="deco", placement="rug",
      variants=V(names, "white", "white"))
for st, w, h, names, second, hold, cat in (
        ("football", 22, 22, ["white"], "black", "one_hand", "toy"),
        ("tennis_ball", 7, 7, ["butter"], "white", "one_hand", "toy"),
        ("tutu", 40, 16, ["rose", "lilac", "sky", "white"], "rose", "one_hand", "item"),
        ("ballet_shoes", 18, 10, ["rose", "white"], "rose", "one_hand", "item")):
    T(id=f"spc_{st}", fn=SP.sportcenter, w=w, h=h, kw={"style": st}, group="sport", category=cat, placement="table",
      hold=hold, grip=[0.5, 0.5], variants=V(names, second, "white"))
