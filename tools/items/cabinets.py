"""
Schrank-Baukasten (P07-Inventar): Sideboard, Vitrine, Wohnwand, Schuhschrank, Küchenzeile, Hängeschrank,
Badschrank, Aktenschrank, Truhe, Metallregal, Wickeltisch … aus EINEM Zeichner – jede Front ist aus Zellen gebaut.

layout: Spalten mit "|" getrennt, in jeder Spalte die Zellen von UNTEN nach OBEN mit "/" getrennt.
  D = Tür · W = Schublade · G = Glastür (Geschirr dahinter) · O = offenes Fach (Bücher/Deko)
  T = TV-/Geräte-Nische · S = Schuhfach · B = Korb/Wäsche · F = Aktenfach
Zonen: 1 = Korpus · 2 = Fronten / Glas · 3 = Griffe, Beine, Arbeitsplatte (Holz/Metall)
state "open": Türen stehen offen (Inhalt sichtbar), Schubladen bleiben zu.
"""
from __future__ import annotations

import random

from .furniture import _books
from .kit import INNER, SHADE, Item, ell, knob, leg, line, rrect, shaded, trap


def _handle(c, x, y, vertical=True, size=5.0):
    if vertical:
        c.fill(rrect(x - 0.7, y - size / 2, x + 0.7, y + size / 2, 0.6), zone=3)
    else:
        c.fill(rrect(x - size / 2, y - 0.7, x + size / 2, y + 0.7, 0.6), zone=3)


def _interior(c, a, y0, b, y1, kind: str, seed: int):
    """Innenleben (offene Tür/offenes Fach): dunkle Rückwand + passende Dinge."""
    rng = random.Random(seed)
    c.fill(rrect(a, y0, b, y1, 0.6), zone=1, shade=0.62)
    if kind in ("O", "D", "F"):
        if y1 - y0 > 14:
            _books(c, a, b, y0 + 0.5, (y1 - y0) * 0.78, seed)
        else:
            for k in range(int((b - a) / 7)):
                c.fill(rrect(a + 2 + k * 7, y0 + 0.5, a + 6 + k * 7, y1 - 2, 0.8), zone=[2, 3][k % 2], shade=0.95)
    elif kind == "G":
        rr = min(5.0, (y1 - y0) * 0.36)                     # Teller aufgestellt (rund) + Gläser + Tassen
        x = a + rr + 1.5
        k = 0
        while x + rr < b - 1:
            if k % 3 == 0:
                c.fill(ell(x, y0 + rr + 0.6, rr, rr, 24), zone=1, shade=1.6)                 # Porzellan: hell
                c.fill(ell(x, y0 + rr + 0.6, rr * 0.6, rr * 0.6, 20), zone=1, shade=1.45)
                c.line(ell(x, y0 + rr + 0.6, rr, rr, 24), INNER * 0.8, zone=0, closed=True)
                x += rr * 2 + 1.5
            else:
                gh = min((y1 - y0) * 0.6, 9.0)
                c.fill(trap(x - 1.6, x + 1.6, y0 + 0.5, x - 2.2, x + 2.2, y0 + gh, 0.4), zone=2, shade=1.3, alpha=0.75)
                c.line(trap(x - 1.6, x + 1.6, y0 + 0.5, x - 2.2, x + 2.2, y0 + gh, 0.4), INNER * 0.6, zone=0, closed=True)
                x += 6
            k += 1
    elif kind == "S":                                        # Schuhpaare
        for k in range(int((b - a) / 12)):
            x = a + 3 + k * 12
            col = [2, 3][k % 2]
            for dx in (0, 5):
                c.fill(rrect(x + dx, y0 + 0.4, x + dx + 5, y0 + 3.2, 1.2), zone=col, shade=0.9)
                c.fill(rrect(x + dx + 0.5, y0 + 2.4, x + dx + 2.6, y0 + 5.2, 1.0), zone=col, shade=0.9)
    elif kind == "B":
        c.fill(rrect(a + 2, y0 + 0.5, b - 2, y1 - 2, 2), zone=3)
        for k in range(1, 4):
            line(c, [(a + 2, y0 + (y1 - y0) * k / 4), (b - 2, y0 + (y1 - y0) * k / 4)], zone=3, shade=0.7)
    elif kind == "T":
        c.fill(rrect(a + 3, y0 + 0.5, b - 3, y0 + (y1 - y0) * 0.35, 0.6), zone=2, shade=0.35)
        c.fill(ell(a + 6, y0 + (y1 - y0) * 0.2, 1.2, 1.2, 12), zone=3)


def cabinet(it: Item, layout: str = "D|D", top: str = "flat", legs: str = "short", plinth: bool = False,
            state: str = "", seed: int = 1):
    """top: flat · counter (Arbeitsplatte, dick, Zone 3) · crown (Kranz) · none   legs: short · tall · none"""
    c, W, H = it.c, it.w, it.h
    leg_h = {"short": 5.0, "tall": 14.0, "none": 0.0}[legs]
    base = leg_h + (8.0 if plinth else 0.0)
    top_h = {"counter": 4.0, "flat": 2.2, "crown": 4.5, "none": 0.0}[top]
    body_top = H - top_h
    x0, x1 = -W / 2, W / 2
    if legs != "none":
        for sx in (-1, 1):
            leg(c, sx * (W / 2 - 4), 0, leg_h + 1, 3.2, 2.4, zone=3)
    if plinth:
        c.fill(rrect(x0 + 2, leg_h, x1 - 2, base + 1, 0.5), zone=1, shade=0.7)
    body = rrect(x0, base, x1, body_top + 0.5, 1.2)
    cl = shaded(c, body, 1, "right", SHADE, 0.06)
    cols = layout.split("|")
    fw = 1.6                                                  # Rahmenstärke zwischen den Fronten
    cw = (W - fw * (len(cols) + 1)) / len(cols)
    for ci, col in enumerate(cols):
        cells = col.split("/")
        a = x0 + fw + ci * (cw + fw)
        b = a + cw
        ch = (body_top - base - fw * (len(cells) + 1)) / len(cells)
        for ri, kind in enumerate(cells):
            y0 = base + fw + ri * (ch + fw)
            y1 = y0 + ch
            sd = seed * 31 + ci * 7 + ri
            if kind in ("O", "T", "S", "B", "F") and kind != "F":
                _interior(c, a, y0, b, y1, kind, sd)
                c.line(rrect(a, y0, b, y1, 0.6), INNER, zone=0, closed=True)
                continue
            if kind == "D" and state == "open":
                _interior(c, a, y0, b, y1, "D", sd)
                flap = [(b, y0), (b + cw * 0.28, y0 - 2), (b + cw * 0.28, y1 + 2), (b, y1)] if ci == len(cols) - 1 or ci % 2 else \
                    [(a, y0), (a - cw * 0.28, y0 - 2), (a - cw * 0.28, y1 + 2), (a, y1)]
                shaded(c, flap, 2, "bottom", SHADE, 0.2)
                continue
            if kind == "G":
                if state == "open":
                    _interior(c, a, y0, b, y1, "G", sd)
                    continue
                c.fill(rrect(a, y0, b, y1, 0.8), zone=2, shade=0.95)
                gl = rrect(a + 2, y0 + 2, b - 2, y1 - 2, 0.6)
                _interior(c, a + 2, y0 + 2, b - 2, y1 - 2, "G", sd)
                c.fill(gl, zone=2, shade=1.35, alpha=0.28)            # Glas-Schimmer
                c.fill([(a + 3, y1 - 3), (a + cw * 0.3, y1 - 3), (a + 3 + cw * 0.05, y0 + 3), (a + 3, y0 + 3)],
                       zone=2, shade=1.4, alpha=0.25)
                c.line(gl, INNER, zone=0, closed=True)
                _handle(c, b - 2.8 if ci % 2 == 0 else a + 2.8, (y0 + y1) / 2, True, min(6, ch * 0.3))
                continue
            front = rrect(a, y0, b, y1, 0.8)
            c.fill(front, zone=2)
            c.fill(rrect(a, y0, b, y0 + min(2.0, ch * 0.2), 0.6), zone=2, shade=0.86)
            c.line(front, INNER, zone=0, closed=True)
            if kind == "W":
                _handle(c, (a + b) / 2, y1 - min(ch * 0.3, 5), False, min(cw * 0.35, 12))
            elif kind == "F":
                c.fill(rrect((a + b) / 2 - 5, y1 - 7, (a + b) / 2 + 5, y1 - 3, 0.5), zone=3, shade=1.1)
                _handle(c, (a + b) / 2, y1 - 10, False, 8)
            else:                                              # Tür: Griff zur Mitte hin
                hx = b - 2.8 if ci % 2 == 0 else a + 2.8
                if len(cols) == 1:
                    hx = b - 2.8
                c.line(rrect(a + 2.2, y0 + 2.2, b - 2.2, y1 - 2.2, 0.6), INNER * 0.9, zone=2, shade=0.8, closed=True)
                _handle(c, hx, (y0 + y1) / 2 if ch < 60 else y0 + min(95.0 - y0, ch * 0.6), True, min(8, ch * 0.3))
    if top != "none":
        th = rrect(x0 - (1.5 if top == "counter" else 0.8), body_top, x1 + (1.5 if top == "counter" else 0.8), H, 0.8)
        c.fill(th, zone=3 if top == "counter" else 1, shade=1.0)
        c.fill(rrect(x0 - 1, body_top, x1 + 1, body_top + top_h * 0.35, 0.5), zone=3 if top == "counter" else 1, shade=0.86)
        c.line(th, INNER, zone=0, closed=True)


def counter_extra(it: Item, kind: str = "sink", layout: str = "D|W/W/W|D", state: str = ""):
    """Küchenzeile mit Spüle oder Kochfeld eingebaut (Arbeitsplatte 90 cm = Fläche zum Abstellen)."""
    cabinet(it, layout, top="counter", legs="none", plinth=True, state=state)
    c, W, H = it.c, it.w, it.h
    if kind == "sink":
        c.fill(rrect(-W * 0.18, H - 1.8, W * 0.02, H - 0.6, 0.8), zone=3, shade=0.7)
        c.line([(-W * 0.08, H - 0.5), (-W * 0.08, H + 16), (-W * 0.02, H + 18), (W * 0.04, H + 14)], 1.4, zone=3, shade=1.1)
        c.fill(rrect(-W * 0.1, H - 0.5, -W * 0.06, H + 2, 0.6), zone=3, shade=1.1)
    elif kind == "hob":
        for k, x in enumerate((-W * 0.25, -W * 0.08)):
            c.fill(ell(x, H + 0.3, W * 0.07, 1.2, 24), zone=3, shade=0.45)
        c.fill(rrect(W * 0.1, H * 0.5, W * 0.4, H * 0.75, 1), zone=2, shade=0.5)
