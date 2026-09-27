"""P04b: Blick-Check-Bogen färbt wie der Shader; Pflanzen sind über getrennte Läufe bit-gleich."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from items.review_sheet import tint  # noqa: E402


def test_tint_matches_shader_formula(tmp_path):
    # Pixel 1: reine Zone 1 · Pixel 2: reine Zone 2 · Pixel 3: halb Zone 3, halb Tinte · Pixel 4: leer
    a = np.array([[[255, 0, 0, 255], [0, 255, 0, 255], [0, 0, 128, 200], [0, 0, 0, 0]]], np.uint8)
    p = tmp_path / "z.png"
    Image.fromarray(a, "RGBA").save(p)
    out = np.asarray(tint(p, ["#ff0000", "#00ff00", "#0000ff"])).astype(int)
    assert tuple(out[0, 0]) == (255, 0, 0, 255)
    assert tuple(out[0, 1]) == (0, 255, 0, 255)
    ink = np.array([0x3B, 0x2A, 0x2A]) * (1 - 128 / 255)
    assert np.allclose(out[0, 2, :3], ink + np.array([0, 0, 128]), atol=2)
    assert out[0, 2, 3] == 200 and out[0, 3, 3] == 0


def _plant_digest(seed: str) -> str:
    code = (
        "import sys, hashlib; sys.path.insert(0, 'tools');"
        "from items.kit import Item; from items.plants import plant;"
        "it = Item(40, 60); plant(it, 'ivy', 'round'); im, _ = it.finish();"
        "print(hashlib.sha1(im.tobytes()).hexdigest())"
    )
    env = {"PYTHONHASHSEED": seed, "PATH": "/usr/bin:/bin"}
    return subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True,
                          check=True).stdout.strip()


def test_plants_are_reproducible_across_runs():
    # hash() ist je Prozess gesalzen – die Pflanzen dürfen davon nicht abhängen
    assert _plant_digest("1") == _plant_digest("2")
