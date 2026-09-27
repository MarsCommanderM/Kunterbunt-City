extends GutTest
## P05-T05/T06/T11: Bereich betreten (Ladezeit, Spawn, Haustiere), Raumzustand retten,
## zurück zur Karte, Rucksack.

var area: AreaScene


func before_each() -> void:
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	if Game.characters.is_empty():
		var c: CharacterData = CharacterData.create("kid")
		c.skin = "#f7c9a2"
		c.character_name = "Testkind"
		Game.add_character(c)
		Game.set_active(c.id)
	if Game.pets.is_empty():
		Game.add_pet(PetData.create("pet_cat"))


func after_each() -> void:
	if area != null and is_instance_valid(area):
		area.queue_free()
	SaveSystem.wipe()


## Zuhause startet seit P07 im (leeren) Wohnzimmer – diese Tests prüfen die eingerichtete Küche.
func _enter(id: StringName = &"home", room_id: StringName = &"kitchen") -> AreaScene:
	if room_id != &"":
		Game.set_last_room(id, room_id)
	SceneRouter.pending_area = id
	area = load("res://src/world/area_scene.tscn").instantiate()
	add_child_autofree(area)
	await wait_process_frames(6)
	return area


func test_bereich_laedt_in_unter_zwei_sekunden() -> void:
	var a: AreaScene = await _enter()
	assert_not_null(a.room, "Raum fehlt")
	assert_lt(a.load_ms, 2000.0, "Ladezeit %.0f ms (Ziel < 2000 ms)" % a.load_ms)
	assert_eq(SceneRouter.last_load_ms, a.load_ms)


func test_eigene_figur_und_haustier_stehen_drin() -> void:
	var a: AreaScene = await _enter()
	assert_not_null(a.me, "die eigene Figur fehlt")
	var h: float = a.me.global_rect().size.y / a.me.global_scale.y
	assert_almost_eq(h, 125.0, 1.5, "Kind ist 125 cm hoch, gemessen %.1f" % h)
	assert_eq(a.pets.size(), 1, "das gewählte Haustier muss mitkommen")
	var pet: ItemNode = a.pets[0]
	assert_almost_eq(pet.global_rect().size.y / pet.global_scale.y, 28.0, 1.5,
		"Katze ist 28 cm hoch (Maßstab-Tabelle)")


func test_start_ausstattung_und_raumzustand() -> void:
	var a: AreaScene = await _enter()
	var n: int = Placement.all_items(a.room).size()
	assert_true(n >= 13, "Start-Ausstattung fehlt (nur %d Items)" % n)
	var snap: Array = RoomSnapshot.capture(a.room)
	assert_true(snap.size() >= 12, "Zustand muss die Möbel und Dinge enthalten")
	assert_false(_has_character(snap), "die Figur gehört nicht in den Raumzustand")
	Game.set_room_state(&"home", &"kitchen", snap)
	Game.save_now()
	var back: Array = Game.room_state(&"home", &"kitchen")
	assert_eq(back.size(), snap.size())


func test_dinge_auf_tischen_bleiben_erhalten() -> void:
	var a: AreaScene = await _enter()
	var snap: Array = RoomSnapshot.capture(a.room)
	var on_table: Array = []
	for e: Variant in snap:
		if String((e as Dictionary).get("on", "")) != "":
			on_table.append(e)
	assert_true(on_table.size() >= 1, "Dinge auf dem Tisch müssen mitgespeichert werden")
	# frischer Aufbau aus dem Zustand
	var b: AreaScene = await _enter()
	var ids: Array = []
	for it: ItemNode in Placement.all_items(b.room):
		ids.append(String(it.def.id))
	assert_true(ids.has("food_carrot"), "Karotte muss wieder auf dem Tisch liegen")


func test_zurueck_zur_karte_speichert() -> void:
	var a: AreaScene = await _enter()
	a.leave()
	await wait_process_frames(3)
	var saved: Dictionary = SaveSystem.load_world(0)
	var rooms: Dictionary = Dictionary(Dictionary(saved.get("areas", {})).get("home", {}))
	assert_true(Array(rooms.get("kitchen", [])).size() >= 12, "Raumzustand ist gespeichert")


func test_rucksack_nimmt_zwanzig_dinge_und_nicht_mehr() -> void:
	Game.backpack.clear()
	for i: int in 20:
		Game.backpack.append({"id": "toy_block"})
	assert_true(Backpack.is_full())
	Game.backpack.clear()
	assert_false(Backpack.is_full())


func test_bereich_zuruecksetzen() -> void:
	Game.set_room_state(&"home", &"kitchen", [{"id": "toy_block", "x": 100.0, "y": 30.0}])
	assert_eq(Game.room_state(&"home", &"kitchen").size(), 1)
	Game.reset_areas()
	assert_eq(Game.room_state(&"home", &"kitchen").size(), 0, "🪄 stellt den Anfang wieder her")


func _has_character(snap: Array) -> bool:
	for e: Variant in snap:
		var id: String = String((e as Dictionary).get("id", ""))
		if id.begins_with("char"):
			return true
	return false
