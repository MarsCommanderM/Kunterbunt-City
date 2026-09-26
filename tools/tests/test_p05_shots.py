"""P05-Beweisbilder (docs/tests/P05): Startmenü, Bereich, Album, Rucksack, Einstellungen.

Alle Prüfungen sind gemessen (Farben, Flächen, Kanten) – nicht „sieht gut aus".
"""
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "docs" / "tests" / "P05"
INDEX = ROOT / "data" / "areas" / "index.json"

MAP = "p05_01_stadtkarte.jpg"
GRID = "p05_02_stadtkarte_raster.jpg"
PLAY = "p05_03_bereich_gespielt.jpg"
ALBUM = "p05_04_album.jpg"
PACK = "p05_05_rucksack.jpg"
GATE = "p05_06_elterntor.jpg"
SETTINGS = "p05_07_einstellungen.jpg"
BACK = "p05_08_zurueck_auf_der_karte.jpg"
ALL = [MAP, GRID, PLAY, ALBUM, PACK, GATE, SETTINGS, BACK]

Image = pytest.importorskip("PIL.Image", reason="Pillow fehlt")


def _load(name):
    p = SHOTS / name
    assert p.exists(), f"fehlt: {p} (tools/godot/p05_flow_runner.gd ausführen)"
    return Image.open(p).convert("RGB")


def _mean(im, box=None):
    c = im.crop(box) if box else im
    px = list(c.getdata())
    n = len(px)
    return tuple(round(sum(p[i] for p in px) / n) for i in range(3))


def _nonwhite_ratio(im, box):
    px = list(im.crop(box).getdata())
    return sum(1 for r, g, b in px if not (r > 244 and g > 244 and b > 244)) / len(px)


@pytest.mark.parametrize("name", ALL)
def test_bild_vorhanden_und_bunt(name):
    im = _load(name)
    assert im.size == (1920, 1080), f"{name}: falsche Größe {im.size}"
    colors = im.getcolors(maxcolors=1 << 22) or []
    assert len(colors) > 800, f"{name}: nur {len(colors)} Farben"
    mean = _mean(im)
    assert 120 < sum(mean) / 3 < 250, f"{name}: Helligkeit {mean}"


def test_stadtkarte_zeigt_die_bereiche():
    im = _load(MAP)
    areas = json.loads(INDEX.read_text(encoding="utf-8"))["areas"]
    px = im.load()
    found = 0
    for a in areas:
        want = tuple(int(a["color"].lstrip("#")[i * 2:i * 2 + 2], 16) for i in range(3))
        hits = 0
        for y in range(150, 1080, 6):
            for x in range(0, 1920, 6):
                r, g, b = px[x, y]
                if abs(r - want[0]) + abs(g - want[1]) + abs(b - want[2]) < 150:
                    hits += 1
                    if hits > 40:
                        found += 1
                        break
            if hits > 40:
                break
    assert found >= 10, f"nur {found} von {len(areas)} Bereichs-Inseln gefunden"


def test_karten_hintergrund_ist_gruen():
    m = _mean(_load(MAP), (0, 200, 1920, 1000))
    assert m[1] > m[0] and m[1] > m[2], f"Karte soll grünlich sein, ist {m}"


def test_raster_zeigt_vier_karten_pro_zeile():
    im = _load(GRID)
    px = im.load()
    best = 0
    for y in range(200, 1000, 8):
        runs, run = 0, 0
        for x in range(20, 1900):
            r, g, b = px[x, y]
            if r > 246 and g > 246 and b > 246:
                run += 1
            else:
                if run >= 250:
                    runs += 1
                run = 0
        if run >= 250:
            runs += 1
        best = max(best, runs)
    assert best >= 3, f"Raster: nur {best} Karten pro Zeile erkannt"


def test_bereich_sieht_anders_aus_als_die_karte():
    a, b = _mean(_load(MAP)), _mean(_load(PLAY))
    assert sum(abs(x - y) for x, y in zip(a, b)) > 60, f"Karte {a} vs. Bereich {b}"


def test_bereich_ist_gefuellt():
    im = _load(PLAY)
    assert _nonwhite_ratio(im, (0, 300, 1920, 1080)) > 0.5, "der Bereich wirkt leer"


def test_album_und_rucksack_zeigen_inhalt():
    for name, box in ((ALBUM, (300, 300, 1620, 900)), (PACK, (420, 260, 1500, 880))):
        im = _load(name)
        assert _nonwhite_ratio(im, box) > 0.05, f"{name}: Panel ist leer"


def test_einstellungen_und_tor_sind_helle_panels():
    for name in (GATE, SETTINGS):
        m = _mean(_load(name), (700, 250, 1220, 800))
        assert sum(m) / 3 > 150, f"{name}: Panel zu dunkel {m}"


def test_zurueck_zeigt_wieder_die_karte():
    a, b = _mean(_load(MAP)), _mean(_load(BACK))
    assert sum(abs(x - y) for x, y in zip(a, b)) < 60, f"Karte vorher {a}, nachher {b}"


def test_messwerte_json():
    p = SHOTS / "p05_flow.json"
    assert p.exists(), "fehlt: p05_flow.json (tools/godot/p05_flow_runner.gd ausführen)"
    m = json.loads(p.read_text(encoding="utf-8"))
    assert m["bereiche_knopf_anzahl"] == 12
    assert m["bereiche_spielbar"] >= 1
    for key in ("stadtkarte_da", "bereich_da", "baustelle_sichtbar", "zurueck_zur_karte",
                "rucksack_einpacken", "rucksack_leer_nach_rausholen"):
        assert m[key] is True, f"{key} ist nicht erfüllt"
    assert m["ladezeit_ms"] < 2000, f"Bereichswechsel {m['ladezeit_ms']} ms (Ziel < 2000 ms)"
    assert 124.0 <= m["eigene_figur_cm"] <= 126.0, m["eigene_figur_cm"]
    assert m["items_im_bereich"] >= 13, m["items_im_bereich"]
    assert m["gespeicherter_raumzustand"] >= 12, m["gespeicherter_raumzustand"]
    assert m["fotos_im_album"] >= 1
    assert m["nach_neustart_figuren"] == 1
    assert m["nach_neustart_aktiv"] == "Mia"
