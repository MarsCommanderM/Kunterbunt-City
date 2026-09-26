extends Node
## Beweis-Screenshots Phase 03: Figuren & Tiere in der Figuren-Sandbox – bedient über die DragController-API
## wie ein Kind (greifen, ziehen, loslassen). Reproduzierbar: Pose-Tweens aus, Tiere nur per tick().
## Jedes Bild wird zusätzlich darauf geprüft, dass die gemeinten Dinge vollständig im Bild sind.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p03_scenario_runner.gd docs/tests/P03

const W: float = 1920.0
const H: float = 1080.0

var sb: Node
var drag: DragController
var cam: WorldCamera
var out_dir: String


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else "docs/tests/P03"
	DirAccess.make_dir_recursive_absolute(out_dir)
	PetNode.autonomous = false
	CharacterRig.animate_poses = false
	AudioBus.clock = func() -> float: return 0.0
	sb = load("res://src/debug/sandbox_characters.tscn").instantiate()
	get_tree().root.add_child(sb)
	await _frames(6)
	drag = sb.drag
	drag.animate = false
	cam = sb.camera
	var s: Dictionary = sb.spawned
	var girl: SpriteCharacter = s[&"char_girl_01"]
	var kid: CharacterRig = s[&"kid"]
	var adult: CharacterRig = s[&"adult"]
	var toddler: CharacterRig = s[&"toddler"]

	# 1) Übersicht: ganzer Raum (Kamerahöhe 400 cm → 711 cm Breite)
	await _stage(360.0, 400.0)
	await _shot("p03_01_sandbox_figuren.jpg", [girl, kid, adult, toddler])

	# 2) Karotte (20 cm) vom Tisch in die Hand des Mädchens (125 cm)
	var carrot: ItemNode = s[&"food_carrot"]
	print("Karotte → Mädchen: ", give(carrot, girl, 0))
	print("  Griff-Abstand zur Hand (cm): %.2f" % _grip_error(carrot))
	await _frame([girl, carrot])
	await _shot("p03_02_karotte_hand_maedchen.jpg", [girl, carrot])
	await _shot_crop("p03_03_karotte_hand_zoom.jpg", girl.hand_overlay.global_position, 46.0, 0.0)

	# 3) Apfel in die Hand des Kindes, Wasserball mit beiden Händen zur Erwachsenen
	print("Apfel → Kind (vorne): ", give(s[&"food_apple_red"], kid, 0))
	print("Wasserball → Erwachsene (zwei Hände): ", give(s[&"toy_beachball"], adult, 2))
	await _frame([kid, adult, s[&"food_apple_red"], s[&"toy_beachball"]])
	await _shot("p03_04_hand_eins_und_zwei.jpg", [kid, adult, s[&"food_apple_red"], s[&"toy_beachball"]])

	# 4) Hinsetzen: Kind auf den Stuhl (45), Erwachsene in den Sessel (42), Teddy auf den 2. Stuhl (45)
	print("Kind → Stuhl: ", seat(kid, s[&"home_chair_mint"], 0))
	print("Erwachsene → Sessel: ", seat(adult, s[&"home_armchair"], 0))
	print("Teddy → Stuhl: ", seat(s[&"toy_teddy_brown"], s[&"home_chair_mint_2"], 0))
	var chair: ItemNode = s[&"home_chair_mint"]
	print("  Sitzhöhe Stuhl (Hüfte über Bodenlinie, cm): %.1f" % _h_over(chair, _hip_y(kid)))
	print("  Füße Kind über Boden (cm): %.1f   Erwachsene: %.1f" % [
		_h_over(chair, _sole_y(kid)), _h_over(s[&"home_armchair"], _sole_y(adult))])
	await _frame([kid, adult, s[&"toy_teddy_brown"], s[&"home_chair_mint"],
		s[&"home_armchair"], s[&"home_chair_mint_2"]])
	await _shot("p03_05_sitzen_und_teddy.jpg", [kid, adult, s[&"toy_teddy_brown"], s[&"home_chair_mint"],
		s[&"home_armchair"], s[&"home_chair_mint_2"]])

	# 5) Kleinkind ins Bett legen (Pose lie, Kopf aufrecht)
	print("Kleinkind → Bett: ", seat(toddler, s[&"home_bed_kid"], 0))
	print("  Liegehöhe (cm über Bodenlinie Bett): %.1f" % _h_over(s[&"home_bed_kid"], toddler.global_rect().end.y))
	await _frame([toddler, s[&"home_bed_kid"]])
	await _shot("p03_06_kleinkind_liegt_im_bett.jpg", [toddler, s[&"home_bed_kid"]])

	# 6) Mädchen tragen: am Kopf greifen, schnell ziehen → Hand hält die Karotte weiter
	await _frame([girl], 40.0)
	var g: Vector2 = girl.global_position + Vector2(0, -105) * girl.global_scale.y
	drag.press(7, g)
	drag.move(7, g + Vector2(0, -30))
	for i: int in 8:
		drag.move(7, g + Vector2(-30 + i * 9.0, -30))
		drag._process(1.0 / 60.0)
	await _shot("p03_07_maedchen_getragen.jpg", [girl])
	drag.release(7, g + Vector2(40, 0))
	# Schablonen-Figur tragen: Arme hoch + Pendeln am Griffpunkt
	var tg: Vector2 = drag.grab_point(kid)
	drag.press(8, tg)
	drag.move(8, tg + Vector2(0, -40))
	for i: int in 10:
		drag.move(8, tg + Vector2(i * 14.0, -60))
		drag._process(1.0 / 60.0)
	print("  Pendel-Winkel beim Tragen (rad): %.3f" % kid.swing.rotation)
	await _frame([kid], 80.0)
	await _shot("p03_08_kind_getragen_pendelt.jpg", [kid])
	drag.release(8, tg + Vector2(140, 20))
	print("  Kind abgesetzt: Pose=%s, Pendel=%.2f" % [kid.body_pose, kid.swing.rotation])

	# 7) Sechs Gesichter (Kopf antippen schaltet weiter)
	await _faces_strip(kid)

	# 8) Essen: Eis an den Mund des Kindes → Mampf → weg, Gesicht verliebt
	var ice: ItemNode = s[&"food_icecream_3"]
	var mouth: Vector2 = kid.mouth_global()
	var off: Vector2 = ice.global_position - ice.global_rect().get_center()
	await _frame([kid])
	drag.scripted_move(ice, mouth + off)
	await _frames(3)
	print("Eis gegessen: ", not is_instance_valid(ice) or ice.is_queued_for_deletion(), " · Gesicht: ", kid.emotion)
	await _shot("p03_10_eis_gegessen_verliebt.jpg", [kid])

	# 9) Hund folgt der nächsten Figur (10 s Simulation) + Maßstabsreihe
	var dog: PetNode = s[&"pet_dog_brown"]
	dog.position = Vector2(girl.position.x + 180.0, dog.position.y)   ## erst Abstand, dann folgt er
	var start: Vector2 = dog.position
	for i: int in 420:
		dog.tick(1.0 / 60.0)
	print("Hund: Abstand %.0f cm → %.0f cm (Modus %d)" % [
		absf(start.x - girl.position.x), absf(dog.position.x - girl.position.x), dog.mode])
	await _frame([dog, girl], 60.0)
	await _shot("p03_11_hund_folgt.jpg", [dog, girl])

	# 10) Maßstabsreihe: alle vier Figuren + Hund + Tisch nebeneinander
	await _massstabsreihe()
	get_tree().quit(0)


## Alle Figuren in einer Reihe vor dem Tisch – der „Hund nicht größer als der Tisch“-Beweis in einem Bild.
func _massstabsreihe() -> void:
	var s: Dictionary = sb.spawned
	var row: Array = [s[&"home_table_wood"], s[&"pet_dog_brown"], s[&"toddler"], s[&"kid"],
		s[&"char_girl_01"], s[&"adult"]]
	var x: float = 120.0
	for it: ItemNode in row:
		it.slot_index = -1
		if it.get_parent():
			it.get_parent().remove_child(it)
		sb.room.ysort_root.add_child(it)
		it.position = Vector2(x, 60.0)
		it.scale = sb.room.floor_band.depth_factor(60.0) * Vector2.ONE
		if it.has_method("refresh_pose"):
			it.refresh_pose(false)
		x += it.def.width_cm * 0.75 + 60.0
	await _frames(4)
	await _frame(row)
	await _shot("p03_12_massstabsreihe.jpg", row)


# ---------------------------------------------------------------- Werkzeug
func give(item: ItemNode, who: ItemNode, index: int) -> String:
	var slot: Dictionary = {}
	for h: Dictionary in who.hand_slots():
		if int(h["index"]) == index:
			slot = h
	if slot.is_empty():
		return "keine freie Hand"
	var grip_off: Vector2 = PlacementCharacter.grip_global(item, Vector2.ZERO)
	drag.scripted_move(item, (slot["global"] as Vector2) - grip_off + Vector2(3, 2))
	return "hand" if who.held_item(index) == item else "nicht gegriffen"


func seat(item: ItemNode, host: ItemNode, i: int) -> String:
	var p: Vector2 = Seats.point_global(host, i)
	if item.has_method("hip_offset"):
		p -= item.hip_offset() * item.global_scale.y
	drag.scripted_move(item, p + Vector2(6, -8))
	return "seat" if Seats.seat_host_of(item) == host else "kein Platz"


func _grip_error(item: ItemNode) -> float:
	var slot: Node2D = item.get_parent()
	return item.to_global((item.def.grip - item.def.pivot) * item.draw_size()).distance_to(slot.global_position)


func _h_over(ref: ItemNode, world_y: float) -> float:
	return (ref.global_position.y - world_y) / ref.global_scale.y


func _hip_y(ch: CharacterRig) -> float:
	return ch.parts.to_global(Vector2(0, -float(ch.t["hip"]["y"]))).y


func _sole_y(ch: CharacterRig) -> float:
	var sp: Sprite2D = ch._layers["Shoes"]
	return (sp.global_transform * sp.get_rect()).end.y


## Bildausschnitt aus den Objekten selbst berechnen: Hülle + 12 % Rand, Höhe geklemmt auf 220…400 cm.
func _frame(nodes: Array, extra_h: float = 0.0) -> void:
	var box := Rect2()
	var first: bool = true
	for n: Node2D in nodes:
		var r: Rect2 = n.global_rect()
		box = r if first else box.merge(r)
		first = false
	if not box.has_area():
		return
	var h_cm: float = maxf(box.size.y * 1.24 + extra_h, box.size.x * 1.24 * H / W)
	cam.set_visible_height(clampf(h_cm, 220.0, 400.0))
	cam.position = box.get_center()
	cam.pan_by_screen(Vector2.ZERO)
	await _frames(2)


func _stage(x: float, h_cm: float, y: float = NAN) -> void:
	cam.set_visible_height(h_cm)
	cam.position = Vector2(x, cam.position.y if is_nan(y) else y)
	cam.pan_by_screen(Vector2.ZERO)
	await _frames(2)


func _faces_strip(rig: CharacterRig) -> void:
	await _frame([rig], -20.0)
	var strip := Image.create(6 * 300, 330, false, Image.FORMAT_RGB8)
	strip.fill(Color(1, 0.97, 0.92))
	for k: int in 6:
		if k > 0:
			var hc: Vector2 = rig.parts.to_global(Vector2(0, -float(rig.t["head"]["cy"])))
			drag.press(9, hc)
			drag.release(9, hc)
		await _frames(3)
		await RenderingServer.frame_post_draw
		var img: Image = get_tree().root.get_texture().get_image()
		img.convert(Image.FORMAT_RGB8)
		var hc_s: Vector2 = get_tree().root.get_canvas_transform() * rig.parts.to_global(
			Vector2(0, -float(rig.t["head"]["cy"])))
		var head_px := Rect2i(Vector2i(hc_s) - Vector2i(150, 165), Vector2i(300, 330))
		strip.blit_rect(img, head_px, Vector2i(k * 300, 0))
		print("  Gesicht %d: %s" % [k + 1, rig.emotion])
	strip.save_jpg(out_dir.path_join("p03_09_sechs_gesichter.jpg"), 0.9)
	print("Screenshot: p03_09_sechs_gesichter.jpg")
	rig.set_emotion("happy")


func _shot(name: String, watch: Array = []) -> void:
	await _frames(4)
	await RenderingServer.frame_post_draw
	get_tree().root.get_texture().get_image().save_jpg(out_dir.path_join(name), 0.9)
	print("Screenshot: %s  %s" % [name, _frame_report(watch)])


## Ausschnitt in Originalauflösung: center_world ± Größe (cm) – für Hand- und Gesicht-Details.
func _shot_crop(name: String, center_world: Vector2, w_cm: float, _h_cm: float) -> void:
	await _frames(4)
	await RenderingServer.frame_post_draw
	var img: Image = get_tree().root.get_texture().get_image()
	var px: float = _px_per_cm()
	var size := Vector2i(maxf(32.0, w_cm * px), maxf(32.0, w_cm * px * H / W))
	var c: Vector2i = Vector2i(_to_img(center_world))
	var r := Rect2i(c - size / 2, size)
	r.position = r.position.clamp(Vector2i.ZERO, Vector2i(img.get_size()) - size)
	img = img.get_region(r)
	img.resize(int(W * 0.5), int(H * 0.5), Image.INTERPOLATE_LANCZOS)
	img.save_jpg(out_dir.path_join(name), 0.92)
	print("Screenshot: %s (Ausschnitt %.0f cm, %d×%d px)" % [name, w_cm, img.get_width(), img.get_height()])


## Stimmt das Bild? Meldet, ob die gemeinten Objekte vollständig im Bild liegen.
func _frame_report(watch: Array) -> String:
	if watch.is_empty():
		return ""
	var full: Array = []
	var cut: Array = []
	for n: Node2D in watch:
		var r: Rect2 = n.global_rect()
		var a: Vector2 = _to_img(r.position)
		var b: Vector2 = _to_img(r.end)
		if a.x >= 0 and a.y >= 0 and b.x <= W and b.y <= H:
			full.append(n.name)
		else:
			cut.append(n.name)
	return "im Bild: %s%s" % [", ".join(full), (" | ANGESCHNITTEN: " + ", ".join(cut)) if cut else ""]


func _px_per_cm() -> float:
	return get_tree().root.get_canvas_transform().get_scale().y * get_tree().root.get_texture().get_image().get_height() \
		/ get_viewport().get_visible_rect().size.y


func _to_img(world: Vector2) -> Vector2:
	var ct: Transform2D = get_tree().root.get_canvas_transform()
	var img: Image = get_tree().root.get_texture().get_image()
	var vr: Vector2 = get_viewport().get_visible_rect().size
	return ct * world * Vector2(img.get_size()) / vr


func _frames(n: int) -> void:
	for _i: int in n:
		await get_tree().process_frame
