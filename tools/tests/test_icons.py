"""P04b-T08: Symbole im Stil C – vollständig, farbig (nicht mehr einfarbig), mit Tinten-Kontur, reproduzierbar."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from make_icons import ICONS, render  # noqa: E402

ICON_DIR = ROOT / "assets/ui/icons"


def _referenced() -> set[str]:
    names: set[str] = set()
    sp = json.loads((ROOT / "data/pets/species.json").read_text())
    names |= {s["icon"] for s in sp["species"]}
    names |= {t["icon"] for t in sp.get("traits", []) if isinstance(t, dict) and "icon" in t}
    names |= {a["icon"] for a in json.loads((ROOT / "data/areas/index.json").read_text())["areas"]}
    for f in (ROOT / "src").rglob("*.gd"):
        s = f.read_text()
        names |= set(re.findall(r'Ui\.(?:button|icon)\("[^"]*",\s*"([a-z_0-9]+)"', s))
        names |= set(re.findall(r'Ui\.(?:icon|tex)\("([a-z_0-9]+)"', s))
    return names


def test_every_referenced_icon_exists():
    missing = sorted(n for n in _referenced() if not (ICON_DIR / f"{n}.png").exists())
    assert missing == [], f"fehlende Symbole: {missing}"


def test_icons_are_colourful_with_ink_outline():
    for name in ICONS:
        a = np.asarray(Image.open(ICON_DIR / f"{name}.png").convert("RGBA"), np.float32)
        assert a.shape[:2] == (256, 256), name
        solid = a[a[..., 3] > 240][:, :3]
        assert len(solid) > 2000, f"{name}: fast leer"
        # Tinte: dunkles Braun am Rand (Stil C, nie Schwarz)
        dark = solid[(solid.sum(axis=1) < 200)]
        assert len(dark) > 150, f"{name}: keine Kontur"
        assert (dark[:, 0] >= dark[:, 2] - 8).mean() > 0.8, f"{name}: Kontur nicht braun"
        # farbig: mind. 2 deutlich verschiedene Füllfarben (nicht das alte einfarbige Violett)
        fill = solid[solid.sum(axis=1) > 300]
        q = np.unique((fill // 48).astype(int), axis=0)
        assert len(q) >= 2, f"{name}: einfarbig"


def test_icon_rendering_is_reproducible():
    n, img = render("area_zoo")
    ref = Image.open(ICON_DIR / "area_zoo.png").convert("RGBA")
    assert np.array_equal(np.asarray(img), np.asarray(ref)), "Symbole müssen bit-gleich neu entstehen"
