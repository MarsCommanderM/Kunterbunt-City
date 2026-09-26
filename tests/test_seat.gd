extends GutTest
## P03-T05: Sitz- und Liegeplätze. Sitzhöhe aus der Tabelle, Hüfte rastet ein, Pose folgt dem Möbel,
## Spielzeug darf sitzen, Geschirr nicht.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func test_seat_heights_come_from_the_scale_table() -> void:
	var cases: Array = [["home_chair_mint", 45.0], ["home_sofa", 42.0], ["home_armchair", 42.0],
		["home_bed_kid", 45.0], ["home_stool", 45.0]]
	for c: Array in cases:
		var it: ItemNode = ItemSpawner.on_floor(k.room, StringName(c[0]), 300.0, 40.0)
		assert_eq(it.def.seat_h_cm, c[1], "%s: Sitzhöhe" % c[0])
		assert_true(it.def.has_seat())
		var bottom: float = it.global_position.y
		var seat: float = Seats.point_global(it, 0).y
		assert_almost_eq((bottom - seat) / it.global_scale.y, c[1], 0.5, "%s: Sitzpunkt über dem Boden" % c[0])


func test_character_snaps_with_hip_onto_the_seat() -> void:
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"home_chair_mint", 300.0, 45.0)
	var kid: CharacterRig = ItemSpawner.character_on_floor(k.room, "kid", 300.0, 45.0)
	_sit(kid, chair)
	assert_eq(kid.get_parent(), chair.on_top_root, "Figur gehört jetzt zum Stuhl")
	assert_eq(kid.slot_index, 0)
	assert_eq(kid.body_pose, "sit")
	var hip: Vector2 = kid.parts.to_global(Vector2(0, -float(kid.t["hip"]["y"])))
	assert_almost_eq(hip.distance_to(Seats.point_global(chair, 0)), 0.0, 1.0,
		"Hüfte sitzt (nicht die Füße) auf dem Sitzpunkt")


func test_sofa_has_three_places_and_bed_one() -> void:
	var sofa: ItemNode = ItemSpawner.on_floor(k.room, &"home_sofa", 300.0, 30.0)
	var bed: ItemNode = ItemSpawner.on_floor(k.room, &"home_bed_kid", 300.0, 25.0)
	assert_eq(sofa.def.seat_slots, 3)
	assert_eq(bed.def.seat_slots, 1)
	var points: Array = []
	for i: int in 3:
		points.append(Seats.point_global(sofa, i).x)
	assert_true(points[0] < points[1] and points[1] < points[2], "drei Plätze nebeneinander")
	assert_almost_eq((points[2] - points[0]) / sofa.global_scale.x,
		sofa.def.width_cm * 0.7 * 2.0 / 3.0, 1.0, "auf 70 % der Breite verteilt")


func test_two_characters_take_two_different_places() -> void:
	var sofa: ItemNode = ItemSpawner.on_floor(k.room, &"home_sofa", 300.0, 30.0)
	var a: CharacterRig = ItemSpawner.character_on_floor(k.room, "kid", 240.0, 30.0)
	var b: CharacterRig = ItemSpawner.character_on_floor(k.room, "toddler", 360.0, 30.0)
	_sit(a, sofa, 0)
	_sit(b, sofa, 2)
	assert_eq(a.slot_index, 0)
	assert_eq(b.slot_index, 2)
	assert_eq(Seats.occupant(sofa, 0), a)
	assert_eq(Seats.occupant(sofa, 1), null, "mittlerer Platz bleibt frei")
	assert_eq(Seats.occupant(sofa, 2), b)


func test_toy_may_sit_dishes_may_not() -> void:
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"home_chair_mint", 300.0, 45.0)
	var teddy: ItemNode = ItemSpawner.on_floor(k.room, &"toy_teddy_brown", 300.0, 45.0)
	var mug: ItemNode = ItemSpawner.on_floor(k.room, &"kitchen_mug", 320.0, 45.0)
	_sit(teddy, chair)
	assert_eq(teddy.get_parent(), chair.on_top_root, "Teddy darf sitzen")
	assert_almost_eq(_h_over(chair, teddy.global_rect().end.y), 45.0, 1.0, "Teddy sitzt auf 45 cm")
	_sit(mug, chair)
	assert_ne(mug.get_parent(), chair.on_top_root, "Tasse gehört auf die Fläche, nicht auf den Sitz")


func test_pet_may_sit_on_the_sofa() -> void:
	var sofa: ItemNode = ItemSpawner.on_floor(k.room, &"home_sofa", 300.0, 30.0)
	var cat: ItemNode = ItemSpawner.on_floor(k.room, &"pet_cat", 300.0, 30.0)
	_sit(cat, sofa, 1)
	assert_eq(cat.get_parent(), sofa.on_top_root, "Katze darf aufs Sofa")
	assert_almost_eq(_h_over(sofa, cat.global_rect().end.y), 42.0, 1.5, "Sitzhöhe 42 cm")


func test_standing_up_restores_stand_pose() -> void:
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"home_chair_mint", 300.0, 45.0)
	var kid: CharacterRig = ItemSpawner.character_on_floor(k.room, "kid", 300.0, 45.0)
	_sit(kid, chair)
	assert_eq(kid.body_pose, "sit")
	k.drag_pivot_to(kid, Vector2(120.0, 60.0), 8)     # wieder auf den Boden
	assert_eq(kid.body_pose, "stand", "aufgestanden")
	assert_eq(kid.slot_index, -1)
	assert_eq(Seats.occupant(chair, 0), null, "Platz ist wieder frei")


func test_bed_pose_is_lie_chair_pose_is_sit() -> void:
	var bed: ItemNode = ItemSpawner.on_floor(k.room, &"home_bed_kid", 300.0, 25.0)
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"home_chair_mint", 600.0, 45.0)
	var t1: CharacterRig = ItemSpawner.character_on_floor(k.room, "toddler", 300.0, 25.0)
	var t2: CharacterRig = ItemSpawner.character_on_floor(k.room, "kid", 600.0, 45.0)
	_sit(t1, bed)
	_sit(t2, chair)
	assert_eq(t1.body_pose, "lie", "Bett → liegen")
	assert_eq(t2.body_pose, "sit", "Stuhl → sitzen")


# ---------------------------------------------------------------- Hilfen
func _sit(who: ItemNode, host: ItemNode, i: int = 0) -> void:
	var p: Vector2 = Seats.point_global(host, i)
	if who.has_method("hip_offset"):
		p -= who.hip_offset() * who.global_scale.y
	k.drag_pivot_to(who, p, 9)


func _h_over(ref: ItemNode, world_y: float) -> float:
	return (ref.global_position.y - world_y) / ref.global_scale.y
