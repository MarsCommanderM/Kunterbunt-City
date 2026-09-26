class_name Gallery
extends Control
## Figuren- und Haustier-Galerie (P04-T08): unbegrenzt viele Figuren, Ordner, duplizieren,
## löschen (Sicherheitsabfrage per Symbol), aktive Figur wählen. Tiere im zweiten Reiter.

signal play
signal back
signal characters_changed

const FOLDERS: Array = ["Alle", "Familie", "Freunde", "Kita", "Fantasie"]
const MODES: Array = ["chars", "pets"]
const CARD_W: float = 300.0
const CARD_H: float = 400.0

var mode: String = "chars"
var folder: String = "Alle"
var can_back: bool = true
var show_play: bool = true

var _grid: GridContainer
var _folder_row: HBoxContainer
var _title: Label
var _cards: Array = []
var _scroll: ScrollContainer


static func open(host: Node, cb: Callable) -> Gallery:
	var g := Gallery.new()
	g.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(g)
	g.play.connect(cb)
	g.play.connect(func() -> void: g.queue_free())
	g.back.connect(func() -> void: g.queue_free())
	return g


func _ready() -> void:
	Ui.background(self)
	var m := MarginContainer.new()
	m.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	m.add_theme_constant_override("margin_left", 28)
	m.add_theme_constant_override("margin_right", 28)
	m.add_theme_constant_override("margin_top", 22)
	m.add_theme_constant_override("margin_bottom", 22)
	add_child(m)
	var v := Ui.vbox(16)
	m.add_child(v)
	v.add_child(_top_bar())
	_folder_row = Ui.hbox(12)
	_folder_row.custom_minimum_size = Vector2(0, 96)
	v.add_child(_folder_row)
	_scroll = ScrollContainer.new()
	_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(_scroll)
	_grid = Ui.grid(5, 18)
	_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_scroll.add_child(_grid)
	_refresh()


func _top_bar() -> Control:
	var bar := Ui.hbox(16)
	bar.custom_minimum_size = Vector2(0, 116)
	if can_back:
		var b := Ui.button("", "back", "ghost", Vector2(112, 100))
		Ui.wire(b, func() -> void: back.emit(), "ui_back")
		bar.add_child(b)
	_title = Ui.label("Meine Figuren", Ui.FONT_TITLE, Ui.INK, HORIZONTAL_ALIGNMENT_LEFT)
	_title.custom_minimum_size = Vector2(420, 100)
	bar.add_child(_title)
	var tabs := Ui.hbox(10)
	var tc := Ui.button("Figuren", "person", "ghost", Vector2(280, 100))
	Ui.wire(tc, func() -> void:
		mode = "chars"
		_refresh())
	var tp := Ui.button("Tiere", "paw", "ghost", Vector2(250, 100))
	Ui.wire(tp, func() -> void:
		mode = "pets"
		_refresh())
	tabs.add_child(tc)
	tabs.add_child(tp)
	bar.add_child(tabs)
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bar.add_child(sp)
	var plus := Ui.button("Neu", "plus", "accent", Vector2(260, 108))
	Ui.wire(plus, func() -> void: new_card())
	bar.add_child(plus)
	if show_play:
		var play_btn := Ui.button("Spielen", "check", "teal", Vector2(320, 112))
		play_btn.disabled = not Flow.can_play()
		Ui.wire(play_btn, func() -> void: play.emit(), "ui_confirm")
		bar.add_child(play_btn)
	return bar


func _build_folders() -> void:
	for c: Node in _folder_row.get_children():
		c.queue_free()
	if mode != "chars":
		_folder_row.visible = false
		return
	_folder_row.visible = true
	for f: Variant in FOLDERS:
		var b := Ui.button(String(f), "folder", "ghost", Vector2(260, 88))
		Ui.mark_selected(b, folder == String(f))
		Ui.wire(b, func() -> void:
			folder = String(f)
			_refresh())
		_folder_row.add_child(b)


# ------------------------------------------------------------------ Karten
func _refresh() -> void:
	if _grid == null:
		return
	_title.text = "Meine Figuren" if mode == "chars" else "Meine Tiere"
	_build_folders()
	for c: Node in _grid.get_children():
		c.queue_free()
	_cards.clear()
	if mode == "chars":
		await _build_char_cards()
	else:
		_build_pet_cards()


func _visible_characters() -> Array:
	var out: Array = []
	for c: Variant in Game.characters:
		var cd: CharacterData = c
		if folder == "Alle" or cd.folder == folder:
			out.append(cd)
	return out


func _build_char_cards() -> void:
	for c: Variant in _visible_characters():
		var cd: CharacterData = c
		_grid.add_child(await _char_card(cd))
	_grid.add_child(_add_card())


func _char_card(cd: CharacterData) -> Control:
	var card := Ui.card(Ui.RADIUS, Ui.CARD)
	card.custom_minimum_size = Vector2(CARD_W, CARD_H)
	var v := Ui.vbox(8)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 12)
	card.add_child(v)
	var pic := TextureRect.new()
	pic.custom_minimum_size = Vector2(240, 250)
	pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	pic.texture = await Portrait.capture(cd.template_id, cd.look(), 240, 280)
	v.add_child(pic)
	v.add_child(Ui.label(cd.display_name(), Ui.FONT_LABEL))
	var row := Ui.hbox(8)
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	var act := Ui.button("", "check", "teal" if Game.active_id == cd.id else "ghost",
		Vector2(64, 64))
	act.disabled = not cd.is_complete()
	Ui.wire(act, func() -> void:
		Game.set_active(cd.id)
		Game.save_characters()
		_refresh())
	row.add_child(act)
	var ed := Ui.button("", "pencil", "ghost", Vector2(64, 64))
	Ui.wire(ed, func() -> void:
		CharacterEditor.open(self, cd, false, func(d: CharacterData) -> void:
			Game.save_characters()
			_refresh()))
	row.add_child(ed)
	var cp := Ui.button("", "copy", "ghost", Vector2(64, 64))
	Ui.wire(cp, func() -> void:
		duplicate_card(cd.id))
	row.add_child(cp)
	var tr := Ui.button("", "trash", "ghost", Vector2(64, 64))
	Ui.wire(tr, func() -> void:
		_confirm_delete(cd.display_name(), func() -> void:
			delete_card(cd.id)), "deny")
	row.add_child(tr)
	v.add_child(row)
	_cards.append({"node": card, "id": cd.id})
	return card


func _build_pet_cards() -> void:
	for p: Variant in Game.pets:
		var pd: PetData = p
		_grid.add_child(_pet_card(pd))
	_grid.add_child(_add_card())


func _pet_card(pd: PetData) -> Control:
	var card := Ui.card(Ui.RADIUS, Ui.CARD)
	card.custom_minimum_size = Vector2(CARD_W, CARD_H)
	var v := Ui.vbox(8)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 12)
	card.add_child(v)
	var stage := PetStage.new()
	stage.custom_minimum_size = Vector2(240, 250)
	stage.show_pet(pd.species_id, [pd.fur, pd.fur2, pd.collar])
	v.add_child(stage)
	v.add_child(Ui.label(pd.display_name(), Ui.FONT_LABEL))
	var row := Ui.hbox(8)
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	var act := Ui.button("", "check", "teal" if Game.active_pets.has(pd.id) else "ghost",
		Vector2(64, 64))
	Ui.wire(act, func() -> void:
		Game.toggle_active_pet(pd.id)
		Game.save_pets()
		_refresh())
	row.add_child(act)
	var snd := Ui.button("", "speaker", "ghost", Vector2(64, 64))
	Ui.wire(snd, func() -> void: AudioBus.play_sfx(PetSpecies.voice(pd.species_id)))
	row.add_child(snd)
	var ed := Ui.button("", "pencil", "ghost", Vector2(64, 64))
	Ui.wire(ed, func() -> void:
		PetEditor.open(self, pd, func(x: PetData) -> void:
			pd.fur = x.fur
			pd.fur2 = x.fur2
			pd.collar = x.collar
			pd.pet_trait = x.pet_trait
			pd.pattern = x.pattern
			pd.pet_name = x.pet_name
			pd.species_id = x.species_id
			Game.save_pets()
			_refresh()))
	row.add_child(ed)
	var tr := Ui.button("", "trash", "ghost", Vector2(64, 64))
	Ui.wire(tr, func() -> void:
		_confirm_delete(pd.display_name(), func() -> void:
			Game.remove_pet(pd.id)
			_refresh()), "deny")
	row.add_child(tr)
	v.add_child(row)
	var trait_row := Ui.hbox(6)
	trait_row.alignment = BoxContainer.ALIGNMENT_CENTER
	trait_row.add_child(Ui.icon(PetSpecies.trait_icon(pd.pet_trait), 40.0))
	trait_row.add_child(Ui.icon(PetSpecies.icon(pd.species_id), 40.0))
	v.add_child(trait_row)
	_cards.append({"node": card, "id": pd.id})
	return card


func _add_card() -> Control:
	var b := Ui.tile(CARD_W)
	b.custom_minimum_size = Vector2(CARD_W, CARD_H)
	b.text = ""
	var inner := Ui.vbox(10)
	inner.mouse_filter = Control.MOUSE_FILTER_IGNORE
	inner.alignment = BoxContainer.ALIGNMENT_CENTER
	inner.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 12)
	b.add_child(inner)
	var pic := Ui.icon("plus", 150.0, Ui.ACCENT)
	inner.add_child(pic)
	inner.add_child(Ui.label("Neu", Ui.FONT_LABEL, Ui.INK_SOFT))
	Ui.mark_selected(b, false)
	Ui.wire(b, func() -> void: new_card())
	return b


# ------------------------------------------------------------------ Aktionen (auch für Tests)
func new_card() -> void:
	if mode == "chars":
		var d: CharacterData = CharacterData.create("kid")
		d.folder = folder if folder != "Alle" else "Familie"
		CharacterEditor.open(self, d, false, func(c: CharacterData) -> void:
			Game.add_character(c)
			Game.set_active(c.id)
			_refresh())
	else:
		PetEditor.open(self, PetData.create(), func(p: PetData) -> void:
			Game.add_pet(p)
			_refresh())


func delete_card(id: StringName) -> void:
	if mode == "chars":
		Game.remove_character(id)
	else:
		Game.remove_pet(id)
	_refresh()


func duplicate_card(id: StringName) -> void:
	if mode == "chars":
		Game.duplicate_character(id)
	else:
		var src: PetData = Game.pet_by_id(id)
		if src != null:
			var copy: PetData = PetData.from_dict(src.to_dict())
			copy.id = StringName("p_%d_%d" % [Time.get_unix_time_from_system(), randi() % 100000])
			Game.add_pet(copy)
	_refresh()


func card_count() -> int:
	return _cards.size()


## Löschen bestätigen – nur Symbole, kein Lesen nötig.
func _confirm_delete(what: String, cb: Callable) -> void:
	var host := Control.new()
	host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(host)
	var dim := ColorRect.new()
	dim.color = Color(0.16, 0.12, 0.22, 0.45)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(dim)
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	panel.size = Vector2(720, 460)
	panel.position = Vector2(-360, -230)
	host.add_child(panel)
	var v := Ui.vbox(18)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 24)
	panel.add_child(v)
	v.add_child(Ui.icon("trash", 120.0, Ui.PINK))
	v.add_child(Ui.label(what, Ui.FONT_TITLE))
	v.add_child(Ui.label("Wirklich löschen?", Ui.FONT_LABEL, Ui.INK_SOFT))
	var row := Ui.hbox(20)
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	var yes := Ui.button("", "check", "pink", Vector2(180, 130))
	Ui.wire(yes, func() -> void:
		host.queue_free()
		cb.call(), "ui_back")
	var no := Ui.button("", "close", "teal", Vector2(180, 130))
	Ui.wire(no, func() -> void: host.queue_free(), "ui_back")
	row.add_child(yes)
	row.add_child(no)
	v.add_child(row)
