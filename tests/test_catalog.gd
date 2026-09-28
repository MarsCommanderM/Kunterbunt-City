extends GutTest
## P04b-T09: Item-Katalog – hunderte Items, jedes in jedem Raum einsetzbar, Farben wie im Spiel, Maßstab aus der Tabelle.

var area: AreaScene


func before_each() -> void:
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	CharacterRig.animate_poses = false
	if Game.characters.is_empty():
		var c: CharacterData = CharacterData.create("kid")
		c.skin = "#f7c9a2"
		c.character_name = "Testkind"
		Game.add_character(c)
		Game.set_active(c.id)


func after_each() -> void:
	if area != null and is_instance_valid(area):
		area.queue_free()
	SaveSystem.wipe()


func test_catalog_has_hundreds_of_valid_items() -> void:
	assert_gte(Catalog.count(), 300, "hunderte Items im Katalog")
	assert_gte(Catalog.items("plants").size(), 200, "hunderte Pflanzen")
	for gid: String in Catalog.group_ids():
		assert_false(Catalog.items(gid).is_empty(), "Reiter %s hat Items" % gid)
		for id: Variant in Catalog.items(gid):
			var def: ItemDefinition = ItemDB.get_item(StringName(String(id)))
			assert_not_null(def, "%s ist in der ItemDB" % id)
			assert_false(def.uses_placeholder, "%s hat echte Grafik (keinen Platzhalter)" % id)
			assert_between(def.colors.size(), 1, 3, "%s hat Farbzonen" % id)
			assert_almost_eq(def.height_cm, ItemDB.height_cm(def.scale_ref) * def.scale_mul, 0.01,
				"%s: Größe aus der Maßstab-Tabelle" % id)


func test_catalog_item_is_tinted_like_in_game() -> void:
	var id: String = String(Catalog.items("sofas")[0])
	var def: ItemDefinition = ItemDB.get_item(StringName(id))
	var it: ItemNode = ItemNode.create(def)
	add_child_autofree(it)
	var mat: ShaderMaterial = it.sprite.material as ShaderMaterial
	assert_not_null(mat, "Katalog-Item nutzt den Zonen-Shader")
	assert_eq(mat.get_shader_parameter("zone1"), def.colors[0])
	assert_eq(mat.get_shader_parameter("ink"), CharacterLook.INK)


func test_color_variants_share_one_sprite_but_differ_in_color() -> void:
	var ids: Array = Catalog.items("sofas")
	var a: ItemDefinition = ItemDB.get_item(StringName(String(ids[0])))
	var b: ItemDefinition = ItemDB.get_item(StringName(String(ids[1])))
	assert_eq(a.sprite_path, b.sprite_path, "Varianten teilen das Sprite")
	assert_ne(a.colors[0], b.colors[0], "…aber nicht die Farbe")


func test_placeholder_furniture_got_real_art() -> void:
	for id: String in ["home_sofa", "home_armchair", "home_bed_kid", "home_stool", "home_table_coffee"]:
		var def: ItemDefinition = ItemDB.get_item(StringName(id))
		assert_false(def.uses_placeholder, "%s: keine graue Kiste mit Text mehr" % id)
		assert_false(def.colors.is_empty(), "%s: Farbzonen" % id)


## Wie gewünscht: Leiste rechts (max. ⅓ des Bildschirms) bleibt offen – Sofa UND Schrank aussuchen,
## beide stehen sofort im Raum, sind frei verschiebbar und werden gespeichert.
func test_sofa_and_cabinet_from_the_side_panel_appear_in_any_room() -> void:
	SceneRouter.pending_area = &"home"
	area = load("res://src/world/area_scene.tscn").instantiate()
	add_child(area)
	await wait_process_frames(6)
	var before: int = area.room.ysort_root.get_child_count()
	var panel: CatalogPanel = CatalogPanel.open(area.ui, area.place_from_catalog)
	await wait_process_frames(2)
	var vp_w: float = panel.get_viewport_rect().size.x
	assert_lte(panel.size.x, vp_w / 3.0 + 1.0, "Katalog nutzt höchstens ein Drittel des Bildschirms")
	panel.show_group("sofas")
	var sofa: String = String(Catalog.items("sofas")[0])
	panel.pick(sofa)
	panel.show_group("storage")
	var cab: String = String(Catalog.items("storage")[0])
	panel.pick(cab)
	assert_true(is_instance_valid(panel) and not panel.is_queued_for_deletion(), "Leiste bleibt offen")
	assert_eq(area.room.ysort_root.get_child_count(), before + 2, "Sofa und Schrank stehen im Raum")
	var ids: Array = []
	for c: Node in area.room.ysort_root.get_children():
		if c is ItemNode:
			ids.append(String((c as ItemNode).def.id))
			if String((c as ItemNode).def.id) in [sofa, cab]:
				assert_true((c as ItemNode).def.movable, "%s ist frei verschiebbar" % (c as ItemNode).def.id)
	assert_has(ids, sofa)
	assert_has(ids, cab)
	var saved: Array = []
	for e: Variant in Game.room_state(&"home", area.room.room_id):
		if e is Dictionary:
			saved.append(String((e as Dictionary).get("id", "")))
	assert_has(saved, sofa, "Sofa wird gespeichert")
	assert_has(saved, cab, "Schrank wird gespeichert")
