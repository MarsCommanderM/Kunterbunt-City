extends Node
## P05-Beweis: App-Start → Pflicht-Editor → **Stadtkarte** → Bereich → zurück.
## Fotografiert jeden Schritt und misst: Ladezeit des Bereichs, gerettete Items, Rucksack,
## Album, Einstellungen. Zahlen statt Augenmaß.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p05_flow_runner.gd docs/tests/P05

var out_dir: String = "docs/tests/P05"
var _m: Dictionary = {}
var _host: Control


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else out_dir
	DirAccess.make_dir_recursive_absolute(out_dir)
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	SaveSystem.wipe()
	for f: String in SaveSystem.album_photos():
		SaveSystem.album_remove(f)
	Game.slot = 0
	Game.load_all()                       # Speicherstand wirklich neu lesen
	Game.characters.clear()
	Game.pets.clear()
	Game.active_id = &""
	Game.active_pets.clear()
	Game.backpack.clear()
	await _frames(3)
	_host = Control.new()
	_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	get_tree().root.add_child(_host)

	# 1 · Pflicht-Editor (ohne Figur geht nichts)
	Flow.start(_host)
	assert(not Flow.can_play())
	var ed: CharacterEditor = await _find(CharacterEditor, 8.0)
	assert(ed != null)
	ed.select_category("skin")
	ed.select_color(CharacterParts.palette_colors("skin")[2])
	ed.select_category("top")
	ed.select_variant("dress")
	ed.data.character_name = "Mia"
	var made: CharacterData = ed.data
	var pet: PetData = PetData.create("pet_cat")
	pet.pet_name = "Mauz"
	Game.add_pet(pet)
	ed.finished.emit(made)
	await _frames(4)

	# 2 · Stadtkarte
	var map: CityMap = await _find(CityMap, 6.0)
	_m["stadtkarte_da"] = map != null
	assert(map != null)
	_m["bereiche_knopf_anzahl"] = Areas.list().size()
	_m["bereiche_spielbar"] = _count_ready()
	await _frames(3)
	await _shot("p05_01_stadtkarte")
	map.mode = "grid"
	map._refresh()
	await _frames(3)
	await _shot("p05_02_stadtkarte_raster")
	map.mode = "map"
	map._refresh()
	await _frames(2)

	# 3 · Baustelle (Bereich ohne Inhalt) – sichtbar, kein Schloss
	var not_ready: StringName = _first_not_ready()
	_m["baustelle_sichtbar"] = String(not_ready) != "" and map._area_buttons.has(String(not_ready))

	# 4 · Bereich betreten
	var t0: int = Time.get_ticks_usec()
	map.entered.emit(&"home")
	await _frames(10)
	var area = _find_area_scene()
	_m["bereich_da"] = area != null
	assert(area != null)
	_m["ladezeit_ms"] = _round1(area.load_ms)          # von der Szene selbst gemessen
	_m["wechsel_gesamt_ms"] = _round1((Time.get_ticks_usec() - t0) / 1000.0)
	_m["eigene_figur_cm"] = _round1(_height(area.me))
	_m["haustiere_im_bereich"] = area.pets.size()
	_m["items_im_bereich"] = Placement.all_items(area.room).size()
	await _frames(4)
	await _shot("p05_03_bereich_gespielt")

	# 5 · Foto → Album
	area.hud.photo.emit()
	await _frames(4)
	_m["fotos_im_album"] = SaveSystem.album_photos().size()
	var alb: Album = Album.open(area.ui)
	await _frames(3)
	await _shot("p05_04_album")
	alb.queue_free()

	# 6 · Rucksack: ein Ding einpacken + wieder herausholen
	var ball: ItemNode = _item_by_id(area, &"toy_beachball")
	if ball != null:
		_m["rucksack_einpacken"] = Backpack.stash(ball)
	_m["rucksack_platz_belegt"] = Game.backpack.size()
	var pack: Backpack = Backpack.open(area.ui, func(_id: String, _i: int) -> bool:
		return area._place_back(_id))
	await _frames(3)
	await _shot("p05_05_rucksack")
	pack._take_out(0)
	await _frames(2)
	_m["rucksack_leer_nach_rausholen"] = Game.backpack.size() == 0
	_m["rucksack_zurueck_in_der_welt"] = _item_by_id(area, &"toy_beachball") != null
	pack.queue_free()

	# 7 · Einstellungen (hinter dem Eltern-Tor)
	var gate: ParentGate = ParentGate.ask(area.ui, func() -> void: pass)
	await _frames(3)
	await _shot("p05_06_elterntor")
	gate.passed.emit()
	await _frames(2)
	var set: SettingsPanel = SettingsPanel.open(area.ui)
	await _frames(3)
	await _shot("p05_07_einstellungen")
	set.queue_free()

	# 8 · Zurück zur Karte: Zustand muss gespeichert sein
	area.leave()
	await _frames(12)
	var map2: CityMap = await _find(CityMap, 8.0)
	_m["zurueck_zur_karte"] = map2 != null
	_m["raumzustand_items"] = Game.room_state(&"home", &"kitchen").size()
	Game.save_now()
	var again: Dictionary = SaveSystem.load_world(0)
	_m["gespeicherte_figuren"] = Array(again.get("characters", [])).size()
	_m["gespeicherte_tiere"] = Array(again.get("pets", [])).size()
	_m["gespeicherter_raumzustand"] = Array(Dictionary(again.get("areas", {})).get("home", {})
		.get("kitchen", [])).size()
	await _frames(3)
	await _shot("p05_08_zurueck_auf_der_karte")

	# 9 · Neustart: alles wieder da?
	Game.slot = 0
	Game.load_all()
	_m["nach_neustart_figuren"] = Game.characters.size()
	_m["nach_neustart_aktiv"] = Game.active_character().character_name if Game.active_character() else ""
	_finish()


# ------------------------------------------------------------------ Hilfen
func _count_ready() -> int:
	var n: int = 0
	for a: Variant in Areas.list():
		if Areas.is_ready(StringName(String((a as Dictionary)["id"]))):
			n += 1
	return n


func _first_not_ready() -> StringName:
	for a: Variant in Areas.list():
		var id := StringName(String((a as Dictionary)["id"]))
		if not Areas.is_ready(id):
			return id
	return &""


func _find_area_scene() -> Node:
	for c: Node in get_tree().root.get_children():
		if c is AreaScene:
			return c
	return null


func _item_by_id(area, id: StringName) -> ItemNode:
	for it: ItemNode in Placement.all_items(area.room):
		if it.def.id == id:
			return it
	return null


func _height(it: ItemNode) -> float:
	return 0.0 if it == null else it.global_rect().size.y / it.global_scale.y


func _round1(v: float) -> float:
	return round(v * 10.0) / 10.0


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
	var path: String = out_dir.path_join("p05_flow.json")
	FileAccess.open(path, FileAccess.WRITE).store_string(JSON.stringify(_m, "\t"))
	print("Messwerte: %s" % JSON.stringify(_m))
	get_tree().quit(0)
