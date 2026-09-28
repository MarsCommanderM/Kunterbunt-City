class_name Room
extends Node2D
## Ein Raum in cm (MASTERPROMPT §6). Wird aus einem Eintrag in data/areas/<bereich>.json aufgebaut.
## Koordinaten: x = 0 … width_cm, y = 0 hintere Bodenlinie, −height_cm Oberkante, +front_y_cm vordere Bodenlinie.

signal debug_toggled(on: bool)

const FRONT_MARGIN_CM: float = 12.0   # Rand unter der vorderen Bodenlinie, den die Kamera noch zeigt

@export var room_id: StringName = &""
var width_cm: float = 600.0
var height_cm: float = 260.0
var camera_cfg: Dictionary = {}
var data: Dictionary = {}
## Fläche, die der Hintergrund abdeckt (cm). Leer = kein Hintergrund.
var background_rect: Rect2 = Rect2()
## P07-T04: Hintergrund-Daten (bg.json) und die aktuelle Einrichtung (Tapete, Muster, Boden).
var bg_meta: Dictionary = {}
var decor: Dictionary = {}
var _decor_root: Node2D

@onready var background: Node2D = $Background
@onready var floor_band: FloorBand = $FloorBand
@onready var surfaces_root: Node2D = $Surfaces
@onready var fixtures_root: Node2D = $Fixtures
@onready var ysort_root: Node2D = $YSortRoot
@onready var foreground: Node2D = $Foreground
@onready var debug_grid: DebugGrid = $DebugGrid

var debug_visible: bool = false:
	set(v):
		debug_visible = v
		floor_band.debug_visible = v
		debug_grid.visible = v
		for s: Surface in get_surfaces():
			s.debug_visible = v
		debug_toggled.emit(v)


## Liest eine Bereichs-Datei. Fehler → leeres Dictionary + Log.
static func load_area(path: String) -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not (parsed is Dictionary):
		Log.error("Room: Bereichsdatei %s fehlt oder ist kaputt" % path)
		return {}
	return parsed


static func find_room(area: Dictionary, id: String) -> Dictionary:
	for r: Dictionary in area.get("rooms", []):
		if r.get("id", "") == id:
			return r
	Log.error("Room: Raum '%s' nicht im Bereich '%s'" % [id, area.get("id", "?")])
	return {}


func setup(room_data: Dictionary, chosen_decor: Dictionary = {}) -> void:
	data = room_data
	room_id = StringName(room_data.get("id", ""))
	width_cm = float(room_data.get("width_cm", 600.0))
	height_cm = float(room_data.get("height_cm", 260.0))
	camera_cfg = room_data.get("camera", {})
	floor_band.setup(room_data.get("floor", {}), width_cm)
	_build_background(String(room_data.get("background", "")), chosen_decor)
	_build_surfaces(room_data.get("surfaces", []))
	debug_grid.setup(width_cm, height_cm, floor_band.front_y_cm)


## Bereich, den die Kamera zeigen darf (cm).
func camera_bounds() -> Rect2:
	var bottom: float = floor_band.front_y_cm + FRONT_MARGIN_CM
	var r := Rect2(0.0, -height_cm, width_cm, height_cm + bottom)
	if background_rect.has_area():
		r = r.intersection(background_rect)   # nie über den Bildrand hinaus zeigen
	return r


func get_surfaces() -> Array[Surface]:
	var out: Array[Surface] = []
	for c: Node in surfaces_root.get_children():
		if c is Surface:
			out.append(c)
	return out


func get_surface(id: StringName) -> Surface:
	for s: Surface in get_surfaces():
		if s.surface_id == id:
			return s
	return null


## Alle Oberflächen, über denen x liegt – von oben nach unten sortiert.
func surfaces_at_x(x_cm: float) -> Array[Surface]:
	var out: Array[Surface] = get_surfaces().filter(func(s: Surface) -> bool: return s.contains_x(x_cm))
	out.sort_custom(func(a: Surface, b: Surface) -> bool: return a.top_y() < b.top_y())
	return out


## P07-T04: Tapete/Boden wechseln – nur die Zonen-Ebenen werden neu gebaut, Items bleiben.
func can_decorate() -> bool:
	return RoomDecor.has_decor(bg_meta)


func apply_decor(chosen: Dictionary) -> void:
	if not can_decorate() or _decor_root == null:
		return
	decor = RoomDecor.merged(bg_meta, chosen)
	RoomDecor.build(_decor_root, bg_meta, decor)


func _build_background(meta_path: String, chosen_decor: Dictionary = {}) -> void:
	for c: Node in background.get_children():
		c.queue_free()
	background_rect = Rect2()
	bg_meta = {}
	_decor_root = null
	if meta_path.is_empty():
		return
	var meta: Variant = JSON.parse_string(FileAccess.get_file_as_string(meta_path))
	if not (meta is Dictionary):
		Log.error("Room: Hintergrund-Daten %s fehlen – calibrate_bg.py ausführen" % meta_path)
		return
	bg_meta = meta
	if RoomDecor.has_decor(meta):                    # Wand + Boden zuerst (Zonen), darüber die festen Details
		_decor_root = Node2D.new()
		_decor_root.name = "Decor"
		background.add_child(_decor_root)
		apply_decor(chosen_decor)
	var ppc: float = float(meta["px_per_cm"])
	var origin: Vector2 = Vector2(meta["origin_px"][0], meta["origin_px"][1])
	background.scale = Vector2.ONE / ppc
	background.position = -origin / ppc
	background_rect = Rect2(background.position, Vector2(meta["size_px"][0], meta["size_px"][1]) / ppc)
	for t: Dictionary in meta["tiles"]:
		var spr := Sprite2D.new()
		spr.texture = load(String(t["file"]))
		spr.centered = false
		spr.position = Vector2(t["x_px"], t["y_px"])
		background.add_child(spr)


func _build_surfaces(list: Array) -> void:
	for c: Node in surfaces_root.get_children():
		c.queue_free()
	for d: Dictionary in list:
		surfaces_root.add_child(Surface.from_dict(d, floor_band))
