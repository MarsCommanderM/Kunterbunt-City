extends GutTest
## Rauchtest: Projekt startet, alle 7 Autoloads existieren, Grundeinstellungen stimmen.

const AUTOLOADS: Array[String] = ["Log", "Settings", "ItemDB", "SaveSystem", "Game", "SceneRouter", "AudioBus"]


func test_all_autoloads_present() -> void:
	for autoload_name: String in AUTOLOADS:
		assert_not_null(get_tree().root.get_node_or_null(autoload_name), "Autoload fehlt: " + autoload_name)


func test_viewport_base_is_1080p() -> void:
	assert_eq(ProjectSettings.get_setting("display/window/size/viewport_width"), 1920)
	assert_eq(ProjectSettings.get_setting("display/window/size/viewport_height"), 1080)


func test_renderer_is_compatibility() -> void:
	assert_eq(ProjectSettings.get_setting("rendering/renderer/rendering_method"), "gl_compatibility")


func test_touch_does_not_emulate_mouse() -> void:
	assert_false(ProjectSettings.get_setting("input_devices/pointing/emulate_mouse_from_touch"))


func test_settings_defaults() -> void:
	assert_eq(Settings.get_value("language"), "de")
