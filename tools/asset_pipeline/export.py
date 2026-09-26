#!/usr/bin/env python3
"""P06-T05 – Export: Sprites mit 8 px/cm + 4 px Padding, Item-JSON upserten.

* Ziel-Dichte **8 px/cm** (doppelte Referenz-Auflösung), kleine Items werden
  hochskaliert, bis die kleinste Kante ≥ 64 px ist – die **Weltgröße (size_cm)
  bleibt exakt** aus der Maßstab-Tabelle.
* 4 px transparentes Padding rundum (Greif-/Zeichen-Rand fürs Rendering).
* PNG nach ``assets/sprites/<bereich>/<id>.png``, Sprite-Pfad im JSON als
  ``res://assets/sprites/<bereich>/<id>.png``.
* Item-JSON: **bestehende Einträge aktualisieren, niemals duplizieren**
  (Upsert pro ``id`` in ``data/items/<datei>.json``).
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SPRITES_ROOT = ROOT / "assets" / "sprites"
ITEMS_ROOT = ROOT / "data" / "items"

PX_PER_CM = 8      # Ausgabe-Dichte (2× Referenz 4 px/cm)
MIN_EDGE_PX = 64   # kleinste Kantenlänge, sonst werden Details matschig
PAD_PX = 4         # transparentes Padding


def target_px(size_cm: list[float], px_per_cm: int = PX_PER_CM,
              min_edge: int = MIN_EDGE_PX) -> tuple[int, int, float]:
    """Sprite-Zielmaße: Dichte px/cm, bei kleinen Items hochskaliert."""
    w_cm, h_cm = size_cm
    density = max(px_per_cm, min_edge / min(w_cm, h_cm))
    w = max(1, round(w_cm * density))
    h = max(1, round(h_cm * density))
    if min(w, h) < min_edge:          # Rundungs-Sicherheit
        f = min_edge / min(w, h)
        w, h = max(1, round(w * f)), max(1, round(h * f))
    return w, h, density


def export_sprite(img: Image.Image, size_cm: list[float], item_id: str, area: str,
                  *, sprites_root: Path | None = None) -> Path:
    """Sprite auf size_cm × 8 px/cm skalieren, padden und als PNG ablegen."""
    root = Path(sprites_root) if sprites_root else SPRITES_ROOT
    w, h, _ = target_px(size_cm)
    im = img.convert("RGBA").resize((w, h), Image.LANCZOS)
    canvas = Image.new("RGBA", (w + 2 * PAD_PX, h + 2 * PAD_PX), (0, 0, 0, 0))
    canvas.alpha_composite(im, (PAD_PX, PAD_PX))
    out = root / area / f"{item_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    return out


def sprite_res_path(area: str, item_id: str) -> str:
    return f"res://assets/sprites/{area}/{item_id}.png"


def build_record(spec: dict, size_cm: list[float], pts: dict, area: str) -> dict:
    """Item-Record im Format von data/items/*.json (Schlüssel wie die Referenz)."""
    rec = {
        "id": spec["id"],
        "scale_ref": spec.get("scale_ref") or spec["id"],
        "size_cm": [round(size_cm[0], 1), round(size_cm[1], 1)],
        "pivot": pts["pivot"],
        "grip": pts["grip"],
        "hold": pts["hold"],
        "hold_angle": pts["hold_angle"],
        "placement": spec.get("placement") or "floor",
        "movable": bool(spec.get("movable", True)),
        "sprite": sprite_res_path(area, spec["id"]),
    }
    if float(spec.get("scale_mul", 1.0)) != 1.0:
        rec["scale_mul"] = float(spec["scale_mul"])
    return rec


def upsert_items(records: list[dict], *, area: str, room: str,
                 items_path: Path) -> list[str]:
    """Records in eine Item-JSON schreiben: ersetzen an Ort und Stelle, neue anhängen.

    Gibt die Liste der neu/aktualisierten IDs zurück. Datei-Struktur
    ``{area, room, items}`` wie in data/items/.
    """
    items_path = Path(items_path)
    if items_path.exists():
        data = json.loads(items_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "items" not in data:
            raise ValueError(f"{items_path}: unerwartete Struktur (['items'] fehlt)")
    else:
        data = {"area": area, "room": room, "items": []}
        items_path.parent.mkdir(parents=True, exist_ok=True)

    by_id = {r["id"]: i for i, r in enumerate(data["items"])}
    changed = []
    for rec in records:
        if rec["id"] in by_id:
            data["items"][by_id[rec["id"]]] = rec
        else:
            by_id[rec["id"]] = len(data["items"])
            data["items"].append(rec)
        changed.append(rec["id"])
    items_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    return changed
