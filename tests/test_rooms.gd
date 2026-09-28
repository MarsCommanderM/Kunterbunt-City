extends GutTest
## P07-T01/T04: Zuhause mit 11 Räumen – Raum wechseln (Figur + Tiere kommen mit, jeder Raum behält seine
## Sachen), leere Räume, Tapete/Boden wählen und speichern.

var area: AreaScene


func before_each() -> void:
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#f7c9a2"
	Game.add_character(c)
	Game.set_active(c.id)
	Game.add_pet(PetData.create("pet_dog_medium" if PetSpecies.ids().has("pet_dog_medium") else "pet_cat"))


func after_each() -> void:
	SaveSystem.wipe()
	Game.load_all()


func _enter() -> AreaScene:
	SceneRouter.pending_area = &"home"
	area = load("res://src/world/area_scene.tscn").instantiate()
	add_child_autofree(area)
	await wait_process_frames(6)
	return area


func _loose_items(a: AreaScene) -> int:
	var n: int = 0
	for it: ItemNode in Placement.all_items(a.room):
		if not (it is CharacterRig) and not (it is PetNode) and not it.def.is_wall():
			n += 1                                     # Licht-Schalter an der Wand zählt nicht als Einrichtung
	return n


func test_zuhause_hat_elf_raeume_mit_vorschaubild() -> void:
	var a: AreaScene = await _enter()
	assert_eq(a.room_ids().size(), 11)
	for rid: Variant in a.room_ids():
		assert_not_null(RoomPicker.thumb_of("home", String(rid)), "Vorschaubild fehlt: %s" % rid)


func test_start_im_leeren_wohnzimmer() -> void:
	var a: AreaScene = await _enter()
	assert_eq(String(a.room.room_id), "living")
	assert_eq(_loose_items(a), 0, "Räume starten leer – das Kind richtet selbst ein")
	assert_not_null(a.me, "eigene Figur fehlt")
	assert_true(a.room.can_decorate(), "Wohnzimmer hat wählbare Tapete/Boden")


func test_raumwechsel_nimmt_figur_und_tier_mit_und_behaelt_sachen() -> void:
	var a: AreaScene = await _enter()
	assert_true(a.place_from_catalog("furn_sofa_classic_mint"), "Sofa aus dem Katalog")
	assert_eq(_loose_items(a), 1)
	assert_true(a.switch_room("bath"))
	await wait_process_frames(3)
	assert_eq(String(a.room.room_id), "bath")
	assert_eq(_loose_items(a), 0, "im Bad steht kein Sofa")
	assert_not_null(a.me, "Figur kommt mit")
	assert_eq(a.pets.size(), 1, "Tier kommt mit")
	assert_eq(Game.last_room(&"home"), "bath")
	assert_true(a.switch_room("living"))
	await wait_process_frames(3)
	assert_eq(_loose_items(a), 1, "das Sofa steht noch im Wohnzimmer")
	var snap: Array = RoomSnapshot.capture(a.room)
	for e: Variant in snap:
		assert_eq(String((e as Dictionary).get("pet_id", "")), "", "eigene Tiere gehören nicht in den Raumzustand")


func test_weiter_im_zuletzt_besuchten_raum() -> void:
	var a: AreaScene = await _enter()
	a.switch_room("garden")
	await wait_process_frames(2)
	a.queue_free()
	await wait_process_frames(2)
	var b: AreaScene = await _enter()
	assert_eq(String(b.room.room_id), "garden")


func test_tapete_und_boden_waehlen_und_speichern() -> void:
	var a: AreaScene = await _enter()
	var before: int = a.room.background.get_child(0).get_child_count()
	a.set_decor({"wall": ["#a9c3dd", "#ffffff", "#f0b6c2"], "pattern": "stars", "pattern_col": "#f6d98a"})
	a.set_decor({"floor": "carpet", "floor_cols": ["#f0b6c2", "#e8a4b3", "#c1547a"]})
	assert_eq(String(a.room.decor["pattern"]), "stars")
	assert_eq(String(a.room.decor["floor"]), "carpet")
	assert_eq(a.room.background.get_child(0).get_child_count(), before, "Ebenen werden ersetzt, nicht gestapelt")
	var wall_spr: Sprite2D = a.room.background.get_child(0).get_child(0)
	var m: ShaderMaterial = wall_spr.material
	assert_true(bool(m.get_shader_parameter("has_pattern")), "Muster liegt auf der Tapete")
	assert_eq((m.get_shader_parameter("zone1") as Color).to_html(false), "a9c3dd")
	Game.save_now()
	Game.decor = {}
	Game.load_all()
	assert_eq(String(Game.room_decor(&"home", &"living")["floor"]), "carpet")
	# neuer Besuch: Einrichtung ist wieder da
	a.queue_free()
	await wait_process_frames(2)
	var b: AreaScene = await _enter()
	assert_eq(String(b.room.decor["pattern"]), "stars")


func test_raum_picker_und_deko_panel_ohne_text() -> void:
	var a: AreaScene = await _enter()
	var p: RoomPicker = RoomPicker.open(a.ui, a)
	await wait_process_frames(2)
	var grid: GridContainer = p.find_child("Rooms", true, false)
	assert_eq(grid.get_child_count(), 11, "eine Kachel je Raum")
	(grid.get_node("Room_kids1") as Button).pressed.emit()
	await wait_process_frames(3)
	assert_eq(String(a.room.room_id), "kids1", "Tippen auf die Kachel wechselt den Raum")
	var d: DecorPanel = DecorPanel.open(a.ui, a)
	await wait_process_frames(2)
	var kinds: GridContainer = d.find_child("FloorKinds", true, false)
	assert_true(kinds.get_child_count() >= 4, "mehrere Bodenarten")
	(kinds.get_node("Floor_tiles") as Button).pressed.emit()
	await wait_process_frames(2)
	assert_eq(String(a.room.decor["floor"]), "tiles")
	for n: Node in d.find_children("*", "Label", true, false):
		assert_true((n as Label).text.strip_edges().is_empty(), "kein Text im Kinder-UI (R-07)")
	d.queue_free()
