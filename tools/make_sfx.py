#!/usr/bin/env python3
"""
Erzeugt die Platzhalter-Soundeffekte (P02-T11) per Synthese – eigene Werke, CC0, 0 €.
Deterministisch (fester Zufalls-Seed) → identische Dateien bei jedem Lauf.
Ausgabe: assets/audio/sfx/*.wav (22,05 kHz, mono, 16 bit)   Aufruf: python3 tools/make_sfx.py [--out DIR]

Material-Sounds fürs Abstellen: soft, wood, clink (Keramik/Glas), plastic, metal, paper.
Dazu: pickup (Anheben), tap, open, close, deny (passt nicht).
"""
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SR = 22050
rng = np.random.default_rng(20260926)


def t(d):
    return np.arange(int(SR * d)) / SR


def env(n, attack=0.004, decay=8.0):
    x = np.arange(n) / SR
    a = np.clip(x / attack, 0, 1)
    return a * np.exp(-decay * x)


def modes(freqs, d, decays, amps=None):
    x = t(d)
    amps = amps or [1.0] * len(freqs)
    return sum(a * np.sin(2 * np.pi * f * x) * np.exp(-k * x) for f, k, a in zip(freqs, decays, amps))


def noise(d, lp=0.2):
    n = rng.standard_normal(int(SR * d))
    out = np.zeros_like(n)
    for i in range(1, len(n)):          # einfacher Tiefpass
        out[i] = out[i - 1] + lp * (n[i] - out[i - 1])
    return out


def norm(x, peak=0.7):
    x = x - np.mean(x)
    fade = min(len(x), int(0.004 * SR))
    x[-fade:] *= np.linspace(1, 0, fade)
    return peak * x / (np.max(np.abs(x)) + 1e-9)


SOUNDS = {
    "pickup": lambda: norm(np.sin(2 * np.pi * np.cumsum(np.linspace(420, 880, int(SR * 0.09))) / SR) * env(int(SR * 0.09), 0.005, 18), 0.45),
    "tap": lambda: norm(modes([1800, 2600], 0.05, [120, 160]) + 0.3 * noise(0.05, 0.6) * env(int(SR * 0.05), 0.001, 90), 0.4),
    "drop_soft": lambda: norm(modes([130, 190], 0.16, [30, 45]) + 0.5 * noise(0.16, 0.05) * env(int(SR * 0.16), 0.002, 30), 0.6),
    "drop_wood": lambda: norm(modes([210, 540, 1130], 0.22, [28, 40, 60], [1, 0.6, 0.3]) + 0.3 * noise(0.22, 0.4) * env(int(SR * 0.22), 0.001, 80), 0.65),
    "drop_clink": lambda: norm(modes([2100, 3320, 5150], 0.35, [14, 18, 24], [1, 0.7, 0.4]), 0.45),
    "drop_plastic": lambda: norm(modes([880, 1390, 2250], 0.12, [45, 55, 70], [1, 0.6, 0.3]) + 0.4 * noise(0.12, 0.5) * env(int(SR * 0.12), 0.001, 60), 0.55),
    "drop_metal": lambda: norm(modes([1210, 2760, 4130, 5570], 0.5, [7, 9, 12, 15], [1, 0.8, 0.5, 0.3]), 0.45),
    "drop_paper": lambda: norm(noise(0.1, 0.35) * env(int(SR * 0.1), 0.003, 35), 0.5),
    "open": lambda: norm(noise(0.22, 0.08) * env(int(SR * 0.22), 0.05, 10) + 0.5 * modes([180], 0.22, [20]), 0.5),
    "close": lambda: norm(modes([120, 260], 0.18, [35, 50]) + 0.4 * noise(0.18, 0.2) * env(int(SR * 0.18), 0.001, 50), 0.6),
    "deny": lambda: norm(np.sin(2 * np.pi * np.cumsum(np.linspace(520, 300, int(SR * 0.16))) / SR) * env(int(SR * 0.16), 0.005, 14), 0.4),
}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    out = Path(args[args.index("--out") + 1]) if "--out" in args else ROOT / "assets" / "audio" / "sfx"
    global rng
    rng = np.random.default_rng(20260926)  # bei jedem Aufruf neu → reproduzierbar
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in SOUNDS.items():
        data = (fn() * 32767).astype("<i2")
        with wave.open(str(out / f"{name}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(data.tobytes())
    print(f"✅ {len(SOUNDS)} Sounds → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
