"""P04-Beweisbilder (docs/tests/P04): messbar prüfen statt gucken.

  * alle Bilder sind echte Rollen (Größe, Kontrast, Farben)
  * `p04_02_schablonen_groessen.jpg`: die 3 Schablonen stehen im Verhältnis 90 : 125 : 172
  * `p04_03_farbzonen.jpg`: jede Figur trägt IHRE Prüffarbe (Zonen-Shader, P04-T04)
"""
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "docs" / "tests" / "P04"
NAMES = ["p04_01_teile_katalog.jpg", "p04_02_schablonen_groessen.jpg", "p04_03_farbzonen.jpg"]
BG = (255, 247, 236)          # Hintergrund der Lookbook-Szene
# Prüffarben für das Farbzonen-Bild – gleiche Liste wie tools/godot/p04_lookbook.gd (PROOF_COLORS).
# Bewusst feste, klar verschiedene Farben: geprüft wird der Zonen-Shader, nicht die (wachsende) Palette.
PROOF_COLORS = ["#f4f1ea", "#ffd166", "#ff9f45", "#ef6f6c", "#c1547a", "#7a5ea8", "#4f7fc0", "#48b0a0", "#7cb342",
                "#a1887f"]

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
    pal = PROOF_COLORS

    def vec(hex_col):
        return [int(hex_col[i:i + 2], 16) / 255 for i in (1, 3, 5)]

    def cos(a, b):
        n = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(x * x for x in b))
        return sum(x * y for x, y in zip(a, b)) / n

    # Aufbau wie tools/godot/p04_lookbook.gd::_farbzonen: n Figuren im Abstand 70 cm, Füße bei y = 95 cm,
    # Kamera in der Mitte, Zoom = min(Breite / (n·70 + 40), Höhe / 210). Oberteil-Band aus der Schablone.
    n_fig = len(pal)
    h_img = im.size[1]
    zoom = min(w / (n_fig * 70.0 + 40.0), h_img / 210.0)
    kid = json.loads((ROOT / "data" / "characters" / "templates.json").read_text(encoding="utf-8"))["templates"]["kid"]
    to = kid["torso"]
    y0 = int(h_img / 2 + (95.0 - to["top"] + (to["top"] - to["bot"]) * 0.25) * zoom)
    y1 = int(h_img / 2 + (95.0 - to["bot"] - (to["top"] - to["bot"]) * 0.2) * zoom)
    half = max(2, int(to["w_top"] * 0.25 * zoom))
    means, hits = [], 0
    for i in range(n_fig):
        cx = int(w / 2 + (-(n_fig - 1) * 35.0 + i * 70.0) * zoom)          # Figuren-Mitte
        acc, n = [0.0, 0.0, 0.0], 0
        for x in range(cx - half, cx + half + 1):
            for y in range(y0, y1):                                        # Oberteil-Band
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
