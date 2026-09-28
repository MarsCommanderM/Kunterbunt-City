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


def bark():
    """Kurzes „Wuff“: Formant-artiger Ton mit schnellem Tonhöhen-Abfall + etwas Rauschen."""
    n = int(SR * 0.22)
    f = np.linspace(620, 330, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
    return (tone + 0.35 * noise(0.22, 0.4)[:n]) * env(n, 0.006, 11)


def meow():
    """„Miau“: Tonhöhe steigt und fällt, Obertöne öffnen sich (i → a → u)."""
    n = int(SR * 0.45)
    x = np.linspace(0, 1, n)
    f = 520 + 380 * np.sin(np.pi * x) ** 1.5
    ph = 2 * np.pi * np.cumsum(f) / SR
    bright = 0.2 + 0.8 * np.sin(np.pi * x)
    tone = np.sin(ph) + bright * 0.6 * np.sin(2 * ph) + bright * 0.3 * np.sin(3 * ph)
    return tone * np.minimum(1, x * 12) * np.minimum(1, (1 - x) * 5)


def norm(x, peak=0.7):
    x = x - np.mean(x)
    fade = min(len(x), int(0.004 * SR))
    x[-fade:] *= np.linspace(1, 0, fade)
    return peak * x / (np.max(np.abs(x)) + 1e-9)


def chirp():
    """Vogel: kurze, helle Triller-Folge (3 Staccato-Töne, leicht nach oben)."""
    parts = []
    for f0, d in ((2600, 0.07), (3200, 0.06), (2900, 0.09)):
        n = int(SR * d)
        f = np.linspace(f0, f0 * 1.15, n)
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)
        parts.append(tone * env(n, 0.004, 26))
        parts.append(np.zeros(int(SR * 0.03)))
    return np.concatenate(parts)


def squeak():
    """Kleines Nagetier: sehr kurzes, hohes Quieken."""
    n = int(SR * 0.16)
    f = np.linspace(1500, 2400, n)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return tone * env(n, 0.004, 24)


def wheek():
    """Meerschweinchen: längeres, aufgeregtes Quieken (Tonhöhe wackelt)."""
    n = int(SR * 0.5)
    x = np.linspace(0, 1, n)
    f = 900 + 700 * np.sin(np.pi * x) + 60 * np.sin(2 * np.pi * 18 * x)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.5 * np.sin(2 * ph)
    return tone * np.minimum(1, x * 20) * np.minimum(1, (1 - x) * 8)


def bubble():
    """Fisch: 3 Blubber-Blops (Ton steigt je Blop kurz an)."""
    parts = []
    for f0 in (420, 560, 480):
        n = int(SR * 0.12)
        f = np.linspace(f0, f0 * 2.2, n)
        parts.append(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 20))
        parts.append(np.zeros(int(SR * 0.06)))
    return np.concatenate(parts)


def whinny():
    """Pony: Wiehern – schnelles Vibrato, abfallende Tonhöhe."""
    n = int(SR * 0.7)
    x = np.linspace(0, 1, n)
    vib = 1.0 + 0.12 * np.sin(2 * np.pi * 22 * x)
    f = (760 - 260 * x) * vib
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)
    return tone * np.minimum(1, x * 14) * np.minimum(1, (1 - x) * 4)


def dragon_cute():
    """Mini-Drache: freundliches, kurzes Brummen mit Knister-Funken."""
    n = int(SR * 0.55)
    x = np.linspace(0, 1, n)
    f = (180 + 60 * np.sin(np.pi * x)) * (1.0 + 0.08 * np.sin(2 * np.pi * 15 * x))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.7 * np.sin(2 * ph) + 0.35 * np.sin(3 * ph)
    crackle = noise(0.55, 0.7)[:n] * (np.sin(2 * np.pi * 7 * x) ** 2) * 0.25
    return (tone + crackle) * np.minimum(1, x * 10) * np.minimum(1, (1 - x) * 5)


def sparkle():
    """Einhorn: 5 glitzernde Glockentöne (aufsteigend)."""
    parts = []
    for i, f0 in enumerate((1180, 1480, 1760, 2220, 2640)):
        n = int(SR * 0.22)
        parts.append(modes([f0, f0 * 2.01], 0.22, [12, 16], [1, 0.4]))
        if i < 4:
            parts.append(np.zeros(int(SR * 0.05)))
    return np.concatenate(parts)


def purr():
    """Katze schnurrt: 25-Hz-Amplitudenmodulation über einem tiefen Brummen."""
    n = int(SR * 0.9)
    x = np.arange(n) / SR
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 25 * x)
    return (np.sin(2 * np.pi * 62 * x) + 0.4 * np.sin(2 * np.pi * 124 * x)) * am * np.minimum(1, x * 6) * np.minimum(1, (1 - x) * 6)


def hiss_soft():
    """Schildkröte: sanftes Zischen (kurz, leise)."""
    n = int(SR * 0.3)
    return noise(0.3, 0.55)[:n] * env(n, 0.03, 9)


def ui_tap():
    """Weicher UI-Klick (kleiner Pop)."""
    n = int(SR * 0.07)
    f = np.linspace(700, 1250, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 40)


def ui_confirm():
    """Bestätigung: zwei Töne aufwärts (C–G), warm."""
    parts = []
    for f0, d in ((523.25, 0.12), (783.99, 0.22)):
        n = int(SR * d)
        parts.append((np.sin(2 * np.pi * f0 * np.arange(n) / SR) + 0.35 * np.sin(4 * np.pi * f0 * np.arange(n) / SR)) * env(n, 0.004, 9))
    return np.concatenate(parts)


def ui_back():
    """Zurück: zwei Töne abwärts."""
    parts = []
    for f0, d in ((659.25, 0.1), (440.0, 0.18)):
        n = int(SR * d)
        parts.append(np.sin(2 * np.pi * f0 * np.arange(n) / SR) * env(n, 0.004, 11))
    return np.concatenate(parts)


def dice_roll():
    """Würfel: 7 kurze Rassel-Schläge."""
    parts = []
    for i in range(7):
        n = int(SR * 0.05)
        parts.append(noise(0.05, 0.5)[:n] * env(n, 0.001, 90) * (0.6 + 0.4 * np.sin(i)))
        parts.append(np.zeros(int(SR * (0.045 + 0.02 * i))))
    return np.concatenate(parts)


def shutter():
    """Foto-Auslöser (Album)."""
    n = int(SR * 0.16)
    return np.concatenate([noise(0.05, 0.8)[:int(SR * 0.05)] * env(int(SR * 0.05), 0.001, 120),
                           np.zeros(int(SR * 0.02)),
                           noise(0.09, 0.6)[:int(SR * 0.09)] * env(int(SR * 0.09), 0.001, 70)])

def water_pour():
    """Gießkanne: plätscherndes Rauschen mit kleinen Tropfen."""
    d = 0.7
    n = int(SR * d)
    base = noise(d, 0.12)[:n] * np.minimum(1.0, np.linspace(0, 6, n)) * np.exp(-np.linspace(0, 2.5, n))
    drops = np.zeros(n)
    for k in range(9):
        i = int(rng.uniform(0.05, 0.6) * SR)
        m = min(n - i, int(SR * 0.05))
        f = rng.uniform(900, 1600)
        drops[i:i + m] += np.sin(2 * np.pi * np.cumsum(np.linspace(f, f * 1.6, m)) / SR) * env(m, 0.001, 70) * 0.35
    return base + drops


def grow():
    """Pflanze wächst eine Stufe: aufsteigendes, weiches Glitzern."""
    parts = []
    for k, f in enumerate((660, 880, 1175)):
        m = int(SR * 0.11)
        parts.append(np.sin(2 * np.pi * f * t(0.11)) * env(m, 0.004, 18) * (0.8 + 0.1 * k))
    return np.concatenate(parts)


def harvest():
    """Ernten: „Plopp" + fröhlicher Zweiklang."""
    pop = np.sin(2 * np.pi * np.cumsum(np.linspace(300, 900, int(SR * 0.06))) / SR) * env(int(SR * 0.06), 0.002, 40)
    ding = modes([1046, 1568], 0.35, [9, 11], [1, 0.6])
    return np.concatenate([pop, np.zeros(int(SR * 0.03)), ding])


def bark_var(f0, f1, d, times=1, gap=0.09):
    """P08-T08: weitere Bell-Varianten (tiefes Doppel-Wuff, helles Kläffen) – gleiche Bauweise wie bark()."""
    parts = []
    for k in range(times):
        n = int(SR * d)
        f = np.linspace(f0 * (1 - 0.06 * k), f1, n)
        ph = 2 * np.pi * np.cumsum(f) / SR
        tone = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
        parts += [(tone + 0.35 * noise(d, 0.4)[:n]) * env(n, 0.006, 11), np.zeros(int(SR * gap))]
    return np.concatenate(parts[:-1])


def mew():
    """Kurzes, hohes „Mii“ (Kätzchen)."""
    n = int(SR * 0.22)
    x = np.linspace(0, 1, n)
    f = 780 + 260 * np.sin(np.pi * x)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.4 * np.sin(2 * ph)) * np.minimum(1, x * 15) * np.minimum(1, (1 - x) * 6)


def scan_beep():
    """Kasse: klares Piep (Rechteck, gefiltert)."""
    n = int(SR * 0.16)
    x = t(0.16)
    return np.sign(np.sin(2 * np.pi * 1760 * x)) * 0.5 * np.minimum(1, x * 300) * np.minimum(1, (0.16 - x) * 120)[:n]


def whistle():
    """Trillerpfeife: hoher Ton mit schnellem Triller (Kugel in der Pfeife)."""
    x = t(0.5)
    f = 2900 + 180 * np.sign(np.sin(2 * np.pi * 28 * x))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.1 * noise(0.5, 0.8)[: len(x)]) * np.minimum(1, x * 60) * np.minimum(1, (0.5 - x) * 20)


def clap():
    """Zweimal klatschen."""
    one = noise(0.06, 0.7) * env(int(SR * 0.06), 0.001, 70)
    return np.concatenate([one, np.zeros(int(SR * 0.12)), one])


def horn():
    """Bus-Hupe: zwei freundliche Töne (Terz) mit Obertönen."""
    parts = []
    for f in (392.0, 330.0):
        x = t(0.28)
        tone = sum(np.sin(2 * np.pi * f * k * x) / k for k in (1, 2, 3, 4))
        parts += [tone * np.minimum(1, x * 60) * np.minimum(1, (0.28 - x) * 30), np.zeros(int(SR * 0.06))]
    return np.concatenate(parts)


def quack():
    """Ente: „Quak" – nasaler Ton (Rechteck-artig) mit schnell fallender Tonhöhe, zweimal."""
    parts = []
    for k in range(2):
        n = int(SR * 0.16)
        f = np.linspace(520 - k * 40, 330, n)
        ph = 2 * np.pi * np.cumsum(f) / SR
        tone = np.tanh(3 * np.sin(ph)) + 0.4 * np.sin(3 * ph)
        parts += [tone * env(n, 0.004, 9), np.zeros(int(SR * 0.08))]
    return np.concatenate(parts)


def coo():
    """Taube: weiches „Gurr" (tiefer Ton mit Tremolo)."""
    x = t(0.6)
    f = 300 + 40 * np.sin(np.pi * x / 0.6)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * x)) * np.minimum(1, x * 20) * np.minimum(1, (0.6 - x) * 8)


def pluck_tone(f, d, bright=0.4, dec=5.0):
    """P10: gezupfter/angeschlagener Ton (Klavier, Xylophon, Gitarre) – Grundton + Obertöne."""
    x = t(d)
    return (np.sin(2 * np.pi * f * x) + bright * np.sin(4 * np.pi * f * x) * np.exp(-x * 6)
            + 0.15 * np.sin(6 * np.pi * f * x) * np.exp(-x * 10)) * np.exp(-x * dec) * np.minimum(1, x * 500)


def bowed(f, d, vib=5.0):
    """Gestrichen/geblasen (Geige, Flöte): weicher Einsatz, Vibrato."""
    x = t(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.006 * np.sin(2 * np.pi * vib * x))) / SR
    return (np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)) * np.minimum(1, x * 8) * np.minimum(1, (d - x) * 6)


def chalk():
    """Kreide auf der Tafel: kurzes, raues Kratzen (3 Striche)."""
    parts = []
    for k in range(3):
        n = noise(0.09, 0.7) * np.sin(np.linspace(0, np.pi, int(SR * 0.09)))
        parts += [n, np.zeros(int(SR * 0.05))]
    return np.concatenate(parts)


def school_bell():
    """Schulglocke: helles Klingeln (schnell angeschlagene Glocke)."""
    x = t(1.1)
    ring = sum(np.sin(2 * np.pi * f * x) * a for f, a in ((1320, 1.0), (2640, 0.4), (3950, 0.2)))
    return ring * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 18 * x))) * np.exp(-x * 1.8) * np.minimum(1, x * 300)


def fizz():
    """Vulkan-Experiment: Sprudeln + Blubbern."""
    x = t(1.2)
    return noise(1.2, 0.5) * np.exp(-x * 1.5) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * x)) + 0.3 * modes([300], 1.2, [3])


def siren():
    """Freundliches „Tatü-tata" (zwei Töne im Wechsel, weich)."""
    parts = []
    for k in range(4):
        f = 660.0 if k % 2 == 0 else 880.0
        x = t(0.32)
        parts.append((np.sin(2 * np.pi * f * x) + 0.3 * np.sin(4 * np.pi * f * x)) * np.minimum(1, x * 40) * np.minimum(1, (0.32 - x) * 40))
    return np.concatenate(parts)


def rotor():
    """Hubschrauber: gepulstes Rauschen („wupp-wupp")."""
    x = t(1.4)
    return noise(1.4, 0.15) * (0.3 + 0.7 * np.maximum(0, np.sin(2 * np.pi * 11 * x)) ** 3) * np.minimum(1, x * 3)


def fair_bell():
    """Hau-den-Lukas-Glocke / Fahrt startet: helles „Ding“ mit Nachklang."""
    return modes([1320, 2640, 3960, 5280], 1.2, [3, 4, 6, 8], [1, 0.5, 0.3, 0.15])


def tada():
    """Zaubertrick: „Ta-daa“ (zwei Akkorde)."""
    a = sum(np.sin(2 * np.pi * f * t(0.14)) for f in (523, 659, 784)) * env(int(SR * 0.14), 0.005, 12)
    b = sum(np.sin(2 * np.pi * f * t(0.6)) for f in (659, 784, 1046)) * env(int(SR * 0.6), 0.005, 3)
    return np.concatenate([a, np.zeros(int(SR * 0.05)), b])


def boo():
    """Lustiges Gespenst: wackelndes „Huuu“ (nie gruselig, eher albern)."""
    x = t(0.9)
    f = 330 + 60 * np.sin(2 * np.pi * 6 * x) - 80 * x
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, x * 8) * np.minimum(1, (0.9 - x) * 5)


def roar():
    """Löwe: freundliches, kurzes Brummen (nie erschreckend)."""
    x = t(0.7)
    f = 140 + 40 * np.sin(np.pi * x / 0.7)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return (tone + 0.3 * noise(0.7, 0.3)) * np.minimum(1, x * 10) * np.minimum(1, (0.7 - x) * 4)


def trumpet():
    """Elefant: Trompeten (aufsteigender Ton mit Obertönen)."""
    x = t(0.8)
    f = 420 + 300 * np.minimum(1, x / 0.3)
    tone = sum(np.sin(2 * np.pi * k * np.cumsum(f) / SR) / k for k in (1, 2, 3, 4))
    return tone * np.minimum(1, x * 20) * np.minimum(1, (0.8 - x) * 4)


def bleat():
    """Ziege/Schaf: „Mäh“ mit Zittern."""
    x = t(0.6)
    f = 520 * (1 + 0.04 * np.sin(2 * np.pi * 24 * x))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * np.minimum(1, x * 15) * np.exp(-x * 2)


def oink():
    """Schwein: zwei kurze Grunzer."""
    parts = []
    for d in (0.14, 0.18):
        x = t(d)
        parts.append((np.sin(2 * np.pi * 180 * x) + 0.5 * noise(d, 0.2)) * np.sin(np.pi * x / d))
        parts.append(np.zeros(int(SR * 0.06)))
    return np.concatenate(parts)


def monkey():
    """Affe: fröhliches „Uh-uh-ah-ah“."""
    parts = []
    for f in (500, 560, 760, 820):
        x = t(0.1)
        parts.append(np.sin(2 * np.pi * np.cumsum(np.linspace(f, f * 1.3, len(x))) / SR) * np.sin(np.pi * x / 0.1))
        parts.append(np.zeros(int(SR * 0.04)))
    return np.concatenate(parts)


def penguin():
    """Pinguin: kurzes Schnattern."""
    x = t(0.35)
    return np.sign(np.sin(2 * np.pi * 330 * x)) * 0.4 * (0.5 + 0.5 * np.sin(2 * np.pi * 18 * x)) * np.sin(np.pi * x / 0.35)


def yum():
    """Tier frisst gern: „Mjam“ (zwei weiche Töne aufwärts)."""
    a = np.sin(2 * np.pi * 660 * t(0.12)) * env(int(SR * 0.12), 0.005, 12)
    b = np.sin(2 * np.pi * 990 * t(0.22)) * env(int(SR * 0.22), 0.005, 8)
    return np.concatenate([a, b])


SOUNDS = {
    "pickup": lambda: norm(np.sin(2 * np.pi * np.cumsum(np.linspace(420, 880, int(SR * 0.09))) / SR) * env(int(SR * 0.09), 0.005, 18), 0.45),
    "tap": lambda: norm(modes([1800, 2600], 0.05, [120, 160]) + 0.3 * noise(0.05, 0.6) * env(int(SR * 0.05), 0.001, 90), 0.4),
    "drop_soft": lambda: norm(modes([130, 190], 0.16, [30, 45]) + 0.5 * noise(0.16, 0.05) * env(int(SR * 0.16), 0.002, 30), 0.6),
    "drop_wood": lambda: norm(modes([210, 540, 1130], 0.22, [28, 40, 60], [1, 0.6, 0.3]) + 0.3 * noise(0.22, 0.4) * env(int(SR * 0.22), 0.001, 80), 0.65),
    "drop_clink": lambda: norm(modes([2100, 3320, 5150], 0.35, [14, 18, 24], [1, 0.7, 0.4]), 0.45),
    "drop_plastic": lambda: norm(modes([880, 1390, 2250], 0.12, [45, 55, 70], [1, 0.6, 0.3]) + 0.4 * noise(0.12, 0.5) * env(int(SR * 0.12), 0.001, 60), 0.55),
    "drop_metal": lambda: norm(modes([1210, 2760, 4130, 5570], 0.5, [7, 9, 12, 15], [1, 0.8, 0.5, 0.3]), 0.45),
    "drop_paper": lambda: norm(noise(0.1, 0.35) * env(int(SR * 0.1), 0.003, 35), 0.5),
    # Phase 03: Tierlaute (über den AudioBus-Limiter) und Essen
    "pet_dog_bark": lambda: norm(bark(), 0.7),
    "pet_cat_meow": lambda: norm(meow(), 0.55),
    "eat_chomp": lambda: norm(np.concatenate([noise(0.07, 0.25) * env(int(SR * 0.07), 0.002, 40), np.zeros(int(SR * 0.05)),
                                              noise(0.07, 0.3) * env(int(SR * 0.07), 0.002, 40)]), 0.5),
    "open": lambda: norm(noise(0.22, 0.08) * env(int(SR * 0.22), 0.05, 10) + 0.5 * modes([180], 0.22, [20]), 0.5),
    "close": lambda: norm(modes([120, 260], 0.18, [35, 50]) + 0.4 * noise(0.18, 0.2) * env(int(SR * 0.18), 0.001, 50), 0.6),
    # Phase 04: Tierstimmen für den Haustier-Editor + UI-Sounds
    "pet_bird_chirp": lambda: norm(chirp(), 0.5),
    "pet_rabbit_squeak": lambda: norm(squeak(), 0.45),
    "pet_hamster_squeak": lambda: norm(squeak(), 0.4),
    "pet_guinea_pig_wheek": lambda: norm(wheek(), 0.5),
    "pet_fish_bubble": lambda: norm(bubble(), 0.45),
    "pet_turtle_hiss": lambda: norm(hiss_soft(), 0.35),
    "pet_pony_whinny": lambda: norm(whinny(), 0.55),
    "pet_dragon_roar": lambda: norm(dragon_cute(), 0.55),
    "pet_unicorn_sparkle": lambda: norm(sparkle(), 0.4),
    "pet_cat_purr": lambda: norm(purr(), 0.45),
    "ui_tap": lambda: norm(ui_tap(), 0.35),
    "ui_confirm": lambda: norm(ui_confirm(), 0.4),
    "ui_back": lambda: norm(ui_back(), 0.35),
    "dice_roll": lambda: norm(dice_roll(), 0.5),
    "shutter": lambda: norm(shutter(), 0.5),
    "deny": lambda: norm(np.sin(2 * np.pi * np.cumsum(np.linspace(520, 300, int(SR * 0.16))) / SR) * env(int(SR * 0.16), 0.005, 14), 0.4),
    # P07-T07: Garten (hinten angehängt → alle bisherigen Sounds bleiben bit-gleich)
    "water_pour": lambda: norm(water_pour(), 0.45),
    "grow": lambda: norm(grow(), 0.4),
    "harvest": lambda: norm(harvest(), 0.5),
    # P08-T08: Tiere + Arbeits-Geräusche der NPCs (wieder hinten angehängt)
    "pet_dog_bark2": lambda: norm(bark_var(480, 260, 0.2, times=2), 0.7),
    "pet_dog_bark3": lambda: norm(bark_var(900, 620, 0.12), 0.6),
    "pet_cat_meow2": lambda: norm(mew(), 0.5),
    "scan_beep": lambda: norm(scan_beep(), 0.35),
    "whistle": lambda: norm(whistle(), 0.4),
    "clap": lambda: norm(clap(), 0.5),
    # P09: Straße + Park
    "bus_horn": lambda: norm(horn(), 0.45),
    "duck_quack": lambda: norm(quack(), 0.5),
    "pigeon_coo": lambda: norm(coo(), 0.4),
    # P10a: Schule & Instrumente (Antippen)
    "chalk": lambda: norm(chalk(), 0.3),
    "sponge": lambda: norm(noise(0.3, 0.1) * env(int(SR * 0.3), 0.05, 6), 0.3),
    "school_bell": lambda: norm(school_bell(), 0.45),
    "fizz": lambda: norm(fizz(), 0.4),
    "triangle": lambda: norm(modes([2700, 3900, 5600], 1.2, [2.5, 3.5, 5], [1, 0.6, 0.3]), 0.4),
    "tambourine": lambda: norm(noise(0.3, 0.9) * env(int(SR * 0.3), 0.002, 10) + 0.3 * modes([6200, 7400], 0.3, [12, 14]), 0.4),
    "drum_hit": lambda: norm(np.sin(2 * np.pi * np.cumsum(np.linspace(160, 60, int(SR * 0.3))) / SR) * env(int(SR * 0.3), 0.002, 9)
                             + 0.3 * noise(0.3, 0.3) * env(int(SR * 0.3), 0.001, 30), 0.6),
    "piano_note": lambda: norm(pluck_tone(523.25, 0.9, 0.5, 3.0) + 0.6 * pluck_tone(659.25, 0.9, 0.4, 3.0), 0.45),
    "xylophone": lambda: norm(np.concatenate([pluck_tone(f, 0.18, 0.2, 14) for f in (784, 988, 1175)]), 0.45),
    "guitar": lambda: norm(sum(pluck_tone(f, 1.0, 0.6, 3.5) * 0.6 for f in (196, 247, 294)), 0.45),
    "violin": lambda: norm(bowed(660.0, 0.7), 0.4),
    "flute": lambda: norm(bowed(880.0, 0.6, 4.0) * 0.8 + 0.08 * noise(0.6, 0.6)[: int(SR * 0.6)], 0.35),
    # P10b: Gesundheitszentrum
    "xray_beep": lambda: norm(np.concatenate([modes([1400], 0.12, [20]), np.zeros(int(SR * 0.06)), modes([1900], 0.2, [12])]), 0.35),
    "monitor_beep": lambda: norm(np.concatenate([np.sin(2 * np.pi * 1000 * t(0.08)) * env(int(SR * 0.08), 0.002, 25),
                                                  np.zeros(int(SR * 0.5))] * 2), 0.3),
    "siren": lambda: norm(siren(), 0.4),
    "rotor": lambda: norm(rotor(), 0.4),
    # P10d Rummelplatz
    "fair_bell": lambda: norm(fair_bell(), 0.45),
    "tada": lambda: norm(tada(), 0.4),
    "boo": lambda: norm(boo(), 0.4),
    # P10g Zoo
    "roar": lambda: norm(roar(), 0.4),
    "trumpet": lambda: norm(trumpet(), 0.35),
    "bleat": lambda: norm(bleat(), 0.4),
    "oink": lambda: norm(oink(), 0.4),
    "monkey": lambda: norm(monkey(), 0.35),
    "penguin": lambda: norm(penguin(), 0.3),
    "yum": lambda: norm(yum(), 0.4),
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
