extends SceneTree
## Screenshot einer Szene (für docs/tests/ und Blick-Checks).
## Aufruf (braucht ein Display, z. B. xvfb-run unter Linux):
##   godot --resolution 1920x1080 -s tools/godot/screenshot.gd -- <szene.tscn> <ausgabe.png> [debug] [zoom_h_cm] [pan_x_cm]


func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if args.size() < 2:
		push_error("Aufruf: -- <szene.tscn> <ausgabe.png> [debug] [zoom_h_cm] [pan_x_cm]")
		quit(2)
		return
	var scene: Node = load(args[0]).instantiate()
	root.add_child(scene)
	for _i: int in 6:
		await process_frame
	if args.size() > 2 and args[2] == "debug" and scene.has_node("DebugOverlay"):
		scene.get_node("DebugOverlay").set_enabled(true)
	var cam: Node = scene.get_node_or_null("WorldCamera")
	if cam and args.size() > 3 and float(args[3]) > 0.0:
		cam.set_visible_height(float(args[3]))
	if cam and args.size() > 4:
		cam.position.x = float(args[4])
		cam.pan_by_screen(Vector2.ZERO)
	for _i: int in 6:
		await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = root.get_texture().get_image()
	img.save_png(args[1])
	print("Screenshot: ", args[1], " ", img.get_size())
	quit(0)
