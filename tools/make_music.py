#!/usr/bin/env python3
"""
P07-T09: Musik + Ambiente per Synthese (NumPy) – 0 €, bit-genau reproduzierbar, CC0 (selbst erzeugt).

  music_home   ruhige Tag-Musik fürs Zuhause (Kalimba-Melodie, Bass, weiche Fläche, Shaker) – nahtlose Schleife
  amb_garden   Vögel + leiser Wind
  amb_indoor   Raumklang + leises Uhr-Ticken
  amb_bath     Wassertropfen + leises Rauschen

Schleifen: Ende und Anfang werden überblendet → kein Knacken beim Wiederholen.
Aufruf: python3 tools/make_music.py [--out assets/audio/music]
"""
from __future__ import annotations

import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SR = 22050
rng = np.random.default_rng(20260927)


def t(d: float) -> np.ndarray:
    return np.arange(int(SR * d)) / SR


def pluck(f: float, d: float, bright: float = 0.35) -> np.ndarray:
    """Kalimba-/Marimba-artiger Ton: Grundton + 2 Obertöne, schnell abklingend."""
    x = t(d)
    env = np.exp(-x * 5.5) * np.minimum(1.0, x * 400)
    return env * (np.sin(2 * np.pi * f * x) + bright * np.sin(2 * np.pi * f * 3.01 * x) * np.exp(-x * 9)
                  + 0.12 * np.sin(2 * np.pi * f * 5.4 * x) * np.exp(-x * 20))


def pad(freqs: list[float], d: float) -> np.ndarray:
    x = t(d)
    env = np.minimum(1.0, x / 0.4) * np.minimum(1.0, (d - x) / 0.4)
    s = np.zeros_like(x)
    for f in freqs:
        for det in (-0.6, 0.6):
            ph = 2 * np.pi * (f + det) * x
            s += (2 / np.pi) * np.arcsin(np.sin(ph))          # Dreieck = weich
    return s * env / (len(freqs) * 2)


def noise(d: float, lp: float = 0.3) -> np.ndarray:
    n = rng.standard_normal(int(SR * d))
    out = np.zeros_like(n)
    a = 0.0
    for i, v in enumerate(n):
        a += lp * (v - a)
        out[i] = a
    return out


def mix(buf: np.ndarray, x: np.ndarray, at: float, gain: float = 1.0) -> None:
    i = int(at * SR)
    j = min(len(buf), i + len(x))
    if i < len(buf):
        buf[i:j] += x[: j - i] * gain


def loop_seam(buf: np.ndarray, fade_s: float = 0.6) -> np.ndarray:
    """Letzte fade_s Sekunden in den Anfang überblenden, dann abschneiden → nahtlose Schleife."""
    n = int(fade_s * SR)
    head, tail = buf[:n].copy(), buf[-n:]
    w = np.linspace(0, 1, n)
    buf = buf[:-n].copy()
    buf[:n] = head * w + tail * (1 - w)
    return buf


def norm(x: np.ndarray, peak: float) -> np.ndarray:
    m = np.max(np.abs(x)) or 1.0
    return x / m * peak


NOTE = {n: 440.0 * 2 ** ((i - 9) / 12) for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def hz(name: str, octave: int) -> float:
    return NOTE[name] * 2 ** (octave - 4)


def music_home() -> np.ndarray:
    bpm = 92.0
    beat = 60.0 / bpm
    chords = [("C", ["C", "E", "G"]), ("A", ["A", "C", "E"]), ("F", ["F", "A", "C"]), ("G", ["G", "B", "D"])] * 4
    total = len(chords) * 4 * beat + 0.6
    buf = np.zeros(int(total * SR) + SR)
    penta = ["C", "D", "E", "G", "A"]
    for bar, (root, triad) in enumerate(chords):
        t0 = bar * 4 * beat
        mix(buf, pad([hz(n, 3) for n in triad], 4 * beat + 0.3), t0, 0.16)
        for k in (0, 2):                                        # Bass auf 1 und 3
            mix(buf, pluck(hz(root, 2), 1.2, 0.1), t0 + k * beat, 0.45)
        for k in range(8):                                      # Melodie in Achteln (nicht jede)
            if rng.random() < (0.35 if k % 2 else 0.75):
                n = penta[int(rng.integers(len(penta)))] if rng.random() < 0.6 else triad[int(rng.integers(3))]
                mix(buf, pluck(hz(n, 5), 0.9), t0 + k * beat / 2, 0.32)
        for k in range(8):                                      # Shaker leise
            mix(buf, noise(0.05, 0.6) * np.exp(-t(0.05) * 60), t0 + k * beat / 2 + 0.01, 0.05 if k % 2 else 0.08)
    return norm(loop_seam(buf[: int(total * SR)]), 0.55)


def tune(chords: list, bpm: float, scale: list, octave: int = 5, swing: float = 0.0) -> np.ndarray:
    """P09: weitere Stücke nach demselben Bauplan wie music_home (Fläche, Bass, Kalimba-Melodie, Shaker)."""
    beat = 60.0 / bpm
    total = len(chords) * 4 * beat + 0.6
    buf = np.zeros(int(total * SR) + SR)
    for bar, (root, triad) in enumerate(chords):
        t0 = bar * 4 * beat
        mix(buf, pad([hz(n, 3) for n in triad], 4 * beat + 0.3), t0, 0.14)
        for k in (0, 2):
            mix(buf, pluck(hz(root, 2), 1.1, 0.1), t0 + k * beat, 0.42)
        for k in range(8):
            if rng.random() < (0.4 if k % 2 else 0.8):
                n = scale[int(rng.integers(len(scale)))] if rng.random() < 0.6 else triad[int(rng.integers(3))]
                mix(buf, pluck(hz(n, octave), 0.8), t0 + k * beat / 2 + (swing * beat if k % 2 else 0.0), 0.3)
        for k in range(8):
            mix(buf, noise(0.05, 0.6) * np.exp(-t(0.05) * 60), t0 + k * beat / 2 + 0.01, 0.05 if k % 2 else 0.08)
    return norm(loop_seam(buf[: int(total * SR)]), 0.55)


def music_town() -> np.ndarray:
    """Einkaufsstraße: munter, G-Dur, leicht geswingt."""
    ch = [("G", ["G", "B", "D"]), ("E", ["E", "G", "B"]), ("C", ["C", "E", "G"]), ("D", ["D", "F#", "A"])] * 4
    return tune(ch, 108.0, ["G", "A", "B", "D", "E"], 5, swing=0.12)


def music_park() -> np.ndarray:
    """Spielplatz & Park: luftig, F-Dur, langsamer."""
    ch = [("F", ["F", "A", "C"]), ("D", ["D", "F", "A"]), ("A#", ["A#", "D", "F"]), ("C", ["C", "E", "G"])] * 4
    return tune(ch, 88.0, ["F", "G", "A", "C", "D"], 5)


def music_school() -> np.ndarray:
    """Schule: fröhlich, D-Dur, hüpfend."""
    ch = [("D", ["D", "F#", "A"]), ("G", ["G", "B", "D"]), ("A", ["A", "C#", "E"]), ("D", ["D", "F#", "A"])] * 4
    return tune(ch, 100.0, ["D", "E", "F#", "A", "B"], 5, swing=0.08)


def music_clinic() -> np.ndarray:
    """Gesundheitszentrum: ruhig und freundlich, C-Dur, sanft."""
    ch = [("C", ["C", "E", "G"]), ("A", ["A", "C", "E"]), ("F", ["F", "A", "C"]), ("G", ["G", "B", "D"])] * 4
    return tune(ch, 84.0, ["C", "D", "E", "G", "A"], 5)


def music_pool() -> np.ndarray:
    """Freizeitbad: sonnig, A-Dur, beschwingt."""
    ch = [("A", ["A", "C#", "E"]), ("F#", ["F#", "A", "C#"]), ("D", ["D", "F#", "A"]), ("E", ["E", "G#", "B"])] * 4
    return tune(ch, 112.0, ["A", "B", "C#", "E", "F#"], 5, swing=0.1)


def music_fair() -> np.ndarray:
    """Rummelplatz: flotter Walzer-Schwung, C-Dur, Drehorgel-Gefühl."""
    ch = [("C", ["C", "E", "G"]), ("G", ["G", "B", "D"]), ("F", ["F", "A", "C"]), ("G", ["G", "B", "D"])] * 4
    return tune(ch, 126.0, ["C", "D", "E", "G", "A"], 5, swing=0.15)


def amb_garden() -> np.ndarray:
    d = 24.0
    buf = noise(d + 0.6, 0.02) * 0.25 * (0.7 + 0.3 * np.sin(2 * np.pi * t(d + 0.6) / 7.0))   # Wind
    for _ in range(26):                                          # Vogel-Zwitschern
        at = rng.uniform(0, d)
        f0 = rng.uniform(2200, 3800)
        for k in range(int(rng.integers(2, 5))):
            dd = rng.uniform(0.05, 0.12)
            x = t(dd)
            sweep = np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f0 * rng.uniform(1.1, 1.5), len(x))) / SR)
            mix(buf, sweep * np.sin(np.pi * x / dd), at + k * (dd + 0.04), 0.18)
    return norm(loop_seam(buf), 0.35)


def amb_indoor() -> np.ndarray:
    d = 12.0
    buf = noise(d + 0.6, 0.01) * 0.15                            # Raumton
    for k in range(int(d)):                                      # Uhr: tick – tack
        click = np.sin(2 * np.pi * (3200 if k % 2 else 2600) * t(0.02)) * np.exp(-t(0.02) * 300)
        mix(buf, click, k + 0.1, 0.12)
    return norm(loop_seam(buf), 0.2)


def amb_bath() -> np.ndarray:
    d = 10.0
    buf = noise(d + 0.6, 0.05) * 0.1
    for _ in range(9):                                           # Tropfen
        at = rng.uniform(0, d)
        f = rng.uniform(900, 1500)
        x = t(0.12)
        drop = np.sin(2 * np.pi * np.cumsum(np.linspace(f, f * 1.8, len(x))) / SR) * np.exp(-x * 40)
        mix(buf, drop, at, 0.5)
    return norm(loop_seam(buf), 0.3)


TRACKS = {"music_home": music_home, "amb_garden": amb_garden, "amb_indoor": amb_indoor, "amb_bath": amb_bath,
          "music_town": music_town, "music_park": music_park, "music_school": music_school,
          "music_clinic": music_clinic, "music_pool": music_pool,
          "music_fair": music_fair}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    out = Path(args[args.index("--out") + 1]) if "--out" in args else ROOT / "assets" / "audio" / "music"
    global rng
    rng = np.random.default_rng(20260927)
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in TRACKS.items():
        data = (np.clip(fn(), -1, 1) * 32767).astype("<i2")
        with wave.open(str(out / f"{name}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(data.tobytes())
        print(f"  {name}: {len(data) / SR:.1f} s")
    print(f"✅ {len(TRACKS)} Stücke → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
