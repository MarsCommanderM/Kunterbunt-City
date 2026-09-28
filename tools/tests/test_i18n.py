"""P11-T03: Alle Sprachdateien haben dieselben Schlüssel, und jeder sichtbare Menü-Text im Code ist übersetzt."""
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAT = re.compile(r'(?:Ui\.(?:label|button)\(|\.text = |_status\.text = |tr\()"([^"]*[A-Za-zÄÖÜäöüß][^"]*)"')
SKIP = {"Kunterbunt City", "%d / %d", "%d cm", "%d  +  %d  =  ?", "Name"}


def _langs():
    return {Path(f).stem: json.loads(Path(f).read_text(encoding="utf-8")) for f in glob.glob(str(ROOT / "data/i18n/*.json"))}


def test_same_keys_everywhere():
    langs = _langs()
    assert len(langs) >= 5
    keys = {k: set(v["messages"]) for k, v in langs.items()}
    first = next(iter(keys.values()))
    for lang, k in keys.items():
        assert k == first, f"{lang}: {sorted(k ^ first)}"
        assert all(str(x).strip() for x in langs[lang]["messages"].values()), lang


def test_every_menu_text_is_translated():
    keys = set(next(iter(_langs().values()))["messages"])
    missing = set()
    for f in glob.glob(str(ROOT / "src/ui/*.gd")):
        for m in PAT.finditer(Path(f).read_text(encoding="utf-8")):
            t = m.group(1)
            if re.fullmatch(r"[a-z_0-9]+", t) or t in SKIP:
                continue
            if t not in keys:
                missing.add(f"{Path(f).name}: {t}")
    assert not missing, sorted(missing)


def test_placeholders_match():
    for lang, d in _langs().items():
        for k, v in d["messages"].items():
            assert re.findall(r"%[sd]", k) == re.findall(r"%[sd]", v), f"{lang}: {k!r} → {v!r}"
