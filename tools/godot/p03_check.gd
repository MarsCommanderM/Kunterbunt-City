extends Node
## P03-Nachweis: misst die Akzeptanzkriterien von Phase 03 (Figuren & Tiere) ZAHLENBASIERT.
## Zwei unabhängige Quellen: (a) Geometrie im Szenenbaum, (b) gerenderte Silhouette pro Item
## (Bilddifferenz mit/ohne Item → exakte Pixel → cm).
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 960x540 -s tools/godot/run.gd -- \
##         res://tools/godot/p03_check.gd [ausgabe.json]

var sb: Node
var drag: DragController
var cam: WorldCamera
var s: Dictionary
var _checks: Array = []
var _last_target = null
var _px_per_cm: float = 1.0


func run(args: PackedStringArray) -> void:
	var out_path: String = args[0] if args.size() > 0 else "/tmp/p03_check.json"
	PetNode.autonomous = false
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	sb = load("res://src/debug/sandbox_characters.tscn").instantiate()
	get_tree().root.add_child(sb)
	await _frames(6)
	drag = sb.drag
	drag.animate = false
	cam = sb.camera
	s = sb.spawned
	_px_per_cm = _calc_px_per_cm()
	print("Maßstab: %.3f Bildpixel pro cm" % _px_per_cm)
	await _haende()
	await _sitzen()
	await _haustier()
	await _tragen()
	await _gesichter()
	await _essen()
	var failed: int = 0
	for c: Dictionary in _checks:
		if not c["ok"]:
			failed += 1
	print("\n════════ P03-Nachweis: %d Prüfungen, %d grün, %d rot ════════" % [_checks.size(), _checks.size() - failed, failed])
	for c: Dictionary in _checks:
		print("  %s  %-46s %s" % ["✅" if c["ok"] else "❌", c["name"], c["detail"]])
	var f := FileAccess.open(out_path, FileAccess.WRITE)
	f.store_string(JSON.stringify(_checks, "\t"))
	f.close()
	print("JSON → ", out_path)
	get_tree().quit(0)


# ---------------------------------------------------------------- 1) Hände & Größenverhältnis
func _haende() -> void:
	var girl: SpriteCharacter = s[&"char_girl_01"]
	var kid: CharacterRig = s[&"kid"]
	var adult: CharacterRig = s[&"adult"]
	await _stage(430.0)
	var girl_h: float = (await _sil_cm([girl])).y
	_add("Mädchen hoch (Soll 125 cm · Tiefe)", absf(girl_h - 125.0 * girl.global_scale.y) < 4.0,
		"%.1f cm" % girl_h)
	var carrot: ItemNode = s[&"food_carrot"]
	var g1: String = give(carrot, girl, 0)
	_add("Karotte → Hand (Mädchen)", g1 == "hand", g1)
	_add("Griff sitzt (Abstand ≤ 1 cm)", _grip_error(carrot) <= 1.0, "%.2f cm" % _grip_error(carrot))
	var carrot_cm: Vector2 = await _sil_cm([carrot])
	_add("Karotte gerendert (Soll 20 cm ±25 %)", absf(carrot_cm.y - 20.0) <= 5.0,
		"%.1f × %.1f cm" % [carrot_cm.x, carrot_cm.y])
	_add("Karotte nicht baseballschlägergroß (< 1/5 Kind)", carrot_cm.y < girl_h * 0.2,
		"%.0f %% der Kind-Größe" % (100.0 * carrot_cm.y / girl_h))
	_add("Finger liegen ÜBER der Karotte", _finger_overlap(girl, carrot),
		"Hand-Overlay überlappt Karotte")
	var apple: ItemNode = s[&"food_apple_red"]
	var apple_cm: Vector2 = await _sil_cm([apple])          ## liegt noch auf dem Tisch
	_add("Apfel gerendert (Soll 8 cm ±2)", absf(apple_cm.y - 8.0) <= 2.0, "%.1f × %.1f cm" % [apple_cm.x, apple_cm.y])
	give(apple, kid, 0)
	var apple_held: Vector2 = apple.global_rect().size / apple.global_scale
	_add("Apfel in der Hand bleibt 8 cm (kein Fußball)", absf(apple_held.y - 8.0 * apple.def.scale_mul) <= 1.5,
		"%.1f × %.1f cm" % [apple_held.x, apple_held.y])
	var ball: ItemNode = s[&"toy_beachball"]
	give(ball, adult, 2)
	var ball_cm: Vector2 = await _sil_cm([ball])
	_add("Wasserball mit zwei Händen (Soll 30 cm ±4)", absf(ball_cm.y - 30.0) <= 4.0,
		"%.1f × %.1f cm" % [ball_cm.x, ball_cm.y])
	var hands: Array = [adult.slot_front.global_position, adult.slot_back.global_position]
	var spread: float = absf(hands[0].x - hands[1].x) / adult.global_scale.x
	_add("Zwei Hände greifen links/rechts am Ball (± Ballbreite)", absf(spread - ball_cm.x) < 8.0,
		"Handabstand %.1f cm, Ball %.1f cm" % [spread, ball_cm.x])


# ---------------------------------------------------------------- 2) Sitzen, Liegen, Teddy
func _sitzen() -> void:
	var kid: CharacterRig = s[&"kid"]
	var adult: CharacterRig = s[&"adult"]
	var toddler: CharacterRig = s[&"toddler"]
	var teddy: ItemNode = s[&"toy_teddy_brown"]
	_add("Kind → Stuhl", seat(kid, s[&"home_chair_mint"], 0) == "seat", "Pose %s" % kid.body_pose)
	var chair: ItemNode = s[&"home_chair_mint"]
	_add("Sitzhöhe Kind = 45 cm (Hüfte über Stuhl-Bodenlinie)",
		absf(_h_over(chair, _hip_y(kid)) - 45.0) <= 2.0, "%.1f cm" % _h_over(chair, _hip_y(kid)))
	_add("Füße des Kindes baumeln über dem Boden (> 5 cm)",
		_h_over(chair, _sole_y(kid)) > 5.0, "%.1f cm" % _h_over(chair, _sole_y(kid)))
	_add("Kopf des sitzenden Kindes ~120 cm (45 + 75)",
		absf(_h_over(chair, kid.global_rect().position.y) - 120.0) <= 6.0,
		"%.1f cm" % _h_over(chair, kid.global_rect().position.y))
	_add("Erwachsene → Sessel", seat(adult, s[&"home_armchair"], 0) == "seat", "Pose %s" % adult.body_pose)
	var arm: ItemNode = s[&"home_armchair"]
	_add("Sitzhöhe Erwachsene = 42 cm (Hüfte über Sessel-Bodenlinie)",
		absf(_h_over(arm, _hip_y(adult)) - 42.0) <= 2.0, "%.1f cm" % _h_over(arm, _hip_y(adult)))
	_add("Füße der Erwachsenen stehen auf dem Boden (±3 cm)",
		absf(_h_over(arm, _sole_y(adult))) <= 3.0, "%.1f cm" % _h_over(arm, _sole_y(adult)))
	_add("Kleinkind → Bett", seat(toddler, s[&"home_bed_kid"], 0) == "seat", "Pose %s" % toddler.body_pose)
	var box: Rect2 = toddler.global_rect()
	var lying: bool = box.size.x / toddler.global_scale.x > 1.5 * box.size.y / toddler.global_scale.y
	_add("Kleinkind LIEGT (breiter als hoch)", lying,
		"%.0f × %.0f cm" % [box.size.x / toddler.global_scale.x, box.size.y / toddler.global_scale.y])
	_add("Liegefläche = 45 cm (Betthöhe ±4)",
		absf(_h_over(s[&"home_bed_kid"], toddler.global_rect().end.y) - 45.0) <= 4.0,
		"%.1f cm" % _h_over(s[&"home_bed_kid"], toddler.global_rect().end.y))
	_add("Kopf bleibt beim Liegen aufrecht", is_zero_approx((toddler.head_pivot as Node2D).global_rotation),
		"Kopf-Rotation %.2f°" % rad_to_deg((toddler.head_pivot as Node2D).global_rotation))
	var dbg_host: ItemNode = Seats.seat_host_of(kid)
	print("  [debug] Kind sitzt auf: %s · Stuhl y=%.1f (scale %.3f) · Sitzpunkt y=%.1f · Kind y=%.1f · Hüfte y=%.1f" % [
		dbg_host.def.id if dbg_host else "nichts", s[&"home_chair_mint"].global_position.y,
		s[&"home_chair_mint"].global_scale.y, Seats.point_global(s[&"home_chair_mint"], 0).y,
		kid.global_position.y, _hip_y(kid)])
	_add("Teddy → Stuhl (45 cm)", seat(teddy, s[&"home_chair_mint_2"], 0) == "seat", "Platz 0")
	var chair2: ItemNode = s[&"home_chair_mint_2"]
	var teddy_bottom: float = (chair2.global_position.y - teddy.global_rect().end.y) / chair2.global_scale.y
	_add("Teddy sitzt auf 45 cm", absf(teddy_bottom - 45.0) <= 2.5, "%.1f cm" % teddy_bottom)
	_add("Teddy-Größe (Soll 30 cm ±4)", absf((await _sil_cm([teddy])).y - 30.0) <= 4.0, "%.1f cm" % (await _sil_cm([teddy])).y)


# ---------------------------------------------------------------- 3) Haustiere
func _haustier() -> void:
	await _stage(520.0)
	var dog: PetNode = s[&"pet_dog_brown"]
	var table: ItemNode = s[&"home_table_wood"]
	var dog_cm: Vector2 = await _sil_cm([dog])
	var table_cm: Vector2 = await _sil_cm([table])
	_add("Hund gerendert (Soll 45 cm · Tiefe)", absf(dog_cm.y - 45.0 * dog.global_scale.y) < 4.0, "%.1f cm" % dog_cm.y)
	_add("Hund kleiner als der Tisch (jede Tiefe)", dog_cm.y < table_cm.y * 0.8,
		"Hund %.1f cm < Tisch %.1f cm" % [dog_cm.y, table_cm.y])
	dog.position = Vector2(s[&"char_girl_01"].position.x + 200.0, dog.position.y)
	await _frames(2)
	var d0: float = dog.position.distance_to(s[&"char_girl_01"].position)
	for _i: int in 600:
		dog.tick(1.0 / 60.0)
	var d1: float = dog.position.distance_to(s[&"char_girl_01"].position)
	_add("Hund folgt der nächsten Figur (10 s)", d1 < d0 - 20.0, "%.0f → %.0f cm" % [d0, d1])
	AudioBus.reset_animal_limiter()
	var barks: Array = [AudioBus.play_animal("pet_dog_bark"), AudioBus.play_animal("pet_dog_bark")]
	_add("Bellen 2× in derselben Sekunde → 1× Ton", barks == [true, false], str(barks))
	AudioBus.clock = func() -> float: return 9.0
	_add("Nach 9 s darf er wieder bellen", AudioBus.play_animal("pet_dog_bark"), "Limitter frei")
	AudioBus.clock = func() -> float: return 0.0


# ---------------------------------------------------------------- 4) Tragen
func _tragen() -> void:
	await _stage(430.0)
	var girl: SpriteCharacter = s[&"char_girl_01"]
	var g: Vector2 = girl.global_position + Vector2(0, -105) * girl.global_scale.y
	drag.press(7, g)
	drag.move(7, g + Vector2(0, -30))
	for i: int in 8:
		drag.move(7, g + Vector2(-30 + i * 9.0, -30))
		drag._process(1.0 / 60.0)
	_add("Beim Tragen 6 cm angehoben", absf(girl.lifted - 1.0) < 0.01, "lifted = %.2f" % girl.lifted)
	_add("Karotte bleibt in der Hand (mit angehoben)", girl.held_item() != null, "hält %s" % (girl.held_item().def.id if girl.held_item() else "nichts"))
	drag.release(7, g + Vector2(40, 0))
	_add("Abgesetzt: nicht mehr angehoben", absf(girl.lifted) < 0.01, "lifted = %.2f" % girl.lifted)
	var toddler: CharacterRig = s[&"toddler"]
	var tg: Vector2 = drag.grab_point(toddler)
	drag.press(8, tg)
	drag.move(8, tg + Vector2(0, -40))
	for i: int in 10:
		drag.move(8, tg + Vector2(i * 14.0, -60))
		drag._process(1.0 / 60.0)
	_add("Figur pendelt am Griffpunkt", absf(toddler.swing.rotation) > 0.05, "%.3f rad" % toddler.swing.rotation)
	drag.release(8, tg + Vector2(140, 20))
	_add("Abgesetzt: Pendel zurück, steht", is_zero_approx(toddler.swing.rotation),
		"Pendel %.3f, Pose %s" % [toddler.swing.rotation, toddler.body_pose])


# ---------------------------------------------------------------- 5) Gefühle & Essen
func _gesichter() -> void:
	var kid: CharacterRig = s[&"kid"]
	var seen: Array = []
	for _k: int in 6:
		seen.append(kid.emotion)
		var hc: Vector2 = kid.parts.to_global(Vector2(0, -float(kid.t["head"]["cy"])))
		drag.press(9, hc)
		drag.release(9, hc)
		await _frames(2)
	_add("Sechs Gefühle durchschaltbar", seen.size() == 6 and _unique(seen) == 6, " / ".join(seen))


func _essen() -> void:
	var kid: CharacterRig = s[&"kid"]
	var ice: ItemNode = s[&"food_icecream_3"]
	var mouth: Vector2 = kid.mouth_global()
	var off: Vector2 = ice.global_position - ice.global_rect().get_center()
	drag.scripted_move(ice, mouth + off)
	await _frames(3)
	_add("Eis am Mund wird gegessen", not is_instance_valid(ice) or ice.is_queued_for_deletion(), "Item weg")
	_add("Gesicht danach verliebt", kid.emotion == "love", "Gefühl %s" % kid.emotion)


# ---------------------------------------------------------------- Messwerkzeug
## Gerenderte Größe eines Items in cm – Bilddifferenz mit/ohne Item (nur sichtbare Pixel zählen).
func _sil_cm(items: Array) -> Vector2:
	var r: Rect2i = await _silhouette(items)
	return Vector2(r.size) / _px_per_cm


## Bounding-Box (Bildpixel) aller Pixel, die sich ändern, wenn die Items ausgeblendet werden.
func _silhouette(items: Array) -> Rect2i:
	var box := Rect2()
	var first: bool = true
	for it: Node2D in items:
		var r: Rect2 = it.global_rect().grow(8.0 * it.global_scale.x)
		box = r if first else box.merge(r)
		first = false
	var a: Image = await _snap()
	var hidden: Array = []
	for it: Node2D in items:
		for sp: Sprite2D in _visuals_of(it):
			sp.visible = false
			hidden.append(sp)
	var b: Image = await _snap()
	for sp: Sprite2D in hidden:
		sp.visible = true
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
				var p := Vector2i(x, y)
				out = Rect2i(p, Vector2i.ONE) if not found else out.expand(p)
				found = true
	return out


## Sichtbare Sprite-Ebenen eines Nodes (der Kontaktschatten aus _draw bleibt an → zählt nicht mit).
func _visuals_of(n: Node) -> Array[Sprite2D]:
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
	var vr: Vector2 = get_viewport().get_visible_rect().size
	return ct.get_scale().y * img.get_height() / vr.y


func _to_img(world: Vector2) -> Vector2:
	var ct: Transform2D = get_tree().root.get_canvas_transform()
	var img: Image = get_tree().root.get_texture().get_image()
	var vr: Vector2 = get_viewport().get_visible_rect().size
	return ct * world * Vector2(img.get_size()) / vr


## Höhe (cm) einer Welt-y über der Bodenlinie von `ref` (das Möbel steht auf dem Boden).
func _h_over(ref: ItemNode, world_y: float) -> float:
	return (ref.global_position.y - world_y) / ref.global_scale.y


func _hip_y(ch: CharacterRig) -> float:
	return ch.parts.to_global(Vector2(0, -float(ch.t["hip"]["y"]))).y


func _sole_y(ch: CharacterRig) -> float:
	var sp: Sprite2D = ch._layers["Shoes"]
	return (sp.global_transform * sp.get_rect()).end.y


## Liegt das Hand-Overlay (Faust) über dem Item? → Differenz des Overlays schneidet das Item.
func _finger_overlap(girl: SpriteCharacter, item: ItemNode) -> bool:
	if girl.hand_overlay == null or not girl.hand_overlay.visible:
		return false
	var ov: Sprite2D = girl.hand_overlay
	if ov == null:
		return false
	var a: Rect2 = ov.global_transform * ov.get_rect()
	return a.intersects(item.global_rect()) and a.get_center().y > item.global_rect().get_center().y - item.global_rect().size.y * 0.5


func give(item: ItemNode, who: ItemNode, index: int) -> String:
	var slot: Dictionary = {}
	_last_target = null
	for h: Dictionary in who.hand_slots():
		if int(h["index"]) == index:
			slot = h
	if slot.is_empty():
		return "keine freie Hand"
	var grip_off: Vector2 = PlacementCharacter.grip_global(item, Vector2.ZERO)
	var res: Array = []
	drag.item_dropped.connect(func(_i: ItemNode, t: Placement.Target) -> void: res.append(t.kind), CONNECT_ONE_SHOT)
	drag.scripted_move(item, (slot["global"] as Vector2) - grip_off + Vector2(3, 2))
	var got: ItemNode = who.held_item(index) if who.has_method("held_item") else null
	return "hand" if got == item else "kein Halt (%s)" % str(res)


func seat(item: ItemNode, host: ItemNode, i: int) -> String:
	var p: Vector2 = Seats.point_global(host, i)
	if item.has_method("hip_offset"):
		p -= item.hip_offset() * item.global_scale.y
	var res: Array = []
	drag.item_dropped.connect(func(_i: ItemNode, t: Placement.Target) -> void: res.append(t.kind), CONNECT_ONE_SHOT)
	drag.scripted_move(item, p + Vector2(6, -8))
	return "seat" if Seats.seat_host_of(item) == host else "kein Platz (%s)" % str(res)


func _grip_error(item: ItemNode) -> float:
	var slot: Node2D = item.get_parent()
	return item.to_global((item.def.grip - item.def.pivot) * item.draw_size()).distance_to(slot.global_position)


func _unique(a: Array) -> int:
	var d: Dictionary = {}
	for v: Variant in a:
		d[v] = true
	return d.size()


func _stage(x: float) -> void:
	cam.position = Vector2(x, cam.position.y)
	cam.pan_by_screen(Vector2.ZERO)
	await _frames(2)


func _add(name: String, ok: bool, detail: String) -> void:
	_checks.append({"name": name, "ok": ok, "detail": detail})


func _frames(n: int) -> void:
	for _i: int in n:
		await get_tree().process_frame
