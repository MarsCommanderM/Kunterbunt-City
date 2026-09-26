class_name SandboxReferenceKitchen
extends Node2D
## P03-T10: Referenz-Küche „Küche Maßstab“ – derselbe Raum, dieselben Sprites (reference/sprites/),
## dieselben Positionen wie reference/kueche_stil_c_massstab.png.
## Umrechnung der Rohbild-Pixel: 1 cm = 166 px / 90 cm = 1,8444 px (Zähler), x0 = 28 px, Boden 600 px.

const AREA_PATH: String = "res://data/areas/test_kitchen.json"
const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")

const PX_PER_CM: float = 166.0 / 90.0      ## Kalibrierung: Arbeitsplatte 90 cm hoch = 166 px
const ORIGIN_X_PX: float = 28.0
const FLOOR_BACK_PX: float = 600.0
const BAND_CM: float = 73.2
const BAND_PX: float = 135.0

## [id, x_px, y_px] genau wie in reference/pipeline_demo_kueche.py compose()
const SCENE: Array = [
	["char_girl_01", 370.0, 715.0], ["pet_dog_brown", 520.0, 712.0], ["home_chair_mint", 850.0, 652.0],
	["home_table_wood", 1010.0, 664.0], ["toy_beachball", 1165.0, 728.0],
]
## Auf dem Tisch: [id, Anteil der Tischbreite]
const ON_TABLE: Array = [
	["home_mug_pink_dots", -0.30], ["food_apple_red", -0.05], ["food_icecream_3", 0.12],
	["flower_tulip_red_pot", 0.32],
]
## Auf der Arbeitsplatte (hintere Ebene, y = 434 px)
const ON_COUNTER: Array = [
	["school_book_blue_star", 640.0], ["home_cup_orange_dots", 692.0], ["food_apple_green", 878.0],
]
const TEDDY_ON_CHAIR: Array = ["toy_teddy_brown", 0.12]   ## sitzt auf der Sitzfläche

var room: Room
var spawned: Dictionary = {}

@onready var camera: WorldCamera = $WorldCamera
@onready var drag: DragController = $DragController


func _ready() -> void:
	room = ROOM_SCENE.instantiate()
	add_child(room)
	move_child(room, 0)
	room.setup(Room.find_room(Room.load_area(AREA_PATH), "kitchen"))
	_populate()
	camera.setup_for_room(room, cm_x(228.0) + 300.0 * 16.0 / 9.0 * 0.5)
	drag.camera = camera
	drag.attach_room(room)


func _populate() -> void:
	for c: Array in SCENE:
		var it: ItemNode = ItemSpawner.character_on_floor(room, c[0], cm_x(c[1]), depth_y(c[2])) \
			if str(c[0]).begins_with("char_") else ItemSpawner.on_floor(room, c[0], cm_x(c[1]), depth_y(c[2]))
		spawned[StringName(c[0])] = it
	var table: ItemNode = spawned[&"home_table_wood"]
	for c: Array in ON_TABLE:
		spawned[StringName(c[0])] = ItemSpawner.on_item(table, c[0], c[1])
	for c: Array in ON_COUNTER:
		spawned[StringName(c[0])] = ItemSpawner.on_surface(room, c[0], &"counter_top", cm_x(c[1]))
	# Teddy sitzt AUF der Sitzfläche (Sitzplatz 0) – nicht auf einer Abstellfläche
	var chair: ItemNode = spawned[&"home_chair_mint"]
	var teddy: ItemNode = ItemSpawner.make(StringName(TEDDY_ON_CHAIR[0]))
	chair.on_top_root.add_child(teddy)
	teddy.position = Seats.point_local(chair, 0) + Vector2(chair.def.width_cm * TEDDY_ON_CHAIR[1], 0.0)
	teddy.scale = chair.global_scale
	teddy.slot_index = 0
	spawned[StringName(TEDDY_ON_CHAIR[0])] = teddy


static func cm_x(x_px: float) -> float:
	return (x_px - ORIGIN_X_PX) / PX_PER_CM


static func depth_y(y_px: float) -> float:
	return (y_px - FLOOR_BACK_PX) * BAND_CM / BAND_PX


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_tree().change_scene_to_file("res://src/main.tscn")
