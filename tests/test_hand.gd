extends GutTest
## Pflicht-Test (Tech-Spec §6): Items in die Hand – Grip exakt auf dem HandSlot, Rotation aus hold_angle,
## Zeichenreihenfolge Arm < Item < Hand, eine Hand / zwei Hände, Größe bleibt maßstäblich.

var k: KitchenFixture
var kid: CharacterRig
var adult: CharacterRig
var girl: SpriteCharacter


func before_each() -> void:
	k = KitchenFixture.new(self)
	kid = ItemSpawner.character_on_floor(k.room, "kid", 300.0, 60.0)
	adult = ItemSpawner.character_on_floor(k.room, "adult", 420.0, 60.0)
	girl = ItemSpawner.character_on_floor(k.room, "char_girl_01", 520.0, 60.0)


func _give(item: ItemNode, who: ItemNode, index: int) -> Placement.Target:
	var slot: Dictionary = {}
	for h: Dictionary in who.hand_slots():
		if int(h["index"]) == index:
			slot = h
	assert_false(slot.is_empty(), "Hand %d ist frei" % index)
	var grip: Vector2 = PlacementCharacter.grip_global(item, Vector2.ZERO)
	return k.drag_pivot_to(item, (slot["global"] as Vector2) - grip, 3)


func test_carrot_lands_exactly_in_hand() -> void:
	var carrot: ItemNode = ItemSpawner.on_floor(k.room, &"food_carrot", 200.0, 40.0)
	var t: Placement.Target = _give(carrot, girl, 0)
	assert_eq(t.kind, &"hand")
	var d: float = carrot.to_global((carrot.def.grip - carrot.def.pivot) * carrot.draw_size()) \
		.distance_to(girl.slot_front.global_position)
	assert_almost_eq(d, 0.0, 0.05, "Griffpunkt sitzt auf der Hand (±0,5 mm)")


func test_held_item_keeps_its_size_and_rotation() -> void:
	var carrot: ItemNode = ItemSpawner.on_floor(k.room, &"food_carrot", 200.0, 40.0)
	var before: Vector2 = carrot.draw_size()
	_give(carrot, girl, 0)
	assert_almost_eq(carrot.draw_size().y, before.y, 0.01, "Karotte bleibt 20 cm groß")
	assert_almost_eq(carrot.global_rotation, deg_to_rad(carrot.def.hold_angle), 0.001,
		"Haltewinkel aus der Item-Definition")


func test_draw_order_arm_item_hand() -> void:
	var carrot: ItemNode = ItemSpawner.on_floor(k.room, &"food_carrot", 200.0, 40.0)
	_give(carrot, kid, 0)
	var arm: Node2D = kid.arm_front
	var kids: Array = arm.get_children()
	var i_slot: int = kids.find(kid.slot_front)
	var i_skin: int = kids.find(kid._layers["ArmFrontSkin"])
	var i_hand: int = kids.find(kid._layers["ArmFrontFingers"])
	assert_true(i_skin < i_slot and i_slot < i_hand, "Zeichenreihenfolge: Arm < Item < Hand-Finger")
	assert_eq(carrot.get_parent(), kid.slot_front, "Item hängt im HandSlot des Arms")
	# Finger-Ebene des vorderen Arms ist sichtbar und liegt über dem Item
	assert_true(kid._layers["ArmFrontFingers"].visible)


func test_two_hand_item_uses_both_hands() -> void:
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"toy_beachball", 200.0, 40.0)
	assert_eq(ball.def.hold, "two_hands")
	var t: Placement.Target = _give(ball, adult, 2)
	assert_eq(t.kind, &"hand")
	assert_eq(ball.get_parent(), adult.slot_two, "Ball liegt im Zwei-Hand-Slot")
	assert_true(adult.hand_slots().is_empty(), "beide Hände sind belegt")
	# Hände sitzen links und rechts am Ball (Abstand ≈ Ballbreite)
	var spread: float = absf(adult.slot_front.global_position.x - adult.slot_back.global_position.x)
	assert_almost_eq(spread, ball.def.width_cm * ball.global_scale.x, 4.0, "Hände greifen seitlich")


func test_one_hand_item_cannot_use_two_hand_slot() -> void:
	var carrot: ItemNode = ItemSpawner.on_floor(k.room, &"food_carrot", 200.0, 40.0)
	assert_eq(carrot.def.hold, "one_hand")
	var t: Placement.Target = _give(carrot, adult, 0)
	assert_eq(t.kind, &"hand")
	assert_eq(carrot.get_parent(), adult.slot_front)
	assert_eq(adult.held_item(1), null, "hintere Hand bleibt frei")


func test_held_item_travels_with_the_character() -> void:
	var carrot: ItemNode = ItemSpawner.on_floor(k.room, &"food_carrot", 200.0, 40.0)
	_give(carrot, girl, 0)
	var before: Vector2 = carrot.global_position
	k.drag_pivot_to(girl, Vector2(120.0, 30.0), 4)
	assert_true(carrot.global_position.distance_to(before) > 50.0, "Karotte wandert mit")
	var d: float = carrot.to_global((carrot.def.grip - carrot.def.pivot) * carrot.draw_size()) \
		.distance_to(girl.slot_front.global_position)
	assert_almost_eq(d, 0.0, 0.05, "und bleibt in der Hand")


func test_sprite_character_hand_overlay_only_while_holding() -> void:
	assert_false(girl.hand_overlay.visible, "leere Hand zeigt keine Faust")
	var carrot: ItemNode = ItemSpawner.on_floor(k.room, &"food_carrot", 200.0, 40.0)
	_give(carrot, girl, 0)
	assert_true(girl.hand_overlay.visible, "Faust liegt über dem Item")
	var ov: Sprite2D = girl.hand_overlay
	assert_true((ov.global_transform * ov.get_rect()).intersects(carrot.global_rect()),
		"Finger überdecken die Karotte")


func test_food_at_mouth_is_eaten() -> void:
	var ice: ItemNode = ItemSpawner.on_floor(k.room, &"food_icecream_3", 200.0, 40.0)
	var mouth: Vector2 = kid.mouth_global()
	k.drag_pivot_to(ice, mouth - (ice.global_rect().get_center() - ice.global_position), 5)
	assert_true(ice.is_queued_for_deletion(), "Eis ist weg")
	assert_eq(kid.emotion, "love", "Gesicht reagiert auf Essen")
