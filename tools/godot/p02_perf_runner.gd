extends Node
## P02-T12 Leistungsmessung: Test-Küche auf N Items auffüllen (Standard 250), 5 s rendern, messen.
## Ausgabe als eine Zeile „PERF …“ – ehrliche Werte der jeweiligen Maschine (llvmpipe = Software-Rendering!).

func run(args: PackedStringArray) -> void:
	var n: int = int(args[0]) if args.size() > 0 else 250
	var sb: Node = load("res://src/debug/sandbox_kitchen.tscn").instantiate()
	get_tree().root.add_child(sb)
	await get_tree().process_frame
	var room: Room = sb.room
	var ids: Array = ItemDB.item_ids().filter(func(id: StringName) -> bool: return ItemDB.get_item(id).movable)
	var i: int = 0
	while Placement.all_items(room).size() < n:
		ItemSpawner.on_floor(room, ids[i % ids.size()], 20.0 + (i * 37) % 680, float((i * 13) % 70))
		i += 1
	# ein Item wird die ganze Zeit gezogen (schlimmster Fall: Drag + Schatten + Sortierung)
	var drag: DragController = sb.drag
	var ball: ItemNode = sb.spawned[&"toy_beachball"]
	var g: Vector2 = drag.grab_point(ball)
	drag.press(7, g)
	for _f: int in 30:
		await get_tree().process_frame
	var frames: int = 0
	var proc_sum: float = 0.0
	var worst: float = 0.0
	var t0: int = Time.get_ticks_usec()
	var last: int = t0
	while Time.get_ticks_usec() - t0 < 5_000_000:
		drag.move(7, g + Vector2(sin(frames * 0.05) * 200.0, -40.0))
		await get_tree().process_frame
		var now: int = Time.get_ticks_usec()
		worst = maxf(worst, (now - last) / 1000.0)
		last = now
		proc_sum += Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0
		frames += 1
	var secs: float = (Time.get_ticks_usec() - t0) / 1_000_000.0
	drag.release(7, g)
	print("PERF items=%d frames=%d fps=%.1f frame_worst=%.1fms process_avg=%.2fms draw_calls=%d objects=%d renderer=%s" % [
		Placement.all_items(room).size(), frames, frames / secs, worst, proc_sum / frames,
		int(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)),
		int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT)), RenderingServer.get_video_adapter_name()])
	get_tree().quit(0)
