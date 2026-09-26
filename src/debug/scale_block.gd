class_name ScaleBlock
extends Node2D
## Platzhalter-Klotz in echter Größe aus data/scale_table.json (Phase 01).
## Ursprung = Pivot unten Mitte. Größe kommt NUR aus ItemDB – nie hart codiert.

@export var scale_ref: String = ""
@export var label: String = ""
@export var color: Color = Color(0.6, 0.7, 0.9)

var size_cm: Vector2 = Vector2.ZERO


func setup(ref: String, text: String, col: Color) -> ScaleBlock:
	scale_ref = ref
	label = text
	color = col
	name = ref
	size_cm = Vector2(ItemDB.width_cm(ref), ItemDB.height_cm(ref))
	queue_redraw()
	return self


## Stellt den Klotz auf den Boden an (x, Tiefe) – mit Tiefen-Faktor.
func place_on_floor(x_cm: float, depth_y_cm: float, band: FloorBand) -> void:
	position = Vector2(x_cm, depth_y_cm)
	scale = Vector2.ONE * band.depth_factor(depth_y_cm)


## Stellt den Klotz auf eine Oberfläche (Pivot exakt auf der Oberkante).
func place_on_surface(x_cm: float, surface: Surface) -> void:
	position = Vector2(x_cm, surface.top_y())
	scale = Vector2.ONE * surface.depth_factor()


## Oberkante in Welt-cm (für Tests).
func top_y() -> float:
	return position.y - size_cm.y * scale.y


func _draw() -> void:
	var r := Rect2(-size_cm.x * 0.5, -size_cm.y, size_cm.x, size_cm.y)
	var sb := StyleBoxFlat.new()
	sb.bg_color = color
	sb.border_color = color.darkened(0.45)
	sb.set_border_width_all(1)
	sb.set_corner_radius_all(int(clampf(minf(size_cm.x, size_cm.y) * 0.18, 1.0, 8.0)))
	sb.anti_aliasing = true
	draw_style_box(sb, r)
	WorldText.draw(self, Vector2(0.0, -size_cm.y - 2.5), "%s %d cm" % [label, roundi(size_cm.y)],
		UiConstants.FONT_LABEL_WORLD, color.darkened(0.65), true)
