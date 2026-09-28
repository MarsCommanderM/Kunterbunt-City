extends GutTest
## P10c Freizeitbad: Daten, Schwimmen (Sitzplatz im Becken, Platsch, Tropfen), Sprungturm, Wasserrutsche,
## Wellen-Anzeige, Bademeister zählt Figuren im Schwimmerbecken.

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


func test_pool_area_has_six_rooms_npcs_and_secrets() -> void:
	var d: Dictionary = Room.load_area(Areas.path_of(&"pool"))
	assert_eq(Array(d["rooms"]).size(), 6)
	assert_eq(NpcRoles.npcs_of("pool").size(), 5)
	assert_eq(Secrets.for_area("pool").size(), 6)
	assert_true(Areas.is_ready(&"pool"))


func test_figure_in_the_basin_swims_and_drips() -> void:
	var basin: ItemNode = ItemSpawner.on_floor(k.room, &"swim_basin_sky", 500.0, 30.0)
	var kid: CharacterRig = _kid(150.0)
	var t: Placement.Target = k.drag_pivot_to(kid, Seats.point_global(basin, 2) - kid.hip_offset() * basin.global_scale.y, 3)
	assert_eq(t.kind, &"seat", "Becken hat Plätze im Wasser")
	AreaActions.on_dropped(fake, kid)
	assert_eq(PoolActions.water_of(kid), basin, "Figur schwimmt")
	assert_not_null(kid.get_node_or_null("Drips"), "tropft")
	assert_true(kid.has_meta("wet_until"))


func test_diving_tower_jumps_into_the_nearest_basin() -> void:
	var tower: ItemNode = ItemSpawner.on_floor(k.room, &"swim_diving_tower_sky", 200.0, 20.0)
	var basin: ItemNode = ItemSpawner.on_floor(k.room, &"swim_basin_sky", 600.0, 35.0)
	var kid: CharacterRig = _kid(tower.position.x, tower.position.y + 10.0)
	CharacterRig.animate_poses = false
	Settings.reduced_motion = true
	assert_true(AreaActions.on_dropped(fake, kid), "springt")
	Settings.reduced_motion = false
	assert_eq(PoolActions.water_of(kid), basin, "landet im Becken")
	assert_eq(kid.body_pose, "sit")


func test_water_slide_ends_in_the_basin() -> void:
	var slide: ItemNode = ItemSpawner.on_floor(k.room, &"swim_water_slide_butter", 300.0, 10.0)
	var basin: ItemNode = ItemSpawner.on_floor(k.room, &"swim_basin_white", 700.0, 40.0)
	var kid: CharacterRig = _kid(slide.position.x - slide.def.width_cm * 0.4, slide.position.y + 10.0)
	Settings.reduced_motion = true
	assert_true(AreaActions.on_dropped(fake, kid), "rutscht")
	Settings.reduced_motion = false
	assert_eq(PoolActions.water_of(kid), basin)


func test_wave_sign_makes_swimmers_cheer() -> void:
	var basin: ItemNode = ItemSpawner.on_floor(k.room, &"swim_basin_sky", 500.0, 30.0)
	var kid: CharacterRig = _kid(150.0)
	PoolActions.seat_in(kid, basin, 1)
	kid.set_emotion("sad")
	var sign: ItemNode = ItemSpawner.on_wall(k.room, &"swim_wave_sign_navy", 300.0, -200.0)
	sign.on_tap()
	assert_eq(sign.state, "on")
	assert_true(AreaActions.on_tapped(fake, sign))
	assert_eq(kid.emotion, "laugh", "Wellen!")


func test_lifeguard_watches_the_swimming_basin() -> void:
	var basin: ItemNode = ItemSpawner.on_floor(k.room, &"swim_basin_sky", 500.0, 30.0)
	var g: NpcBrain = NpcSpawner.spawn(k.room, NpcRoles.role("lifeguard"), {"id": "g", "role": "lifeguard", "x_cm": 300, "y_cm": 60})
	var kid: CharacterRig = _kid(150.0)
	PoolActions.seat_in(kid, basin, 0)
	assert_true(g.work.in_water(kid), "Bademeister erkennt Schwimmer im Freizeitbad-Becken")
