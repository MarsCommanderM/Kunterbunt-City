"""Sounds (P02-T11, P03): 14 synthetische WAVs (CC0, 0 €), kurz, leise genug, bit-genau reproduzierbar."""
import hashlib
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SFX = ROOT / "assets" / "audio" / "sfx"
NAMES = ["pickup", "tap", "drop_soft", "drop_wood", "drop_clink", "drop_plastic", "drop_metal",
         "drop_paper", "open", "close", "deny", "pet_dog_bark", "pet_cat_meow", "eat_chomp"]


def test_all_sounds_present_and_short():
    for n in NAMES:
        with wave.open(str(SFX / f"{n}.wav")) as w:
            assert w.getframerate() == 22050 and w.getnchannels() == 1 and w.getsampwidth() == 2
            assert 0.03 < w.getnframes() / 22050 <= 0.5, n


def test_reproducible(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "tools" / "make_sfx.py"), "--out", str(tmp_path)], check=True)
    for n in NAMES:
        a = hashlib.md5((tmp_path / f"{n}.wav").read_bytes()).hexdigest()
        b = hashlib.md5((SFX / f"{n}.wav").read_bytes()).hexdigest()
        assert a == b, n
