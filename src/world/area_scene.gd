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
var area_file: Dictionary = {}       ## data/areas/<bereich>.json (alle Räume)
var room: Room
var camera: WorldCamera
var drag: DragController
var hud: AreaHud
var ui: CanvasLayer                  ## Ebene für UI-Panels (Rucksack, Album, Eltern …)
var me: ItemNode                     ## die eigene Figur
var light_mod: CanvasModulate        ## P07-T05: Raum dunkel, wenn der Licht-Schalter aus ist
var pets: Array = []                 ## [PetNode]
var load_ms: float = 0.0
var _t0: int = 0


func _ready() -> void:
	_t0 = Time.get_ticks_usec()
	area_id = SceneRouter.take_pending_area()
	if area_id == &"":
		area_id = Areas.first_ready()
	area = Areas.get_area(area_id)
	area_file = Room.load_area(Areas.path_of(area_id))
	area["default_items"] = area_file.get("default_items", [])
	if area.is_empty():
		push_error("AreaScene: unbekannter Bereich '%s'" % String(area_id))
		return
	_build_world()
	_enter_room(_start_room(), true)
	_build_hud()
	load_ms = (Time.get_ticks_usec() - _t0) / 1000.0
	SceneRouter.last_load_ms = load_ms
	Log.info("Bereich '%s' betreten (%.0f ms, %d Items)" % [
		String(area_id), load_ms, Placement.all_items(room).size()])
	_check_load_time()


## P07: Räume dieses Bereichs (Reihenfolge wie in der Datei).
func room_ids() -> Array:
	var out: Array = []
	for r: Variant in Array(area_file.get("rooms", [])):
		out.append(String((r as Dictionary).get("id", "")))
	return out


func room_data(rid: String) -> Dictionary:
	for r: Variant in Array(area_file.get("rooms", [])):
		if String((r as Dictionary).get("id", "")) == rid:
			return r
	return {}


## Weiter im zuletzt besuchten Raum, sonst im Start-Raum des Bereichs.
func _start_room() -> String:
	var ids: Array = room_ids()
	var last: String = Game.last_room(area_id)
	if ids.has(last):
		return last
	var r: String = Areas.room_of(area_id)
	if ids.has(r):
		return r
	return String(ids[0]) if not ids.is_empty() else ""


func _build_world() -> void:
	var garden_timer := Timer.new()                      # P07-T07: Garten-Uhr (1 s)
	garden_timer.wait_time = 1.0
	garden_timer.autostart = true
	garden_timer.timeout.connect(func() -> void:
		if room != null and Garden.tick(room) > 0:
			_on_world_changed())
	add_child(garden_timer)
	camera = WorldCamera.new()
	add_child(camera)
	drag = DragController.new()
	add_child(drag)
	drag.camera = camera
	drag.item_dropped.connect(_on_item_dropped)
	drag.item_tapped.connect(_on_item_tapped)
	light_mod = CanvasModulate.new()
	add_child(light_mod)


func _enter_room(rid: String, first: bool) -> void:
	room = ROOM_SCENE.instantiate()
	add_child(room)
	move_child(room, 0)
	room.setup(room_data(rid), Game.room_decor(area_id, StringName(rid)))
	var spawn: Vector2 = _spawn_point()
	camera.setup_for_room(room, spawn.x)
	if first:
		drag.attach_room(room)
	else:
		drag.reset_for_room(room)
	Game.set_last_room(area_id, room.room_id)
	_spawn(spawn)
	Garden.catch_up(room)                                # während der Abwesenheit gewachsen/verwelkt
	RoomLight.apply(room, light_mod)


## Start-Raum: Spawn-Punkt aus der Stadtkarte. Andere Räume: Mitte, halb vorn im Bodenband.
func _spawn_point() -> Vector2:
	if String(room.room_id) == Areas.room_of(area_id):
		return Areas.spawn_of(area_id)
	var front: float = room.floor_band.front_y_cm if room.floor_band != null else 70.0
	return Vector2(minf(room.width_cm * 0.5, 400.0), front * 0.5)


## P07-T01: in einen anderen Raum gehen – der alte Raum wird gespeichert, Figur und eigene Tiere kommen mit.
func switch_room(rid: String) -> bool:
	if room == null or rid == String(room.room_id) or not room_ids().has(rid):
		return false
	Game.set_room_state(area_id, room.room_id, RoomSnapshot.capture(room))
	var old: Room = room
	remove_child(old)
	old.queue_free()
	me = null
	pets.clear()
	_enter_room(rid, false)
	if hud != null:
		hud.show_room_buttons(room_ids().size() > 1, room.can_decorate())
	AudioBus.play_sfx("ui_confirm")
	Game.mark_dirty(area_id, room.room_id)
	return true


## P07-T04: Tapete/Boden des aktuellen Raums ändern (wird gespeichert).
func set_decor(d: Dictionary) -> void:
	if room == null or not room.can_decorate():
		return
	var chosen: Dictionary = Game.room_decor(area_id, room.room_id)
	chosen.merge(d, true)
	Game.set_room_decor(area_id, room.room_id, chosen)
	room.apply_decor(chosen)


func _spawn(spawn: Vector2) -> void:
	var state: Array = Game.room_state(area_id, room.room_id)
	if state.is_empty() and not _defaults_for_room().is_empty():
		_spawn_defaults()
	else:
		var n: int = RoomSnapshot.apply(room, state)
		Log.info("Raumzustand geladen: %d Items" % n)
		_spawn_me(spawn)
	_spawn_pets(spawn)
	if me != null:
		_arrive(me)


## Start-Ausstattung: je Raum (`default_items` im Raum), sonst die des Bereichs für den Start-Raum.
func _defaults_for_room() -> Array:
	var own: Array = Array(room.data.get("default_items", []))
	if not own.is_empty():
		return own
	if String(room.room_id) == Areas.room_of(area_id):
		return Array(area.get("default_items", []))
	return []


func _spawn_defaults() -> void:
	var list: Array = _defaults_for_room()
	var by_id: Dictionary = {}
	for e: Variant in list:
		var d: Dictionary = e
		if d.has("on"):
			continue                       # Dinge auf Tischen kommen im zweiten Durchgang
		var did := StringName(String(d["id"]))
		var ddef: ItemDefinition = ItemDB.get_item(did)
		if ddef != null and ddef.is_wall():             # Licht-Schalter, Bilder … hängen an der Wand (y = Oberkante)
			by_id[String(d["id"])] = ItemSpawner.on_wall(room, did, float(d.get("x_cm", 0.0)), float(d.get("y_cm", -120.0)))
			continue
		by_id[String(d["id"])] = ItemSpawner.on_floor(room, did, float(d.get("x_cm", 0.0)), float(d.get("y_cm", 0.0)))
	for e: Variant in list:
		var d: Dictionary = e
		if not d.has("on"):
			continue
		var host: ItemNode = by_id.get(String(d["on"]))
		if host != null:
			ItemSpawner.on_item(host, StringName(String(d["id"])), float(d.get("x_rel", 0.0)))
	_spawn_me(_spawn_point())


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
			PetLook.apply(pet.sprite, [pd.fur, pd.fur2, pd.collar], pd.pattern)
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
	hud.catalog.connect(func() -> void: CatalogPanel.open(ui, place_from_catalog))
	hud.rooms.connect(func() -> void: RoomPicker.open(ui, self))
	hud.decor.connect(func() -> void: DecorPanel.open(ui, self))
	hud.show_room_buttons(room_ids().size() > 1, room != null and room.can_decorate())
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
	var it: ItemNode = ItemSpawner.place(room, StringName(id), x, y)
	if it != null:
		_on_world_changed()
	return it != null


## P04b-T09: Item aus dem Katalog in den freien Teil des Bildes stellen (links neben der Katalog-Leiste).
## n = wievieltes Ding in dieser Katalog-Sitzung → leicht versetzt, damit nichts übereinander liegt.
func place_from_catalog(id: String, n: int = 0) -> bool:
	var x: float = Areas.spawn_of(area_id).x
	if camera != null:
		var vp_w: float = get_viewport().get_visible_rect().size.x
		var view_w_cm: float = vp_w / maxf(camera.zoom.x, 0.001)
		var free_frac: float = 1.0 - CatalogPanel.WIDTH_FRAC        # sichtbarer Teil links der Leiste
		x = camera.get_screen_center_position().x - view_w_cm * 0.5 + view_w_cm * free_frac * 0.5
		x += float((n % 5) - 2) * view_w_cm * free_frac * 0.16
	var back: float = room.floor_band.back_y_cm if room.floor_band != null else 0.0
	var front: float = room.floor_band.front_y_cm if room.floor_band != null else 80.0
	var depth: float = lerpf(back, front, [0.55, 0.3, 0.8][n % 3])
	var it: ItemNode = ItemSpawner.place(room, StringName(id), x, depth)   # Wand-Items hängen sich auf
	if it == null:
		return false
	AudioBus.play_item_sfx(it.def, "drop")
	_on_world_changed()
	return true


## Tippen: Tür → in einen anderen Raum (P07: „Wechsel über Türen"), sonst Zustand merken + Licht prüfen.
func _on_item_tapped(it: ItemNode) -> void:
	var id: String = String(it.def.id)
	if (id.begins_with("door_") or id.begins_with("garden_gate")) and room_ids().size() > 1 and ui != null:
		RoomPicker.open(ui, self)
	_on_world_changed()


func _on_world_changed() -> void:
	if room != null:
		RoomLight.apply(room, light_mod)
	Game.set_room_state(area_id, room.room_id, RoomSnapshot.capture(room))
	Game.mark_dirty(area_id, room.room_id)


## Ding auf den Rucksack-Knopf gezogen? → einpacken.
func _on_item_dropped(item: ItemNode, _target) -> void:
	if room != null and Garden.on_drop(room, item):      # P07-T07: gesät oder gegossen
		_on_world_changed()
		return
	var host: Node = item.get_parent().get_parent() if item.get_parent() != null else null
	if host is ItemNode:
		Recipes.check(host as ItemNode)          # P04b-T10: Zutat ins (eingeschaltete) Gerät → kochen
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
