extends GutTest
## Alle Item-Dateien laden fehlerfrei; jedes Item hat eine Textur; Größen = Maßstab-Tabelle.


func test_all_items_loaded_without_errors() -> void:
	assert_eq(ItemDB.validation_errors.size(), 0, "\n".join(ItemDB.validation_errors))
	# Zahl der Items = Summe aller Einträge in data/items/*.json (P04b: der Katalog wächst ständig)
	var want: int = 0
	for f: String in DirAccess.get_files_at("res://data/items/"):
		if f.ends_with(".json"):
			var d: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/items/" + f))
			want += Array((d as Dictionary).get("items", [])).size() if d is Dictionary else Array(d).size()
	assert_eq(ItemDB.item_count(), want, "jedes Item aus data/items/ ist geladen")
	assert_gte(ItemDB.item_count(), 77, "mindestens die 77 Items aus Phase 02–04")


func test_every_item_has_loadable_texture() -> void:
	for id: StringName in ItemDB.item_ids():
		var def: ItemDefinition = ItemDB.get_item(id)
		var tex: Texture2D = load(def.sprite_path)
		assert_not_null(tex, "%s: %s" % [id, def.sprite_path])


func test_heights_match_scale_table() -> void:
	for id: StringName in ItemDB.item_ids():
		var def: ItemDefinition = ItemDB.get_item(id)
		assert_almost_eq(def.height_cm, ItemDB.height_cm(def.scale_ref, def.scale_mul), 0.0001, String(id))


func test_real_style_c_sprites_are_used() -> void:
	for id: StringName in [&"food_apple_red", &"pet_dog_brown", &"home_table_wood", &"home_chair_mint"]:
		var def: ItemDefinition = ItemDB.get_item(id)
		assert_false(def.uses_placeholder, String(id))
		assert_string_starts_with(def.sprite_path, "res://assets/sprites/home/")


func test_unknown_item_is_error() -> void:
	assert_null(ItemDB.get_item(&"gibts_nicht"))
	assert_push_error("unbekanntes Item")


func test_dog_is_smaller_than_table_and_apple_smaller_than_ball() -> void:
	assert_lt(ItemDB.get_item(&"pet_dog_brown").height_cm, ItemDB.get_item(&"home_table_wood").height_cm)
	assert_lt(ItemDB.get_item(&"food_apple_red").height_cm, ItemDB.get_item(&"toy_basketball").height_cm)
