extends GutTest
## Pflicht-Test (Tech-Spec §6): Anfassen → Ziehen → Abstellen, mit echten Items in der echten Test-Küche.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func test_apple_from_counter_onto_table() -> void:
	var apple: ItemNode = ItemSpawner.on_surface(k.room, &"food_apple_red", &"counter_top", 300.0)
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 600.0, 40.0)
	var top: float = table.top_global_y()
	var t: Placement.Target = k.drag_pivot_to(apple, Vector2(600.0, top - 30.0))
	assert_eq(t.kind, &"item_surface")
	assert_eq(apple.get_parent(), table.on_top_root, "Apfel gehört jetzt zum Tisch")
	assert_almost_eq(apple.global_position.y, top, 0.01, "steht genau auf der Tischplatte")
	assert_almost_eq(apple.global_position.x, 600.0, 0.01)
	assert_almost_eq(apple.global_scale.y, table.global_scale.y, 0.0001, "gleiche Tiefe wie der Tisch")


func test_drop_in_air_falls_to_floor_with_depth_scale() -> void:
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 100.0, 10.0)
	var t: Placement.Target = k.drag_pivot_to(ball, Vector2(560.0, 60.0))
	assert_eq(t.kind, &"floor")
	assert_eq(ball.get_parent(), k.room.ysort_root)
	assert_almost_eq(ball.position, Vector2(560.0, 60.0), Vector2(0.01, 0.01))
	assert_almost_eq(ball.scale.y, k.room.floor_band.depth_factor(60.0), 0.0001)


func test_drop_high_above_empty_floor_lands_on_back_line() -> void:
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 100.0, 10.0)
	var t: Placement.Target = k.drag_pivot_to(ball, Vector2(600.0, -150.0))
	assert_eq(t.kind, &"floor")
	assert_almost_eq(ball.position.y, k.room.floor_band.back_y_cm, 0.01, "fällt runter bis zur hinteren Bodenlinie")


func test_drop_below_floor_band_is_clamped() -> void:
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 100.0, 10.0)
	k.drag_pivot_to(ball, Vector2(600.0, 500.0))
	assert_almost_eq(ball.position.y, k.room.floor_band.front_y_cm, 0.01)
	assert_almost_eq(ball.scale.y, 1.12, 0.0001, "vorne max. ×1,12")


func test_while_dragging_item_is_in_drag_layer_and_lifted() -> void:
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 300.0, 30.0)
	var p: Vector2 = apple.global_rect().get_center()
	k.drag.press(0, p)
	k.drag.move(0, p + Vector2(20, -20))
	assert_eq(apple.get_parent(), k.drag.drag_layer)
	assert_eq(apple.lifted, 1.0)
	assert_true(k.drag.is_dragging(apple))
	k.drag.release(0, p + Vector2(20, -20))
	assert_eq(apple.lifted, 0.0)
	assert_eq(k.drag.active_count(), 0)


func test_tap_does_not_move_item() -> void:
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 300.0, 30.0)
	var before: Vector2 = apple.global_position
	watch_signals(k.drag)
	k.tap(apple)
	assert_eq(apple.global_position, before)
	assert_signal_emitted(k.drag, "item_tapped")
	assert_signal_not_emitted(k.drag, "item_dropped")
	assert_eq(k.drag.undo.size(), 0, "Tippen ist kein Undo-Schritt")


func test_fixture_cannot_be_dragged_but_opens_on_tap() -> void:
	var fridge: ItemNode = ItemSpawner.on_floor(k.room, &"fix_fridge", 520.0, 1.0)
	var p: Vector2 = k.grab_point(fridge)
	var before: Vector2 = fridge.global_position
	k.drag.press(0, p)
	k.drag.move(0, p + Vector2(80, 0))
	k.drag.release(0, p + Vector2(80, 0))
	assert_eq(fridge.global_position, before, "Kühlschrank bleibt fest")
	assert_eq(fridge.get_parent(), k.room.ysort_root)
	assert_false(fridge.is_open, "wischen über den Kühlschrank öffnet ihn nicht")
	k.tap(fridge)
	assert_true(fridge.is_open, "antippen öffnet")


func test_dragging_table_takes_items_along() -> void:
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 400.0, 30.0)
	var apple: ItemNode = ItemSpawner.on_item(table, &"food_apple_red", -0.3)
	var local_before: Vector2 = apple.position
	var dx: float = apple.global_position.x - table.global_position.x
	k.drag_pivot_to(table, Vector2(250.0, 50.0))
	assert_almost_eq(table.global_position, Vector2(250.0, 50.0), Vector2(0.01, 0.01))
	assert_eq(apple.get_parent(), table.on_top_root)
	assert_eq(apple.position, local_before, "liegt unverändert auf dem Tisch")
	var ratio: float = table.global_scale.x / k.room.floor_band.depth_factor(30.0)
	assert_almost_eq(apple.global_position.x - table.global_position.x, dx * ratio, 0.01)
	assert_almost_eq(apple.global_position.y, table.top_global_y(), 0.01, "Apfel bleibt auf der Platte")


func test_pick_prefers_item_on_top_of_table() -> void:
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 400.0, 30.0)
	var apple: ItemNode = ItemSpawner.on_item(table, &"food_apple_red", 0.0)
	assert_eq(k.drag.pick_item(apple.global_rect().get_center()), apple)


func test_pick_prefers_front_item() -> void:
	var back: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 300.0, 20.0)
	var front: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 305.0, 30.0)
	var p: Vector2 = back.global_rect().get_center().lerp(front.global_rect().get_center(), 0.5)
	assert_eq(k.drag.pick_item(p), front)


func test_tiny_egg_has_48dp_touch_area() -> void:
	var egg: ItemNode = ItemSpawner.on_floor(k.room, &"food_egg", 300.0, 30.0)
	var min_cm: float = UiConstants.MIN_TOUCH_DP / Units.zoom_for_visible_height(1080.0, Units.DEFAULT_VIEW_HEIGHT_CM)
	assert_lt(egg.global_rect().size.x, min_cm, "Ei ist kleiner als die Tippfläche")
	var near: Vector2 = egg.global_rect().get_center() + Vector2(min_cm * 0.45, 0)
	assert_eq(k.drag.pick_item(near), egg, "knapp neben dem Ei trifft trotzdem")
	assert_null(k.drag.pick_item(egg.global_rect().get_center() + Vector2(min_cm * 0.6, 0)))


func test_big_sprite_uses_alpha_hit() -> void:
	var dog: ItemNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 300.0, 30.0)
	var r: Rect2 = dog.global_rect()
	assert_true(dog.hit_test(r.get_center(), 13.0))
	assert_false(dog.hit_test(r.position + Vector2(1, 1), 13.0), "transparente Ecke zählt nicht")


func test_multitouch_three_at_once_fourth_refused() -> void:
	var items: Array[ItemNode] = []
	for i: int in 4:
		items.append(ItemSpawner.on_floor(k.room, &"toy_beachball", 80.0 + i * 120.0, 40.0))
	for i: int in 3:
		assert_true(k.drag.press(i, items[i].global_rect().get_center()))
		k.drag.move(i, items[i].global_rect().get_center() + Vector2(0, -30))
	assert_false(k.drag.press(3, items[3].global_rect().get_center()), "max. 3 gleichzeitig")
	assert_eq(k.drag.active_count(), 3)
	for i: int in 3:
		k.drag.release(i, Vector2(100.0 + i * 150.0, 50.0))
	assert_eq(k.drag.active_count(), 0)
	for i: int in 3:
		assert_eq(items[i].get_parent(), k.room.ysort_root)


func test_signals_and_sounds() -> void:
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 300.0, 30.0)
	watch_signals(k.drag)
	AudioBus.history.clear()
	k.drag_pivot_to(apple, Vector2(400.0, 40.0))
	assert_signal_emitted(k.drag, "item_picked_up")
	assert_signal_emitted(k.drag, "item_dropped")
	assert_has(AudioBus.history, "pickup")
	assert_has(AudioBus.history, "drop_soft", "Essen fällt weich")


func test_hold_without_moving_lifts_after_80ms() -> void:
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 300.0, 30.0)
	k.drag._now_override = 10.0
	k.drag.press(0, apple.global_rect().get_center())
	k.drag._now_override = 10.09
	k.drag._process(0.016)
	assert_eq(apple.get_parent(), k.drag.drag_layer, "nach 80 ms angehoben")
	k.drag.release(0, apple.global_rect().get_center())
	k.drag._now_override = -1.0


func test_acceptance_apple_on_counter_is_exactly_90cm() -> void:
	# Akzeptanz P02: Apfel auf die Arbeitsplatte ziehen → steht exakt auf 90 cm (±0,5)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 600.0, 60.0)
	k.drag_pivot_to(apple, Vector2(300.0, -130.0))
	assert_almost_eq(-apple.global_position.y, 90.0, 0.5, "Unterkante Apfel = 90 cm über dem Boden")
	assert_almost_eq(apple.global_rect().size.y, 8.0, 0.01, "und bleibt 8 cm groß")
