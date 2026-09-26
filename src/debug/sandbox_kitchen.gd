extends Node2D
## Test-Küche für Phase 02 (P02-T10): alle 61 Items (18 echte Stil-C-Sprites + 43 Platzhalter),
## verteilt auf Arbeitsplatte, Regale, Tisch, Kühlschrank, Rucksack und Boden. Alles zieh- und stapelbar.

const AREA_PATH: String = "res://data/areas/test_kitchen.json"
const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")

## Arbeitsplatte (x in cm)
const COUNTER: Array = [
	["kitchen_microwave", 160.0], ["food_carrot", 196.0], ["food_apple_green", 210.0], ["food_egg", 222.0],
	["food_egg_chocolate", 233.0], ["kitchen_pot", 262.0], ["kitchen_pan", 292.0], ["kitchen_kettle", 326.0],
	["home_cup_orange_dots", 346.0], ["kitchen_glass", 360.0], ["food_banana", 374.0], ["food_tomato", 388.0],
	["kitchen_cutting_board", 408.0], ["food_toast", 408.0], ["food_bread_loaf", 428.0], ["kitchen_toaster", 452.0],
	["kitchen_spoon", 468.0],
]
const SHELVES: Array = [
	["shelf_left_low", "flower_tulip_yellow_pot", 185.0], ["shelf_left_low", "item_crayon", 238.0],
	["shelf_left_high", "food_pizza", 200.0], ["shelf_left_high", "food_cupcake", 290.0],
	["shelf_right", "school_book_blue_star", 350.0], ["shelf_right", "toy_car_small", 400.0],
	["shelf_right", "kitchen_mug", 440.0],
]
const FLOOR: Array = [  # [id, x, Tiefe]
	["home_table_coffee", 95.0, 40.0], ["item_bucket", 150.0, 66.0], ["toy_doll", 180.0, 52.0],
	["toy_basketball", 215.0, 62.0], ["toy_teddy_brown", 300.0, 42.0], ["toy_teddy_brown_b", 330.0, 66.0],
	["toy_beachball", 372.0, 58.0], ["pet_dog_brown", 420.0, 48.0], ["item_backpack", 468.0, 64.0],
	["home_chair_mint", 548.0, 52.0], ["item_watering_can", 40.0, 70.0], ["home_stool", 688.0, 70.0],
]


var room: Room
var spawned: Dictionary = {}   ## id → ItemNode

@onready var camera: WorldCamera = $WorldCamera
@onready var drag: DragController = $DragController
@onready var overlay: DebugOverlay = $DebugOverlay
@onready var undo_button: UndoButton = $Hud/UndoButton


func _ready() -> void:
	room = ROOM_SCENE.instantiate()
	add_child(room)
	move_child(room, 0)
	var area: Dictionary = Room.load_area(AREA_PATH)
	room.setup(Room.find_room(area, "kitchen"))
	_populate()
	camera.setup_for_room(room, float(area["spawn"]["x_cm"]))
	drag.camera = camera
	drag.attach_room(room)
	undo_button.undo = drag.undo
	overlay.room = room
	overlay.camera = camera


func _populate() -> void:
	for c: Array in COUNTER:
		_keep(ItemSpawner.on_surface(room, c[0], &"counter_top", c[1]))
	for s: Array in SHELVES:
		_keep(ItemSpawner.on_surface(room, s[1], s[0], s[2]))
	for f: Array in FLOOR:
		_keep(ItemSpawner.on_floor(room, f[0], f[1], f[2]))
	# Kühlschrank (fest, Behälter) mit Inhalt
	var fridge: ItemNode = _keep(ItemSpawner.on_floor(room, &"fix_fridge", 520.0, 1.0))
	for id: StringName in [&"food_milk_carton", &"food_cheese", &"food_juice_bottle", &"food_cake", &"food_icecream_3b"]:
		_keep(ItemSpawner.into_container(fridge, id))
	# Rucksack mit Inhalt
	var bag: ItemNode = spawned[&"item_backpack"]
	_keep(ItemSpawner.into_container(bag, &"item_book_2"))
	# Esstisch mit Dingen und einem Tellerstapel
	var table: ItemNode = _keep(ItemSpawner.on_floor(room, &"home_table_wood", 628.0, 36.0))
	_keep(ItemSpawner.on_item(table, &"food_apple_red", -0.38))
	_keep(ItemSpawner.on_item(table, &"home_mug_pink_dots", -0.22))
	_keep(ItemSpawner.on_item(table, &"food_icecream_3", -0.06))
	var plate: ItemNode = _keep(ItemSpawner.on_item(table, &"kitchen_plate_1", 0.1))
	for i: int in range(2, 5):
		plate = _keep(ItemSpawner.on_item(plate, StringName("kitchen_plate_%d" % i), 0.0, true))
	_keep(ItemSpawner.on_item(table, &"flower_tulip_red_pot", 0.25))
	_keep(ItemSpawner.on_item(table, &"item_vase_bouquet", 0.4))
	# Couchtisch
	var coffee: ItemNode = spawned[&"home_table_coffee"]
	_keep(ItemSpawner.on_item(coffee, &"food_watermelon", -0.2))
	_keep(ItemSpawner.on_item(coffee, &"item_book_1", 0.25))
	# Hocker mit Schüsselstapel
	var stool: ItemNode = spawned[&"home_stool"]
	var bowl: ItemNode = _keep(ItemSpawner.on_item(stool, &"kitchen_bowl_1"))
	_keep(ItemSpawner.on_item(bowl, &"kitchen_bowl_2", 0.0, true))
	# Klotz-Turm (3) + einzelner Klotz auf dem Boden
	var block: ItemNode = _keep(ItemSpawner.on_floor(room, &"toy_block_1", 250.0, 60.0))
	for i: int in range(2, 4):
		block = _keep(ItemSpawner.on_item(block, StringName("toy_block_%d" % i), 0.0, true))
	_keep(ItemSpawner.on_floor(room, &"toy_block_4", 268.0, 68.0))
	var missing: Array = ItemDB.item_ids().filter(func(id: StringName) -> bool: return not spawned.has(id))
	if not missing.is_empty():
		Log.warn("Sandbox: nicht platziert: %s" % str(missing))


func _keep(it: ItemNode) -> ItemNode:
	if it:
		spawned[it.def.id] = it
	return it


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_tree().change_scene_to_file("res://src/main.tscn")
	elif event is InputEventKey and event.pressed and (event as InputEventKey).keycode == KEY_Z \
			and (event as InputEventKey).ctrl_pressed:
		drag.undo.undo()
