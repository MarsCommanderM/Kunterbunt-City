extends Node
## P09-Beweis: Einkaufsstraße (Straße + alle Läden) und Spielplatz & Park (alle Räume) im echten Renderer,
## dazu Kasse, Anziehen, Friseur, Strauß, Rutsche, Schaukel, Enten. Bedient die Spiel-API wie ein Finger.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p09_areas_runner.gd docs/tests/P09

var out_dir: String = "docs/tests/P09"
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
	for area_id: StringName in [&"shopping", &"playground"]:
		SceneRouter.pending_area = area_id
		var a: AreaScene = load("res://src/world/area_scene.tscn").instantiate()
		get_tree().root.add_child(a)
		await _frames(8)
		var tour: Array = []
		for rid: Variant in a.room_ids():
			a.switch_room(String(rid))
			await _frames(4)
			if String(rid) in ["street", "playground", "pond", "meadow"]:
				a.camera.set_visible_height(560.0)
				await _frames(2)
			tour.append("%s:%d/%d" % [rid, Placement.all_items(a.room).size(), a.npcs.size()])
			await _shot("p09_%s_%s" % [area_id, rid])
			if String(rid) == "street":
				a.camera.position.x = 1500.0
				a.camera._clamp_position()
				await _shot("p09_%s_street_mitte" % area_id)
		_m[String(area_id)] = tour
		if area_id == &"shopping":
			await _shop_actions(a)
		else:
			await _park_actions(a)
		Game.save_now()
		a.queue_free()
		await _frames(3)
	var f := FileAccess.open(out_dir.path_join("p09_areas.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(_m, "  "))
	f.close()
	print(JSON.stringify(_m))
	get_tree().quit(0)


func _find(a: AreaScene, prefix: String) -> ItemNode:
	for it: ItemNode in Placement.all_items(a.room):
		if String(it.def.id).begins_with(prefix):
			return it
	return null


func _shop_actions(a: AreaScene) -> void:
	# Modeladen: Kleid in die Hand → angezogen
	a.switch_room("fashion")
	await _frames(4)
	var dress: ItemNode = _find(a, "cloth_dress")
	dress.reparent((a.me as CharacterRig).slot_front, false)
	dress.position = Vector2.ZERO
	_m["angezogen"] = AreaActions.on_dropped(a, dress)
	_m["oberteil"] = String(Dictionary((a.me as CharacterRig).look["parts"]).get("top", ""))
	await _shot("p09_20_modeladen_angezogen")
	# Friseur: Figur in den Stuhl, Stuhl antippen
	a.switch_room("hairdresser")
	await _frames(4)
	var chair: ItemNode = _find(a, "shop_barber_chair")
	var rig: CharacterRig = a.me as CharacterRig
	rig.reparent(chair.on_top_root, false)
	rig.slot_index = 0
	rig.global_position = Seats.point_global(chair, 0) - rig.hip_offset() * rig.global_scale.y
	rig.refresh_pose(false)
	var before: String = String(Dictionary(rig.look["parts"]).get("hair", ""))
	AreaActions.on_tapped(a, chair)
	AreaActions.on_tapped(a, chair)
	_m["frisur"] = [before, String(Dictionary(rig.look["parts"]).get("hair", ""))]
	await _shot("p09_21_friseur_neue_frisur")
	# Blumenladen: 3 Blumen → Strauß
	a.switch_room("florist")
	await _frames(4)
	var flowers: Array = []
	for it: ItemNode in Placement.all_items(a.room):
		if it.def.tags.has("flower") and it.get_parent() != a.room.ysort_root:
			flowers.append(it)                          # die Blumen auf der Theke
	_m["blumen_auf_theke"] = flowers.size()
	if not flowers.is_empty():
		NpcSpawner.item_dropped(a.room, flowers[0])
	_m["strauss"] = _find(a, "flower_bouquet") != null
	await _shot("p09_22_blumenladen_strauss")
	# Supermarkt: Apfel an die Kasse
	a.switch_room("market")
	await _frames(4)
	var apple: ItemNode = _find(a, "food_banana")
	var reg: ItemNode = _find(a, "shop_cash_register")
	apple.reparent(a.room.ysort_root, true)
	apple.global_position = reg.global_position + Vector2(40.0, 0.0)
	_m["kasse"] = NpcSpawner.item_dropped(a.room, apple)
	await _shot("p09_23_supermarkt_kasse")
	_m["sticker_shopping"] = Game.secrets.size()


func _park_actions(a: AreaScene) -> void:
	a.switch_room("playground")
	await _frames(4)
	var swing: ItemNode = _find(a, "play_swing_double")
	var rig: CharacterRig = a.me as CharacterRig
	rig.reparent(swing.on_top_root, false)
	rig.slot_index = 0
	rig.global_position = Seats.point_global(swing, 0) - rig.hip_offset() * rig.global_scale.y
	rig.refresh_pose(false)
	PlayMotion.refresh(a.room)
	PlayMotion.tick(0.45)
	a.camera.setup_for_room(a.room, swing.position.x)
	_m["schaukel_schwingt"] = absf(swing.on_top_root.rotation) > 0.01
	await _shot("p09_30_schaukel")
	a.switch_room("pond")
	await _frames(4)
	var ducks: int = 0
	for it: ItemNode in Placement.all_items(a.room):
		if String(it.def.id).begins_with("wild_duck"):
			ducks += 1
			for _i: int in 40:
				(it as PetNode).tick(0.1)
	_m["enten"] = ducks
	a.camera.setup_for_room(a.room, 900.0)
	await _shot("p09_31_teich_enten")


func _frames(n: int) -> void:
	for i: int in n:
		await get_tree().process_frame
	await RenderingServer.frame_post_draw


func _shot(name: String) -> void:
	await _frames(3)
	var img: Image = get_tree().root.get_texture().get_image()
	if img != null:
		img.save_jpg(out_dir.path_join(name + ".jpg"), 0.88)
		print("Screenshot: %s" % name)
