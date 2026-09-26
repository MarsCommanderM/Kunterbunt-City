extends GutTest
## Stapeln (max. 8, nur „stackable“) und Behälter (Plätze, Größe, Schachtelung ≤ 2).

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func _stack(n: int, x: float = 300.0) -> Array[ItemNode]:
	var out: Array[ItemNode] = []
	var p: ItemNode = ItemSpawner.on_floor(k.room, &"kitchen_plate_1", x, 40.0)
	out.append(p)
	for i: int in n - 1:
		p = ItemSpawner.on_item(p, &"kitchen_plate_2", 0.0, true)
		out.append(p)
	return out


func test_plate_stacks_on_plate() -> void:
	var base: Array[ItemNode] = _stack(1)
	var plate: ItemNode = ItemSpawner.on_floor(k.room, &"kitchen_plate_3", 100.0, 40.0)
	var t: Placement.Target = k.drag_pivot_to(plate, Vector2(302.0, base[0].top_global_y(true) - 6.0))
	assert_eq(t.kind, &"stack")
	assert_eq(plate.get_parent(), base[0].on_top_root)
	assert_almost_eq(plate.global_position.x, base[0].global_position.x, 0.01, "Stapel wird zentriert")
	assert_almost_eq(plate.global_position.y, base[0].top_global_y(true), 0.01)


func test_drop_on_stack_goes_to_the_top() -> void:
	var s: Array[ItemNode] = _stack(4)
	var plate: ItemNode = ItemSpawner.on_floor(k.room, &"kitchen_plate_3", 100.0, 40.0)
	k.drag_pivot_to(plate, Vector2(300.0, s[3].top_global_y(true) - 2.0))
	assert_eq(plate.get_parent(), s[3].on_top_root)
	assert_eq(plate.stack_depth_below(), 5)


func test_stack_max_8() -> void:
	var s: Array[ItemNode] = _stack(8)
	assert_eq(s[7].stack_depth_below(), 8)
	var plate: ItemNode = ItemSpawner.on_floor(k.room, &"kitchen_plate_3", 100.0, 40.0)
	var t: Placement.Target = k.drag_pivot_to(plate, Vector2(300.0, s[7].top_global_y(true) - 2.0))
	assert_eq(t.kind, &"floor", "9. Teller passt nicht mehr")
	assert_string_contains(t.rejected_reason, "Stapel")


func test_non_stackable_does_not_stack() -> void:
	var s: Array[ItemNode] = _stack(1)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 100.0, 40.0)
	var t: Placement.Target = Placement.find_target(k.room, apple, Vector2(300.0, s[0].top_global_y(true) - 2.0), Vector2(300, -10))
	assert_ne(t.kind, &"stack")


func test_dragging_bottom_takes_whole_stack() -> void:
	var s: Array[ItemNode] = _stack(3)
	k.drag_pivot_to(s[0], Vector2(500.0, 60.0))
	assert_almost_eq(s[2].global_position.x, 500.0, 0.01)
	assert_eq(s[2].stack_depth_below(), 3)


func test_taking_middle_splits_stack() -> void:
	var s: Array[ItemNode] = _stack(3)
	k.drag_pivot_to(s[1], Vector2(500.0, 60.0))
	assert_eq(s[1].get_parent(), k.room.ysort_root)
	assert_eq(s[2].get_parent(), s[1].on_top_root, "oberer Teller kommt mit")
	assert_false(s[0].has_stacked_child())


func test_tap_opens_and_closes_backpack() -> void:
	var bag: ItemNode = ItemSpawner.on_floor(k.room, &"item_backpack", 300.0, 40.0)
	assert_false(bag.is_open)
	k.tap(bag)
	assert_true(bag.is_open)
	assert_true(bag.contents_root.visible)
	k.tap(bag)
	assert_false(bag.is_open)


func test_drop_into_open_backpack() -> void:
	var bag: ItemNode = ItemSpawner.on_floor(k.room, &"item_backpack", 300.0, 40.0)
	bag.set_open(true)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 100.0, 40.0)
	var c: Vector2 = bag.global_rect().get_center()
	var t: Placement.Target = k.drag_pivot_to(apple, c)
	assert_eq(t.kind, &"container")
	assert_eq(apple.get_parent(), bag.contents_root)
	assert_eq(apple.slot_index, 0)
	bag.set_open(false)
	assert_false(apple.is_visible_in_tree(), "zu → Inhalt unsichtbar")
	assert_ne(k.drag.pick_item(c), apple, "Inhalt eines geschlossenen Behälters ist nicht greifbar")


func test_closed_backpack_does_not_swallow_items() -> void:
	var bag: ItemNode = ItemSpawner.on_floor(k.room, &"item_backpack", 300.0, 40.0)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 100.0, 40.0)
	var t: Placement.Target = k.drag_pivot_to(apple, bag.global_rect().get_center())
	assert_ne(t.kind, &"container")


func test_too_big_for_backpack() -> void:
	var bag: ItemNode = ItemSpawner.on_floor(k.room, &"item_backpack", 300.0, 40.0)
	bag.set_open(true)
	var teddy: ItemNode = ItemSpawner.on_floor(k.room, &"toy_teddy_brown", 100.0, 40.0)   # 30 cm > 25
	var t: Placement.Target = k.drag_pivot_to(teddy, bag.global_rect().get_center())
	assert_eq(t.kind, &"floor")
	assert_string_contains(t.rejected_reason, "zu groß")


func test_backpack_full() -> void:
	var bag: ItemNode = ItemSpawner.on_floor(k.room, &"item_backpack", 300.0, 40.0)
	bag.set_open(true)
	for i: int in bag.def.container_slots:
		assert_not_null(ItemSpawner.into_container(bag, &"food_egg"))
	assert_eq(bag.free_slot(), -1)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 100.0, 40.0)
	var t: Placement.Target = k.drag_pivot_to(apple, bag.global_rect().get_center())
	assert_string_contains(t.rejected_reason, "voll")


func test_contents_in_real_size_never_overlap_or_stick_out() -> void:
	var bag: ItemNode = ItemSpawner.on_floor(k.room, &"item_backpack", 300.0, 40.0)
	bag.set_open(true)
	for id: StringName in [&"item_book_2", &"food_toast", &"food_apple_red", &"food_egg", &"food_banana", &"food_cheese"]:
		assert_not_null(ItemSpawner.into_container(bag, id))
	var panel: Rect2 = (bag.contents_root as ItemNode.ContentsPanel).rect
	var rects: Array[Rect2] = []
	for c: Node in bag.contents_root.get_children():
		var it: ItemNode = c
		assert_almost_eq(it.global_rect().size.y, it.def.height_cm * bag.global_scale.y, 0.01, "echte Größe: %s" % it.def.id)
		var r := Rect2(it.position + it.local_rect().position, it.draw_size())
		assert_true(panel.grow(0.01).encloses(r), "%s liegt in der Innenfläche" % it.def.id)
		for o: Rect2 in rects:
			assert_false(o.grow(-0.01).intersects(r.grow(-0.01)), "%s überlappt" % it.def.id)
		rects.append(r)
	assert_gte(panel.size.x, bag.interior_rect().size.x)


func test_taking_item_out_reflows_rest() -> void:
	var bag: ItemNode = ItemSpawner.on_floor(k.room, &"item_backpack", 300.0, 40.0)
	bag.set_open(true)
	var a: ItemNode = ItemSpawner.into_container(bag, &"food_apple_red")
	var b: ItemNode = ItemSpawner.into_container(bag, &"food_egg")
	var b_before: Vector2 = b.position
	k.drag_pivot_to(a, Vector2(600.0, 60.0))
	assert_lt(b.position.x, b_before.x, "Ei rutscht nach links auf den freien Platz")


func test_nesting_max_two_levels() -> void:
	var fridge: ItemNode = ItemSpawner.on_floor(k.room, &"fix_fridge", 300.0, 1.0)
	fridge.set_open(true)
	var box_def: ItemDefinition = ItemDB.get_item(&"item_bucket").duplicate()
	box_def.height_cm = 10.0
	var box: ItemNode = ItemNode.create(box_def)
	fridge.contents_root.add_child(box)
	box.slot_index = 0
	fridge.relayout_contents()
	box.set_open(true)
	var box2: ItemNode = ItemNode.create(box_def)
	k.room.ysort_root.add_child(box2)
	box2.position = Vector2(100, 40)
	var t: Placement.Target = Placement.find_target(k.room, box2, box.global_rect().get_center(), box.global_rect().get_center())
	assert_eq(t.kind, &"floor")
	assert_string_contains(t.rejected_reason, "2 Ebenen")


func test_each_plate_in_stack_is_grabbable() -> void:
	var s: Array[ItemNode] = _stack(3)
	for i: int in 3:
		assert_eq(k.drag.pick_item(s[i].global_rect().get_center()), s[i], "Teller %d" % i)
