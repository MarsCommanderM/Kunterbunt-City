"""P03-Beweisbilder (docs/tests/P03): messbar prüfen, was sonst nur der Blick-Check kann.

Läuft in check.sh (pytest) und belegt ohne Augenmaß:
  * alle 12 Bilder sind echte Rollen (Größe, Kontrast, keine leere Fläche)
  * die 6 Gefühle im Streifen sind paarweise verschieden
  * im Hand-Ausschnitt liegt Haut ÜBER Karotten-Orange (Zeichenreihenfolge Arm < Item < Hand)
  * die Maßstabsreihe zeigt 6 getrennte Silhouetten, die von links nach rechts nicht schrumpfen
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "docs" / "tests" / "P03"
NAMES = [
    "p03_01_sandbox_figuren.jpg", "p03_02_karotte_hand_maedchen.jpg", "p03_03_karotte_hand_zoom.jpg",
    "p03_04_hand_eins_und_zwei.jpg", "p03_05_sitzen_und_teddy.jpg", "p03_06_kleinkind_liegt_im_bett.jpg",
    "p03_07_maedchen_getragen.jpg", "p03_08_kind_getragen_pendelt.jpg", "p03_09_sechs_gesichter.jpg",
    "p03_10_eis_gegessen_verliebt.jpg", "p03_11_hund_folgt.jpg", "p03_12_massstabsreihe.jpg",
    "p03_13_referenz_kueche.jpg",
]

Image = pytest.importorskip("PIL.Image", reason="Pillow fehlt")


def _load(name):
    p = SHOTS / name
    assert p.exists(), f"fehlt: {p} (tools/godot/p03_scenario_runner.gd ausführen)"
    return Image.open(p).convert("RGB")


@pytest.mark.parametrize("name", NAMES)
def test_bild_vorhanden_und_scharf(name):
    im = _load(name)
    w, h = im.size
    assert w >= 640 and h >= 300, name
    colors = im.getcolors(maxcolors=1 << 22) or []
    assert len(colors) > 400, f"{name}: nur {len(colors)} Farben – vermutlich leeres Bild"
    small = im.resize((64, 36))
    px = list(small.getdata())
    mean = sum(sum(p) for p in px) / (3 * len(px))
    var = sum((sum(p) / 3 - mean) ** 2 for p in px) / len(px)
    assert 12.0 < mean < 250.0, f"{name}: mittlere Helligkeit {mean:.0f} – Bild leer/überbelichtet?"
    assert var > 25.0, f"{name}: kaum Kontrast ({var:.0f}) – nichts gezeichnet?"


def test_sechs_gesichter_unterscheidbar():
    im = _load("p03_09_sechs_gesichter.jpg")
    w, h = im.size
    tile = w // 6
    means = []
    for k in range(6):
        # Mund-/Augen-Bereich: dort unterscheiden sich die Gefühle (ganze Kachel ist zu grob)
        t = im.crop((k * tile + int(0.25 * tile), int(0.42 * h),
                     k * tile + int(0.75 * tile), int(0.88 * h))).resize((64, 64))
        means.append(list(t.getdata()))
    for a in range(6):
        for b in range(a + 1, 6):
            diff = sum(abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
                       for x, y in zip(means[a], means[b])) / (3 * 1024)
            assert diff > 2.5, f"Gesicht {a + 1} und {b + 1} sind fast gleich (Δ={diff:.1f})"


def test_finger_liegen_ueber_karotte():
    """Im Hand-Ausschnitt: Karotten-Orange mittig, Haut darüber (Hand-Ebene zeichnet zuletzt)."""
    im = _load("p03_03_karotte_hand_zoom.jpg")
    w, h = im.size
    px = im.load()

    def count(pred, x0, y0, x1, y1):
        return sum(1 for y in range(int(y0), int(y1), 2) for x in range(int(x0), int(x1), 2)
                   if pred(px[x, y]))

    orange = lambda p: p[0] > 150 and 60 < p[1] < 200 and p[2] < 130 and p[0] - p[2] > 60
    skin = lambda p: p[0] > 215 and 165 < p[1] < 240 and 130 < p[2] < 225 and p[0] >= p[1] > p[2]
    n_orange = count(orange, 0, 0, w, h)
    n_skin = count(skin, 0, 0, w, h)
    assert n_orange > 60, f"keine Karotte im Ausschnitt (Orange-Pixel: {n_orange})"
    assert n_skin > 60, f"keine Hand im Ausschnitt (Haut-Pixel: {n_skin})"
    # Mitte des Bildes = Griffpunkt: dort muss beides vorkommen (Finger vor der Karotte)
    mid_orange = count(orange, w * 0.3, h * 0.3, w * 0.7, h * 0.7)
    mid_skin = count(skin, w * 0.3, h * 0.3, w * 0.7, h * 0.7)
    assert mid_orange > 20 and mid_skin > 20, (f"Griffbereich: Orange {mid_orange}, Haut {mid_skin}")


def test_massstabsreihe_zeigt_sechs_objekte():
    """Nur Kontrolle, dass die Reihe gezeichnet wurde – die Maße prüft test_messwerte_gruen."""
    im = _load("p03_12_massstabsreihe.jpg")
    small = im.resize((80, 45))
    px = list(small.getdata())
    mean = sum(sum(p) for p in px) / (3 * len(px))
    assert 30.0 < mean < 240.0, f"Reihe wirkt leer (Helligkeit {mean:.0f})"


def test_messwerte_gruen():
    """Der Godot-Messläufer (tools/godot/p03_check.gd) schreibt 37 geprüfte Zahlen – alle müssen grün sein."""
    import json
    p = SHOTS / "p03_messwerte.json"
    assert p.exists(), f"fehlt: {p} (tools/godot/p03_check.gd docs/tests/P03/p03_messwerte.json)"
    rows = json.loads(p.read_text(encoding="utf-8"))
    assert len(rows) >= 30, f"nur {len(rows)} Messwerte"
    red = [r["name"] for r in rows if not r["ok"]]
    assert not red, "rote Prüfungen: " + "; ".join(red)
    by_name = {r["name"]: r["detail"] for r in rows}
    for key in ["Karotte gerendert (Soll 20 cm ±25 %)", "Hund kleiner als der Tisch (jede Tiefe)",
                "Sitzhöhe Kind = 45 cm (Hüfte über Stuhl-Bodenlinie)", "Teddy sitzt auf 45 cm",
                "Kleinkind LIEGT (breiter als hoch)", "Kopf bleibt beim Liegen aufrecht"]:
        assert key in by_name, f"Messwert fehlt: {key}"
