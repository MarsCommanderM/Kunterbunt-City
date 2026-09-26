class_name CharacterEditor
extends Control
## Charakter-Editor (P04-T03/T05/T06/T07).
## Links die große Vorschau (Tippen = Gefühl wechseln), rechts Kategorien als SYMBOLE, unten die
## Farben. Ohne Lesen bedienbar. Pflicht: Schablone + Hautton, sonst bleibt der ✓-Knopf aus.

signal finished(data: CharacterData)
signal cancelled

const TEMPLATES: Array = ["toddler", "kid", "adult"]
const CATS: Array = [
	{"id": "template", "icon": "person", "label": "Größe"},
	{"id": "skin", "icon": "hand", "label": "Haut"},
	{"id": "hair", "icon": "hair", "label": "Haare"},
	{"id": "top", "icon": "shirt", "label": "Oberteil"},
	{"id": "bottom", "icon": "pants", "label": "Hose"},
	{"id": "shoes", "icon": "shoe", "label": "Schuhe"},
	{"id": "eyes", "icon": "eye", "label": "Augen"},
	{"id": "mouth", "icon": "mouth", "label": "Mund"},
	{"id": "accessory", "icon": "bow", "label": "Hut & mehr"},
	{"id": "aid", "icon": "heart", "label": "Hilfe"},
]

var data: CharacterData
var mandatory: bool = false      ## true = Pflicht-Ablauf (kein Zurück, bevor die Figur fertig ist)
var _slot: String = "top"
var _zone: int = 0
var _last_outfit: int = 0

var _stage: FigureStage
var _cat_row: HBoxContainer
var _variants: GridContainer
var _palette_row: HBoxContainer
var _zone_row: HBoxContainer
var _done: Button
var _hint: Label
var _name_btn: Button
var _outfit_row: HBoxContainer


static func open(host: Node, d: CharacterData, is_mandatory: bool, cb: Callable) -> CharacterEditor:
	var e := CharacterEditor.new()
	e.data = d
	e.mandatory = is_mandatory
	e.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(e)
	e.finished.connect(cb)
	e.finished.connect(func(_x: CharacterData) -> void: e.queue_free())
	e.cancelled.connect(func() -> void: e.queue_free())
	return e


func _ready() -> void:
	if data == null:
		data = CharacterData.create("kid")
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
	# Feste Aufteilung: links die Vorschau (720 px), rechts die Auswahl (Rest). Anker statt
	# Container-Ketten – so kann die Mindestbreite der Kacheln die Vorschau nicht wegdrücken.
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


# ------------------------------------------------------------------ Kopfzeile
func _top_bar() -> Control:
	var bar := Ui.hbox(16)
	bar.custom_minimum_size = Vector2(0, 116)
	if not mandatory:
		var back := Ui.button("", "back", "ghost", Vector2(112, 100))
		Ui.wire(back, func() -> void: cancelled.emit(), "ui_back")
		bar.add_child(back)
	_name_btn = Ui.button(_title_text(), "nametag", "ghost", Vector2(420, 100))
	Ui.wire(_name_btn, func() -> void:
		NamePicker.open(self, data.character_name, data.voice, func(n: String) -> void:
			data.character_name = n
			_name_btn.text = " " + _title_text()
			Game.save_characters()))
	bar.add_child(_name_btn)
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bar.add_child(sp)
	var dice := Ui.button("Würfeln", "dice", "accent", Vector2(300, 100))
	Ui.wire(dice, func() -> void: roll_dice(), "dice_roll")
	bar.add_child(dice)
	var pet := Ui.button("Tier", "paw", "teal", Vector2(250, 100))
	Ui.wire(pet, func() -> void:
		PetEditor.open(self, PetData.create("pet_dog_medium"), func(p: PetData) -> void:
			Game.add_pet(p)))
	bar.add_child(pet)
	_done = Ui.button("Fertig", "check", "accent", Vector2(330, 112))
	_done.disabled = true
	Ui.wire(_done, func() -> void:
		finished.emit(data), "ui_confirm")
	bar.add_child(_done)
	return bar


func _title_text() -> String:
	return data.character_name if not data.character_name.is_empty() else "Name?"


# ------------------------------------------------------------------ Vorschau
func _preview_card() -> Control:
	var card := Ui.card(Ui.RADIUS, Ui.CARD)
	card.custom_minimum_size = Vector2(700, 940)
	card.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN   # Vorschau bleibt immer gleich breit
	var v := Ui.vbox(12)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 18)
	card.add_child(v)
	_stage = FigureStage.new()
	_stage.custom_minimum_size = Vector2(660, 660)
	_stage.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	_stage.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_stage.tapped.connect(func() -> void:
		_stage.next_emotion()
		AudioBus.play_sfx("tap"))
	v.add_child(_stage)
	_hint = Ui.label("Wähle eine Hautfarbe", Ui.FONT_SMALL, Ui.ACCENT_DARK)
	v.add_child(_hint)
	v.add_child(Ui.label("Tippen = Gefühl", Ui.FONT_SMALL, Ui.INK_SOFT))
	_outfit_row = Ui.hbox(10)
	_outfit_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(_outfit_row)
	_build_outfits()
	return card


func _build_outfits() -> void:
	for c: Node in _outfit_row.get_children():
		c.queue_free()
	for i: int in CharacterData.OUTFITS:
		var b := Ui.tile(96.0)
		b.text = str(i + 1)
		b.add_theme_font_size_override("font_size", 30)
		var filled: bool = not Dictionary(data.outfits[i]).is_empty()
		Ui.mark_selected(b, filled and data.outfit == i)
		if filled:
			b.icon = Ui.tex("star")
			b.expand_icon = true
		Ui.wire(b, func() -> void: _outfit_tap(i))
		_outfit_row.add_child(b)
	var trash := Ui.button("", "trash", "ghost", Vector2(96, 96))
	Ui.wire(trash, func() -> void: clear_outfit(_last_outfit), "ui_back")
	_outfit_row.add_child(trash)


func _outfit_tap(i: int) -> void:
	_last_outfit = i
	if Dictionary(data.outfits[i]).is_empty():
		store_outfit(i)
	else:
		wear_outfit(i)


# ------------------------------------------------------------------ rechte Spalte
func _right_column() -> Control:
	var v := Ui.vbox(16)
	v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_cat_row = Ui.hbox(12)
	_cat_row.custom_minimum_size = Vector2(0, 128)
	v.add_child(_cat_row)
	_build_cats()
	var card := Ui.card(Ui.RADIUS, Ui.CARD_SOFT)
	card.size_flags_vertical = Control.SIZE_EXPAND_FILL
	card.custom_minimum_size = Vector2(0, 520)
	v.add_child(card)
	var sv := ScrollContainer.new()
	sv.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 16)
	card.add_child(sv)
	_variants = Ui.grid(4, 16)
	_variants.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sv.add_child(_variants)
	var pal_card := Ui.card(Ui.RADIUS, Ui.CARD)
	pal_card.custom_minimum_size = Vector2(0, 200)
	v.add_child(pal_card)
	var pv := Ui.vbox(8)
	pv.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 14)
	pal_card.add_child(pv)
	_zone_row = Ui.hbox(12)
	_zone_row.alignment = BoxContainer.ALIGNMENT_CENTER
	pv.add_child(_zone_row)
	_palette_row = Ui.hbox(14)
	_palette_row.alignment = BoxContainer.ALIGNMENT_CENTER
	pv.add_child(_palette_row)
	return v


func _build_cats() -> void:
	for c: Node in _cat_row.get_children():
		c.queue_free()
	for cat: Variant in CATS:
		var id: String = String((cat as Dictionary)["id"])
		var b := Ui.button("", String((cat as Dictionary)["icon"]), "", Vector2(120, 116))
		Ui.mark_selected(b, id == _slot)
		Ui.wire(b, func() -> void: select_category(id))
		_cat_row.add_child(b)


# ------------------------------------------------------------------ Inhalt je Kategorie
func _build_variants() -> void:
	for c: Node in _variants.get_children():
		c.queue_free()
	_variants.columns = 4
	if _slot == "template":
		_build_templates()
	elif _slot == "skin":
		_variants.columns = 5
		_build_swatches(CharacterParts.palette_colors("skin"), 150.0)
	else:
		for id: Variant in CharacterParts.ids(_slot):
			_variants.add_child(_part_tile(String(id)))


func _build_templates() -> void:
	_variants.columns = 3
	for tid: Variant in TEMPLATES:
		var t: Dictionary = CharacterTemplates.get_template(String(tid))
		var cm: float = float(ItemDB.height_cm(String(t.get("scale_ref", "char_child"))))
		var b := Ui.tile(240.0)
		b.custom_minimum_size = Vector2(240, 300)
		var inner := Ui.vbox(6)
		inner.mouse_filter = Control.MOUSE_FILTER_IGNORE
		inner.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 8)
		b.add_child(inner)
		var pic := Ui.icon("person", 150.0)
		pic.custom_minimum_size = Vector2(200, 170)
		inner.add_child(pic)
		inner.add_child(Ui.label("%d cm" % int(cm), 34))
		Ui.mark_selected(b, data.template_id == String(tid))
		Ui.wire(b, func() -> void: select_template(String(tid)))
		_variants.add_child(b)


func _build_swatches(colors: Array, size: float) -> void:
	for hex: Variant in colors:
		var b := Ui.tile(size)
		b.text = ""
		var fill: Color = Color(String(hex))
		b.add_theme_stylebox_override("normal", Ui.box(fill, Ui.RADIUS_SMALL,
			Color(0, 0, 0, 0), 0, 8))
		b.add_theme_stylebox_override("hover", Ui.box(fill.lightened(0.08), Ui.RADIUS_SMALL,
			Color(0, 0, 0, 0), 0, 12))
		b.add_theme_stylebox_override("pressed", Ui.box(fill.darkened(0.12), Ui.RADIUS_SMALL,
			Color(0, 0, 0, 0), 0, 2))
		var cur: String = _current_color()
		Ui.mark_selected(b, cur == String(hex))
		Ui.wire(b, func() -> void: select_color(String(hex)))
		_variants.add_child(b)


## Kachel mit dem Teil-Sprite, schon in der richtigen Farbe (Shader).
func _part_tile(id: String) -> Control:
	var b := Ui.tile(200.0)
	b.custom_minimum_size = Vector2(200, 240)
	var v: Dictionary = CharacterParts.variant(_slot, id)
	var part: String = String(v.get("part", ""))
	var pic := TextureRect.new()
	pic.texture = CharacterTemplates.part_texture(data.template_id, part)
	pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	pic.custom_minimum_size = Vector2(180, 170)
	pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var cols: Array = []
	for c: Variant in Array(data.colors.get(_slot, [])):
		cols.append(Color(String(c)))
	if cols.is_empty():
		cols = [Color.WHITE]
	CharacterLook.apply(pic, cols)
	var box := Ui.vbox(4)
	box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	box.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 10)
	b.add_child(box)
	box.add_child(pic)
	Ui.mark_selected(b, String(data.parts.get(_slot, "")) == id)
	Ui.wire(b, func() -> void: select_variant(id))
	return b


func _build_palette() -> void:
	for c: Node in _palette_row.get_children():
		c.queue_free()
	for c: Node in _zone_row.get_children():
		c.queue_free()
	if _slot == "template":
		_palette_row.visible = false
		_zone_row.visible = false
		return
	_palette_row.visible = true
	_zone_row.visible = true
	var zones: int = 1
	if _slot != "skin":
		zones = clampi(CharacterParts.zones(_slot, String(data.parts.get(_slot, ""))), 1, 3)
	if zones > 1:
		for z: int in zones:
			var b := Ui.button(str(z + 1), "", "ghost", Vector2(96, 72))
			Ui.mark_selected(b, z == _zone)
			Ui.wire(b, func() -> void:
				_zone = z
				_build_palette())
			_zone_row.add_child(b)
	_build_swatches_in(_palette_row, CharacterParts.palette_colors(CharacterParts.group_for(_slot)), 96.0)


func _build_swatches_in(row: HBoxContainer, colors: Array, size: float) -> void:
	for hex: Variant in colors:
		var b := Ui.tile(size)
		var fill: Color = Color(String(hex))
		b.add_theme_stylebox_override("normal", Ui.box(fill, Ui.RADIUS_SMALL,
			Color(0, 0, 0, 0), 0, 8))
		b.add_theme_stylebox_override("hover", Ui.box(fill.lightened(0.08), Ui.RADIUS_SMALL,
			Color(0, 0, 0, 0), 0, 12))
		b.add_theme_stylebox_override("pressed", Ui.box(fill.darkened(0.12), Ui.RADIUS_SMALL,
			Color(0, 0, 0, 0), 0, 2))
		var cur: String = _current_color()
		Ui.mark_selected(b, cur == String(hex))
		Ui.wire(b, func() -> void: select_color(String(hex)))
		row.add_child(b)


func _current_color() -> String:
	if _slot == "skin":
		return data.skin
	if _slot == "template":
		return ""
	var cols: Array = Array(data.colors.get(_slot, []))
	if _zone < cols.size():
		return String(cols[_zone])
	return ""


# ------------------------------------------------------------------ Aktionen (auch für Tests)
func select_category(cat: String) -> void:
	_slot = cat
	_zone = 0
	_refresh()


func select_template(tid: String) -> void:
	if not CharacterTemplates.ids().has(tid):
		return
	data.template_id = tid
	_refresh()


func select_variant(id: String) -> void:
	if _slot == "skin" or _slot == "template":
		return
	data.parts[_slot] = id
	var n: int = clampi(CharacterParts.zones(_slot, id), 1, 3)
	var group: String = CharacterParts.group_for(_slot)
	var pal: Array = CharacterParts.palette_colors(group)
	var cols: Array = []
	for i: int in n:
		cols.append(pal[(i * 3 + 1) % maxi(1, pal.size())])
	data.colors[_slot] = cols
	_zone = mini(_zone, n - 1)
	_refresh()


## Welche Farbzone (1…3) die Palette gerade einfärbt.
func select_zone(z: int) -> void:
	_zone = clampi(z, 0, 2)
	_refresh()


func select_color(hex: String) -> void:
	if _slot == "skin":
		data.skin = hex
	elif _slot != "template":
		data.set_color(_slot, _zone, hex)
	_refresh()


func roll_dice() -> void:
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	data.randomize_look(rng)
	_refresh()
	AudioBus.play_sfx("dice_roll")


func store_outfit(i: int) -> void:
	data.store_outfit(i)
	_last_outfit = i
	_refresh()


func wear_outfit(i: int) -> void:
	data.wear_outfit(i)
	_last_outfit = i
	_refresh()


func clear_outfit(i: int) -> void:
	data.clear_outfit(i)
	_refresh()


func is_done_enabled() -> bool:
	return not _done.disabled


# ------------------------------------------------------------------ Anzeige auffrischen
func _refresh() -> void:
	if _stage == null:
		return
	_stage.show_look(data.template_id, data.look(), true)
	_build_cats()
	_build_variants()
	_build_palette()
	_build_outfits()
	var ok: bool = data.is_complete()
	_done.disabled = not ok
	_hint.visible = not ok
	_hint.text = "Wähle eine Hautfarbe" if data.skin.is_empty() else "Wähle eine Größe"
	if _name_btn != null:
		_name_btn.text = " " + _title_text()
