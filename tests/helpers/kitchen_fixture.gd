class_name KitchenFixture
extends RefCounted
## Gemeinsamer Test-Aufbau: echte Test-Küche + DragController ohne Animation (deterministisch).

const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")

var room: Room
var drag: DragController


func _init(test: GutTest) -> void:
	room = ROOM_SCENE.instantiate()
	test.add_child_autofree(room)
	room.setup(Room.find_room(Room.load_area("res://data/areas/test_kitchen.json"), "kitchen"))
	drag = DragController.new()
	drag.animate = false
	test.add_child_autofree(drag)
	drag.attach_room(room)


## Greift das Item in der Mitte und zieht es so, dass sein Pivot bei `pivot_target` landet.
func drag_pivot_to(item: ItemNode, pivot_target: Vector2, id: int = 0) -> Placement.Target:
	var grab: Vector2 = grab_point(item)
	var offset: Vector2 = item.global_position - grab
	var result: Array = []
	var cb := func(_it: ItemNode, t: Placement.Target) -> void: result.append(t)
	drag.item_dropped.connect(cb)
	drag.press(id, grab)
	drag.move(id, grab + Vector2(0, -20))
	drag.move(id, pivot_target - offset)
	drag.release(id, pivot_target - offset)
	drag.item_dropped.disconnect(cb)
	return result[0] if not result.is_empty() else null


## Tippen (ohne Bewegung).
func tap(item: ItemNode, id: int = 0) -> void:
	var p: Vector2 = grab_point(item)
	drag.press(id, p)
	drag.release(id, p)



func grab_point(item: ItemNode) -> Vector2:
	return drag.grab_point(item)
