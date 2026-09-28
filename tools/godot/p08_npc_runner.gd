extends Node
## P08-Beweis: Nachbarin + Briefträger im Garten, Kassiererin scannt (Piep, Tüte), Bademeister holt eine Figur
## aus dem Becken, Hund frisst aus dem Napf und schläft im Körbchen. Bedient die Spiel-API, Zeit per tick().
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p08_npc_runner.gd docs/tests/P08

const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")

var out_dir: String = "docs/tests/P08"
var _m: Dictionary = {}


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else out_dir
	DirAccess.make_dir_recursive_absolute(out_dir)
	CharacterRig.animate_poses = false
	PetNode.autonomous = false
	NpcBrain.autonomous = false
	AudioBus.clock = func() -> float: return 0.0
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	Game.characters.clear()
	Game.pets.clear()
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#f7c9a2"
	Game.add_character(c)
	Game.set_active(c.id)
	Game.set_last_room(&"home", &"garden")
	SceneRouter.pending_area = &"home"
	var a: AreaScene = load("res://src/world/area_scene.tscn").instantiate()
	get_tree().root.add_child(a)
	await _frames(8)
	_m["garten_npcs"] = a.npcs.map(func(b: NpcBrain) -> String: return String(b.role["id"]))
	a.camera.setup_for_room(a.room, 250.0)
	await _shot("p08_01_garten_nachbarin_post")
	var post: NpcBrain = null
	for b: NpcBrain in a.npcs:
		if String(b.role["id"]) == "postman":
			post = b
	post.work._mail_t = 999.0
	for _i: int in 40:
		post.tick(0.1)
	await _shot("p08_02_post_am_briefkasten")
	for _i: int in 200:
		post.tick(0.1)
	_m["post_zugestellt"] = post.work.delivered
	_m["post_zurueck"] = post.at_post()
	a.queue_free()
	await _frames(2)

	# Test-Laden in der Test-Küche: Kasse auf der Arbeitsplatte-Höhe am Boden, Kassiererin dahinter
	var room: Room = _room()
	var cam := WorldCamera.new()
	add_child(cam)
	cam.setup_for_room(room, 330.0)
	var reg: ItemNode = ItemSpawner.on_floor(room, &"shop_cash_register_cream", 300.0, 20.0)
	var cashier: NpcBrain = NpcSpawner.spawn(room, NpcRoles.role("cashier"), {"id": "npc_cash", "role": "cashier", "x_cm": 220.0, "y_cm": 12.0})
	var kid: ItemNode = ItemSpawner.character_on_floor(room, "kid", 430.0, 50.0, c.look())
	var apple: ItemNode = ItemSpawner.on_floor(room, &"food_apple_coral", 340.0, 28.0)
	await _shot("p08_03_kasse_vorher")
	NpcSpawner.item_dropped(room, apple)
	_m["gescannt"] = cashier.work.scanned
	_m["kasse"] = reg.state
	_m["tuete"] = String((apple.get_parent().get_parent() as ItemNode).def.id)
	await _shot("p08_04_kasse_piep_tuete")
	room.queue_free()
	kid = null
	await _frames(2)

	# Bademeister: Figur ins Becken, nach 10 s holt er sie raus
	room = _room()
	cam.setup_for_room(room, 380.0)
	cam.set_visible_height(360.0)
	var pool: ItemNode = ItemSpawner.on_floor(room, &"garden_pool_frame_s_sky", 380.0, 30.0)
	var guard: NpcBrain = NpcSpawner.spawn(room, NpcRoles.role("lifeguard"), {"id": "npc_guard", "role": "lifeguard", "x_cm": 120.0, "y_cm": 50.0})
	var swimmer: CharacterRig = ItemSpawner.character_on_floor(room, "kid", 380.0, 32.0, c.look())
	var p: Vector2 = Seats.point_global(pool, 1) - swimmer.hip_offset() * swimmer.global_scale.y
	swimmer.reparent(pool.on_top_root, false)
	swimmer.slot_index = 1
	swimmer.global_position = p
	swimmer.refresh_pose(false)
	await _shot("p08_05_im_becken")
	for _i: int in 105:
		guard.tick(0.1)
	await _shot("p08_06_bademeister_kommt")
	for _i: int in 150:
		guard.tick(0.1)
	_m["gerettet"] = guard.work.rescued
	await _shot("p08_07_gerettet")
	room.queue_free()
	await _frames(2)

	# Hund: Hunger → Napf, dann müde → Körbchen
	room = _room()
	cam.setup_for_room(room, 400.0)
	cam.set_visible_height(260.0)
	var bowl: ItemNode = ItemSpawner.on_floor(room, &"petgear_bowl_coral", 470.0, 50.0)
	ItemStates.set_state(bowl, "full", true)
	ItemSpawner.on_floor(room, &"petgear_basket_oak", 330.0, 40.0)
	var dog: PetNode = ItemSpawner.on_floor(room, &"pet_dog_brown", 250.0, 50.0) as PetNode
	dog.brain.needs["hunger"] = 1.0
	dog._timer = 0.0
	for _i: int in 90:
		dog.tick(1.0 / 30.0)
	await _shot("p08_08_hund_am_napf")
	for _i: int in 300:
		dog.tick(1.0 / 30.0)
	_m["napf"] = bowl.state
	dog.brain.needs["tired"] = 1.0
	dog._timer = 0.0
	for _i: int in 240:
		dog.tick(1.0 / 30.0)
	_m["hund"] = ["IDLE", "WALK", "FOLLOW", "SEEK", "SLEEP"][dog.mode]
	await _shot("p08_09_hund_schlaeft")
	var f := FileAccess.open(out_dir.path_join("p08_npc.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(_m, "  "))
	f.close()
	print(JSON.stringify(_m))
	get_tree().quit(0)


func _room() -> Room:
	var r: Room = ROOM_SCENE.instantiate()
	add_child(r)
	r.setup(Room.find_room(Room.load_area("res://data/areas/test_kitchen.json"), "kitchen"))
	return r


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
