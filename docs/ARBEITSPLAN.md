# 🗺️ ARBEITSPLAN · Kunterbunt City

> Automatisch erzeugt aus `docs/phasen/` durch `tools/github_setup.py`. Live-Stand: **Issues & Meilensteine** auf https://github.com/MarsCommanderM/Kunterbunt-City

Rhythmus: Agent baut eine Phase → Phasenbericht → 👤 prüft → nächste Phase.

## Phase 00 · Setup & Werkzeuge
*Ein sauberes, testbares Godot-Projekt, in dem jede spätere Phase sicher gebaut werden kann.*  
Bauplan: `docs/phasen/PHASE_00_SETUP.md`

- [ ] **P00-T01** project.godot anlegen: Name „Kunterbunt City“, Renderer Compatibility, 1920×1080, Stretch canvas_items/expand, Querformat
- [ ] **P00-T02** Ordnerstruktur exakt nach MASTERPROMPT §4 anlegen (leere Ordner mit .gitkeep)
- [ ] **P00-T03** .gitignore (Godot: .godot/, *.import-Cache nach Godot-Empfehlung, export/, Python: __pycache__/, .venv/)
- [ ] **P00-T04** GUT installieren nach addons/gut/ (aus dem offiziellen GUT-Repository, MIT, Version passend zu Godot 4), Plugin aktivieren, Beispieltest tests/test_smoke.gd
- [ ] **P00-T05** Python: tools/requirements.txt (pillow, numpy, scipy, pytest, pyyaml), tools/tests/test_validate_scale.py testet validate_scale.py (grün mit Originaldaten, rot mit manipulierter Kopie „Hund 90 cm“)
- [ ] **P00-T06** tests/test_no_network.gd: durchsucht alle .gd in res://src nach verbotenen Klassen (siehe Tech-Spec §6)
- [ ] **P00-T07** Autoload-Gerüste anlegen (leer, typisiert, mit Doc-Kommentar): Log, Settings, ItemDB, SaveSystem, Game, SceneRouter, AudioBus
- [ ] **P00-T08** Export-Presets: Web (Threads aus), Android (Querformat), Windows/Linux/macOS, export/ ignoriert
- [ ] **P00-T09** scripts/check.sh (+ check.ps1 für Windows): führt Maßstab-Prüfer, pytest und GUT headless aus, Exit-Code ≠ 0 bei Fehlern
- [ ] **P00-T10** Optional: .github/workflows/ci.yml führt check.sh headless aus (Godot per frei verfügbarem Docker-Image oder Download)
- [ ] **P00-T11** CREDITS.md anlegen (GUT, Godot, Python-Pakete mit Lizenz)
- [ ] **P00-T12** docs/PROGRESS.md ausfüllen

**Abnahme:**
- [ ] `scripts/check.sh` läuft durch: Maßstab ✅, pytest ✅ (mind. 2 Tests), GUT ✅ (Smoke + No-Network)
- [ ] Projekt öffnet sich in Godot ohne Fehler/Warnungen im Output
- [ ] Web-Export lässt sich erzeugen (leere Szene) und lokal starten (`python3 -m http.server` im Export-Ordner)
- [ ] Ordnerstruktur = MASTERPROMPT §4

## Phase 01 · Welt-Maßstab, Raum & Kamera
*Eine Welt in Zentimetern, in der jede Größe automatisch stimmt. Dazu ein Test-Raum, in dem man scrollt und zoomt.*  
Bauplan: `docs/phasen/PHASE_01_WELT_MASSSTAB.md`

- [ ] **P01-T01** src/core/units.gd: Konstanten und Helfer (cm ↔ Einheiten = 1:1, depth_factor(), camera_zoom_for_height()) + GUT-Tests
- [ ] **P01-T02** ItemDB lädt data/scale_table.json und stellt get_scale(ref) -> Dictionary bereit. Unbekannte Referenz = klarer Fehler
- [ ] **P01-T03** src/world/room.gd + room.tscn: Maße aus data/areas/*.json (Breite/Höhe cm), Kinder-Nodes nach Tech-Spec §3.2/MASTERPROMPT §6
- [ ] **P01-T04** src/world/world_camera.gd: sichtbare Höhe 300 cm (Standard), Pinch-Zoom und Mausrad (Grenzen aus Raumdaten), horizontales Wisch-Scrollen mit Trägheit, Grenzen = Raumränder
- [ ] **P01-T05** src/world/floor_band.gd: hintere und vordere Bodenlinie, depth_factor(y) max. 1,12, Visualisierung im Debug-Modus
- [ ] **P01-T06** src/world/surface.gd: Oberfläche (Typ, x-Bereich, Höhe cm, Tiefe), Debug-Zeichnung
- [ ] **P01-T07** data/areas/test_kitchen.json + Test-Raum: Hintergrund reference/raw_kitchen_bg.png, eingemessen mit Arbeitsplatte 90 cm (px 434 → 600, Maßstab-Bibel §6), Bodenband, Arbeitsplatte als Surface
- [ ] **P01-T08** tools/asset_pipeline/calibrate_bg.py (erste Version, Ordner anlegen): liest calibration aus der Raum-JSON, skaliert den Hintergrund auf 8 px/cm, schreibt nach assets/backgrounds/…
- [ ] **P01-T09** Maßstab-Testszene src/debug/scale_test.tscn: Platzhalter-Rechtecke für char_child, pet_dog_medium, home_table_dining, food_apple, toy_football automatisch aus der Tabelle + cm-Lineal
- [ ] **P01-T10** Debug-Overlay (Taste F3 / 3-Finger-Tipp in Debug-Builds): Raster 10 cm, Oberflächen, Bodenband, FPS

**Abnahme:**
- [ ] Pflicht-Tests aus Tech-Spec §6 angelegt und grün: `tests/test_depth.gd`
- [ ] In der Testszene: Hund (45) < Tisch (75) < Arbeitsplatte (90) < Kind (125), am Lineal nachmessbar
- [ ] Kamera zeigt 300 cm Höhe bei Standard-Zoom (Test: Sichtbereich ±2 cm)
- [ ] Tiefen-Faktor: hinten 1,00, vorne 1,12, nie größer (GUT-Test)
- [ ] Der eingemessene Hintergrund hat die Arbeitsplatte auf 90 cm ±2 cm
- [ ] Scrollen und Zoomen funktionieren mit Maus **und** Touch-Emulation
- [ ] `check.sh` grün

## Phase 02 · Item-System & Drag-and-Drop
*Das Kern-Gefühl: Items anfassen, anheben, ziehen, sauber abstellen, stapeln, in Behälter legen, rückgängig machen. Es muss sich *perfekt* anfühlen.*  
Bauplan: `docs/phasen/PHASE_02_ITEMS_DRAGDROP.md`

- [ ] **P02-T01** tools/make_placeholders.py: pro scale_table-Eintrag ein PNG (8 px/cm, abgerundet, Kategorie-Farbe, Umriss, Kurzname + „20 cm“) nach assets/placeholders/ + pytest
- [ ] **P02-T02** ItemDefinition (Resource) + Laden aller data/items/*.json in ItemDB, Validierung (scale_ref, grip bei hold ≠ none, Sprite existiert, sonst Platzhalter)
- [ ] **P02-T03** ItemNode (item_node.tscn): Sprite in Weltgröße (Maßstab-Bibel §1), Pivot-Offset, Tippfläche min. 48 dp (unabhängig von der Grafik), weicher Kontaktschatten
- [ ] **P02-T04** DragController: Zustände IDLE/PRESS/LIFT/DRAG/DROP (Tech-Spec §4.1), Anheben mit Hüpf-Effekt, Multitouch bis 3 Items
- [ ] **P02-T05** Drop-Logik: Oberfläche unter dem Item finden → Pivot exakt auf der Oberflächenhöhe; sonst sanft auf die nächste Fläche darunter fallen (≤ 0,4 s)
- [ ] **P02-T06** Platzierungsregeln: placement + Größe (≤ 60 cm auf Tischen, S-11); passt ein Item nicht → federt zurück auf den Boden
- [ ] **P02-T07** Stapeln (stackable, max. 8) und Container (Kühlschrank, Schrank, Tasche: Slots, öffnen/schließen per Tipp, verschachtelt max. 2 Ebenen)
- [ ] **P02-T08** UndoStack (30 Schritte pro Raum) + Rückgängig-Button im HUD
- [ ] **P02-T09** Tiefe: Items im Bodenband per y sortiert und skaliert (Faktor aus Phase 01)
- [ ] **P02-T10** Test-Raum mit 60 Platzhalter-Items aus data/items/home_kitchen_demo.json + Platzhaltern (Küche)
- [ ] **P02-T11** Sounds-Hooks: pickup/drop je Material (vorerst Platzhalter-Töne mit jsfxr erzeugt, CC0/eigene)
- [ ] **P02-T12** Performance-Test: 250 Items im Raum, 60 FPS Desktop, Messung in PROGRESS.md

**Abnahme:**
- [ ] Pflicht-Tests aus Tech-Spec §6 angelegt und grün: `tests/test_scale.gd` + `tests/test_drag_drop.gd`
- [ ] Apfel auf die Arbeitsplatte ziehen → steht exakt auf 90 cm (GUT ±0,5 cm)
- [ ] Apfel ins Leere loslassen → fällt auf den Boden, nie aus der Welt
- [ ] Ein Ei (6 cm) ist mit dem Finger gut greifbar (Tippfläche ≥ 48 dp)
- [ ] 3 Items gleichzeitig ziehbar (Touch-Emulation)
- [ ] Rückgängig stellt 30 Aktionen wieder her
- [ ] 250 Items → ≥ 60 FPS (Desktop)
- [ ] `check.sh` grün

## Phase 03 · Figuren & Haustiere (Grundsystem)
*Figuren, die man ziehen, hinsetzen, hinlegen und Items richtig in die Hand geben kann. Dazu ein Basis-Haustier.*  
Bauplan: `docs/phasen/PHASE_03_FIGUREN_TIERE.md`

- [ ] **P03-T01** CharacterRig aus Ebenen: Körper, Kopf, Haare hinten/vorne, Augen, Mund, Oberteil, Hose, Schuhe, Arm hinten, Arm vorne, Hand vorne (eigene Ebene). Platzhalter-Teile passend zu char_*-Größen
- [ ] **P03-T02** 3 Schablonen: toddler (90), kid (125), adult (172). Größe nur aus der Tabelle
- [ ] **P03-T03** Posen: stand, hold_one (Arm vorne), hold_two (Arm vorne beidseitig), sit, lie. Wechsel mit kurzer Tween-Animation
- [ ] **P03-T04** HandSlot (rechts/links): Item übergeben → Grip auf HandSlot (±0,5 cm), Rotation hold_angle, Zeichenreihenfolge Arm < Item < Hand (Tech-Spec §4.2)
- [ ] **P03-T05** SeatSlot: Stuhl, Sofa, Bett (Pose sit/lie), Einrasten im Radius 30 cm, Sitzhöhe aus der Tabelle (Stuhl 45 cm). Items (Teddy) können ebenfalls sitzen
- [ ] **P03-T06** Figur ziehen: am Körper greifen, hängt lustig am Griffpunkt (leichtes Pendeln), Absetzen auf dem Bodenband
- [ ] **P03-T07** Emotionen: 6 Gesichter (fröhlich, lachend, überrascht, traurig, müde, verliebt), Tipp auf den Kopf wechselt; Reaktionen auf Essen (Mampf-Animation)
- [ ] **P03-T08** Tiefen-Faktor gilt für Figuren genauso wie für Items (Test: Figur vorne und Tisch vorne behalten das Verhältnis)
- [ ] **P03-T09** PetNode + einfaches Verhalten: sitzen, laufen, folgt der Figur, Tipp → Laut (über AudioBus-Limiter). Hund mittel 45 cm
- [ ] **P03-T10** Szene „Küche Maßstab“ nachbauen wie reference/kueche_stil_c_massstab.png, mit den echten Sprites aus reference/sprites/ (Figur-Sprite dort nur als Einzelbild)

**Abnahme:**
- [ ] Pflicht-Tests aus Tech-Spec §6 angelegt und grün: `tests/test_hand.gd`
- [ ] Karotte in die Hand → Finger liegen über der Karotte, Karotte ≈ 20 cm (neben Kind 125 cm) – Screenshot
- [ ] Teddy auf dem Stuhl sitzt auf 45 cm Sitzhöhe
- [ ] Hund ist in jeder Tiefe kleiner als der Tisch (Test)
- [ ] Figur setzt sich auf Stuhl/Sofa, legt sich ins Bett
- [ ] Nachbau der Referenz-Küche wirkt proportional identisch (👤 Blick-Check)
- [ ] `check.sh` grün

## Phase 04 · Charakter- & Haustier-Editor
*Beim ersten Start muss eine eigene Figur erstellt werden. Danach unbegrenzt Figuren und Haustiere erstellen, bearbeiten und löschen.*  
Bauplan: `docs/phasen/PHASE_04_EDITOR.md`

- [ ] **P04-T01** Datenformat data/character_parts/*.json: Slot (hair_front, hair_back, eyes, mouth, top, bottom, shoes, accessory, aid), Schablone, Farbzonen (bis 3), Sprite-Pfade, Tags
- [ ] **P04-T02** Figur-Datenmodell CharacterData (Schablone, Hautton, Teile + Farben, Name, Stimme 1–8) ↔ JSON, Speichern über SaveSystem
- [ ] **P04-T03** Editor-UI (src/ui/character_editor/): links große Vorschau (reagiert mit Emotionen), rechts Kategorien als Symbole, unten Farbpalette. Kein Lese-Zwang
- [ ] **P04-T04** Umfärben per Shader (Farbzonen-Maske R/G/B im Teil-Sprite → Farbe aus Palette)
- [ ] **P04-T05** 🎲 Zufallsknopf (würfelt stimmige Kombination), 5 Outfit-Plätze pro Figur
- [ ] **P04-T06** Namens-Auswahl: 200 Namen als Bild-Kacheln + Würfel. Freie Eingabe nur hinter dem Eltern-Tor, lokaler Wortfilter
- [ ] **P04-T07** Pflicht-Ablauf: erster Start → Editor → „Fertig“-Haken aktiv erst, wenn Schablone + Hautton gewählt sind → danach Startmenü
- [ ] **P04-T08** Figuren-Galerie: unbegrenzt, Ordner (Familie, Freunde …), duplizieren, löschen (mit Sicherheitsabfrage per Symbol)
- [ ] **P04-T09** Haustier-Editor: Tierart (Tabelle pet_*), Fell/Farbe, Muster, Halsband, Charakterzug (verspielt/verschlafen/neugierig/verfressen/schüchtern)
- [ ] **P04-T10** Platzhalter-Teile: je Slot 5 Varianten als Platzhalter (echte Stil-C-Teile kommen über die Pipeline in Phase 06/07)

**Abnahme:**
- [ ] Ohne eigene Figur ist kein Bereich betretbar (Test)
- [ ] 100 Figuren speichern/laden ohne Ruckeln
- [ ] Umfärben funktioniert pro Teil mit 3 Zonen
- [ ] Größe der Figur hängt nur von der Schablone ab (Kind immer 125 cm)
- [ ] Editor ist ohne Lesen bedienbar (👤 Kindertest mit 1 Kind)
- [ ] `check.sh` grün

## Phase 05 · Startmenü (Stadtkarte), Speichern, Bereichswechsel
*Der komplette Spielfluss: App-Start → (Pflicht-Editor) → Stadtkarte mit einem Button pro Bereich → Spawn im Bereich → zurück zur Karte. Alles wird gespeichert.*  
Bauplan: `docs/phasen/PHASE_05_MENU_SAVE.md`

- [ ] **P05-T01** Splash (max. 3 s, überspringbar) → Prüfung „eigene Figur vorhanden?“ → Editor oder Stadtkarte
- [ ] **P05-T02** Stadtkarte (src/ui/main_menu/): 11 große Bereichs-Buttons (mind. 120×120 px @1080p) mit Bild, Symbol und eigenem Sound. Bereiche ohne Inhalt: sichtbar, aber mit einer freundlichen „Baustelle“-Animation statt Schloss
- [ ] **P05-T03** Umschaltbar: Karte (illustriert) / Raster (übersichtlich für Kleine)
- [ ] **P05-T04** Oben: Figuren-Button, Rucksack-Button, Album-Button, Eltern-Button (Eltern-Tor)
- [ ] **P05-T05** SceneRouter: Ladebildschirm (< 2 s, mit Mini-Animation), Spawn am spawn-Punkt des Bereichs mit Ankunfts-Animation (Tür/Bus), aktive Figur + gewählte Haustiere
- [ ] **P05-T06** In jedem Bereich: Karten-Button oben links (zurück), Rucksack unten rechts, Rückgängig
- [ ] **P05-T07** SaveSystem komplett: Raumzustände, Figuren, Haustiere, Rucksack, Album. Autosave bei jeder Änderung (entprellt 2 s) + beim Verlassen. 3 Welt-Slots
- [ ] **P05-T08** save_version + Migrationen + Tests mit Beispieldateien in tests/fixtures/
- [ ] **P05-T09** Eltern-Tor: Rechenaufgabe mit Zahlen-Symbolen oder „3 Finger 3 Sekunden halten“
- [ ] **P05-T10** Einstellungen (hinter dem Tor): Lautstärken (Musik/Effekte/Tiere), große UI, reduzierte Animation, Sprache, Bereich zurücksetzen (🪄), Speicherstand exportieren/importieren (Datei, ohne Internet)
- [ ] **P05-T11** Rucksack (Tech-Spec §4.7): 20 Plätze, Items wandern zwischen Bereichen

**Abnahme:**
- [ ] Pflicht-Tests aus Tech-Spec §6 angelegt und grün: `tests/test_save_migration.gd` + Fixtures in `tests/fixtures/`
- [ ] Kompletter Ablauf ohne Lesen bedienbar
- [ ] Bereichswechsel < 2 s (Messung)
- [ ] App schließen und neu starten → alles exakt wie vorher (Positionen ±0,1 cm)
- [ ] Alte Speicherdatei (v1-Fixture) lädt nach einer Format-Änderung korrekt
- [ ] Web-Build speichert im Browser (Seite neu laden → Zustand bleibt)
- [ ] `check.sh` grün

## Phase 06 · Asset-Pipeline (produktiv)
*Aus KI-Bildern werden mit einem Befehl fertige, maßstabsgetreue Sprites samt Item-JSON und Atlas, inklusive automatischer Prüfung.*  
Bauplan: `docs/phasen/PHASE_06_ASSET_PIPELINE.md`

- [ ] **P06-T01** tools/asset_pipeline/cutout.py aus der Demo übernehmen und härten: Loch-Regel (> 500 px, Mittelwert > 250), Modus character (keine Löcher), Kanten-Entmischung + pytest mit Testbildern (Augenweiß bleibt, Henkel wird transparent)
- [ ] **P06-T02** split.py: Objekte finden, Zeilen über die vertikale Mitte, Anzahl == YAML, sonst Fehler mit Vorschaubild der gefundenen Objekte
- [ ] **P06-T03** scale.py: Höhe aus scale_table × scale_mul, Breite aus dem Seitenverhältnis, Warnung bei > 30 % Abweichung
- [ ] **P06-T04** points.py: Pivot + Grip-Vorgaben je Kategorie (z. B. Tasse → Henkel = rechte Kante 45 % Höhe), Vorschaubild mit markierten Punkten zum Korrigieren (YAML-Override)
- [ ] **P06-T05** export.py: 8 px/cm, 4 px Padding, assets/sprites/<bereich>/…png, Item-JSON in data/items/ (bestehende Einträge aktualisieren, nicht duplizieren)
- [ ] **P06-T06** atlas.py: Atlas pro Bereich (≤ 4096², Godot-kompatibel) + Import-Einstellungen
- [ ] **P06-T07** calibrate_bg.py (aus Phase 01) fertigstellen: Hintergründe einmessen, in Kacheln ≤ 2048 px zerlegen
- [ ] **P06-T08** lineup.py: alle Items eines Bereichs + Kind + Hund + Tisch am cm-Lineal → docs/tests/lineup_<bereich>.png
- [ ] **P06-T09** scene_test.py: Test-Komposition wie die Referenz-Küche (Kind hält ein Item, Teddy auf dem Stuhl, Items auf dem Tisch)
- [ ] **P06-T10** run.py incoming/<bereich>/ = alles in einem Durchlauf (2→8) + Zusammenfassung (neu/aktualisiert/Warnungen)
- [ ] **P06-T11** Figurenteile-Modus: Differenz Teil-Bild − Schablone → Teil-Ebene, Ausrichtung an Schablonen-Ankern (Kopf, Hals, Hüfte, Hände)
- [ ] **P06-T12** Anleitung docs/asset_settings.md für 👤: ComfyUI-Einstellungen, Stil-Block, Negativ-Prompt, LoRA-Training (kostenlos)

**Abnahme:**
- [ ] `python3 tools/asset_pipeline/run.py reference/` erzeugt aus den Demo-Rohbildern dieselben 18 Sprites + JSON wie die Referenz
- [ ] Maßstab-Prüfer grün, keine Seitenverhältnis-Warnung für die Demo-Items
- [ ] Lineup- und Test-Szenen-Bild werden erzeugt
- [ ] Neues Blatt → im Spiel sichtbar, ohne Code-Änderung
- [ ] pytest-Abdeckung für cutout/split/scale
- [ ] `check.sh` grün

## Phase 07 · Vertical Slice „Zuhause & Garten“
*Ein kompletter Bereich in finaler Qualität (Stil C). Er ist der Maßstab für alle weiteren Bereiche.*  
Bauplan: `docs/phasen/PHASE_07_SLICE_ZUHAUSE.md`

- [ ] **P07-T01** data/areas/home.json: 11 Szenen (Flur, Wohnzimmer, Küche, Eltern-SZ, 2 Kinderzimmer, Bad, Dachboden, Keller, Garage, Garten), Türen zwischen Räumen, Spawn Flur
- [ ] **P07-T02** Pro Raum: Hintergrund (👤 generiert) eingemessen, Oberflächen, SeatSlots, Container, Fixtures
- [ ] **P07-T03** 190 Items (≈ 65 Vorlagen + Varianten) als Item-JSON. Solange Grafik fehlt: Platzhalter. Jeder Eintrag mit scale_ref
- [ ] **P07-T04** Möbel im Zuhause bewegbar (Ausnahme laut Welt-Doku). Tapete und Boden wählbar (12 + 12)
- [ ] **P07-T05** Fixtures: Herd (an/aus, Topf blubbert), Ofen, Spüle (Wasser), Kühlschrank (Container), Badewanne (Schaum), Dusche, Toilette (Spülen-Sound), Waschmaschine, Licht-Schalter pro Raum, TV
- [ ] **P07-T06** RecipeSystem + 25 Rezepte (Spiegelei, Toast, Smoothie, Pizza, Kuchen, Salat …) datengetrieben
- [ ] **P07-T07** Garten: Pflanzen wachsen in 3 Stufen (Samen + Erde + Wasser), Gemüse ernten, Planschbecken, Baumhaus (SeatSlot oben, Leiter)
- [ ] **P07-T08** Nachbarin am Zaun und Postbote (einfach, echte KI kommt in Phase 08)
- [ ] **P07-T09** Audio: Musik (Tag), Ambiente pro Raum, Item-Sounds nach Material
- [ ] **P07-T10** 6 Geheimnisse (Dachboden-Truhe, Maus im Keller …) → Sammel-Album
- [ ] **P07-T11** Lineup docs/tests/lineup_home.png + Test-Szene pro Raum

**Abnahme:**
- [ ] Alle 11 Szenen begehbar, Wechsel über Türen
- [ ] 190 Items, 0 Maßstab-Fehler, 0 Seitenverhältnis-Warnungen bei echter Grafik
- [ ] 25 Rezepte funktionieren (GUT je Rezept)
- [ ] 60 FPS im vollsten Raum mit 250 Items (Desktop), ≥ 30 FPS Web auf Mittelklasse-Laptop
- [ ] 👤 **Kindertest** (2–3 Kinder, 15 Min.): keine Frust-Stellen, Protokoll in `docs/tests/`
- [ ] `check.sh` grün

## Phase 08 · NPC- & Tier-KI
*Feste Figuren arbeiten (kassieren, patrouillieren, behandeln, trainieren), Tiere haben ein Eigenleben, und nichts davon stört das Spielen.*  
Bauplan: `docs/phasen/PHASE_08_NPC_TIER_KI.md`

- [ ] **P08-T01** NpcStateMachine (Tech-Spec §4.5): Basis-Zustände idle/work/react/carried/return_to_post, Übergänge per Timer, Ereignis, Spieler
- [ ] **P08-T02** Rollen-Loader data/npc_roles/*.json + NPC-Loader data/npcs/*.json
- [ ] **P08-T03** Wegfindung im Raum: Bodenband als einfache Laufbahn (x/y innerhalb des Bands), Hindernisse = große Möbel; kein NavMesh-Overkill
- [ ] **P08-T04** Rollen implementieren: cashier, shelf_stocker, lifeguard, teacher, janitor, doctor, nurse, coach, supervisor, mechanic, florist, zookeeper, ride_operator, vendor, receptionist (je mit 2–4 Arbeits-Animationen, erst Platzhalter)
- [ ] **P08-T05** Tagesplan light: Laden öffnet (NPC schließt auf) – Standard „immer offen“ (Einstellung)
- [ ] **P08-T06** Garantien als Tests: NPC blockiert keinen Drop, verlässt nie den Raum, kehrt nach return_after_s zurück, reagiert beim Tragen
- [ ] **P08-T07** PetBrain (Tech-Spec §4.6): Bedürfnisse, Aktionen (Napf, Ball, Körbchen, folgen), Charakterzug beeinflusst die Gewichte
- [ ] **P08-T08** Tierlaute: Hund bellt (3 Varianten), Katze miaut/schnurrt beim Streicheln, Vogel zwitschert. Intervall 15–60 s + globaler Limiter 1 / 8 s
- [ ] **P08-T09** Hintergrund-Figuren (Badegäste, Passanten) als „leichte“ NPCs ohne Interaktion, max. 6 pro Szene
- [ ] **P08-T10** Performance: 15 aktive NPCs/Tiere + 250 Items → 60 FPS (Desktop)

**Abnahme:**
- [ ] Beispiel-Szene: Kassiererin scannt ein Item an der Kasse (Piep, Tüte erscheint)
- [ ] Bademeister-Test: läuft den Rand ab, pfeift bei rennender Figur, rettet nach 10 s unter Wasser (Platzhalter-Becken)
- [ ] Alle Garantie-Tests grün
- [ ] Nie mehr als 1 Tierlaut pro 8 s (Test)
- [ ] `check.sh` grün

## Phase 09 · MVP: Einkaufsstraße + Spielplatz → Release v0.1
*3 spielbare Bereiche (Zuhause, Einkaufsstraße inkl. Blumenladen, Spielplatz & Park), kostenlos veröffentlicht.*  
Bauplan: `docs/phasen/PHASE_09_MVP_RELEASE.md`

- [ ] **P09-T01** data/areas/shopping.json: Straße + 9 Läden (Welt-Doku §2), Bushaltestelle = Bereichswechsel mit Bus-Animation
- [ ] **P09-T02** 200 Items Einkaufsstraße (Supermarkt, Bäckerei, Blumenladen, Mode, Friseur, Spielzeug, Tierhandlung, Eisdiele, Musik)
- [ ] **P09-T03** Kassen-Logik (Rolle cashier): Item + Figur an die Kasse → Scan, Tüte ✋ mit Inhalt, unbegrenztes Spielgeld
- [ ] **P09-T04** Modeladen: Kleidung auf die Figur ziehen = anziehen (nutzt Editor-Teile). Friseur: Frisur ändern live
- [ ] **P09-T05** Blumenladen: florist bindet 3 Blumen zu einem Strauß (Rezept), Gewächshaus mit Wachstum
- [ ] **P09-T06** data/areas/playground.json: Spielplatz, Teich, Wiese. Schaukel/Rutsche/Wippe/Karussell als Fixtures mit SeatSlots und Bewegung
- [ ] **P09-T07** Enten-KI (schwimmen, schnattern, flüchten), Sand formen (3 Förmchen), Seifenblasen
- [ ] **P09-T08** Lineups + Test-Szenen für beide Bereiche
- [ ] **P09-T09** Release-Build: Web (itch.io-tauglich), Android APK, Windows/Linux/macOS. Version 0.1.0, Changelog
- [ ] **P09-T10** itch.io-Seite vorbereiten (Texte, Screenshots aus dem Spiel, Altersangabe, Datenschutz-Hinweis „sammelt keine Daten“) – Veröffentlichen macht 👤

**Abnahme:**
- [ ] 3 Bereiche, ~435 Items, 0 Maßstab-Fehler
- [ ] Web-Build läuft auf itch.io (Test-Upload als Entwurf) inkl. Speichern
- [ ] APK läuft auf einem Android-Tablet (👤)
- [ ] 👤 Kindertest mit 3–5 Kindern, keine Blocker
- [ ] `check.sh` grün

## Phase 10 · Content-Wellen (Bereiche 4–11)
*Die restlichen 8 Bereiche, jeder nach demselben Bereichs-Bauplan. Jeder Bereich ist eine eigene Unterphase mit eigenem Bericht.*  
Bauplan: `docs/phasen/PHASE_10_CONTENT_WELLEN.md`

- [ ] **10a** Schule & Pausenhof (Bereichs-Bauplan B-01…B-12)
- [ ] **10b** Gesundheitszentrum (Bereichs-Bauplan B-01…B-12)
- [ ] **10c** Freizeitbad (Bereichs-Bauplan B-01…B-12)
- [ ] **10d** Rummelplatz (Bereichs-Bauplan B-01…B-12)
- [ ] **10e** Sportzentrum (Bereichs-Bauplan B-01…B-12)
- [ ] **10f** Eishalle (Bereichs-Bauplan B-01…B-12)
- [ ] **10g** Zoo (Bereichs-Bauplan B-01…B-12)
- [ ] **10h** Werkstatt (Bereichs-Bauplan B-01…B-12)

**Abnahme:**
- [ ] Szenen vollständig, Item-Ziel erreicht, 0 Maßstab-Fehler
- [ ] NPC-Garantie-Tests grün
- [ ] ≥ 10 Interaktionen/Rezepte getestet
- [ ] Performance im Budget
- [ ] Lineup-Bild + Test-Szene in `docs/tests/`
- [ ] `check.sh` grün

## Phase 11 · Politur & Release 1.0
*Stabil, schnell, barrierearm, mehrsprachig, veröffentlicht.*  
Bauplan: `docs/phasen/PHASE_11_POLITUR_RELEASE.md`

- [ ] **P11-T01** Performance-Durchgang pro Bereich (Profiler), Atlas-Optimierung, Web-Download < 150 MB
- [ ] **P11-T02** Barrierefreiheit: Farbenblind-Modus, große UI, reduzierte Animation, Mono-Audio
- [ ] **P11-T03** Lokalisierung der wenigen Texte (Eltern-Bereich/Menüs): Deutsch, Englisch → danach Türkisch, Arabisch (RTL prüfen), Spanisch, Französisch, Polnisch, Ukrainisch
- [ ] **P11-T04** Speicherstand-Robustheit: kaputte Datei → Backup laden (2 rotierende Backups)
- [ ] **P11-T05** Stabilitätstest: 60 Min. automatisiertes Zufalls-Spielen (Bot zieht Items, wechselt Bereiche) ohne Absturz/Speicherleck
- [ ] **P11-T06** Datenschutzerklärung (kurz + kindgerecht): „Dieses Spiel sammelt keine Daten.“
- [ ] **P11-T07** Marken-Check Name (👤 DPMA/EUIPO), CREDITS.md vollständig (Modelle, CC0-Quellen, Tools)
- [ ] **P11-T08** Release 1.0: itch.io (Web/PC/Android), GitHub Pages (Web), optional F-Droid (Open Source)
- [ ] **P11-T09** Nach-1.0-Backlog anlegen: Tag/Nacht, Wetter, Jahreszeiten, Fotomodus, neue Bereiche (Bauernhof, Strand, Flughafen, Weltraum)

**Abnahme:**
- [ ] 11 Bereiche, ~1.000 Items, 62 NPCs, 0 Maßstab-Fehler
- [ ] Alle Budgets eingehalten (Tech-Spec §5)
- [ ] 60-Minuten-Bot-Test ohne Fehler
- [ ] 👤 Abschluss-Kindertest (5+ Kinder, 3 Altersgruppen)
- [ ] Release veröffentlicht
