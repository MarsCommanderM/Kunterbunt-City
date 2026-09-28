"""P07-T09: Musik/Ambiente – vorhanden, nicht übersteuert, nahtlose Schleife, bit-genau reproduzierbar."""
from __future__ import annotations

import json
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import make_music  # noqa: E402


def _read(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        assert w.getframerate() == 22050 and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32767


def test_alle_stuecke_da_und_sauber():
    for name in make_music.TRACKS:
        x = _read(ROOT / "assets/audio/music" / f"{name}.wav")
        assert len(x) > 22050 * 8, name
        assert np.max(np.abs(x)) < 0.95, f"{name} übersteuert"
        assert abs(x[-1] - x[0]) < 0.08, f"{name}: Schleife knackt"


def test_zuhause_hat_musik_und_ambiente():
    h = json.loads((ROOT / "data/areas/home.json").read_text(encoding="utf-8"))
    assert h["music"] in make_music.TRACKS
    for r in h["rooms"]:
        assert r.get("ambience") in make_music.TRACKS, r["id"]


def test_reproduzierbar(tmp_path):
    make_music.main(["--out", str(tmp_path)])
    for name in make_music.TRACKS:
        assert (tmp_path / f"{name}.wav").read_bytes() == (ROOT / "assets/audio/music" / f"{name}.wav").read_bytes(), name
