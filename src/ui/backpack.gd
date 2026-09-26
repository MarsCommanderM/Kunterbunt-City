class_name Backpack
extends Control
## Rucksack (P05-T11 / Tech-Spec §4.7): 20 Plätze, Dinge wandern zwischen Bereichen mit.
## Antippen: gefüllter Platz → rausholen (im Bereich), leerer Platz bleibt leer.
## Rein kommt ein Ding, indem man es auf den Rucksack-Knopf zieht (AreaScene).

signal changed

const SLOTS: int = 20
const TILE: float = 190.0

var _grid: GridContainer
var _place_cb: Callable


static func open(host: Node, place_cb: Callable = Callable(), cb: Callable = Callable()) -> Backpack:
	var b := Backpack.new()
	b.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	b._place_cb = place_cb
	host.add_child(b)
	if cb.is_valid():
		b.changed.connect(cb)
	return b


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.16, 0.12, 0.22, 0.45)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	panel.size = Vector2(1180, 900)
	panel.position = Vector2(-590, -450)
	add_child(panel)
	var v := Ui.vbox(14)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 24)
	panel.add_child(v)
	var head := Ui.hbox(14)
	head.alignment = BoxContainer.ALIGNMENT_CENTER
	head.add_child(Ui.label("Rucksack", Ui.FONT_TITLE))
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(sp)
	head.add_child(Ui.label("%d / %d" % [Game.backpack.size(), SLOTS], Ui.FONT_LABEL, Ui.INK_SOFT))
	var x := Ui.button("", "close", "ghost", Vector2(96, 96))
	Ui.wire(x, func() -> void: queue_free(), "ui_back")
	head.add_child(x)
	v.add_child(head)
	_grid = Ui.grid(5, 16)
	_grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(_grid)
	v.add_child(Ui.label("Zum Einpacken: Ding auf den Rucksack ziehen", Ui.FONT_SMALL,
		Ui.INK_SOFT))
	_fill()


func _fill() -> void:
	for c: Node in _grid.get_children():
		c.queue_free()
	for i: int in SLOTS:
		var b := Ui.tile(TILE)
		b.custom_minimum_size = Vector2(TILE, TILE)
		if i < Game.backpack.size():
			var e: Dictionary = Game.backpack[i]
			var def: ItemDefinition = ItemDB.get_item(StringName(String(e.get("id", ""))))
			if def != null:
				var pic := TextureRect.new()
				pic.texture = load(def.sprite_path)
				pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
				pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
				pic.custom_minimum_size = Vector2(TILE - 40, TILE - 40)
				pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
				var box := Ui.vbox(2)
				box.mouse_filter = Control.MOUSE_FILTER_IGNORE
				box.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT,
					Control.PRESET_MODE_MINSIZE, 10)
				b.add_child(box)
				box.add_child(pic)
			Ui.mark_selected(b, true)
			Ui.wire(b, func() -> void: _take_out(i))
		else:
			Ui.mark_selected(b, false)
		_grid.add_child(b)


func _take_out(i: int) -> void:
	if i >= Game.backpack.size():
		return
	if not _place_cb.is_valid():
		AudioBus.play_sfx("deny")
		return
	var e: Dictionary = Game.backpack[i]
	if _place_cb.call(String(e.get("id", "")), i):
		Game.backpack.remove_at(i)
		Game.save_now()
		_fill()
		changed.emit()


# ------------------------------------------------------------------ statisch: einpacken
## Ding in den Rucksack legen (AreaScene zieht es auf den Knopf).
static func stash(item: ItemNode) -> bool:
	if Game.backpack.size() >= SLOTS:
		AudioBus.play_sfx("deny")
		return false
	Game.backpack.append({"id": String(item.def.id)})
	var p: Node = item.get_parent()
	if p != null:
		p.remove_child(item)
	item.queue_free()
	Game.save_now()
	AudioBus.play_sfx("ui_confirm")
	return true


static func is_full() -> bool:
	return Game.backpack.size() >= SLOTS
