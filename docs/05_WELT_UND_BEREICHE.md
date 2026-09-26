# 05 · Welt & Bereiche 🗺️
> 🔒 = fest eingebaut (im Hintergrund oder als Fixture, nicht bewegbar) · ✋ = bewegbar (Item) · 🤖 = fester NPC (Rolle)
> Item-Ziel = Anzahl inkl. Varianten. Vorlagen ≈ 35 % davon.

## Übersicht

| # | Bereich | Phase | Szenen | Items | Feste NPCs | Kamera (cm) |
|---|---|---|---|---|---|---|
| 1 | Zuhause & Garten | 07 (Slice) | 10 | 190 | 2 | 300 / Garten 400 |
| 2 | Einkaufsstraße inkl. Blumenladen | 09 (MVP) | 10 | 200 | 11 | 300 / Straße 450 |
| 3 | Spielplatz & Park | 09 (MVP) | 3 | 45 | 4 | 450 |
| 4 | Schule & Pausenhof | 10a | 9 | 80 | 7 (+8 NPC-Kinder) | 300 / Hof 450 |
| 5 | Gesundheitszentrum | 10b | 11 | 100 | 10 | 300 / Dach 500 |
| 6 | Freizeitbad | 10c | 6 | 55 | 4 | 350 / Sprungturm 700 |
| 7 | Rummelplatz | 10d | 8 | 60 | 6 | 450 / Riesenrad 700 |
| 8 | Sportzentrum | 10e | 7 | 60 | 5 | 350 / Platz 500 |
| 9 | Eishalle | 10f | 4 | 40 | 4 | 400 |
| 10 | Zoo | 10g | 9 | 70 | 5 (+20 Tierarten) | 450 / Savanne 700 |
| 11 | Werkstatt | 10h | 5 | 70 | 4 | 350 |
| – | Global (Rucksack, Handy, Kamera, Fahrzeuge) | 05/09 | – | 30 | – | – |
| | **Summe** | | **82** | **1.000** | **62** | |

**Rollen-Vorlagen (15):** `cashier` · `shelf_stocker` · `lifeguard` · `teacher` · `janitor` · `doctor` · `nurse` · `coach` · `supervisor` · `mechanic` · `florist` · `zookeeper` · `ride_operator` · `vendor` · `receptionist`. Alle 62 NPCs sind Instanzen dieser Rollen.

---

## 1 · Zuhause & Garten (Vertical Slice, Phase 07)
- **Szenen:** Flur · Wohnzimmer · Küche + Essbereich · Elternschlafzimmer · Kinderzimmer 1 · Kinderzimmer 2 · Bad · Dachboden (Geheimraum) · Keller/Waschküche · Garage · Garten (Baumhaus, Gewächshaus, Planschbecken, Grill)
- **🔒 Einbauten:** Küchenzeile, Herd, Spüle, Kühlschrank, Badewanne, Dusche, Toilette, Waschbecken, Treppen, Türen, Fenster
- **Besonderheit:** Im Zuhause sind **Möbel ✋ bewegbar** (Sofa, Betten, Tische, Stühle, Schränke). Tapete und Boden sind wählbar (je 12).
- **🤖:** Nachbarin (`vendor`-Variante „winkt am Zaun“), Postbote (bringt alle 5 Min. ein Paket mit einem Zufalls-Item aus dem Zuhause-Pool)
- **Interaktionen:** Kochen (Rezepte), Licht an/aus, Wasserhahn, Badeschaum, Waschmaschine, TV (Farb-Animationen), Gießen → Pflanze wächst (3 Stufen), Gemüsebeet ernten, Schlafen (Figur liegt, Zzz)

## 2 · Einkaufsstraße inkl. Blumenladen (MVP, Phase 09)
- **Szenen:** Straße (Brunnen, Bänke, Bushaltestelle = Bereichswechsel) + 9 Läden: Supermarkt · Bäckerei & Café · **Blumenladen mit Gewächshaus** · Modeladen (Kleidung wirkt direkt auf die Figur) · Friseur (ändert die Frisur live) · Spielzeugladen · Tierhandlung · Eisdiele · Musik-/Elektroladen
- **🔒:** Theken, Kassen, Regale, Kühlregal, Umkleide, Friseurstuhl, Ofen der Bäckerei
- **🤖:** 9 × `cashier` (einer pro Laden), `shelf_stocker` (Supermarkt), `florist` (bindet Sträuße, gießt), Friseurin (`vendor`-Variante)
- **Kassen-Logik:** Figur + Item an die Kasse → NPC scannt (Piep), Kassenlade, Tüte ✋ erscheint mit den Items. **Spielgeld unbegrenzt**, es gibt keine Wirtschaft.

## 3 · Spielplatz & Park (MVP, Phase 09)
- **Szenen:** Spielplatz (Rutsche, Schaukeln, Wippe, Karussell, Sandkasten, Klettergerüst) · Teich mit Enten · Picknick-/Hundewiese mit Eiswagen
- **🤖:** Eisverkäufer (`vendor`), Parkwächter (`supervisor`), Jogger (läuft Runden), Oma füttert Enten
- **Tiere:** Enten (schwimmen, schnattern, flüchten), Tauben, Eichhörnchen
- **Interaktionen:** Sand formen (3 Förmchen), Schaukeln (Figur rastet ein, schwingt), Rutschen, Seifenblasen, Drachen

## 4 · Schule & Pausenhof (10a)
- **Szenen:** Eingangshalle mit Spinden · 2 Klassenzimmer · Musikraum · Kunstraum · NaWi-Raum · Turnhalle · Mensa · Lehrerzimmer · Pausenhof (Klettergerüst, Tischtennis, Hüpfkästchen, Schulgarten)
- **🤖:** Lehrerin (`teacher`), Musiklehrer, Kunstlehrerin, Hausmeister (`janitor`), Mensa-Koch (`vendor`), Schulleiterin, Pausenaufsicht (`supervisor`) + 8 NPC-Kinder
- **Interaktionen:** **Tafel bemalbar**, Schulglocke startet die Pause (NPC-Kinder gehen auf den Hof), Instrumente, Vulkan-Experiment

## 5 · Gesundheitszentrum (10b)
- **Szenen:** Empfang/Wartezimmer · Hausarzt · Zahnarzt · Kinderarzt · Tierarzt · Röntgen · Notaufnahme · Babystation · Patientenzimmer · Cafeteria · Dach mit Hubschrauber · Apotheke
- **🤖:** Empfang (`receptionist`), 4 × `doctor`, 2 × `nurse`, Apothekerin (`cashier`), Rettungssanitäter, Hebamme
- **Interaktionen:** Röntgen zeigt lustige Dinge im Bauch, Pflaster, Gips, Fieber messen, Baby wiegen, Tiere behandeln. **Nie gruselig, kein Blut.**

## 6 · Freizeitbad (10c)
- **Szenen:** Kasse & Umkleiden · Schwimmerbecken · Babybecken · Sprungturm (1/3/5 m) · Rutsche · Whirlpool · Liegewiese mit Kiosk
- **🤖:** **Bademeister** (`lifeguard`: läuft den Beckenrand ab, setzt sich auf den Hochstuhl, pfeift bei Rennen, holt Figuren nach 10 s unter Wasser mit dem Rettungsring), Kassiererin, Kiosk, Schwimmlehrerin
- **Interaktionen:** Schwimmen/Tauchen, Wellen und Spritzer, nasse Figuren tropfen und trocknen

## 7 · Rummelplatz (10d)
- **Szenen:** Eingang · Riesenrad · Autoscooter · Karussell · Achterbahn · Geisterbahn (lustig) · Buden · Bühne
- **🤖:** 4 × `ride_operator`, Losverkäuferin, Zuckerwatte (`vendor`), Clown, Zauberer
- **Interaktionen:** Figur ins Fahrgeschäft setzen → Fahrt startet. Gewinne (Plüsch) sind ✋ und können mit nach Hause.

## 8 · Sportzentrum (10e)
- **Szenen:** Empfang · Fitness · Sporthalle · Fußballplatz mit Tribüne · Tennis · Kletterwand · Ballettraum
- **🤖:** Fußballtrainer (`coach`: Hütchen, Pfiff, Jubel bei Tor), Fitnesstrainerin (`coach`), Aufsicht Kletterwand (`supervisor`: sichert Figuren), Ballettlehrerin, Empfang
- **Interaktionen:** Ball-Physik mit Tor-Erkennung, Anzeigetafel, Pokale ✋

## 9 · Eishalle (10f)
- **Szenen:** Kasse & Verleih · Eisfläche · Tribüne · Imbiss
- **🤖:** Verleih (tauscht Schuhe), Eislauf-Trainerin (Pirouetten), **Eismaschinen-Fahrer** (alle 3 Min., Eis glänzt danach), Imbiss
- **Interaktionen:** Figuren rutschen (eigene Reibung), Eishockey, Disco-Licht-Modus

## 10 · Zoo (10g)
- **Szenen:** Eingang · Savanne (Giraffe, Zebra, Löwe) · Affenhaus · Elefanten · Pinguine · Reptilien · Aquarium · Streichelzoo · Tierbaby-Station
- **🤖:** Direktorin, 2 × `zookeeper` (Fütterung zu festen Zeiten), Guide, Kasse
- **Tiere:** **echte Größen** (Giraffe 480 cm → Kamera zoomt raus). Streichelzoo-Tiere sind ✋ tragbar (Ziege, Kaninchen).
- **Interaktionen:** Richtiges Futter → Freude. Affen klauen manchmal ein Item und legen es woanders ab.

## 11 · Werkstatt (10h)
- **Szenen:** Autowerkstatt mit Hebebühne · Waschanlage · Tankstelle mit Shop · Lackiererei · Fahrradwerkstatt · Schrottplatz (Geheimnisse)
- **🤖:** 2 × `mechanic`, Tankwart (`cashier`), Waschanlage (`vendor`)
- **Interaktionen:** Fahrzeug-Baukasten (Räder, Farbe, Hupe), das Auto ist in anderen Bereichen nutzbar, Waschen, Tanken, Reifenwechsel

---

## Globale Inhalte
- **Figuren-Editor:** 3 Körper-Schablonen × Hauttöne (12) · Frisuren (40 zum Start, bis 80) · Haarfarben (24) · Augen (20) · Münder (15) · Kleidung (200 zum Start, bis 400, je 2–3 Farbzonen) · Accessoires (60) · Hilfsmittel (Rollstuhl, Brille, Hörgerät, Prothese)
- **Haustiere:** Hund (4 Formen), Katze (3), Vogel, Kaninchen, Hamster, Meerschweinchen, Fisch, Schildkröte, Pony, Mini-Drache, Mini-Einhorn. Charakterzug: verspielt / verschlafen / neugierig / verfressen / schüchtern
- **Sammel-Album:** 5–10 Geheimnisse pro Bereich, alle nur erspielbar
