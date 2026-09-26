# PHASE 09 · MVP: Einkaufsstraße + Spielplatz → Release v0.1
**Ziel:** 3 spielbare Bereiche (Zuhause, Einkaufsstraße inkl. Blumenladen, Spielplatz & Park), kostenlos veröffentlicht.
**Voraussetzung:** Phasen 07, 08.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P09-T01 | `data/areas/shopping.json`: Straße + 9 Läden (Welt-Doku §2), Bushaltestelle = Bereichswechsel mit Bus-Animation |
| P09-T02 | 200 Items Einkaufsstraße (Supermarkt, Bäckerei, Blumenladen, Mode, Friseur, Spielzeug, Tierhandlung, Eisdiele, Musik) |
| P09-T03 | Kassen-Logik (Rolle `cashier`): Item + Figur an die Kasse → Scan, Tüte ✋ mit Inhalt, unbegrenztes Spielgeld |
| P09-T04 | Modeladen: Kleidung auf die Figur ziehen = anziehen (nutzt Editor-Teile). Friseur: Frisur ändern live |
| P09-T05 | Blumenladen: `florist` bindet 3 Blumen zu einem Strauß (Rezept), Gewächshaus mit Wachstum |
| P09-T06 | `data/areas/playground.json`: Spielplatz, Teich, Wiese. Schaukel/Rutsche/Wippe/Karussell als Fixtures mit SeatSlots und Bewegung |
| P09-T07 | Enten-KI (schwimmen, schnattern, flüchten), Sand formen (3 Förmchen), Seifenblasen |
| P09-T08 | Lineups + Test-Szenen für beide Bereiche |
| P09-T09 | Release-Build: Web (itch.io-tauglich), Android APK, Windows/Linux/macOS. Version `0.1.0`, Changelog |
| P09-T10 | itch.io-Seite vorbereiten (Texte, Screenshots aus dem Spiel, Altersangabe, Datenschutz-Hinweis „sammelt keine Daten“) – Veröffentlichen macht 👤 |

## Akzeptanzkriterien
- [ ] 3 Bereiche, ~435 Items, 0 Maßstab-Fehler
- [ ] Web-Build läuft auf itch.io (Test-Upload als Entwurf) inkl. Speichern
- [ ] APK läuft auf einem Android-Tablet (👤)
- [ ] 👤 Kindertest mit 3–5 Kindern, keine Blocker
- [ ] `check.sh` grün

## 👤 Mensch
itch.io-Account (kostenlos), Upload, APK auf dem Tablet testen, Kindertest.

## Startprompt
> Lies MASTERPROMPT.md, docs/05_WELT_UND_BEREICHE.md §2–3 und docs/phasen/PHASE_09_MVP_RELEASE.md. Baue Einkaufsstraße und Spielplatz nach demselben Qualitätsstandard wie Zuhause und bereite Release v0.1 vor. Phasenbericht und stoppen.
