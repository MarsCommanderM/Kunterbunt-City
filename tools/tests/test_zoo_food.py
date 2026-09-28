"""P10g: Kein Start-Futter liegt in Fress-Reichweite eines Tiers, das es mag (sonst ist es beim Betreten schon weg)."""
import glob
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FEED_CM = 140.0          # = ZooActions.FEED_CM


def test_start_food_is_not_eaten_on_arrival():
    items = {}
    for f in glob.glob(str(ROOT / "data/items/*.json")):
        for it in json.loads(Path(f).read_text(encoding="utf-8"))["items"]:
            items[it["id"]] = it
    bad = []
    for area in glob.glob(str(ROOT / "data/areas/*.json")):
        d = json.loads(Path(area).read_text(encoding="utf-8"))
        for r in d.get("rooms", []):
            entries = [e for e in r.get("default_items", []) if "x_cm" in e and e["id"] in items]
            animals = [e for e in entries if "zoo" in items[e["id"]].get("tags", [])]
            for e in entries:
                it = items[e["id"]]
                if "zoo_food" not in it.get("tags", []) and not e["id"].startswith("food_"):
                    continue
                for a in animals:
                    diet = [t[5:] for t in items[a["id"]]["tags"] if t.startswith("eats:")]
                    near = abs(a["x_cm"] - e["x_cm"]) - items[a["id"]]["size_cm"][0] / 2 < FEED_CM
                    if near and abs(a["y_cm"] - e["y_cm"]) < 80 and any(e["id"].startswith(p) for p in diet):
                        bad.append(f"{r['id']}: {e['id']} neben {a['id']}")
    assert not bad, bad
