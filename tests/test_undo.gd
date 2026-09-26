extends GutTest
## Rückgängig: max. 30 Schritte, stellt Eltern, Position, Größe und Behälter-Platz wieder her.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func test_undo_restores_counter_position() -> void:
	var apple: ItemNode = ItemSpawner.on_surface(k.room, &"food_apple_red", &"counter_top", 300.0)
	var pos: Vector2 = apple.global_position
	var sc: Vector2 = apple.global_scale
	k.drag_pivot_to(apple, Vector2(600.0, 60.0))
	assert_ne(apple.global_position, pos)
	assert_true(k.drag.undo.undo())
	assert_eq(apple.get_parent(), k.room.ysort_root)
	assert_almost_eq(apple.global_position, pos, Vector2(0.01, 0.01))
	assert_almost_eq(apple.global_scale, sc, Vector2(0.0001, 0.0001))


func test_undo_takes_item_back_out_of_table_stack() -> void:
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 500.0, 30.0)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 200.0, 50.0)
	k.drag_pivot_to(apple, Vector2(500.0, table.top_global_y() - 10.0))
	assert_eq(apple.get_parent(), table.on_top_root)
	k.drag.undo.undo()
	assert_eq(apple.get_parent(), k.room.ysort_root)
	assert_almost_eq(apple.position, Vector2(200.0, 50.0), Vector2(0.01, 0.01))


func test_undo_restores_container_slot() -> void:
	var bag: ItemNode = ItemSpawner.on_floor(k.room, &"item_backpack", 300.0, 40.0)
	bag.set_open(true)
	ItemSpawner.into_container(bag, &"food_egg")
	var apple: ItemNode = ItemSpawner.into_container(bag, &"food_apple_red")
	assert_eq(apple.slot_index, 1)
	k.drag_pivot_to(apple, Vector2(600.0, 60.0))
	assert_eq(apple.slot_index, -1)
	k.drag.undo.undo()
	assert_eq(apple.get_parent(), bag.contents_root)
	assert_eq(apple.slot_index, 1)


func test_max_30_steps() -> void:
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 100.0, 30.0)
	for i: int in 35:
		k.drag_pivot_to(ball, Vector2(100.0 + (i % 2) * 200.0, 30.0))
	assert_eq(k.drag.undo.size(), UndoStack.MAX_STEPS)
	var n: int = 0
	while k.drag.undo.undo():
		n += 1
	assert_eq(n, 30)
	assert_false(k.drag.undo.can_undo())


func test_freed_item_is_skipped() -> void:
	var a: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 100.0, 30.0)
	var b: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 400.0, 30.0)
	k.drag_pivot_to(b, Vector2(450.0, 50.0))
	k.drag_pivot_to(a, Vector2(200.0, 50.0))
	a.free()
	assert_true(k.drag.undo.undo(), "überspringt gelöschtes Item und macht den Apfel rückgängig")
	assert_almost_eq(b.position, Vector2(400.0, 30.0), Vector2(0.01, 0.01))


func test_undo_on_empty_is_false() -> void:
	assert_false(UndoStack.new().undo())


func test_undo_button_state() -> void:
	var btn := UndoButton.new()
	add_child_autofree(btn)
	btn.undo = k.drag.undo
	assert_true(btn.disabled, "nichts zum Rückgängigmachen → grau")
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 100.0, 30.0)
	k.drag_pivot_to(ball, Vector2(300.0, 40.0))
	assert_false(btn.disabled)
	btn.pressed.emit()
	assert_true(btn.disabled)
	assert_almost_eq(ball.position, Vector2(100.0, 30.0), Vector2(0.01, 0.01))
	assert_gte(btn.custom_minimum_size.x, UiConstants.MIN_TOUCH_DP)
