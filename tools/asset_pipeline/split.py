#!/usr/bin/env python3
"""P06-T02 – Zerlegen: Blatt in Einzelobjekte schneiden, Lesereihenfolge, Anzahl-Prüfung.

Übernommen und gehärtet aus reference/pipeline_demo_kueche.py:

* Objekte = zusammenhängende Vordergrundflächen (Dilation 8), ab ``min_area``.
* Reihenfolge: erst Zeilen über die **vertikale Mitte** bilden (neue Zeile bei
  center_y-Abstand > ``row_gap``, NICHT über die Oberkante – sonst vertauscht
  sich Tulpe ↔ Teddy), dann innerhalb der Zeile links → rechts.
* Die Anzahl muss zur Blatt-YAML passen, sonst ``SplitError`` samt
  Vorschaubild mit nummerierten Objekten (statt still zu raten).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

from cutout import cutout

MIN_AREA = 1500   # px – kleinere Flöhe vom Raster ignorieren
ROW_GAP = 90      # px – Abstand der vertikalen Mittel, ab dem eine neue Zeile beginnt
DILATE = 8        # px – zusammenhängende Objekte werden mit Puffer verbunden


class SplitError(Exception):
    """Objektanzahl passt nicht zur YAML (Vorschau-Datei im Exception-Attribut)."""

    def __init__(self, message: str, preview: Path | None = None):
        super().__init__(message)
        self.preview = preview


def _find_objects(rgba: np.ndarray, fg: np.ndarray, min_area: int) -> list[dict]:
    """Alle Objekte finden und in Lesereihenfolge sortieren (Zeilen → links→rechts)."""
    lab, _n = ndi.label(ndi.binary_dilation(fg, iterations=DILATE))
    objs: list[dict] = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        if sl is None:
            continue
        if (lab[sl] == i).sum() < min_area:
            continue
        crop = rgba[sl].copy()
        crop[..., 3] = crop[..., 3] * (lab[sl] == i)
        objs.append(dict(cy=sl[0].start + crop.shape[0] / 2, x=sl[1].start, sl=sl, arr=crop))
    if not objs:
        return []
    objs.sort(key=lambda o: o["cy"])
    rows, cur = [], [objs[0]]
    for o in objs[1:]:
        if o["cy"] - cur[-1]["cy"] > ROW_GAP:
            rows.append(cur)
            cur = [o]
        else:
            cur.append(o)
    rows.append(cur)
    return [o for r in rows for o in sorted(r, key=lambda o: o["x"])]


def split(rgba: np.ndarray, fg: np.ndarray, *, min_area: int = MIN_AREA) -> list[Image.Image]:
    """Feld → PIL-Bilder in Lesereihenfolge (unbeschnitten, Alpha maskiert)."""
    return [Image.fromarray(o["arr"], "RGBA") for o in _find_objects(rgba, fg, min_area)]


def trim(img: Image.Image) -> Image.Image:
    """Transparenten Rand abschneiden (Alpha-Bbox)."""
    bb = img.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    return img.crop(bb) if bb else img


def _preview(sheet: Image.Image, objs: list[dict], out: Path) -> Path:
    """Vorschaubild: jedes gefundene Objekt mit rotem Kasten + Index."""
    vis = sheet.convert("RGB")
    d = ImageDraw.Draw(vis)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
    for n, o in enumerate(objs):
        x0, y0 = o["sl"][1].start, o["sl"][0].start
        x1, y1 = o["sl"][1].stop, o["sl"][0].stop
        d.rectangle([x0, y0, x1, y1], outline=(220, 30, 30), width=3)
        d.text((x0 + 6, y0 + 4), str(n), fill=(220, 30, 30), font=font)
    out.parent.mkdir(parents=True, exist_ok=True)
    vis.save(out)
    return out


def split_sheet(path, expected_ids: list[str], out_dir,
                *, min_area: int = MIN_AREA, remove_holes: bool = True) -> list[Image.Image]:
    """Blatt freistellen, zerlegen, trimmen und gegen die YAML-Liste prüfen.

    ``expected_ids``: die IDs aus blatt.yaml in Lesereihenfolge.
    Passt die Anzahl nicht, wird ``SplitError`` geworfen (mit Vorschaubild).
    """
    path = Path(path)
    out_dir = Path(out_dir)
    rgba, fg = cutout(str(path), remove_holes=remove_holes)
    objs = _find_objects(rgba, fg, min_area)
    if len(objs) != len(expected_ids):
        prev = _preview(Image.open(path), objs,
                        out_dir / f"{path.stem}_split_preview.png")
        raise SplitError(
            f"{path.name}: {len(objs)} Objekte gefunden, {len(expected_ids)} erwartet "
            f"({', '.join(expected_ids[:8])}{' …' if len(expected_ids) > 8 else ''})",
            preview=prev)
    return [trim(Image.fromarray(o["arr"], "RGBA")) for o in objs]
