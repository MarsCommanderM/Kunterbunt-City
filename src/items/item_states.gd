class_name ItemStates
extends RefCounted
## P04b-T10: Zustände von Items – Schrank/Schublade auf/zu, Geräte an/aus, Lampe an …
## Antippen schaltet weiter; jeder Zustand hat ein eigenes Sprite (deckungsgleich), einen Ton und optional eine
## Animation (shake/pulse/bounce). Behälter mit „open_top“ (Topf, Toaster) zeigen ihren Inhalt immer.
## Nach jedem Wechsel prüft das Rezept-System, ob etwas gekocht wird.



static func init(it: ItemNode) -> void:
	if it.def.has_states():
		it.state = String(it.def.states[0])
	if it.def.is_container() and it.def.open_top():
		it.is_open = true
		it.contents_root.visible = true


## Zustand setzen (silent: ohne Ton, z. B. beim Laden eines Speicherstands).
static func set_state(it: ItemNode, s: String, silent: bool = false) -> void:
	if not it.def.states.has(s) or s == it.state:
		return
	it.state = s
	var path: String = String(it.def.state_sprites.get(s, it.def.sprite_path))
	it.sprite.texture = load(path)
	it.apply_world_size()
	if it.def.is_container() and not it.def.open_top():
		var open: bool = s == "open"
		if open != it.is_open:
			it.is_open = open
			it.contents_root.visible = open
			it.opened_changed.emit(it, open)
	if not silent:
		if s in ["open", "closed"]:
			AudioBus.play_item_sfx(it.def, "open" if s == "open" else "close")
		else:
			AudioBus.play_sfx(String(it.def.sfx.get(s, "ui_tap")))
	_animate(it)
	Recipes.check(it)


static func next_state(it: ItemNode) -> void:
	if Garden.handles_tap(it):                             # P07-T07: Beete wachsen, statt beim Tippen umzuschalten
		Garden.on_tap(it)
		return
	var i: int = it.def.states.find(it.state)
	set_state(it, String(it.def.states[(i + 1) % it.def.states.size()]))


## Gilt als „heiß/an“: selbst an – oder steht in/auf einem Gerät, das an ist (Pfanne auf dem Herd).
static func is_on(it: ItemNode) -> bool:
	var n: Node = it
	while n != null:
		if n is ItemNode and (n as ItemNode).state == "on":
			return true
		n = n.get_parent()
	return false


static func _animate(it: ItemNode) -> void:
	if it.state_tween != null:
		it.state_tween.kill()
		it.state_tween = null
		it.sprite.rotation = 0.0
	var kind: String = String(it.def.anim.get(it.state, ""))
	if kind.is_empty() or not it.is_inside_tree():
		return
	var tw: Tween = it.create_tween().set_loops()
	match kind:
		"shake":
			tw.tween_property(it.sprite, "rotation", 0.035, 0.06)
			tw.tween_property(it.sprite, "rotation", -0.035, 0.12)
			tw.tween_property(it.sprite, "rotation", 0.0, 0.06)
		"bounce":
			tw.tween_property(it.sprite, "position:y", -2.0, 0.18).set_trans(Tween.TRANS_SINE)
			tw.tween_property(it.sprite, "position:y", 0.0, 0.18).set_trans(Tween.TRANS_SINE)
		_:   # pulse
			tw.tween_property(it.sprite, "modulate", Color(1.08, 1.04, 0.96), 0.5).set_trans(Tween.TRANS_SINE)
			tw.tween_property(it.sprite, "modulate", Color.WHITE, 0.5).set_trans(Tween.TRANS_SINE)
	it.state_tween = tw
