extends GutTest
## Sounds: Material je Kategorie, eigener Sound vor Standard, fehlende Datei = still (kein Absturz).


func before_each() -> void:
	AudioBus.history.clear()


func test_category_default_drop_sound() -> void:
	AudioBus.play_item_sfx(ItemDB.get_item(&"toy_basketball"), "drop")
	AudioBus.play_item_sfx(ItemDB.get_item(&"kitchen_glass"), "drop")
	assert_eq(AudioBus.history, ["drop_plastic", "drop_clink"] as Array[String])


func test_item_sfx_overrides_category() -> void:
	AudioBus.play_item_sfx(ItemDB.get_item(&"home_table_wood"), "drop")
	assert_eq(AudioBus.history.back(), "drop_wood")


func test_all_sound_files_exist() -> void:
	for n: String in ["pickup", "tap", "drop_soft", "drop_wood", "drop_clink", "drop_plastic", "drop_metal", "drop_paper", "open", "close", "deny"]:
		assert_true(ResourceLoader.exists(AudioBus.SFX_DIR + n + ".wav"), n)


func test_missing_sound_is_silent() -> void:
	AudioBus.play_sfx("gibts_nicht")
	assert_eq(AudioBus.history.back(), "gibts_nicht")
	assert_null(AudioBus._get_stream("gibts_nicht"))
