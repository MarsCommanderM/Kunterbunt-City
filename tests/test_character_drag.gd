extends GutTest
## P03-T06: Figuren ziehen – greifen am Körper, 6 cm anheben, lustiges Pendeln am Griffpunkt,
## Absetzen im Bodenband, Pose dabei „stehen", Rückgängig stellt die Figur zurück.

var k: KitchenFixture
var kid: CharacterRig


func before_each() -> void:
	k = KitchenFixture.new(self)
	kid = ItemSpawner.character_on_floor(k.room, "kid", 300.0, 60.0)


func test_grab_and_drop_moves_the_character() -> void:
	var t: Placement.Target = k.drag_pivot_to(kid, Vector2(150.0, 40.0))
	assert_eq(t.kind, &"floor")
	assert_eq(kid.get_parent(), k.room.ysort_root)
	assert_almost_eq(kid.position.x, 150.0, 0.01)
	assert_almost_eq(kid.scale.y, k.room.floor_band.depth_factor(40.0), 0.0001)


func test_character_is_lifted_6cm_while_dragging() -> void:
	var grab: Vector2 = k.grab_point(kid)
	assert_almost_eq(kid.lifted, 0.0, 0.001)
	k.drag.press(1, grab)
	k.drag.move(1, grab + Vector2(0, -20.0))
	assert_almost_eq(kid.lifted, 1.0, 0.001, "angehoben")
	assert_almost_eq(kid.lift_node().position.y, -ItemNode.LIFT_CM, 0.01,
		"Körper samt Händen lokal 6 cm über dem Boden")
	assert_almost_eq(kid.global_rect().position.y - kid.position.y,
		-(kid.global_rect().size.y + ItemNode.LIFT_CM * kid.global_scale.y), 2.0,
		"in der Welt 6 cm × Tiefen-Faktor angehoben")
	k.drag.release(1, grab + Vector2(0, -20.0))
	assert_almost_eq(kid.lifted, 0.0, 0.001, "wieder abgesetzt")


func test_pose_is_stand_while_carried() -> void:
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"home_chair_mint", 300.0, 45.0)
	_sit(chair)
	assert_eq(kid.body_pose, "sit")
	k.drag_pivot_to(kid, Vector2(150.0, 60.0), 2)
	assert_eq(kid.body_pose, "stand", "beim Tragen wird die Figur gerade gezogen")


func test_swings_while_dragged_and_calms_down_afterwards() -> void:
	var grab: Vector2 = k.grab_point(kid)
	k.drag.press(3, grab)
	k.drag.move(3, grab + Vector2(0, -40.0))
	for i: int in 10:
		k.drag.move(3, grab + Vector2(i * 14.0, -60.0))
		k.drag._process(1.0 / 60.0)
	assert_true(absf(kid.swing.rotation) > 0.05, "pendelt (%.3f rad)" % kid.swing.rotation)
	assert_true(absf(kid.swing.rotation) < 0.7, "aber nicht überschlagen")
	k.drag.release(3, grab + Vector2(140.0, 20.0))
	assert_almost_eq(kid.swing.rotation, 0.0, 0.001, "Pendel steht wieder gerade")


func test_held_item_comes_along_when_character_is_dropped() -> void:
	var carrot: ItemNode = ItemSpawner.on_floor(k.room, &"food_carrot", 200.0, 40.0)
	var slot: Dictionary = kid.hand_slots()[0]
	k.drag_pivot_to(carrot, (slot["global"] as Vector2) - PlacementCharacter.grip_global(carrot, Vector2.ZERO), 4)
	assert_eq(kid.held_item(0), carrot)
	k.drag_pivot_to(kid, Vector2(500.0, 30.0), 5)
	assert_almost_eq(carrot.to_global((carrot.def.grip - carrot.def.pivot) * carrot.draw_size())
		.distance_to(kid.slot_front.global_position), 0.0, 0.05, "Karotte bleibt in der Hand")


func test_undo_puts_the_character_back() -> void:
	var before: Vector2 = kid.position
	k.drag_pivot_to(kid, Vector2(150.0, 40.0))
	assert_ne(kid.position, before)
	k.drag.undo.undo()
	assert_almost_eq(kid.position.x, before.x, 0.01, "Rückgängig: zurück auf den alten Platz")
	assert_almost_eq(kid.position.y, before.y, 0.01)
	assert_almost_eq(kid.scale.y, k.room.floor_band.depth_factor(before.y), 0.0001, "alte Tiefe")


func test_characters_cannot_be_put_into_hands() -> void:
	var adult: CharacterRig = ItemSpawner.character_on_floor(k.room, "adult", 400.0, 60.0)
	var slot: Dictionary = adult.hand_slots()[0]
	var t: Placement.Target = k.drag_pivot_to(kid, slot["global"] as Vector2, 6)
	assert_ne(t.kind, &"hand", "Figuren trägt man nicht in der Hand")
	assert_ne(kid.get_parent(), adult.slot_front)


func test_drop_outside_the_band_is_clamped() -> void:
	k.drag_pivot_to(kid, Vector2(300.0, 500.0))
	assert_true(k.room.floor_band.contains(kid.position), "Figur bleibt im Bodenband: %s" % kid.position)


func _sit(chair: ItemNode) -> void:
	var p: Vector2 = Seats.point_global(chair, 0) - kid.hip_offset() * kid.global_scale.y
	k.drag_pivot_to(kid, p, 7)
