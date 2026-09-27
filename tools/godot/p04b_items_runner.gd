extends Node
## P04b-Beweis: Katalog-Items im echten Raum (Stil der Figuren, Farbzonen, Maßstab) + Katalog-Fenster.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p04b_items_runner.gd docs/tests/P04b

var out_dir: String = "docs/tests/P04b"


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else out_dir
	DirAccess.make_dir_recursive_absolute(out_dir)
	CharacterRig.animate_poses = false
	PetNode.autonomous = false
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	Game.characters.clear()
	Game.pets.clear()
	var c: CharacterData = CharacterData.create("kid")
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	var set: Dictionary = CharacterParts.random_set("kid", rng)
	c.parts = set["parts"]
	c.colors = set["colors"]
	c.parts["accessory"] = "none"
	c.parts["aid"] = "none"
	c.skin = CharacterParts.palette_colors("skin")[4]
	c.character_name = "Mia"
	Game.add_character(c)
	Game.set_active(c.id)
	SceneRouter.pending_area = &"home"
	var area: AreaScene = load("res://src/world/area_scene.tscn").instantiate()
	get_tree().root.add_child(area)
	await _frames(8)
	# Raum leeren (Entscheidung: leere Räume + Katalog) und neu einrichten – nur aus dem Katalog
	for it: ItemNode in Placement.all_items(area.room):
		if not (it is CharacterRig) and not (it is PetNode):
			it.queue_free()
	await _frames(2)
	var setup: Array = [
		["furn_sofa_round_rose", 300.0, 22.0], ["furn_armchair_classic_sky", 470.0, 26.0],
		["plant_monstera_basket_oak", 150.0, 14.0], ["furn_bookshelf_oak", 80.0, 10.0],
		["deco_lamp_floor_butter", 560.0, 16.0], ["furn_table_coffee_oak", 330.0, 60.0],
		["plant_ficus_terracotta_terracotta", 640.0, 20.0], ["furn_chair_beanbag_yellow", 200.0, 66.0],
		["plant_cactus_ball_terracotta_terracotta_rose", 520.0, 70.0], ["furn_toybox_butter", 610.0, 62.0],
	]
	for e: Array in setup:
		var it: ItemNode = ItemSpawner.on_floor(area.room, StringName(String(e[0])), float(e[1]), float(e[2]))
		if it == null:
			print("fehlt: ", e[0])
	var tab: ItemNode = null
	for it: ItemNode in Placement.all_items(area.room):
		if String(it.def.id) == "furn_table_coffee_oak":
			tab = it
	if tab != null:
		ItemSpawner.on_item(tab, &"plant_succulent_bowl_cream", -0.2)
		ItemSpawner.on_item(tab, &"plant_tulips_round_cream_coral", 0.25)
	area.camera.set_visible_height(330.0)
	await _frames(6)
	await _shot("p04b_01_raum_aus_dem_katalog")
	var panel: CatalogPanel = CatalogPanel.open(area.ui, area.place_from_catalog)
	await _frames(4)
	panel.show_group("plants")
	await _frames(6)
	await _shot("p04b_02_katalog_pflanzen")
	panel.show_group("sofas")
	await _frames(6)
	await _shot("p04b_03_katalog_sofas")
	print("Katalog: %d Items in %d Reitern" % [Catalog.count(), Catalog.group_ids().size()])
	panel.queue_free()
	# Zustände: Schrank/Schublade auf, Geräte an, Kochen
	for it: ItemNode in Placement.all_items(area.room):
		if not (it is CharacterRig) and not (it is PetNode):
			it.queue_free()
	await _frames(2)
	Recipes.instant = true
	var st: Array = [
		["app_fridge_cream", 90.0, 10.0, "open"], ["furn_wardrobe_sky", 230.0, 8.0, "open"],
		["furn_dresser_mint", 360.0, 16.0, "open"], ["app_stove_cream", 480.0, 12.0, "on"],
		["deco_lamp_floor_butter", 580.0, 14.0, "on"], ["elec_tv_black", 660.0, 40.0, "on"],
		["furn_toybox_butter", 150.0, 66.0, "open"], ["kit_blender_cream", 330.0, 70.0, "on"],
	]
	var made: Dictionary = {}
	for e: Array in st:
		var it2: ItemNode = ItemSpawner.on_floor(area.room, StringName(String(e[0])), float(e[1]), float(e[2]))
		if it2 == null:
			print("fehlt: ", e[0])
			continue
		made[String(e[0])] = it2
	if made.has("app_fridge_cream"):
		for f: String in ["food_apple_coral", "food_carton_cream", "food_cheese_butter", "food_cake_cream"]:
			ItemSpawner.into_container(made["app_fridge_cream"], StringName(f))
	if made.has("app_stove_cream"):
		var pan: ItemNode = ItemSpawner.into_container(made["app_stove_cream"], &"kit_pan_black")
		if pan != null:
			ItemSpawner.into_container(pan, &"food_egg_cream")
	if made.has("kit_blender_cream"):
		ItemSpawner.into_container(made["kit_blender_cream"], &"food_banana_butter")
	for e: Array in st:
		if made.has(String(e[0])):
			ItemStates.set_state(made[String(e[0])], String(e[3]), true)
	area.camera.set_visible_height(330.0)
	await _frames(8)
	await _shot("p04b_04_zustaende_kochen")
	# „Alles geht überall“: Schwimmbad-Luftmatratze als Bett in der Küche (Zuhause hat bis P07 nur diesen Raum)
	for it: ItemNode in Placement.all_items(area.room):
		if not (it is CharacterRig) and not (it is PetNode):
			it.queue_free()
	await _frames(2)
	var mat: ItemNode = ItemSpawner.on_floor(area.room, &"pool_air_mattress_coral", 330.0, 30.0)
	ItemSpawner.on_floor(area.room, &"furn_sofa_classic_mint", 560.0, 8.0)
	ItemSpawner.on_floor(area.room, &"pool_swim_ring_sky", 180.0, 12.0)
	ItemSpawner.on_floor(area.room, &"pool_inflatable_animal_butter", 110.0, 50.0)
	ItemSpawner.on_floor(area.room, &"plant_palm_basket_oak", 700.0, 12.0)
	ItemSpawner.on_floor(area.room, &"camp_lantern_green", 460.0, 60.0)
	var fig: CharacterRig = null
	for it: ItemNode in Placement.all_items(area.room):
		if it is CharacterRig:
			fig = it
	var how: String = "keine Figur"
	if fig != null and mat != null:
		var p: Vector2 = Seats.point_global(mat, 0)
		p -= fig.hip_offset() * fig.global_scale.y
		area.drag.scripted_move(fig, p + Vector2(6, -8))
		how = fig.body_pose if Seats.seat_host_of(fig) == mat else "nicht auf der Matratze"
	for it: ItemNode in Placement.all_items(area.room):
		if String(it.def.id) == "camp_lantern_green":
			ItemStates.set_state(it, "on", true)
	print("Luftmatratze in der Küche: Figur %s" % how)
	area.camera.set_visible_height(330.0)
	await _frames(90)     # Ablegen/Ankunfts-Hüpfer ausklingen lassen (Tweens)
	await _shot("p04b_05_luftmatratze_in_der_kueche")
	get_tree().quit()


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
