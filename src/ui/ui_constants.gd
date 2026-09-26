class_name UiConstants
extends RefCounted
## Zentrale UI-Werte (keine Magic Numbers im UI-Code, MASTERPROMPT §7).

const MIN_TOUCH_DP: float = 48.0          # kleinste Tippfläche
const FONT_DEBUG: int = 22
const FONT_HUD: int = 26
const FONT_LABEL_WORLD: int = 9           # Beschriftung in Welt-cm (Zielgröße)
const WORLD_TEXT_OVERSAMPLE: float = 6.0  # Welt-Text wird n-fach gerendert und verkleinert → scharf beim Zoom
const COLOR_HUD_BG: Color = Color(1, 1, 1, 0.82)
const COLOR_HUD_TEXT: Color = Color(0.24, 0.18, 0.36)
const THREE_FINGER_TAP_S: float = 0.35    # alle drei Finger innerhalb dieser Zeit = Debug-Geste
