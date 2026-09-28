#!/usr/bin/env python3
"""
P09/P10: Bereichs-Dateien erzeugen (data/areas/<bereich>.json + data/npcs/<bereich>.json) aus den Layouts in
tools/areas/<bereich>.py. Jede Item-ID, jedes Raum-Symbol und jede NPC-Rolle wird gegen die Daten geprüft.
Danach: python3 tools/make_rooms.py --area <bereich> (Hintergründe).
Aufruf: python3 tools/make_areas.py [bereich …]
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from areas.common import ROOT, check  # noqa: E402

AREAS = ["shopping", "playground", "school"]


def main(argv: list[str] | None = None) -> int:
    only = (sys.argv[1:] if argv is None else argv) or AREAS
    bad = []
    for name in only:
        mod = importlib.import_module(f"areas.{name}")
        area, npcs = mod.area(), mod.npcs()
        bad += check(area, npcs)
        (ROOT / f"data/areas/{area['id']}.json").write_text(json.dumps(area, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        (ROOT / f"data/npcs/{area['id']}.json").write_text(json.dumps(npcs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  {area['id']}: {len(area['rooms'])} Räume, {sum(len(r['default_items']) for r in area['rooms'])} Start-Items, "
              f"{len(npcs['npcs'])} NPCs")
    for b in bad:
        print("❌", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
