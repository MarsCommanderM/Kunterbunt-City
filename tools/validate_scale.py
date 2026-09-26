#!/usr/bin/env python3
"""
Maßstab-Prüfer für Kunterbunt City  (0 €, nur Python-Standardbibliothek)
========================================================================
Prüft:
  1. data/scale_table.json  gegen  data/scale_rules.json   (Größen-Regeln)
  2. alle data/items/*.json (falls vorhanden):
       - jedes Item verweist per "scale_ref" auf einen Eintrag der Maßstab-Tabelle
       - size_cm[1] (Höhe) == Tabellen-Höhe × (scale_mul, Standard 1.0; erlaubt 0.7–1.3 für Varianten)
       - Seitenverhältnis des Sprites weicht max. tolerance_aspect von der Tabelle ab
       - grip gesetzt, wenn hold != none

Aufruf:   python3 tools/validate_scale.py          -> Exit-Code 0 = alles OK, 1 = Fehler
Wird in jeder Phase und in CI ausgeführt. Ein roter Maßstab-Test blockiert jeden Commit.
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)

def main() -> int:
    table = load("data/scale_table.json")
    rules = load("data/scale_rules.json")["rules"]
    T = {e["id"]: e for e in table["entries"]}
    errors, warns = [], []

    # ---------- Tabelle in sich prüfen
    for r in rules:
        t = r["type"]
        if t == "lt":
            a, b = T.get(r["a"]), T.get(r["b"])
            if not a or not b:
                errors.append(f"Regel verweist auf unbekannte ID: {r}")
            elif not a["h_cm"] < b["h_cm"]:
                errors.append(f"{r['a']} ({a['h_cm']} cm) muss kleiner sein als {r['b']} ({b['h_cm']} cm)")
        elif t == "hold_max":
            for e in T.values():
                if e["hold"] == r["hold"] and e["h_cm"] > r["max_h_cm"]:
                    errors.append(f"{e['id']}: hold={r['hold']} aber {e['h_cm']} cm > {r['max_h_cm']} cm")
        elif t == "surface_fit":
            for e in T.values():
                if e["placement"] == r["placement"] and e["h_cm"] > r["max_h_cm"]:
                    errors.append(f"{e['id']}: steht auf '{r['placement']}' aber ist {e['h_cm']} cm hoch (max {r['max_h_cm']})")
        elif t == "category_range":
            for e in T.values():
                if e["category"] == r["category"] and not (r["min_h_cm"] <= e["h_cm"] <= r["max_h_cm"]):
                    errors.append(f"{e['id']}: {e['h_cm']} cm außerhalb {r['category']}-Bereich {r['min_h_cm']}–{r['max_h_cm']}")
        elif t == "seat_below_table":
            seat, tab = T[r["seat"]].get("seat_h_cm"), T[r["table"]].get("surface_h_cm")
            if seat is None or tab is None or tab - seat < r["min_gap_cm"]:
                errors.append(f"Sitz {r['seat']} ({seat}) und Tisch {r['table']} ({tab}): Abstand < {r['min_gap_cm']} cm")
        else:
            warns.append(f"Unbekannter Regeltyp: {t}")

    # ---------- Items prüfen
    tol = table.get("tolerance_aspect", 0.3)
    n_items = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "items", "*.json"))):
        data = json.load(open(path, encoding="utf-8"))
        for it in data.get("items", data if isinstance(data, list) else []):
            n_items += 1
            iid = it.get("id", "?")
            ref = T.get(it.get("scale_ref", ""))
            if not ref:
                errors.append(f"{iid}: fehlendes/unbekanntes scale_ref '{it.get('scale_ref')}'")
                continue
            mul = it.get("scale_mul", 1.0)
            if not 0.7 <= mul <= 1.3:
                errors.append(f"{iid}: scale_mul {mul} außerhalb 0.7–1.3")
            w, h = it.get("size_cm", [0, 0])
            exp_h = ref["h_cm"] * mul
            if abs(h - exp_h) > 0.5:
                errors.append(f"{iid}: Höhe {h} cm ≠ erwartet {exp_h:.1f} cm (scale_ref {ref['id']})")
            if ref["w_cm"] > 0 and h > 0:
                ar, ar_ref = w / h, ref["w_cm"] / ref["h_cm"]
                if abs(ar - ar_ref) / ar_ref > tol:
                    warns.append(f"{iid}: Seitenverhältnis {ar:.2f} weicht >{int(tol*100)} % von {ar_ref:.2f} ab – Sprite prüfen")
            if it.get("hold", ref["hold"]) != "none" and not it.get("grip"):
                errors.append(f"{iid}: hold={it.get('hold', ref['hold'])} aber kein grip-Punkt")

    for w in warns:
        print("WARNUNG:", w)
    if errors:
        print(f"\n❌ MASSSTAB-FEHLER ({len(errors)}):")
        for e in errors:
            print("  -", e)
        return 1
    print(f"✅ Maßstab OK – {len(T)} Tabellen-Einträge, {len(rules)} Regeln, {n_items} Items geprüft")
    return 0

if __name__ == "__main__":
    sys.exit(main())
