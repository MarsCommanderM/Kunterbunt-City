class_name DragController
extends Node
## Anfassen, Ziehen, Abstellen (Tech-Spec §4.1, P02-T04).
## IDLE → PRESS → LIFT (nach 80 ms oder 8 px) → DRAG → DROP. Bis zu 3 Items gleichzeitig (Multitouch).
## Öffentliche API arbeitet in Welt-cm (press/move/release) – Eingabe-Events werden nur übersetzt.
## Muss im Baum NACH der Kamera stehen, damit es Eingaben zuerst bekommt.

signal item_picked_up(item: ItemNode)
signal item_dropped(item: ItemNode, target: Placement.Target)
signal item_tapped(item: ItemNode)

const LIFT_DELAY_S: float = 0.08
const LIFT_MOVE_PX: float = 8.0
const TAP_MAX_S: float = 0.3
const MAX_DRAGS: int = 3
const FOLLOW_SHARPNESS: float = 28.0   ## „folgt dem Finger mit leichter Verzögerung“
const MOUSE_ID: int = 1000

enum State { PRESS, DRAG }

@export var room: Room
@export var camera: WorldCamera
## Tests schalten Animationen ab (sofortiges Einrasten).
@export var animate: bool = true

var undo: UndoStack = UndoStack.new()
var drag_layer: Node2D
var _drags: Dictionary = {}            ## pointer id → Drag
var _now_override: float = -1.0        ## Tests: feste Zeit


class Drag:
	var item: ItemNode
	var state: int = State.PRESS
	var press_world: Vector2
	var press_time: float
	var pointer_world: Vector2
	var grab_offset: Vector2
	var last_pos: Vector2
	var velocity: Vector2 = Vector2.ZERO
	var moved_px: float = 0.0
	var from_parent: Node
	var from_pos: Vector2
	var from_scale: Vector2
	var from_slot: int = -1


func _ready() -> void:
	set_process(false)
	if room:
		attach_room(room)


func attach_room(r: Room) -> void:
	room = r
	drag_layer = room.get_node_or_null("DragLayer")
	if drag_layer == null:
		drag_layer = Node2D.new()
		drag_layer.name = "DragLayer"
		drag_layer.z_index = 60
		room.add_child(drag_layer)


func active_count() -> int:
	return _drags.size()


func is_dragging(item: ItemNode) -> bool:
	for d: Drag in _drags.values():
		if d.item == item:
			return true
	return false


# ---------------------------------------------------------------- öffentliche API (Welt-cm)

## Finger/Maus runter. true = ein Item wurde getroffen (Event gehört dem Controller).
func press(id: int, world: Vector2) -> bool:
	if _drags.size() >= MAX_DRAGS or _drags.has(id):
		return false
	var item: ItemNode = pick_item(world)
	if item == null or is_dragging(item):
		return false
	if not item.def.movable and not item.def.is_container():
		return false                    # feste Dinge ohne Funktion: Kamera darf scrollen
	var d := Drag.new()
	d.item = item
	d.press_world = world
	d.pointer_world = world
	d.press_time = _now()
	_drags[id] = d
	set_process(true)
	return true


func move(id: int, world: Vector2) -> void:
	if not _drags.has(id):
		return
	var d: Drag = _drags[id]
	d.pointer_world = world
	d.moved_px = maxf(d.moved_px, (world - d.press_world).length() * _zoom())
	if d.state == State.PRESS and d.moved_px >= LIFT_MOVE_PX and d.item.def.movable:
		_lift(d)


func release(id: int, world: Vector2) -> void:
	if not _drags.has(id):
		return
	var d: Drag = _drags[id]
	d.pointer_world = world
	_drags.erase(id)
	var is_tap: bool = d.moved_px < LIFT_MOVE_PX and _now() - d.press_time <= TAP_MAX_S
	if d.state == State.PRESS:
		if d.moved_px < LIFT_MOVE_PX and (is_tap or not d.item.def.movable):
			_tap(d.item, world)
	elif is_tap:
		_restore(d)
		_tap(d.item, world)
	else:
		_drop(d)
	set_process(not _drags.is_empty())


## Oberstes greifbares Item unter dem Punkt (Mindest-Tippfläche 48 dp).
func pick_item(world: Vector2) -> ItemNode:
	var min_world: float = UiConstants.MIN_TOUCH_DP / _zoom()
	var best: ItemNode = null
	var best_key: Vector4 = Vector4(-INF, -INF, -INF, -INF)
	for it: ItemNode in Placement.all_items(room):
		if not it.is_visible_in_tree() or not it.hit_test(world, min_world):
			continue
		# direkt getroffen schlägt „nur über die 48-dp-Tippfläche“ (sonst wäre im Tellerstapel nur der oberste greifbar)
		var dk: Vector3 = _draw_key(it)
		var key := Vector4(1.0 if it.global_rect().has_point(world) else 0.0, dk.x, dk.y, dk.z)
		if key > best_key:
			best_key = key
			best = it
	return best


## Ein Punkt, an dem das Item wirklich greifbar ist (sichtbare Pixel, nicht verdeckt) – für Skripte/Tests/NPCs.
func grab_point(item: ItemNode) -> Vector2:
	var r: Rect2 = item.global_rect()
	for fy: float in [0.5, 0.3, 0.12, 0.7, 0.9]:
		for fx: float in [0.5, 0.35, 0.65, 0.1, 0.9]:
			var p: Vector2 = r.position + r.size * Vector2(fx, fy)
			if pick_item(p) == item:
				return p
	return r.get_center()


## Skript-Zug: greift das Item und setzt seinen Pivot bei pivot_target ab (gleicher Weg wie ein Finger).
func scripted_move(item: ItemNode, pivot_target: Vector2, id: int = 90) -> void:
	var grab: Vector2 = grab_point(item)
	var offset: Vector2 = item.global_position - grab
	press(id, grab)
	move(id, grab + Vector2(0, -20))
	move(id, pivot_target - offset)
	release(id, pivot_target - offset)


# ---------------------------------------------------------------- intern

## Zeichenreihenfolge-Schlüssel: (y des Boden-Vorfahren, Schachtelungstiefe, −Fläche → kleinere zuerst)
func _draw_key(it: ItemNode) -> Vector3:
	var n: Node = it
	var depth: int = 0
	while n.get_parent() and n.get_parent() != room.ysort_root:
		n = n.get_parent()
		depth += 1
	var y: float = (n as Node2D).position.y if n is Node2D else 0.0
	var r: Rect2 = it.global_rect()
	return Vector3(y, depth, -r.size.x * r.size.y)


func _lift(d: Drag) -> void:
	var it: ItemNode = d.item
	d.from_parent = it.get_parent()
	d.from_pos = it.position
	d.from_scale = it.scale
	d.from_slot = it.slot_index
	d.grab_offset = it.global_position - d.press_world   # Stelle, an der angefasst wurde, bleibt unter dem Finger
	it.reparent(drag_layer, true)
	it.slot_index = -1
	it.rotation = 0.0                       # aus der Hand genommen: wieder aufrecht
	_relayout_owner(d.from_parent)
	it.on_drag_start(d.press_world)
	d.last_pos = it.global_position
	it.set_lifted(true, animate)
	d.state = State.DRAG
	AudioBus.play_item_sfx(it.def, "pickup")
	item_picked_up.emit(it)


func _process(delta: float) -> void:
	for d: Drag in _drags.values():
		if d.state == State.PRESS:
			if d.item.def.movable and _now() - d.press_time >= LIFT_DELAY_S:
				_lift(d)
			continue
		var target: Vector2 = d.pointer_world + d.grab_offset
		var k: float = 1.0 if not animate else 1.0 - exp(-FOLLOW_SHARPNESS * delta)
		d.item.global_position = d.item.global_position.lerp(target, k)
		var s: float = room.floor_band.depth_factor(d.item.global_position.y)
		d.item.global_scale = d.item.global_scale.lerp(Vector2(s, s), k)
		if delta > 0.0:
			d.velocity = d.velocity.lerp((d.item.global_position - d.last_pos) / delta, 0.35)
		d.last_pos = d.item.global_position
		d.item.on_drag_update(delta, d.velocity)


func _drop(d: Drag) -> void:
	var it: ItemNode = d.item
	var pivot: Vector2 = d.pointer_world + d.grab_offset
	var t: Placement.Target = Placement.find_target(room, it, pivot, d.pointer_world)
	it.on_drag_end()
	it.reparent(t.parent, true)
	var parent_scale: float = (t.parent as Node2D).global_scale.y if t.parent is Node2D else 1.0
	var final_local: Vector2 = (t.parent as Node2D).to_local(t.global_pos)
	var final_scale: Vector2 = Vector2.ONE * (t.global_scale / maxf(parent_scale, 0.0001))
	it.slot_index = t.slot
	undo.push(it, d.from_parent, d.from_pos, d.from_scale, d.from_slot)
	if t.kind == &"container":
		var c: ItemNode = t.node
		var lay: Dictionary = c.content_layout()
		(c.contents_root as ItemNode.ContentsPanel).rect = lay["rect"]
		c.contents_root.queue_redraw()
		final_local = lay[it]
	elif t.kind == &"hand":
		final_local = CharacterRig.grip_local(it)   # Griffpunkt = Slot-Ursprung, egal wie der Arm steht
	it.set_lifted(false, animate)
	if animate:
		var dist: float = absf(t.global_pos.y - it.global_position.y)
		var tw: Tween = it.create_tween().set_parallel(true)
		tw.tween_property(it, "position", final_local, Placement.fall_time(dist)) \
			.set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tw.tween_property(it, "scale", final_scale, Placement.fall_time(dist))
	else:
		it.position = final_local
		it.scale = final_scale
	it.on_placed()
	_relayout_owner(t.parent)
	if t.kind == &"hand":
		it.rotation = 0.0                   # Slot dreht (aufrecht + Haltewinkel), Item selbst nicht
	elif t.kind == &"mouth" and t.node.has_method("eat"):
		t.node.eat(it, animate)
	if not t.rejected_reason.is_empty():
		AudioBus.play_sfx("deny")
		Log.debug("Drop abgelehnt: " + t.rejected_reason)
	AudioBus.play_item_sfx(it.def, "drop")
	item_dropped.emit(it, t)


func _restore(d: Drag) -> void:
	d.item.reparent(d.from_parent, false)
	d.item.position = d.from_pos
	d.item.scale = d.from_scale
	d.item.slot_index = d.from_slot
	d.item.set_lifted(false, animate)
	d.item.on_drag_end()
	d.item.on_placed()
	_relayout_owner(d.from_parent)


## Behälter-Inhalt neu ordnen bzw. Figur neu posieren (Hand/Sitz hat sich geändert).
static func _relayout_owner(node: Node) -> void:
	if node and node.name == "Contents" and node.get_parent() is ItemNode:
		(node.get_parent() as ItemNode).relayout_contents()
	var n: Node = node
	while n and not (n is ItemNode):
		n = n.get_parent()
	if n and n.has_method("refresh_pose"):
		n.refresh_pose(true)


func _tap(item: ItemNode, world: Vector2 = Vector2.INF) -> void:
	if world.is_finite():
		item.on_tap_at(world)
	else:
		item.on_tap()
	item_tapped.emit(item)


func _zoom() -> float:
	return camera.zoom.x if camera else Units.zoom_for_visible_height(1080.0, Units.DEFAULT_VIEW_HEIGHT_CM)


func _now() -> float:
	return _now_override if _now_override >= 0.0 else Time.get_ticks_msec() / 1000.0


# ---------------------------------------------------------------- Eingaben übersetzen

func _unhandled_input(event: InputEvent) -> void:
	if camera == null:
		return
	if event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var w: Vector2 = camera.screen_to_world(event.position)
		if event.pressed:
			if press(MOUSE_ID, w):
				get_viewport().set_input_as_handled()
		elif _drags.has(MOUSE_ID):
			release(MOUSE_ID, w)
			get_viewport().set_input_as_handled()
	elif event is InputEventMouseMotion and _drags.has(MOUSE_ID):
		move(MOUSE_ID, camera.screen_to_world(event.position))
		get_viewport().set_input_as_handled()
	elif event is InputEventScreenTouch:
		var t := event as InputEventScreenTouch
		var tw: Vector2 = camera.screen_to_world(t.position)
		if t.pressed:
			if press(t.index, tw):
				get_viewport().set_input_as_handled()
		elif _drags.has(t.index):
			release(t.index, tw)
			get_viewport().set_input_as_handled()
	elif event is InputEventScreenDrag and _drags.has((event as InputEventScreenDrag).index):
		move(event.index, camera.screen_to_world(event.position))
		get_viewport().set_input_as_handled()
