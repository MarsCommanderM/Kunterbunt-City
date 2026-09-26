extends GutTest
## Abnahme P01: In der Testszene gilt Hund (45) < Tisch (75) < Arbeitsplatte (90) < Kind (125) – gemessen in Welt-cm.

var scene: Node2D


func before_all() -> void:
	scene = load("res://src/debug/scale_test.tscn").instantiate()
	add_child(scene)
	await wait_process_frames(2)


func after_all() -> void:
	scene.free()


func _world_h(ref: String) -> float:
	var b: ScaleBlock = scene.blocks[ref]
	return b.size_cm.y * b.scale.y


func test_dog_lt_table_lt_counter_lt_child() -> void:
	var counter: float = scene.room.get_surface(&"counter_top").h_cm
	assert_lt(_world_h("pet_dog_medium"), _world_h("home_table_dining"))
	assert_lt(_world_h("home_table_dining"), counter)
	assert_lt(counter, _world_h("char_child"))


func test_dog_below_table_top_on_screen_even_in_front() -> void:
	# Hund steht weiter vorne als der Tisch (größerer Tiefen-Faktor) – muss trotzdem kleiner bleiben.
	assert_lt(_world_h("pet_dog_medium"), ItemDB.height_cm("home_table_dining"))


func test_apple_sits_exactly_on_counter() -> void:
	var apple: ScaleBlock = scene.blocks["food_apple"]
	assert_almost_eq(apple.position.y, scene.room.get_surface(&"counter_top").top_y(), 0.5)


func test_apple_much_smaller_than_football() -> void:
	assert_lt(_world_h("food_apple") * 2.0, _world_h("toy_football"))


func test_all_sizes_come_from_table() -> void:
	for ref: String in scene.blocks:
		var b: ScaleBlock = scene.blocks[ref]
		assert_eq(b.size_cm.y, ItemDB.height_cm(ref), ref)
