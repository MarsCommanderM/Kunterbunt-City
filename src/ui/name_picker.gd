class_name NamePicker
extends Control
## Namens-Auswahl (P04-T06): 200 Namen als Bild-Kacheln + 🎲 Würfel.
## Freie Eingabe NUR hinter dem Eltern-Tor (Bleistift-Knopf) – danach lokaler Wortfilter.
## Ohne Lesen bedienbar: Antippen → der Name wird vorgelesen (Stimme der Figur) und übernommen.

signal picked(name: String)
signal cancelled

const FILE: String = "res://data/names.json"
const COLS: int = 6

static var _names: Array = []

var _grid: GridContainer
var _scroll: ScrollContainer
var _current: String = ""
var _voice: int = 1


static func open(host: Node, current: String, voice: int, cb: Callable) -> NamePicker:
	var n := NamePicker.new()
	n._current = current
	n._voice = voice
	n.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(n)
	n.picked.connect(cb)
	n.picked.connect(func(_x: String) -> void: n.queue_free())
	n.cancelled.connect(func() -> void: n.queue_free())
	return n


static func names() -> Array:
	if _names.is_empty():
		var d: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(FILE))
		for n: Variant in d.get("names", []):
			_names.append(String(n))
	return _names


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.16, 0.12, 0.22, 0.45)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	panel.size = Vector2(1560, 900)
	panel.position = Vector2(-780, -450)
	add_child(panel)
	var v := Ui.vbox(16)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 26)
	panel.add_child(v)

	var head := Ui.hbox()
	head.alignment = BoxContainer.ALIGNMENT_CENTER
	head.add_child(Ui.label("Wie heißt deine Figur?", Ui.FONT_TITLE))
	var dice := Ui.button("Würfeln", "dice", "accent", Vector2(280, 96))
	dice.name = "DiceButton"
	Ui.wire(dice, func() -> void: _roll(), "dice_roll")
	head.add_child(dice)
	var pencil := Ui.button("selbst schreiben", "pencil", "lilac", Vector2(360, 96))
	pencil.name = "PencilButton"
	Ui.wire(pencil, func() -> void:
		ParentGate.ask(self, func() -> void: _free_text()))
	head.add_child(pencil)
	var x := Ui.button("", "close", "ghost", Vector2(96, 96))
	x.name = "CloseButton"
	Ui.wire(x, func() -> void: cancelled.emit(), "ui_back")
	head.add_child(x)
	v.add_child(head)

	_scroll = ScrollContainer.new()
	_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	v.add_child(_scroll)
	_grid = Ui.grid(COLS, 14)
	_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_scroll.add_child(_grid)
	_fill()


func _fill() -> void:
	for c: Node in _grid.get_children():
		c.queue_free()
	for n: Variant in names():
		var b := Ui.tile(228.0)
		b.text = String(n)
		b.add_theme_font_size_override("font_size", 30)
		b.custom_minimum_size = Vector2(228, 92)
		Ui.mark_selected(b, String(n) == _current)
		Ui.wire(b, func() -> void: _pick(String(n)))
		_grid.add_child(b)
	await get_tree().process_frame
	if _current.is_empty():
		return
	var i: int = names().find(_current)
	if i >= 0 and i < _grid.get_child_count():
		var c: Control = _grid.get_child(i)
		_scroll.ensure_control_visible(c)


func _roll() -> void:
	var list: Array = names()
	_current = String(list[randi() % list.size()])
	AudioBus.play_sfx("ui_confirm")
	_fill()


func _pick(n: String) -> void:
	_current = n
	picked.emit(n)


func _free_text() -> void:
	var host := Control.new()
	host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(host)
	var dim := ColorRect.new()
	dim.color = Color(0.16, 0.12, 0.22, 0.55)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(dim)
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	panel.size = Vector2(900, 460)
	panel.position = Vector2(-450, -230)
	host.add_child(panel)
	var v := Ui.vbox(18)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 26)
	panel.add_child(v)
	v.add_child(Ui.label("Name eingeben", Ui.FONT_TITLE))
	var edit := LineEdit.new()
	edit.placeholder_text = "Name"
	edit.custom_minimum_size = Vector2(700, 110)
	edit.add_theme_font_size_override("font_size", 44)
	edit.text = _current
	v.add_child(edit)
	var hint := Ui.label("", Ui.FONT_SMALL, Ui.PINK)
	v.add_child(hint)
	var row := Ui.hbox()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	var ok := Ui.button("Fertig", "check", "teal", Vector2(280, 110))
	Ui.wire(ok, func() -> void:
		var why: String = NameFilter.check(edit.text)
		if not why.is_empty():
			hint.text = "Bitte anderen Namen: " + why
			AudioBus.play_sfx("deny")
			return
		_current = NameFilter.pretty(edit.text)
		host.queue_free()
		picked.emit(_current))
	var back := Ui.button("zurück", "back", "ghost", Vector2(240, 110))
	Ui.wire(back, func() -> void: host.queue_free(), "ui_back")
	row.add_child(ok)
	row.add_child(back)
	v.add_child(row)
	edit.grab_focus()
