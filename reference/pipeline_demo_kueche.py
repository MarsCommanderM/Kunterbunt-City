#!/usr/bin/env python3
"""
Kunterbunt City – Asset-Pipeline Stil C  (0 €)
==============================================
KI-Bild (weißer Hintergrund)  ->  freistellen  ->  in Einzel-Items schneiden
->  Maßstab (cm) + Griffpunkt + Aufstellpunkt  ->  Sprites + items.json
->  Test-Szene: alles maßstabsgetreu in der Küche

Benötigt nur: pip install pillow numpy scipy   (alles kostenlos)
"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
SPR = os.path.join(HERE, "sprites"); os.makedirs(SPR, exist_ok=True)
sys.path.insert(0, os.path.join(HERE, "..", "..", "item_generator"))
def game_size(real_cm):
    """v2: ECHTE Größen – keine Vergrößerung mehr (Apfel bleibt 8 cm, Ball 30 cm)."""
    return real_cm

# ------------------------------------------------------------------ 1. Freistellen
def cutout(path, remove_holes=True, hole_min=500):
    """Weißen Hintergrund entfernen (Flood-Fill von den Rändern) + saubere Kanten."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    mn, mx = im.min(2), im.max(2)
    white = (mn > 232) & ((mx - mn) < 20)
    lab, n = ndi.label(white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    # eingeschlossene, rein weiße Löcher (z. B. im Tassenhenkel) ebenfalls entfernen
    sizes = ndi.sum(np.ones_like(mn), lab, index=np.arange(n + 1))
    means = ndi.mean(mn, lab, index=np.arange(n + 1))
    for i in range(1, n + 1 if remove_holes else 1):   # Figuren: AUS (Augenweiß bleibt!)
        if i not in border and sizes[i] > hole_min and means[i] > 250:
            bg |= lab == i
    fg = ~bg
    fg = ndi.binary_opening(fg, iterations=1)
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    a = np.asarray(alpha).astype(np.float32) / 255
    a = np.clip((a - 0.15) / 0.7, 0, 1)
    # Farb-Entmischung an den Kanten (kein weißer Rand)
    safe = np.maximum(a, 0.05)[..., None]
    rgb = np.clip((im - (1 - safe) * 255) / safe, 0, 255)
    rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
    return rgba, fg

def split(rgba, fg, min_area=1500):
    """Blatt in einzelne Objekte zerlegen (Lesereihenfolge: Zeile für Zeile)."""
    lab, n = ndi.label(ndi.binary_dilation(fg, iterations=8))
    objs = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        area = (lab[sl] == i).sum()
        if area < min_area:
            continue
        crop = rgba[sl].copy()
        crop[..., 3] = crop[..., 3] * (lab[sl] == i)
        objs.append((sl[0].start, sl[1].start, crop))
    # Zeilen über die vertikale Mitte bilden (neue Zeile bei großem Abstand), dann links -> rechts
    objs = [(o[0] + o[2].shape[0] / 2, o[1], o[2]) for o in objs]
    objs.sort(key=lambda o: o[0])
    rows, cur = [], [objs[0]]
    for o in objs[1:]:
        if o[0] - cur[-1][0] > 90:
            rows.append(cur); cur = [o]
        else:
            cur.append(o)
    rows.append(cur)
    ordered = [o for r in rows for o in sorted(r, key=lambda o: o[1])]
    return [Image.fromarray(o[2]) for o in ordered]

def trim(img):
    bb = img.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    return img.crop(bb)

# ------------------------------------------------------------------ 2. Katalog mit Maßen
# real_h: echte Höhe in cm · grip: Griffpunkt (0..1) · hold · angle · place
ITEMS_SHEET = [
    ("food_carrot",            20, (0.50, 0.36), "one_hand",  -20, "table"),
    ("food_apple_red",          8, (0.50, 0.62), "one_hand",    0, "table"),
    ("home_mug_pink_dots",     10, (0.90, 0.45), "one_hand",    0, "table"),
    ("home_cup_orange_dots",    9, (0.50, 0.55), "one_hand",    0, "table"),
    ("food_apple_green",        8, (0.50, 0.62), "one_hand",    0, "table"),
    ("food_egg",                6, (0.50, 0.55), "one_hand",    0, "table"),
    ("food_icecream_3",        17, (0.50, 0.80), "one_hand",    0, "table"),
    ("food_icecream_3b",       17, (0.50, 0.80), "one_hand",    0, "table"),
    ("school_book_blue_star",  22, (0.10, 0.50), "one_hand",    0, "shelf"),
    ("food_egg_chocolate",     10, (0.50, 0.55), "one_hand",    0, "table"),
    ("toy_beachball",          30, (0.50, 0.50), "two_hands",   0, "floor"),
    ("toy_teddy_brown",        30, (0.22, 0.62), "one_hand",    0, "floor"),
    ("toy_teddy_brown_b",      30, (0.22, 0.62), "one_hand",    0, "floor"),
    ("flower_tulip_red_pot",   30, (0.50, 0.82), "one_hand",    0, "table"),
    ("flower_tulip_yellow_pot",30, (0.50, 0.82), "one_hand",    0, "table"),
]
FURN_SHEET = [
    ("pet_dog_brown",  45, None, "none", 0, "floor"),
    ("home_table_wood", 75, None, "none", 0, "floor"),
    ("home_chair_mint", 90, None, "none", 0, "floor"),
]
CHAR_H = 125            # Kind = 125 cm (Figuren werden NICHT vergrößert)

def build_sprites():
    recs = {}
    for sheet, spec, is_char in [("raw_items.png", ITEMS_SHEET, False),
                                 ("raw_furniture_dog.png", FURN_SHEET, False)]:
        rgba, fg = cutout(os.path.join(HERE, sheet))
        parts = [trim(p) for p in split(rgba, fg)]
        assert len(parts) == len(spec), f"{sheet}: {len(parts)} Objekte gefunden, {len(spec)} erwartet"
        for img, (id_, real_h, grip, hold, ang, place) in zip(parts, spec):
            h_cm = game_size(real_h) if not id_.startswith("pet_") else real_h
            w_cm = h_cm * img.width / img.height
            img.save(os.path.join(SPR, id_ + ".png"))
            recs[id_] = dict(id=id_, size_cm=[round(w_cm, 1), round(h_cm, 1)], pivot=[0.5, 1.0],
                             grip=list(grip) if grip else None, hold=hold, hold_angle=ang,
                             placement=place, movable=True, sprite=f"sprites/{id_}.png")
    rgba, fg = cutout(os.path.join(HERE, "raw_girl.png"), remove_holes=False)
    girl = split(rgba, fg)
    girl = trim(max(girl, key=lambda i: i.width * i.height))
    girl.save(os.path.join(SPR, "char_girl_01.png"))
    recs["char_girl_01"] = dict(id="char_girl_01", size_cm=[round(CHAR_H * girl.width / girl.height, 1), CHAR_H],
                                pivot=[0.5, 1.0], hand_grip=None, sprite="sprites/char_girl_01.png")
    return recs

def find_fist(girl):
    """Handmitte der rechten (erhobenen) Hand finden: äußerster Hautpunkt rechts oben."""
    a = np.asarray(girl).astype(int)
    h, w = a.shape[:2]
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    skin = (al > 200) & (r > 200) & (g > 150) & (g < 215) & (b > 120) & (b < 190) & (r - b > 40)
    ys, xs = np.nonzero(skin[: int(h * 0.62), int(w * 0.62):])
    xs = xs + int(w * 0.62)
    sel = xs > xs.max() - 0.09 * w
    return float(xs[sel].mean()) / w, float(ys[sel].mean()) / h

# ------------------------------------------------------------------ 3. Test-Szene
BG = "raw_kitchen_bg.png"
SCALE_OUT = 2                     # Ausgabe in doppelter Auflösung
# Raum-Maßstab: Arbeitsplatte (90 cm) = 165 px -> 1,83 px/cm an der Rückwand.
# Tiefe: vorne max. +12 % (Regel S-07) – sonst wirkt ein Hund vorne größer als der Tisch.
DEPTH_MAX = 0.12
def px_per_cm(y):
    t = max(0.0, min(1.0, (y - 600) / 135))
    return 1.83 * (1 + DEPTH_MAX * t) * SCALE_OUT

def load(id_):
    return Image.open(os.path.join(SPR, id_ + ".png")).convert("RGBA")

def scaled(rec, y_floor):
    img = load(rec["id"]); s = px_per_cm(y_floor)
    w, h = rec["size_cm"][0] * s, rec["size_cm"][1] * s
    return img.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)

def drop_shadow(canvas, cx, y, w, strength=0.28):
    sh = Image.new("L", (int(w * 1.4) + 40, int(w * 0.35) + 40), 0)
    ImageDraw.Draw(sh).ellipse([20, 20, sh.width - 20, sh.height - 20], fill=int(255 * strength))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    layer = Image.new("RGBA", sh.size, (60, 35, 20, 0)); layer.putalpha(sh)
    canvas.alpha_composite(layer, (int(cx - sh.width / 2), int(y - sh.height / 2)))

def put(canvas, img, cx, base_y, shadow=True):
    if shadow:
        drop_shadow(canvas, cx, base_y, img.width * 0.8)
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(base_y - img.height)))

def compose(recs, fist):
    bg = Image.open(os.path.join(HERE, BG)).convert("RGBA")
    W, H = bg.width * SCALE_OUT, bg.height * SCALE_OUT
    c = bg.resize((W, H), Image.LANCZOS)
    S = SCALE_OUT
    R = recs
    # Gegenstände auf der Arbeitsplatte (hintere Ebene, y=600 -> Platte bei y≈432)
    counter_y = 434 * S; s_back = px_per_cm(600)
    for id_, x in [("school_book_blue_star", 640), ("home_cup_orange_dots", 692), ("food_apple_green", 878)]:
        rec = R[id_]; img = load(id_)
        img = img.resize((round(rec["size_cm"][0] * s_back), round(rec["size_cm"][1] * s_back)), Image.LANCZOS)
        put(c, img, x * S, counter_y, shadow=False)
    # Stuhl (etwas weiter hinten), Tisch davor
    yc = 652; chair = scaled(R["home_chair_mint"], yc); put(c, chair, 850 * S, yc * S)
    # Teddy sitzt AUF dem Stuhl: Aufstellpunkt = Sitzfläche (Slot "seat", 50 % der Stuhlhöhe)
    seat_y = yc * S - chair.height * 0.50
    put(c, scaled(R["toy_teddy_brown"], yc), 850 * S + chair.width * 0.12, seat_y + 6, shadow=False)
    yt = 664; table = scaled(R["home_table_wood"], yt); tx = 1010 * S; put(c, table, tx, yt * S)
    top_y = yt * S - table.height + table.height * 0.085      # Tischplatte (Aufstellfläche)
    for id_, dx in [("home_mug_pink_dots", -0.30), ("food_apple_red", -0.05), ("food_icecream_3", 0.12), ("flower_tulip_red_pot", 0.32)]:
        img = scaled(R[id_], yt); put(c, img, tx + dx * table.width, top_y + 4, shadow=False)
    # Ball vorne rechts, Teddy, Hund
    put(c, scaled(R["toy_beachball"], 728), 1165 * S, 728 * S)
    yd = 712; dog = scaled(R["pet_dog_brown"], yd); put(c, dog, 520 * S, yd * S)
    # Figur mit Karotte in der Hand (Karotte HINTER der Faust -> Finger liegen darüber)
    yg = 715; girl = scaled(R["char_girl_01"], yg)
    gx0 = int(370 * S - girl.width / 2); gy0 = int(yg * S - girl.height)
    hand = (gx0 + fist[0] * girl.width, gy0 + fist[1] * girl.height)
    car = R["food_carrot"]; cimg = scaled(car, yg)
    rot = cimg.rotate(-car["hold_angle"], resample=Image.BICUBIC, expand=True)
    # Griffpunkt nach Rotation berechnen
    gxp, gyp = car["grip"][0] * cimg.width - cimg.width / 2, car["grip"][1] * cimg.height - cimg.height / 2
    t = math.radians(car["hold_angle"])
    rx, ry = gxp * math.cos(t) - gyp * math.sin(t), gxp * math.sin(t) + gyp * math.cos(t)
    drop_shadow(c, 370 * S, yg * S, girl.width * 0.8)
    c.alpha_composite(rot, (int(hand[0] - (rot.width / 2 + rx)), int(hand[1] - (rot.height / 2 + ry))))
    c.alpha_composite(girl, (gx0, gy0))
    return c

def lineup(recs):
    """Alle Items + Figur auf einer Linie, gleicher Maßstab, mit Lineal."""
    s = 3.0; pad = 60; gy = 470
    order = ["char_girl_01", "pet_dog_brown", "food_egg", "food_apple_red", "home_mug_pink_dots", "food_egg_chocolate",
             "food_icecream_3", "food_carrot", "school_book_blue_star", "toy_beachball", "toy_teddy_brown",
             "flower_tulip_red_pot", "home_table_wood", "home_chair_mint"]
    imgs = [(k, load(k).resize((round(recs[k]["size_cm"][0] * s), round(recs[k]["size_cm"][1] * s)), Image.LANCZOS)) for k in order]
    W = pad * 2 + 40 + sum(max(i.width, 70) + 28 for _, i in imgs)
    c = Image.new("RGBA", (W, gy + 90), (255, 248, 236, 255))
    d = ImageDraw.Draw(c)
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
    fn = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    for cm in range(0, 141, 10):
        y = gy - cm * s
        d.line([(pad, y), (W - 20, y)], fill=(210, 200, 185) if cm % 50 else (180, 170, 155), width=1)
        if cm % 50 == 0:
            d.text((12, y - 9), f"{cm}", fill=(130, 130, 140), font=fn)
    d.rectangle([0, gy, W, gy + 90], fill=(232, 199, 154))
    x = pad + 40
    names = {"char_girl_01": "Kind", "pet_dog_brown": "Hund", "food_egg": "Ei", "food_apple_red": "Apfel",
             "home_mug_pink_dots": "Tasse", "food_egg_chocolate": "Schoko-Ei", "food_icecream_3": "Eis", "food_carrot": "Karotte",
             "school_book_blue_star": "Buch", "toy_beachball": "Ball", "toy_teddy_brown": "Teddy",
             "flower_tulip_red_pot": "Tulpe", "home_table_wood": "Tisch", "home_chair_mint": "Stuhl"}
    for k, im in imgs:
        slot = max(im.width, 70)
        cx = x + slot / 2
        drop_shadow(c, cx, gy, im.width * 0.8, 0.22)
        c.alpha_composite(im, (int(cx - im.width / 2), gy - im.height))
        t = names[k]; h = recs[k]["size_cm"][1]
        d.text((cx - d.textlength(t, font=fb) / 2, gy + 14), t, fill=(58, 63, 88), font=fb)
        tt = f"{h:.0f} cm"; d.text((cx - d.textlength(tt, font=fn) / 2, gy + 38), tt, fill=(110, 110, 125), font=fn)
        x += slot + 28
    return c

RULES = [  # (a, '<', b): Höhe von a muss kleiner sein als Höhe von b
    ("food_egg", "<", "food_apple_red"), ("food_apple_red", "<", "home_mug_pink_dots"),
    ("home_mug_pink_dots", "<", "food_carrot"), ("food_carrot", "<", "toy_beachball"),
    ("toy_beachball", "<", "pet_dog_brown"), ("pet_dog_brown", "<", "home_table_wood"),
    ("home_table_wood", "<", "home_chair_mint"), ("home_chair_mint", "<", "char_girl_01"),
    ("toy_teddy_brown", "<", "pet_dog_brown"),
]
def check_rules(recs):
    bad = [f"{a} ({recs[a]['size_cm'][1]} cm) ist NICHT kleiner als {b} ({recs[b]['size_cm'][1]} cm)"
           for a, op, b in RULES if not recs[a]["size_cm"][1] < recs[b]["size_cm"][1]]
    if bad:
        raise SystemExit("MASSSTAB-FEHLER:\n  " + "\n  ".join(bad))
    print(f"Maßstab-Regeln: {len(RULES)}/{len(RULES)} OK")

def main():
    recs = build_sprites()
    check_rules(recs)
    girl = load("char_girl_01")
    fist = find_fist(girl)
    recs["char_girl_01"]["hand_grip"] = [round(fist[0], 3), round(fist[1], 3)]
    with open(os.path.join(HERE, "items_stil_c.json"), "w", encoding="utf-8") as f:
        json.dump({"px_per_cm_reference": 4.0, "items": list(recs.values())}, f, indent=2, ensure_ascii=False)
    scene = compose(recs, fist)
    scene.convert("RGB").save(os.path.join(HERE, "..", "kueche_stil_c_raum_gesamt.png"))
    # Spiel-Kamera: zeigt ~300 cm Raumhöhe (Regel S-08), 16:9, horizontal scrollbar
    S = SCALE_OUT; vis_h = 300 * px_per_cm(640)          # px für 3 m
    y1 = 744 * S; y0 = y1 - vis_h; w = vis_h * 16 / 9; x0 = 228 * S
    cam = scene.crop((int(x0), int(y0), int(x0 + w), int(y1))).resize((1920, 1080), Image.LANCZOS)
    cam.convert("RGB").save(os.path.join(HERE, "..", "kueche_stil_c_massstab.png"))
    lineup(recs).convert("RGB").save(os.path.join(HERE, "..", "lineup_stil_c.png"))
    print("Hand bei", fist, "->", len(recs), "Sprites fertig")

if __name__ == "__main__":
    main()
