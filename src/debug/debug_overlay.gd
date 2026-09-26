class_name DebugOverlay
extends CanvasLayer
## Debug-Anzeige (nur Debug-Builds): F3 oder Drei-Finger-Tipp.
## Zeigt 10-cm-Raster, Oberflächen, Bodenband, FPS, Kamerahöhe und Zeiger-Position in cm.

@export var room: Room
@export var camera: WorldCamera

var _label: Label
var _touch_times: Dictionary = {}
var enabled: bool = false


func _ready() -> void:
	layer = 50
	_label = Label.new()
	_label.position = Vector2(24, 96)
	_label.add_theme_font_size_override("font_size", UiConstants.FONT_DEBUG)
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0, 0, 0, 0.6)
	sb.set_content_margin_all(10)
	sb.set_corner_radius_all(8)
	_label.add_theme_stylebox_override("normal", sb)
	_label.add_theme_color_override("font_color", Color.WHITE)
	add_child(_label)
	set_enabled(false)


func set_enabled(on: bool) -> void:
	enabled = on and OS.is_debug_build()
	_label.visible = enabled
	if room:
		room.debug_visible = enabled
	set_process(enabled)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and (event as InputEventKey).keycode == KEY_F3:
		set_enabled(not enabled)
		get_viewport().set_input_as_handled()
	elif event is InputEventScreenTouch:
		var t := event as InputEventScreenTouch
		var now: float = Time.get_ticks_msec() / 1000.0
		if t.pressed:
			_touch_times[t.index] = now
			var recent: int = _touch_times.values().filter(
				func(v: float) -> bool: return now - v < UiConstants.THREE_FINGER_TAP_S).size()
			if recent >= 3:
				_touch_times.clear()
				set_enabled(not enabled)
		else:
			_touch_times.erase(t.index)


func _process(_delta: float) -> void:
	var lines: PackedStringArray = ["FPS %d" % Engine.get_frames_per_second()]
	if camera:
		lines.append("Kamera: %.0f cm hoch (%.0f–%.0f)" % [camera.visible_h_cm, camera.min_h_cm, camera.max_h_cm])
		var w: Vector2 = camera.get_global_mouse_position()
		lines.append("Zeiger: x %.0f cm · y %.0f cm" % [w.x, w.y])
		if room:
			lines.append("Tiefen-Faktor hier: %.3f" % room.floor_band.depth_factor(w.y))
	_label.text = "\n".join(lines)
