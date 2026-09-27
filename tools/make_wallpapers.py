#!/usr/bin/env python3
"""
Tapeten-Muster (P07-T04): kachelbare Alpha-Masken für den Wand-Shader (`pattern_tex`, nur Zone 1 = Tapete).
Das Kind wählt Muster + zwei Farben – ohne ein einziges neues Hintergrundbild.

Aufruf: python3 tools/make_wallpapers.py
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parents[1] / "assets/shaders/wallpapers"
N = 256
SS = 4
S = N * SS


def _save(name: str, a: Image.Image) -> None:
    a = a.resize((N, N), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.4))
    img = Image.new("RGBA", (N, N), (255, 255, 255, 0))
    img.putalpha(a)
    img.save(OUT / f"{name}.png", optimize=True)


def _tiled(draw_fn) -> Image.Image:
    a = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(a)
    for ox in (-S, 0, S):
        for oy in (-S, 0, S):
            draw_fn(d, ox, oy)
    return a


def _flower(d, cx, cy, r):
    for k in range(5):
        ang = 2 * math.pi * k / 5
        px, py = cx + r * 0.62 * math.cos(ang), cy + r * 0.62 * math.sin(ang)
        d.ellipse([px - r * 0.45, py - r * 0.45, px + r * 0.45, py + r * 0.45], fill=255)
    d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28], fill=0)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    u = S / 4
    _save("stripes", _tiled(lambda d, ox, oy: [d.rectangle([ox + k * u, oy, ox + k * u + u * 0.42, oy + S], fill=255)
                                                for k in range(4)]))
    _save("pinstripes", _tiled(lambda d, ox, oy: [d.rectangle([ox + k * u / 2, oy, ox + k * u / 2 + u * 0.08, oy + S], fill=255)
                                                   for k in range(8)]))
    _save("dots", _tiled(lambda d, ox, oy: [d.ellipse([ox + (i + (0.5 if j % 2 else 0)) * u + u * 0.35, oy + j * u + u * 0.35,
                                                      ox + (i + (0.5 if j % 2 else 0)) * u + u * 0.65, oy + j * u + u * 0.65], fill=255)
                                            for i in range(-1, 5) for j in range(4)]))
    _save("checks", _tiled(lambda d, ox, oy: [d.rectangle([ox + i * u, oy + j * u, ox + (i + 1) * u, oy + (j + 1) * u], fill=255)
                                              for i in range(4) for j in range(4) if (i + j) % 2 == 0]))
    _save("flowers", _tiled(lambda d, ox, oy: [_flower(d, ox + (i + (0.5 if j % 2 else 0)) * S / 2 + S / 4,
                                                       oy + j * S / 2 + S / 4, S * 0.1) for i in range(-1, 3) for j in range(2)]))
    _save("stars", _tiled(lambda d, ox, oy: [d.polygon(
        [(ox + cx + (S * 0.07 if k % 2 == 0 else S * 0.03) * math.cos(-math.pi / 2 + k * math.pi / 5),
          oy + cy + (S * 0.07 if k % 2 == 0 else S * 0.03) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)], fill=255)
        for cx, cy in ((S * 0.25, S * 0.25), (S * 0.75, S * 0.75), (S * 0.75, S * 0.25 + S * 0.05), (S * 0.25, S * 0.75))]))

    def bricks(d, ox, oy):
        bh = S / 8
        bw = S / 4
        for j in range(8):
            off = bw / 2 if j % 2 else 0
            y = oy + j * bh
            d.rectangle([ox, y, ox + S, y + bh * 0.1], fill=255)
            for i in range(-1, 5):
                x = ox + i * bw + off
                d.rectangle([x, y, x + bw * 0.05, y + bh], fill=255)
    _save("bricks", _tiled(bricks))

    def tiles(d, ox, oy):
        t = S / 6
        for k in range(7):
            d.rectangle([ox + k * t, oy, ox + k * t + t * 0.06, oy + S], fill=255)
            d.rectangle([ox, oy + k * t, ox + S, oy + k * t + t * 0.06], fill=255)
    _save("tiles", _tiled(tiles))

    def waves(d, ox, oy):
        for j in range(4):
            pts = [(ox + x, oy + j * u + u * 0.5 + u * 0.18 * math.sin(2 * math.pi * x / (S / 2))) for x in range(0, S + 1, 8)]
            for w in range(-int(u * 0.09), int(u * 0.09)):
                d.line([(x, y + w) for x, y in pts], fill=255, width=2)
    _save("waves", _tiled(waves))
    print(f"✅ 9 Tapeten-Muster → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
