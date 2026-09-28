class_name PetEditor
extends Control
## Haustier-Editor (P04-T09): Tierart, Fell (2 Farben), Muster, Halsband, Charakterzug.
## Links das Tier (Tippen = Stimme hören), rechts Kategorien als Symbole, unten die Farben.

signal finished(pet: PetData)
signal cancelled

const CATS: Array = [
	{"id": "species", "icon": "paw", "label": "Tierart"},
	{"id": "fur", "icon": "palette", "label": "Fell"},
	{"id": "fur2", "icon": "palette", "label": "Bauch"},
	{"id": "collar", "icon": "heart", "label": "Halsband"},
	{"id": "pattern", "icon": "brush", "label": "Muster"},
	{"id": "trait", "icon": "ball", "label": "Charakter"},
]

var pet: PetData
var _cat: String = "species"
var _stage: PetStage
var _cat_row: HBoxContainer
var _variants: GridContainer
var _palette_row: HBoxContainer
var _name_btn: Button
var _done: Button


static func open(host: Node, p: PetData, cb: Callable) -> PetEditor:
	var e := PetEditor.new()
	e.pet = p if p != null else PetData.create()
	e.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(e)
	e.finished.connect(cb)
	e.finished.connect(func(_x: PetData) -> void: e.queue_free())
	e.cancelled.connect(func() -> void: e.queue_free())
	return e


func _ready() -> void:
	Ui.background(self)
	var m := MarginContainer.new()
	m.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	m.add_theme_constant_override("margin_left", 28)
	m.add_theme_constant_override("margin_right", 28)
	m.add_theme_constant_override("margin_top", 22)
	m.add_theme_constant_override("margin_bottom", 22)
	add_child(m)
	var v := Ui.vbox(18)
	m.add_child(v)
	v.add_child(_top_bar())
	var body := Control.new()
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(body)
	var left := _preview_card()
	left.set_anchors_and_offsets_preset(Control.PRESET_LEFT_WIDE)
	left.set_offset(SIDE_RIGHT, 720)
	body.add_child(left)
	var right := _right_column()
	right.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	right.set_offset(SIDE_LEFT, 740)
	body.add_child(right)
	_refresh()


func _top_bar() -> Control:
	var bar := Ui.hbox(16)
	bar.custom_minimum_size = Vector2(0, 116)
	var back := Ui.button("", "back", "ghost", Vector2(112, 100))
	Ui.wire(back, func() -> void: cancelled.emit(), "ui_back")
	bar.add_child(back)
	_name_btn = Ui.button(_title(), "nametag", "ghost", Vector2(420, 100))
	Ui.wire(_name_btn, func() -> void:
		NamePicker.open(self, pet.pet_name, 1, func(n: String) -> void:
			pet.pet_name = n
			_name_btn.text = " " + _title()))
	bar.add_child(_name_btn)
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bar.add_child(sp)
	var dice := Ui.button("Würfeln", "dice", "accent", Vector2(300, 100))
	Ui.wire(dice, func() -> void: roll_dice(), "dice_roll")
	bar.add_child(dice)
	_done = Ui.button("Fertig", "check", "accent", Vector2(330, 112))
	Ui.wire(_done, func() -> void: finished.emit(pet), "ui_confirm")
	bar.add_child(_done)
	return bar


func _title() -> String:
	return pet.pet_name if not pet.pet_name.is_empty() else "Name?"


func _preview_card() -> Control:
	var card := Ui.card(Ui.RADIUS, Ui.CARD)
	card.custom_minimum_size = Vector2(700, 940)
	card.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	var v := Ui.vbox(12)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 18)
	card.add_child(v)
	_stage = PetStage.new()
	_stage.custom_minimum_size = Vector2(660, 660)
	_stage.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	_stage.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	v.add_child(_stage)
	var tap := Ui.button("Stimme hören", "speaker", "teal", Vector2(420, 104))
	Ui.wire(tap, func() -> void: play_voice())
	v.add_child(tap)
	var lbl := Ui.label("", Ui.FONT_LABEL, Ui.INK_SOFT)
	lbl.name = "SpeciesLabel"
	v.add_child(lbl)
	return card


func _right_column() -> Control:
	var v := Ui.vbox(16)
	v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_cat_row = Ui.hbox(12)
	_cat_row.custom_minimum_size = Vector2(0, 128)
	v.add_child(_cat_row)
	var card := Ui.card(Ui.RADIUS, Ui.CARD_SOFT)
	card.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(card)
	var sv := ScrollContainer.new()
	sv.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 16)
	card.add_child(sv)
	_variants = Ui.grid(4, 16)
	_variants.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sv.add_child(_variants)
	var pal := Ui.card(Ui.RADIUS, Ui.CARD)
	pal.custom_minimum_size = Vector2(0, 180)
	v.add_child(pal)
	_palette_row = Ui.hbox(14)
	_palette_row.alignment = BoxContainer.ALIGNMENT_CENTER
	_palette_row.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 14)
	pal.add_child(_palette_row)
	return v


# ------------------------------------------------------------------ Inhalt
func _build_cats() -> void:
	for c: Node in _cat_row.get_children():
		c.queue_free()
	for cat: Variant in CATS:
		var id: String = String((cat as Dictionary)["id"])
		var b := Ui.button("", String((cat as Dictionary)["icon"]), "", Vector2(120, 116))
		Ui.mark_selected(b, id == _cat)
		Ui.wire(b, func() -> void:
			_cat = id
			_refresh())
		_cat_row.add_child(b)


func _build_variants() -> void:
	for c: Node in _variants.get_children():
		c.queue_free()
	_variants.columns = 4
	match _cat:
		"species":
			_variants.columns = 4
			for sid: Variant in PetSpecies.ids():
				var b := Ui.tile(200.0)
				b.custom_minimum_size = Vector2(200, 230)
				var inner := Ui.vbox(6)
				inner.mouse_filter = Control.MOUSE_FILTER_IGNORE
				inner.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT,
					Control.PRESET_MODE_MINSIZE, 8)
				b.add_child(inner)
				inner.add_child(_pet_pic(String(sid), PetSpecies.default_fur(String(sid)), "plain"))   # echtes Tier
				inner.add_child(Ui.label(PetSpecies.label(String(sid)), Ui.FONT_SMALL))
				Ui.mark_selected(b, pet.species_id == String(sid))
				Ui.wire(b, func() -> void:
					pet.species_id = String(sid)
					var cols: Array = PetSpecies.default_fur(pet.species_id)
					pet.fur = String(cols[0])
					pet.fur2 = String(cols[1])
					pet.collar = String(cols[2])
					play_voice()
					_refresh())
				_variants.add_child(b)
		"fur", "fur2", "collar":
			_variants.columns = 5
			_build_swatches(_current_colors(), 140.0)
		"pattern":
			_variants.columns = 5
			for p: Variant in PetSpecies.patterns():
				var pid: String = String((p as Dictionary)["id"])
				var b := Ui.tile(190.0)
				b.custom_minimum_size = Vector2(190, 190)
				var pic := _pet_pic(pet.species_id, [pet.fur, pet.fur2, pet.collar], pid)      # Muster am Tier zeigen
				pic.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 12)
				b.add_child(pic)
				Ui.mark_selected(b, pet.pattern == pid)
				Ui.wire(b, func() -> void:
					pet.pattern = pid
					_refresh())
				_variants.add_child(b)
		"trait":
			_variants.columns = 5
			for t: Variant in PetSpecies.traits(pet.species_id):
				var tid: String = String((t as Dictionary)["id"])
				var b := Ui.tile(190.0)
				b.custom_minimum_size = Vector2(190, 190)
				var inner := Ui.vbox(6)
				inner.mouse_filter = Control.MOUSE_FILTER_IGNORE
				inner.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT,
					Control.PRESET_MODE_MINSIZE, 8)
				b.add_child(inner)
				var pic := Ui.icon(PetSpecies.trait_icon(tid), 96.0)
				inner.add_child(pic)
				inner.add_child(Ui.label(PetSpecies.trait_label(tid), Ui.FONT_SMALL))
				Ui.mark_selected(b, pet.pet_trait == tid)
				Ui.wire(b, func() -> void:
					pet.pet_trait = tid
					_refresh())
				_variants.add_child(b)


func _current_colors() -> Array:
	if _cat == "fur2":
		return CharacterParts.palette_colors("fur")
	if _cat == "collar":
		var out: Array = []
		for c: Variant in PetSpecies.collars():
			out.append(String((c as Dictionary)["color"]))
		return out
	return CharacterParts.palette_colors("fur")


func _build_swatches(colors: Array, size: float) -> void:
	ColorDots.fill(_variants, colors, size, _current_color(), select_color)


func _build_palette() -> void:
	ColorDots.fill(_palette_row, _current_colors(), 84.0, _current_color(), select_color)


## Kleines Tierbild (Kachel): dieselbe Einfärbung wie im Spiel.
func _pet_pic(sid: String, cols: Array, pat: String) -> PetStage:
	var st := PetStage.new()
	st.custom_minimum_size = Vector2(180, 150)
	st.mouse_filter = Control.MOUSE_FILTER_IGNORE
	st.show_pet(sid, cols, pat)
	return st


func _current_color() -> String:
	match _cat:
		"fur":
			return pet.fur
		"fur2":
			return pet.fur2
		"collar":
			return pet.collar
	return ""


# ------------------------------------------------------------------ Aktionen
## Kategorie wechseln („species", „fur", „fur2", „collar", „pattern", „trait").
func select_category(cat: String) -> void:
	for c: Variant in CATS:
		if String((c as Dictionary)["id"]) == cat:
			_cat = cat
			_refresh()
			return


func select_color(hex: String) -> void:
	match _cat:
		"fur":
			pet.fur = hex
		"fur2":
			pet.fur2 = hex
		"collar":
			pet.collar = hex
	_refresh()


func set_species(sid: String) -> void:
	if not PetSpecies.ids().has(sid):
		return
	pet.species_id = sid
	_refresh()


func set_trait(tid: String) -> void:
	if PetSpecies.trait_ids(pet.species_id).has(tid):
		pet.pet_trait = tid
		_refresh()


func set_pattern(pid: String) -> void:
	if PetSpecies.pattern_ids().has(pid):
		pet.pattern = pid
		_refresh()


func roll_dice() -> void:
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	var ids: Array = PetSpecies.ids()
	var sid: String = String(ids[rng.randi() % ids.size()])
	pet.species_id = sid
	var cols: Array = PetSpecies.default_fur(sid)
	pet.fur = String(CharacterParts.palette_colors("fur")[rng.randi() % 8])
	pet.fur2 = String(cols[1])
	pet.collar = String(cols[2])
	var ps: Array = PetSpecies.pattern_ids()
	pet.pattern = String(ps[rng.randi() % ps.size()])
	var ts: Array = PetSpecies.trait_ids(sid)
	pet.pet_trait = String(ts[rng.randi() % ts.size()])
	AudioBus.play_sfx("dice_roll")
	_refresh()


func play_voice() -> void:
	AudioBus.play_sfx(PetSpecies.voice(pet.species_id))


func _refresh() -> void:
	if _stage == null:
		return
	_stage.show_pet(pet.species_id, [pet.fur, pet.fur2, pet.collar], pet.pattern)
	_build_cats()
	_build_variants()
	_build_palette()
	var lbl: Label = _stage.get_parent().get_node_or_null("SpeciesLabel") as Label
	if lbl != null:
		var def: ItemDefinition = ItemDB.get_item(StringName(pet.species_id))
		lbl.text = tr("%s · %d cm hoch") % [PetSpecies.label(pet.species_id),
			int(def.height_cm) if def != null else 0]
	if _name_btn != null:
		_name_btn.text = " " + _title()
	_done.disabled = not pet.is_complete()
