class_name ColorDots
extends RefCounted
## P04b-T06: Runde Farbpunkte für Editor-Paletten (statt grauer Kästen). Die Farbe steckt in einem
## eigenen Kreis – eine Auswahl-Markierung kann sie nicht mehr überschreiben (alter Fehler: leere Felder).


## Ein runder Farbknopf. `selected` = dicker Ring in Akzentfarbe.
static func dot(hex: String, size: float, selected: bool) -> Button:
	var b := Button.new()
	b.custom_minimum_size = Vector2(size, size)
	b.set_meta("color", hex)
	var empty := StyleBoxEmpty.new()
	for st: String in ["normal", "hover", "pressed", "focus", "disabled"]:
		b.add_theme_stylebox_override(st, empty)
	var disc := Panel.new()
	disc.mouse_filter = Control.MOUSE_FILTER_IGNORE
	disc.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var s := StyleBoxFlat.new()
	s.bg_color = Color(hex)
	s.set_corner_radius_all(int(size))
	s.set_border_width_all(int(size * 0.07) + (5 if selected else 0))
	s.border_color = Ui.ACCENT if selected else Color.WHITE
	s.shadow_color = Ui.SHADOW
	s.shadow_size = 8 if selected else 5
	s.shadow_offset = Vector2(0, 4)
	s.anti_aliasing_size = 1.5
	disc.add_theme_stylebox_override("panel", s)
	b.add_child(disc)
	if selected:
		var tick := Ui.icon("check", size * 0.46)
		tick.mouse_filter = Control.MOUSE_FILTER_IGNORE
		tick.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, int(size * 0.26))
		b.add_child(tick)
	return b


## Reihe/Raster aus Farbpunkten füllen; cb(hex) beim Tippen.
static func fill(parent: Container, colors: Array, size: float, current: String, cb: Callable) -> void:
	for c: Node in parent.get_children():
		c.queue_free()
	for hex: Variant in colors:
		var h: String = String(hex)
		var b := dot(h, size, h.to_lower() == current.to_lower())
		Ui.wire(b, func() -> void: cb.call(h))
		parent.add_child(b)
