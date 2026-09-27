extends Node
## P07-Beweis: Zuhause mit 11 Räumen – leerer Raum, Raum-Wahl, Deko-Leiste, selbst eingerichtetes Kinderzimmer
## (Fenster, Vorhang, Teppich, Bett, Regal, Spielzeug) und der Garten. Bedient die Spiel-API wie ein Finger.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p07_rooms_runner.gd docs/tests/P07

var out_dir: String = "docs/tests/P07"
var _m: Dictionary = {}
var _now: float = 5000000.0          ## Garten-Uhr (Feld, nicht lokal: Lambdas kopieren lokale Variablen)


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else out_dir
	DirAccess.make_dir_recursive_absolute(out_dir)
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	Game.characters.clear()
	Game.pets.clear()
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#f7c9a2"
	c.character_name = "Mia"
	Game.add_character(c)
	Game.set_active(c.id)
	Game.add_pet(PetData.create("pet_cat"))
	SceneRouter.pending_area = &"home"
	var a: AreaScene = load("res://src/world/area_scene.tscn").instantiate()
	get_tree().root.add_child(a)
	await _frames(8)
	_m["start_raum"] = String(a.room.room_id)
	_m["raeume"] = a.room_ids().size()
	await _shot("p07_01_wohnzimmer_leer")

	# Raum-Wahl
	var picker: RoomPicker = RoomPicker.open(a.ui, a)
	await _shot("p07_02_raumwahl")
	picker.queue_free()

	# Kinderzimmer einrichten: Tapete mit Sternen, Teppichboden, dann Dinge aus dem Katalog
	a.switch_room("kids1")
	await _frames(4)
	a.set_decor({"wall": ["#a9c3dd", "#ffffff", "#fbfaf7"], "pattern": "stars", "pattern_col": "#f6d98a",
		"floor": "carpet", "floor_cols": ["#f0b6c2", "#e8a4b3", "#c1547a"]})
	var cam_x: float = a.camera.get_screen_center_position().x
	var put: Array = [
		["win_double_m_white", cam_x - 160, -210], ["curtain_long_stars_navy", cam_x - 160, -238],
		["win_round_m_white", cam_x + 240, -200], ["poster_rocket_navy", cam_x + 60, -190],
		["rug_round_rose", cam_x - 20, 40], ["furn_bed_canopy_rose", cam_x - 230, 20], ["furn_bookshelf_oak", cam_x + 330, 5],
		["toy_plush_unicorn_white", cam_x + 20, 50], ["toy_tipi_cream", cam_x + 170, 20], ["deco_lamp_floor_butter", cam_x - 20, 8],
		["toy_ball_pit_sky", cam_x + 120, 60], ["baby_stacker_cream", cam_x - 80, 60]]
	var n: int = 0
	for p: Array in put:
		var id := StringName(String(p[0]))
		var def: ItemDefinition = ItemDB.get_item(id)
		if def == null:
			print("fehlt: ", id)
			continue
		var it: ItemNode = ItemSpawner.on_wall(a.room, id, float(p[1]), float(p[2])) if def.is_wall() else \
			ItemSpawner.on_floor(a.room, id, float(p[1]), float(p[2]))
		if it != null:
			n += 1
	_m["kinderzimmer_items"] = n
	a._on_world_changed()
	await _frames(4)
	await _shot("p07_03_kinderzimmer_eingerichtet")
	var deco: DecorPanel = DecorPanel.open(a.ui, a)
	await _shot("p07_04_deko_leiste")
	deco.queue_free()

	# Garten: Start-Anlage (Nutzgarten, Blumen, Sitzen/Grillen, Pool, Teich) – drei Abschnitte
	a.switch_room("garden")
	await _frames(4)
	_m["garten_items"] = Placement.all_items(a.room).size()
	a.camera.set_visible_height(600.0)
	var k: int = 0
	for gx: float in [520.0, 1250.0, 1980.0]:
		a.camera.position.x = gx
		a.camera._clamp_position()
		await _frames(3)
		k += 1
		await _shot("p07_05_garten_%d" % k)
	# Kreislauf: säen → gießen → wachsen → ernten (Uhr vorgedreht)
	Garden.fixed_now = _now
	var bed: ItemNode = null
	var seeds: ItemNode = null
	var can: ItemNode = null
	for it: ItemNode in Placement.all_items(a.room):
		if String(it.def.id) == "garden_raised_bed_m_carrot_oak":
			bed = it
		elif String(it.def.id) == "garden_seeds_carrot_pack":
			seeds = it
		elif String(it.def.id) == "garden_watering_can_mint":
			can = it
	a.camera.setup_for_room(a.room, bed.position.x + 60.0)     # Normal-Zoom, Boden unten im Bild
	for step: Array in [["gesaet", 0], ["gegossen", 1], ["gewachsen", 2], ["reif", 3], ["geerntet", 4]]:
		match int(step[1]):
			0:
				seeds.get_parent().remove_child(seeds)
				a.room.ysort_root.add_child(seeds)
				seeds.position = bed.position + Vector2(4.0, 4.0)
				_m["gesaet"] = Garden.on_drop(a.room, seeds)
			1:
				can.position = bed.position + Vector2(-6.0, 6.0)
				_m["gegossen"] = Garden.on_drop(a.room, can)
			2, 3:
				_now += Garden.GROW_S + 1.0
				Garden.fixed_now = _now
				Garden.tick(a.room)
			4:
				_m["ernte"] = Garden.harvest(bed).size()
		_m["beet_" + String(step[0])] = bed.state
		await _frames(3)
		await _shot("p07_06_beet_%d_%s" % [int(step[1]), String(step[0])])
	# T11: Rundgang durch alle Räume (Test-Szene je Raum) – leer bis auf den Licht-Schalter, Küche mit Ausstattung
	var tour: Array = []
	for rid: Variant in a.room_ids():
		a.switch_room(String(rid))
		await _frames(4)
		tour.append("%s:%d" % [rid, Placement.all_items(a.room).size()])
		await _shot("p07_10_raum_%s" % String(rid))
	_m["rundgang"] = tour
	_m["letzter_raum"] = Game.last_room(&"home")
	Game.save_now()
	var f := FileAccess.open(out_dir.path_join("p07_rooms.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(_m, "  "))
	f.close()
	print(JSON.stringify(_m))
	get_tree().quit(0)


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
