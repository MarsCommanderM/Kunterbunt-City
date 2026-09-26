# PHASE 08 · NPC- & Tier-KI
**Ziel:** Feste Figuren **arbeiten** (kassieren, patrouillieren, behandeln, trainieren), Tiere haben ein Eigenleben, und nichts davon stört das Spielen.
**Voraussetzung:** Phase 07.

## Aufgaben
| ID | Aufgabe |
|---|---|
| P08-T01 | `NpcStateMachine` (Tech-Spec §4.5): Basis-Zustände `idle/work/react/carried/return_to_post`, Übergänge per Timer, Ereignis, Spieler |
| P08-T02 | Rollen-Loader `data/npc_roles/*.json` + NPC-Loader `data/npcs/*.json` |
| P08-T03 | Wegfindung im Raum: Bodenband als einfache Laufbahn (x/y innerhalb des Bands), Hindernisse = große Möbel; kein NavMesh-Overkill |
| P08-T04 | Rollen implementieren: `cashier`, `shelf_stocker`, `lifeguard`, `teacher`, `janitor`, `doctor`, `nurse`, `coach`, `supervisor`, `mechanic`, `florist`, `zookeeper`, `ride_operator`, `vendor`, `receptionist` (je mit 2–4 Arbeits-Animationen, erst Platzhalter) |
| P08-T05 | Tagesplan light: Laden öffnet (NPC schließt auf) – **Standard „immer offen“** (Einstellung) |
| P08-T06 | Garantien als Tests: NPC blockiert keinen Drop, verlässt nie den Raum, kehrt nach `return_after_s` zurück, reagiert beim Tragen |
| P08-T07 | `PetBrain` (Tech-Spec §4.6): Bedürfnisse, Aktionen (Napf, Ball, Körbchen, folgen), Charakterzug beeinflusst die Gewichte |
| P08-T08 | Tierlaute: Hund bellt (3 Varianten), Katze miaut/schnurrt beim Streicheln, Vogel zwitschert. Intervall 15–60 s + **globaler Limiter** 1 / 8 s |
| P08-T09 | Hintergrund-Figuren (Badegäste, Passanten) als „leichte“ NPCs ohne Interaktion, max. 6 pro Szene |
| P08-T10 | Performance: 15 aktive NPCs/Tiere + 250 Items → 60 FPS (Desktop) |

## Akzeptanzkriterien
- [ ] Beispiel-Szene: Kassiererin scannt ein Item an der Kasse (Piep, Tüte erscheint)
- [ ] Bademeister-Test: läuft den Rand ab, pfeift bei rennender Figur, rettet nach 10 s unter Wasser (Platzhalter-Becken)
- [ ] Alle Garantie-Tests grün
- [ ] Nie mehr als 1 Tierlaut pro 8 s (Test)
- [ ] `check.sh` grün

## Startprompt
> Lies MASTERPROMPT.md, docs/06_TECH_SPEC.md §4.5–4.6 und docs/phasen/PHASE_08_NPC_TIER_KI.md. Baue die NPC- und Tier-KI mit einfachen, testbaren Zustandsmaschinen und Rollen-Vorlagen. Phasenbericht und stoppen.
