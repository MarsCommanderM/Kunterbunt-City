class_name NpcWork
extends RefCounted
## P08-T04: Was eine Rolle bei der Arbeit tut. Animationen sind Platzhalter aus Arm-/Körper-Bewegungen des Rigs:
##   arm_up   (wave, point, whistle, offer, lever, deliver) · arm_work (scan, type, stock, repair, sweep, arrange,
##   feed, water, listen, clap) · nod (nod) · look (dreht sich um und wieder zurück).
## Rollen-Aktionen:
##   watch  (Kasse)        : Ding neben der Kasse abgelegt → Piep, Kasse springt auf, Ding wandert in eine Tüte
##   water  (Bademeister)  : Figur im Becken → nach RESCUE_S holt er sie raus (Pfiff) · rennende Figur → Pfiff
##   deliver(Briefträger)  : alle deliver_every_s zum Briefkasten, legt Post davor, läuft zurück

const ANIM_S: float = 1.2
const MOTION: Dictionary = {"wave": "arm_up", "point": "arm_up", "whistle": "arm_up", "offer": "arm_up", "lever": "arm_up",
	"deliver": "arm_up", "scan": "arm_work", "type": "arm_work", "stock": "arm_work", "repair": "arm_work",
	"sweep": "arm_work", "arrange": "arm_work", "feed": "arm_work", "water": "arm_work", "listen": "arm_work",
	"clap": "arm_work", "nod": "nod", "look": "look"}
const SOUND: Dictionary = {"scan": "scan_beep", "whistle": "whistle", "clap": "clap", "deliver": "drop_paper"}
const WATCH_CM: float = 90.0          ## so nah an der Kasse muss ein Ding landen
const SCAN_MAX_H_CM: float = 60.0
const BAG_ID: StringName = &"shop_bag_coral"
const RESCUE_S: float = 10.0
const RUN_CM_S: float = 260.0
const WHISTLE_COOLDOWN_S: float = 4.0
const POOL_RANGE_CM: float = 300.0
const MAIL_NEAR_CM: float = 90.0

var brain: NpcBrain
var scanned: int = 0                  ## gezählt für Tests/Beweis
var rescued: int = 0
var whistles: int = 0
var delivered: int = 0
var _busy: float = 0.0
var _tween: Tween
var _under: Dictionary = {}           ## instance_id → Sekunden im Wasser
var _last_pos: Dictionary = {}        ## instance_id → letzte Position (global)
var _whistle_cd: float = 0.0
var _mail_t: float = 0.0
var _water_acc: float = 0.0           ## Becken nur 4× pro Sekunde prüfen (spart Zeit bei 250 Items)
var _task: String = ""                ## "" | deliver | rescue
var _rescue: ItemNode


func _init(b: NpcBrain) -> void:
	brain = b


func busy() -> bool:
	return _busy > 0.0


func stop() -> void:
	_busy = 0.0
	_task = ""
	if _tween != null and _tween.is_valid():
		_tween.kill()
	_reset_pose()


func tick(dt: float) -> void:
	_busy = maxf(0.0, _busy - dt)
	_whistle_cd = maxf(0.0, _whistle_cd - dt)
	_mail_t += dt
	if not _water_prefixes().is_empty():
		_water_acc += dt
		if _water_acc >= 0.25:
			_watch_water(_water_acc)
			_water_acc = 0.0


# ---------------------------------------------------------------- Animationen (Platzhalter)

func play(anim: String) -> void:
	_busy = ANIM_S
	if SOUND.has(anim):
		AudioBus.play_sfx(String(SOUND[anim]))
	var rig: CharacterRig = brain.body
	if not CharacterRig.animate_poses or not rig.is_inside_tree() or Settings.reduced_motion:
		return
	if _tween != null and _tween.is_valid():
		_tween.kill()
	_tween = rig.create_tween()
	match String(MOTION.get(anim, "look")):
		"arm_up":
			_tween.tween_property(rig.arm_front, "rotation", -2.4, 0.25).set_trans(Tween.TRANS_BACK)
			for k: int in 2:
				_tween.tween_property(rig.arm_front, "rotation", -2.0, 0.15)
				_tween.tween_property(rig.arm_front, "rotation", -2.5, 0.15)
		"arm_work":
			for k: int in 3:
				_tween.tween_property(rig.arm_front, "rotation", -0.9, 0.14)
				_tween.tween_property(rig.arm_front, "rotation", -0.35, 0.14)
		"nod":
			for k: int in 2:
				_tween.tween_property(rig.head_pivot, "rotation", 0.12, 0.15)
				_tween.tween_property(rig.head_pivot, "rotation", 0.0, 0.15)
		_:
			var f: float = rig.swing.scale.x
			_tween.tween_property(rig.swing, "scale:x", -f, 0.12)
			_tween.tween_interval(0.6)
			_tween.tween_property(rig.swing, "scale:x", f, 0.12)
	_tween.tween_callback(_reset_pose)


func _reset_pose() -> void:
	if is_instance_valid(brain.body):
		brain.body.head_pivot.rotation = 0.0
		brain.body.refresh_pose(false)


## Antippen: die Figur winkt zurück.
func greet() -> void:
	play("wave")
	brain.worked.emit("wave")


# ---------------------------------------------------------------- Kasse

func _watch_prefixes() -> Array:
	var w: Variant = brain.role.get("watch", "")
	return (w as Array) if w is Array else ([String(w)] if String(w) != "" else [])


func on_item_dropped(item: ItemNode) -> bool:
	if item == null or item is CharacterRig or item.def.height_cm > SCAN_MAX_H_CM or item.def.hold == "none":
		return false
	var register: ItemNode = _nearest_prefixed(_watch_prefixes(), item.global_position, WATCH_CM)
	if register == null or register == item or String(item.def.id).begins_with("shop_bag"):
		return false
	scan(item, register)
	return true


## Piep, Kasse auf, Ding in die Tüte (neben der Kasse; eine vorhandene Tüte mit Platz wird weiter befüllt).
func scan(item: ItemNode, register: ItemNode) -> ItemNode:
	brain.face(signf(register.global_position.x - brain.body.global_position.x))
	brain.play_work("scan")
	if register.def.states.has("open"):
		ItemStates.set_state(register, "open", true)
	scanned += 1
	var bag: ItemNode = _nearest_prefixed(["shop_bag"], register.global_position, 160.0)
	if bag == null or bag.free_slot() < 0:
		var p: Vector2 = brain.room.ysort_root.to_local(register.global_position)
		bag = ItemSpawner.on_floor(brain.room, BAG_ID, p.x + 70.0, brain.room.floor_band.front_y_cm * 0.6)
	if bag != null and bag.def.is_container() and item.def.height_cm <= bag.def.container_max_item_h_cm \
			and bag.free_slot() >= 0:
		var slot: int = bag.free_slot()
		item.reparent(bag.contents_root, false)
		item.position = Vector2.ZERO
		item.rotation = 0.0
		item.slot_index = slot
		bag.relayout_contents()
	return bag


# ---------------------------------------------------------------- Briefträger/in

func start_delivery() -> bool:
	if _mail_t < float(brain.role.get("deliver_every_s", 90.0)):
		return false
	var box: ItemNode = _nearest_prefixed([String(brain.role.get("target", ""))], brain.body.global_position, INF)
	if box == null:
		return false
	_mail_t = 0.0
	_task = "deliver"
	brain.walk_to(brain.room.ysort_root.to_local(box.global_position) + Vector2(-50.0, 8.0))
	return true


## Weg zu Ende: true = die Rolle macht jetzt etwas (Brain bleibt nicht einfach stehen).
func arrived() -> bool:
	match _task:
		"deliver":
			_task = ""
			_deliver_mail()
			AudioBus.play_sfx(String(SOUND["deliver"]))
			brain.worked.emit("deliver")
			brain.walk_to(brain.post)                    # gleich wieder zurück
			return true
		"rescue":
			_task = ""
			_pull_out()
			return true
	return false


func _deliver_mail() -> void:
	var id := StringName(String(brain.role.get("deliver", "")))
	if id == &"" or not ItemDB.has_item(id):
		return
	var p: Vector2 = brain.body.position
	if _nearest_prefixed([String(id)], brain.room.ysort_root.to_global(p), MAIL_NEAR_CM) != null:
		return                                             # da liegt noch Post – nicht alles zumüllen
	if ItemSpawner.on_floor(brain.room, id, p.x + 30.0, p.y + 6.0) != null:
		delivered += 1


# ---------------------------------------------------------------- Bademeister/in

func _water_prefixes() -> Array:
	var w: Variant = brain.role.get("water", [])
	return (w as Array) if w is Array else [String(w)]


func in_water(c: ItemNode) -> bool:
	var host: ItemNode = Seats.seat_host_of(c)
	if host == null:
		return false
	for p: Variant in _water_prefixes():
		if String(host.def.id).begins_with(String(p)):
			return true
	return false


func _figures() -> Array:
	var out: Array = []
	for it: ItemNode in Placement.all_items(brain.room):
		if it is CharacterRig and it != brain.body and not it.has_meta("npc_id"):
			out.append(it)
	var dl: Node = brain.room.get_node_or_null("DragLayer")
	if dl != null:
		for c: Node in dl.get_children():
			if c is CharacterRig and not c.has_meta("npc_id"):
				out.append(c)
	return out


func _watch_water(dt: float) -> void:
	var pool: ItemNode = _nearest_prefixed(_water_prefixes(), brain.body.global_position, INF)
	for c: ItemNode in _figures():
		var key: int = c.get_instance_id()
		if in_water(c):
			_under[key] = float(_under.get(key, 0.0)) + dt
			if float(_under[key]) >= RESCUE_S and _task != "rescue" and brain.state != NpcBrain.State.CARRIED:
				_start_rescue(c)
		else:
			_under.erase(key)
		var gp: Vector2 = c.global_position
		if _last_pos.has(key) and dt > 0.0 and pool != null and _whistle_cd <= 0.0:
			var v: float = gp.distance_to(_last_pos[key]) / dt
			if v > RUN_CM_S and absf(gp.x - pool.global_position.x) < POOL_RANGE_CM:
				_whistle_cd = WHISTLE_COOLDOWN_S
				whistles += 1
				if not brain.is_carried():
					brain.play_work("whistle")
		_last_pos[key] = gp


func _start_rescue(c: ItemNode) -> void:
	_rescue = c
	_task = "rescue"
	whistles += 1
	AudioBus.play_sfx("whistle")
	var host: ItemNode = Seats.seat_host_of(c)
	var edge: Vector2 = brain.room.ysort_root.to_local(host.global_position if host else c.global_position)
	edge.x += (host.def.width_cm * 0.5 + 40.0) if host else 60.0
	brain.walk_to(edge)


## Figur aus dem Wasser holen: neben das Becken auf den Boden, erschrocken → fröhlich.
func _pull_out() -> void:
	if not is_instance_valid(_rescue) or not in_water(_rescue):
		return
	var c: ItemNode = _rescue
	c.reparent(brain.room.ysort_root, true)
	c.slot_index = -1
	c.rotation = 0.0
	c.position = NpcPath.clamp_to_room(brain.room, brain.body.position + Vector2(40.0, 4.0))
	c.scale = Vector2.ONE * brain.room.floor_band.depth_factor(c.position.y)
	if c is CharacterRig:
		(c as CharacterRig).refresh_pose(false)
		(c as CharacterRig).set_emotion("surprised")
	_under.erase(c.get_instance_id())
	rescued += 1
	brain.play_work("whistle")


# ---------------------------------------------------------------- Hilfen

func _nearest_prefixed(prefixes: Array, at: Vector2, max_d: float) -> ItemNode:
	var best: ItemNode = null
	var bd: float = max_d
	for it: ItemNode in Placement.all_items(brain.room):
		var id: String = String(it.def.id)
		for p: Variant in prefixes:
			if String(p) != "" and id.begins_with(String(p)):
				var d: float = absf(it.global_position.x - at.x) + absf(it.global_position.y - at.y) * 0.5
				if d <= bd:
					bd = d
					best = it
				break
	return best
