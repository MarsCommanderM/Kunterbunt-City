class_name SettingsPanel
extends Control
## Einstellungen (P05-T10) – nur HINTER dem Eltern-Tor: Lautstärken, große Schrift,
## wenig Animation, Sprache, Bereich zurücksetzen (🪄) und Speicherstand exportieren/importieren
## (Datei, kein Internet).

signal closed

var _status: Label


static func open(host: Node) -> SettingsPanel:
	var s := SettingsPanel.new()
	s.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(s)
	return s


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.16, 0.12, 0.22, 0.5)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	panel.size = Vector2(1180, 940)
	panel.position = Vector2(-590, -470)
	add_child(panel)
	var v := Ui.vbox(16)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 26)
	panel.add_child(v)
	var head := Ui.hbox(14)
	head.alignment = BoxContainer.ALIGNMENT_CENTER
	head.add_child(Ui.label("Einstellungen", Ui.FONT_TITLE))
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(sp)
	var x := Ui.button("", "close", "ghost", Vector2(96, 96))
	Ui.wire(x, func() -> void:
		closed.emit()
		queue_free(), "ui_back")
	head.add_child(x)
	v.add_child(head)

	for key: String in ["volume_music", "volume_sfx", "volume_animals"]:
		v.add_child(_slider(key))
	for key: String in ["large_ui", "reduced_motion", "shops_always_open"]:
		v.add_child(_toggle(key))
	v.add_child(_row("Sprache", [["de", "Deutsch"], ["en", "English"]], "language",
		func(val: String) -> void: Settings.language = val))

	var reset_row := Ui.hbox(14)
	reset_row.alignment = BoxContainer.ALIGNMENT_CENTER
	var reset := Ui.button("Bereich zurücksetzen", "brush", "pink", Vector2(520, 104))
	Ui.wire(reset, func() -> void:
		ParentGate.ask(self, func() -> void:
			Game.reset_areas()
			_status.text = "Alle Bereiche sind wieder wie am Anfang."
			AudioBus.play_sfx("ui_confirm")))
	reset_row.add_child(reset)
	var wipe := Ui.button("Alles löschen", "trash", "pink", Vector2(420, 104))
	Ui.wire(wipe, func() -> void:
		ParentGate.ask(self, func() -> void:
			Game.wipe()
			_status.text = "Alles gelöscht. Beim nächsten Start baust du eine neue Figur."
			AudioBus.play_sfx("deny")))
	reset_row.add_child(wipe)
	v.add_child(reset_row)

	var io := Ui.hbox(14)
	io.alignment = BoxContainer.ALIGNMENT_CENTER
	var exp_btn := Ui.button("Speichern als Datei", "folder", "teal", Vector2(470, 104))
	Ui.wire(exp_btn, func() -> void:
		var p: String = SaveSystem.export_world(Game.slot)
		_status.text = "Gespeichert: " + (p if not p.is_empty() else "hat nicht geklappt"))
	io.add_child(exp_btn)
	var imp_btn := Ui.button("Datei laden", "folder", "teal", Vector2(420, 104))
	Ui.wire(imp_btn, func() -> void:
		var p: String = "user://export/kunterbunt-city-welt-%d.json" % Game.slot
		_status.text = "Geladen ✅" if SaveSystem.import_world(p, Game.slot) else "Keine Datei gefunden")
	io.add_child(imp_btn)
	v.add_child(io)

	var slots := Ui.hbox(12)
	slots.alignment = BoxContainer.ALIGNMENT_CENTER
	slots.add_child(Ui.label("Welt:", Ui.FONT_LABEL, Ui.INK_SOFT))
	for i: int in SaveSystem.SLOTS:
		var b := Ui.button(str(i + 1), "star", "ghost" if i != Game.slot else "accent",
			Vector2(120, 88))
		Ui.wire(b, func() -> void:
			Game.switch_slot(i)
			_status.text = "Welt %d geladen." % (i + 1))
		slots.add_child(b)
	v.add_child(slots)

	_status = Ui.label("", Ui.FONT_SMALL, Ui.INK_SOFT)
	v.add_child(_status)


func _labels() -> Dictionary:
	return {
		"volume_music": "Musik", "volume_sfx": "Effekte", "volume_animals": "Tiere",
		"large_ui": "große Schrift & Knöpfe", "reduced_motion": "wenig Animation",
		"shops_always_open": "Läden immer offen",
	}


func _slider(key: String) -> Control:
	var row := Ui.hbox(16)
	row.add_child(Ui.label(_labels()[key], Ui.FONT_LABEL, Ui.INK, HORIZONTAL_ALIGNMENT_LEFT))
	var sl := HSlider.new()
	sl.min_value = 0.0
	sl.max_value = 1.0
	sl.step = 0.05
	sl.custom_minimum_size = Vector2(520, 70)
	sl.value = float(Settings.get_value(key))
	sl.value_changed.connect(func(v: float) -> void:
		Settings.set_value(key, v)
		AudioBus.play_sfx("ui_tap"))          # kurz anhören, wie laut es ist
	row.add_child(sl)
	return row


func _toggle(key: String) -> Control:
	var row := Ui.hbox(16)
	row.add_child(Ui.label(_labels()[key], Ui.FONT_LABEL, Ui.INK, HORIZONTAL_ALIGNMENT_LEFT))
	var b := Ui.button("", "check", "teal" if bool(Settings.get_value(key)) else "ghost",
		Vector2(120, 88))
	Ui.wire(b, func() -> void:
		Settings.set_value(key, not bool(Settings.get_value(key)))
		_refresh_toggle(b, key))
	row.add_child(b)
	return row


func _refresh_toggle(b: Button, key: String) -> void:
	Ui.style_button(b, Ui.TEAL if bool(Settings.get_value(key)) else Color(1, 1, 1, 0.0),
		not bool(Settings.get_value(key)))


func _row(title: String, options: Array, key: String, cb: Callable) -> Control:
	var row := Ui.hbox(14)
	row.add_child(Ui.label(title, Ui.FONT_LABEL, Ui.INK, HORIZONTAL_ALIGNMENT_LEFT))
	for o: Array in options:
		var b := Ui.button(String(o[1]), "", "accent" if String(Settings.get_value(key)) == String(o[0]) else "ghost",
			Vector2(260, 88))
		Ui.wire(b, func() -> void: cb.call(String(o[0])))
		row.add_child(b)
	return row
