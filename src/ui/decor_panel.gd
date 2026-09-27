class_name DecorPanel
extends Control
## P07-T04: Tapete und Boden des aktuellen Raums wählen. Leiste rechts (der Raum bleibt links sichtbar und
## ändert sich sofort mit). Vier Reihen, jede mit Symbol statt Text (R-07):
##   🖌 Wandfarbe · ⭐ Muster (+ Musterfarbe) · Paneel-Farbe · Boden-Art (+ Farbsatz).

const WIDTH_FRAC: float = 0.36
const DOT: float = 78.0
const TILE: float = 118.0

var _scene: AreaScene
var _box: VBoxContainer


static func open(host: Node, scene: AreaScene) -> DecorPanel:
	var p := DecorPanel.new()
	p._scene = scene
	p.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	host.add_child(p)
	return p


func _ready() -> void:
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.name = "Panel"
	panel.mouse_filter = Control.MOUSE_FILTER_STOP
	panel.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
	panel.anchor_left = 1.0 - WIDTH_FRAC
	panel.offset_left = 0
	panel.offset_top = 20
	panel.offset_bottom = -20
	panel.offset_right = -20
	add_child(panel)
	var outer := Ui.vbox(10)
	outer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 20)
	panel.add_child(outer)
	var head := Ui.hbox(10)
	head.add_child(Ui.icon("brush", 72))
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(sp)
	var x := Ui.button("", "close", "ghost", Vector2(88, 88))
	x.name = "Close"
	Ui.wire(x, func() -> void: queue_free(), "ui_back")
	head.add_child(x)
	outer.add_child(head)
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	outer.add_child(scroll)
	_box = Ui.vbox(16)
	_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(_box)
	_fill()


func _cur() -> Dictionary:
	return _scene.room.decor if _scene.room != null else {}


func _choose(d: Dictionary) -> void:
	_scene.set_decor(d)
	AudioBus.play_sfx("ui_tap")
	_fill.call_deferred()


func _fill() -> void:
	for c: Node in _box.get_children():
		_box.remove_child(c)
		c.queue_free()
	var cur: Dictionary = _cur()
	if cur.is_empty():
		return
	var cols: int = maxi(3, int((get_viewport_rect().size.x * WIDTH_FRAC - 60.0) / (DOT + 14.0)))
	var meta: Dictionary = _scene.room.bg_meta
	if Array(meta.get("layers", [])).size() > 0:
		# Wandfarbe (Zone 1)
		_section("palette")
		var g1 := _grid(cols, "WallColors")
		ColorDots.fill(g1, RoomDecor.WALL_COLORS, DOT, String(Array(cur["wall"])[0]),
			func(hex: String) -> void: _choose({"wall": [hex, Array(cur["wall"])[1], Array(cur["wall"])[2]]}))
		# Muster
		_section("star")
		var g2 := _grid(maxi(2, int(cols * DOT / TILE)), "Patterns")
		for pat: Variant in RoomDecor.PATTERNS:
			g2.add_child(_pattern_tile(String(pat), cur))
		if not String(cur.get("pattern", "")).is_empty():
			var g3 := _grid(cols, "PatternColors")
			ColorDots.fill(g3, RoomDecor.PATTERN_COLORS, DOT * 0.8, String(cur.get("pattern_col", "#ffffff")),
				func(hex: String) -> void: _choose({"pattern_col": hex}))
		# Paneel/Sockel (Zone 3)
		_section("home")
		var g4 := _grid(cols, "PanelColors")
		ColorDots.fill(g4, RoomDecor.PANEL_COLORS, DOT * 0.8, String(Array(cur["wall"])[2]),
			func(hex: String) -> void: _choose({"wall": [Array(cur["wall"])[0], Array(cur["wall"])[1], hex]}))
	# Boden: Art + Farbsatz
	_section("shoe")
	var kinds: Array = RoomDecor.floor_kinds(meta)
	var g5 := _grid(maxi(2, int(cols * DOT / TILE)), "FloorKinds")
	for k: Variant in kinds:
		g5.add_child(_floor_tile(String(k), cur))
	var presets: Array = RoomDecor.FLOOR_PRESETS.get(String(cur.get("floor", "")), [])
	var firsts: Array = []
	for p: Variant in presets:
		firsts.append(String(Array(p)[0]))
	var g6 := _grid(cols, "FloorColors")
	ColorDots.fill(g6, firsts, DOT * 0.8, String(Array(cur["floor_cols"])[0]),
		func(hex: String) -> void:
			for p: Variant in presets:
				if String(Array(p)[0]) == hex:
					_choose({"floor_cols": Array(p).duplicate()}))


func _section(icon_name: String) -> void:
	var r := Ui.hbox(8)
	r.add_child(Ui.icon(icon_name, 52))
	var line := ColorRect.new()
	line.color = Ui.INK_SOFT
	line.color.a = 0.25
	line.custom_minimum_size = Vector2(0, 3)
	line.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	line.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	r.add_child(line)
	_box.add_child(r)


func _grid(cols: int, n: String) -> GridContainer:
	var g := Ui.grid(cols, 12)
	g.name = n
	_box.add_child(g)
	return g


## Muster-Kachel: Wandfarbe + Muster in Musterfarbe („ohne" = glatte Fläche).
func _pattern_tile(pat: String, cur: Dictionary) -> Button:
	var b := Ui.tile(TILE)
	b.custom_minimum_size = Vector2(TILE, TILE)
	b.name = "Pattern_" + (pat if not pat.is_empty() else "none")
	var bg := ColorRect.new()
	bg.color = Color(String(Array(cur["wall"])[0]))
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 14)
	b.add_child(bg)
	var tex: Texture2D = RoomDecor.pattern_texture(pat)
	if tex != null:
		var pic := TextureRect.new()
		pic.texture = tex
		pic.stretch_mode = TextureRect.STRETCH_TILE
		pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		pic.modulate = Color(String(cur.get("pattern_col", "#ffffff")))
		pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
		pic.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 14)
		b.add_child(pic)
	Ui.mark_selected(b, String(cur.get("pattern", "")) == pat)
	Ui.wire(b, func() -> void: _choose({"pattern": pat}))
	return b


## Boden-Kachel: ein Stück echter Boden, eingefärbt mit dem ersten Farbsatz der Art.
func _floor_tile(kind: String, cur: Dictionary) -> Button:
	var b := Ui.tile(TILE)
	b.custom_minimum_size = Vector2(TILE, TILE)
	b.name = "Floor_" + kind
	var fl: Dictionary = Dictionary(_scene.room.bg_meta.get("floors", {})).get(kind, {})
	var tiles: Array = fl.get("tiles", [])
	if not tiles.is_empty():
		var pic := TextureRect.new()
		var full: Texture2D = load(String((tiles[0] as Dictionary)["file"]))
		var at := AtlasTexture.new()
		at.atlas = full
		var h: float = full.get_height()
		at.region = Rect2(full.get_width() * 0.4, 0, h, h)      # quadratischer Ausschnitt aus der Mitte
		pic.texture = at
		pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		pic.stretch_mode = TextureRect.STRETCH_SCALE
		var preset: Array = Array(RoomDecor.FLOOR_PRESETS.get(kind, [["#d9a066", "#c98a4b", "#8a5a3c"]])[0])
		var m := ShaderMaterial.new()
		m.shader = RoomDecor.SHADER
		for i: int in 3:
			m.set_shader_parameter("zone%d" % (i + 1), Color(String(preset[i])))
		m.set_shader_parameter("ink", RoomDecor.INK)
		pic.material = m
		pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
		pic.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 14)
		b.add_child(pic)
	Ui.mark_selected(b, String(cur.get("floor", "")) == kind)
	Ui.wire(b, func() -> void:
		var d: Dictionary = {"floor": kind}
		if String(cur.get("floor", "")) != kind:
			d["floor_cols"] = Array(RoomDecor.FLOOR_PRESETS[kind][0]).duplicate()
		_choose(d))
	return b
