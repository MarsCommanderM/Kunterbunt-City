class_name Surface
extends Node2D
## Abstellfläche (Tischplatte, Regal, Fensterbank …) in cm.
## Die Oberkante liegt h_cm über dem Boden an der Tiefe depth_y_cm.

enum Type { FLOOR, TABLE, SHELF, WALL, SEAT }

const TYPE_NAMES: Dictionary = {
	"floor": Type.FLOOR, "table": Type.TABLE, "shelf": Type.SHELF, "wall": Type.WALL, "seat": Type.SEAT,
}

@export var surface_id: StringName = &""
@export var type: Type = Type.TABLE
@export var x_from_cm: float = 0.0
@export var x_to_cm: float = 100.0
@export var h_cm: float = 75.0
@export var depth_y_cm: float = 0.0

## Wird von Room gesetzt, damit die Höhe den Tiefen-Faktor bekommt.
var floor_band: FloorBand

var debug_visible: bool = false:
	set(v):
		debug_visible = v
		queue_redraw()


static func from_dict(d: Dictionary, band: FloorBand) -> Surface:
	var s := Surface.new()
	s.surface_id = StringName(d["id"])
	s.name = String(d["id"])
	s.type = TYPE_NAMES.get(String(d.get("type", "table")), Type.TABLE)
	s.x_from_cm = float(d["x_cm"][0])
	s.x_to_cm = float(d["x_cm"][1])
	s.h_cm = float(d["h_cm"])
	s.depth_y_cm = float(d.get("depth_y_cm", 0.0))
	s.floor_band = band
	return s


## Bildschirm-y der Oberkante (hier stehen Dinge mit ihrem Pivot).
func top_y() -> float:
	if floor_band:
		return floor_band.screen_y(depth_y_cm, h_cm)
	return depth_y_cm - h_cm


func depth_factor() -> float:
	return floor_band.depth_factor(depth_y_cm) if floor_band else 1.0


func contains_x(x_cm: float) -> bool:
	return x_cm >= x_from_cm and x_cm <= x_to_cm


func width_cm() -> float:
	return x_to_cm - x_from_cm


func _draw() -> void:
	if not debug_visible:
		return
	var y: float = top_y()
	var col := Color(0.1, 0.8, 0.3) if type == Type.TABLE else Color(0.9, 0.6, 0.1)
	draw_line(Vector2(x_from_cm, y), Vector2(x_to_cm, y), col, 2.0)
	WorldText.draw(self, Vector2(x_from_cm + 2.0, y - 3.0), "%s · %d cm" % [surface_id, roundi(h_cm)], 7.0, col.darkened(0.3))
