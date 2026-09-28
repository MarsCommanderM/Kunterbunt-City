#!/usr/bin/env python3
"""
Fellmuster für Haustiere (P04b-T07): kachelbare Alpha-Masken für den Shader (`pattern_tex`).
Weiß + Alpha = wo das Muster liegt. Der Shader mischt es nur in Zone 1 (Fell) – Augen, Bauch, Halsband bleiben.

Aufruf: python3 tools/make_pet_patterns.py
"""
from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parents[1] / "assets/shaders/patterns"
N = 256
SS = 4


def _save(name: str, a: Image.Image) -> None:
    a = a.resize((N, N), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))
    img = Image.new("RGBA", (N, N), (255, 255, 255, 0))
    img.putalpha(a)
    img.save(OUT / f"{name}.png", optimize=True)


def _tile_blobs(rng: random.Random, n: int, rmin: float, rmax: float, irregular: bool) -> Image.Image:
    S = N * SS
    a = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(a)
    for _ in range(n):
        cx, cy = rng.uniform(0, S), rng.uniform(0, S)
        r = rng.uniform(rmin, rmax) * S
        pts = []
        for k in range(24):
            ang = 2 * math.pi * k / 24
            rr = r * (1 + (rng.uniform(-0.25, 0.25) if irregular else 0))
            pts.append((cx + rr * math.cos(ang), cy + rr * 0.85 * math.sin(ang)))
        for ox in (-S, 0, S):              # kachelbar: an allen Nachbarn wiederholen
            for oy in (-S, 0, S):
                d.polygon([(x + ox, y + oy) for x, y in pts], fill=255)
    return a


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(7)
    _save("patches", _tile_blobs(rng, 5, 0.12, 0.2, True))
    _save("spots", _tile_blobs(rng, 14, 0.035, 0.06, False))
    S = N * SS
    a = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(a)
    for k in range(3):                     # Tigerstreifen: wellige, spitz zulaufende Bänder
        x0 = S * (k + 0.5) / 3
        left, right = [], []
        for j in range(33):
            y = S * j / 32
            w = S * 0.05 * (0.35 + math.sin(math.pi * j / 32) ** 0.6)
            x = x0 + S * 0.04 * math.sin(2 * math.pi * j / 32 + k)
            left.append((x - w, y))
            right.append((x + w, y))
        d.polygon(left + right[::-1], fill=255)
    _save("stripes", a)
    t = np.zeros((N, N), np.float32)       # Spitzen: Pfoten unten + Ohren oben dunkler (nicht gekachelt)
    y = np.linspace(0, 1, N)[:, None]
    t += np.clip((y - 0.86) / 0.1, 0, 1)
    t += np.clip((0.14 - y) / 0.1, 0, 1)
    t = np.broadcast_to(np.clip(t, 0, 1), (N, N))
    _save("tips", Image.fromarray((t * 255).astype(np.uint8), "L"))
    print(f"✅ 4 Fellmuster → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
