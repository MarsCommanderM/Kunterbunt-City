extends GutTest
## P04-T01/T04/T10: Teile-Katalog, Varianten, Farbzonen-Umfärbung (Shader), Palette.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func test_every_slot_has_five_variants() -> void:
	var slots: Array = CharacterParts.slot_ids()
	assert_eq(slots.size(), 8, "acht Slots laut Tech-Spec")
	for slot: String in slots:
		assert_eq(CharacterParts.ids(slot).size(), 5, "Slot %s hat 5 Varianten" % slot)
		assert_false(CharacterParts.label(slot).is_empty())
		assert_false(CharacterParts.icon(slot).is_empty())


func test_every_variant_has_a_sprite_for_every_template() -> void:
	for tid: String in CharacterTemplates.ids():
		for slot: String in CharacterParts.slot_ids():
			for id: String in CharacterParts.ids(slot):
				var v: Dictionary = CharacterParts.variant(slot, id)
				assert_true(CharacterTemplates.has_part(tid, String(v["part"])),
					"%s/%s/%s: Sprite fehlt" % [tid, slot, id])
				if v.get("part_back"):
					assert_true(CharacterTemplates.has_part(tid, String(v["part_back"])),
						"%s/%s/%s: Rückteil fehlt" % [tid, slot, id])


func test_zones_are_between_1_and_3() -> void:
	for slot: String in CharacterParts.slot_ids():
		for id: String in CharacterParts.ids(slot):
			assert_between(CharacterParts.zones(slot, id), 1, 3, "%s/%s" % [slot, id])


func test_rig_builds_with_every_variant() -> void:
	for tid: String in CharacterTemplates.ids():
		for slot: String in CharacterParts.slot_ids():
			for id: String in CharacterParts.ids(slot):
				var look: Dictionary = CharacterParts.default_set(tid)
				look["parts"][slot] = id
				var rig: CharacterRig = CharacterRig.create_character(tid, look)
				assert_not_null(rig, "%s/%s/%s" % [tid, slot, id])
				assert_almost_eq(rig.global_rect().size.y, ItemDB.height_cm(
					String(CharacterTemplates.get_template(tid)["scale_ref"])), 3.0,
					"%s mit %s/%s bleibt maßstäblich" % [tid, slot, id])
				rig.free()


func test_zone_shader_receives_the_palette_colors() -> void:
	var rig: CharacterRig = ItemSpawner.character_on_floor(k.room, "kid", 300.0, 60.0)
	var top: Sprite2D = rig._layers["Top"]
	var mat: ShaderMaterial = top.material as ShaderMaterial
	assert_not_null(mat, "Oberteil hat das Zonen-Material")
	assert_eq(mat.shader, CharacterLook.SHADER)
	var want: Array = CharacterLook.colors_for(rig.look, "Top")
	for i: int in want.size():
		assert_eq(mat.get_shader_parameter("zone%d" % (i + 1)), want[i], "Zone %d" % (i + 1))
	# Farbe wechseln → Shader-Parameter folgt sofort (wie im Editor)
	var l: Dictionary = rig.look
	l["colors"] = {"top": ["#ff0000"]}       # wie im Editor: Farbe klicken
	rig.look = l
	CharacterLook.apply(top, CharacterLook.colors_for(rig.look, "Top"))
	var mat2: ShaderMaterial = top.material as ShaderMaterial
	assert_eq(mat2.get_shader_parameter("zone1"), Color("#ff0000"), "neue Farbe sofort sichtbar")
	assert_eq(mat2.get_shader_parameter("zone2"), Color("#ff0000"), "unbenutzte Zone folgt Zone 1")


func test_skin_and_fixed_parts_keep_their_colors() -> void:
	var rig: CharacterRig = ItemSpawner.character_on_floor(k.room, "kid", 300.0, 60.0)
	var skin_col: Color = (rig._layers["Head"].material as ShaderMaterial).get_shader_parameter("zone1")
	assert_eq(skin_col, Color(String(CharacterTemplates.default_look("kid")["skin"])))
	var eyes: Color = (rig._layers["Eyes"].material as ShaderMaterial).get_shader_parameter("zone1")
	assert_eq(eyes, Color(String(CharacterLook.FIXED["Eyes"][0])), "Augen bleiben fertig koloriert")


func test_palette_has_enough_colors() -> void:
	for g: String in CharacterParts.palette_groups():
		assert_gte(CharacterParts.palette_colors(g).size(), 5, "Palette %s" % g)
	for c: Variant in CharacterParts.palette_colors("skin"):
		var col: Color = Color(String(c))
		assert_gt((col.r + col.g + col.b) / 3.0, 0.1, "Hautton nicht zu dunkel: %s" % str(c))


func test_random_set_is_valid_and_reproducible() -> void:
	var a := RandomNumberGenerator.new()
	var b := RandomNumberGenerator.new()
	a.seed = 1234
	b.seed = 1234
	var s1: Dictionary = CharacterParts.random_set("kid", a)
	var s2: Dictionary = CharacterParts.random_set("kid", b)
	assert_eq(s1, s2, "gleicher Seed → gleiche Figur (🎲 ist reproduzierbar)")
	for slot: String in CharacterParts.slot_ids():
		assert_true(CharacterParts.ids(slot).has(String(s1["parts"][slot])), "Zufall trifft %s" % slot)
