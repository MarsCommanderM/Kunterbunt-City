class_name NpcBrain
extends Node
## P08-T01: Zustandsmaschine einer festen Figur (Tech-Spec §4.5). Hängt als Kind an ihrer CharacterRig.
##   IDLE   → wartet (Zufall work_every_s), dann WORK (Arbeits-Animation) oder WALK (patrol/wander/deliver)
##   WALK   → läuft einen Weg ab (NpcPath: um große Möbel herum, immer im Bodenband)
##   WORK   → spielt eine Arbeits-Animation (NpcWork), danach IDLE
##   CARRIED→ ein Kind trägt die Figur (Arme hoch, staunt)
##   REACT  → gerade abgesetzt oder angetippt: freut sich kurz
##   RETURN → spätestens return_after_s nach dem Absetzen: steht auf und läuft zurück an ihren Platz
## Garantien (tests/test_npc.gd): blockiert keinen Drop, verlässt nie den Raum, kehrt zurück, reagiert beim Tragen.

enum State { IDLE, WALK, WORK, CARRIED, REACT, RETURN }

signal state_changed(state: int)
signal worked(anim: String)

const REACT_S: float = 1.0
const ARRIVE_CM: float = 3.0
const HOME_CM: float = 20.0          ## weiter weg als das = „nicht am Platz"

## Global aus in Tests/Beweis-Runnern: dann bewegt sich nichts von selbst, nur per tick().
static var autonomous: bool = true

var role: Dictionary = {}
var npc: Dictionary = {}              ## Eintrag aus data/npcs/<bereich>.json
var body: CharacterRig
var room: Room
var post: Vector2                     ## Arbeitsplatz (cm, Raum-Koordinaten)
var state: int = State.IDLE
var path: Array = []                  ## restliche Wegpunkte
var anim: String = ""                 ## laufende Arbeits-Animation
var since_drop: float = -1.0          ## Sekunden seit dem Absetzen (−1 = nicht versetzt)
var patrol_dir: float = 1.0
var work: NpcWork
var _timer: float = 1.0
var _walk_t: float = 0.0
var _last: Vector2                    ## Position nach dem letzten tick → erkennt Versetzen zwischen zwei ticks
var _rng := RandomNumberGenerator.new()


static func attach(rig: CharacterRig, r: Room, role_data: Dictionary, npc_data: Dictionary) -> NpcBrain:
	var b := NpcBrain.new()
	b.name = "NpcBrain"
	b.body = rig
	b.room = r
	b.role = role_data
	b.npc = npc_data
	b.post = rig.position
	b._last = rig.position
	b._rng.seed = hash(String(npc_data.get("id", "npc")))
	b._timer = b._rng.randf_range(0.5, 2.0)
	b.work = NpcWork.new(b)
	rig.set_meta("npc_id", String(npc_data.get("id", "")))
	rig.add_child(b)
	rig.tapped.connect(func(_it: ItemNode) -> void: b.on_tapped())
	return b


func _ready() -> void:
	set_process(autonomous)


func _process(delta: float) -> void:
	if not autonomous:
		set_process(false)
		return
	tick(delta)


func speed() -> float:
	return float(role.get("speed_cm_s", 70.0))


func return_after() -> float:
	return float(role.get("return_after_s", 8.0))


func behavior() -> String:
	return String(role.get("behavior", "station"))


## Wird gerade getragen (hochgehoben oder außerhalb des Raums in der Zieh-Ebene)?
func is_carried() -> bool:
	return body.lifted > 0.01 or not room.is_ancestor_of(body)


func is_seated() -> bool:
	return body.get_parent() != room.ysort_root


func at_post() -> bool:
	return not is_seated() and body.position.distance_to(post) <= HOME_CM


func set_state(s: int) -> void:
	if s == state:
		return
	state = s
	match s:
		State.CARRIED:
			body.set_emotion("surprised")
			work.stop()
			path.clear()
		State.REACT:
			body.set_emotion("laugh")
			_timer = REACT_S
		State.RETURN:
			body.set_emotion("happy")
			_stand_up()
			path = NpcPath.route(room, body.position, post)
		State.IDLE:
			body.set_emotion("happy")
			_timer = _rng.randf_range(float(role["work_every_s"][0]), float(role["work_every_s"][1])) \
				if role.has("work_every_s") else 3.0
	state_changed.emit(s)


func tick(dt: float) -> void:
	if body == null or room == null:
		return
	if is_carried():
		set_state(State.CARRIED)
		since_drop = -1.0
		_set_walk_pose(false)
		return
	if state == State.CARRIED or (since_drop < 0.0 and _displaced()):    # gerade abgesetzt / versetzt
		since_drop = 0.0
		_last = body.position
		set_state(State.REACT)
		return
	if since_drop >= 0.0:
		since_drop += dt
		if since_drop >= return_after() - 0.001 and state != State.RETURN:
			since_drop = -1.0
			if at_post():
				set_state(State.IDLE)
			else:
				set_state(State.RETURN)
			return
	work.tick(dt)
	_tick_state(dt)
	_last = body.position


## Ohne eigenes Laufen woanders (Kind hat die Figur zwischen zwei ticks versetzt, Rückgängig) oder hingesetzt?
func _displaced() -> bool:
	if state == State.RETURN or state == State.WALK:
		return is_seated()
	return is_seated() or body.position.distance_to(_last) > HOME_CM


func _tick_state(dt: float) -> void:
	match state:
		State.REACT:
			_timer -= dt
			if _timer <= 0.0:
				set_state(State.IDLE)
		State.IDLE:
			if since_drop >= 0.0:
				return                                   # abgesetzt: wartet (freut sich), bis return_after_s um ist
			_timer -= dt
			if _timer <= 0.0:
				_next_action()
		State.WORK:
			if not work.busy():
				set_state(State.IDLE)
		State.WALK, State.RETURN:
			if is_seated():
				_stand_up()
			if _walk(dt):
				var was_return: bool = state == State.RETURN
				_set_walk_pose(false)
				if was_return or not work.arrived():
					set_state(State.IDLE)


## Nächste Tat je nach Verhalten der Rolle.
func _next_action() -> void:
	match behavior():
		"patrol":
			var reach: float = float(role.get("patrol_cm", 150.0))
			patrol_dir = -patrol_dir
			walk_to(post + Vector2(patrol_dir * reach, 0.0))
		"wander":
			var reach2: float = float(role.get("patrol_cm", 150.0))
			walk_to(post + Vector2(_rng.randf_range(-reach2, reach2), _rng.randf_range(-20.0, 20.0)))
		"deliver":
			if not work.start_delivery():
				play_work()
		_:
			play_work()


## Arbeits-Animation aus der Rolle (zufällig).
func play_work(which: String = "") -> void:
	var list: Array = Array(role.get("work", ["look"]))
	anim = which if which != "" else String(list[_rng.randi() % list.size()])
	set_state(State.WORK)
	work.play(anim)
	worked.emit(anim)


func walk_to(target: Vector2) -> void:
	path = NpcPath.route(room, body.position, target)
	set_state(State.WALK)


## Einen Schritt laufen. true = angekommen.
func _walk(dt: float) -> bool:
	if path.is_empty():
		return true
	var target: Vector2 = path[0]
	var to: Vector2 = target - body.position
	var step: float = speed() * dt
	if to.length() <= maxf(step, ARRIVE_CM):
		body.position = NpcPath.clamp_to_room(room, target)
		path.pop_front()
	else:
		body.position = NpcPath.clamp_to_room(room, body.position + to.normalized() * step)
		if absf(to.x) > 1.0:
			face(signf(to.x))
		_walk_t += dt
		_set_walk_pose(true)
	body.scale = Vector2.ONE * room.floor_band.depth_factor(body.position.y)
	return path.is_empty()


func face(dir: float) -> void:
	if dir != 0.0 and body.swing != null:
		body.swing.scale.x = -1.0 if dir < 0.0 else 1.0


func _set_walk_pose(on: bool) -> void:
	if body.swing != null and body.lifted <= 0.01:
		body.swing.rotation = sin(_walk_t * 12.0) * 0.05 if on else 0.0


## Sitzt/liegt die Figur (ein Kind hat sie aufs Sofa gesetzt)? → aufstehen, auf den Boden davor.
func _stand_up() -> void:
	if not is_seated():
		return
	var gp: Vector2 = body.global_position
	body.reparent(room.ysort_root, true)
	body.slot_index = -1
	var local: Vector2 = room.ysort_root.to_local(gp)
	body.position = NpcPath.clamp_to_room(room, Vector2(local.x, maxf(local.y, room.floor_band.back_y_cm + 10.0)))
	body.rotation = 0.0
	body.scale = Vector2.ONE * room.floor_band.depth_factor(body.position.y)
	body.refresh_pose(false)


func on_tapped() -> void:
	if state == State.CARRIED:
		return
	work.greet()
	if state != State.RETURN and state != State.WALK:
		set_state(State.REACT)


## Ein Ding wurde im Raum abgelegt (Kasse: scannen). true = die Rolle hat reagiert.
func on_item_dropped(item: ItemNode) -> bool:
	if state == State.CARRIED or state == State.RETURN:
		return false
	return work.on_item_dropped(item)
