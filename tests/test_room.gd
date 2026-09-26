extends GutTest
## Raum aus Daten + eingemessener Hintergrund (Regel S-10).

const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")
var room: Room


func before_each() -> void:
	room = ROOM_SCENE.instantiate()
	add_child_autofree(room)
	room.setup(Room.find_room(Room.load_area("res://data/areas/test_kitchen.json"), "kitchen"))


func test_counter_is_90cm() -> void:
	var counter: Surface = room.get_surface(&"counter_top")
	assert_not_null(counter)
	assert_almost_eq(counter.h_cm, 90.0, 2.0)
	assert_almost_eq(counter.top_y(), -90.0, 2.0)


func test_background_calibrated_counter_pixel_is_90cm() -> void:
	# Arbeitsplatte im Quellbild bei px 434 → muss in der Welt bei y = −90 cm (±2) liegen.
	var meta: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(room.data["background"]))
	var cal: Dictionary = room.data["calibration"]
	var k: float = float(meta["px_per_cm"]) / float(meta["source_px_per_cm"])
	var out_px_y: float = (float(cal["px_top"]) - float(cal["crop_px"][1])) * k
	var world_y: float = room.background.position.y + out_px_y * room.background.scale.y
	assert_almost_eq(world_y, -90.0, 2.0)


func test_background_has_tiles_within_limit() -> void:
	assert_gt(room.background.get_child_count(), 0)
	for s: Sprite2D in room.background.get_children():
		assert_true(s.texture.get_width() <= 2048 and s.texture.get_height() <= 2048)


func test_surfaces_sorted_top_down() -> void:
	var list: Array[Surface] = room.surfaces_at_x(200.0)
	assert_gt(list.size(), 1)
	for i: int in range(1, list.size()):
		assert_lt(list[i - 1].top_y(), list[i].top_y())


func test_camera_bounds_include_floor() -> void:
	var b: Rect2 = room.camera_bounds()
	assert_gt(b.end.y, room.floor_band.front_y_cm)
	assert_almost_eq(b.size.x, room.width_cm, 0.01)


func test_ysort_enabled() -> void:
	assert_true(room.ysort_root.y_sort_enabled)
