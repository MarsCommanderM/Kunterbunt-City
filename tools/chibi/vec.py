"""
Vektor-Zeichenkern für die Figuren (Phase 04b) – nur Pillow + NumPy + SciPy, 0 €, reproduzierbar.

Koordinaten in **cm**, y nach **oben** (Boden = 0). Intern 4× überabgetastet, am Ende auf px/cm verkleinert.

Farbkodierung (Shader `zone_tint.gdshader`):
    R/G/B = Gewicht der Farbzone 1/2/3, Rest (1 − R − G − B) = Tinte (dunkle Kontur).
    → Kontur = (0,0,0), volle Zone 1 = (1,0,0), Schatten auf Zone 1 = (0.86,0,0) usw.
Jedes Teil bekommt automatisch eine gleichmäßig dicke Außenkontur (Abstands-Transformation).
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

SS = 4
Pt = tuple[float, float]


# ------------------------------------------------------------------ Pfade
def bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 24) -> list[Pt]:
    """Kubische Bézier-Kurve als Punktliste (ohne Endpunkt)."""
    out = []
    for i in range(n):
        t = i / n
        a = (1 - t) ** 3
        b = 3 * (1 - t) ** 2 * t
        c = 3 * (1 - t) * t * t
        d = t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def path(start: Pt, *segs: Sequence[Pt], n: int = 24) -> list[Pt]:
    """Geschlossener Pfad: start, dann Segmente – 1 Punkt = Linie, 3 Punkte = Bézier (c1, c2, ende)."""
    pts: list[Pt] = []
    cur = start
    for s in segs:
        if len(s) == 1:
            pts.append(cur)
            cur = s[0]
        else:
            pts.extend(bez(cur, s[0], s[1], s[2], n))
            cur = s[2]
    pts.append(cur)
    return pts


def blob(cx: float, cy: float, rx: float, ry: float, n: int = 64, squish: float = 0.0, top: float = 1.0) -> list[Pt]:
    """Weiche Ellipse. squish > 0 macht den unteren Teil breiter (Kinderkopf), top skaliert die obere Hälfte."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = math.cos(a), math.sin(a)
        k = 1.0 + squish * (-y) * (1 - abs(y)) * 0.6
        pts.append((cx + rx * x * k, cy + ry * y * (top if y > 0 else 1.0)))
    return pts


def mirror(pts: Iterable[Pt], cx: float) -> list[Pt]:
    return [(2 * cx - x, y) for x, y in pts]


# ------------------------------------------------------------------ Zeichenfläche
class ZCanvas:
    """Zeichenfläche mit 3 Farbzonen + Tinte. Befehle sammeln, `render()` erzeugt RGBA."""

    def __init__(self, box: tuple[float, float, float, float], ppc: float = 8.0, outline_cm: float = 0.85):
        """box = (x0, y0, x1, y1) in Figuren-cm (Ursprung zwischen den Füßen, y nach oben)."""
        self.x0, self.y0, x1, y1 = box
        w_cm, h_cm = x1 - self.x0, y1 - self.y0
        self.w_cm, self.h_cm, self.ppc = w_cm, h_cm, ppc
        self.s = ppc * SS
        self.size = (max(1, round(w_cm * self.s)), max(1, round(h_cm * self.s)))
        self.W = np.zeros((self.size[1], self.size[0], 3), np.float32)   # Zonen-Gewichte
        self.A = np.zeros((self.size[1], self.size[0]), np.float32)      # Deckung
        self.outline_cm = outline_cm

    # --- Koordinaten
    def p(self, x: float, y: float) -> Pt:
        return (x - self.x0) * self.s, (self.h_cm - (y - self.y0)) * self.s

    # Masken sind Ausschnitte (Maske, y0, x0) – gerechnet wird nur im Bereich der Form (schnell).
    def _bbox(self, q, pad: float):
        xs = [a[0] for a in q]
        ys = [a[1] for a in q]
        x0 = max(0, int(min(xs) - pad) - 1)
        y0 = max(0, int(min(ys) - pad) - 1)
        x1 = min(self.size[0], int(max(xs) + pad) + 2)
        y1 = min(self.size[1], int(max(ys) + pad) + 2)
        return x0, y0, max(x0 + 1, x1), max(y0 + 1, y1)

    def _poly_mask(self, pts: Sequence[Pt]):
        q = [self.p(*a) for a in pts]
        x0, y0, x1, y1 = self._bbox(q, 1)
        m = Image.new("L", (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(m).polygon([(x - x0, y - y0) for x, y in q], fill=255)
        return np.asarray(m, np.float32) / 255.0, y0, x0

    def _stroke_mask(self, pts: Sequence[Pt], w_cm: float, closed: bool = False):
        q = [self.p(*a) for a in pts] + ([self.p(*pts[0])] if closed else [])
        w = max(1, round(w_cm * self.s))
        x0, y0, x1, y1 = self._bbox(q, w)
        m = Image.new("L", (x1 - x0, y1 - y0), 0)
        d = ImageDraw.Draw(m)
        ql = [(x - x0, y - y0) for x, y in q]
        d.line(ql, fill=255, width=w, joint="curve")
        r = w / 2
        for x, y in (ql[0], ql[-1]):
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        return np.asarray(m, np.float32) / 255.0, y0, x0

    # --- Malen (Maler-Reihenfolge: später liegt oben)
    def _put(self, mk, w: Sequence[float], clip=None, alpha: float = 1.0):
        m, y0, x0 = mk
        h, wd = m.shape
        sl = (slice(y0, y0 + h), slice(x0, x0 + wd))
        if clip is not None:
            cm, cy0, cx0 = clip
            full = np.zeros((h, wd), np.float32)
            # Überlappung von Maske und Clip-Ausschnitt
            ya, yb = max(y0, cy0), min(y0 + h, cy0 + cm.shape[0])
            xa, xb = max(x0, cx0), min(x0 + wd, cx0 + cm.shape[1])
            if ya < yb and xa < xb:
                full[ya - y0:yb - y0, xa - x0:xb - x0] = cm[ya - cy0:yb - cy0, xa - cx0:xb - cx0]
            m = m * full
        col = np.asarray(w, np.float32)
        if alpha < 1.0:
            # halbdurchsichtige Tinte (Schatten): nur über bereits Gemaltem abdunkeln
            k = (m * alpha)[..., None]
            self.W[sl] = self.W[sl] * (1 - k) + col * k
            return
        self.W[sl] = self.W[sl] * (1 - m[..., None]) + col * m[..., None]
        self.A[sl] = np.maximum(self.A[sl], m)

    def fill(self, pts: Sequence[Pt], zone: int = 1, shade: float = 1.0, clip=None, alpha: float = 1.0):
        """Fläche in Zone 1…3 (0 = Tinte) mit Helligkeit shade (1 = voll, <1 = Richtung Tinte).
        alpha < 1: Schatten/Glanz auf vorhandener Farbe (ändert die Deckung nicht)."""
        self._put(self._poly_mask(pts), self._w(zone, shade), clip, alpha)

    def ellipse(self, cx, cy, rx, ry, zone: int = 1, shade: float = 1.0, clip=None, alpha: float = 1.0):
        self.fill(blob(cx, cy, rx, ry), zone, shade, clip, alpha)

    def line(self, pts: Sequence[Pt], w_cm: float, zone: int = 0, shade: float = 1.0, closed=False, clip=None,
             alpha: float = 1.0):
        self._put(self._stroke_mask(pts, w_cm, closed), self._w(zone, shade), clip, alpha)

    def dashed(self, pts: Sequence[Pt], w_cm: float, dash_cm: float, zone: int = 0, shade: float = 1.0, clip=None):
        """Gestrichelte Linie (Naht-/Stich-Optik in Haaren und Stoff)."""
        acc, on, seg = 0.0, True, [pts[0]]
        for a, b in zip(pts, pts[1:]):
            d = math.dist(a, b)
            t = 0.0
            while t < d:
                step = min(dash_cm - acc, d - t)
                t += step
                acc += step
                p = (a[0] + (b[0] - a[0]) * t / d, a[1] + (b[1] - a[1]) * t / d)
                seg.append(p)
                if acc >= dash_cm - 1e-6:
                    if on and len(seg) > 1:
                        self.line(seg, w_cm, zone, shade, clip=clip)
                    on, acc, seg = not on, 0.0, [p]
        if on and len(seg) > 1:
            self.line(seg, w_cm, zone, shade, clip=clip)

    def erase(self, pts: Sequence[Pt], soft: float = 1.0):
        """Form ausschneiden (Deckung weg) – z. B. das Gesichtsfenster aus einer Haarkappe."""
        m, y0, x0 = self._poly_mask(pts)
        h, wd = m.shape
        sl = (slice(y0, y0 + h), slice(x0, x0 + wd))
        self.A[sl] = self.A[sl] * (1 - m * soft)

    def mask(self, pts: Sequence[Pt]):
        """Maske einer Form – als `clip` für Muster und Schatten innerhalb einer Fläche."""
        return self._poly_mask(pts)

    def coverage(self) -> np.ndarray:
        return self.A.copy()

    @staticmethod
    def _w(zone: int, shade: float) -> list[float]:
        w = [0.0, 0.0, 0.0]
        if zone:
            w[zone - 1] = shade
        return w

    # --- Ergebnis
    def outline_under(self, extra_cm: float | None = None):
        """Gleichmäßige Tinten-Kontur um alles bisher Gemalte."""
        r = (self.outline_cm if extra_cm is None else extra_cm) * self.s
        if r <= 0:
            return
        inside = self.A > 0.5
        dist = ndimage.distance_transform_edt(~inside)
        ring = np.clip(r + 0.5 - dist, 0, 1).astype(np.float32)
        ring = np.maximum(ring - self.A, 0)
        # Ring ist Tinte (Gewichte 0) → nur Deckung erhöhen
        self.W = self.W * (1 - ring[..., None])
        self.A = np.maximum(self.A, ring)

    def render_part(self, anchor: Pt, pad_cm: float = 0.5) -> tuple[Image.Image, dict]:
        """Rendern, auf die Deckung zuschneiden und Anker (Figuren-cm) in Teil-cm umrechnen.
        Ergebnis-Info: w_cm, h_cm, anchor_cm (x ab links, y ab unten) – Format von parts.json."""
        img = self.render()
        bb = img.getchannel("A").point(lambda v: 255 if v > 2 else 0).getbbox()
        if bb is None:
            bb = (0, 0, 1, 1)
        pad = round(pad_cm * self.ppc)
        l, t, r, b = max(0, bb[0] - pad), max(0, bb[1] - pad), min(img.width, bb[2] + pad), min(img.height, bb[3] + pad)
        img = img.crop((l, t, r, b))
        ox = self.x0 + l / self.ppc                       # Figuren-cm der linken Kante
        oy = self.y0 + self.h_cm - b / self.ppc           # Figuren-cm der Unterkante
        info = {"w_cm": round(img.width / self.ppc, 3), "h_cm": round(img.height / self.ppc, 3),
                "anchor_cm": [round(anchor[0] - ox, 3), round(anchor[1] - oy, 3)]}
        return img, info

    def render(self) -> Image.Image:
        rgb = np.clip(self.W * 255.0 + 0.5, 0, 255).astype(np.uint8)
        a = np.clip(self.A * 255.0 + 0.5, 0, 255).astype(np.uint8)
        img = Image.fromarray(np.dstack([rgb, a]), "RGBA")
        out = (max(1, round(self.w_cm * self.ppc)), max(1, round(self.h_cm * self.ppc)))
        # Vormultipliziert verkleinern, sonst bluten transparente Pixel dunkel ein
        pm = np.asarray(img, np.float32) / 255.0
        pm[..., :3] *= pm[..., 3:4]
        big = Image.fromarray(np.clip(pm * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")
        small = np.asarray(big.resize(out, Image.LANCZOS), np.float32) / 255.0
        al = small[..., 3:4]
        small[..., :3] = np.where(al > 1e-4, small[..., :3] / np.maximum(al, 1e-4), 0)
        return Image.fromarray(np.clip(small * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")


# ------------------------------------------------------------------ Vorschau (wie der Shader)
INK = (0.23, 0.16, 0.16)


def tint(img: Image.Image, zones: Sequence[Sequence[float]], ink=INK) -> Image.Image:
    """CPU-Nachbau von zone_tint.gdshader: Farbe = R·z1 + G·z2 + B·z3 + (1−R−G−B)·Tinte."""
    a = np.asarray(img, np.float32) / 255.0
    w = a[..., :3]
    z = np.asarray([list(zones[i]) if i < len(zones) else list(zones[0]) for i in range(3)], np.float32)
    rest = np.clip(1 - w.sum(-1, keepdims=True), 0, 1)
    col = w @ z + rest * np.asarray(ink, np.float32)
    return Image.fromarray(np.clip(np.dstack([col, a[..., 3]]) * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")


def hexcol(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore[return-value]
