#!/usr/bin/env python3
"""P04/P05: Icon-Set fuer die UI (Stil C, Premium Vektor).

Alle Icons entstehen hier rein rechnerisch (PIL, 4x uebersampelt) und landen als
128x128-PNG mit Alpha in assets/ui/icons/. Farbe: ein dunkles Violett (#2b2440),
damit die Icons per `modulate` einfaerbbar bleiben. Kostenlos, keine externen Assets.

Aufruf:  python3 tools/make_ui_icons.py
"""
from PIL import Image, ImageDraw
import math
import os

def maxf(a, b):
    return a if a > b else b

SS = 4                    # Uebersammlung (Kanten schoen rund)
N = 128                    # Icon-Groesse in px
OUT = "assets/ui/icons"
INK = (43, 36, 64, 255)    # #2b2440
W = 11.0                   # Standard-Linienstaerke (im 128er Raster)
PAD = 14.0


class Ico:
    """Zeichenflaeche im 128er Raster; alles wird am Ende verkleinert."""

    def __init__(self):
        self.im = Image.new("RGBA", (N * SS, N * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.ink = INK

    def s(self, *vals):
        return tuple(v * SS for v in vals)

    # ---------------- Grundformen ----------------
    def line(self, pts, w=W, ink=None):
        p = [(x * SS, y * SS) for x, y in pts]
        self.d.line(p, fill=ink or self.ink, width=int(w * SS), joint="curve")
        for x, y in pts:                      # runde Enden
            r = w * SS * 0.5
            self.d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=ink or self.ink)

    def poly(self, pts, ink=None):
        self.d.polygon([(x * SS, y * SS) for x, y in pts], fill=ink or self.ink)

    def rrect(self, box, r, ink=None, outline=0.0, w=W):
        x0, y0, x1, y1 = [v * SS for v in box]
        rr = r * SS
        if outline > 0.0:
            self.d.rounded_rectangle([x0, y0, x1, y1], radius=rr, outline=ink or self.ink,
                                     width=int(outline * SS))
        else:
            self.d.rounded_rectangle([x0, y0, x1, y1], radius=rr, fill=ink or self.ink)

    def circle(self, cx, cy, r, ink=None, outline=0.0, w=W):
        rr = r * SS
        box = [(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS]
        if outline > 0.0:
            self.d.ellipse(box, outline=ink or self.ink, width=int(outline * SS))
        else:
            self.d.ellipse(box, fill=ink or self.ink)

    def ellipse(self, cx, cy, rx, ry, ink=None):
        self.d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS],
                       fill=ink or self.ink)

    def dot(self, cx, cy, r, ink=None):
        self.circle(cx, cy, r, ink)

    def arc(self, box, a0, a1, w=W, ink=None):
        b = [v * SS for v in box]
        self.d.arc(b, a0, a1, fill=ink or self.ink, width=int(w * SS))
        # runde Enden des Bogens
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        rx, ry = (b[2] - b[0]) / 2, (b[3] - b[1]) / 2
        for a in (a0, a1):
            x = cx + rx * math.cos(math.radians(a))
            y = cy + ry * math.sin(math.radians(a))
            r = w * SS * 0.5
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=ink or self.ink)

    def ring(self, box, r, w=W, ink=None):
        """Rahmen: gefuellte Form minus innere Form → dicke Kontur zum Einfaerben."""
        x0, y0, x1, y1 = box
        self.rrect(box, r, ink)
        self.cut(lambda: self.rrect((x0 + w, y0 + w, x1 - w, y1 - w), maxf(1.0, r - w), ink))

    def ring_circle(self, cx, cy, r, w=W, ink=None):
        self.circle(cx, cy, r, ink)
        self.cut(lambda: self.circle(cx, cy, r - w, ink))

    def cut(self, fn):
        """Alles, was fn zeichnet, wieder herausschneiden (Loescher)."""
        layer = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        save_d, save_ink = self.d, self.ink
        self.d = ImageDraw.Draw(layer)
        self.ink = (0, 0, 0, 255)
        fn()
        self.d = save_d
        self.ink = save_ink
        self.im = Image.alpha_composite(self.im, Image.eval(layer, lambda v: v))
        # Alpha dort entfernen, wo die Ebene deckt
        a = self.im.split()[3]
        la = layer.split()[3]
        from PIL import ImageChops
        self.im.putalpha(ImageChops.subtract(a, la))

    def save(self, name):
        self.im.resize((N, N), Image.LANCZOS).save(os.path.join(OUT, name + ".png"))


# ------------------------------------------------------------------ Icons
def shirt(i):
    i.poly([(34, 26), (58, 20), (64, 34), (70, 20), (94, 26), (104, 48), (92, 60), (86, 54),
            (86, 106), (42, 106), (42, 54), (36, 60), (24, 48)])


def pants(i):
    i.poly([(36, 22), (92, 22), (96, 104), (74, 104), (68, 62), (60, 62), (54, 104), (32, 104)])
    i.cut(lambda: i.poly([(56, 22), (72, 22), (70, 40), (58, 40)]))


def shoe(i):
    i.poly([(20, 88), (22, 60), (38, 56), (56, 66), (74, 52), (104, 62), (108, 78), (108, 90),
            (20, 90)])
    i.cut(lambda: i.rrect((24, 84, 106, 94), 5))
    i.line([(100, 66), (104, 76)], 7)


def hair(i):
    for k, dx in enumerate((0, 14, 28)):
        i.arc((24 + dx, 18 + k * 6, 96 + dx, 100 + k * 6), 200, 340, 10)
    i.poly([(30, 30), (44, 30), (40, 100), (26, 100)])


def eye(i):
    for cx in (44, 84):
        i.circle(cx, 64, 26, outline=11)
    i.dot(44, 64, 11)
    i.dot(84, 64, 11)


def mouth(i):
    i.arc((28, 34, 100, 100), 20, 160, 13)
    i.line([(28, 58), (100, 58)], 11)


def bow(i):
    i.poly([(64, 64), (18, 34), (18, 94)])
    i.poly([(64, 64), (110, 34), (110, 94)])
    i.circle(64, 64, 15)


def glasses(i):
    i.circle(38, 66, 26, outline=11)
    i.circle(90, 66, 26, outline=11)
    i.line([(64, 60), (64, 60)], 0.1)
    i.arc((56, 48, 72, 66), 190, 350, 9)
    i.line([(12, 56), (30, 56)], 9)
    i.line([(98, 56), (116, 56)], 9)


def person(i):
    i.circle(64, 32, 20)
    i.poly([(64, 56), (98, 70), (94, 116), (34, 116), (30, 70)])


def hand(i):
    i.rrect((40, 26, 88, 108), 22)
    i.poly([(24, 56), (44, 50), (46, 74)])
    i.cut(lambda: i.rrect((58, 44, 74, 96), 8))


def paw(i):
    i.ellipse(64, 82, 28, 24)
    for cx, cy, r in ((34, 52, 13), (54, 34, 14), (76, 34, 14), (96, 54, 13)):
        i.ellipse(cx, cy, r, r)


def dice(i):
    i.rrect((18, 18, 110, 110), 24, outline=11)
    for cx, cy in ((44, 44), (86, 44), (64, 65), (44, 86), (86, 86)):
        i.dot(cx, cy, 9)


def check(i):
    i.line([(26, 66), (54, 94), (104, 34)], 17)


def close(i):
    i.line([(32, 32), (96, 96)], 15)
    i.line([(96, 32), (32, 96)], 15)


def back(i):
    i.line([(78, 26), (40, 64), (78, 102)], 16)


def forward(i):
    i.line([(50, 26), (88, 64), (50, 102)], 16)


def trash(i):
    i.rrect((30, 44, 98, 112), 10, outline=11)
    i.line([(22, 40), (106, 40)], 11)
    i.rrect((52, 28, 76, 42), 6)
    for x in (50, 64, 78):
        i.line([(x, 60), (x, 98)], 7)


def copy(i):
    i.rrect((20, 20, 78, 78), 14, outline=11)
    i.rrect((50, 50, 108, 108), 14, outline=11)


def folder(i):
    i.poly([(16, 34), (56, 34), (66, 46), (112, 46), (112, 106), (16, 106)])
    i.cut(lambda: i.poly([(28, 52), (100, 52), (100, 94), (28, 94)]))


def plus(i):
    i.line([(64, 26), (64, 102)], 16)
    i.line([(26, 64), (102, 64)], 16)


def gear(i):
    i.circle(64, 64, 30)
    for a in range(0, 360, 45):
        x = 64 + 42 * math.cos(math.radians(a))
        y = 64 + 42 * math.sin(math.radians(a))
        i.dot(x, y, 12)
    i.cut(lambda: i.circle(64, 64, 14))


def map(i):
    i.poly([(16, 32), (52, 20), (88, 32), (112, 22), (112, 96), (76, 108), (40, 96), (16, 106)])
    i.cut(lambda: (i.line([(52, 20), (52, 108)], 8), i.line([(88, 32), (88, 100)], 8)))


def heart(i):
    i.circle(46, 52, 24)
    i.circle(82, 52, 24)
    i.poly([(24, 58), (104, 58), (64, 108)])


def star(i):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        r = 52 if k % 2 == 0 else 22
        pts.append((64 + r * math.cos(a), 64 + r * math.sin(a)))
    i.poly(pts)


def speaker(i):
    i.poly([(24, 52), (46, 52), (70, 28), (70, 100), (46, 76), (24, 76)])
    i.arc((74, 40, 100, 88), 300, 60, 9)
    i.arc((86, 28, 118, 100), 300, 60, 9)


def mute(i):
    i.poly([(24, 52), (46, 52), (70, 28), (70, 100), (46, 76), (24, 76)])
    i.line([(84, 48), (112, 80)], 11)
    i.line([(112, 48), (84, 80)], 11)


def palette(i):
    i.circle(64, 60, 44)
    i.cut(lambda: (i.dot(44, 44, 11), i.dot(84, 44, 11), i.dot(38, 74, 11),
                   i.dot(64, 76, 11), i.dot(90, 74, 11)))


def bone(i):
    i.rrect((34, 56, 94, 74), 9)
    for xs, ys in (((24, 44), (24, 86)), ((104, 44), (104, 86))):
        for (x, y) in (xs, ys):
            i.circle(x, y, 14)


def moon(i):
    i.circle(72, 60, 42)
    i.cut(lambda: i.circle(50, 48, 38))


def magnifier(i):
    i.circle(56, 56, 30, outline=12)
    i.line([(78, 78), (106, 106)], 15)


def ball(i):
    i.circle(64, 64, 42, outline=11)
    i.cut(lambda: i.circle(64, 64, 34))
    i.poly([(64, 30), (86, 50), (78, 78), (50, 78), (42, 50)])


def wall_peek(i):          # scheu
    i.rrect((24, 74, 104, 104), 10)
    i.cut(lambda: (i.dot(46, 60, 12), i.dot(82, 60, 12)))
    i.line([(24, 74), (104, 74)], 9)


def lock(i):
    i.rrect((30, 58, 98, 112), 14)
    i.arc((44, 22, 84, 80), 180, 360, 12)
    i.cut(lambda: (i.circle(64, 80, 9), i.rrect((60, 82, 68, 100), 4)))


def home(i):
    i.poly([(64, 18), (114, 60), (102, 60), (102, 108), (26, 108), (26, 60), (14, 60)])
    i.cut(lambda: i.rrect((48, 74, 80, 108), 6))


def brush(i):
    i.poly([(30, 98), (58, 70), (74, 86), (46, 114)])
    i.rrect((58, 18, 96, 74), 12, outline=11)
    i.cut(lambda: i.line([(66, 62), (88, 40)], 9))


def undo(i):
    i.arc((26, 26, 102, 102), 40, 320, 13)
    i.poly([(24, 30), (24, 66), (58, 44)])


def backpack(i):
    i.rrect((28, 46, 100, 112), 22)
    i.arc((48, 20, 80, 66), 180, 360, 12)
    i.cut(lambda: i.rrect((44, 76, 84, 98), 10))


def album(i):
    i.rrect((16, 26, 112, 102), 12)
    i.cut(lambda: i.rrect((28, 38, 100, 90), 8))
    i.circle(46, 56, 12)
    i.poly([(36, 86), (58, 64), (72, 80), (86, 66), (96, 86)])


def pencil(i):
    i.poly([(28, 100), (40, 112), (52, 100), (100, 52), (88, 40), (40, 88)])
    i.poly([(84, 36), (100, 52), (92, 60), (76, 44)])
    i.cut(lambda: i.line([(34, 94), (48, 108)], 6))


def name_tag(i):
    i.rrect((16, 44, 84, 88), 12, outline=11)
    i.poly([(84, 56), (114, 40), (114, 92), (84, 74)])
    i.cut(lambda: (i.line([(30, 60), (66, 60)], 8), i.line([(30, 74), (54, 74)], 8)))


def dog(i):
    i.ellipse(64, 72, 30, 26)
    i.circle(64, 36, 22)
    i.poly([(34, 26), (44, 12), (54, 26)])
    i.poly([(74, 26), (84, 12), (94, 26)])
    i.cut(lambda: (i.dot(56, 38, 5), i.dot(72, 38, 5), i.ellipse(64, 50, 8, 6)))


def cat(i):
    i.ellipse(64, 74, 30, 24)
    i.circle(64, 40, 22)
    i.poly([(42, 24), (46, 4), (62, 20)])
    i.poly([(86, 24), (82, 4), (66, 20)])
    i.cut(lambda: (i.dot(55, 40, 5), i.dot(73, 40, 5)))


def bunny(i):
    i.ellipse(64, 80, 26, 22)
    i.circle(64, 44, 20)
    i.ellipse(50, 16, 9, 20)
    i.ellipse(78, 16, 9, 20)
    i.cut(lambda: (i.dot(57, 44, 5), i.dot(71, 44, 5), i.ellipse(56, 12, 5, 13),
                   i.ellipse(72, 12, 5, 13)))


def bird(i):
    i.ellipse(58, 70, 28, 24)
    i.circle(76, 40, 18)
    i.poly([(92, 40), (108, 48), (92, 52)])
    i.cut(lambda: i.dot(82, 36, 5))
    i.poly([(38, 62), (20, 78), (42, 78)])


def fish(i):
    i.ellipse(58, 64, 34, 22)
    i.poly([(92, 64), (116, 42), (116, 86)])
    i.cut(lambda: i.dot(40, 58, 6))


def hamster(i):
    i.ellipse(64, 68, 32, 28)
    i.circle(40, 40, 15)
    i.circle(88, 40, 15)
    i.cut(lambda: (i.dot(64, 74, 6), i.arc((50, 58, 78, 82), 20, 160, 7)))


def house_area(i):
    i.poly([(64, 16), (114, 56), (114, 110), (14, 110), (14, 56)])
    i.cut(lambda: (i.rrect((46, 74, 82, 110), 6), i.poly([(24, 44), (104, 44), (104, 56), (24, 56)])))


def hospital(i):
    i.rrect((20, 22, 108, 108), 16)
    i.cut(lambda: (i.rrect((54, 40, 74, 90), 6), i.rrect((40, 54, 88, 76), 6)))


def school(i):
    i.poly([(64, 16), (110, 44), (110, 62), (18, 62), (18, 44)])
    i.rrect((26, 62, 102, 110), 6, outline=11)
    i.cut(lambda: (i.rrect((46, 74, 62, 96), 4), i.rrect((70, 74, 86, 96), 4)))


def pool(i):
    i.arc((20, 30, 108, 90), 0, 180, 12)
    for k in range(3):
        y = 96 + k * 6
        i.arc((24 + k * 8, y - 14, 104 - k * 8, y + 14), 0, 180, 8)


def playground(i):
    i.line([(24, 104), (104, 104)], 11)
    i.line([(36, 104), (36, 30)], 11)
    i.line([(92, 104), (92, 30)], 11)
    i.line([(36, 30), (92, 30)], 11)
    i.line([(52, 30), (52, 62)], 8)
    i.line([(76, 30), (76, 62)], 8)
    i.line([(52, 62), (76, 62)], 6)


def ferris(i):
    i.circle(64, 58, 42, outline=11)
    for a in range(0, 360, 45):
        x = 64 + 42 * math.cos(math.radians(a))
        y = 58 + 42 * math.sin(math.radians(a))
        i.dot(x, y, 8)
    i.poly([(46, 104), (82, 104), (64, 74)])


def shop(i):
    i.rrect((20, 44, 108, 110), 10, outline=11)
    i.poly([(14, 44), (114, 44), (104, 20), (24, 20)])
    i.cut(lambda: i.rrect((44, 70, 84, 100), 6))


def sports(i):
    i.circle(64, 64, 44, outline=11)
    i.cut(lambda: i.circle(64, 64, 36))
    i.poly([(28, 64), (100, 64), (64, 28), (64, 100)])


def ice(i):
    i.rrect((24, 74, 104, 88), 8)
    i.line([(64, 78), (64, 22)], 11)
    i.poly([(64, 22), (92, 40), (78, 52), (64, 40), (50, 52), (36, 40)])


def flower(i):
    for a in range(0, 360, 72):
        x = 64 + 26 * math.cos(math.radians(a))
        y = 44 + 26 * math.sin(math.radians(a))
        i.circle(x, y, 16)
    i.dot(64, 44, 13)
    i.line([(64, 62), (64, 112)], 10)
    i.ellipse(88, 88, 16, 9)


def zoo(i):
    i.circle(64, 40, 26)
    for a in range(0, 360, 60):
        x = 64 + 34 * math.cos(math.radians(a))
        y = 40 + 34 * math.sin(math.radians(a))
        i.dot(x, y, 9)
    i.cut(lambda: (i.dot(54, 38, 5), i.dot(74, 38, 5), i.ellipse(64, 54, 10, 7)))
    i.poly([(34, 108), (94, 108), (88, 84), (40, 84)])


def wrench(i):
    i.line([(36, 92), (92, 36)], 17)
    i.circle(94, 30, 20)
    i.cut(lambda: i.circle(94, 30, 10))


def car(i):
    i.rrect((16, 62, 112, 100), 14)
    i.poly([(34, 62), (48, 40), (82, 40), (96, 62)])
    i.cut(lambda: (i.rrect((44, 46, 84, 60), 8), i.circle(40, 100, 12), i.circle(88, 100, 12)))


def gift(i):
    i.rrect((20, 54, 108, 110), 8)
    i.rrect((16, 34, 112, 62), 8)
    i.cut(lambda: (i.rrect((56, 34, 72, 110), 6), i.ellipse(50, 22, 14, 12),
                   i.ellipse(78, 22, 14, 12)))


def camera_icon(i):
    i.rrect((16, 38, 112, 98), 14, outline=11)
    i.poly([(52, 38), (64, 24), (76, 38)])
    i.cut(lambda: i.circle(64, 68, 24))
    i.circle(64, 68, 14)


def music(i):
    i.dot(38, 94, 14)
    i.dot(90, 82, 14)
    i.line([(50, 94), (50, 26)], 10)
    i.line([(102, 82), (102, 14)], 10)
    i.line([(50, 26), (102, 14)], 10)


def sun(i):
    i.dot(64, 64, 26)
    for a in range(0, 360, 45):
        x0 = 64 + 36 * math.cos(math.radians(a))
        y0 = 64 + 36 * math.sin(math.radians(a))
        x1 = 64 + 52 * math.cos(math.radians(a))
        y1 = 64 + 52 * math.sin(math.radians(a))
        i.line([(x0, y0), (x1, y1)], 9)


ICONS = {
    "shirt": shirt, "pants": pants, "shoe": shoe, "hair": hair, "eye": eye, "mouth": mouth,
    "bow": bow, "glasses": glasses, "person": person, "hand": hand, "paw": paw, "dice": dice,
    "check": check, "close": close, "back": back, "forward": forward, "trash": trash,
    "copy": copy, "folder": folder, "plus": plus, "gear": gear, "map": map, "heart": heart,
    "star": star, "speaker": speaker, "mute": mute, "palette": palette, "bone": bone,
    "moon": moon, "magnifier": magnifier, "ball": ball, "peek": wall_peek, "lock": lock,
    "home": home, "brush": brush, "undo": undo, "backpack": backpack, "album": album,
    "pencil": pencil, "nametag": name_tag,
    "dog": dog, "cat": cat, "bunny": bunny, "bird": bird, "fish": fish, "hamster": hamster,
    "area_home": house_area, "area_hospital": hospital, "area_school": school,
    "area_pool": pool, "area_playground": playground, "area_fair": ferris, "area_shop": shop,
    "area_sports": sports, "area_ice": ice, "area_flower": flower, "area_zoo": zoo,
    "area_workshop": wrench, "car": car, "gift": gift, "camera": camera_icon,
    "music": music, "sun": sun,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in ICONS.items():
        i = Ico()
        fn(i)
        i.save(name)
    print("Icons: %d → %s" % (len(ICONS), OUT))


if __name__ == "__main__":
    main()
