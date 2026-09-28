"""
Katalog, Teil P10f (Eishalle, Welt-Doku §9): Eisfläche (Figuren gleiten), Eismaschine (alle 3 Min., Eis glänzt),
Bande, Eishockey-Tor, Lauflern-Pinguin, Discokugel (Disco-Licht), Verleih, Imbiss.
"""
from __future__ import annotations

from . import icerink as IR
from .catalog import T, cols


def V(names: list, second: str, third: str) -> list:
    return [(n, cols(n, second if second != n else "cream", third)) for n in names]


T(id="ice_surface", fn=IR.icerink, w=1800, h=70, kw={"style": "surface"}, group="winter", category="deco", placement="rug",
  states={"scratched": {"state": "scratched"}}, state0="shiny", variants=[("white", cols("#e6f4fb", "sky", "white"))])
for st, w, h, names, second, third, extra in (
        ("resurfacer", 320, 190, ["white", "sky"], "sky", "metal", {"seat": {"h": 120, "pose": "sit", "slots": 1}}),
        ("boards", 600, 110, ["white"], "coral", "white", {}),
        ("hockey_goal", 180, 120, ["coral"], "white", "white", {}),
        ("penguin", 60, 90, ["navy", "sky"], "orange", "white", {}),
        ("rental", 300, 200, ["sky", "oak"], "coral", "white", {"surface_h": 88})):
    T(id=f"ice_{st}", fn=IR.icerink, w=w, h=h, kw={"style": st}, group="winter", category="furniture", placement="floor",
      variants=V(names, second, third), **extra)
T(id="ice_disco_ball", fn=IR.icerink, w=50, h=90, kw={"style": "disco_ball"}, group="winter", category="item", placement="wall",
  states={"on": {"state": "on"}}, state0="off", sfx={"on": "tada"}, anim={"on": "wiggle"}, variants=V(["lilac"], "sky", "white"))
for st, w, h, names, second in (("cocoa", 9, 13, ["coral", "sky"], "butter"), ("pretzel", 14, 12, ["oak"], "oak"),
                                ("fries", 11, 15, ["coral"], "butter")):
    T(id=f"ice_{st}", fn=IR.icerink, w=w, h=h, kw={"style": st}, group="food", category="food", placement="table",
      hold="one_hand", grip=[0.5, 0.4], variants=V(names, second, "white"))
