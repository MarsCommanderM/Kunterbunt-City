class_name RoomPicker
extends Control
## P07-T01: Raum-Wahl im Bereich – ein Vorschaubild je Raum (so, wie das Kind ihn zuletzt eingerichtet hat,
## sonst das Standard-Bild), dazu ein kleines Erkennungs-Ding (Sofa, Bett, Badewanne …). Kein Text (R-07).

const TILE: Vector2 = Vector2(330, 210)

var _scene: AreaScene


static func open(host: Node, scene: AreaScene) -> RoomPicker:
	var p := RoomPicker.new()
	p._scene = scene
	p.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(p)
	return p


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.16, 0.12, 0.22, 0.45)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var ids: Array = _scene.room_ids()
	var cols: int = 4
	var rows: int = ceili(ids.size() / float(cols))
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.size = Vector2(cols * (TILE.x + 18) + 60, rows * (TILE.y + 18) + 170)
	panel.set_anchors_preset(Control.PRESET_CENTER)
	panel.position = -panel.size * 0.5
	add_child(panel)
	var v := Ui.vbox(14)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 24)
	panel.add_child(v)
	var head := Ui.hbox(14)
	head.add_child(Ui.icon("home", 84))
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(sp)
	var x := Ui.button("", "close", "ghost", Vector2(96, 96))
	x.name = "Close"
	Ui.wire(x, func() -> void: queue_free(), "ui_back")
	head.add_child(x)
	v.add_child(head)
	var grid := Ui.grid(cols, 18)
	grid.name = "Rooms"
	v.add_child(grid)
	var current: String = String(_scene.room.room_id) if _scene.room != null else ""
	for rid: Variant in ids:
		grid.add_child(_tile(String(rid), String(rid) == current))


func _tile(rid: String, selected: bool) -> Button:
	var b := Ui.tile(TILE.x)
	b.custom_minimum_size = TILE
	b.name = "Room_" + rid
	b.set_meta("room", rid)
	var data: Dictionary = _scene.room_data(rid)
	var thumb: Texture2D = thumb_of(String(_scene.area_id), rid)
	if thumb != null:
		var pic := TextureRect.new()
		pic.texture = thumb
		pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
		pic.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 12)
		b.add_child(pic)
	var def: ItemDefinition = ItemDB.get_item(StringName(String(data.get("icon", ""))))
	if def != null:                                    # Erkennungs-Ding unten rechts
		var badge := Panel.new()                      # weißer Kreis unten rechts IN der Kachel
		badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(1, 1, 1, 0.92)
		sb.set_corner_radius_all(60)
		badge.add_theme_stylebox_override("panel", sb)
		badge.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
		badge.offset_left = -118
		badge.offset_top = -118
		badge.offset_right = -14
		badge.offset_bottom = -14
		b.add_child(badge)
		var icon: TextureRect = ItemThumb.make(def, 80)
		icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
		icon.set_anchors_preset(Control.PRESET_FULL_RECT)
		icon.offset_left = 12
		icon.offset_top = 12
		icon.offset_right = -12
		icon.offset_bottom = -12
		icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		badge.add_child(icon)
	Ui.mark_selected(b, selected)
	Ui.wire(b, func() -> void:
		_scene.switch_room(rid)
		queue_free())
	return b


static func thumb_of(area_id: String, rid: String) -> Texture2D:
	var p: String = "res://assets/backgrounds/%s/%s_thumb.png" % [area_id, rid]
	return load(p) if ResourceLoader.exists(p) else null
