#!/usr/bin/env python3
"""P06-T03 – Maßstab: Höhe aus scale_table × scale_mul, Breite aus dem Seitenverhältnis.

Regeln (Tech-Spec / docs/04_ASSET_PIPELINE.md):
* ``h_cm  = Tabelle[scale_ref].h_cm × scale_mul``   (scale_mul Standard 1.0)
* ``w_cm  = h_cm × Seitenverhältnis des Sprites``   (aus dem freigestellten Teil)
* Weicht die so berechnete Breite mehr als ``tolerance_aspect`` (30 %) von der
  Tabellen-Breite ab → **Warnung** (Sprite ist zu breit/schmal gezeichnet).
* Unbekanntes ``scale_ref`` → ``ScaleError`` (kein Raten).

Alles kommt ausschließlich aus data/scale_table.json – die Tabelle ist die Bibel.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
TABLE_PATH = ROOT / "data" / "scale_table.json"


class ScaleError(Exception):
    """scale_ref fehlt in der Tabelle o. Ä. – harter Fehler, kein Weitermachen."""


def load_table(path=TABLE_PATH) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {e["id"]: e for e in data["entries"]}, data.get("tolerance_aspect", 0.3)


def resolve(spec: dict, sprite_w: int, sprite_h: int, table=None) -> dict:
    """Ein YAML-Item + Sprite-Maße → size_cm inkl. Warnungen.

    ``spec``: {"id": …, "scale_ref": …, "scale_mul": 0.9?}
    Gibt {"size_cm": [w, h], "aspect": float, "warnings": [str, …]} zurück.
    """
    if table is None:
        table, tol = load_table()
    else:
        tol = 0.3 if not isinstance(table, tuple) else table[1]
        table = table[0] if isinstance(table, tuple) else table

    ref = spec.get("scale_ref") or spec.get("id")
    entry = table.get(ref)
    if entry is None:
        raise ScaleError(f"scale_ref '{ref}' fehlt in data/scale_table.json")

    mul = float(spec.get("scale_mul", 1.0))
    h_cm = entry["h_cm"] * mul
    if sprite_h <= 0 or sprite_w <= 0:
        raise ScaleError(f"{spec.get('id')}: Sprite-Maße {sprite_w}×{sprite_h} sind ungültig")
    aspect = sprite_w / sprite_h
    w_cm = h_cm * aspect

    warnings: list[str] = []
    label = spec.get("id") or ref
    tbl_w = entry.get("w_cm", 0)
    if tbl_w and tbl_w > 0:
        dev = abs(w_cm - tbl_w) / tbl_w
        if dev > tol:
            warnings.append(
                f"{label}: Breite {w_cm:.1f} cm weicht >{int(tol * 100)} % von "
                f"Tabellen-Breite {tbl_w:.1f} cm ab (Seitenverhältnis {aspect:.2f})")
    return {"size_cm": [round(w_cm, 1), round(h_cm, 1)],
            "aspect": round(aspect, 4),
            "warnings": warnings}


def resolve_image(spec: dict, img: Image.Image, table=None) -> dict:
    """Wie resolve(), aber mit PIL-Bild statt Zahlen."""
    return resolve(spec, img.width, img.height, table)
