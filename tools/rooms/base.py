"""
Raum-Hintergründe im Stil C (P07): Vektor wie Items/Figuren, aber groß. Grundlagen.

Raum-Koordinaten (wie im Spiel, `Room`): x = 0 … Breite, y = 0 hintere Bodenlinie, nach oben negativ
(Wand bis −Wandhöhe), nach vorn positiv (Boden bis +front). Gezeichnet wird mit ZCanvas (y nach oben), darum
hier: y_up = −y_raum. Ausgabe 4 px/cm (wie die eingemessene Küche), intern 2× übersampelt (Speicher!).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import chibi.vec as vec  # noqa: E402

vec.SS = 2                       # große Flächen: 2× reicht (4 px/cm Ausgabe), sonst Gigabytes
PPC = 4.0
OUT = 0.5                        # Tinten-Kontur (cm) wie bei Items
INNER = 0.35
INK = np.array([0x3B, 0x2A, 0x2A], np.float32) / 255.0
WALL_H = 260.0                   # S-04: Raumhöhe
FRONT = 70.0                     # vordere Bodenlinie (cm vor der Wand)
BOTTOM = 110.0                   # so weit reicht der Boden nach vorn (Kamera-Rand + Luft)
TOP_EXTRA = 0.0


def hexcol(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


def canvas(x0: float, y0: float, x1: float, y1: float, outline: float = OUT) -> vec.ZCanvas:
    """Zeichenfläche für ein Element; Box in (x, y_up)-cm."""
    return vec.ZCanvas((x0, y0, x1, y1), PPC, outline_cm=outline)


def bake(c: vec.ZCanvas, cols: list[str], outline: bool = True) -> Image.Image:
    """Zonen → feste Farben (Shader-Formel), Tinte = dunkles Braun."""
    if outline:
        c.outline_under()
    a = np.asarray(c.render(), np.float32) / 255.0
    r, g, b, al = a[..., 0:1], a[..., 1:2], a[..., 2:3], a[..., 3:4]
    rest = np.clip(1.0 - r - g - b, 0.0, 1.0)
    z = [hexcol(x) for x in (cols + ["#ffffff"] * 3)[:3]]
    rgb = r * z[0] + g * z[1] + b * z[2] + rest * INK
    return Image.fromarray(np.clip(np.concatenate([rgb, al], -1) * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")


def raw(c: vec.ZCanvas, outline: bool = False) -> Image.Image:
    """Zonen-kodiert lassen (Spiel färbt per Shader ein – Tapete/Boden wählbar)."""
    if outline:
        c.outline_under()
    return c.render()


class Sheet:
    """Großes Bild eines Raums (px). paste() setzt Element-Bilder an ihre cm-Position."""

    def __init__(self, width_cm: float, top_cm: float = WALL_H, bottom_cm: float = BOTTOM):
        self.w_cm, self.top, self.bottom = width_cm, top_cm, bottom_cm
        self.img = Image.new("RGBA", (round(width_cm * PPC), round((top_cm + bottom_cm) * PPC)), (0, 0, 0, 0))

    def paste(self, im: Image.Image, x0_cm: float, y1_up_cm: float) -> None:
        """Bild mit linker Kante x0 und OBERKANTE y1 (y_up) einsetzen."""
        px = (round(x0_cm * PPC), round((self.top - y1_up_cm) * PPC))
        self.img.alpha_composite(im, (max(0, px[0]), max(0, px[1])),
                                 (max(0, -px[0]), max(0, -px[1])))

    def origin_px(self) -> list[float]:
        return [0.0, self.top * PPC]


def tiles(img: Image.Image, stem: Path, root: Path, max_px: int = 2048) -> list[dict]:
    """In Kacheln ≤ 2048 px schneiden (Web/Android-Limit) und speichern."""
    out = []
    for ty in range(0, img.height, max_px):
        for tx in range(0, img.width, max_px):
            part = img.crop((tx, ty, min(img.width, tx + max_px), min(img.height, ty + max_px)))
            if part.getchannel("A").getbbox() is None:
                continue
            f = stem.parent / f"{stem.name}_{ty // max_px}_{tx // max_px}.png"
            part.save(f, optimize=True)
            out.append({"file": "res://" + f.relative_to(root).as_posix(), "x_px": tx, "y_px": ty,
                        "w_px": part.width, "h_px": part.height})
    return out
