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
| `assets/audio/sfx/*.wav` (29 Effekte: Material-Sounds, 10 Tierstimmen, UI-Töne, Würfel, Auslöser) | selbst synthetisiert mit `tools/make_sfx.py` (NumPy, fester Seed) | CC0 / eigenes Werk |

## Schriften & Symbole (Phase 04)
| Name | Zweck | Lizenz |
|---|---|---|
| Baloo 2 (`assets/fonts/Baloo2.ttf`) | Anzeige-Schrift der UI (rund, freundlich) | SIL Open Font License 1.1 (Google Fonts) |
| Nunito (`assets/fonts/Nunito.ttf`) | Fließtext | SIL Open Font License 1.1 (Google Fonts) |
| `assets/ui/icons/*.png` (63 Symbole) | UI-Symbole – selbst gezeichnet mit `tools/make_ui_icons.py` (Pillow, keine Emoji-Fonts nötig) | CC0 / eigenes Werk |
| `assets/sprites/pets/*.png` (13 Tiere) + `assets/shaders/patterns/*.png` (4 Fellmuster) | Haustiere im Stil C, selbst gezeichnet (`tools/make_pet_sprites.py`, `tools/pets/`, `tools/make_pet_patterns.py`) | CC0 / eigenes Werk |

## Figuren-Teile (Phase 03, Platzhalter)
| Datei | Quelle | Lizenz |
|---|---|---|
| `assets/characters/parts/*/*.png` (139 Teile je Schablone, 4 Schablonen) | selbst erzeugt mit `tools/make_chibi_parts.py` + `tools/chibi/` (Pillow/NumPy/SciPy, Vektor-Zeichnung, Maße aus `data/characters/templates.json`) | CC0 / eigenes Werk |
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
