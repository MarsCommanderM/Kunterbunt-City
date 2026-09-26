extends Node
## P04-End-to-End-Beweis: App-Start → Pflicht-Editor → Galerie → „Spielen" → Bereich.
## Danach steht die SELBSTGEBAUTE Figur (Aussehen aus dem Editor, Größe aus der Schablone)
## mit dem eigenen Haustier in der Welt. Alles gemessen, nichts geschätzt.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p04_flow_runner.gd docs/tests/P04

var out_dir: String = "docs/tests/P04"
var _m: Dictionary = {}


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else out_dir
	DirAccess.make_dir_recursive_absolute(out_dir)
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	SaveSystem.wipe()
	Game.characters.clear()
	Game.pets.clear()
	Game.active_id = &""
	Game.active_pets.clear()
	await _frames(3)
	var host := Control.new()
	host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	get_tree().root.add_child(host)

	# 1 · Spielfluss startet: ohne Figur MUSS der Editor kommen.
	Flow.start(host)
	assert(not Flow.can_play())
	var ed: CharacterEditor = await _find(CharacterEditor, 8.0) as CharacterEditor
	_m["pflicht_editor_ohne_figur"] = ed != null
	if ed == null:
		_finish()
		return
	# 2 · Figur bauen (Hautton ist Pflicht, Name kommt aus der Namenswahl).
	ed.select_category("skin")
	ed.select_color(CharacterParts.palette_colors("skin")[2])
	ed.select_category("top")
	ed.select_variant("dress")
	ed.select_color(CharacterParts.palette_colors("cloth")[1])
	ed.data.character_name = "Mia"
	_m["fertig_erst_nach_hautton"] = ed.is_done_enabled()
	var made: CharacterData = ed.data
	_m["schablone"] = made.template_id
	# 3 · Haustier dazu (Editor) und ab in die Galerie.
	var pet: PetData = PetData.create("pet_cat")
	pet.pet_name = "Mauz"
	pet.pet_trait = "curious"
	Game.add_pet(pet)
	_m["haustier"] = pet.species_id
	ed.finished.emit(made)
	await _frames(3)
	var gal: Gallery = await _find(Gallery, 4.0) as Gallery
	_m["galerie_nach_fertig"] = gal != null
	_m["spielen_frei"] = Flow.can_play()
	if gal != null:
		await _shot("p04_14_galerie_mit_eigener_figur")
	# 4 · „Spielen" → Bereich. Die eigene Figur + das eigene Tier müssen drin stehen.
	Flow.enter_area(host)
	await _frames(8)
	var sb = get_tree().root.get_node_or_null("SandboxCharacters")
	if sb == null:
		for c: Node in get_tree().root.get_children():
			if c.get_class() == "Node2D" and c.has_method("_unhandled_input"):
				sb = c
	_m["bereich_betreten"] = sb != null
	if sb == null:
		_finish()
		return
	_measures(sb)
	await _frames(3)
	await _shot("p04_15_eigene_figur_im_spiel")
	_finish()


func _measures(sb) -> void:
	var me: ItemNode = sb.spawned.get(&"me")
	_m["eigene_figur_da"] = me != null
	if me != null:
		var h: float = me.global_rect().size.y / me.global_scale.y
		_m["eigene_figur_cm"] = round(h * 10.0) / 10.0
		_m["sichtbar"] = sb.camera.get_viewport_rect().has_point(
			sb.camera.get_screen_center_position() * 0.0 + _screen_of(sb, me))
	var pet: PetNode = null
	for k: Variant in sb.spawned:
		var it: ItemNode = sb.spawned[k]
		if it is PetNode:
			pet = it
	if pet != null:
		_m["haustier_da"] = true
		_m["haustier_cm"] = round(pet.global_rect().size.y / pet.global_scale.y * 10.0) / 10.0
		_m["haustier_art"] = String(pet.def.id)
	var table: ItemNode = sb.spawned.get(&"home_table_wood")
	if table != null and pet != null:
		_m["haustier_kleiner_als_tisch"] = pet.global_rect().size.y < table.global_rect().size.y


func _screen_of(sb, it: ItemNode) -> Vector2:
	return sb.camera.get_screen_center_position() + (it.global_position - sb.camera.global_position) * sb.camera.zoom


func _find(kind: Variant, timeout_s: float) -> Node:
	var t: float = 0.0
	while t < timeout_s:
		var n: Node = _search(get_tree().root, kind)
		if n != null:
			return n
		await get_tree().create_timer(0.2).timeout
		t += 0.2
	return null


func _search(n: Node, kind: Variant) -> Node:
	for c: Node in n.get_children():
		if is_instance_of(c, kind):
			return c
		var deep: Node = _search(c, kind)
		if deep != null:
			return deep
	return null


func _frames(n: int) -> void:
	for i: int in n:
		await get_tree().process_frame
	await RenderingServer.frame_post_draw


func _shot(name: String) -> void:
	await _frames(3)
	var img: Image = get_tree().root.get_texture().get_image()
	if img != null:
		img.save_jpg(out_dir.path_join(name + ".jpg"), 0.9)
		print("Screenshot: %s" % name)


func _finish() -> void:
	_m["gespeicherte_figuren"] = Game.characters.size()
	_m["gespeicherte_tiere"] = Game.pets.size()
	var path: String = out_dir.path_join("p04_flow.json")
	FileAccess.open(path, FileAccess.WRITE).store_string(JSON.stringify(_m, "\t"))
	print("Messwerte: %s" % JSON.stringify(_m))
	get_tree().quit(0)
