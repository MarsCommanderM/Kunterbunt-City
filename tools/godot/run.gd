extends SceneTree
## Starter für Skript-Abläufe (Beweis-Screenshots, Messungen). -s-Skripte werden VOR den Autoloads
## kompiliert – deshalb lädt dieser Starter den eigentlichen Ablauf (ein Node mit run(args)) erst zur Laufzeit.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- <runner.gd> [args…]
## Beispiele:
##   … -s tools/godot/run.gd -- res://tools/godot/p02_scenario_runner.gd docs/tests/P02
##   … -s tools/godot/run.gd -- res://tools/godot/p02_perf_runner.gd 250


func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if args.is_empty():
		push_error("Aufruf: -- <runner.gd> [args…]")
		quit(2)
		return
	var runner: Node = load(args[0]).new()
	root.add_child(runner)
	runner.call_deferred("run", args.slice(1))
