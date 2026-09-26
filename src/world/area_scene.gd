class_name AreaScene
extends Node2D
## Ein Bereich zum Spielen (P05-T05/T06): Raum aus data/areas/*.json, eigene Figur am
## `spawn`-Punkt mit Ankunfts-Freude, eigene Haustiere dabei, Items aus dem gespeicherten
## Zustand (oder der Start-Ausstattung). Oben links zurück zur Karte, unten rechts der
## Rucksack, 📷 macht ein Foto fürs Album. Jede Änderung wird (entprellt) gespeichert.

const ROOM_SCENE: PackedScene = preload("res://src/world/room.tscn")
const UNDO_BUTTON: GDScript = preload("res://src/ui/undo_button.gd")

signal left_area

var area_id: StringName = &""
var area: Dictionary = {}
var room: Room
var camera: WorldCamera
var drag: DragController
var hud: AreaHud
var ui: CanvasLayer                  ## Ebene für UI-Panels (Rucksack, Album, Eltern …)
var me: ItemNode                     ## die eigene Figur
var pets: Array = []                 ## [PetNode]
var load_ms: float = 0.0
var _t0: int = 0


func _ready() -> void:
	_t0 = Time.get_ticks_usec()
	area_id = SceneRouter.take_pending_area()
	if area_id == &"":
		area_id = Areas.first_ready()
	area = Areas.get_area(area_id)
	var area_file: Dictionary = Room.load_area(Areas.path_of(area_id))
	area["default_items"] = area_file.get("default_items", [])
	if area.is_empty():
		push_error("AreaScene: unbekannter Bereich '%s'" % String(area_id))
		return
	_build_room()
	_spawn()
	_build_hud()
	load_ms = (Time.get_ticks_usec() - _t0) / 1000.0
	SceneRouter.last_load_ms = load_ms
	Log.info("Bereich '%s' betreten (%.0f ms, %d Items)" % [
		String(area_id), load_ms, Placement.all_items(room).size()])
	_check_load_time()


func _build_room() -> void:
	room = ROOM_SCENE.instantiate()
	add_child(room)
	move_child(room, 0)
	var data: Dictionary = Room.load_area(Areas.path_of(area_id))
	var rid: String = Areas.room_of(area_id)
	room.setup(Room.find_room(data, rid) if not rid.is_empty() else data["rooms"][0])
	camera = WorldCamera.new()
	add_child(camera)
	camera.setup_for_room(room, Areas.spawn_of(area_id).x)
	drag = DragController.new()
	add_child(drag)
	drag.camera = camera
	drag.attach_room(room)
	drag.item_dropped.connect(_on_item_dropped)
	drag.item_tapped.connect(func(_it: ItemNode) -> void: _on_world_changed())


func _spawn() -> void:
	var spawn: Vector2 = Areas.spawn_of(area_id)
	var state: Array = Game.room_state(area_id, room.room_id)
	if state.is_empty():
		_spawn_defaults()
	else:
		var n: int = RoomSnapshot.apply(room, state)
		Log.info("Raumzustand geladen: %d Items" % n)
		_spawn_me(spawn)
	_spawn_pets(spawn)
	if me != null:
		_arrive(me)


func _spawn_defaults() -> void:
	var list: Array = area.get("default_items", [])
	var by_id: Dictionary = {}
	for e: Variant in list:
		var d: Dictionary = e
		if d.has("on"):
			continue                       # Dinge auf Tischen kommen im zweiten Durchgang
		by_id[String(d["id"])] = ItemSpawner.on_floor(room, StringName(String(d["id"])),
			float(d.get("x_cm", 0.0)), float(d.get("y_cm", 0.0)))
	for e: Variant in list:
		var d: Dictionary = e
		if not d.has("on"):
			continue
		var host: ItemNode = by_id.get(String(d["on"]))
		if host != null:
			ItemSpawner.on_item(host, StringName(String(d["id"])), float(d.get("x_rel", 0.0)))
	_spawn_me(Areas.spawn_of(area_id))


## Die eigene Figur (Aussehen aus dem Editor, Größe aus der Schablone).
func _spawn_me(spawn: Vector2) -> void:
	var c: CharacterData = Game.active_character()
	if c != null:
		me = ItemSpawner.character_on_floor(room, c.template_id, spawn.x, spawn.y, c.look())


func _spawn_pets(spawn: Vector2) -> void:
	var i: int = 0
	for pid: Variant in Game.active_pets:
		var pd: PetData = Game.pet_by_id(pid)
		if pd == null:
			continue
		var x: float = spawn.x - 60.0 + i * 120.0
		var pet: ItemNode = ItemSpawner.on_floor(room, StringName(pd.species_id), x, spawn.y + 6.0)
		if pet == null:
			continue
		pet.set_meta("pet_id", String(pd.id))
		if PetSpecies.ids().has(pd.species_id):
			CharacterLook.apply(pet.sprite, [Color(pd.fur), Color(pd.fur2), Color(pd.collar)])
		pets.append(pet)
		i += 1


## Ankunft: kurze Freude (Hüpfen + „hallo"), danach ist die Figur normal bedienbar.
func _arrive(fig: ItemNode) -> void:
	if fig is CharacterRig:
		(fig as CharacterRig).set_emotion("laugh")
	if Settings.reduced_motion:
		return
	var tw: Tween = create_tween()
	tw.tween_property(fig, "position:y", fig.position.y - 18.0, 0.18).set_trans(Tween.TRANS_QUAD)
	tw.tween_property(fig, "position:y", fig.position.y, 0.32).set_trans(Tween.TRANS_BOUNCE)
	await tw.finished
	await get_tree().create_timer(0.5).timeout
	if is_instance_valid(fig) and fig is CharacterRig:
		(fig as CharacterRig).set_emotion("happy")


func _build_hud() -> void:
	ui = CanvasLayer.new()
	ui.layer = 50
	add_child(ui)
	hud = AreaHud.new()
	add_child(hud)
	hud.setup(drag.undo)
	hud.photo.connect(_on_photo)
	hud.leave.connect(func() -> void: leave())
	hud.backpack.connect(func() -> void:
		Backpack.open(ui, func(_id: String, _i: int) -> bool: return _place_back(_id)))
	camera.set_visible_height(room.camera_cfg.get("default_h_cm", 300.0))


func _on_photo() -> void:
	await RenderingServer.frame_post_draw
	var img: Image = get_viewport().get_texture().get_image()
	if img == null:
		return
	var path: String = SaveSystem.album_add(img)
	if path.is_empty():
		return
	AudioBus.play_sfx("shutter")
	hud.flash()


## Ding aus dem Rucksack zurück in die Welt (neben der eigenen Figur).
func _place_back(id: String) -> bool:
	var x: float = me.position.x + 70.0 if me != null else Areas.spawn_of(area_id).x
	var y: float = me.position.y if me != null else Areas.spawn_of(area_id).y
	var it: ItemNode = ItemSpawner.on_floor(room, StringName(id), x, y)
	if it != null:
		_on_world_changed()
	return it != null


func _on_world_changed() -> void:
	Game.set_room_state(area_id, room.room_id, RoomSnapshot.capture(room))
	Game.mark_dirty(area_id, room.room_id)


## Ding auf den Rucksack-Knopf gezogen? → einpacken.
func _on_item_dropped(item: ItemNode, _target) -> void:
	if item is CharacterRig:
		_on_world_changed()
		return
	if hud != null and hud.is_over_backpack() and Backpack.stash(item):
		_on_world_changed()
		return
	_on_world_changed()


func leave() -> void:
	Game.set_room_state(area_id, room.room_id, RoomSnapshot.capture(room))
	Game.save_now()
	left_area.emit()
	SceneRouter.goto_map()


func _check_load_time() -> void:
	if load_ms > 2000.0:
		Log.warn("Bereichswechsel dauerte %.0f ms (Ziel < 2000 ms)" % load_ms)
