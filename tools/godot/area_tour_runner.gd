extends Node
## P10-Beweis (für jeden Bereich gleich): betritt die Bereiche, geht durch alle Räume, macht je Raum ein Bild und
## zählt Items/NPCs. Aufruf:
##   xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##       res://tools/godot/area_tour_runner.gd docs/tests/P10 school [zoo …]

var out_dir: String = "docs/tests/P10"
var _m: Dictionary = {}


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else out_dir
	DirAccess.make_dir_recursive_absolute(out_dir)
	CharacterRig.animate_poses = false
	PetNode.autonomous = false
	NpcBrain.autonomous = false
	AudioBus.clock = func() -> float: return 0.0
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	Game.characters.clear()
	Game.pets.clear()
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#e2ab80"
	Game.add_character(c)
	Game.set_active(c.id)
	for i: int in range(1, args.size()):
		var area_id := StringName(args[i])
		SceneRouter.pending_area = area_id
		var a: AreaScene = load("res://src/world/area_scene.tscn").instantiate()
		get_tree().root.add_child(a)
		await _frames(8)
		var tour: Array = []
		for rid: Variant in a.room_ids():
			a.switch_room(String(rid))
			await _frames(4)
			if a.room.width_cm > 1200.0:
				a.camera.set_visible_height(minf(560.0, float(a.room.camera_cfg.get("max_h_cm", 560.0))))
				await _frames(2)
			tour.append("%s:%d/%d" % [rid, Placement.all_items(a.room).size(), a.npcs.size()])
			await _shot("%s_%s" % [area_id, rid])
		_m[String(area_id)] = {"raeume": tour, "ladezeit_ms": round(a.load_ms)}
		a.queue_free()
		await _frames(3)
	var f := FileAccess.open(out_dir.path_join("tour_%s.json" % "_".join(args.slice(1))), FileAccess.WRITE)
	f.store_string(JSON.stringify(_m, "  "))
	f.close()
	print(JSON.stringify(_m))
	get_tree().quit(0)


func _frames(n: int) -> void:
	for i: int in n:
		await get_tree().process_frame
	await RenderingServer.frame_post_draw


func _shot(name: String) -> void:
	await _frames(3)
	var img: Image = get_tree().root.get_texture().get_image()
	if img != null:
		img.save_jpg(out_dir.path_join(name + ".jpg"), 0.86)
		print("Screenshot: %s" % name)
