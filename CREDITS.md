# Credits & Lizenzen

Kunterbunt City kostet nichts und nutzt ausschließlich frei lizenzierte Werkzeuge und Inhalte.
**Regel:** Jede neue externe Quelle (Addon, Sound, Font, Modell) wird hier mit Lizenz eingetragen, **bevor** sie ins Repo kommt.

## Engine & Werkzeuge
| Name | Zweck | Lizenz |
|---|---|---|
| Godot Engine 4.7.2 | Spiel-Engine | MIT |
| GUT (Godot Unit Test) 9.6.1 | Tests, liegt in `addons/gut/` | MIT (© Butch Wesley) |
| Python, Pillow, NumPy, SciPy, PyYAML, pytest | Asset-Pipeline & Tests | PSF / HPND / BSD / MIT |

## Grafik-Erzeugung
| Name | Zweck | Lizenz / Hinweis |
|---|---|---|
| ComfyUI | lokale Bild-Erzeugung | GPL-3.0 (nur Werkzeug, wird nicht mit dem Spiel ausgeliefert) |
| FLUX.1 [schnell] | Bildmodell | Apache 2.0 |
| LoRA `kbcstyle` | eigener Stil-C-Feinschliff | selbst trainiert |

> Hinweis: Rein KI-generierte Bilder sind nach aktueller Rechtslage in vielen Ländern nur eingeschränkt urheberrechtlich geschützt. Die Pipeline (Freistellen, Zuschneiden, Nachbearbeitung) und die Zusammenstellung sind eigene Arbeit.

## Platzhalter-Grafik
| Datei | Quelle | Lizenz |
|---|---|---|
| `assets/placeholders/*.png` | selbst erzeugt mit `tools/make_placeholders.py` (Pillow, aus `data/scale_table.json`) | CC0 / eigenes Werk |

## Audio
| Datei/Paket | Quelle | Lizenz |
|---|---|---|
| `assets/audio/sfx/*.wav` (14 Effekte, inkl. `pet_dog_bark`, `pet_cat_meow`, `eat_chomp`) | selbst synthetisiert mit `tools/make_sfx.py` (NumPy, fester Seed) | CC0 / eigenes Werk |

## Figuren-Teile (Phase 03, Platzhalter)
| Datei | Quelle | Lizenz |
|---|---|---|
| `assets/characters/parts/*/*.png` (63 Teile, 3 Schablonen) | selbst erzeugt mit `tools/make_rig_parts.py` (Pillow, Maße aus `data/characters/templates.json`) | CC0 / eigenes Werk |
| `assets/characters/sprite/char_girl_01*.png`, `char_girl_01.json` | Referenz-Sprite aus `reference/sprites/` (Stil-C-Pipeline), Faust-Position gemessen mit `tools/dev/make_girl_hand.py` | CC0 / eigenes Werk |

> Die Figuren-Teile sind bewusst **Platzhalter** (vektorige Grundformen in Stil C). Die echten,
> mehrschichtigen Assets entstehen in Phase 06 mit derselben Pipeline – die Ebenen-Struktur
> (`CharacterRig`, `parts.json`) bleibt dabei unverändert.

## Haustiere (Phase 03)
| Datei | Quelle | Lizenz |
|---|---|---|
| `assets/sprites/home/pet_dog_brown.png`, `pet_cat` (Platzhalter) | Stil-C-Referenz-Sprites bzw. `tools/make_placeholders.py` | CC0 / eigenes Werk |

## Schriften
| Font | Quelle | Lizenz |
|---|---|---|
| (noch leer, z. B. eine OFL-Schrift) | | SIL OFL 1.1 |
