#!/usr/bin/env python3
"""P06-T10 – Alles in einem Durchlauf: run.py <verzeichnis> [Optionen]

Ablauf je Blatt (YAML neben dem Bild, z. B. ``raw_items.yaml``):
  2. Freistellen      cutout.py   (Figuren: ``mode: character``, Augenweiß bleibt)
  3. Zerlegen         split.py    Anzahl == YAML, sonst Fehler mit Vorschaubild
  4. Maßstab          scale.py    Höhe = Tabelle × scale_mul, Breite aus Seitenverhältnis
  5. Punkte           points.py   Pivot/Grip je Kategorie, YAML-Override gewinnt
  6. Export           export.py   8 px/cm, 4 px Padding, JSON-Upsert (kein Duplikat)

Danach (sofern nicht abgeschaltet):
  8. Lineup-Bild      docs/tests/lineup_<bereich>.png
  9. Test-Szene       docs/tests/P06/scene_test*.png (bei ``scene: reference_kitchen``)

Beispiel:
  python3 tools/asset_pipeline/run.py reference/
  python3 tools/asset_pipeline/run.py incoming/home --points-preview
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from export import (  # noqa: E402
    ITEMS_ROOT,
    SPRITES_ROOT,
    build_record,
    export_sprite,
    upsert_items,
)
from lineup import render as lineup_render  # noqa: E402
from points import find_hand_grip, points, preview as points_preview  # noqa: E402
from scale import ScaleError, load_table, resolve  # noqa: E402
from scene_test import render_reference_kitchen  # noqa: E402
from split import SplitError, split_sheet  # noqa: E402

CHAR_ROOT = ROOT / "assets" / "characters" / "sprite"


def _process_sheet(y: Path, *, table_pair, sprites_root: Path, items_root: Path,
                   char_root: Path, points_dir: Path | None, errors: list[str],
                   warnings: list[str]) -> tuple[dict, dict, str | None]:
    """Ein Blatt abarbeiten. Gibt (recs, zusammenfassung, area) zurück."""
    spec = yaml.safe_load(y.read_text(encoding="utf-8")) or {}
    sheet = y.parent / (spec.get("sheet") or f"{y.stem}.png")
    if not sheet.exists():
        errors.append(f"{y.name}: Blatt {sheet.name} fehlt")
        return {}, {}, None
    area = spec.get("area", "home")
    room = spec.get("room", "")
    mode = spec.get("mode", "items")
    item_specs = list(spec.get("items") or [])
    expected = [it["id"] for it in item_specs]
    if not expected:
        errors.append(f"{y.name}: keine items deklariert")
        return {}, {}, area

    try:
        parts = split_sheet(sheet, expected, y.parent,
                            remove_holes=(mode != "character"), mode=mode)
    except SplitError as e:
        errors.append(str(e))
        if e.preview:
            errors.append(f"  Vorschau: {e.preview}")
        return {}, {}, area

    recs: dict[str, dict] = {}
    records: list[dict] = []
    for it, img in zip(item_specs, parts):
        ref = it.get("scale_ref") or it["id"]
        entry = table_pair[0].get(ref)
        try:
            sc = resolve(it, img.width, img.height, table_pair)
        except ScaleError as e:
            errors.append(str(e))
            continue
        warnings.extend(sc["warnings"])
        pts = points(it, entry)
        if mode == "character":
            grip = find_hand_grip(img)
            out = export_sprite(img, sc["size_cm"], it["id"], area,
                                out_path=char_root / f"{it['id']}.png")
            rec = {"id": it["id"], "size_cm": sc["size_cm"], "hand_grip": grip,
                   "sprite": f"res://assets/characters/sprite/{it['id']}.png",
                   "_path": out}
            (char_root / f"{it['id']}.sprite.json").write_text(
                json.dumps({k: rec[k] for k in ("id", "size_cm", "hand_grip", "sprite")},
                           indent=1) + "\n", encoding="utf-8")
            recs[it["id"]] = rec
        else:
            rec = build_record(it, sc["size_cm"], pts, area)
            out = export_sprite(img, sc["size_cm"], it["id"], area,
                                sprites_root=sprites_root)
            records.append(rec)                      # ohne _path → sauberes JSON
            recs[it["id"]] = {**rec, "_path": out}
        if points_dir is not None:
            points_preview(img, pts, points_dir / f"{it['id']}.png")

    summary = {"blatt": sheet.name, "modus": mode, "items": len(item_specs)}
    if records:
        items_file = spec.get("items_json") or f"{area}.json"
        path = items_root / items_file
        before = {}
        if path.exists():
            before = {r["id"]: r for r in
                      json.loads(path.read_text(encoding="utf-8")).get("items", [])}
        upsert_items(records, area=area, room=room, items_path=path)
        after = {r["id"]: r for r in
                 json.loads(path.read_text(encoding="utf-8"))["items"]}
        summary["neu"] = sum(1 for r in records if r["id"] not in before)
        summary["aktualisiert"] = sum(
            1 for r in records
            if r["id"] in before and before[r["id"]] != {k: v for k, v in after[r["id"]].items()})
        summary["unveraendert"] = sum(
            1 for r in records
            if r["id"] in before and before[r["id"]] == after[r["id"]])
        summary["json"] = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    return recs, summary, area


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="Verzeichnis mit Blättern + <blatt>.yaml")
    ap.add_argument("--items-root", type=Path, default=ITEMS_ROOT)
    ap.add_argument("--sprites-root", type=Path, default=SPRITES_ROOT)
    ap.add_argument("--characters-root", type=Path, default=CHAR_ROOT)
    ap.add_argument("--lineup-dir", type=Path, default=ROOT / "docs" / "tests")
    ap.add_argument("--scene-dir", type=Path, default=ROOT / "docs" / "tests" / "P06")
    ap.add_argument("--points-preview", action="store_true",
                    help="Vorschaubilder mit Pivot/Grip-Markern schreiben")
    ap.add_argument("--no-lineup", action="store_true")
    ap.add_argument("--no-scene", action="store_true")
    a = ap.parse_args(argv)

    src = Path(a.dir)
    yamls = sorted(src.glob("*.yaml"))
    if not yamls:
        print(f"❌ Keine <blatt>.yaml in {src}")
        return 1

    table_pair = load_table()
    errors: list[str] = []
    warnings: list[str] = []
    all_recs: dict[str, dict] = {}
    last_items_json: Path | None = None
    area_first: str | None = None
    scene_flags: set[str] = set()
    totals = {"neu": 0, "aktualisiert": 0, "unveraendert": 0}

    for y in yamls:
        spec_safe = yaml.safe_load(y.read_text(encoding="utf-8")) or {}
        if spec_safe.get("scene"):
            scene_flags.add(spec_safe["scene"])
        recs, summary, area = _process_sheet(
            y, table_pair=table_pair, sprites_root=Path(a.sprites_root),
            items_root=Path(a.items_root), char_root=Path(a.characters_root),
            points_dir=(src / "points_preview") if a.points_preview else None,
            errors=errors, warnings=warnings)
        if area and area_first is None:
            area_first = area
        all_recs.update(recs)
        if "json" in summary:
            last_items_json = ROOT / summary["json"]
        for k in ("neu", "aktualisiert", "unveraendert"):
            totals[k] += summary.get(k, 0)
        print(f"  ✓ {summary.get('blatt', y.name)} [{summary.get('modus', '?')}] "
              f"{summary.get('items', 0)} Items"
              + (f" → {summary['json']} (+{summary.get('neu', 0)} neu, "
                 f"{summary.get('aktualisiert', 0)} aktualisiert)" if "json" in summary else ""))

    if not a.no_lineup and last_items_json is not None and area_first:
        p = lineup_render(last_items_json, Path(a.lineup_dir) / f"lineup_{area_first}.png")
        print(f"  ✓ Lineup → {p}")
    if not a.no_scene and "reference_kitchen" in scene_flags and all_recs:
        bg = src / "raw_kitchen_bg.png"
        if bg.exists():
            for p in render_reference_kitchen(all_recs, bg, Path(a.scene_dir),
                                              sprites_root=Path(a.sprites_root)):
                print(f"  ✓ Test-Szene → {p}")
        else:
            warnings.append("scene: reference_kitchen, aber raw_kitchen_bg.png fehlt")

    print(f"\nZusammenfassung: {totals['neu']} neu · {totals['aktualisiert']} aktualisiert · "
          f"{totals['unveraendert']} unverändert · {len(warnings)} Warnung(en)")
    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        print(f"\n❌ {len(errors)} Fehler:")
        for e in errors:
            print(f"  • {e}")
        return 1
    print("✅ Alles ok.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
