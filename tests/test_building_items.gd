extends GutTest
## P07: Räume sind leer – Fenster, Türen, Vorhänge, Poster hängen an der Wand, Teppiche liegen flach unter allem.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func _first(prefix: String) -> StringName:
	for gid: String in Catalog.group_ids():
		for id: Variant in Catalog.items(gid):
			if String(id).begins_with(prefix):
				return StringName(String(id))
	return &""


func _bottom_y(it: ItemNode) -> float:
	return it.global_rect().end.y


func test_catalog_has_windows_doors_curtains_rugs() -> void:
	for g: String in ["windows", "doors", "curtains", "rugs", "walldeco"]:
		assert_true(Catalog.group_ids().has(g), "Katalog-Reiter %s" % g)
	var shapes: Dictionary = {}
	for id: Variant in Catalog.items("windows"):
		shapes[String(id).split("_")[1]] = true
	assert_gte(shapes.size(), 10, "viele Fensterformen")
	var rugs: Array = Catalog.items("rugs").map(func(x: Variant) -> String: return String(x))
	for kind: String in ["rug_rect", "rug_round", "rug_runner", "rug_doormat"]:
		assert_true(rugs.any(func(x: String) -> bool: return x.begins_with(kind)), kind)


func test_window_hangs_at_sill_height_and_never_below_floor() -> void:
	var w: ItemNode = ItemSpawner.place(k.room, _first("win_double_m"), 300.0, 30.0)
	assert_true(w.def.is_wall())
	assert_almost_eq(_bottom_y(w), -ItemSpawner.WALL_SILL_CM, 1.0, "Fensterbank auf 90 cm")
	assert_eq(w.z_index, -2, "Wand liegt hinter allem")
	var t: Placement.Target = k.drag_pivot_to(w, Vector2(300.0, 60.0))   # mitten auf den Boden gezogen
	assert_eq(t.kind, &"wall", "bleibt an der Wand")
	assert_lte(_bottom_y(w), 0.5, "nie unter die Bodenlinie")
	t = k.drag_pivot_to(w, Vector2(300.0, -150.0))
	assert_almost_eq(w.position.y, -150.0, 1.0, "hängt, wo man es loslässt")


func test_door_stands_on_the_floor_line() -> void:
	var d: ItemNode = ItemSpawner.place(k.room, _first("door_wood"), 200.0, 30.0)
	assert_almost_eq(_bottom_y(d), 0.0, 0.6, "Tür steht auf der Bodenlinie")
	k.drag_pivot_to(d, Vector2(250.0, -180.0))
	assert_almost_eq(_bottom_y(d), 0.0, 0.6, "auch nach dem Verschieben")


func test_rug_lies_under_everything_and_never_on_a_table() -> void:
	var rug: ItemNode = ItemSpawner.on_floor(k.room, _first("rug_rect"), 300.0, 40.0)
	assert_eq(rug.z_index, -1, "Teppich unter allem")
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 500.0, 20.0)
	var t: Placement.Target = Placement.find_target(k.room, rug, Vector2(500.0, table.top_global_y() - 1.0),
		Vector2(500.0, table.top_global_y() - 5.0))
	assert_eq(t.kind, &"floor", "Teppich landet nie auf dem Tisch")
	var chair: ItemNode = ItemSpawner.on_floor(k.room, _first("furn_chair_dining"), 300.0, 40.0)
	var seat_y: float = chair.global_position.y - 44.0 * chair.global_scale.y   # Sitzfläche (45 cm) – liegt über dem Teppich
	assert_true(rug.global_rect().has_point(Vector2(300.0, seat_y)), "Punkt liegt auch auf dem Teppich")
	assert_eq(k.drag.pick_item(Vector2(300.0, seat_y)), chair, "Stuhl auf dem Teppich wird zuerst gegriffen")


func test_wall_items_survive_save_and_load() -> void:
	var w: ItemNode = ItemSpawner.place(k.room, _first("win_round_m"), 420.0, 30.0)
	var pos: Vector2 = w.position
	var wid: StringName = w.def.id
	var snap: Array = RoomSnapshot.capture(k.room)
	RoomSnapshot.clear(k.room)
	await wait_process_frames(2)
	RoomSnapshot.apply(k.room, snap)
	var back: ItemNode = null
	for it: ItemNode in Placement.all_items(k.room):
		if it.def.id == wid:
			back = it
	assert_not_null(back)
	assert_almost_eq(back.position.y, pos.y, 0.2, "hängt wieder an derselben Stelle der Wand")
	assert_eq(back.z_index, -2)
