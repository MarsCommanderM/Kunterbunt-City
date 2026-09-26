"""P04-Beweisbilder (docs/tests/P04): messbar prüfen statt gucken.

  * alle Bilder sind echte Rollen (Größe, Kontrast, Farben)
  * `p04_02_schablonen_groessen.jpg`: die 3 Schablonen stehen im Verhältnis 90 : 125 : 172
  * `p04_03_farbzonen.jpg`: jede Figur trägt IHRE Palettenfarbe (Zonen-Shader, P04-T04)
"""
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "docs" / "tests" / "P04"
NAMES = ["p04_01_teile_katalog.jpg", "p04_02_schablonen_groessen.jpg", "p04_03_farbzonen.jpg"]
BG = (255, 247, 236)          # Hintergrund der Lookbook-Szene

Image = pytest.importorskip("PIL.Image", reason="Pillow fehlt")


def _load(name):
    p = SHOTS / name
    assert p.exists(), f"fehlt: {p} (tools/godot/p04_lookbook.gd ausführen)"
    return Image.open(p).convert("RGB")


def _is_bg(p):
    return abs(p[0] - BG[0]) + abs(p[1] - BG[1]) + abs(p[2] - BG[2]) <= 40


@pytest.mark.parametrize("name", NAMES)
def test_bild_vorhanden_und_scharf(name):
    im = _load(name)
    assert im.size[0] >= 1200 and im.size[1] >= 600
    colors = im.getcolors(maxcolors=1 << 22) or []
    assert len(colors) > 500, f"{name}: nur {len(colors)} Farben"
    small = im.resize((64, 36))
    px = list(small.getdata())
    mean = sum(sum(p) for p in px) / (3 * len(px))
    var = sum((sum(p) / 3 - mean) ** 2 for p in px) / len(px)
    assert 10.0 < mean < 250.0 and var > 25.0, f"{name}: Helligkeit {mean:.0f}, Kontrast {var:.0f}"


def test_schablonen_im_tabellenverhaeltnis():
    """Höhen der drei Schablonen im Bild → Verhältnis muss 90 : 125 : 172 sein (Größe nur aus der Schablone)."""
    im = _load("p04_02_schablonen_groessen.jpg")
    w, h = im.size
    px = im.load()
    heights = []
    for cx in [int((x + 235) / 470 * w) for x in (-140, 0, 140)]:     # Figuren-Mitten
        ys = [y for y in range(h) if not _is_bg(px[cx, y])]
        assert ys, "Figur nicht gefunden"
        heights.append(max(ys) - min(ys))
    base = heights[1]                                                  # Kind = 125 cm
    want = [90 / 125, 1.0, 172 / 125]
    for got, w_, name in zip(heights, want, ["toddler", "kid", "adult"]):
        assert abs(got / base - w_) < 0.10, f"{name}: {got / base:.2f} statt {w_:.2f} (px {heights})"


def test_farbzonen_faerben_jede_figur_eigen():
    """10 Figuren, je eine Palettenfarbe: gemessene Farb-Richtung muss zur zugewiesenen Farbe passen."""
    im = _load("p04_03_farbzonen.jpg")
    w, _ = im.size
    px = im.load()
    pal = json.loads((ROOT / "data" / "character_parts" / "palette.json").read_text(encoding="utf-8"))["cloth"]["colors"]

    def vec(hex_col):
        return [int(hex_col[i:i + 2], 16) / 255 for i in (1, 3, 5)]

    def cos(a, b):
        n = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(x * x for x in b))
        return sum(x * y for x, y in zip(a, b)) / n

    means, hits = [], 0
    for i in range(len(pal)):
        cx = int((-315 + i * 70 + 370) / 740 * w)                       # Figuren-Mitte
        acc, n = [0.0, 0.0, 0.0], 0
        for x in range(cx - 25, cx + 26):
            for y in range(575, 665):                                  # Oberteil-Band
                p = px[x, y]
                acc = [a + b / 255 for a, b in zip(acc, p)]
                n += 1
        m = [a / n for a in acc]
        means.append(m)
        best = max(range(len(pal)), key=lambda k: cos(m, vec(pal[k])))
        hits += 1 if best == i else 0
    assert hits >= 9, f"nur {hits}/{len(pal)} Farben korrekt zugeordnet"
    for a in range(len(means)):
        for b in range(a + 1, len(means)):
            d = sum(abs(x - y) for x, y in zip(means[a], means[b]))
            assert d > 0.05, f"Figuren {a} und {b} haben dieselbe Farbe"
