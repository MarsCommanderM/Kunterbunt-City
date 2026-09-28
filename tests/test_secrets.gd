extends GutTest
## P07-T10: 7 Geheimnisse im Zuhause → Sticker im Album; Speicherstand v4 (Migration v3→v4 aus Fixture, R-11).

var area: AreaScene


func before_each() -> void:
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	Recipes.instant = true
	CharacterRig.animate_poses = false
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#f7c9a2"
	Game.add_character(c)
	Game.set_active(c.id)


func after_each() -> void:
	Recipes.instant = false
	Garden.fixed_now = -1.0
	SaveSystem.wipe()
	Game.load_all()


func _enter(room_id: String) -> AreaScene:
	Game.set_last_room(&"home", StringName(room_id))
	SceneRouter.pending_area = &"home"
	area = load("res://src/world/area_scene.tscn").instantiate()
	add_child_autofree(area)
	await wait_process_frames(6)
	return area


func _switch_off(a: AreaScene) -> void:
	for it: ItemNode in Placement.all_items(a.room):
		if String(it.def.id).begins_with(RoomLight.SWITCH):
			ItemStates.set_state(it, "off", true)
	a._on_world_changed()


func test_sieben_geheimnisse_mit_stickern() -> void:
	assert_eq(Secrets.for_area("home").size(), 7)
	for s: Variant in Secrets.for_area("home"):
		assert_not_null(Secrets.sticker_def(s), "Sticker fehlt: %s" % (s as Dictionary)["id"])


func test_truhe_auf_dem_dachboden() -> void:
	var a: AreaScene = await _enter("attic")
	var chest: ItemNode = ItemSpawner.on_floor(a.room, &"furn_chest_walnut", 400.0, 30.0)
	assert_false(Game.has_secret("attic_treasure"))
	chest.on_tap()
	a._on_item_tapped(chest)
	assert_true(Game.has_secret("attic_treasure"), "Truhe geöffnet → Schatz gefunden")
	await wait_process_frames(2)
	assert_not_null(a.ui.find_child("SecretToast", true, false), "Sticker springt auf")


func test_maus_im_dunklen_keller_und_nicht_woanders() -> void:
	var a: AreaScene = await _enter("living")
	_switch_off(a)
	assert_false(Game.has_secret("basement_mouse"), "im Wohnzimmer gibt es keine Maus")
	a.switch_room("basement")
	await wait_process_frames(2)
	_switch_off(a)
	assert_true(Game.has_secret("basement_mouse"))


func test_ernte_und_kochen_sind_ereignisse() -> void:
	var a: AreaScene = await _enter("garden")
	Garden.fixed_now = 1000.0
	var bed: ItemNode = ItemSpawner.on_floor(a.room, &"garden_raised_bed_m_carrot_oak", 900.0, 30.0)
	ItemStates.set_state(bed, "ripe", true)
	Game.mark_dirty(&"home", &"garden")
	Garden.harvest(bed)
	assert_true(Game.has_secret("garden_harvest"))
	var toaster: ItemNode = ItemSpawner.on_floor(a.room, &"kit_toaster_cream", 1000.0, 30.0)
	ItemSpawner.into_container(toaster, &"cook_bread_slice_pine")
	ItemStates.set_state(toaster, "on", true)
	assert_true(Game.has_secret("kitchen_cook"), "Kochen zählt überall")


func test_geheimnisse_werden_gespeichert_und_im_album_gezeigt() -> void:
	Game.add_secret("bath_foam")
	Game.save_now()
	Game.secrets = []
	Game.load_all()
	assert_true(Game.has_secret("bath_foam"))
	var album: Album = Album.open(self)
	await wait_process_frames(2)
	var st: Node = album.find_child("Sticker_bath_foam", true, false)
	assert_not_null(st)
	assert_true(bool(st.get_meta("found")))
	assert_false(bool(album.find_child("Sticker_attic_treasure", true, false).get_meta("found")))
	album.queue_free()


func test_v3_wandert_nach_v4() -> void:
	var old: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tests/fixtures/world_v3.json"))
	assert_eq(int(old["save_version"]), 3)
	var f := FileAccess.open(SaveSystem.world_path(2), FileAccess.WRITE)
	f.store_string(JSON.stringify(old))
	f.close()
	var w: Dictionary = SaveSystem.load_world(2)
	assert_eq(int(w["save_version"]), 4)
	assert_eq(w["secrets"], [])
	assert_eq(String(Dictionary(Dictionary(w["decor"])["home"])["living"]["floor"]), "carpet", "Einrichtung bleibt")
