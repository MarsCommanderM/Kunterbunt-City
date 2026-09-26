#!/usr/bin/env python3
"""
Kunterbunt City – GitHub-Setup (nur Standardbibliothek).

Legt GENAU EIN neues Repo an (Standard: MarsCommanderM/Kunterbunt-City),
pusht diesen Ordner und erzeugt den Arbeitsplan:
  • Labels   (phase-00 … phase-11, mensch, abnahme, massstab, content)
  • Meilensteine (eine pro Phase, Phase 10 aufgeteilt in 10a–10h)
  • Issues   (eine pro Task P00-T01 …, je Phase ein Abnahme-Issue,
              je Phase ein 👤-Mensch-Issue, je Bereich 10a–10h ein Bauplan-Issue)
  • docs/ARBEITSPLAN.md (komplette Checkliste, wird mit gepusht)

Zwei Wege:
  A) GitHub CLI (empfohlen):  gh auth login   →   python3 tools/github_setup.py
  B) Token:                   GITHUB_TOKEN=... python3 tools/github_setup.py --use-token
     (Fine-grained Token, nur für das Repo Kunterbunt-City, Rechte: Contents RW,
      Issues RW, Metadata R. Das Repo muss dann vorher leer auf github.com angelegt sein.)

Sicherheit:
  • Existiert das Repo schon und ist NICHT leer → Abbruch (nichts wird überschrieben).
  • Läuft das Skript erneut, werden vorhandene Labels/Meilensteine/Issues übersprungen.
  • --dry-run zeigt nur an, was passieren würde.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / "phasen"
API = "https://api.github.com"

LABELS = {
    "mensch": ("d93f0b", "Aufgabe für den Menschen 👤"),
    "abnahme": ("0e8a16", "Phasen-Abnahme / Akzeptanzkriterien"),
    "massstab": ("5319e7", "Betrifft Größen / scale_table"),
    "content": ("fbca04", "Bereich / Items / Inhalte"),
    "task": ("c5def5", "Agenten-Task"),
}
PHASE_COLOR = "1d76db"


# ───────────────────────── Phasen-Dateien einlesen ─────────────────────────
def clean(md: str) -> str:
    md = re.sub(r"\*\*|`", "", md)
    return re.sub(r"\s+", " ", md).strip()


def section(text: str, head: str) -> str:
    m = re.search(rf"^## {re.escape(head)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def parse_phases() -> list[dict]:
    phases = []
    for f in sorted(PHASE_DIR.glob("PHASE_*.md")):
        text = f.read_text(encoding="utf-8")
        num = re.match(r"PHASE_(\d+)", f.name).group(1)
        title = clean(text.splitlines()[0].lstrip("# ").split("·", 1)[-1])
        goal = re.search(r"^\*\*Ziel:\*\*(.*)$", text, re.M)
        tasks = [
            {"id": tid, "text": txt.strip()}
            for tid, txt in re.findall(r"^\| (P\d\d-T\d\d) \| (.+?) \|\s*$", text, re.M)
        ]
        accept = re.findall(r"^- \[ \] (.+)$", section(text, "Akzeptanzkriterien"), re.M)
        human = section(text, "👤 Mensch")
        start = section(text, "Startprompt")
        p = {
            "num": num, "file": f"docs/phasen/{f.name}", "title": title,
            "goal": clean(goal.group(1)) if goal else "", "tasks": tasks,
            "accept": accept, "human": human, "start": start, "sub": [],
        }
        if num == "10":
            p["sub"] = [
                {"id": sid, "name": clean(name), "ref": clean(ref)}
                for sid, name, ref in re.findall(r"^\| (10[a-h]) \| (.+?) \| (.+?) \|\s*$", text, re.M)
            ]
            p["bsteps"] = re.findall(r"^\| (B-\d\d) \| (.+?) \|\s*$", text, re.M)
        phases.append(p)
    return phases


# ───────────────────────── Plan erzeugen ─────────────────────────
def build_plan(phases: list[dict], repo: str) -> dict:
    labels = dict(LABELS)
    milestones, issues = [], []
    for p in phases:
        lab = f"phase-{p['num']}"
        labels[lab] = (PHASE_COLOR, f"Phase {p['num']} · {p['title']}")
        link = f"📄 Bauplan: [`{p['file']}`](https://github.com/{repo}/blob/main/{p['file']})"
        if p["sub"]:
            for s in p["sub"]:
                ms = f"P{s['id']} · {s['name']}"
                milestones.append({"title": ms, "description": f"Content-Welle {s['id']} – {s['name']} (Welt-Doku {s['ref']})"})
                steps = "\n".join(f"- [ ] **{b}** {t}" for b, t in p["bsteps"])
                acc = "\n".join(f"- [ ] {a}" for a in p["accept"])
                issues.append({
                    "title": f"{s['id']} · Bereich „{s['name']}“ nach Bereichs-Bauplan",
                    "labels": [lab, "content", "task"], "milestone": ms,
                    "body": f"{link}\nWelt-Doku: `docs/05_WELT_UND_BEREICHE.md` {s['ref']}\n\n"
                            f"## Bereichs-Bauplan\n{steps}\n\n## Akzeptanzkriterien\n{acc}\n\n"
                            f"## Startprompt\n> Lies MASTERPROMPT.md, docs/05_WELT_UND_BEREICHE.md {s['ref']} und "
                            f"{p['file']}. Baue Unterphase {s['id']} „{s['name']}“ nach dem Bereichs-Bauplan "
                            f"B-01 bis B-12. Phasenbericht und stoppen.\n",
                })
            continue
        ms = f"P{p['num']} · {p['title']}"
        milestones.append({"title": ms, "description": p["goal"][:250]})
        for t in p["tasks"]:
            short = clean(t["text"])
            short = short if len(short) <= 80 else short[:77].rsplit(" ", 1)[0] + " …"
            extra = ["massstab"] if re.search(r"scale|Maßstab|cm|Größe", t["text"]) else []
            issues.append({
                "title": f"{t['id']} · {short}", "labels": [lab, "task", *extra], "milestone": ms,
                "body": f"{link}\n\n## Aufgabe\n{t['text']}\n\n## Definition of Done\n"
                        "- [ ] Umgesetzt wie beschrieben\n- [ ] `bash scripts/check.sh` grün "
                        "(ab P00-T09; davor `python3 tools/validate_scale.py`)\n"
                        "- [ ] `docs/PROGRESS.md` aktualisiert\n"
                        f"- [ ] Commit `[{t['id']}] …` mit `Closes #<diese Nr>`\n",
            })
        acc = "\n".join(f"- [ ] {a}" for a in p["accept"])
        issues.append({
            "title": f"🏁 Phase {p['num']} abnehmen · {p['title']}", "labels": [lab, "abnahme"], "milestone": ms,
            "body": f"{link}\n\n**Ziel:** {p['goal']}\n\n## Akzeptanzkriterien\n{acc}\n\n"
                    f"## Phasenbericht\nNach MASTERPROMPT §11 hier als Kommentar einfügen.\n\n"
                    f"## Startprompt\n{p['start']}\n",
        })
        if p["human"]:
            issues.append({
                "title": f"👤 Mensch-Aufgaben Phase {p['num']}", "labels": [lab, "mensch"], "milestone": ms,
                "body": f"{link}\n\n{p['human']}\n",
            })
    return {"labels": labels, "milestones": milestones, "issues": issues}


def write_arbeitsplan(phases: list[dict], repo: str) -> Path:
    out = ["# 🗺️ ARBEITSPLAN · Kunterbunt City", "",
           f"> Automatisch erzeugt aus `docs/phasen/` durch `tools/github_setup.py`. "
           f"Live-Stand: **Issues & Meilensteine** auf https://github.com/{repo}", "",
           "Rhythmus: Agent baut eine Phase → Phasenbericht → 👤 prüft → nächste Phase.", ""]
    for p in phases:
        out += [f"## Phase {p['num']} · {p['title']}", f"*{p['goal']}*  ", f"Bauplan: `{p['file']}`", ""]
        for t in p["tasks"]:
            out.append(f"- [ ] **{t['id']}** {clean(t['text'])}")
        for s in p["sub"]:
            out.append(f"- [ ] **{s['id']}** {s['name']} (Bereichs-Bauplan B-01…B-12)")
        if p["accept"]:
            out += ["", "**Abnahme:**"] + [f"- [ ] {a}" for a in p["accept"]]
        out.append("")
    path = ROOT / "docs" / "ARBEITSPLAN.md"
    path.write_text("\n".join(out), encoding="utf-8")
    return path


# ───────────────────────── GitHub-Zugriff ─────────────────────────
class GH:
    def __init__(self, repo: str, token: str | None, dry: bool):
        self.repo, self.token, self.dry = repo, token, dry

    def api(self, method: str, path: str, data: dict | None = None, ok404=False):
        if self.dry and method != "GET":
            return {}
        if self.token:
            req = urllib.request.Request(API + path, method=method,
                                         data=json.dumps(data).encode() if data is not None else None)
            req.add_header("Authorization", f"Bearer {self.token}")
            req.add_header("Accept", "application/vnd.github+json")
            req.add_header("X-GitHub-Api-Version", "2022-11-28")
            try:
                with urllib.request.urlopen(req) as r:
                    body = r.read()
                    return json.loads(body) if body else {}
            except urllib.error.HTTPError as e:
                if ok404 and e.code == 404:
                    return None
                raise SystemExit(f"❌ GitHub-API {method} {path}: {e.code} {e.read().decode()[:300]}")
        cmd = ["gh", "api", "-X", method, path, "-H", "Accept: application/vnd.github+json"]
        if data is not None:
            cmd += ["--input", "-"]
        r = subprocess.run(cmd, input=json.dumps(data) if data is not None else None,
                           capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            if ok404 and "404" in (r.stderr + r.stdout):
                return None
            raise SystemExit(f"❌ gh api {method} {path}: {r.stderr.strip() or r.stdout.strip()}")
        return json.loads(r.stdout) if r.stdout.strip() else {}

    def paged(self, path: str) -> list:
        out, page = [], 1
        while True:
            sep = "&" if "?" in path else "?"
            chunk = self.api("GET", f"{path}{sep}per_page=100&page={page}", ok404=True) or []
            out += chunk
            if len(chunk) < 100:
                return out
            page += 1


def run(cmd: list[str], **kw):
    print("  $", " ".join(c if "@github.com" not in c else "<remote-mit-token>" for c in cmd))
    r = subprocess.run(cmd, cwd=ROOT, **kw)
    if r.returncode != 0:
        raise SystemExit(f"❌ Befehl fehlgeschlagen: {cmd[0]} {cmd[1] if len(cmd) > 1 else ''}")


def ensure_git_commit():
    if not (ROOT / ".git").exists():
        run(["git", "init", "-b", "main"])
    for key in ("user.name", "user.email"):
        if subprocess.run(["git", "config", key], cwd=ROOT, capture_output=True).returncode != 0:
            raise SystemExit(f"❌ git {key} fehlt. Einmalig: git config --global {key} \"…\"")
    run(["git", "add", "-A"])
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0:
        run(["git", "commit", "-q", "-m", "Agenten-Bausatz v2.0: Masterprompt, Phasenplan, Maßstab-System"])
    run(["git", "branch", "-M", "main"])


# ───────────────────────── Hauptablauf ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default="MarsCommanderM/Kunterbunt-City")
    ap.add_argument("--public", action="store_true", help="öffentlich statt privat anlegen")
    ap.add_argument("--use-token", action="store_true", help="GITHUB_TOKEN statt gh CLI verwenden")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-push", action="store_true", help="nur Labels/Meilensteine/Issues")
    a = ap.parse_args()

    phases = parse_phases()
    plan = build_plan(phases, a.repo)
    path = write_arbeitsplan(phases, a.repo)
    print(f"📋 Plan: {len(plan['labels'])} Labels · {len(plan['milestones'])} Meilensteine · "
          f"{len(plan['issues'])} Issues  →  {path.relative_to(ROOT)} geschrieben")

    if a.dry_run and not a.use_token and not shutil.which("gh"):
        for ms in plan["milestones"]:
            n = sum(i["milestone"] == ms["title"] for i in plan["issues"])
            print(f"   🎯 {ms['title']:<48} {n:>3} Issues")
        print("ℹ️  Dry-Run ohne GitHub-Zugriff beendet.")
        return

    token = os.environ.get("GITHUB_TOKEN") if a.use_token else None
    if a.use_token and not token:
        raise SystemExit("❌ --use-token gesetzt, aber GITHUB_TOKEN ist leer.")
    if not a.use_token:
        if not shutil.which("gh"):
            raise SystemExit("❌ GitHub CLI fehlt → https://cli.github.com installieren, dann: gh auth login")
        if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
            raise SystemExit("❌ Nicht eingeloggt → gh auth login")
    gh = GH(a.repo, token, a.dry_run)

    # 1) Repo anlegen / prüfen
    info = gh.api("GET", f"/repos/{a.repo}", ok404=True)
    if info is None:
        if a.use_token:
            raise SystemExit(f"❌ Repo {a.repo} existiert nicht. Mit Token-Weg bitte vorher LEER auf github.com anlegen.")
        print(f"🆕 Lege {a.repo} an ({'öffentlich' if a.public else 'privat'}) …")
        if not a.dry_run:
            ensure_git_commit()
            run(["gh", "repo", "create", a.repo, "--public" if a.public else "--private",
                 "--description", "Kostenloses Kinder-Sandbox-Spiel (Godot 4, Stil C) – Agenten-Bausatz & Phasenplan",
                 "--source", ".", "--remote", "origin", "--push"])
    else:
        if info.get("size", 0) > 0 and not a.skip_push:
            raise SystemExit(f"⛔ {a.repo} existiert bereits und ist nicht leer – Abbruch, nichts verändert. "
                             "(Nur Issues nachtragen: --skip-push)")
        if not a.skip_push and not a.dry_run:
            print(f"📦 {a.repo} ist leer → pushe …")
            ensure_git_commit()
            url = (f"https://x-access-token:{token}@github.com/{a.repo}.git" if token
                   else f"https://github.com/{a.repo}.git")
            subprocess.run(["git", "remote", "remove", "origin"], cwd=ROOT, capture_output=True)
            run(["git", "remote", "add", "origin", f"https://github.com/{a.repo}.git"])
            run(["git", "push", url if token else "origin", "main"])
            if not token:
                run(["git", "branch", "--set-upstream-to=origin/main", "main"])

    # 2) Labels
    have = {l["name"] for l in gh.paged(f"/repos/{a.repo}/labels")} if info is not None else set()
    for name, (color, desc) in plan["labels"].items():
        if name not in have:
            gh.api("POST", f"/repos/{a.repo}/labels", {"name": name, "color": color, "description": desc})
    print(f"🏷️  Labels ok")

    # 3) Meilensteine
    ms_num = {m["title"]: m["number"] for m in gh.paged(f"/repos/{a.repo}/milestones?state=all")} \
        if info is not None else {}
    for i, ms in enumerate(plan["milestones"]):
        if ms["title"] not in ms_num:
            r = gh.api("POST", f"/repos/{a.repo}/milestones", ms)
            ms_num[ms["title"]] = r.get("number", i + 1)
    print(f"🎯 {len(plan['milestones'])} Meilensteine ok")

    # 4) Issues (in Reihenfolge, damit die Nummern dem Plan folgen)
    existing = {x["title"] for x in gh.paged(f"/repos/{a.repo}/issues?state=all")} if info is not None else set()
    todo = [i for i in plan["issues"] if i["title"] not in existing]
    print(f"📝 Erzeuge {len(todo)} Issues (≈ {len(todo) * 1.3 / 60:.0f} Min. wegen GitHub-Tempolimit) …")
    for n, iss in enumerate(todo, 1):
        gh.api("POST", f"/repos/{a.repo}/issues", {
            "title": iss["title"], "body": iss["body"], "labels": iss["labels"],
            "milestone": ms_num[iss["milestone"]],
        })
        if n % 10 == 0 or n == len(todo):
            print(f"   {n}/{len(todo)}")
        if not a.dry_run:
            time.sleep(1.3)

    print(f"\n✅ Fertig: https://github.com/{a.repo}/milestones")


if __name__ == "__main__":
    main()
