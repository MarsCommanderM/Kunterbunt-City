#!/usr/bin/env python3
"""
P11: Programm-Symbol (Fenster, Desktop-Verknüpfung, Installer) aus den Stil-C-Bereichssymbolen:
buntes Rund-Quadrat (Regenbogen-Streifen = „kunterbunt“), darauf das Zuhause-Symbol, davor Riesenrad und Baum.
Ausgabe: assets/app/icon.png (1024 px), assets/app/icon.ico (16–256 px). Bit-gleich reproduzierbar.
Aufruf: python3 tools/make_app_icon.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "assets/ui/icons"
OUT = ROOT / "assets/app"
S = 1024
STRIPES = ["#e07a7a", "#f09a55", "#f6d98a", "#9fc3a0", "#6fc3e8", "#b9a6d6"]
INK = (90, 62, 48, 255)


def build() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((24, 24, S - 24, S - 24), radius=220, fill=255)
    bg = Image.new("RGBA", (S, S), "#fff7ea")
    d = ImageDraw.Draw(bg)
    band = (S - 48) / len(STRIPES)
    for k, c in enumerate(STRIPES):                          # Regenbogen-Hügel unten
        y0 = int(S * 0.62 + k * band * 0.3)
        d.ellipse((-S * 0.3, y0, S * 1.3, y0 + S * 0.9), fill=c)
    d.ellipse((S * 0.62, S * 0.1, S * 0.86, S * 0.34), fill="#f6d98a")      # Sonne
    img.paste(bg, (0, 0), mask)
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    for name, box in (("area_home", (190, 170, 834, 814)), ("area_fair", (40, 470, 420, 850)), ("area_zoo", (600, 470, 980, 850))):
        p = ICONS / f"{name}.png"
        if not p.exists():
            continue
        ic = Image.open(p).convert("RGBA").resize((box[2] - box[0], box[3] - box[1]), Image.LANCZOS)
        sh = Image.new("RGBA", ic.size, (60, 40, 30, 90))
        sh.putalpha(ic.getchannel("A").point(lambda a: a * 90 // 255))
        shadow.alpha_composite(sh, (box[0] + 14, box[1] + 18))
        img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
        shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        img.alpha_composite(ic, (box[0], box[1]))
    ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(ring).rounded_rectangle((24, 24, S - 24, S - 24), radius=220, outline=INK, width=22)
    img.alpha_composite(ring)
    return img


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    img = build()
    img.save(OUT / "icon.png", optimize=True)
    img.save(OUT / "icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"✅ {OUT / 'icon.png'} + icon.ico")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
