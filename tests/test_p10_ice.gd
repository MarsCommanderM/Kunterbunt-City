extends GutTest
## P10f Eishalle: Daten, Gleiten mit Schwung (begrenzt auf die Eisfläche), Pirouette, Kratzer → Eismaschine → glänzt,
## Eishockey (Puck ins Tor), Discokugel färbt das Licht, Schlittschuhe anziehen.

var k: KitchenFixture
var fake: AreaScene


func before_each() -> void:
	NpcBrain.autonomous = false
	Settings.reduced_motion = true
	k = KitchenFixture.new(self)
	fake = AreaScene.new()
	fake.room = k.room
	IceActions._glides = 0
	IceActions._timer = 0.0


func after_each() -> void:
	Settings.reduced_motion = false
	fake.free()


func after_all() -> void:
	NpcBrain.autonomous = true


func _kid(x: float, y: float = 40.0) -> CharacterRig:
	return ItemSpawner.character_on_floor(k.room, "kid", x, y) as CharacterRig


func _ice() -> ItemNode:
	return ItemSpawner.on_floor(k.room, &"ice_surface_white", 600.0, 40.0)


func test_ice_area_has_four_rooms_npcs_and_secrets() -> void:
	var d: Dictionary = Room.load_area(Areas.path_of(&"ice"))
	assert_eq(Array(d["rooms"]).size(), 4)
	assert_eq(NpcRoles.npcs_of("ice").size(), 4)
	assert_eq(Secrets.for_area("ice").size(), 6)
	assert_true(Areas.is_ready(&"ice"))


func test_figure_glides_with_momentum_and_stays_on_the_ice() -> void:
	var ice: ItemNode = _ice()
	var kid: CharacterRig = _kid(400.0)
	kid.set_meta("drop_velocity", Vector2(400.0, 0.0))
	assert_true(AreaActions.on_dropped(fake, kid), "gleitet")
	assert_almost_eq(kid.position.x, 400.0 + 160.0, 0.5, "Schwung 400 cm/s → 160 cm")
	kid.set_meta("drop_velocity", Vector2(5000.0, 0.0))
	AreaActions.on_dropped(fake, kid)
	assert_lte(kid.position.x, ice.position.x + ice.def.width_cm * 0.5, "nie über die Eisfläche hinaus")


func test_no_momentum_is_a_pirouette_off_the_ice_nothing_happens() -> void:
	_ice()
	var kid: CharacterRig = _kid(500.0)
	kid.set_meta("drop_velocity", Vector2.ZERO)
	assert_true(AreaActions.on_dropped(fake, kid))
	assert_almost_eq(kid.position.x, 500.0, 0.01, "Pirouette auf der Stelle")
	var other: CharacterRig = _kid(500.0, 40.0)
	other.position = Vector2(100.0, 200.0)
	assert_false(IceActions.on_dropped(fake, other), "neben dem Eis: normal abstellen")


func test_ice_gets_scratched_and_the_resurfacer_makes_it_shine() -> void:
	var ice: ItemNode = _ice()
	var m: ItemNode = ItemSpawner.on_floor(k.room, &"ice_resurfacer_white", 150.0, 20.0)
	var driver: NpcBrain = NpcSpawner.spawn(k.room, NpcRoles.role("ice_driver"), {"id": "d", "role": "ice_driver", "x_cm": 300, "y_cm": 30})
	var kid: CharacterRig = _kid(500.0)
	for i: int in IceActions.SCRATCH_AFTER:
		IceActions.glide(k.room, kid, ice, 200.0)
	assert_eq(ice.state, "scratched")
	IceActions.refresh(k.room)
	IceActions.tick(fake, IceActions.RESURF_EVERY_S - 1.0)
	assert_eq(ice.state, "scratched", "noch nicht")
	IceActions.tick(fake, 2.0)
	assert_eq(ice.state, "shiny", "Eismaschine war da")
	assert_eq(Seats.occupant(m, 0), driver.body, "Fahrer/in sitzt auf der Maschine")


func test_puck_into_the_hockey_goal() -> void:
	var goal: ItemNode = ItemSpawner.on_floor(k.room, &"ice_hockey_goal_coral", 900.0, 40.0)
	var puck: ItemNode = ItemSpawner.on_floor(k.room, &"sport_puck_black", 500.0, 45.0)
	_kid(440.0)
	assert_true(SportActions.kick(k.room, puck), "Puck gleitet weit genug (1,6 × Schuss)")
	assert_almost_eq(puck.position.x, goal.position.x, 0.5)


func test_disco_ball_colours_the_light() -> void:
	fake.light_mod = CanvasModulate.new()
	fake.add_child(fake.light_mod)
	var ball: ItemNode = ItemSpawner.on_wall(k.room, &"ice_disco_ball_lilac", 300.0, -240.0)
	IceActions.refresh(k.room)
	ball.on_tap()
	assert_eq(ball.state, "on")
	IceActions.tick(fake, 1.0)
	assert_ne(fake.light_mod.color, Color.WHITE, "farbiges Licht")
	ball.on_tap()
	IceActions.tick(fake, 0.1)
	assert_false(IceActions._disco, "Disco aus")
