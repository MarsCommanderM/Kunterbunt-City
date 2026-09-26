extends Node
## P04-Beweisbilder: Editor, Namenswahl, Eltern-Tor, Galerie, Haustier-Editor.
## Fährt die echte UI (keine Attrappe) und fotografiert jeden Schritt.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p04_ui_runner.gd docs/tests/P04

var out_dir: String = "docs/tests/P04"
var _n: int = 0


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else out_dir
	DirAccess.make_dir_recursive_absolute(out_dir)
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	SaveSystem.wipe()
	Game.characters.clear()
	Game.pets.clear()
	Game.active_id = &""
	await _frames(3)
	# Der Spielfluss (src/ui/flow.gd): Splash → Pflicht-Editor → Galerie.
	# Achtung: bei -s lädt Gott nicht die Hauptszene – der Ablauf wird hier selbst gestartet.
	var host := Control.new()
	host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	get_tree().root.add_child(host)
	Flow.start(host)
	var ed: CharacterEditor = await _wait_editor(8.0)
	if ed == null:
		push_error("Kein Editor im Baum – Pflicht-Ablauf kaputt")
		get_tree().quit(1)
		return
	await _frames(4)
	await _shot("p04_04_editor_pflicht")          # 1: Editor, ✓ noch aus (kein Hautton)
	ed.select_category("skin")
	ed.select_color(CharacterParts.palette_colors("skin")[2])
	await _frames(3)
	await _shot("p04_05_hautton_gewaehlt")        # 2: ✓ ist jetzt frei
	ed.select_category("top")
	ed.select_variant("dress")
	ed.select_color(CharacterParts.palette_colors("cloth")[1])
	await _frames(3)
	await _shot("p04_06_kleid_farbe")             # 3: Teil + Farbe getauscht
	ed.select_category("hair")
	ed.select_variant("pigtails")
	ed.roll_dice()
	await _frames(3)
	await _shot("p04_07_wuerfel")                 # 4: 🎲 Zufallsfigur
	ed.store_outfit(0)
	ed.wear_outfit(0)
	ed.data.character_name = "Mia"
	await _namen(ed)
	await _tor(ed)
	var made: CharacterData = ed.data
	made.character_name = "Mia"
	ed.finished.emit(made)
	await _frames(3)
	var gal: Gallery = _find(Gallery) as Gallery
	if gal != null:
		gal.can_back = true
	if gal == null:
		push_error("Keine Galerie nach ✓")
		get_tree().quit(1)
		return
	Game.set_active(made.id)
	#noch zwei Figuren für die Galerie
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	for i: int in 2:
		var d: CharacterData = CharacterData.create("kid")
		d.character_name = ["Ben", "Lina"][i]
		d.skin = String(CharacterParts.palette_colors("skin")[i + 3])
		d.randomize_look(rng)
		d.folder = "Freunde"
		Game.add_character(d)
	for p: Variant in ["pet_dog_medium", "pet_cat", "pet_bird", "pet_rabbit"]:
		Game.add_pet(PetData.create(String(p)))
	await gal._refresh()
	await _frames(4)
	await _shot("p04_08_galerie_figuren")         # 5: Galerie mit 3 Figuren
	gal.mode = "pets"
	await gal._refresh()
	await _frames(3)
	await _shot("p04_09_galerie_tiere")           # 6: Galerie · Tiere
	var pe: PetEditor = PetEditor.open(get_tree().root, PetData.create("pet_dog_medium"),
		func(_p: PetData) -> void: pass)
	await _frames(4)
	await _shot("p04_10_haustier_editor")         # 7: Haustier-Editor
	pe.set_trait("sleepy")
	pe.set_pattern("stripes")
	pe._cat = "fur"
	pe.select_color(CharacterParts.palette_colors("fur")[4])
	await _frames(3)
	await _shot("p04_11_haustier_fell")           # 8: Fell umgefärbt
	pe.finished.emit(pe.pet)
	await _frames(2)
	get_tree().quit(0)


# ------------------------------------------------------------------ Hilfen
func _wait_editor(timeout_s: float) -> CharacterEditor:
	var t: float = 0.0
	while t < timeout_s:
		var e: CharacterEditor = _find(CharacterEditor) as CharacterEditor
		if e != null:
			return e
		await get_tree().create_timer(0.2).timeout
		t += 0.2
	return null


func _find(kind: Variant) -> Node:
	return _search(get_tree().root, kind)


func _search(n: Node, kind: Variant) -> Node:
	for c: Node in n.get_children():
		if is_instance_of(c, kind):
			return c
		var deep: Node = _search(c, kind)
		if deep != null:
			return deep
	return null


func _namen(host: Node) -> void:
	var np: NamePicker = NamePicker.open(host, "", 1, func(_n: String) -> void: pass)
	await _frames(4)
	await _shot("p04_12_namenswahl")
	np.picked.emit("Mia")


func _tor(host: Node) -> void:
	var gate: ParentGate = ParentGate.ask(host, func() -> void: pass)
	await _frames(4)
	await _shot("p04_13_elterntor")
	gate.passed.emit()


func _frames(n: int) -> void:
	for i: int in n:
		await get_tree().process_frame
	await RenderingServer.frame_post_draw


func _shot(name: String) -> void:
	_n += 1
	await _frames(3)
	var img: Image = get_tree().root.get_texture().get_image()
	if img == null:
		return
	img.save_jpg(out_dir.path_join(name + ".jpg"), 0.88)
	print("Screenshot: %s" % name)
