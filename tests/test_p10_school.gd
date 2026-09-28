extends GutTest
## P10a Schule: Tafel mit Kreide-Bildern, Schulglocke (Kinder jubeln), Band aus 3 Instrumenten, Vulkan, Spinde.

var k: KitchenFixture


func before_each() -> void:
	NpcBrain.autonomous = false
	k = KitchenFixture.new(self)
	AreaActions._band.clear()


func after_all() -> void:
	NpcBrain.autonomous = true


func test_school_area_has_ten_rooms_and_sixteen_npcs() -> void:
	var d: Dictionary = Room.load_area(Areas.path_of(&"school"))
	assert_eq(Array(d["rooms"]).size(), 10)
	assert_eq(NpcRoles.npcs_of("school").size(), 16)
	assert_eq(Secrets.for_area("school").size(), 7)


func test_blackboard_cycles_through_chalk_pictures() -> void:
	var b: ItemNode = ItemSpawner.on_wall(k.room, &"edu_blackboard_green", 300.0, -230.0)
	var seen: Array = [b.state]
	for i: int in 4:
		b.on_tap()
		seen.append(b.state)
	assert_eq(seen, ["empty", "sun", "house", "cat", "shapes"], "Kreide-Bilder nacheinander")
	b.on_tap()
	assert_eq(b.state, "empty", "Schwamm: wieder leer")
	assert_eq(String(b.def.sfx["cat"]), "chalk")


func test_school_bell_makes_the_pupils_cheer() -> void:
	var p1: NpcBrain = NpcSpawner.spawn(k.room, NpcRoles.role("pupil"), {"id": "p1", "role": "pupil", "x_cm": 200, "y_cm": 50})
	var p2: NpcBrain = NpcSpawner.spawn(k.room, NpcRoles.role("pupil2"), {"id": "p2", "role": "pupil2", "x_cm": 400, "y_cm": 50})
	var t: NpcBrain = NpcSpawner.spawn(k.room, NpcRoles.role("teacher"), {"id": "t", "role": "teacher", "x_cm": 600, "y_cm": 10})
	assert_eq(p1.body.def.height_cm, ItemDB.height_cm(&"char_child"), "Schulkinder sind Kinder (125 cm)")
	var bell: ItemNode = ItemSpawner.on_wall(k.room, &"edu_bell_butter", 300.0, -240.0)
	bell.on_tap()
	assert_eq(bell.state, "ring")
	var fake := AreaScene.new()
	fake.room = k.room
	assert_true(AreaActions.on_tapped(fake, bell))
	assert_eq(p1.anim, "wave")
	assert_eq(p2.body.emotion, "laugh", "jubeln")
	assert_eq(t.anim, "clap", "Lehrerin klatscht")
	fake.free()


func test_three_instruments_make_a_band() -> void:
	var fake := AreaScene.new()
	fake.room = k.room
	var drums: ItemNode = ItemSpawner.on_floor(k.room, &"music_drums_coral", 200.0, 30.0)
	var xylo: ItemNode = ItemSpawner.on_floor(k.room, &"toy_xylophone_coral", 350.0, 60.0)
	var tri: ItemNode = ItemSpawner.on_floor(k.room, &"edu_triangle_metal", 450.0, 60.0)
	assert_eq(String(drums.def.sfx["tap"]), "drum_hit", "Instrumente klingen beim Antippen")
	assert_false(AreaActions.on_tapped(fake, drums))
	assert_false(AreaActions.on_tapped(fake, drums), "zweimal dasselbe zählt nicht")
	assert_false(AreaActions.on_tapped(fake, xylo))
	assert_true(AreaActions.on_tapped(fake, tri), "drittes Instrument → Band")
	fake.free()


func test_volcano_and_locker_states() -> void:
	var v: ItemNode = ItemSpawner.on_floor(k.room, &"edu_volcano_oak", 300.0, 60.0)
	v.on_tap()
	assert_eq(v.state, "erupt")
	assert_eq(String(v.def.sfx["erupt"]), "fizz")
	var l: ItemNode = ItemSpawner.on_floor(k.room, &"edu_locker_sky", 500.0, 10.0)
	l.on_tap()
	assert_eq(l.state, "open", "Spind geht auf")
