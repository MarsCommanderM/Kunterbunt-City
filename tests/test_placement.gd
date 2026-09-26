extends GutTest
## Wo landet ein Item? Oberflächen, Regel S-11 (max. 60 cm auf Flächen), Platz unter Regalen, Einrasten.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func _target(item: ItemNode, pivot: Vector2) -> Placement.Target:
	return Placement.find_target(k.room, item, pivot, pivot + Vector2(0, -5))


func test_counter_is_found_from_above() -> void:
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 50.0, 30.0)
	var t: Placement.Target = _target(apple, Vector2(300.0, -120.0))
	assert_eq(t.kind, &"surface")
	assert_eq((t.node as Surface).surface_id, &"counter_top")
	assert_almost_eq(t.global_pos.y, -90.0, 2.0)


func test_snaps_when_slightly_below_surface() -> void:
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 50.0, 30.0)
	var counter: Surface = k.room.get_surface(&"counter_top")
	var t: Placement.Target = _target(apple, Vector2(300.0, counter.top_y() + Placement.SNAP_CM - 1.0))
	assert_eq(t.kind, &"surface", "bis 10 cm drunter rastet noch ein")
	t = _target(apple, Vector2(300.0, counter.top_y() + Placement.SNAP_CM + 5.0))
	assert_eq(t.kind, &"floor", "tiefer → fällt auf den Boden")


func test_shelf_wins_over_counter_when_above_it() -> void:
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 50.0, 30.0)
	var shelf: Surface = k.room.get_surface(&"shelf_right")
	var t: Placement.Target = _target(apple, Vector2(380.0, shelf.top_y() - 5.0))
	assert_eq(t.node, shelf)


func test_chair_on_counter_is_rejected_to_floor() -> void:
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"home_chair_mint", 50.0, 30.0)
	var t: Placement.Target = _target(chair, Vector2(300.0, -100.0))
	assert_eq(t.kind, &"floor")
	assert_string_contains(t.rejected_reason, "Boden")
	var counter: Surface = k.room.get_surface(&"counter_top")
	assert_almost_eq(t.global_pos.y, counter.depth_y_cm + Placement.FRONT_OF_SURFACE_CM, 0.01, "federt vor die Theke")


func test_rule_s11_max_60cm_on_surfaces() -> void:
	var vase: ItemNode = ItemSpawner.on_floor(k.room, &"item_vase_bouquet", 50.0, 30.0)   # 50 cm
	assert_eq(_target(vase, Vector2(300.0, -100.0)).kind, &"surface", "50 cm ist erlaubt")
	var def: ItemDefinition = vase.def.duplicate()
	def.height_cm = 70.0
	var tall := ItemNode.create(def)
	add_child_autofree(tall)
	var t: Placement.Target = _target(tall, Vector2(300.0, -100.0))
	assert_eq(t.kind, &"floor")
	assert_string_contains(t.rejected_reason, "max. 60")


func test_shelf_clearance_is_respected() -> void:
	var low: Surface = k.room.get_surface(&"shelf_left_low")
	var high: Surface = k.room.get_surface(&"shelf_left_high")
	var gap: float = low.top_y() - high.top_y()
	var vase: ItemNode = ItemSpawner.on_floor(k.room, &"item_vase_bouquet", 50.0, 30.0)
	assert_gt(vase.def.height_cm, gap, "Vase (50) ist höher als der Regalabstand")
	var t: Placement.Target = _target(vase, Vector2(200.0, low.top_y() - 3.0))
	assert_eq(t.kind, &"floor")
	assert_string_contains(t.rejected_reason, "passt nicht unter")
	var tulip: ItemNode = ItemSpawner.on_floor(k.room, &"flower_tulip_red_pot", 50.0, 30.0)
	assert_eq(_target(tulip, Vector2(200.0, low.top_y() - 3.0)).node, low, "Tulpe passt drunter")


func test_too_wide_for_stool() -> void:
	var stool: ItemNode = ItemSpawner.on_floor(k.room, &"home_stool", 300.0, 40.0)
	var micro: ItemNode = ItemSpawner.on_floor(k.room, &"kitchen_microwave", 50.0, 30.0)
	var t: Placement.Target = _target(micro, Vector2(300.0, stool.top_global_y() - 4.0))
	assert_eq(t.kind, &"floor")
	assert_string_contains(t.rejected_reason, "breiter")
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 50.0, 30.0)
	assert_eq(_target(apple, Vector2(300.0, stool.top_global_y() - 4.0)).node, stool)


func test_table_cannot_go_on_table() -> void:
	var t1: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 300.0, 40.0)
	var coffee: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_coffee", 600.0, 40.0)
	var t: Placement.Target = _target(coffee, Vector2(300.0, t1.top_global_y() - 5.0))
	assert_eq(t.kind, &"floor")


func test_item_outside_surface_x_range_falls() -> void:
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 600.0, 40.0)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 50.0, 30.0)
	var xr: Vector2 = table.surface_x_range()
	assert_eq(_target(apple, Vector2(xr.y + 3.0, table.top_global_y() - 5.0)).kind, &"floor")
	assert_eq(_target(apple, Vector2(xr.y - 3.0, table.top_global_y() - 5.0)).kind, &"item_surface")


func test_table_surface_uses_measured_tabletop() -> void:
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 600.0, 0.0)
	# Stil-C-Tisch: Platte liegt bei 12 % von oben → 75·0,88 = 66 cm über dem Boden (perspektivische Oberseite)
	assert_almost_eq(table.top_global_y(), -66.0, 0.01)


func test_fall_time_never_above_0_4s() -> void:
	assert_lte(Placement.fall_time(300.0), 0.4)
	assert_gt(Placement.fall_time(90.0), Placement.fall_time(10.0), "tiefer fällt länger")
	assert_gte(Placement.fall_time(0.0), 0.08)
