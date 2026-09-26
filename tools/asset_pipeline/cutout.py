#!/usr/bin/env python3
"""P06-T01 – Freistellen: KI-Blatt (weißer Hintergrund) → RGBA mit sauberen Kanten.

Übernommen und gehärtet aus reference/pipeline_demo_kueche.py:

* Hintergrund = weiße Flächen, per Flood-Fill vom Bildrand her (Labeling).
* Eingeschlossene weiße Löcher > hole_min px UND Mittelwert > 250 → transparent
  (z. B. Tassenhenkel). Modus ``remove_holes=False`` (Figuren/Tiere): Löcher
  bleiben erhalten, damit das Augenweiß nicht verschwindet.
* Kanten-Entmischung gegen den weißen Saum (Alpha-Division).

Nur Gratis-Abhängigkeiten: pillow, numpy, scipy.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

# Weiß-Erkennung (wie Demo): fast neutral und hell.
_WHITE_MN = 232
_WHITE_RANGE = 20
# Loch-Regel: eingeschlossene Fläche in Pixeln / Mindest-Helligkeit.
HOLE_MIN = 500
HOLE_MEAN = 250


def cutout(src, *, remove_holes: bool = True, hole_min: int = HOLE_MIN):
    """Blatt freistellen.

    ``src``: Pfad oder PIL-Bild.
    Gibt ``(rgba, fg)`` zurück: rgba = uint8-RGBA-Array (H×W×4),
    fg = bool-Maske des Vordergrunds (nach Öffnen, vor Weichzeichner).
    """
    if isinstance(src, Image.Image):
        im = np.asarray(src.convert("RGB")).astype(np.float32)
    else:
        im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)

    mn, mx = im.min(2), im.max(2)
    white = (mn > _WHITE_MN) & ((mx - mn) < _WHITE_RANGE)
    lab, n = ndi.label(white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border)) if border else np.zeros(white.shape, dtype=bool)

    # Eingeschlossene, rein weiße Löcher (Henkel, Handtuch-Öse …) entfernen.
    if remove_holes and n > 0:
        sizes = ndi.sum(np.ones_like(mn), lab, index=np.arange(n + 1))
        means = ndi.mean(mn, lab, index=np.arange(n + 1))
        for i in range(1, n + 1):
            if i not in border and sizes[i] > hole_min and means[i] > HOLE_MEAN:
                bg |= lab == i

    fg = ~bg
    fg = ndi.binary_opening(fg, iterations=1)
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    a = np.asarray(alpha).astype(np.float32) / 255
    a = np.clip((a - 0.15) / 0.7, 0, 1)
    # Kanten-Entmischung: Farbe aus der Alpha-Gemischte Farbe freirechnen.
    safe = np.maximum(a, 0.05)[..., None]
    rgb = np.clip((im - (1 - safe) * 255) / safe, 0, 255)
    rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
    return rgba, fg


def cutout_character(src, *, hole_min: int = HOLE_MIN):
    """Figuren-/Tier-Modus: keine Loch-Entfernung (Augenweiß bleibt erhalten)."""
    return cutout(src, remove_holes=False, hole_min=hole_min)


def as_image(rgba: np.ndarray) -> Image.Image:
    """RGBA-Array als PIL-Bild (für split.py u. a.)."""
    return Image.fromarray(rgba, "RGBA")
