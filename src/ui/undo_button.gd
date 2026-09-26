class_name UndoButton
extends Button
## Runder Rückgängig-Knopf (P02-T08). Gezeichnetes Symbol – keine Schrift nötig, kein Lesen nötig.

var undo: UndoStack:
	set(v):
		undo = v
		if undo:
			undo.changed.connect(func(_n: int) -> void: _refresh())
		_refresh()


func _ready() -> void:
	custom_minimum_size = Vector2(120, 120)
	focus_mode = Control.FOCUS_NONE
	for st: String in ["normal", "hover", "pressed", "disabled"]:
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(1, 1, 1, 0.92) if st != "pressed" else Color(0.93, 0.9, 1.0)
		sb.set_corner_radius_all(60)
		sb.shadow_color = Color(0.2, 0.1, 0.3, 0.18)
		sb.shadow_size = 8
		sb.shadow_offset = Vector2(0, 4)
		add_theme_stylebox_override(st, sb)
	pressed.connect(func() -> void:
		if undo:
			undo.undo()
			AudioBus.play_sfx("tap"))
	_refresh()


func _refresh() -> void:
	disabled = undo == null or not undo.can_undo()
	modulate.a = 0.45 if disabled else 1.0
	queue_redraw()


func _draw() -> void:
	var c: Vector2 = size * 0.5
	var r: float = size.x * 0.24
	var col := UiConstants.COLOR_HUD_TEXT
	draw_arc(c, r, deg_to_rad(200), deg_to_rad(470), 32, col, size.x * 0.07, true)
	var tip: Vector2 = c + Vector2(cos(deg_to_rad(200)), sin(deg_to_rad(200))) * r
	var pts := PackedVector2Array([tip + Vector2(-size.x * 0.1, -size.x * 0.02), tip + Vector2(size.x * 0.08, -size.x * 0.1), tip + Vector2(size.x * 0.04, size.x * 0.1)])
	draw_colored_polygon(pts, col)
