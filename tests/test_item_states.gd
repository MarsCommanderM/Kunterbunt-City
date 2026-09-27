extends GutTest
## P04b-T10: Schränke/Schubladen auf, Geräte an/aus, Kochen mit Rezepten, Zustand wird gespeichert.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)
	Recipes.instant = true


func after_each() -> void:
	Recipes.instant = false


func _first(prefix: String) -> StringName:
	for gid: String in Catalog.group_ids():
		for id: Variant in Catalog.items(gid):
			if String(id).begins_with(prefix):
				return StringName(String(id))
	return &""


func test_every_stateful_item_has_matching_state_sprites() -> void:
	var n: int = 0
	for gid: String in Catalog.group_ids():
		for id: Variant in Catalog.items(gid):
			var def: ItemDefinition = ItemDB.get_item(StringName(String(id)))
			if not def.has_states():
				continue
			n += 1
			var base: Texture2D = load(def.sprite_path)
			for s: Variant in def.state_sprites:
				var tex: Texture2D = load(String(def.state_sprites[s]))
				assert_not_null(tex, "%s: Sprite für '%s'" % [id, s])
				assert_eq(tex.get_size(), base.get_size(), "%s: '%s' deckungsgleich (kein Springen)" % [id, s])
	assert_gte(n, 60, "viele Items mit Zuständen (auf/zu, an/aus)")


func test_tap_opens_wardrobe_and_switches_lamp_on() -> void:
	var wr: ItemNode = ItemSpawner.on_floor(k.room, _first("furn_wardrobe"), 300.0, 20.0)
	var tex0: Texture2D = wr.sprite.texture
	wr.on_tap()
	assert_eq(wr.state, "open", "Schrank ist offen")
	assert_ne(wr.sprite.texture, tex0, "offene Türen werden gezeigt")
	var h0: float = wr.global_rect().size.y
	wr.on_tap()
	assert_eq(wr.state, "closed")
	assert_almost_eq(wr.global_rect().size.y, h0, 0.5, "Größe bleibt beim Umschalten gleich")
	var lamp: ItemNode = ItemSpawner.on_floor(k.room, _first("deco_lamp_floor"), 400.0, 20.0)
	lamp.on_tap()
	assert_eq(lamp.state, "on", "Lampe ist an")


func test_fridge_opens_and_takes_food() -> void:
	var fr: ItemNode = ItemSpawner.on_floor(k.room, _first("app_fridge"), 300.0, 10.0)
	assert_false(fr.is_open)
	fr.on_tap()
	assert_true(fr.is_open, "Kühlschrank auf → Inhalt sichtbar")
	var egg: ItemNode = ItemSpawner.into_container(fr, _first("food_egg"))
	assert_not_null(egg, "Ei passt in den Kühlschrank")


func test_toaster_makes_toast() -> void:
	var t: ItemNode = ItemSpawner.on_floor(k.room, _first("kit_toaster"), 300.0, 30.0)
	assert_true(t.is_open, "Toaster zeigt seinen Inhalt immer")
	ItemSpawner.into_container(t, _first("cook_bread_slice"))
	t.on_tap()
	assert_eq(t.state, "on")
	var names: Array = []
	for c: Node in t.contents_root.get_children():
		if c is ItemNode and not c.is_queued_for_deletion():
			names.append(String((c as ItemNode).def.id))
	assert_has(names, "cook_toast_oak", "Brot wird zu Toast")


func test_pan_on_stove_fries_egg() -> void:
	var stove: ItemNode = ItemSpawner.on_floor(k.room, _first("app_stove"), 300.0, 10.0)
	var pan: ItemNode = ItemSpawner.into_container(stove, _first("kit_pan"))
	assert_not_null(pan)
	ItemSpawner.into_container(pan, _first("food_egg"))
	stove.on_tap()
	var got: bool = false
	for c: Node in pan.contents_root.get_children():
		if c is ItemNode and String((c as ItemNode).def.id) == "cook_fried_egg_white" and not c.is_queued_for_deletion():
			got = true
	assert_true(got, "Ei in der Pfanne auf dem heißen Herd wird Spiegelei")


func test_state_is_saved_and_restored() -> void:
	var wr: ItemNode = ItemSpawner.on_floor(k.room, _first("furn_wardrobe"), 300.0, 20.0)
	wr.on_tap()
	var snap: Array = RoomSnapshot.capture(k.room)
	wr.queue_free()
	for it: ItemNode in Placement.all_items(k.room):
		it.free() if not it.is_queued_for_deletion() else null
	await wait_process_frames(1)
	RoomSnapshot.apply(k.room, snap)
	var found: ItemNode = null
	for it: ItemNode in Placement.all_items(k.room):
		if String(it.def.id).begins_with("furn_wardrobe"):
			found = it
	assert_not_null(found)
	assert_eq(found.state, "open", "offener Schrank bleibt nach dem Laden offen")


## P04b-T11: draußen grillen, am Lagerfeuer kochen, Kasse und Werkstatt zum Spielen.
func _contents(host: ItemNode) -> Array:
	var names: Array = []
	for c: Node in host.contents_root.get_children():
		if c is ItemNode and not c.is_queued_for_deletion():
			names.append(String((c as ItemNode).def.id))
	return names


func test_grill_turns_bbq_food_into_sausage() -> void:
	var g: ItemNode = ItemSpawner.on_floor(k.room, _first("garden_grill"), 300.0, 10.0)
	assert_eq(g.state, "off")
	ItemSpawner.into_container(g, _first("garden_bbq_food"))
	g.on_tap()
	assert_eq(g.state, "on", "Tippen zündet den Grill an")
	assert_has(_contents(g), "cook_sausage_rust", "Grillgut wird zur Wurst")


func test_campfire_toasts_bread_only_when_burning() -> void:
	var f: ItemNode = ItemSpawner.on_floor(k.room, _first("camp_campfire"), 300.0, 10.0)
	ItemSpawner.into_container(f, _first("cook_bread_slice"))
	Recipes.check(f)
	assert_does_not_have(_contents(f), "cook_toast_oak", "kaltes Feuer kocht nicht")
	f.on_tap()
	assert_has(_contents(f), "cook_toast_oak", "am brennenden Feuer wird Brot zu Toast")


func test_register_toolbox_cooler_tent_open_and_drill_runs() -> void:
	for pre: String in ["shop_cash_register", "work_toolbox", "pool_cooler", "camp_tent_"]:
		var it: ItemNode = ItemSpawner.on_floor(k.room, _first(pre), 300.0, 10.0)
		assert_true(it.def.has_states(), pre + " hat Zustände")
		it.on_tap()
		assert_eq(it.state, "open", pre + " geht auf")
	var d: ItemNode = ItemSpawner.on_floor(k.room, _first("work_drill"), 300.0, 10.0)
	d.on_tap()
	assert_eq(d.state, "on", "Bohrer läuft")
	var l: ItemNode = ItemSpawner.on_floor(k.room, _first("camp_lantern"), 300.0, 10.0)
	l.on_tap()
	assert_eq(l.state, "on", "Laterne leuchtet")
