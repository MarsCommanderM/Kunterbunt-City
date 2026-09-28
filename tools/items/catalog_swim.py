"""
Katalog, Teil P10c (Freizeitbad, Welt-Doku §6): Becken, Babybecken, Sprungturm, Wasserrutsche, Whirlpool,
Hochstuhl, Rettungsring, Duschen, Startblöcke, Schwimmbrett, Tauchringe, Wasserball, Kiosk, Spinde, Kabinen.
Figuren „schwimmen“, indem sie in einem Becken sitzen (Sitzplätze im Wasser, Bademeister zählt sie).
"""
from __future__ import annotations

from . import aquatic as AQ
from .catalog import T, cols

WATER = "#7cc6e0"
ON = {"states": {"on": {"state": "on"}}, "state0": "off"}
OPEN = {"states": {"open": {"state": "open"}}, "state0": "closed"}


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second, third)) for n in names]


for st, w, h, names, second, third, extra in (
        ("basin", 900, 80, ["sky", "white"], WATER, "white", {"seat": {"h": 40, "pose": "sit", "slots": 6}}),
        ("baby_pool", 320, 50, ["butter", "coral", "mint"], WATER, "white", {"seat": {"h": 22, "pose": "sit", "slots": 3}}),
        ("diving_tower", 260, 540, ["sky", "coral"], "coral", "white", {}),
        ("water_slide", 560, 420, ["butter", "coral", "mint"], WATER, "white", {}),
        ("whirlpool", 260, 90, ["sky", "white", "sand"], WATER, "white", {**ON, "seat": {"h": 50, "pose": "sit", "slots": 4},
                                                                           "sfx": {"on": "fizz"}, "anim": {"on": "pulse"}}),
        ("guard_chair", 90, 200, ["coral", "white"], "coral", "white", {"seat": {"h": 132, "pose": "sit", "slots": 1}}),
        ("shower", 60, 220, ["metal"], WATER, "metal", {**ON, "sfx": {"on": "water_pour"}}),
        ("kiosk", 260, 240, ["butter", "sky", "mint"], "coral", "white", {"surface_h": 105}),
        ("lockers", 120, 190, ["sky", "coral", "mint", "butter"], "butter", "metal", {**OPEN, "sfx": {"open": "open"}}),
        ("cabin", 110, 210, ["white"], "coral", "white", {**OPEN}),
        ("turnstile", 90, 100, ["metal"], "coral", "metal", {}),
        ("bench_tiled", 180, 45, ["white", "sky"], "sky", "white", {"seat": {"h": 45, "pose": "sit", "slots": 3}}),
        ("start_block", 55, 75, ["white"], "coral", "white", {})):
    T(id=f"swim_{st}", fn=AQ.aquatic, w=w, h=h, kw={"style": st}, group="pool", category="furniture", placement="floor",
      variants=V(names, second if second != names[0] else "cream", third), **extra)
T(id="swim_wave_sign", fn=AQ.aquatic, w=80, h=60, kw={"style": "wave_sign"}, group="pool", category="item", placement="wall",
  **ON, sfx={"on": "water_pour"}, variants=V(["navy"], WATER, "white"))
T(id="swim_lifebuoy", fn=AQ.aquatic, w=70, h=70, kw={"style": "lifebuoy"}, group="pool", category="toy", placement="floor",
  hold="one_hand", grip=[0.5, 0.95], variants=V(["coral", "orange"], "coral", "white"))
for st, w, h, names, second, hold in (
        ("kickboard", 30, 45, ["sky", "butter", "coral", "mint"], "white", "one_hand"),
        ("dive_rings", 30, 12, ["coral"], "butter", "one_hand"),
        ("beach_ball", 40, 40, ["coral", "sky", "butter"], "butter", "two_hands")):
    T(id=f"swim_{st}", fn=AQ.aquatic, w=w, h=h, kw={"style": st}, group="pool", category="toy", placement="table",
      hold=hold, grip=[0.5, 0.5], variants=V(names, second if second != names[0] else "sky", "white"))
