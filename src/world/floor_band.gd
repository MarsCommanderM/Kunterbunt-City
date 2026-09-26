class_name FloorBand
extends Node2D
## Bodenband: Streifen zwischen hinterer (y = back_y_cm) und vorderer Bodenlinie (y = front_y_cm).
## Liefert den Tiefen-Faktor (max. 1,12, Regel S-07) und hält Dinge im Band.

@export var back_y_cm: float = 0.0
@export var front_y_cm: float = 80.0
@export var width_cm: float = 600.0
@export var depth_scale_max: float = Units.DEPTH_SCALE_LIMIT:
	set(v):
		depth_scale_max = clampf(v, 1.0, Units.DEPTH_SCALE_LIMIT)

var debug_visible: bool = false:
	set(v):
		debug_visible = v
		queue_redraw()


func setup(data: Dictionary, room_width_cm: float) -> void:
	back_y_cm = float(data.get("back_y_cm", 0.0))
	front_y_cm = float(data.get("front_y_cm", 80.0))
	depth_scale_max = float(data.get("depth_scale_max", Units.DEPTH_SCALE_LIMIT))
	width_cm = room_width_cm
	queue_redraw()


func depth_t(y_cm: float) -> float:
	return Units.depth_t(y_cm, back_y_cm, front_y_cm)


func depth_factor(y_cm: float) -> float:
	return Units.depth_factor(y_cm, back_y_cm, front_y_cm, depth_scale_max)


## Bildschirm-y eines Punkts h_cm über dem Boden bei Tiefe y_cm.
func screen_y(y_cm: float, height_cm: float) -> float:
	return Units.screen_y(y_cm, height_cm, back_y_cm, front_y_cm, depth_scale_max)


func contains(p: Vector2) -> bool:
	return p.x >= 0.0 and p.x <= width_cm and p.y >= back_y_cm and p.y <= front_y_cm


func clamp_point(p: Vector2) -> Vector2:
	return Vector2(clampf(p.x, 0.0, width_cm), clampf(p.y, back_y_cm, front_y_cm))


func _draw() -> void:
	if not debug_visible:
		return
	var band := Rect2(0.0, back_y_cm, width_cm, front_y_cm - back_y_cm)
	draw_rect(band, Color(0.2, 0.6, 1.0, 0.12))
	draw_line(Vector2(0, back_y_cm), Vector2(width_cm, back_y_cm), Color(0.1, 0.4, 1.0), 1.5)
	draw_line(Vector2(0, front_y_cm), Vector2(width_cm, front_y_cm), Color(0.1, 0.4, 1.0), 1.5)
