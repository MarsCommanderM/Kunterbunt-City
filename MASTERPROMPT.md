# 🏙️ KUNTERBUNT CITY – MASTERPROMPT für den Coding-Agenten
**Version 2.0 · Stand 26.09.2026 · Verbindlich für jede Sitzung**

> **An den Agenten:** Du bist der leitende Entwickler dieses Spiels. Lies diese Datei **zu Beginn jeder Sitzung vollständig**. Lies danach `docs/PROGRESS.md` (wo stehen wir?) und die aktuelle Phasen-Datei in `docs/phasen/`. Arbeite **nur** an der aktuellen Phase.
> Detail-Dokumente: `docs/01_KRITISCHE_REVIEW.md` (warum), `docs/02_MASSSTAB_BIBEL.md` (Größen), `docs/03_STIL_GUIDE_C.md` (Look), `docs/04_ASSET_PIPELINE.md` (Grafik-Produktion), `docs/05_WELT_UND_BEREICHE.md` (Inhalte), `docs/06_TECH_SPEC.md` (Architektur & Datenformate).

---

## 0. Arbeitsprotokoll (IMMER so arbeiten)

1. **Orientieren:** `MASTERPROMPT.md` → `docs/PROGRESS.md` → aktuelle `docs/phasen/PHASE_XX_*.md` lesen.
2. **Planen:** Schreibe einen kurzen Plan (max. 10 Punkte) für die nächste Aufgabe (Task-ID aus der Phasen-Datei). Bei Unklarheit: **nachfragen statt raten**.
3. **Klein bauen:** Eine Task nach der anderen. Kleine Commits (`[P02-T03] Drag&Drop: Einrasten auf Tischflächen`). Jede Task hat ein GitHub-Issue mit derselben ID im Titel → im Commit `Closes #<Nr>` angeben (Nummer per `gh issue list --search "P02-T03"`). Gesamtübersicht: `docs/ARBEITSPLAN.md`.
4. **Prüfen nach JEDER Task:**
   ```bash
   python3 tools/validate_scale.py                      # Maßstab – muss grün sein
   python3 -m pytest tools/tests -q                     # Tool-Tests (ab Phase 0)
   godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit   # Godot-Tests (ab Phase 0)
   ```
   **Rot = nicht committen.** Erst reparieren.
5. **Dokumentieren:** `docs/PROGRESS.md` aktualisieren (erledigt / offen / Probleme / nächste Task).
6. **Phasen-Ende:** Alle Akzeptanzkriterien der Phase abhaken, Bericht im Format aus Abschnitt 11 ausgeben und **STOPPEN**. Die nächste Phase beginnt erst nach „OK“ vom Menschen.
7. **👤-Aufgaben** (Grafik generieren, Kindertest, Veröffentlichen) macht der Mensch. Du bereitest sie vor (Anleitung, Prompts, Werkzeuge) und wartest.

---

## 1. Das Spiel in 60 Sekunden

**Kunterbunt City** ist eine **digitale Puppenhaus-Sandbox** (Genre wie Toca Life World) für Kinder von **5–9 Jahren**. Sie ist **hochwertiger als Toca**, **100 % kostenlos** und hat **keine Paywall, keine Werbung, keine Datensammlung**.

- **11 Bereiche:** Zuhause mit Garten · Gesundheitszentrum (Krankenhaus + Praxen) · Schule mit Pausenhof · Freizeitbad · Spielplatz & Park · Rummelplatz · Einkaufsstraße (inkl. Blumenladen) · Sportzentrum · Eishalle · Zoo · Werkstatt
- **~1.000 bewegbare Items** (~350 Vorlagen + Varianten), alle **maßstabsgetreu**
- **Pflicht beim ersten Start:** eigene Figur erstellen. Danach unbegrenzt viele Figuren und Haustiere.
- **Startmenü (Stadtkarte):** Pro Bereich ein Button → die Figur erscheint am Spawn-Punkt dieses Bereichs.
- **Feste NPCs mit KI:** Kassierer/in kassiert, Bademeister patrouilliert, Trainer/in trainiert, Ärzt/in behandelt usw.
- **Haustiere mit Eigenleben:** Hund bellt ab und zu, Katze miaut, Vogel zwitschert.
- **Alles frei bewegbar** außer fest eingebauten Objekten (Einbauten) und festen NPCs.
- **Look:** Stil C „Premium Vektor“ (siehe `reference/kueche_stil_c_massstab.png`).

---

## 2. Unverhandelbare Regeln

| ID | Regel |
|---|---|
| **R-01** | **0 € Kosten.** Keine kostenpflichtigen Dienste, SDKs, Assets oder Abos. Nur freie Software (MIT/Apache/BSD/CC0). |
| **R-02** | **Kein Netzwerk im Spiel.** Kein HTTPRequest, kein WebSocket, keine Analytics, kein Crash-Reporting-Dienst, keine Accounts, kein Chat. |
| **R-03** | **Keine Werbung, keine In-App-Käufe, keine Lootboxen, keine Energie-/Warte-Mechaniken, keine Paywall.** |
| **R-04** | **Maßstab ist Gesetz.** Jede Größe kommt aus `data/scale_table.json`. Keine Größen „nach Gefühl“, keine hart codierten Pixelmaße für Items/Figuren. |
| **R-05** | **1 Godot-Einheit = 1 cm.** Welt, Physik, Positionen und Größen in cm. |
| **R-06** | **Datengetrieben.** Items, Rezepte, NPC-Rollen, Bereiche und Figurenteile liegen in `data/` (JSON). Kein Item ist nur im Code definiert. |
| **R-07** | **Ohne Lesen spielbar.** Kein Text im Kinder-UI, der zum Spielen nötig ist. Nur Symbole, Farben, Töne. |
| **R-08** | **Eltern-Tor** vor Einstellungen, freier Texteingabe und allem, was das Spiel verlässt. |
| **R-09** | **Kein „Toca“** (oder andere fremde Marken) in Code, Dateinamen, Assets, Prompts oder Texten. |
| **R-10** | **Platzhalter zuerst.** Der Code funktioniert komplett mit Platzhalter-Sprites in exakter cm-Größe. Echte Grafik wird nur eingetauscht. |
| **R-11** | **Speicherstände sind heilig.** Jede Formatänderung braucht eine Versionsnummer und eine Migration plus Test. |
| **R-12** | **Tests grün vor Commit.** Maßstab-Prüfer, Python-Tests und Godot-Tests. |

---

## 3. Tech-Stack

| Bereich | Wahl |
|---|---|
| Engine | **Godot 4.x** (aktuelle stabile, mind. 4.4), **Renderer: Compatibility** |
| Sprache | **GDScript mit statischer Typisierung** (`var x: int`, `func f() -> void`) |
| Tests Godot | **GUT** (Godot Unit Test, MIT) unter `addons/gut/` |
| Tools | **Python 3.11+** (`tools/`), Tests mit **pytest**, Bildverarbeitung mit **Pillow, numpy, scipy** |
| Grafik-KI (👤) | **ComfyUI** lokal + frei lizenziertes Modell (z. B. FLUX.1 [schnell], Apache 2.0) + eigenes Stil-LoRA |
| Grafik-Nachbearbeitung (👤) | Krita, Inkscape (frei) |
| Audio (👤/Agent) | jsfxr/ChipTone (SFX), BeepBox/LMMS (Musik), Freesound nur **CC0** |
| Versionierung | Git + GitHub (kostenlos), optional GitHub Actions (headless Tests) |
| Export | **Web** (HTML5, *Thread Support aus*), **Android** (APK), **Windows/macOS/Linux** |
| Veröffentlichung (👤) | itch.io, GitHub Pages, F-Droid – alle 0 € |

---

## 4. Repository-Struktur (Soll)

```
kunterbunt-city/
├─ MASTERPROMPT.md            ← diese Datei
├─ AGENTS.md / CLAUDE.md / GEMINI.md   ← verweisen auf MASTERPROMPT.md
├─ README.md                  ← Anleitung für den Menschen
├─ CREDITS.md                 ← alle Quellen & Lizenzen (Pflicht)
├─ project.godot
├─ addons/gut/                ← Test-Framework
├─ data/
│   ├─ scale_table.json       ← MASSSTAB-TABELLE (Quelle der Wahrheit)
│   ├─ scale_rules.json       ← Größen-Regeln (automatisch geprüft)
│   ├─ items/*.json           ← Item-Definitionen pro Bereich/Raum
│   ├─ recipes/*.json         ← Kombinationen
│   ├─ areas/*.json           ← Bereiche, Räume, Spawn, Kamera, Oberflächen
│   ├─ npc_roles/*.json       ← NPC-Rollen-Vorlagen
│   ├─ npcs/*.json            ← konkrete NPCs (Rolle + Ort)
│   ├─ character_parts/*.json ← Editor-Teile (Frisuren, Kleidung …)
│   └─ pets/*.json
├─ src/
│   ├─ core/                  ← Autoloads: Game, SaveSystem, ItemDB, AudioBus, Settings, SceneRouter
│   ├─ world/                 ← Room, Surface, FloorBand, DepthSort, WorldCamera
│   ├─ items/                 ← ItemNode, ItemDefinition, DragController, Container, Recipes
│   ├─ characters/            ← CharacterNode, CharacterRig, HandSlot, SeatSlot, Emotions
│   ├─ pets/                  ← PetNode, PetBrain
│   ├─ npc/                   ← NpcNode, NpcStateMachine, Schedule, roles/
│   ├─ ui/                    ← MainMenu (Stadtkarte), CharacterEditor, Backpack, ParentGate, HUD
│   └─ areas/                 ← je Bereich: Szenen (.tscn) + bereichsspezifische Skripte
├─ assets/
│   ├─ placeholders/          ← automatisch erzeugte Platzhalter (cm-genau)
│   ├─ sprites/<bereich>/     ← echte Stil-C-Sprites (aus Pipeline)
│   ├─ backgrounds/<bereich>/
│   ├─ audio/
│   └─ fonts/
├─ tools/
│   ├─ validate_scale.py      ← Maßstab-Prüfer (existiert)
│   ├─ make_placeholders.py   ← Phase 2
│   ├─ asset_pipeline/        ← Phase 6: freistellen, zuschneiden, skalieren, Atlas
│   └─ tests/                 ← pytest
├─ tests/                     ← GUT-Tests (Godot)
├─ scripts/check.sh (+ .ps1) ← führt ALLE Qualitäts-Tore aus (Phase 0)
├─ reference/                 ← Stil- & Maßstab-Referenzen (NICHT ins Spiel exportieren)
└─ docs/
    ├─ PROGRESS.md            ← Gedächtnis des Agenten
    ├─ 01_KRITISCHE_REVIEW.md … 06_TECH_SPEC.md
    └─ phasen/PHASE_00 … PHASE_11
```

---

## 5. Maßstab – Kurzfassung (Details: `docs/02_MASSSTAB_BIBEL.md`)

| ID | Regel |
|---|---|
| **S-01** | Alle Größen in **cm**, Quelle: `data/scale_table.json`. |
| **S-02** | **Echte Größen.** Keine künstliche Vergrößerung kleiner Items. Varianten dürfen per `scale_mul` **0,7–1,3** abweichen (z. B. kleine/große Tasse). |
| **S-03** | Figuren: Baby 55 · Kleinkind 90 · **Kind 125** · Teen 155 · Erwachsen 172 · Senior 165 cm. Stil „großer Kopf“ (seit P04b): Kind ≈ 2 Kopfhöhen, Erwachsene ≈ 2,9. Größe nur aus der Tabelle, Frisur/Hut darf den Kopf überragen. |
| **S-04** | Welt-Fixmaße: Tisch 75 · Stuhlsitz 45 · Arbeitsplatte 90 · Tür 200 · Raumhöhe 260 cm. |
| **S-05** | Sprite-Höhe in der Welt = `h_cm × scale_mul`. Breite folgt aus dem Seitenverhältnis des Sprites (Toleranz ±30 % zur Tabelle, sonst Warnung). |
| **S-06** | Jedes Item hat **Pivot** (Aufstellpunkt, meist unten Mitte) und, wenn tragbar, einen **Grip** (Griffpunkt für die Hand). |
| **S-07** | **Tiefe:** Bodenband mit hinterer und vorderer Linie. Skalierung **1,00 → max. 1,12**. Sortierung nach Tiefe (y). |
| **S-08** | **Kamera:** zeigt standardmäßig **300 cm** Höhe. Zoom 220–450 cm, Außenbereiche und Zoo bis 700 cm. **Große Dinge werden nie geschrumpft, die Kamera zoomt raus.** |
| **S-09** | **Tippfläche** min. 48 dp, unabhängig von der Grafikgröße (auch ein Ei ist gut greifbar). |
| **S-10** | **Hintergründe werden eingemessen:** Referenzmaß im Bild (Arbeitsplatte 90 cm oder Tür 200 cm) → px/cm → Hintergrund wird auf Weltmaßstab skaliert. |
| **S-11** | Items **auf Oberflächen** (Tisch, Regal, Arbeitsplatte) max. 60 cm hoch. Oberflächen haben feste Höhen aus der Tabelle. |
| **S-12** | Gehaltene Items: `one_hand` max. 150 cm, `two_hands` max. 60 cm, `none` = nicht tragbar (Möbel, Fahrzeuge, große Tiere). |

---

## 6. Architektur – Kurzfassung (Details: `docs/06_TECH_SPEC.md`)

**Autoloads (max. 7):** `Game` (Zustand, aktuelle Figur), `SceneRouter` (Bereichswechsel, Ladebildschirm), `SaveSystem`, `ItemDB` (lädt `data/items`, `scale_table`, Rezepte), `AudioBus` (inkl. Tierlaut-Limiter), `Settings`, `Log`.

**Welt-Aufbau pro Raum:**
```
Room (Node2D)                   ← Maße in cm, Kamera-Grenzen
 ├─ Background (Sprite2D)       ← eingemessen (S-10)
 ├─ Surfaces (Node2D)           ← Surface-Nodes: Boden-Band, Tischplatten, Regale, Sitzplätze
 ├─ Fixtures (Node2D)           ← feste Einbauten mit Interaktion (Herd, Dusche, Kasse)
 ├─ YSortRoot (Node2D, y_sort)  ← Items, Figuren, Tiere, NPCs
 └─ Foreground (Node2D)         ← Dinge vor allem (Pflanzen vorne, Türrahmen)
```

**Kern-Klassen:** `ItemDefinition` (Resource aus JSON) · `ItemNode` (Sprite, Tippfläche, Zustand) · `DragController` (Touch/Maus, Anheben, Loslassen, Einrasten) · `Surface` (Höhe, Kapazität, erlaubte Placements) · `CharacterNode` + `CharacterRig` (Teile, Posen, `HandSlot`) · `SeatSlot` · `Container` · `RecipeSystem` · `NpcNode` + `NpcStateMachine` · `PetNode` + `PetBrain` · `UndoStack`.

**Datenfluss:** `data/*.json` → `ItemDB` (validiert beim Start, Fehler = klare Meldung) → Szenen instanziieren `ItemNode`s → Zustand ändert sich → `SaveSystem` speichert den Raumzustand (Item-ID, Position cm, Zustand, Container, Halter).

---

## 7. Code-Konventionen

- Dateien & Ordner `snake_case`, Klassen `PascalCase` mit `class_name`, Konstanten `UPPER_SNAKE`.
- **Bezeichner Englisch, Kommentare und Doku Deutsch.**
- Statische Typen überall. Keine `get_node("../../..")`-Ketten, sondern `@export` oder Signale.
- Signale für Ereignisse (`item_picked_up`, `item_dropped(item, surface)`, `character_sat(seat)`).
- Keine Magic Numbers: cm-Werte aus Daten, UI-Werte in `src/ui/ui_constants.gd`.
- Jede neue öffentliche Funktion in `src/` bekommt mindestens einen GUT-Test.
- Keine Datei > 400 Zeilen. Lieber aufteilen.
- Performance: kein `_process` auf Items im Ruhezustand. Nur das gezogene Item und aktive NPCs/Tiere ticken.

---

## 8. Qualitäts-Tore

| Tor | Wann | Befehl / Prüfung |
|---|---|---|
| **Alles** | jede Task | `bash scripts/check.sh` (ab Phase 00, bündelt die drei folgenden) |
| Maßstab | jede Task | `python3 tools/validate_scale.py` |
| Tool-Tests | jede Task | `python3 -m pytest tools/tests -q` |
| Godot-Tests | jede Task | `godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` |
| Kein Netzwerk | jede Task | Test `tests/test_no_network.gd` durchsucht `src/` nach verbotenen Klassen |
| Performance | Phasen-Ende | 60 FPS mit 250 Items + 15 aktiven NPCs/Tieren im Test-Raum (Desktop), Messung in `docs/PROGRESS.md` |
| Lineup | wenn neue Sprites kommen | `tools/asset_pipeline/lineup.py` → Bild prüfen (👤) |
| Kindertest | Phasen 3, 7, 9, 11 | 👤 Beobachtungsprotokoll in `docs/tests/` |

---

## 9. Phasen-Übersicht

| Phase | Name | Ergebnis |
|---|---|---|
| **00** | Setup & Werkzeuge | Godot-Projekt, Ordner, GUT, pytest, Git, Export-Presets, CI |
| **01** | Welt-Maßstab, Raum & Kamera | cm-Welt, Kamera 300 cm, Scrollen/Zoomen, Bodenband, Tiefe, Test-Raum |
| **02** | Item-System & Drag-and-Drop | ItemDB, Platzhalter, Ziehen, Einrasten, Stapeln, Behälter, Rückgängig |
| **03** | Figuren & Haustiere (Grundsystem) | Figur mit Posen, Hand-Slot (Grip), Sitzen/Liegen, Emotionen, Basis-Haustier |
| **04** | Charakter- & Haustier-Editor | Pflicht-Erstellung, Teile-Bibliothek, unbegrenzt speichern |
| **05** | Startmenü, Speichern, Bereichswechsel | Stadtkarte, Spawn, Rucksack, Eltern-Tor, Einstellungen, Speichern + Migration |
| **06** | Asset-Pipeline (produktiv) | Freistellen → Zuschneiden → cm → Atlas → Godot-Import + Lineup (👤 Grafik) |
| **07** | Vertical Slice „Zuhause“ | Alle Räume und der Garten, ~190 Items, Rezepte, Sounds, echte Grafik |
| **08** | NPC- & Tier-KI | Zustandsmaschinen, Rollen, Tagesplan, Rückkehr zum Platz, Laut-Limiter |
| **09** | MVP: Einkaufsstraße + Spielplatz → **Release v0.1** | Kassen-Logik, 9 Läden inkl. Blumenladen, Spielplatz, Web/Android auf itch.io |
| **10** | Content-Wellen (Bereiche 4–11) | Pro Bereich derselbe Bauplan (10a–10h) |
| **11** | Politur & **Release 1.0** | Performance, Barrierefreiheit, Sprachen, Kindertests, Veröffentlichung |
| *nach 1.0* | Backlog | Tag/Nacht, Wetter, Jahreszeiten, Fotomodus, weitere Bereiche |

---

## 10. Globale Definition of Done (für jede Task)

- [ ] Funktion umgesetzt, wie in der Phasen-Datei beschrieben
- [ ] Alle Größen aus `scale_table.json`, Maßstab-Prüfer grün
- [ ] Tests geschrieben und grün (Godot + Python)
- [ ] Keine Verstöße gegen R-01 bis R-12
- [ ] Funktioniert mit Maus **und** Touch (Touch per Emulation getestet)
- [ ] `docs/PROGRESS.md` aktualisiert
- [ ] Commit mit Task-ID

---

## 11. Berichtsformat am Ende einer Phase

```
## Phasenbericht PXX – <Name>
Status: ✅ fertig / ⚠️ teilweise / ❌ blockiert
Erledigt: <Task-IDs mit 1 Zeile je Task>
Akzeptanzkriterien: <jede Zeile: ✅/❌ + Nachweis (Test-Name, Screenshot-Pfad, Messwert)>
Tests: Maßstab ✅ | pytest x/y ✅ | GUT x/y ✅
Performance: <FPS, RAM>
Offene Punkte / Risiken: <…>
👤 Aufgaben für dich: <konkrete Schritte>
Vorschlag nächste Phase: PXX+1 – bitte mit „OK“ freigeben.
```

---

## 12. Verboten (sofort ablehnen, auch wenn es „nur schnell“ wäre)

- Bezahl-Dienste, Werbe-SDKs, Analytics, Tracking, Firebase, Crashlytics
- Netzwerk-Code jeder Art im Spiel
- Größen per Augenmaß, `scale = Vector2(0.37, 0.37)` ohne Herleitung aus cm
- Items oder Figuren direkt in Szenen „hinmalen“ ohne Eintrag in `data/`
- Fremde Marken, fremde Assets mit unklarer Lizenz, Assets aus der Google-Bildersuche
- Text, den ein Kind lesen muss, um weiterzukommen
- Große Umbauten ohne Rückfrage, Löschen von Tests, um „grün“ zu werden

---

## 13. Mini-Glossar

**Pivot** = Aufstellpunkt · **Grip** = Griffpunkt für die Hand · **Surface** = Abstellfläche mit Höhe · **Fixture** = fester Einbau · **Bodenband** = begehbarer Tiefenbereich des Bodens · **Platzhalter** = automatisch erzeugtes Ersatzbild in exakter cm-Größe · **Rolle** = NPC-Vorlage (z. B. Kassierer/in) · **Vertical Slice** = kleiner, aber komplett fertiger Teil · **MVP** = erste veröffentlichbare Version
