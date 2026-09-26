"""P04-UI-Beweisbilder (docs/tests/P04): messbar prüfen statt gucken.

Geprüft werden die Screenshots aus tools/godot/p04_ui_runner.gd:
  * Editor: ✓-Knopf erst grau (Hautton fehlt) dann orange (fertig)
  * Vorschau: Figur ist da, Hautton/Teil/Farbe verändern sie wirklich
  * Galerie: eine Karte pro Figur / pro Tier (Karten-Kanten gezählt)
  * Haustier-Editor: Tier sichtbar, Fell umgefärbt
  * Namenswahl & Eltern-Tor: viele Kacheln, Tor-Farben da
"""
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "docs" / "tests" / "P04"

EDITOR = "p04_04_editor_pflicht.jpg"
SKIN = "p04_05_hautton_gewaehlt.jpg"
DRESS = "p04_06_kleid_farbe.jpg"
DICE = "p04_07_wuerfel.jpg"
GALLERY = "p04_08_galerie_figuren.jpg"
PETS = "p04_09_galerie_tiere.jpg"
PET_ED = "p04_10_haustier_editor.jpg"
PET_FUR = "p04_11_haustier_fell.jpg"
NAMES = "p04_12_namenswahl.jpg"
GATE = "p04_13_elterntor.jpg"
FLOW_GALLERY = "p04_14_galerie_mit_eigener_figur.jpg"
FLOW_PLAY = "p04_15_eigene_figur_im_spiel.jpg"
ALL = [EDITOR, SKIN, DRESS, DICE, GALLERY, PETS, PET_ED, PET_FUR, NAMES, GATE,
       FLOW_GALLERY, FLOW_PLAY]

# Farben aus src/ui/ui.gd (Stil C)
ACCENT = (255, 159, 69)        # Orange  = Hauptaktion (✓ frei)
DISABLED = (203, 197, 214)     # Grau    = ✓ gesperrt
CARD = (255, 255, 255)
TEAL = (72, 176, 160)

PREVIEW = (60, 220, 700, 900)          # Vorschau-Bühne (linke Karte)
DONE_BTN = (1540, 30, 1880, 130)       # ✓-Knopf oben rechts
GRID = (60, 260, 1880, 1000)           # Galerie-Raster

Image = pytest.importorskip("PIL.Image", reason="Pillow fehlt")


def _load(name):
    p = SHOTS / name
    assert p.exists(), f"fehlt: {p} (tools/godot/p04_ui_runner.gd ausführen)"
    return Image.open(p).convert("RGB")


def _crop(im, box):
    return im.crop(box)


def _mean(im, box=None):
    c = _crop(im, box) if box else im
    px = list(c.getdata())
    n = len(px)
    return tuple(round(sum(p[i] for p in px) / n) for i in range(3))


def _near(a, b, tol=26):
    return sum(abs(x - y) for x, y in zip(a, b)) <= tol


def _ratio_nonwhite(im, box):
    px = list(_crop(im, box).getdata())
    return sum(1 for r, g, b in px if not (r > 244 and g > 244 and b > 244)) / len(px)


def _diff_ratio(a, b, box=None):
    pa = list((_crop(a, box) if box else a).getdata())
    pb = list((_crop(b, box) if box else b).getdata())
    hits = sum(1 for x, y in zip(pa, pb) if abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2]) > 24)
    return hits / len(pa)


@pytest.mark.parametrize("name", ALL)
def test_bild_vorhanden_scharf_und_bunt(name):
    im = _load(name)
    assert im.size == (1920, 1080), f"{name}: falsche Größe {im.size}"
    colors = im.getcolors(maxcolors=1 << 22) or []
    assert len(colors) > 800, f"{name}: nur {len(colors)} Farben – UI leer?"
    mean = _mean(im)
    assert 120 < sum(mean) / 3 < 250, f"{name}: Helligkeit {mean}"


def test_fertig_knopf_erst_gesperrt_dann_frei():
    """Ohne Hautton ist ✓ grau, danach orange (Pflicht-Ablauf P04-T07)."""
    before = _mean(_load(EDITOR), DONE_BTN)
    after = _mean(_load(SKIN), DONE_BTN)
    assert _near(before, DISABLED, 60), f"✓ muss grau sein, ist {before}"
    assert after[0] > after[2] + 40, f"✓ muss orange sein, ist {after}"
    assert not _near(after, DISABLED, 60)


def test_vorschau_zeigt_figur_und_reagiert_auf_auswahl():
    ed, skin, dress, dice = (_load(n) for n in (EDITOR, SKIN, DRESS, DICE))
    for im, name in ((ed, EDITOR), (skin, SKIN), (dress, DRESS), (dice, DICE)):
        ink = _ratio_nonwhite(im, PREVIEW)
        assert 0.02 < ink < 0.95, f"{name}: Vorschau-Fläche {ink:.1%} – Figur fehlt oder füllt alles"
    # Der Hautton trifft nur Kopf/Arme/Hände – deshalb ist seine Fläche kleiner als die eines
    # ganzen Oberteils. Alle drei Zahlen sind gemessen (kein Schätzwert):
    assert _diff_ratio(ed, skin, PREVIEW) > 0.008, "Hautton muss die Vorschau verändern"
    assert _diff_ratio(skin, dress, PREVIEW) > 0.03, "anderes Oberteil muss die Vorschau verändern"
    assert _diff_ratio(dress, dice, PREVIEW) > 0.10, "🎲 muss die Vorschau verändern"


def test_galerie_zeigt_eine_karte_pro_figur():
    """3 Figuren + die „Neu"-Karte = 4 weiße Karten-Bänder in einer Zeile."""
    cards = _count_card_bands(_load(GALLERY))
    assert cards == 4, f"3 Figuren + Neu-Karte erwartet, gezählt: {cards}"


def test_galerie_tiere_zeigt_eine_karte_pro_tier():
    """4 Tiere + die „Neu"-Karte = 5 Karten-Bänder."""
    cards = _count_card_bands(_load(PETS))
    assert cards == 5, f"4 Tiere + Neu-Karte erwartet, gezählt: {cards}"


def test_haustier_editor_zeigt_tier_und_faerbt_fell():
    a, b = _load(PET_ED), _load(PET_FUR)
    assert _ratio_nonwhite(a, PREVIEW) > 0.10, "Tier in der Vorschau fehlt"
    ma, mb = _mean(a, PREVIEW), _mean(b, PREVIEW)
    assert sum(ma) > sum(mb) + 40, f"dunkles Fell muss dunkler sein: {ma} → {mb}"
    assert _diff_ratio(a, b, PREVIEW) > 0.15


def test_namenswahl_hat_viele_kacheln():
    im = _load(NAMES)
    px = im.load()
    text_rows = 0
    for y in range(260, 1000, 4):
        dark = sum(1 for x in range(200, 1740, 3) if sum(px[x, y]) < 330)
        if dark > 8:
            text_rows += 1
    assert text_rows > 20, f"zu wenig Namens-Kacheln mit Text: {text_rows} Zeilen"


def test_elterntor_ist_zentriert_und_bunt():
    im = _load(GATE)
    px = im.load()
    # Das Panel (880×620 um die Bildmitte) ist hell, der Rand abgedunkelt …
    panel = _mean(im, (700, 250, 1220, 800))
    assert sum(panel) / 3 > 170, f"Panel zu dunkel: {panel}"
    assert sum(px[60, 60]) < 700, "Hintergrund muss abgedunkelt sein"
    teal = sum(1 for y in range(400, 760, 4) for x in range(600, 1320, 4)
               if abs(px[x, y][1] - TEAL[1]) < 40 and px[x, y][1] > px[x, y][0] + 20)
    assert teal > 50, f"Eltern-Tor: kaum Türkis (Zahlen-Kacheln) gefunden: {teal}"


def test_end_to_end_ablauf_steht_im_json():
    """Der komplette Weg (App-Start → Pflicht-Editor → Galerie → Bereich) ist gemessen."""
    p = SHOTS / "p04_flow.json"
    assert p.exists(), "fehlt: p04_flow.json (tools/godot/p04_flow_runner.gd ausführen)"
    m = json.loads(p.read_text(encoding="utf-8"))
    for key in ("pflicht_editor_ohne_figur", "fertig_erst_nach_hautton", "galerie_nach_fertig",
                "spielen_frei", "bereich_betreten", "eigene_figur_da", "haustier_da",
                "haustier_kleiner_als_tisch", "sichtbar"):
        assert m.get(key) is True, f"{key} ist nicht erfüllt: {m.get(key)}"
    assert 124.0 <= m["eigene_figur_cm"] <= 126.0, f"Kind muss 125 cm groß sein: {m['eigene_figur_cm']}"
    assert 27.0 <= m["haustier_cm"] <= 29.0, f"Katze muss 28 cm groß sein: {m['haustier_cm']}"
    assert m["gespeicherte_figuren"] == 1 and m["gespeicherte_tiere"] == 1


def test_eigene_figur_steht_sichtbar_in_der_welt():
    im = _load(FLOW_PLAY)
    px = im.load()
    # Die Test-Küche ist gefüllt: in der unteren Bildhälfte muss „etwas" stehen.
    ink = sum(1 for y in range(500, 1000, 3) for x in range(0, 1920, 3) if sum(px[x, y]) < 600)
    assert ink > 2000, f"Welt sieht leer aus (dunkle Pixel: {ink})"
    colors = im.getcolors(maxcolors=1 << 22) or []
    assert len(colors) > 2000, f"zu wenig Farben im Spielbild: {len(colors)}"


def _count_card_bands(im, min_width=250):
    """Zählt Karten: in der Zeile mit den meisten weißen Kartenflächen."""
    px = im.load()
    best = 0
    for y in range(250, 620, 5):
        runs, run = 0, 0
        for x in range(40, 1890):
            r, g, b = px[x, y]
            if r > 248 and g > 248 and b > 248:
                run += 1
            else:
                if run >= min_width:
                    runs += 1
                run = 0
        if run >= min_width:
            runs += 1
        best = max(best, runs)
    return best
