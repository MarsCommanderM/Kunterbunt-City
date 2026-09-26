extends GutTest
## Pflicht-Test (Tech-Spec §6, Maßstab-Bibel): JEDES Item wird exakt so groß gezeichnet wie in der Tabelle –
## und die Verhältnisse stimmen („eine Karotte ist kein Baseballschläger, der Hund nicht größer als der Tisch“).

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func test_every_item_drawn_at_table_height() -> void:
	for id: StringName in ItemDB.item_ids():
		var it: ItemNode = ItemSpawner.on_floor(k.room, id, 300.0, 0.0)   # hinten: Tiefen-Faktor 1,0
		assert_almost_eq(it.global_rect().size.y, ItemDB.get_item(id).height_cm, 0.01, String(id))
		it.free()


func test_every_item_keeps_ratio_in_front() -> void:
	for id: StringName in ItemDB.item_ids():
		var it: ItemNode = ItemSpawner.on_floor(k.room, id, 300.0, 500.0)  # ganz vorne: ×1,12
		assert_almost_eq(it.global_rect().size.y, ItemDB.get_item(id).height_cm * 1.12, 0.02, String(id))
		it.free()


func test_size_order_is_believable() -> void:
	var order: Array[StringName] = [&"food_egg", &"food_apple_red", &"home_mug_pink_dots", &"food_carrot",
		&"toy_teddy_brown", &"pet_dog_brown", &"home_table_wood", &"home_chair_mint", &"fix_fridge"]
	var prev: float = 0.0
	for id: StringName in order:
		var h: float = ItemSpawner.make(id).draw_size().y
		assert_gt(h, prev, "%s muss größer sein als sein Vorgänger" % id)
		prev = h


func test_item_on_table_same_scale_as_table() -> void:
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 400.0, 60.0)
	var apple: ItemNode = ItemSpawner.on_item(table, &"food_apple_red")
	assert_almost_eq(apple.global_rect().size.y / table.global_rect().size.y, 8.0 / 75.0, 0.0001)


func test_dragging_keeps_size_except_depth() -> void:
	var dog: ItemNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 200.0, 0.0)
	k.drag_pivot_to(dog, Vector2(500.0, 73.2))
	assert_almost_eq(dog.global_rect().size.y, 45.0 * k.room.floor_band.depth_factor(73.2), 0.01)
	assert_lte(dog.global_rect().size.y, 45.0 * 1.12 + 0.01, "nie größer als ×1,12")
