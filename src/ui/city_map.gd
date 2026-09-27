class_name CityMap
extends Control
## Stadtkarte / Startmenü (P05-T02…T04): ein Knopf pro Bereich (Bild + Symbol + eigener Sound).
## Oben: Figur, Rucksack, Album, Eltern. Umschaltbar zwischen **Karte** (illustriert) und
## **Raster** (übersichtlich für kleine Kinder). Nicht fertige Bereiche zeigen eine Baustelle.

signal entered(area_id: StringName)
signal open_characters
signal open_backpack
signal open_album
signal open_parents

const TOP_H: float = 132.0
const BTN: Vector2 = Vector2(260, 210)

var mode: String = "map"          ## "map" | "grid"
var _body: Control
var _top: HBoxContainer
var _fig_btn: Button
var _area_buttons: Dictionary = {}
var _busy: Control
var _wobble_t: float = 0.0


func _ready() -> void:
	Ui.background(self)
	_build()
	_refresh()


# ------------------------------------------------------------------ Aufbau
func _process(delta: float) -> void:
	if Settings.reduced_motion:
		return
	_wobble_t += delta
	for a: Variant in Areas.list():
		var id: String = String((a as Dictionary)["id"])
		if Areas.is_ready(StringName(id)):
			continue
		var b: Button = _area_buttons.get(id)
		if b == null:
			continue
		var badge: Node = b.get_node_or_null("Baustelle")
		if badge != null and bool(badge.get_meta("wobble", false)):
			badge.rotation = sin(_wobble_t * 3.0 + float(hash(id)) * 0.01) * 0.35


func _build() -> void:
	var v := Ui.vbox(14)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 22)
	add_child(v)
	v.add_child(_top_bar())
	_body = Control.new()
	_body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(_body)
	_build_map()


func _top_bar() -> Control:
	_top = Ui.hbox(14)
	_top.custom_minimum_size = Vector2(0, TOP_H)
	_fig_btn = Ui.button("Figur", "person", "", Vector2(330, 112))
	Ui.wire(_fig_btn, func() -> void: open_characters.emit())
	_top.add_child(_fig_btn)
	var pack := Ui.button("Rucksack", "backpack", "", Vector2(300, 112))
	Ui.wire(pack, func() -> void: open_backpack.emit())
	_top.add_child(pack)
	var album := Ui.button("Album", "album", "", Vector2(270, 112))
	Ui.wire(album, func() -> void: open_album.emit())
	_top.add_child(album)
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_top.add_child(sp)
	var view := Ui.button("Raster", "map", "ghost", Vector2(280, 112))
	view.name = "ViewToggle"
	Ui.wire(view, func() -> void:
		mode = "grid" if mode == "map" else "map"
		_refresh())
	_top.add_child(view)
	var parents := Ui.button("Eltern", "gear", "lilac", Vector2(280, 112))
	Ui.wire(parents, func() -> void: open_parents.emit())
	_top.add_child(parents)
	return _top


func _clear_body() -> void:
	for c: Node in _body.get_children():
		c.queue_free()


func _refresh() -> void:
	_clear_body()
	if mode == "map":
		_build_map()
	else:
		_build_grid()
	var view: Button = _top.get_node_or_null("ViewToggle") as Button
	if view != null:
		view.text = " Raster" if mode == "map" else " Karte"
	_refresh_figure()


## Oben links: die aktive Figur (Bild aus der Galerie-Kamera, Name).
func _refresh_figure() -> void:
	var c: CharacterData = Game.active_character()
	if c == null:
		_fig_btn.text = " Figur"
		_fig_btn.icon = Ui.tex("person")
		return
	_fig_btn.text = " " + c.display_name()
	if Portrait.can_render():
		var tex: Texture2D = await Portrait.capture(c.template_id, c.look(), 96, 112)
		if tex != null and is_instance_valid(_fig_btn):
			_fig_btn.icon = tex
			_fig_btn.add_theme_constant_override("icon_max_width", 96)


func _build_map() -> void:
	var bg := TextureRect.new()
	bg.texture = load("res://assets/ui/city_map.png")
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_body.add_child(bg)
	var scale_y: float = _body.size.y / 1080.0 if _body.size.y > 1.0 else 1.0
	for a: Variant in Areas.list():
		var area: Dictionary = a
		var id := StringName(String(area["id"]))
		var b := _area_button(id, true)
		b.custom_minimum_size = BTN
		b.size = BTN
		b.position = Vector2(float(area["map_x"]), float(area["map_y"])) * scale_y - BTN * 0.5
		_body.add_child(b)
		_area_buttons[String(id)] = b


func _build_grid() -> void:
	var s := ScrollContainer.new()
	s.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_body.add_child(s)
	var g := Ui.grid(4, 22)
	g.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 20)
	s.add_child(g)
	for a: Variant in Areas.list():
		var id := StringName(String((a as Dictionary)["id"]))
		var b := _area_button(id, false)
		b.custom_minimum_size = Vector2(420, 232)
		g.add_child(b)
		_area_buttons[String(id)] = b
	# letzte Reihe auffüllen, damit das Raster ruhig aussieht
	while g.get_child_count() % 4 != 0:
		var filler := Control.new()
		filler.custom_minimum_size = Vector2(420, 232)
		g.add_child(filler)


func _area_button(id: StringName, on_map: bool = true) -> Button:
	var ready: bool = Areas.is_ready(id)
	# Auf der Karte: spielbare Bereiche farbig, Baustellen durchsichtig (die Karte bleibt sichtbar).
	# Im Raster: weiße Karten (ruhig und übersichtlich) – spielbare bleiben farbig.
	var kind: String = "accent" if ready else ("ghost" if on_map else "")
	var b := Ui.button(Areas.label(id), Areas.icon(id), kind, BTN)
	b.add_theme_font_size_override("font_size", Ui.FONT_LABEL)
	b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
	b.vertical_icon_alignment = VERTICAL_ALIGNMENT_TOP
	b.add_theme_constant_override("icon_max_width", 120)
	var col: Color = Areas.color(id)
	b.add_theme_color_override("font_color", Ui.INK)
	if ready:
		Ui.style_button(b, col.lightened(0.35))
	Ui.wire(b, func() -> void: _tap_area(id), Areas.sound(id) if ready else "deny")
	if not ready:
		var badge := Ui.icon("wrench", 64.0)
		badge.name = "Baustelle"
		badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
		badge.set_anchors_and_offsets_preset(Control.PRESET_TOP_RIGHT)
		badge.position = Vector2(-56, 18)
		b.add_child(badge)
		# Baustelle „arbeitet": kleines Wippen (respektiert „Animationen reduzieren").
		if not Settings.reduced_motion:
			badge.set_meta("wobble", true)
	return b


func _tap_area(id: StringName) -> void:
	if not Areas.is_ready(id):
		AudioBus.play_sfx("deny")
		_bubble(id)
		return
	entered.emit(id)


## Kurzes Sprechblasen-Hinweis „kommt bald" – ohne Text-Zwang (nur Symbol + Farbe).
func _bubble(id: StringName) -> void:
	var b: Button = _area_buttons.get(String(id))
	if b == null:
		return
	var old: Node = b.get_node_or_null("Bubble")
	if old != null:
		old.queue_free()
	var bub := Panel.new()
	bub.name = "Bubble"
	bub.mouse_filter = Control.MOUSE_FILTER_IGNORE
	bub.add_theme_stylebox_override("panel", Ui.box(Ui.ACCENT, 22))
	bub.size = Vector2(220, 96)
	bub.position = Vector2(b.size.x * 0.5 - 110, -84)
	b.add_child(bub)
	var l := Ui.label("kommt bald", Ui.FONT_SMALL, Color.WHITE)
	l.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bub.add_child(l)
	var tw: Tween = create_tween()
	tw.tween_interval(1.6)
	tw.tween_callback(func() -> void:
		if is_instance_valid(bub):
			bub.queue_free())


# ------------------------------------------------------------------ Ladebildschirm
## Zeigt ein Ladebild (P05-T05, Ziel < 2 s) und ruft `work` danach auf.
func with_loading(work: Callable) -> void:
	_busy = Control.new()
	_busy.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_busy.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_busy)
	var dim := ColorRect.new()
	dim.color = Color(0.98, 0.95, 0.9, 0.92)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_busy.add_child(dim)
	var v := Ui.vbox(20)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	_busy.add_child(v)
	var sun := Ui.icon("sun", 180.0)
	v.add_child(sun)
	v.add_child(Ui.label("Laden …", Ui.FONT_TITLE, Ui.INK_SOFT))
	if not Settings.reduced_motion:
		var tw: Tween = create_tween().set_loops()
		tw.tween_property(sun, "rotation", TAU, 0.9)
	await get_tree().process_frame
	await work.call()
	if is_instance_valid(_busy):
		_busy.queue_free()
