extends Node
## P07-Beweis: Zuhause mit 11 Räumen – leerer Raum, Raum-Wahl, Deko-Leiste, selbst eingerichtetes Kinderzimmer
## (Fenster, Vorhang, Teppich, Bett, Regal, Spielzeug) und der Garten. Bedient die Spiel-API wie ein Finger.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p07_rooms_runner.gd docs/tests/P07

var out_dir: String = "docs/tests/P07"
var _m: Dictionary = {}


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

	# Garten (draußen, Kulisse) mit Beeten, Pool, Pavillon
	a.switch_room("garden")
	await _frames(4)
	var gx: float = a.camera.get_screen_center_position().x
	for p: Array in [["garden_fence_picket_m_white", gx - 330, 0], ["garden_fence_picket_m_white", gx - 180, 0],
			["garden_raised_bed_m_carrot_oak", gx - 250, 30], ["garden_flower_bed_m_rose", gx - 60, 45],
			["garden_pool_frame_s_sky", gx + 200, 40], ["garden_parasol_coral", gx + 60, 15],
			["garden_table_bistro_white", gx - 20, 10], ["garden_hedge_box_leaf", gx + 380, 0]]:
		ItemSpawner.on_floor(a.room, StringName(String(p[0])), float(p[1]), float(p[2]))
	var bed: ItemNode = null
	for it: ItemNode in Placement.all_items(a.room):
		if String(it.def.id).begins_with("garden_raised_bed"):
			bed = it
	if bed != null:
		ItemStates.set_state(bed, "ripe", true)
	await _frames(4)
	await _shot("p07_05_garten")
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
