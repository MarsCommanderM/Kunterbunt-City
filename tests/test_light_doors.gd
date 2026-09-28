extends GutTest
## P07-T05: Licht-Schalter macht den Raum dunkel, eingeschaltete Lampen leuchten; Tür antippen → Raum-Wahl.

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


func after_each() -> void:
	SaveSystem.wipe()
	Game.load_all()


func _enter() -> AreaScene:
	SceneRouter.pending_area = &"home"
	area = load("res://src/world/area_scene.tscn").instantiate()
	add_child_autofree(area)
	await wait_process_frames(6)
	return area


func _switch(a: AreaScene) -> ItemNode:
	for it: ItemNode in Placement.all_items(a.room):
		if String(it.def.id).begins_with(RoomLight.SWITCH):
			return it
	return null


func test_jeder_innenraum_hat_einen_lichtschalter_an_der_wand() -> void:
	var a: AreaScene = await _enter()
	var sw: ItemNode = _switch(a)
	assert_not_null(sw, "Licht-Schalter im Wohnzimmer")
	assert_true(sw.def.is_wall())
	assert_eq(sw.state, "on")
	assert_eq(a.light_mod.color, Color.WHITE, "Licht an = hell")


func test_schalter_aus_macht_dunkel_und_lampe_leuchtet() -> void:
	var a: AreaScene = await _enter()
	var lamp: ItemNode = ItemSpawner.on_floor(a.room, &"deco_lamp_floor_butter", 500.0, 20.0)
	ItemStates.set_state(lamp, "on", true)
	var sw: ItemNode = _switch(a)
	sw.on_tap()
	a._on_item_tapped(sw)
	assert_eq(sw.state, "off")
	assert_eq(a.light_mod.color, RoomLight.DARK, "Licht aus = Nacht-Stimmung")
	assert_not_null(lamp.get_node_or_null("Glow"), "eingeschaltete Lampe leuchtet im Dunkeln")
	sw.on_tap()
	a._on_item_tapped(sw)
	await wait_process_frames(2)
	assert_eq(a.light_mod.color, Color.WHITE)
	assert_null(lamp.get_node_or_null("Glow"), "bei hellem Raum kein extra Licht")


func test_tuer_antippen_oeffnet_raumwahl() -> void:
	var a: AreaScene = await _enter()
	var door: ItemNode = ItemSpawner.place(a.room, &"door_wood_oak", 300.0, 20.0)
	assert_not_null(door)
	a._on_item_tapped(door)
	await wait_process_frames(2)
	var picker: Node = a.ui.find_child("*", true, false)
	var found: bool = false
	for n: Node in a.ui.get_children():
		if n is RoomPicker:
			found = true
	assert_true(found, "Tür führt zur Raum-Wahl")
