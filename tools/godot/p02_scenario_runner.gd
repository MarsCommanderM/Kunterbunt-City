extends Node
## Beweis-Screenshots Phase 02: bedient die Test-Küche wie ein Kind (über die DragController-API)
## und speichert nach jedem Schritt ein Bild. Reproduzierbar: keine Zufallswerte, Animationen aus.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- res://tools/godot/p02_scenario_runner.gd docs/tests/P02

var sb: Node
var out_dir: String


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else "docs/tests/P02"
	DirAccess.make_dir_recursive_absolute(out_dir)
	sb = load("res://src/debug/sandbox_kitchen.tscn").instantiate()
	get_tree().root.add_child(sb)
	await _frames(6)
	var drag: DragController = sb.drag
	drag.animate = false
	var cam: WorldCamera = sb.camera
	var it: Dictionary = sb.spawned
	print("Items in der Küche: ", Placement.all_items(sb.room).size())
	await _shot("p02_01_sandbox_61_items.jpg")

	# 1) Apfel vom Tisch anheben – mitten im Ziehen (angehoben, Schatten größer)
	var apple: ItemNode = it[&"food_apple_red"]
	var g: Vector2 = drag.grab_point(apple)
	drag.press(1, g)
	drag.move(1, g + Vector2(-40, -60))
	drag._process(1.0)
	await _shot("p02_02_apfel_angehoben.jpg")
	# … und auf die Arbeitsplatte neben die Karotte
	drag.release(1, Vector2(250, -110))
	# Karotte + Ei auf den Esstisch
	var table: ItemNode = it[&"home_table_wood"]
	drag.scripted_move(it[&"food_carrot"], Vector2(640, table.top_global_y() - 25))
	drag.scripted_move(it[&"food_egg"], Vector2(655, table.top_global_y() - 25))
	# Hund auf den Boden vor den Tisch
	drag.scripted_move(it[&"pet_dog_brown"], Vector2(600, 70))
	await _shot("p02_03_abgestellt_tisch_boden.jpg")

	# 2) Kühlschrank + Rucksack antippen → Inhalt sichtbar
	var fridge: ItemNode = it[&"fix_fridge"]
	var bag: ItemNode = it[&"item_backpack"]
	for c: ItemNode in [fridge, bag]:
		var p: Vector2 = drag.grab_point(c)
		drag.press(2, p)
		drag.release(2, p)
	# Ei aus dem Tisch in den Rucksack, Käse aus dem Kühlschrank auf die Platte
	drag.scripted_move(it[&"food_toast"], bag.global_rect().get_center())
	drag.scripted_move(it[&"food_cheese"], Vector2(440, -130))
	await _shot("p02_04_kuehlschrank_rucksack_offen.jpg")

	# 3) Klötze-Turm: 4. Klotz auf den 3er-Turm, dann Teller auf den Tellerstapel
	var tower_top: ItemNode = it[&"toy_block_3"]
	drag.scripted_move(it[&"toy_block_4"], Vector2(tower_top.global_position.x, tower_top.top_global_y(true) - 3))
	var plate_top: ItemNode = it[&"kitchen_plate_4"]
	drag.scripted_move(it[&"kitchen_bowl_2"], Vector2(plate_top.global_position.x, plate_top.top_global_y(true) - 2))
	_focus(cam, 110.0, Vector2(tower_top.global_position.x, 20.0))
	print("Klotz-Turm Höhe: ", (it[&"toy_block_4"] as ItemNode).stack_depth_below())
	await _shot("p02_05a_klotzturm_zoom.jpg")
	_focus(cam, 110.0, Vector2(plate_top.global_position.x, -40.0))
	print("Teller-Stapel + Schüssel: ", (it[&"kitchen_bowl_2"] as ItemNode).stack_depth_below())
	await _shot("p02_05b_tellerstapel_zoom.jpg")
	cam.set_visible_height(Units.DEFAULT_VIEW_HEIGHT_CM)
	cam.position = Vector2(float(sb.room.width_cm) * 0.5, cam.position.y)
	cam.pan_by_screen(Vector2.ZERO)

	# 4) Abgelehnt: Stuhl auf die Arbeitsplatte → federt auf den Boden davor
	var chair: ItemNode = it[&"home_chair_mint"]
	var res: Array = []
	drag.item_dropped.connect(func(_i: ItemNode, t: Placement.Target) -> void: res.append(t.rejected_reason), CONNECT_ONE_SHOT)
	drag.scripted_move(chair, Vector2(300, -120))
	print("Stuhl auf Arbeitsplatte: ", res)
	await _shot("p02_06_stuhl_abgelehnt_boden.jpg")

	# 5) Rückgängig ×4 (Stuhl, Schüssel, Klotz, Käse zurück)
	for i: int in 4:
		drag.undo.undo()
	print("Undo-Schritte übrig: ", drag.undo.size())
	await _shot("p02_07_nach_4x_rueckgaengig.jpg")

	# 6) Debug-Ansicht: Flächen, Bodenband, Hitboxen
	sb.overlay.set_enabled(true)
	await _shot("p02_08_debug_flaechen.jpg")
	get_tree().quit(0)


func _focus(cam: WorldCamera, h_cm: float, center: Vector2) -> void:
	cam.set_visible_height(h_cm)
	cam.position = center
	cam.pan_by_screen(Vector2.ZERO)   # an die Raumgrenzen klemmen


func _frames(n: int) -> void:
	for _i: int in n:
		await get_tree().process_frame


func _shot(name: String) -> void:
	await _frames(4)
	await RenderingServer.frame_post_draw
	var img: Image = get_tree().root.get_texture().get_image()
	if name.ends_with(".jpg"):
		img.save_jpg(out_dir.path_join(name), 0.9)   # Beweisbilder: JPG hält das Repo klein
	else:
		img.save_png(out_dir.path_join(name))
	print("Screenshot: ", name)
