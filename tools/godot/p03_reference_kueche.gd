extends Node
## P03-T10: Referenz-Küche nachbauen und NACHMESSEN.
## Baut dieselbe Szene wie reference/kueche_stil_c_massstab.png im echten Raum auf (gleiche Sprites,
## gleiche cm-Positionen, gleiche Kamera: 300 cm hoch, 16:9) und misst jedes Objekt per Silhouette.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p03_reference_kueche.gd docs/tests/P03

var sb: Node
var drag: DragController
var cam: WorldCamera
var out_dir: String
var _px_per_cm: float = 3.6


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else "docs/tests/P03"
	DirAccess.make_dir_recursive_absolute(out_dir)
	PetNode.autonomous = false
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	sb = load("res://src/debug/sandbox_reference_kitchen.tscn").instantiate()
	get_tree().root.add_child(sb)
	await _frames(6)
	drag = sb.drag
	drag.animate = false
	cam = sb.camera
	var s: Dictionary = sb.spawned
	var girl: SpriteCharacter = s[&"char_girl_01"]

	# Karotte in die Hand (wie im Referenzbild)
	var carrot: ItemNode = ItemSpawner.on_surface(sb.room, &"food_carrot", &"counter_top", 300.0)
	var slot: Dictionary = girl.hand_slots()[0]
	drag.scripted_move(carrot, (slot["global"] as Vector2) - PlacementCharacter.grip_global(carrot, Vector2.ZERO))
	await _frames(3)

	# Kamera wie im Referenzbild: 300 cm hoch, Ausschnitt ab x = 228 px, Unterkante bei y = 744 px
	cam.set_visible_height(300.0)
	cam.position = Vector2(SandboxReferenceKitchen.cm_x(228.0) + 300.0 * 16.0 / 9.0 * 0.5,
		SandboxReferenceKitchen.depth_y(744.0) - 150.0)
	cam.pan_by_screen(Vector2.ZERO)
	await _frames(3)
	_px_per_cm = _calc_px_per_cm()

	print("── Referenz-Küche: Soll (Tabelle × Tiefen-Faktor) gegen gemessene Bildgröße")
	var rows: Array = []
	var worst: float = 0.0
	for key: StringName in s:
		var it: ItemNode = s[key]
		if it == null:
			continue
		var want: float = it.def.height_cm * it.global_scale.y
		var got: float = (await _sil_cm([it])).y
		var dev: float = absf(got - want) / maxf(want, 1.0) * 100.0
		worst = maxf(worst, dev)
		rows.append({"id": str(key), "soll_cm": want, "ist_cm": got, "abweichung_prozent": dev})
		print("   %-24s soll %6.1f cm · gemessen %6.1f cm · Δ %4.1f %%   %s" % [
			str(key), want, got, dev, "✅" if dev <= 8.0 else "❌"])
	var chair: ItemNode = s[&"home_chair_mint"]
	var teddy: ItemNode = s[&"toy_teddy_brown"]
	var seat_h: float = (chair.global_position.y - teddy.global_rect().end.y) / chair.global_scale.y
	print("   Teddy sitzt auf %.1f cm (Stuhl-Sitzhöhe %.0f cm)  %s" % [
		seat_h, chair.def.seat_h_cm, "✅" if absf(seat_h - chair.def.seat_h_cm) <= 2.5 else "❌"])
	var car: Vector2 = await _sil_cm([carrot])
	print("   %-24s soll %6.1f cm · gemessen %6.1f cm · Δ %4.1f %%" % [
		"food_carrot (in Hand)", carrot.def.height_cm * carrot.global_scale.y, car.y,
		absf(car.y - carrot.def.height_cm * carrot.global_scale.y) / (carrot.def.height_cm * carrot.global_scale.y) * 100.0])
	print("   größte Abweichung: %.1f %%" % worst)

	await RenderingServer.frame_post_draw
	get_tree().root.get_texture().get_image().save_jpg(out_dir.path_join("p03_13_referenz_kueche.jpg"), 0.9)
	print("Screenshot: p03_13_referenz_kueche.jpg")
	var f := FileAccess.open(out_dir.path_join("p03_13_referenz_kueche.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rows, "\t"))
	f.close()
	get_tree().quit(0)


func _sil_cm(items: Array) -> Vector2:
	var r: Rect2i = await _silhouette(items)
	return Vector2(r.size) / _px_per_cm


func _silhouette(items: Array) -> Rect2i:
	var box := Rect2()
	var first: bool = true
	for it: Node2D in items:
		var r: Rect2 = it.global_rect().grow(8.0 * it.global_scale.x)
		box = r if first else box.merge(r)
		first = false
	var hidden: Array = []
	for it: Node2D in items:
		for sp: Sprite2D in _visuals(it):
			sp.visible = false
			hidden.append(sp)
	var b: Image = await _snap()
	for sp: Sprite2D in hidden:
		sp.visible = true
	var a: Image = await _snap()
	await _frames(1)
	var x0: int = maxi(0, int(_to_img(box.position).x))
	var y0: int = maxi(0, int(_to_img(box.position).y))
	var x1: int = mini(b.get_width() - 1, int(_to_img(box.end).x))
	var y1: int = mini(b.get_height() - 1, int(_to_img(box.end).y))
	var out := Rect2i()
	var found: bool = false
	for y: int in range(y0, y1 + 1):
		for x: int in range(x0, x1 + 1):
			if a.get_pixel(x, y) != b.get_pixel(x, y):
				out = Rect2i(Vector2i(x, y), Vector2i.ONE) if not found else out.expand(Vector2i(x, y))
				found = true
	return out


func _visuals(n: Node) -> Array[Sprite2D]:
	var out: Array[Sprite2D] = []
	if n is CharacterRig:
		for sp: Variant in (n as CharacterRig)._layers.values():
			if (sp as Sprite2D).is_visible_in_tree():
				out.append(sp)
	elif n is SpriteCharacter and (n as SpriteCharacter).sprite:
		out.append((n as SpriteCharacter).sprite)
	elif n is ItemNode and (n as ItemNode).sprite:
		out.append((n as ItemNode).sprite)
	return out


func _snap() -> Image:
	await _frames(2)
	await RenderingServer.frame_post_draw
	var img: Image = get_tree().root.get_texture().get_image()
	img.convert(Image.FORMAT_RGBA8)
	return img


func _calc_px_per_cm() -> float:
	var ct: Transform2D = get_tree().root.get_canvas_transform()
	var img: Image = get_tree().root.get_texture().get_image()
	return ct.get_scale().y * img.get_height() / get_viewport().get_visible_rect().size.y


func _to_img(world: Vector2) -> Vector2:
	var ct: Transform2D = get_tree().root.get_canvas_transform()
	var img: Image = get_tree().root.get_texture().get_image()
	return ct * world * Vector2(img.get_size()) / get_viewport().get_visible_rect().size


func _frames(n: int) -> void:
	for _i: int in n:
		await get_tree().process_frame
