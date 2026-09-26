# 01 · Kritische Überarbeitung des Blueprints (v1.3 → v2.0)

> Dieses Dokument erklärt **warum** sich das Projekt geändert hat. Es wurde aus 9 Perspektiven geprüft.
> Verbindlich für den Bau ist ab jetzt **`MASTERPROMPT.md`** + **`docs/phasen/`**. Der alte Blueprint ist nur noch Ideen-Sammlung.

---

## 1. Das größte Problem: Maßstab (gelöst)

| Fehler in v1.x | Folge | Neue Regel in v2.0 |
|---|---|---|
| Kleine Items wurden künstlich vergrößert („Spielmaßstab“ +80 %) | Apfel 14 cm, Ball 41 cm → Apfel wirkte fast wie ein Fußball | **Echte Größen.** Keine Vergrößerung. Greifbarkeit wird über eine **unsichtbare Tippfläche** gelöst (min. 48 dp), nicht über die Grafik |
| Vorne im Raum wurde alles um bis zu 54 % größer gezeichnet | Hund vorne wirkte größer als der Tisch hinten | **Tiefen-Skalierung max. +12 %** zwischen hinterster und vorderster Bodenlinie |
| Jedes KI-Bild hatte seine eigene Größe | Karotte wie ein Baseballschläger | **Jedes Item hat einen Eintrag in `data/scale_table.json`** (cm). Die Pixelgröße wird immer daraus berechnet, nie „nach Gefühl“ |
| KI-Räume waren zu hoch (über 4 m) | Figuren und Items wirkten winzig | **Kamera zeigt 300 cm Raumhöhe.** Hintergründe werden an einem Referenzmaß (Arbeitsplatte 90 cm / Tür 200 cm) **eingemessen** |
| Keine automatische Kontrolle | Fehler fielen erst beim Hinschauen auf | **`tools/validate_scale.py`** mit 43 Größen-Regeln (z. B. *Hund < Tisch*, *Apfel < Fußball*). Ist ein Test rot, darf nicht committet werden |

**Beweis:** `reference/kueche_stil_c_massstab.png` besteht aus 18 einzeln freigestellten Teilen, alle nach Tabelle skaliert. `reference/lineup_stil_c.png` zeigt alle Größen am cm-Lineal.

---

## 2. Die 9 Perspektiven

### 2.1 👧 Kind (4–10 Jahre) – „Verstehe ich das ohne Lesen?“
- ✅ Bleibt: kein Text nötig, große Buttons, keine Ziele, kein Game Over.
- 🔧 **Neu:** Echte Größen machen die Welt **begreifbar**. Ein Kind weiß, dass ein Apfel kleiner ist als ein Ball.
- 🔧 **Neu:** Aufgehobene Items bekommen einen **leichten Hüpf- und Leucht-Effekt**, damit auch kleine Dinge (Ei, Stift) gut sichtbar sind.
- 🔧 Kernzielgruppe **5–9 Jahre** (4–12 war zu breit). Ältere spielen trotzdem mit.
- ❌ Gestrichen: freie Texteingabe für Namen im Kinderbereich. Stattdessen gibt es eine **Namens-Auswahl** (200 Namen) plus einen Würfel. Freie Eingabe gibt es nur hinter dem Eltern-Tor.

### 2.2 👨‍👩‍👧 Eltern – „Ist das sicher?“
- ✅ Bleibt: keine Werbung, keine Käufe, kein Chat, keine Accounts, kein Internet nötig.
- ❌ **Gestrichen: Story-Rekorder mit Mikrofon.** Er braucht eine Mikrofon-Berechtigung, bringt Datenschutz-Risiko (Kinderstimmen) und Plattform-Aufwand. Er kommt auch nach 1.0 höchstens ohne Ton.
- 🔧 Fotomodus erst nach 1.0 (Speichern in die Galerie braucht Berechtigungen).
- 🔧 **Null Netzwerk-Code** im Spiel ist technisch erzwungen (Test prüft, dass keine HTTP-Klassen benutzt werden).

### 2.3 🎮 Game Design – „Macht das Kern-Gefühl Spaß?“
- 🔧 **Gefühl vor Menge.** Drag & Drop, Einrasten, Hinsetzen und In-die-Hand-geben müssen sich *perfekt* anfühlen, **bevor** Inhalte gebaut werden (Phasen 1–3).
- 🔧 „1.000 Items“ ist ehrlich gerechnet: **ca. 350 einzigartige Vorlagen + Farbvarianten und Zustände = 1.000**.
- 🔧 Kombinationen (Teig + Ofen = Brot) werden **datengetrieben** gebaut (`data/recipes/*.json`), nicht fest im Code.
- ❌ Tag/Nacht, Wetter und Jahreszeiten kommen **nach 1.0**. Sie sind schön, aber nicht Kern.

### 2.4 🎨 Art Direction – „Sieht es besser aus als Toca?“
- ✅ **Stil C (Premium Vektor)** ist festgelegt (`docs/03_STIL_GUIDE_C.md`).
- 🔧 **Nur Einbauten stehen im Hintergrund.** Alles, was man bewegen kann, ist ein eigenes Sprite.
- ⚠️ **Größtes Kunst-Risiko: Charakter-Editor.** Frei kombinierbare Frisuren und Kleidung müssen **exakt** auf dieselbe Körper-Schablone passen, und das schafft KI nicht zuverlässig allein.
  → Lösung: **3 Körper-Schablonen** (Kleinkind / Kind / Erwachsen) als feste Vorlage. Teile werden auf der Schablone generiert (img2img) und in Krita nachgebessert. **Weniger Körperformen, dafür sauber.** Mehr Formen erst nach 1.0.
- 🔧 Figuren haben **3 Posen als Einzelteile**: Arm unten, Arm vorne (hält Item), sitzend. Die Hand ist eine **eigene Ebene über dem gehaltenen Item**, so liegen die Finger sauber darüber.

### 2.5 🛠️ Technik – „Läuft das auf einem alten Tablet und im Browser?“
- 🔧 **Godot 4 (aktuelle stabile 4.x, mind. 4.4)**, Renderer **„Compatibility“** (WebGL2, ältere Tablets). „Forward+“ wäre für Web und Mobil zu schwer.
- 🔧 **Web-Export ohne Threads** (Thread Support aus). Dann sind keine speziellen Server-Header nötig, und das Spiel läuft auf itch.io und GitHub Pages.
- 🔧 **1 Godot-Einheit = 1 cm.** Die Kamera-Zoomstufe rechnet das auf den Bildschirm um. Damit gibt es nie mehr „Pixel-Größen nach Gefühl“.
- 🔧 **Texturen:** Sprites in 2× Auflösung (Referenz 4 px/cm → Quelle 8 px/cm), pro Bereich ein **Atlas**, VRAM-Kompression. Budget: **< 250 MB RAM pro Bereich**, Web-Download **< 150 MB**.
- 🔧 Speichern über `user://` (im Browser automatisch IndexedDB). Speicherstände haben eine **Versionsnummer und Migration**.

### 2.6 🤖 KI-Verhalten – „Schafft ein Solo-Entwickler 60 NPCs?“
- 🔧 **Keine Behavior Trees.** Einfache, testbare **Zustandsmaschinen** mit **Rollen-Vorlagen**. Zum Beispiel ist „Kassierer/in“ **eine** Vorlage, die 9 Läden benutzen. Aus ca. 60 NPCs werden so **ca. 15 Rollen**.
- 🔧 NPCs kehren **immer** an ihren Arbeitsplatz zurück, blockieren nie und reagieren auf Tragen und Absetzen.
- 🔧 Tierlaute sind **mengenbegrenzt**: max. 1 Tierlaut alle 8 Sekunden pro Szene.

### 2.7 📦 Umfang & Zeit – „Ist das machbar?“
- 🔧 **MVP = 3 Bereiche** (Zuhause, Einkaufsstraße inkl. Blumenladen, Spielplatz) → Release v0.1 kostenlos auf itch.io.
- 🔧 Die restlichen 8 Bereiche kommen in **Content-Wellen**, jeweils nach demselben **Bereichs-Bauplan** (Phase 10).
- 🔧 **Code und Kunst sind entkoppelt:** Der Agent baut alles zuerst mit **Platzhalter-Grafiken in exakter cm-Größe**. Die echte Stil-C-Grafik wird später eingetauscht, ohne dass Code geändert werden muss.

### 2.8 ⚖️ Recht – „Gibt es Ärger?“
- 🔧 Kein „Toca“ in Name, Code, Dateinamen oder Prompts. Der Arbeitstitel „Kunterbunt City“ wird vor Release markenrechtlich geprüft (DPMA/EUIPO).
- 🔧 KI-Modelle nur mit Lizenzen, die die Nutzung der Bilder erlauben (z. B. FLUX.1 [schnell], Apache 2.0). Jedes Modell wird in `CREDITS.md` dokumentiert.
- ℹ️ Rein KI-generierte Bilder sind in der EU oft **nicht urheberrechtlich geschützt**. Andere könnten sie also kopieren. Das ist kein Hindernis, aber gut zu wissen. Nachbearbeitung von Hand stärkt die eigenen Rechte.
- 🔧 DSGVO und COPPA: Es werden **keine** Daten erhoben. Das ist die einfachste und sicherste Lösung.

### 2.9 🧑‍💻 Agenten-Workflow – „Kann ein KI-Agent im Terminal das sauber bauen?“
- 🔧 **Eine Phase = eine abgeschlossene, testbare Einheit** mit Akzeptanzkriterien.
- 🔧 Der Agent **kann keine Bilder generieren**. Kunst ist eine 👤 **Mensch-Aufgabe** (ComfyUI lokal). Der Agent baut die Werkzeuge dafür (Freistellen, Maßstab, Atlas).
- 🔧 Automatische Tests (GUT für Godot, Python für Tools) plus Maßstab-Prüfer **nach jeder Aufgabe**.
- 🔧 `docs/PROGRESS.md` ist das Gedächtnis des Agenten zwischen den Sitzungen.

---

## 3. Entscheidungs-Übersicht (alt → neu)

| Thema | v1.x | **v2.0 (verbindlich)** |
|---|---|---|
| Item-Größen | +80 % für kleine Items | **Echte Größen** aus `scale_table.json` |
| Tiefe im Raum | bis +54 % | **max. +12 %** |
| Weltmaßstab | 4 px/cm | **1 Einheit = 1 cm**, Kamera 300 cm Raumhöhe |
| Grafik | Code-Formen / Stil offen | **Stil C** + KI-Pipeline + Platzhalter zuerst |
| Engine-Renderer | offen | **Godot 4.x Compatibility** |
| NPC-KI | Behavior Trees | **Zustandsmaschinen + Rollen-Vorlagen** |
| Story-Rekorder | geplant | **gestrichen** (Datenschutz) |
| Tag/Nacht, Wetter, Foto | 1.0 | **nach 1.0** |
| Namenseingabe | frei | **Auswahl + Würfel**, frei nur für Eltern |
| Körperformen | 8 | **3 Schablonen** (sauber kombinierbar) |
| Zielgruppe | 4–12 | **Kern 5–9** |
| Item-Zahl | 1.000 „Stück“ | **~350 Vorlagen → 1.000 inkl. Varianten** |
| Qualitätssicherung | manuell | **Automatische Tests + Maßstab-Prüfer** |
