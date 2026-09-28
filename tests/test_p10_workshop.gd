extends GutTest
## P10h Werkstatt: Daten, Hupe, Hebebühne hebt das Auto (Bild), Reifenwechsel, Lackieren (Farbvariante),
## Waschanlage, Tanken, Schrottplatz-Schatz.

var k: KitchenFixture
var fake: AreaScene


func before_each() -> void:
	NpcBrain.autonomous = false
	Settings.reduced_motion = true
	k = KitchenFixture.new(self)
	fake = AreaScene.new()
	fake.room = k.room


func after_each() -> void:
	Settings.reduced_motion = false
	fake.free()


func after_all() -> void:
	NpcBrain.autonomous = true


func _car(x: float = 500.0) -> ItemNode:
	return ItemSpawner.on_floor(k.room, &"veh_car_hatch_sky", x, 30.0)


func test_workshop_area_has_six_rooms_npcs_and_secrets() -> void:
	var d: Dictionary = Room.load_area(Areas.path_of(&"workshop"))
	assert_eq(Array(d["rooms"]).size(), 6)
	assert_eq(NpcRoles.npcs_of("workshop").size(), 5)
	assert_eq(Secrets.for_area("workshop").size(), 7)
	assert_true(Areas.is_ready(&"workshop"))


func test_tapping_a_car_honks() -> void:
	AudioBus.history.clear()
	assert_true(AreaActions.on_tapped(fake, _car()))
	assert_true(AudioBus.history.has("bus_horn"))


func test_lift_raises_the_car_picture_and_lowers_it_again() -> void:
	var l: ItemNode = ItemSpawner.on_floor(k.room, &"garage_car_lift_coral", 500.0, 25.0)
	var car: ItemNode = _car(500.0)
	var y0: float = car.sprite.position.y
	l.on_tap()
	assert_eq(l.state, "up")
	assert_true(AreaActions.on_tapped(fake, l))
	assert_almost_eq(car.sprite.position.y, y0 - WorkshopActions.LIFT_UP_CM, 0.01, "Auto oben")
	assert_eq(car.position, Vector2(500.0, car.position.y), "gespeicherter Standplatz bleibt")
	l.on_tap()
	AreaActions.on_tapped(fake, l)
	assert_almost_eq(car.sprite.position.y, y0, 0.01, "wieder unten")


func test_spray_gun_paints_the_car_in_its_colour() -> void:
	_car(500.0)
	var gun: ItemNode = ItemSpawner.on_floor(k.room, &"garage_spray_gun_butter", 720.0, 35.0)
	assert_true(AreaActions.on_dropped(fake, gun))
	var ids: Array = []
	for it: ItemNode in Placement.all_items(k.room):
		ids.append(String(it.def.id))
	assert_true(ids.has("veh_car_hatch_butter"), "gleiches Modell, neue Farbe")
	assert_false(ids.has("veh_car_hatch_sky"))


func test_tire_change_and_wash() -> void:
	var car: ItemNode = _car(500.0)
	var tire: ItemNode = ItemSpawner.on_floor(k.room, &"work_tire_summer_black", 720.0, 35.0)
	assert_true(AreaActions.on_dropped(fake, tire), "Reifen gewechselt")
	assert_null(tire.get_parent())
	var tunnel: ItemNode = ItemSpawner.on_floor(k.room, &"garage_wash_tunnel_sky", 500.0, 25.0)
	AreaActions.on_dropped(fake, car)
	assert_eq(tunnel.state, "on", "Waschanlage läuft, wenn ein Auto hineinfährt")


func test_scrap_pile_hides_a_golden_hubcap() -> void:
	var pile: ItemNode = ItemSpawner.on_floor(k.room, &"garage_scrap_pile_rust", 400.0, 20.0)
	pile.on_tap()
	assert_eq(pile.state, "found")
	assert_true(AreaActions.on_tapped(fake, pile))
	var found: bool = false
	for it: ItemNode in Placement.all_items(k.room):
		found = found or String(it.def.id) == "garage_hubcap_gold"
	assert_true(found, "Schatz liegt vor dem Schrotthaufen")
