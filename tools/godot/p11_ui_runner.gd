extends Node
## P11-Beweis: Einstellungs-Fenster in mehreren Sprachen (passt alles hinein? Mono-Schalter da?).
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##     res://tools/godot/p11_ui_runner.gd docs/tests/P11


func run(args: PackedStringArray) -> void:
	var out: String = args[0] if args.size() > 0 else "docs/tests/P11"
	DirAccess.make_dir_recursive_absolute(out)
	var bg := ColorRect.new()
	bg.color = Color("#cfe8d0")
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var layer := CanvasLayer.new()
	get_tree().root.add_child(layer)
	layer.add_child(bg)
	for lang: String in ["de", "en", "tr"]:
		Settings.set_value("language", lang)
		var p := SettingsPanel.new()
		p.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		layer.add_child(p)
		for i: int in 6:
			await get_tree().process_frame
		await RenderingServer.frame_post_draw
		get_tree().root.get_texture().get_image().save_jpg(out.path_join("settings_%s.jpg" % lang), 0.85)
		p.queue_free()
		await get_tree().process_frame
	Settings.set_value("language", "de")
	get_tree().quit(0)
