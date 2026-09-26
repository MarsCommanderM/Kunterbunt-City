#!/usr/bin/env python3
"""
Hand-Ebene für die echte Stil-C-Figur char_girl_01 (P03-T10 / Tech-Spec §4.2 „Finger über dem Item“).

Schneidet die Faust (Haut + Kontur, ohne gelben Ärmel) aus dem Einzelbild in eine eigene Ebene gleicher
Leinwandgröße. Im Spiel: Körper → gehaltenes Item → Hand-Ebene. Deterministisch, 0 €.
Ausgabe: assets/characters/sprite/char_girl_01{,_hand}.png + char_girl_01.json (Griffpunkt in px).
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "reference" / "sprites" / "char_girl_01.png"
OUT = ROOT / "assets" / "characters" / "sprite"
FIST_BOX = (329, 318, 387, 392)   # px im Original (per Raster-Zoom bestimmt)
GRIP_PX = (356, 357)              # Mitte der Faust = Griffpunkt


def is_sleeve(r: int, g: int, b: int) -> bool:
    """Gelb/Orange des Pullovers (nicht Haut, nicht Kontur)."""
    return r > 170 and g > 110 and b < 110 and (r - b) > 110


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.open(SRC).convert("RGBA")
    shutil.copy(SRC, OUT / "char_girl_01.png")
    hand = Image.new("RGBA", im.size, (0, 0, 0, 0))
    px, hp = im.load(), hand.load()
    x0, y0, x1, y1 = FIST_BOX
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if a > 0 and not is_sleeve(r, g, b):
                hp[x, y] = (r, g, b, a)
    # Ärmelrand links abschneiden (Übergang Bündchen → Faust)
    for y in range(y0, y1):
        for x in range(x0, x0 + 6):
            hp[x, y] = (0, 0, 0, 0)
    # Löcher (fälschlich als Ärmel erkannte Hautschatten) schließen: Maske schließen, Pixel aus dem Original
    mask = hand.getchannel("A").point(lambda v: 255 if v > 0 else 0)
    closed = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    cp = closed.load()
    for y in range(y0, y1):
        for x in range(x0 + 6, x1):
            if cp[x, y] and hp[x, y][3] == 0 and px[x, y][3] > 0:
                hp[x, y] = px[x, y]
    hand.save(OUT / "char_girl_01_hand.png", optimize=True)
    meta = {"source": "reference/sprites/char_girl_01.png", "size_px": list(im.size), "scale_ref": "char_child",
            "grip_px": list(GRIP_PX), "fist_box_px": list(FIST_BOX), "hand": "right (Bild rechts)"}
    (OUT / "char_girl_01.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"✅ Hand-Ebene: {OUT / 'char_girl_01_hand.png'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
