extends Control
## Einstiegsszene (vorläufig). Wird in Phase 05 durch Splash → Editor/Stadtkarte ersetzt.
## Bis dahin: Titel + Knopf zur Maßstab-Testszene (Phase 01).

const SCALE_TEST: String = "res://src/debug/scale_test.tscn"


func _ready() -> void:
	Log.info("Kunterbunt City %s gestartet" % ProjectSettings.get_setting("application/config/version"))
	var btn := Button.new()
	btn.text = "  📏  Maßstab-Test öffnen  "
	btn.add_theme_font_size_override("font_size", UiConstants.FONT_HUD + 10)
	btn.custom_minimum_size = Vector2(520, 110)
	btn.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	btn.position += Vector2(-260, -260)
	btn.pressed.connect(func() -> void: get_tree().change_scene_to_file(SCALE_TEST))
	add_child(btn)
	var sub := Label.new()
	sub.text = "Phase 01 · Welt in Zentimetern · Godot %s" % Engine.get_version_info()["string"]
	sub.add_theme_font_size_override("font_size", UiConstants.FONT_HUD)
	sub.add_theme_color_override("font_color", UiConstants.COLOR_HUD_TEXT)
	sub.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.position += Vector2(-sub.get_minimum_size().x * 0.5, 90)
	add_child(sub)
