extends GutTest
## Kamera: 300 cm sichtbar (±2), Zoomgrenzen, bleibt im Raum.

const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")
var room: Room
var cam: WorldCamera


func before_each() -> void:
	room = ROOM_SCENE.instantiate()
	add_child_autofree(room)
	room.setup(Room.find_room(Room.load_area("res://data/areas/test_kitchen.json"), "kitchen"))
	cam = WorldCamera.new()
	add_child_autofree(cam)
	cam.setup_for_room(room)


func test_default_shows_300cm() -> void:
	assert_almost_eq(cam.view_size().y, 300.0, 2.0)


func test_zoom_is_clamped() -> void:
	cam.set_visible_height(50.0)
	assert_almost_eq(cam.visible_h_cm, 220.0, 0.01)
	cam.set_visible_height(5000.0)
	assert_almost_eq(cam.visible_h_cm, 400.0, 0.01)


func test_stays_inside_room() -> void:
	cam.pan_by_screen(Vector2(100000, 100000))
	var r: Rect2 = cam.visible_rect()
	var b: Rect2 = room.camera_bounds()
	assert_true(r.position.x >= b.position.x - 0.01, "links")
	assert_true(r.position.y >= b.position.y - 0.01, "oben")
	cam.pan_by_screen(Vector2(-100000, -100000))
	r = cam.visible_rect()
	assert_true(r.end.x <= b.end.x + 0.01, "rechts")
	assert_true(r.end.y <= b.end.y + 0.01, "unten")


func test_starts_with_floor_visible() -> void:
	assert_gt(cam.visible_rect().end.y, room.floor_band.front_y_cm)


func test_zoom_keeps_anchor_under_finger() -> void:
	cam.set_visible_height(300.0)
	var anchor: Vector2 = cam.screen_to_world(cam.viewport_px() * 0.5 + Vector2(100, 0))
	var screen_before: Vector2 = cam.world_to_screen(anchor)
	cam.zoom_by(1.2, anchor)
	assert_almost_eq(cam.world_to_screen(anchor).x, screen_before.x, 1.0)


func test_fling_stops_by_itself() -> void:
	cam.set_visible_height(300.0)
	cam.fling(Vector2(400, 0))
	assert_true(cam.is_gliding())
	await wait_seconds(1.5)
	assert_false(cam.is_gliding(), "Trägheit muss auslaufen")


# --- Eingaben wie vom Spieler (Maus + Touch-Emulation) ---

func test_mouse_wheel_zooms_in() -> void:
	cam.set_visible_height(300.0)
	var e := InputEventMouseButton.new()
	e.button_index = MOUSE_BUTTON_WHEEL_UP
	e.pressed = true
	e.position = cam.viewport_px() * 0.5
	cam._unhandled_input(e)
	assert_lt(cam.visible_h_cm, 300.0)


func test_mouse_drag_scrolls() -> void:
	cam.set_visible_height(300.0)
	var x0: float = cam.position.x
	var down := InputEventMouseButton.new()
	down.button_index = MOUSE_BUTTON_LEFT
	down.pressed = true
	cam._unhandled_input(down)
	var move := InputEventMouseMotion.new()
	move.relative = Vector2(-200, 0)
	cam._unhandled_input(move)
	assert_gt(cam.position.x, x0, "Maus nach links ziehen → Welt nach rechts")


func test_touch_one_finger_scrolls() -> void:
	var x0: float = cam.position.x
	cam._unhandled_input(_touch(0, Vector2(900, 500), true))
	cam._unhandled_input(_drag(0, Vector2(700, 500)))
	assert_gt(cam.position.x, x0)


func test_touch_pinch_zooms() -> void:
	cam.set_visible_height(300.0)
	cam._unhandled_input(_touch(0, Vector2(800, 500), true))
	cam._unhandled_input(_touch(1, Vector2(1000, 500), true))
	cam._unhandled_input(_drag(1, Vector2(1000, 500)))
	cam._unhandled_input(_drag(1, Vector2(1200, 500)))   # Finger auseinander → reinzoomen
	assert_lt(cam.visible_h_cm, 300.0)


func _touch(i: int, p: Vector2, down: bool) -> InputEventScreenTouch:
	var e := InputEventScreenTouch.new()
	e.index = i
	e.position = p
	e.pressed = down
	return e


func _drag(i: int, p: Vector2) -> InputEventScreenDrag:
	var e := InputEventScreenDrag.new()
	e.index = i
	e.position = p
	return e
