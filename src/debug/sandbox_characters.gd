extends Node2D
## Figuren-Sandbox (Phase 03): 3 Schablonen-Figuren (Kleinkind 90, Kind 125, Erwachsene 172), das fertige
## Referenz-Mädchen, Hund + Katze, Stuhl, Sofa, Sessel, Kinderbett, Esstisch mit Essen, Teddy.

const AREA_PATH: String = "res://data/areas/test_kitchen.json"
const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")
## Aufteilung in Kamerabühnen (Kamera zeigt 300 cm): Bett ~120 · Sitzen ~430 · Tisch ~645.
const FURNITURE: Array = [  # [id, x, Tiefe]
	["home_bed_kid", 95.0, 22.0], ["home_sofa", 290.0, 20.0], ["home_chair_mint", 415.0, 48.0],
	["home_armchair", 480.0, 26.0], ["home_table_wood", 645.0, 30.0],
]
const FURNITURE_2: Array = [  # zweiter Stuhl (Teddy-Beweis auf 45 cm)
	["home_chair_mint", 555.0, 44.0],
]
const FIGURES: Array = [  # [Schablone/Sprite, x, Tiefe]
	["adult", 330.0, 58.0], ["kid", 380.0, 64.0], ["toddler", 430.0, 70.0], ["char_girl_01", 470.0, 60.0],
]
const LOOSE: Array = [
	["pet_dog_brown", 520.0, 72.0], ["pet_cat", 160.0, 70.0], ["toy_teddy_brown", 250.0, 73.0],
	["toy_beachball", 690.0, 72.0],
]

var room: Room
var spawned: Dictionary = {}   ## id → ItemNode (Figuren: Schablonen-Name)

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
	camera.setup_for_room(room, 380.0)
	drag.camera = camera
	drag.attach_room(room)
	undo_button.undo = drag.undo
	overlay.room = room
	overlay.camera = camera


func _populate() -> void:
	for f: Array in FURNITURE:
		_keep(ItemSpawner.on_floor(room, f[0], f[1], f[2]))
	var table: ItemNode = spawned[&"home_table_wood"]
	_keep(ItemSpawner.on_item(table, &"food_carrot", -0.3))
	_keep(ItemSpawner.on_item(table, &"food_apple_red", -0.1))
	_keep(ItemSpawner.on_item(table, &"food_icecream_3", 0.1))
	_keep(ItemSpawner.on_item(table, &"home_mug_pink_dots", 0.3))
	for c: Array in FIGURES:
		var tid: String = String(c[0])
		var me: CharacterData = Game.active_character()
		if tid == "kid" and me != null and me.is_complete():
			# Eigene Figur aus dem Editor (P04): Aussehen von ihr, GRÖSSE aus der Schablone.
			spawned[&"me"] = ItemSpawner.character_on_floor(room, me.template_id, c[1], c[2], me.look())
			continue
		spawned[StringName(tid)] = ItemSpawner.character_on_floor(room, tid, c[1], c[2])
	for f: Array in FURNITURE_2:
		spawned[StringName(f[0] + "_2")] = ItemSpawner.on_floor(room, f[0], f[1], f[2])
	_spawn_loose()


## Haustiere: die eigenen (aus dem Haustier-Editor) ersetzen die Platzhalter-Tiere.
func _spawn_loose() -> void:
	var mine: Array = []
	for pid: Variant in Game.active_pets:
		var pd: PetData = Game.pet_by_id(pid)
		if pd != null:
			mine.append(pd)
	for l: Array in LOOSE:
		var id: String = String(l[0])
		var pick: PetData = null
		if mine.size() > 0 and (id == "pet_dog_brown" or id == "pet_cat"):
			pick = mine.pop_front()
		if pick == null:
			_keep(ItemSpawner.on_floor(room, l[0], l[1], l[2]))
			continue
		var pet: ItemNode = _keep(ItemSpawner.on_floor(room, StringName(pick.species_id), l[1], l[2]))
		# Nur die neuen Zonen-Sprites (P04) werden eingefärbt – fertige Stil-C-Bilder nicht.
		if pet != null and PetSpecies.ids().has(pick.species_id):
			PetLook.apply(pet.sprite, [pick.fur, pick.fur2, pick.collar], pick.pattern)


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
