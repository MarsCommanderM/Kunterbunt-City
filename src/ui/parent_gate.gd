class_name ParentGate
extends Control
## Eltern-Tor (P04-T06, P05-T09): zwei Wege, die ein Kind nicht aus Versehen schafft –
##   1. Rechenaufgabe mit Zahlen-Kacheln (kein Lesen nötig, nur Ziffern)
##   2. Drei Punkte drei Sekunden halten (auch für Kinder, die noch nicht rechnen)
## Beides lokal, kein Netz, kein Login.

signal passed
signal cancelled

const HOLD_S: float = 3.0
const DIGITS: int = 9

var _mode: int = 0                    # 0 = rechnen, 1 = halten
var _a: int = 3
var _b: int = 4
var _hold: float = 0.0
var _holding: bool = false
var _panel: Panel
var _body: VBoxContainer
var _ring: Control
var _title: Label


static func ask(host: Node, cb: Callable) -> ParentGate:
	var g := ParentGate.new()
	g.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(g)
	g.passed.connect(cb)
	g.passed.connect(func() -> void: g._close())
	g.cancelled.connect(func() -> void: g._close())
	return g


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.16, 0.12, 0.22, 0.45)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	_panel = Ui.card(Ui.RADIUS, Ui.CARD)
	_panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	_panel.size = Vector2(880, 620)
	_panel.position = Vector2(-440, -310)
	add_child(_panel)
	var v := Ui.vbox(16)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 28)
	_panel.add_child(v)
	var head := Ui.hbox()
	head.alignment = BoxContainer.ALIGNMENT_CENTER
	_title = Ui.label("Eltern-Tor", Ui.FONT_TITLE)
	head.add_child(_title)
	v.add_child(head)
	_body = Ui.vbox(18)
	_body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(_body)
	var foot := Ui.hbox()
	foot.alignment = BoxContainer.ALIGNMENT_CENTER
	var mode_btn := Ui.button("andere Art", "dice", "ghost", Vector2(300, 84))
	Ui.wire(mode_btn, func() -> void:
		_mode = 1 - _mode
		_build())
	var back_btn := Ui.button("zurück", "back", "ghost", Vector2(260, 84))
	Ui.wire(back_btn, func() -> void: cancelled.emit(), "ui_back")
	foot.add_child(mode_btn)
	foot.add_child(back_btn)
	v.add_child(foot)
	_build()


func _close() -> void:
	queue_free()


func _build() -> void:
	for c: Node in _body.get_children():
		c.queue_free()
	_hold = 0.0
	_holding = false
	if _mode == 0:
		_title.text = "Eltern-Tor · rechnen"
		_new_task()
		var q := Ui.label("%d  +  %d  =  ?" % [_a, _b], 76)
		_body.add_child(q)
		var opts: Array = _options()
		var g := Ui.grid(4, 20)
		for o: int in opts:
			var b := Ui.button(str(o), "", "teal", Vector2(170, 130))
			b.add_theme_font_size_override("font_size", 52)
			Ui.wire(b, func() -> void: _answer(o))
			g.add_child(b)
		_body.add_child(g)
	else:
		_title.text = "Eltern-Tor · halten"
		_body.add_child(Ui.label("Drei Punkte drei Sekunden halten", Ui.FONT_LABEL, Ui.INK_SOFT))
		_ring = Control.new()
		_ring.custom_minimum_size = Vector2(320, 320)
		_ring.mouse_filter = Control.MOUSE_FILTER_STOP
		_ring.draw.connect(_draw_ring)
		_ring.gui_input.connect(_ring_input)
		_body.add_child(_ring)


func _new_task() -> void:
	_a = 2 + randi() % 8
	_b = 2 + randi() % 8


func _options() -> Array:
	var right: int = _a + _b
	var opts: Array = [right]
	while opts.size() < 4:
		var v: int = clampi(right + (randi() % 7) - 3, 2, DIGITS + DIGITS)
		if not opts.has(v):
			opts.append(v)
	opts.shuffle()
	return opts


func _answer(v: int) -> void:
	if v == _a + _b:
		AudioBus.play_sfx("ui_confirm")
		passed.emit()
	else:
		AudioBus.play_sfx("deny")
		_new_task()
		_build()


# ------------------------------------------------------------------ Halte-Kreis
func _ring_input(e: InputEvent) -> void:
	var pressed: bool = false
	if e is InputEventMouseButton:
		var mb: InputEventMouseButton = e
		if mb.button_index != MOUSE_BUTTON_LEFT:
			return
		pressed = mb.pressed
	elif e is InputEventScreenTouch:
		pressed = (e as InputEventScreenTouch).pressed
	else:
		return
	_holding = pressed
	if not pressed and _hold < HOLD_S:
		_hold = 0.0
		_ring.queue_redraw()


func _process(delta: float) -> void:
	if _holding and _mode == 1 and _ring != null:
		_hold += delta
		_ring.queue_redraw()
		if _hold >= HOLD_S:
			_holding = false
			AudioBus.play_sfx("ui_confirm")
			passed.emit()


func _draw_ring() -> void:
	var c: Vector2 = _ring.size * 0.5
	var r: float = _ring.size.x * 0.42
	_ring.draw_circle(c, r, Ui.TEAL.lightened(0.25))
	var prog: float = clampf(_hold / HOLD_S, 0.0, 1.0)
	if prog > 0.0:
		_ring.draw_arc(c, r * 0.74, -PI * 0.5, -PI * 0.5 + TAU * prog, 72, Ui.ACCENT, 40, true)
	_ring.draw_circle(c, r * 0.55, Ui.CARD)
	for i: int in 3:
		var a: float = -PI * 0.5 + TAU * float(i) / 3.0
		_ring.draw_circle(c + Vector2(cos(a), sin(a)) * r * 0.30, 22, Ui.INK)
