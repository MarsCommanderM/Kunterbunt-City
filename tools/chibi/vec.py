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

    def _poly_mask(self, pts: Sequence[Pt]) -> np.ndarray:
        m = Image.new("L", self.size, 0)
        ImageDraw.Draw(m).polygon([self.p(*q) for q in pts], fill=255)
        return np.asarray(m, np.float32) / 255.0

    def _stroke_mask(self, pts: Sequence[Pt], w_cm: float, closed: bool = False) -> np.ndarray:
        m = Image.new("L", self.size, 0)
        d = ImageDraw.Draw(m)
        q = [self.p(*a) for a in pts] + ([self.p(*pts[0])] if closed else [])
        w = max(1, round(w_cm * self.s))
        d.line(q, fill=255, width=w, joint="curve")
        r = w / 2
        for x, y in (q[0], q[-1]):
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        return np.asarray(m, np.float32) / 255.0

    # --- Malen (Maler-Reihenfolge: später liegt oben)
    def _put(self, mask: np.ndarray, w: Sequence[float], clip: np.ndarray | None = None, cover: bool = True):
        if clip is not None:
            mask = mask * clip
        col = np.asarray(w, np.float32)
        self.W = self.W * (1 - mask[..., None]) + col * mask[..., None]
        if cover:
            self.A = np.maximum(self.A, mask)

    def fill(self, pts: Sequence[Pt], zone: int = 1, shade: float = 1.0, clip: np.ndarray | None = None):
        """Fläche in Zone 1…3 (0 = Tinte) mit Helligkeit shade (1 = voll, <1 = Richtung Tinte)."""
        self._put(self._poly_mask(pts), self._w(zone, shade), clip)

    def ellipse(self, cx, cy, rx, ry, zone: int = 1, shade: float = 1.0, clip=None):
        self.fill(blob(cx, cy, rx, ry), zone, shade, clip)

    def line(self, pts: Sequence[Pt], w_cm: float, zone: int = 0, shade: float = 1.0, closed=False, clip=None):
        self._put(self._stroke_mask(pts, w_cm, closed), self._w(zone, shade), clip)

    def mask(self, pts: Sequence[Pt]) -> np.ndarray:
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
