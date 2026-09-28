# 🏙️ Kunterbunt City · Agenten-Bausatz

Kostenloses Sandbox-Spiel im Stil von Toca Boca, aber größer und hochwertiger (Stil C „Premium-Vektor“): 11 Bereiche, ~1.000 bewegliche Items, Charakter-Editor, Figuren mit echter Arbeits-KI und Haustiere. **Alles kostet 0 €.**

Dieser Ordner ist das **Repo** und zugleich die **komplette Bauanleitung für deinen KI-Agenten** im VS-Code-Terminal.

---

## Spielen & Bauen (Version 0.1.0)
```bash
godot --headless --export-release "Web" export/web/index.html      # Browser-Version
godot --headless --export-release "Linux" export/linux/KunterbuntCity.x86_64
godot --headless --export-release "Windows" export/windows/KunterbuntCity.exe
NODE_PATH=$(npm root -g) node tools/dev/web_smoke.cjs export/web out.png --play   # Web-Build im Browser testen
```
Export-Vorlagen (nur Web/Linux/Windows, ohne 1,3-GB-Archiv): `python3 tools/dev/fetch_web_templates.py 4.7.2 --desktop`.
Änderungen: `CHANGELOG.md` · itch.io-Texte: `docs/release/itch_seite.md`.

## 1. Was liegt wo?
| Datei | Für wen | Inhalt |
|---|---|---|
| `MASTERPROMPT.md` | 🤖 Agent | **Die Verfassung**: Regeln, Stack, Architektur, Maßstab, Qualitäts-Tore, Phasen |
| `docs/PROGRESS.md` | 🤖 + 👤 | Fortschritt / Gedächtnis zwischen Sitzungen |
| `docs/phasen/PHASE_00 … 11` | 🤖 | Detaillierte Baupläne mit Tasks, Akzeptanzkriterien, Startprompt |
| `docs/01_KRITISCHE_REVIEW.md` | 👤 | Was am alten Entwurf geändert wurde und warum |
| `docs/02_MASSSTAB_BIBEL.md` | 🤖 | Formeln und Regeln: Warum der Hund nie größer als der Tisch ist |
| `docs/03_STIL_GUIDE_C.md` | 👤 | Prompts zum Generieren der Grafiken (Stil C) |
| `docs/04_ASSET_PIPELINE.md` | 🤖 + 👤 | Vom KI-Bild zum maßstabsgetreuen Sprite |
| `docs/05_WELT_UND_BEREICHE.md` | 🤖 | Alle 11 Bereiche, Szenen, NPCs, Items |
| `docs/06_TECH_SPEC.md` | 🤖 | Schemas, Systeme, Budgets, Tests |
| `data/scale_table.json` | 🤖 | **Einzige Quelle für Größen** (cm) |
| `tools/validate_scale.py` | 🤖 | Maßstab-Prüfer, muss immer grün sein |
| `reference/` | beide | Stil- und Maßstab-Referenzbilder, Demo-Sprites |

## 2. Voraussetzungen (einmalig, alles kostenlos)
1. **Godot 4.4+** (godotengine.org), und `godot` muss im PATH sein, sodass `godot --version` funktioniert
2. **Python 3.11+**
3. **Git** + ein Repo auf GitHub/Codeberg (optional)
4. Ein Agent im Terminal, z. B.:
   - **Claude Code** (`claude`), liest automatisch `CLAUDE.md`
   - **OpenAI Codex CLI** (`codex`), liest automatisch `AGENTS.md`
   - **Gemini CLI** (`gemini`), liest automatisch `GEMINI.md`
   - **GitHub Copilot** (Agent-Modus in VS Code), liest `.github/copilot-instructions.md`
   > Alle Pointer-Dateien verweisen auf `MASTERPROMPT.md`. Das Spiel selbst bleibt kostenlos, egal welchen Agenten du nimmst. Für Gratis-Nutzung eignet sich z. B. Gemini CLI mit der kostenlosen Stufe.
5. Für die Grafik später (Phase 06): **ComfyUI** lokal + ein frei lizenziertes Modell (siehe Stil-Guide)

## 3. GitHub-Repo + Arbeitsplan anlegen (einmalig)
Ein Befehl legt **nur das neue Repo `MarsCommanderM/Kunterbunt-City`** an (privat), pusht diesen Ordner und erzeugt den Arbeitsplan: **19 Meilensteine** (eine pro Phase, 10a–10h einzeln) und **142 Issues** (jede Task, Abnahme pro Phase, 👤-Aufgaben).
```bash
# einmalig: GitHub CLI installieren → https://cli.github.com
gh auth login                         # im Browser bestätigen
cd kunterbunt-city
python3 tools/github_setup.py --dry-run   # zeigt nur an, was passieren würde
python3 tools/github_setup.py             # legt an (≈ 3 Min. wegen GitHub-Tempolimit)
```
- Windows: `python` statt `python3`. Öffentlich statt privat: `--public`.
- Existiert das Repo schon mit Inhalt → Abbruch, es wird **nichts** überschrieben.
- Erneut ausführen ist harmlos: Vorhandenes wird übersprungen.
- `docs/ARBEITSPLAN.md` = derselbe Plan als Checkliste im Repo.

Der Agent schließt Issues über Commits: `[P02-T04] DragController (Closes #31)`.

## 4. So arbeitest du mit dem Agenten
```bash
cd kunterbunt-city
python3 tools/validate_scale.py        # muss "OK" melden
claude        # oder: codex / gemini
```
Dann den **Startprompt** aus der aktuellen Phasen-Datei hineinkopieren, z. B. für den Anfang:

> Lies MASTERPROMPT.md, docs/PROGRESS.md und docs/phasen/PHASE_00_SETUP.md. Setze Phase 00 Task für Task um. Nach jeder Task check.sh ausführen (sobald vorhanden), PROGRESS.md aktualisieren und committen. Am Ende Phasenbericht nach MASTERPROMPT §11 und stoppen.

**Der Rhythmus:**
1. Agent baut eine Phase → schreibt einen **Phasenbericht** → stoppt
2. **Du** prüfst: Spiel starten, Screenshots und Lineup ansehen, 👤-Aufgaben erledigen
3. Passt es? → Startprompt der nächsten Phase. Passt es nicht? → Feedback geben, der Agent korrigiert
4. Neue Sitzung/Kontext voll? Einfach sagen: *„Lies MASTERPROMPT.md und docs/PROGRESS.md und mach weiter.“*

## 5. Goldene Regeln (Kurzfassung)
- 📏 **Größen nie raten**: nur aus `data/scale_table.json`. Neue Items brauchen einen Tabelleneintrag, danach muss der Prüfer grün sein.
- 🎨 **Nur Stil C**: keine Code-gezeichnete Grafik als Endergebnis, Platzhalter nur übergangsweise.
- 💶 **0 €**: nur freie Lizenzen (MIT/Apache/CC0/CC-BY), keine Werbung, keine Käufe, kein Tracking.
- 🌐 **Kein Internet im Spiel.**
- ✅ **Nichts committen, was `scripts/check.sh` rot macht.**

## 6. Deine Aufgaben als Mensch 👤 (Überblick)
| Wann | Was |
|---|---|
| Phase 00 | Tools installieren |
| Phase 03, 07, 09, 11 | Kindertests (Kinder spielen lassen und beobachten, nicht helfen) |
| ab Phase 06 | Grafiken mit ComfyUI generieren (Prompts im Stil-Guide), in `incoming/` legen, Lineup prüfen |
| Phase 09 / 11 | Auf itch.io veröffentlichen, APK auf dem Tablet testen, Namens-Markencheck |
