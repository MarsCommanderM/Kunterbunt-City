class_name Units
extends RefCounted
## Einheiten & Maßstab-Formeln (docs/02_MASSSTAB_BIBEL.md §1).
## 1 Godot-Einheit = 1 cm. y = 0 ist die hintere Bodenlinie, negatives y = nach oben.

## Absolute Obergrenze des Tiefen-Faktors (Regel S-07). Wird NIE überschritten, egal was in den Daten steht.
const DEPTH_SCALE_LIMIT: float = 1.12
## Standard-Kamerahöhe in Innenräumen (Regel S-08).
const DEFAULT_VIEW_HEIGHT_CM: float = 300.0
## Referenz-Auflösung der Sprites/Hintergründe.
const SPRITE_PX_PER_CM: float = 8.0


## Position im Bodenband: 0 = hinten, 1 = vorne (geklemmt).
static func depth_t(y_cm: float, back_y_cm: float, front_y_cm: float) -> float:
	if is_equal_approx(front_y_cm, back_y_cm):
		return 0.0
	return clampf((y_cm - back_y_cm) / (front_y_cm - back_y_cm), 0.0, 1.0)


## Tiefen-Faktor 1,00 (hinten) … max. 1,12 (vorne).
static func depth_factor(y_cm: float, back_y_cm: float, front_y_cm: float,
		scale_max: float = DEPTH_SCALE_LIMIT) -> float:
	var s_max: float = clampf(scale_max, 1.0, DEPTH_SCALE_LIMIT)
	return 1.0 + (s_max - 1.0) * depth_t(y_cm, back_y_cm, front_y_cm)


## Bildschirm-y eines Punkts, der h_cm über dem Boden an Tiefe depth_y_cm steht.
static func screen_y(depth_y_cm: float, height_cm: float, back_y_cm: float, front_y_cm: float,
		scale_max: float = DEPTH_SCALE_LIMIT) -> float:
	return depth_y_cm - height_cm * depth_factor(depth_y_cm, back_y_cm, front_y_cm, scale_max)


## Kamera-Zoom, damit visible_h_cm genau die Viewport-Höhe füllt.
static func zoom_for_visible_height(viewport_h_px: float, visible_h_cm: float) -> float:
	assert(visible_h_cm > 0.0)
	return viewport_h_px / visible_h_cm


static func visible_height_for_zoom(viewport_h_px: float, zoom: float) -> float:
	assert(zoom > 0.0)
	return viewport_h_px / zoom


## Skalierung eines Sprites, damit es world_h_cm hoch ist.
static func sprite_scale(texture_h_px: float, world_h_cm: float) -> float:
	assert(texture_h_px > 0.0)
	return world_h_cm / texture_h_px
