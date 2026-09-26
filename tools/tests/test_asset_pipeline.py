"""P06-T01 – cutout.py: weißer Hintergrund weg, Loch-Regel, Figuren-Modus, keine weißen Säume.

Beweise (synthetische Testbilder, reproduzierbar ohne KI):
  * Randfläche (Hintergrund) wird transparent, Objektmitte bleibt deckend.
  * Henkel-Loch (> 500 px, sehr weiß) wird transparent – Modus ``remove_holes``.
  * Augenweiß-Szenario (``cutout_character``): Loch bleibt.
  * Mini-Loch (< 500 px) bleibt in beiden Modi.
  * Kanten-Entmischung: halbtransparente Kante ist Objektfarbe, nicht Weiß.
  * Annahme als Pfad UND als PIL-Bild.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "asset_pipeline"))

from cutout import cutout, cutout_character  # noqa: E402

RED = (200, 40, 40)


def _blob_with_hole(diameter=600, blob=(90, 90, 510, 510), hole_r=16) -> Image.Image:
    """Roter Blob auf Weiß mit weißem, eingeschlossenem Loch in der Mitte."""
    im = Image.new("RGB", (diameter, diameter), "white")
    dr = ImageDraw.Draw(im)
    dr.ellipse(blob, fill=RED)
    c = diameter // 2
    dr.ellipse([c - hole_r, c - hole_r, c + hole_r, c + hole_r], fill="white")
    return im


def test_background_transparent_object_opaque():
    rgba, fg = cutout(_blob_with_hole(hole_r=0))
    a = rgba[..., 3]
    assert a[0, 0] == 0, "Ecke (Hintergrund) muss transparent sein"
    assert a[300, 150] == 255, "Objektmitte muss deckend sein"
    assert fg[300, 150] and not fg[0, 0]


def test_henkel_hole_removed_in_default_mode():
    """Loch > 500 px & sehr weiß → transparent (Tassenhenkel-Regel)."""
    rgba, _ = cutout(_blob_with_hole(hole_r=16))  # ~800 px
    a = rgba[..., 3]
    assert a[300, 300] == 0, "Henkel-Loch muss transparent werden"
    assert a[300, 150] == 255, "Objekt selbst bleibt"


def test_character_mode_keeps_eye_white():
    """Figuren-Modus: dasselbe Loch bleibt (Augenweiß-Regel)."""
    rgba, _ = cutout_character(_blob_with_hole(hole_r=16))
    a = rgba[..., 3]
    assert a[300, 300] == 255, "Augenweiß darf NICHT transparent werden"
    assert a[0, 0] == 0, "Hintergrund trotzdem frei"


def test_small_hole_stays_in_both_modes():
    """Loch < 500 px bleibt in beiden Modi (Regel hält sich an hole_min)."""
    im = _blob_with_hole(hole_r=4)  # ~50 px
    for fn in (cutout, cutout_character):
        rgba, _ = fn(im)
        assert rgba[300, 300, 3] == 255, f"{fn.__name__}: Mini-Loch bleibt"


def test_no_white_fringe_on_edges():
    """Kanten-Entmischung: halbtransparente Kante trägt Objektfarbe, nicht Weiß."""
    rgba, _ = cutout(_blob_with_hole(hole_r=0))
    a = rgba[..., 3].astype(np.float32) / 255
    mid = (a > 0.25) & (a < 0.75)
    assert mid.sum() >= 20, "erwartet eine weiche Kante"
    rb = rgba[..., 0].astype(np.int16) - rgba[..., 2].astype(np.int16)
    assert float(np.median(rb[mid])) > 60, "Kante ist weißlich statt rot"


def test_accepts_path(tmp_path):
    p = tmp_path / "sheet.png"
    _blob_with_hole(hole_r=16).save(p)
    rgba, fg = cutout(str(p))
    assert rgba.shape[2] == 4 and fg.any() and not fg.all()


def test_cutout_output_is_rgb8():
    """Godot-tauglich: uint8, H×W×4, Alpha 0..255."""
    rgba, _ = cutout(_blob_with_hole(hole_r=8))
    assert rgba.dtype == np.uint8
    assert rgba.ndim == 3 and rgba.shape[2] == 4
    assert rgba[..., 3].min() == 0 and rgba[..., 3].max() == 255
