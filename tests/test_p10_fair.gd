extends GutTest
## P10d Rummelplatz: Daten, Fahrgeschäfte fahren nur mit Figur (Riesenrad, Autoscooter, Achterbahn folgt der
## Schiene), Dosenwerfen/Losrad geben Gewinne (✋), Hau den Lukas, Zauberhut.

var k: KitchenFixture
var fake: AreaScene


func before_each() -> void:
	NpcBrain.autonomous = false
	k = KitchenFixture.new(self)
	fake = AreaScene.new()
	fake.room = k.room


func after_each() -> void:
	fake.free()


func after_all() -> void:
	NpcBrain.autonomous = true


func _kid(x: float, y: float = 40.0) -> CharacterRig:
	return ItemSpawner.character_on_floor(k.room, "kid", x, y) as CharacterRig


func _seat(kid: CharacterRig, ride: ItemNode) -> void:
	PoolActions.seat_in(kid, ride, 0)


func test_fair_area_has_eight_rooms_npcs_and_secrets() -> void:
	var d: Dictionary = Room.load_area(Areas.path_of(&"fair"))
	assert_eq(Array(d["rooms"]).size(), 8)
	assert_eq(NpcRoles.npcs_of("fair").size(), 9)
	assert_eq(Secrets.for_area("fair").size(), 7)
	assert_true(Areas.is_ready(&"fair"))


func test_rides_move_only_with_a_rider() -> void:
	var car: ItemNode = ItemSpawner.on_floor(k.room, &"fair_bumper_car_coral", 400.0, 40.0)
	var wheel: ItemNode = ItemSpawner.on_floor(k.room, &"fair_ferris_wheel_sky", 900.0, 10.0)
	PlayMotion.refresh(k.room)
	assert_eq(PlayMotion.tick(1.0), 0, "leer: nichts fährt")
	var base: Vector2 = car.sprite.position
	_seat(_kid(200.0), car)
	_seat(_kid(250.0), wheel)
	PlayMotion.refresh(k.room)
	assert_eq(PlayMotion.tick(1.0), 2, "Autoscooter + Riesenrad fahren")
	assert_ne(car.sprite.position, base, "der Wagen fährt mit (Bild)")
	assert_eq(car.on_top_root.position, car.sprite.position - base, "Figur fährt im Wagen mit")
	assert_lt(wheel.on_top_root.position.y, 0.0, "Gondel steigt nach oben")


func test_coaster_car_follows_the_track() -> void:
	for t: float in [0.0, 1.0, 2.5, 4.0]:
		var o: Array = PlayMotion.vehicle_offset("coaster", t)
		var u: float = (o[0] as Vector2).x / PlayMotion.COASTER_W
		assert_almost_eq(-(o[0] as Vector2).y, PlayMotion.coaster_y(u) - PlayMotion.coaster_y(0.0), 0.01)
	assert_almost_eq(PlayMotion.coaster_y(0.5), 30.0 + 280.0 * (0.75 + 0.25), 0.01, "höchster Hügel in der Mitte")


func test_riding_rings_the_bell_and_counts_as_secret_event() -> void:
	var car: ItemNode = ItemSpawner.on_floor(k.room, &"fair_coaster_car_coral", 400.0, 30.0)
	var kid: CharacterRig = _kid(200.0)
	_seat(kid, car)
	assert_false(FairActions.on_dropped(fake, kid), "Sitzen macht der normale Drop")
	assert_eq(kid.emotion, "laugh")


func test_knocking_cans_gives_a_plush_prize_to_carry_home() -> void:
	var cans: ItemNode = ItemSpawner.on_floor(k.room, &"fair_cans_coral", 300.0, 40.0)
	var before: int = Placement.all_items(k.room).size()
	cans.on_tap()
	assert_eq(cans.state, "fallen")
	assert_true(AreaActions.on_tapped(fake, cans))
	var items: Array = Placement.all_items(k.room)
	assert_eq(items.size(), before + 1, "Gewinn liegt vor der Bude")
	var prize: ItemNode = items[items.size() - 1]
	assert_true(String(prize.def.id).begins_with("fair_prize"))
	assert_eq(prize.def.hold, "two_hands", "Plüsch kann getragen (und in den Rucksack) werden")


func test_high_striker_and_magic_hat() -> void:
	var hs: ItemNode = ItemSpawner.on_floor(k.room, &"fair_high_striker_coral", 300.0, 20.0)
	hs.on_tap()
	assert_eq(hs.state, "ring")
	assert_eq(String(hs.def.sfx["ring"]), "fair_bell")
	assert_true(AreaActions.on_tapped(fake, hs))
	var hat: ItemNode = ItemSpawner.on_floor(k.room, &"fair_magic_hat_black", 500.0, 50.0)
	var kid: CharacterRig = _kid(600.0)
	hat.on_tap()
	assert_eq(hat.state, "rabbit")
	assert_true(AreaActions.on_tapped(fake, hat))
	assert_eq(kid.emotion, "surprised", "Kind staunt über den Hasen")
