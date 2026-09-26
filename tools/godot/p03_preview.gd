extends Node
## Schneller Blick auf die Figuren-Sandbox (Entwicklung, kein Beweis).
func run(args: PackedStringArray) -> void:
	PetNode.autonomous = false
	var sb: Node = load("res://src/debug/sandbox_characters.tscn").instantiate()
	get_tree().root.add_child(sb)
	for i: int in 8:
		await get_tree().process_frame
	await RenderingServer.frame_post_draw
	get_tree().root.get_texture().get_image().save_png(args[0] if args.size() > 0 else "/tmp/p03_prev.png")
	get_tree().quit(0)
