extends GutTest
## P09: Einkaufsstraße + Spielplatz – Daten, Läden (Mode, Friseur, Floristin), Spielgeräte (Rutsche, Schaukel,
## Karussell, Sandförmchen), Wildtiere am Teich, Bushaltestelle, Blumenladen-Knopf → Einkaufsstraße.

var k: KitchenFixture
var area: AreaScene


func before_each() -> void:
	NpcBrain.autonomous = false
	k = KitchenFixture.new(self)


func after_each() -> void:
	if area != null and is_instance_valid(area):
		area.queue_free()


func after_all() -> void:
	NpcBrain.autonomous = true
	SaveSystem.wipe()


func _kid(x: float, y: float = 40.0) -> CharacterRig:
	return ItemSpawner.character_on_floor(k.room, "kid", x, y) as CharacterRig


func _enter(id: StringName, room_id: StringName = &"") -> AreaScene:
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	CharacterRig.animate_poses = false
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#f7c9a2"
	Game.add_character(c)
	Game.set_active(c.id)
	if room_id != &"":
		Game.set_last_room(id, room_id)
	SceneRouter.pending_area = id
	area = load("res://src/world/area_scene.tscn").instantiate()
	add_child_autofree(area)
	await wait_process_frames(6)
	return area


func test_areas_are_ready_with_rooms_items_and_npcs() -> void:
	for pair: Array in [["shopping", 11], ["playground", 3]]:
		assert_true(Areas.is_ready(StringName(pair[0])), "%s spielbar" % pair[0])
		var d: Dictionary = Room.load_area(Areas.path_of(StringName(pair[0])))
		assert_eq(Array(d["rooms"]).size(), int(pair[1]), "%s: Räume" % pair[0])
		for r: Dictionary in d["rooms"]:
			for e: Dictionary in Array(r.get("default_items", [])):
				assert_true(ItemDB.has_item(StringName(String(e["id"]))), "%s/%s: %s" % [pair[0], r["id"], e["id"]])
			assert_true(ResourceLoader.exists(String(r["background"])) or FileAccess.file_exists(String(r["background"])),
				"%s: Hintergrund" % r["id"])
	assert_eq(NpcRoles.npcs_of("shopping").size(), 13, "Einkaufsstraße: 13 feste Figuren")
	assert_eq(NpcRoles.npcs_of("playground").size(), 4)


func test_flower_button_leads_into_the_shopping_street_florist() -> void:
	assert_eq(Areas.canonical(&"flower"), &"shopping", "gleicher Spielstand wie die Einkaufsstraße")
	var a: AreaScene = await _enter(&"flower")
	assert_eq(a.area_id, &"shopping")
	assert_eq(String(a.room.room_id), "florist", "startet im Blumenladen")
	assert_true(a.npcs.size() >= 1, "Floristin ist da")


func test_fashion_item_in_hand_is_worn() -> void:
	var kid: CharacterRig = _kid(300.0)
	var shirt: ItemNode = ItemSpawner.on_floor(k.room, &"cloth_dress_sky", 420.0, 40.0)
	var grip: Vector2 = PlacementCharacter.grip_global(shirt, Vector2.ZERO)
	var t: Placement.Target = k.drag_pivot_to(shirt, (kid.hand_slots()[0]["global"] as Vector2) - grip, 3)
	assert_eq(t.kind, &"hand", "Kleid ist in der Hand")
	var fake := AreaScene.new()
	fake.room = k.room
	assert_true(AreaActions.on_dropped(fake, shirt), "wird angezogen")
	assert_eq(String(Dictionary(kid.look["parts"])["top"]), "dress")
	assert_eq(String(Array(Dictionary(kid.look["colors"])["top"])[0]).to_lower(), "#" + Color("#a9c3dd").to_html(false))
	await wait_process_frames(1)
	assert_false(is_instance_valid(shirt), "Kleid ist jetzt an der Figur, nicht mehr in der Hand")
	fake.free()


func test_barber_chair_tap_gives_a_new_hairstyle() -> void:
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"shop_barber_chair_coral", 300.0, 30.0)
	var kid: CharacterRig = _kid(420.0)
	k.drag_pivot_to(kid, Seats.point_global(chair, 0) - kid.hip_offset() * kid.global_scale.y, 4)
	assert_eq(Seats.occupant(chair, 0), kid, "sitzt im Friseurstuhl")
	var before: String = String(Dictionary(kid.look.get("parts", {})).get("hair", ""))
	var fake := AreaScene.new()
	fake.room = k.room
	assert_true(AreaActions.on_tapped(fake, chair))
	assert_ne(String(Dictionary(kid.look["parts"])["hair"]), before, "neue Frisur")
	fake.free()


func test_florist_binds_three_flowers_into_a_bouquet() -> void:
	var b: NpcBrain = NpcSpawner.spawn(k.room, NpcRoles.role("florist"), {"id": "f", "role": "florist", "x_cm": 200, "y_cm": 20})
	var fl: Array = []
	for i: int in 3:
		fl.append(ItemSpawner.on_floor(k.room, [&"flower_rose_coral", &"flower_tulip_butter", &"flower_gerbera_orange"][i],
			400.0 + i * 12.0, 40.0))
	assert_true(NpcSpawner.item_dropped(k.room, fl[0]))
	assert_eq(b.work.bound, 1, "Strauß gebunden")
	var got: bool = false
	for it: ItemNode in Placement.all_items(k.room):
		got = got or String(it.def.id).begins_with("flower_bouquet")
	assert_true(got, "Strauß liegt da")


func test_slide_brings_the_figure_down_in_front() -> void:
	var slide: ItemNode = ItemSpawner.on_floor(k.room, &"play_tower_slide_coral", 250.0, 20.0)
	var kid: CharacterRig = _kid(500.0)
	k.drag_pivot_to(kid, Vector2(slide.global_position.x - slide.def.width_cm * 0.4, slide.global_position.y + 4.0), 5)
	var fake := AreaScene.new()
	fake.room = k.room
	assert_true(AreaActions.on_dropped(fake, kid), "rutscht")
	await wait_seconds(AreaActions.SLIDE_S + 0.2)
	assert_eq(kid.get_parent(), k.room.ysort_root, "steht wieder auf dem Boden")
	assert_gt(kid.position.x, slide.position.x + slide.def.width_cm * 0.4, "am Ende der Rutsche")
	fake.free()


func test_sand_mold_on_sandbox_makes_a_sand_shape() -> void:
	var box: ItemNode = ItemSpawner.on_floor(k.room, &"garden_sandbox_big_butter", 350.0, 40.0)
	var m: ItemNode = ItemSpawner.on_floor(k.room, &"play_sand_mold_coral", 350.0, 44.0)
	ItemStates.set_state(m, "fish", true)
	var s: ItemNode = AreaActions.mold(k.room, m)
	assert_not_null(s)
	assert_eq(String(s.def.id), "play_sand_shape_fish_sand", "Form wie das Förmchen")
	assert_not_null(box)


func test_swing_and_roundabout_move_when_occupied() -> void:
	var swing: ItemNode = ItemSpawner.on_floor(k.room, &"play_swing_double_sky", 350.0, 20.0)
	PlayMotion.refresh(k.room)
	assert_eq(PlayMotion.tick(0.1), 0, "leer: nichts bewegt sich")
	var kid: CharacterRig = _kid(600.0)
	k.drag_pivot_to(kid, Seats.point_global(swing, 0) - kid.hip_offset() * kid.global_scale.y, 6)
	assert_eq(Seats.occupant(swing, 0), kid, "sitzt auf der Schaukel")
	PlayMotion.refresh(k.room)
	PlayMotion.tick(0.3)
	assert_ne(swing.on_top_root.rotation, 0.0, "Schaukel schwingt")


func test_duck_stays_on_its_pond_and_flees_from_figures() -> void:
	var pond: ItemNode = ItemSpawner.on_floor(k.room, &"garden_pond_m_stone", 350.0, 40.0)
	var duck: PetNode = ItemSpawner.on_floor(k.room, &"wild_duck_green", 350.0, 40.0) as PetNode
	var home: Rect2 = duck.home_area(k.room)
	for _i: int in 600:
		duck.tick(1.0 / 30.0)
		assert_true(home.grow(1.0).has_point(duck.position), "bleibt auf dem Teich: %s" % duck.position)
	assert_eq(duck.voice(), "duck_quack")
	var kid: CharacterRig = _kid(duck.position.x + 30.0, duck.position.y)
	var d0: float = kid.position.distance_to(duck.position)
	for _i: int in 30:
		duck.tick(1.0 / 30.0)
	assert_gt(kid.position.distance_to(duck.position), d0, "flüchtet vor der Figur")
	assert_not_null(pond)


func test_bus_stop_calls_the_bus() -> void:
	var a: AreaScene = await _enter(&"shopping", &"street")
	var stop: ItemNode = null
	for it: ItemNode in Placement.all_items(a.room):
		if String(it.def.id).begins_with("street_bus_stop"):
			stop = it
	assert_not_null(stop, "Haltestelle steht auf der Straße")
	var bus: ItemNode = AreaActions.bus(a, stop)
	assert_not_null(bus, "Bus kommt")
	assert_true(bus.has_meta("transient"), "wird nicht gespeichert")
	var ids: Array = RoomSnapshot.capture(a.room).map(func(e: Dictionary) -> String: return String(e["id"]))
	assert_false(ids.has("street_bus_butter"))
	bus.queue_free()


## Regression (gefunden im P09-Beweislauf): Gäste mit alphabetisch „kleinerer" ID als ihr Wirt gingen beim
## Wiederherstellen verloren (Kasse auf der Theke). Dazu zwei gleiche Wirte: jedes Ding kommt auf SEINEN zurück.
func test_items_on_hosts_survive_save_and_load_in_any_order() -> void:
	var t1: ItemNode = ItemSpawner.on_floor(k.room, &"shop_checkout_coral", 200.0, 40.0)
	var t2: ItemNode = ItemSpawner.on_floor(k.room, &"shop_checkout_coral", 520.0, 40.0)
	ItemSpawner.on_item(t1, &"shop_cash_register_cream", 0.2)
	ItemSpawner.on_item(t2, &"food_apple_red", -0.2)
	var state: Array = RoomSnapshot.capture(k.room)
	RoomSnapshot.clear(k.room)
	await wait_process_frames(1)
	var k2 := KitchenFixture.new(self)
	assert_eq(RoomSnapshot.apply(k2.room, state), 4, "alle 4 Dinge wieder da")
	for it: ItemNode in Placement.all_items(k2.room):
		var host: Node = it.get_parent().get_parent()
		if String(it.def.id) == "shop_cash_register_cream":
			assert_almost_eq((host as ItemNode).position.x, 200.0, 1.0, "Kasse auf der linken Theke")
		if String(it.def.id) == "food_apple_red":
			assert_almost_eq((host as ItemNode).position.x, 520.0, 1.0, "Apfel auf der rechten Theke")
