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
| `assets/audio/sfx/*.wav` (11 Platzhalter-Effekte) | selbst synthetisiert mit `tools/make_sfx.py` (NumPy, fester Seed) | CC0 / eigenes Werk |

## Schriften
| Font | Quelle | Lizenz |
|---|---|---|
| (noch leer, z. B. eine OFL-Schrift) | | SIL OFL 1.1 |
