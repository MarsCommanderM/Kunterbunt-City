class_name Album
extends Control
## Foto-Album (P05-T04): alle Fotos, die mit 📷 in einem Bereich gemacht wurden.
## Liegen lokal unter user://album/ – kein Netz, keine Cloud.

static func open(host: Node) -> Album:
	var a := Album.new()
	a.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(a)
	return a


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.16, 0.12, 0.22, 0.45)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	panel.size = Vector2(1500, 940)
	panel.position = Vector2(-750, -470)
	add_child(panel)
	var v := Ui.vbox(14)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 24)
	panel.add_child(v)
	var head := Ui.hbox(14)
	head.alignment = BoxContainer.ALIGNMENT_CENTER
	head.add_child(Ui.label("Album", Ui.FONT_TITLE))
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(sp)
	var x := Ui.button("", "close", "ghost", Vector2(96, 96))
	Ui.wire(x, func() -> void: queue_free(), "ui_back")
	head.add_child(x)
	v.add_child(head)
	var files: Array = SaveSystem.album_photos()
	if files.is_empty():
		v.add_child(Ui.label("Noch kein Foto – drück im Bereich auf 📷", Ui.FONT_LABEL,
			Ui.INK_SOFT))
		return
	var s := ScrollContainer.new()
	s.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(s)
	var g := Ui.grid(4, 16)
	g.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 10)
	s.add_child(g)
	for f: Variant in files:
		g.add_child(_tile(String(f)))


func _tile(path: String) -> Control:
	var b := Ui.tile(330.0)
	b.custom_minimum_size = Vector2(330, 250)
	var img := Image.new()
	var pic := TextureRect.new()
	if img.load(path) == OK:
		pic.texture = ImageTexture.create_from_image(img)
	pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	pic.custom_minimum_size = Vector2(310, 180)
	pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var box := Ui.vbox(6)
	box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	box.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 8)
	b.add_child(box)
	box.add_child(pic)
	var del := Ui.label("löschen", Ui.FONT_SMALL, Ui.INK_SOFT)
	box.add_child(del)
	Ui.wire(b, func() -> void:
		SaveSystem.album_remove(path)
		queue_free()
		call_deferred("_reopen"), "deny")
	return b


func _reopen() -> void:
	if get_parent() != null:
		Album.open(get_parent())
