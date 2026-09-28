extends Node
## P11-T05: Stabilitätstest – ein Zufalls-Bot spielt X Sekunden lang (Standard 60 Min.) wie ein Kind:
## Dinge ziehen und abstellen, antippen, aus dem Katalog holen, Räume und Bereiche wechseln, rückgängig machen.
## Gemessen: Fehler/Warnungen (eigener Logger), Speicher, Knoten, verwaiste Knoten. Bericht: <out>/bot_report.json
## Aufruf: godot --headless -s tools/godot/run.gd -- res://tools/godot/p11_bot_runner.gd docs/tests/P11 3600 [seed]
## Exit-Code 1 bei Fehlern oder Speicher-/Knoten-Wachstum über den Grenzen.

const AREA_S: float = 90.0                 ## so lange bleibt der Bot in einem Bereich
const MAX_ITEMS: int = 250                 ## Budget (Tech-Spec): nie mehr Dinge in einem Raum
const MAX_MEM_GROWTH_MB: float = 150.0
const MAX_ORPHANS: int = 50


class BotLogger extends Logger:
	var errors: Array = []
	var warnings: int = 0

	func _log_error(function: String, file: String, line: int, code: String, rationale: String,
			_editor_notify: bool, error_type: int, _script_backtrace: Array[ScriptBacktrace]) -> void:
		var msg: String = "%s:%d %s %s" % [file, line, code, rationale]
		if error_type == ERROR_TYPE_WARNING:
			warnings += 1
		elif errors.size() < 50 and not _harmless(msg):
			errors.append(msg)

	func _log_message(_message: String, _error: bool) -> void:
		pass

	static func _harmless(msg: String) -> bool:
		return msg.contains("ERR_CANT_OPEN") and msg.contains("audio")   # Container ohne Soundkarte


var _log := BotLogger.new()
var _rng := RandomNumberGenerator.new()
var _stats: Dictionary = {"moves": 0, "taps": 0, "spawns": 0, "rooms": 0, "areas": 0, "undos": 0}
var _catalog: Array = []


func run(args: PackedStringArray) -> void:
	var out: String = args[0] if args.size() > 0 else "docs/tests/P11"
	var seconds: float = float(args[1]) if args.size() > 1 else 3600.0
	_rng.seed = int(args[2]) if args.size() > 2 else 20260928
	DirAccess.make_dir_recursive_absolute(out)
	OS.add_logger(_log)
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#e2ab80"
	Game.add_character(c)
	Game.set_active(c.id)
	_catalog = ItemDB.item_ids()
	var areas: Array = []
	for a: Variant in Areas.ids():
		if Areas.is_ready(StringName(a)) and not areas.has(Areas.canonical(StringName(a))):
			areas.append(Areas.canonical(StringName(a)))
	var t0: float = Time.get_ticks_msec() / 1000.0
	var mem0: float = 0.0
	var nodes0: int = 0
	var samples: Array = []
	while Time.get_ticks_msec() / 1000.0 - t0 < seconds:
		var area_id: StringName = areas[_rng.randi() % areas.size()]
		SceneRouter.pending_area = area_id
		var scene: AreaScene = load("res://src/world/area_scene.tscn").instantiate()
		get_tree().root.add_child(scene)
		await _frames(6)
		_stats["areas"] += 1
		var until: float = Time.get_ticks_msec() / 1000.0 + AREA_S
		while Time.get_ticks_msec() / 1000.0 < until and Time.get_ticks_msec() / 1000.0 - t0 < seconds:
			await _step(scene)
		scene.queue_free()
		await _frames(4)
		var s: Dictionary = _sample(t0)
		samples.append(s)
		if mem0 == 0.0:
			mem0 = float(s["mem_mb"])
			nodes0 = int(s["nodes"])
		print("Bot: %s · %d s · %.0f MB · %d Knoten · %d Fehler" % [area_id, int(s["t"]), s["mem_mb"], s["nodes"],
			_log.errors.size()])
	var last: Dictionary = _sample(t0)
	var report: Dictionary = {
		"seconds": int(last["t"]), "seed": _rng.seed, "stats": _stats, "errors": _log.errors, "warnings": _log.warnings,
		"mem_start_mb": mem0, "mem_end_mb": last["mem_mb"], "mem_growth_mb": float(last["mem_mb"]) - mem0,
		"nodes_start": nodes0, "nodes_end": last["nodes"], "orphans_end": last["orphans"], "samples": samples,
	}
	var ok: bool = _log.errors.is_empty() and float(report["mem_growth_mb"]) < MAX_MEM_GROWTH_MB \
		and int(last["orphans"]) < MAX_ORPHANS
	report["ok"] = ok
	var f := FileAccess.open(out.path_join("bot_report.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(report, "  "))
	f.close()
	print("Bot fertig: %s · %s" % ["OK" if ok else "FEHLER", JSON.stringify(_stats)])
	get_tree().quit(0 if ok else 1)


func _sample(t0: float) -> Dictionary:
	return {"t": Time.get_ticks_msec() / 1000.0 - t0,
		"mem_mb": Performance.get_monitor(Performance.MEMORY_STATIC) / 1048576.0,
		"nodes": int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT)),
		"orphans": int(Performance.get_monitor(Performance.OBJECT_ORPHAN_NODE_COUNT))}


func _step(scene: AreaScene) -> void:
	var room: Room = scene.room
	var items: Array[ItemNode] = Placement.all_items(room)
	var roll: float = _rng.randf()
	if roll < 0.40 and not items.is_empty():
		var it: ItemNode = items[_rng.randi() % items.size()]
		if it.def.movable and it.is_inside_tree() and not it.has_meta("npc_id"):
			scene.drag.scripted_move(it, _random_floor_point(room))
			_stats["moves"] += 1
	elif roll < 0.65 and not items.is_empty():
		var it: ItemNode = items[_rng.randi() % items.size()]
		if it.is_inside_tree():
			var p: Vector2 = scene.drag.grab_point(it)
			if scene.drag.press(91, p):
				scene.drag.release(91, p)
				_stats["taps"] += 1
	elif roll < 0.75 and items.size() < MAX_ITEMS:
		var id: StringName = StringName(_catalog[_rng.randi() % _catalog.size()])
		var local: Vector2 = room.ysort_root.to_local(_random_floor_point(room))
		ItemSpawner.on_floor(room, id, local.x, local.y)
		_stats["spawns"] += 1
	elif roll < 0.80:
		var rooms: Array = scene.room_ids()
		if rooms.size() > 1:
			scene.switch_room(String(rooms[_rng.randi() % rooms.size()]))
			_stats["rooms"] += 1
	elif roll < 0.84 and scene.drag.undo != null:
		scene.drag.undo.undo()
		_stats["undos"] += 1
	await _frames(2)


func _random_floor_point(room: Room) -> Vector2:
	var x: float = _rng.randf_range(40.0, room.width_cm - 40.0)
	var y: float = _rng.randf_range(room.floor_band.back_y_cm, room.floor_band.front_y_cm)
	return room.ysort_root.to_global(Vector2(x, y))


func _frames(n: int) -> void:
	for i: int in n:
		await get_tree().process_frame
