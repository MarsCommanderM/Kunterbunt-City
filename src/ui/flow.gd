class_name Flow
extends RefCounted
## Spielfluss (P04-T07, Ausbau in P05):
##   App-Start → kurzer Splash → „eigene Figur vorhanden?“ → **nein**: Editor (Pflicht, kein
##   Zurück) → **ja**: Galerie → „Spielen“ → Bereich.
## Ohne vollständige Figur (Schablone + Hautton) ist kein Bereich betretbar.

const SPLASH_S: float = 1.8


static func start(host: Node) -> void:
	host.add_child(_splash())
	await host.get_tree().create_timer(SPLASH_S).timeout
	if not can_play():
		first_character(host)
	else:
		open_map(host)


static func _splash() -> Control:
	var c := Control.new()
	c.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	c.mouse_filter = Control.MOUSE_FILTER_STOP
	Ui.background(c)
	var v := Ui.vbox(20)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	c.add_child(v)
	var s := Ui.icon("sun", 220.0, Ui.ACCENT)
	v.add_child(s)
	v.add_child(Ui.label("Kunterbunt City", 82))
	v.add_child(Ui.label("Tippen zum Überspringen", Ui.FONT_SMALL, Ui.INK_SOFT))
	c.gui_input.connect(func(e: InputEvent) -> void:
		if (e is InputEventScreenTouch and (e as InputEventScreenTouch).pressed) \
				or (e is InputEventMouseButton and (e as InputEventMouseButton).pressed):
			c.queue_free())
	c.set_meta("skip", true)
	return c


## Pflicht-Ablauf: neue Figur, kein Zurück, ✓ erst mit Hautton.
static func first_character(host: Node) -> void:
	var d: CharacterData = CharacterData.create("kid")
	d.folder = "Familie"
	CharacterEditor.open(host, d, true, func(c: CharacterData) -> void:
		Game.add_character(c)
		Game.set_active(c.id)
		open_map(host))


## Die Stadtkarte (Startmenü): ein Knopf pro Bereich + Figur, Rucksack, Album, Eltern.
static func open_map(host: Node) -> Control:
	var m := CityMap.new()
	m.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(m)
	m.entered.connect(func(id: StringName) -> void:
		SceneRouter.goto_area(id))
	m.open_characters.connect(func() -> void:
		var g := Gallery.new()
		g.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		m.add_child(g)
		g.show_play = false
		g.back.connect(func() -> void:
			g.queue_free()
			m._refresh()))
	m.open_backpack.connect(func() -> void:
		Backpack.open(m))
	m.open_album.connect(func() -> void:
		Album.open(m))
	m.open_parents.connect(func() -> void:
		ParentGate.ask(m, func() -> void: SettingsPanel.open(m)))
	return m


## Figuren-Galerie (von überall erreichbar).
static func open_gallery(host: Node, with_play: bool = true) -> Gallery:
	var g := Gallery.new()
	g.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	g.show_play = with_play
	host.add_child(g)
	g.back.connect(func() -> void: g.queue_free())
	g.play.connect(func() -> void:
		g.queue_free()
		open_map(host))
	g.characters_changed.connect(func() -> void: Game.save_characters())
	return g


## Darf gespielt werden? Ohne vollständige Figur (Schablone + Hautton) ist KEIN Bereich betretbar.
static func can_play() -> bool:
	return Game.has_complete_character()
