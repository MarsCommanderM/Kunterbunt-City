extends Node
## P03-Geometrie-Dump: jede Figur-Ebene in cm über dem Standpunkt der Figur (Füße = 0).
## Beweis statt Augenmaß – die Zahlen wandern 1:1 in tests/test_character.gd.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1280x720 -s tools/godot/run.gd -- \
##         res://tools/godot/p03_pose_dump.gd [ausgabe.json]

var _out_path: String


func run(args: PackedStringArray) -> void:
	_out_path = args[0] if args.size() > 0 else "/tmp/p03_pose_dump.json"
	PetNode.autonomous = false
	AudioBus.clock = func() -> float: return 0.0
	var sb: Node = load("res://src/debug/sandbox_characters.tscn").instantiate()
	get_tree().root.add_child(sb)
	await _frames(6)
	var rows: Array = []
	for key: StringName in [&"adult", &"kid", &"toddler", &"char_girl_01"]:
		var ch: ItemNode = sb.spawned[key]
		var is_rig: bool = ch is CharacterRig
		for pose: String in (["stand", "sit", "lie"] if is_rig else ["stand"]):
			if is_rig:
				(ch as CharacterRig).refresh_pose(false)   # erst Umgebung, dann Pose erzwingen
				(ch as CharacterRig)._set_body_pose(pose)
				(ch as CharacterRig)._apply_arms(
					CharacterRig.ARM_IDLE, CharacterRig.ARM_IDLE)
			await _frames(1)
			var row: Dictionary = _measure(ch, key, pose)
			rows.append(row)
			_print(row)
	var f := FileAccess.open(_out_path, FileAccess.WRITE)
	f.store_string(JSON.stringify(rows, "\t"))
	f.close()
	print("JSON → ", _out_path)
	get_tree().quit(0)


func _measure(ch: ItemNode, key: StringName, pose: String) -> Dictionary:
	var foot: float = ch.global_position.y                 ## Standpunkt der Figur (Boden-Linie)
	var s: float = ch.global_scale.y
	var hip_y: float = foot
	if ch.has_method("hip_offset"):
		hip_y = foot + (ch.hip_offset() * s).y
	var layers: Array = []
	var box: Rect2 = Rect2()
	if ch is CharacterRig:
		var rig: CharacterRig = ch
		for lname: String in rig._layers.keys():
			var sp: Sprite2D = rig._layers[lname]
			if not sp.is_visible_in_tree():
				continue
			var r: Rect2 = sp.global_transform * sp.get_rect()
			layers.append({
				"layer": lname,
				"tint": _tint_name(rig, sp),
				"y_bot": _cm(foot, r.end.y, s),
				"y_top": _cm(foot, r.position.y, s),
				"x_l": _x(ch.global_position.x, r.position.x, s),
				"x_r": _x(ch.global_position.x, r.end.x, s),
			})
			box = box.merge(r) if box.has_area() else r
	else:
		var sp2: Sprite2D = ch.sprite
		if sp2:
			var r2: Rect2 = sp2.global_transform * sp2.get_rect()
			box = r2
	return {
		"who": key, "pose": pose, "scale": s,
		"hip_cm": _cm(foot, hip_y, s),
		"body_bot_cm": _cm(foot, box.end.y, s),
		"body_top_cm": _cm(foot, box.position.y, s),
		"width_cm": roundf(box.size.x / s * 10.0) / 10.0,
		"layers": layers,
	}


func _cm(foot: float, y: float, s: float) -> float:
	return roundf((foot - y) / s * 10.0) / 10.0


func _x(cx: float, x: float, s: float) -> float:
	return roundf((x - cx) / s * 10.0) / 10.0


func _tint_name(rig: CharacterRig, sp: Sprite2D) -> String:
	var look: Dictionary = rig.look
	for k: String in ["skin", "hair", "shirt", "pants", "shoes"]:
		if look.has(k):
			if sp.modulate.is_equal_approx(Color(String(look[k]))):
				return k
	return "-" if sp.modulate.is_equal_approx(Color.WHITE) else "?"


func _print(row: Dictionary) -> void:
	print("── %s · %s · scale %.3f · Hüfte %.1f cm · Körper %.1f … %.1f cm (breit %.1f)" % [
		row["who"], row["pose"], row["scale"], row["hip_cm"], row["body_bot_cm"], row["body_top_cm"], row["width_cm"]])
	for l: Dictionary in row["layers"]:
		print("     %-14s %-6s y %6.1f … %6.1f   x %6.1f … %6.1f" % [
			l["layer"], l["tint"], l["y_bot"], l["y_top"], l["x_l"], l["x_r"]])


func _frames(n: int) -> void:
	for _i: int in n:
		await get_tree().process_frame
