extends GutTest
## P11-T02/T03: Sprachen (Eltern-/Menü-Texte) und Mono-Ton.


func after_each() -> void:
	Settings.set_value("language", "de")
	Settings.set_value("mono_audio", false)


func test_six_languages_german_first() -> void:
	var langs: Array = I18n.languages()
	assert_eq(langs.size(), 6)
	assert_eq(String(langs[0][0]), "de")


func test_switching_language_translates_menu_texts() -> void:
	Settings.set_value("language", "en")
	assert_eq(TranslationServer.get_locale(), "en")
	assert_eq(tr("Rucksack"), "Backpack")
	assert_eq(tr("Welt %d geladen.") % 2, "World 2 loaded.")
	Settings.set_value("language", "pl")
	assert_eq(tr("Einstellungen"), "Ustawienia")
	Settings.set_value("language", "de")
	assert_eq(tr("Rucksack"), "Rucksack", "Deutsch = Original")


func test_labels_follow_the_language_automatically() -> void:
	var l := Label.new()
	l.text = "Einstellungen"
	add_child_autofree(l)
	Settings.set_value("language", "fr")
	await wait_process_frames(2)
	assert_eq(l.tr(l.text), "Réglages")


func test_mono_audio_toggles_the_master_effect() -> void:
	Settings.set_value("mono_audio", true)
	assert_true(AudioBus.is_mono())
	Settings.set_value("mono_audio", false)
	assert_false(AudioBus.is_mono())
