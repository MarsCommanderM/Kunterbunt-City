extends GutTest
## P10b Gesundheitszentrum: Daten (12 Räume, 12 Figuren, Geheimnisse), Röntgen-Bilder, Blaulicht, Herzmonitor,
## Verarzten (Armschlinge/Pflaster/Augenklappe in die Hand → Figur trägt es).

var k: KitchenFixture


func before_each() -> void:
	NpcBrain.autonomous = false
	k = KitchenFixture.new(self)


func after_all() -> void:
	NpcBrain.autonomous = true


func test_hospital_area_has_twelve_rooms_npcs_and_secrets() -> void:
	var d: Dictionary = Room.load_area(Areas.path_of(&"hospital"))
	assert_eq(Array(d["rooms"]).size(), 12)
	assert_eq(NpcRoles.npcs_of("hospital").size(), 12)
	assert_eq(Secrets.for_area("hospital").size(), 6)
	assert_true(Areas.is_ready(&"hospital"), "auf der Stadtkarte spielbar")


func test_xray_shows_pictures_one_after_another() -> void:
	var x: ItemNode = ItemSpawner.on_floor(k.room, &"med_xray_white", 300.0, 30.0)
	var seen: Array = [x.state]
	for i: int in 3:
		x.on_tap()
		seen.append(x.state)
	assert_eq(seen, ["off", "fish", "car", "ribs"], "Röntgenbilder nacheinander")
	assert_eq(String(x.def.sfx["fish"]), "xray_beep")


func test_ambulance_siren_and_heart_monitor_beep() -> void:
	var amb: ItemNode = ItemSpawner.on_floor(k.room, &"med_ambulance_white", 400.0, 30.0)
	amb.on_tap()
	assert_eq(amb.state, "on")
	assert_eq(String(amb.def.sfx["on"]), "siren")
	var mon: ItemNode = ItemSpawner.on_floor(k.room, &"med_heart_monitor_white", 200.0, 30.0)
	mon.on_tap()
	assert_eq(mon.state, "beep")
	for s: String in ["siren", "monitor_beep", "xray_beep", "rotor"]:
		assert_true(ResourceLoader.exists("res://assets/audio/sfx/%s.wav" % s), s)


func test_sling_in_hand_is_worn_as_aid() -> void:
	var kid: CharacterRig = ItemSpawner.character_on_floor(k.room, "kid", 300.0, 40.0) as CharacterRig
	var sling: ItemNode = ItemSpawner.on_floor(k.room, &"med_sling_sky", 420.0, 40.0)
	var grip: Vector2 = PlacementCharacter.grip_global(sling, Vector2.ZERO)
	var t: Placement.Target = k.drag_pivot_to(sling, (kid.hand_slots()[0]["global"] as Vector2) - grip, 3)
	assert_eq(t.kind, &"hand", "Schlinge ist in der Hand")
	var fake := AreaScene.new()
	fake.room = k.room
	assert_true(AreaActions.on_dropped(fake, sling), "Figur wird verarztet")
	assert_eq(String(Dictionary(kid.look["parts"])["aid"]), "arm_sling")
	fake.free()


func test_every_aid_item_maps_to_an_existing_part() -> void:
	var ids: Array = CharacterParts.ids("aid")
	for pre: String in ["health_bandage", "med_sling", "med_eye_patch"]:
		assert_true(ids.has(String(AreaActions.WEAR[pre][1])), pre)
