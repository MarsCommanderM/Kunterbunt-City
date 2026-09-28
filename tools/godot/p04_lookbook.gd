extends Node
## P04-Beweisbilder: alle Teile-Varianten (Katalog), die 3 Schablonen im Größenvergleich und die
## Farbzonen-Umfärbung. Rein rechnerisch aufgebaut – kein Raum nötig.
## Aufruf: xvfb-run -a godot --rendering-driver opengl3 --resolution 1920x1080 -s tools/godot/run.gd -- \
##         res://tools/godot/p04_lookbook.gd docs/tests/P04

const W: float = 1920.0
const H: float = 1080.0

var root: Node2D
var cam: Camera2D
var out_dir: String
var _labels: Array = []          ## [Label, Weltposition] – Schrift in BILDPUNKTEN, nicht in cm


func run(args: PackedStringArray) -> void:
	out_dir = args[0] if args.size() > 0 else "docs/tests/P04"
	DirAccess.make_dir_recursive_absolute(out_dir)
	CharacterRig.animate_poses = false
	root = Node2D.new()
	get_tree().root.add_child(root)
	cam = Camera2D.new()
	root.add_child(cam)
	cam.make_current()
	await _katalog()
	await _schablonen()
	await _farbzonen()
	get_tree().quit(0)


## 8 Slots × 5 Varianten: jede Zelle eine Figur (Kind), darüber der Slot, darunter der Varianten-Name.
func _katalog() -> void:
	var slots: Array = CharacterParts.slot_ids()
	var cell_w: float = 78.0
	var cell_h: float = 165.0
	var grid_w: float = 5.0 * cell_w
	var grid_h: float = slots.size() * cell_h
	for r: int in slots.size():
		var slot: String = String(slots[r])
		_label("%s %s" % [CharacterParts.icon(slot), CharacterParts.label(slot)],
			Vector2(-grid_w * 0.5 - 8.0, -grid_h * 0.5 + r * cell_h + cell_h * 0.5), 26,
			HORIZONTAL_ALIGNMENT_RIGHT)
		for c: int in CharacterParts.ids(slot).size():
			var id: String = String(CharacterParts.ids(slot)[c])
			var look: Dictionary = CharacterParts.default_set("kid")
			look["skin"] = CharacterParts.palette_colors("skin")[1]
			look["parts"][slot] = id
			var fig: CharacterRig = CharacterRig.create_character("kid", look)
			root.add_child(fig)
			fig.position = Vector2(-grid_w * 0.5 + (c + 0.5) * cell_w,
				-grid_h * 0.5 + (r + 1) * cell_h - 8.0)
			_label(id, fig.position + Vector2(0, 12.0), 20, HORIZONTAL_ALIGNMENT_CENTER)
	await _shot("p04_01_teile_katalog.jpg", grid_w + 110.0, grid_h + 40.0)
	_clear()


## Größenvergleich: Kleinkind 90 · Kind 125 · Erwachsene 172 – nur aus der Schablone.
func _schablonen() -> void:
	var ids: Array = ["toddler", "kid", "adult"]
	var x: float = -140.0
	for tid: String in ids:
		var look: Dictionary = CharacterParts.default_set(tid)
		look["skin"] = CharacterParts.palette_colors("skin")[1]
		var fig: CharacterRig = CharacterRig.create_character(tid, look)
		root.add_child(fig)
		fig.position = Vector2(x, 95.0)
		_label("%s · %d cm" % [tid, int(ItemDB.height_cm(String(
			CharacterTemplates.get_template(tid)["scale_ref"])))],
			fig.position + Vector2(0, 20.0), 30, HORIZONTAL_ALIGNMENT_CENTER)
		x += 140.0
	await _shot("p04_02_schablonen_groessen.jpg", 470.0, 230.0)
	_clear()


## Farbzonen: dasselbe Oberteil in 6 Palettenfarben (Zone 1) + Kragen/Knöpfe (Zone 2/3).
## Prüffarben – gleiche Liste wie tools/tests/test_p04_shots.py (fest, damit der Shader-Test nicht von der
## wachsenden Palette abhängt).
const PROOF_COLORS: Array = ["#f4f1ea", "#ffd166", "#ff9f45", "#ef6f6c", "#c1547a", "#7a5ea8", "#4f7fc0",
	"#48b0a0", "#7cb342", "#a1887f"]


func _farbzonen() -> void:
	var cols: Array = PROOF_COLORS
	var x: float = -(cols.size() - 1) * 0.5 * 70.0
	for c: Variant in cols:
		var look: Dictionary = CharacterParts.default_set("kid")
		look["skin"] = CharacterParts.palette_colors("skin")[1]
		look["parts"]["top"] = "shirt"
		look["colors"]["top"] = [String(c), "#ffffff", "#ffe08a"]
		var fig: CharacterRig = CharacterRig.create_character("kid", look)
		root.add_child(fig)
		fig.position = Vector2(x, 95.0)
		_label(String(c), fig.position + Vector2(0, 18.0), 22, HORIZONTAL_ALIGNMENT_CENTER)
		x += 70.0
	await _shot("p04_03_farbzonen.jpg", cols.size() * 70.0 + 40.0, 210.0)


func _label(text: String, world_pos: Vector2, size_px: int, align: HorizontalAlignment) -> void:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", size_px)
	l.add_theme_color_override("font_color", Color(0.16, 0.13, 0.22))
	l.horizontal_alignment = align
	l.size = Vector2(240.0, size_px * 1.6)
	root.add_child(l)
	_labels.append([l, world_pos])


## Texte erst beim Foto skalieren: 1 cm Welt = zoom px → Schrift bleibt immer gleich groß.
func _apply_labels(zoom: float) -> void:
	for e: Array in _labels:
		var l: Label = e[0]
		l.scale = Vector2.ONE / zoom
		l.position = (e[1] as Vector2) - Vector2(120.0, 0.0) / zoom


func _shot(name: String, w_cm: float, h_cm: float) -> void:
	var zoom: float = minf(W / maxf(w_cm, 1.0), H / maxf(h_cm, 1.0))
	cam.zoom = Vector2.ONE * zoom
	cam.position = Vector2(0.0, 0.0)
	_apply_labels(zoom)
	await _frames(4)
	await RenderingServer.frame_post_draw
	get_tree().root.get_texture().get_image().save_jpg(out_dir.path_join(name), 0.9)
	print("Screenshot: %s (%.0f × %.0f cm)" % [name, w_cm, h_cm])


## Szene für das nächste Bild leeren.
func _clear() -> void:
	for c: Node in root.get_children():
		if c != cam:
			c.free()
	_labels = []


func _frames(n: int) -> void:
	for _i: int in n:
		await get_tree().process_frame
