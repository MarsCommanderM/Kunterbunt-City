class_name Flow
extends RefCounted
## Spielfluss (P04-T07, Ausbau in P05):
##   App-Start → kurzer Splash → „eigene Figur vorhanden?“ → **nein**: Editor (Pflicht, kein
##   Zurück) → **ja**: Galerie → „Spielen“ → Bereich.
## Ohne vollständige Figur (Schablone + Hautton) ist kein Bereich betretbar.

const SPLASH_S: float = 1.8
const SANDBOX: String = "res://src/debug/sandbox_characters.tscn"


static func start(host: Node) -> void:
	host.add_child(_splash())
	await host.get_tree().create_timer(SPLASH_S).timeout
	if not Game.has_complete_character():
		first_character(host)
	else:
		open_gallery(host)


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
		open_gallery(host))


static func open_gallery(host: Node) -> void:
	var g := Gallery.new()
	g.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	host.add_child(g)
	g.back.connect(func() -> void: g.queue_free())
	g.play.connect(func() -> void:
		g.queue_free()
		enter_area(host))
	g.characters_changed.connect(func() -> void: Game.save_characters())


## Darf gespielt werden? Ohne vollständige Figur (Schablone + Hautton) ist KEIN Bereich betretbar.
static func can_play() -> bool:
	return Game.has_complete_character()


## Bereich betreten (P05: SceneRouter + Stadtkarte). Vorher: Test-Welt.
static func enter_area(host: Node) -> void:
	if not can_play():
		first_character(host)          # Sicherheit: ohne Figur geht nichts
		return
	host.get_tree().change_scene_to_file(SANDBOX)
