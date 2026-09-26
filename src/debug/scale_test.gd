extends Node2D
## Maßstab-Testszene (P01-T09): eingemessene Test-Küche + Platzhalter in echter Größe + cm-Lineal.
## Alle Größen kommen aus data/scale_table.json.

const AREA_PATH: String = "res://data/areas/test_kitchen.json"
const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")

## [scale_ref, Beschriftung, Farbe, x_cm, Tiefe_cm (Boden) oder Oberflächen-ID]
const LAYOUT: Array = [
	["home_table_dining", "Tisch", Color(0.80, 0.62, 0.42), 585.0, 30.0],
	["char_child", "Kind", Color(0.98, 0.70, 0.62), 470.0, 50.0],
	["pet_dog_medium", "Hund", Color(0.78, 0.60, 0.40), 390.0, 58.0],
	["toy_football", "Fußball", Color(0.95, 0.95, 0.95), 320.0, 62.0],
	["food_apple", "Apfel", Color(0.90, 0.25, 0.25), 200.0, &"counter_top"],
	["food_apple", "Apfel", Color(0.90, 0.25, 0.25), 535.0, &"table:home_table_dining"],
]

var room: Room
var blocks: Dictionary = {}   # scale_ref -> ScaleBlock (erster Treffer)

@onready var camera: WorldCamera = $WorldCamera
@onready var overlay: DebugOverlay = $DebugOverlay


func _ready() -> void:
	room = ROOM_SCENE.instantiate()
	add_child(room)
	move_child(room, 0)
	room.setup(Room.find_room(Room.load_area(AREA_PATH), "kitchen"))
	_place_blocks()
	var ruler := CmRuler.new()
	ruler.position = Vector2(425.0, 0.0)   # zwischen Hund und Kind, auf der hinteren Bodenlinie
	room.ysort_root.add_child(ruler)
	var area: Dictionary = Room.load_area(AREA_PATH)
	camera.setup_for_room(room, float(area.get("focus_x_cm", area["spawn"]["x_cm"])))
	overlay.room = room
	overlay.camera = camera


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_tree().change_scene_to_file("res://src/main.tscn")


func _place_blocks() -> void:
	for row: Array in LAYOUT:
		var b: ScaleBlock = ScaleBlock.new().setup(row[0], row[1], row[2])
		room.ysort_root.add_child(b)
		var where: Variant = row[4]
		if where is float:
			b.place_on_floor(row[3], where, room.floor_band)
		elif String(where).begins_with("table:"):
			var table: ScaleBlock = blocks[String(where).trim_prefix("table:")]
			var h: float = float(ItemDB.get_scale(table.scale_ref).get("surface_h_cm", table.size_cm.y))
			b.position = Vector2(row[3], table.position.y - h * table.scale.y)
			b.scale = table.scale
			b.z_index = 1
		else:
			b.place_on_surface(row[3], room.get_surface(where))
		if not blocks.has(row[0]):
			blocks[row[0]] = b
