class_name IceActions
extends RefCounted
## P10f Eishalle (AreaActions ruft on_dropped, AreaScene ruft tick/refresh):
##   Gleiten     : Figur auf dem Eis loslassen → gleitet mit dem Schwung des Ziehens weiter (ohne Schwung: Pirouette)
##   Kratzer     : nach 3 Fahrten ist das Eis zerkratzt · Eismaschine fährt alle 3 Min. übers Eis → glänzt wieder
##   Disco       : Discokugel an → farbiges Licht wandert durch die Halle
##   (Eishockey: Puck + Tor laufen über SportActions)

const RESURF_EVERY_S: float = 180.0
const DRIVE_S: float = 10.0
const GLIDE_S: float = 1.1
const GLIDE_MIN_CM: float = 50.0
const GLIDE_MAX_CM: float = 320.0
const SCRATCH_AFTER: int = 3

static var _surfaces: Array = []
static var _machines: Array = []
static var _discos: Array = []
static var _timer: float = 0.0
static var _hue: float = 0.0
static var _disco: bool = false
static var _glides: int = 0


## Eis-Dinge im Raum merken (beim Raumwechsel und nach Änderungen) → kein Suchen in jedem Frame.
static func refresh(room: Room) -> void:
	_surfaces.clear()
	_machines.clear()
	_discos.clear()
	if room == null:
		return
	for it: ItemNode in Placement.all_items(room):
		var id: String = String(it.def.id)
		if id.begins_with("ice_surface"):
			_surfaces.append(it)
		elif id.begins_with("ice_resurfacer"):
			_machines.append(it)
		elif id.begins_with("ice_disco_ball"):
			_discos.append(it)


static func surface_at(room: Room, p: Vector2) -> ItemNode:
	for it: ItemNode in Placement.all_items(room):
		if String(it.def.id).begins_with("ice_surface") and absf(p.x - it.position.x) < it.def.width_cm * 0.5 \
				and absf(p.y - it.position.y) < 60.0:
			return it
	return null


static func on_dropped(scene: AreaScene, item: ItemNode) -> bool:
	if not (item is CharacterRig) or item.get_parent() != scene.room.ysort_root:
		return false
	var ice: ItemNode = surface_at(scene.room, item.position)
	if ice == null:
		return false
	var v: Vector2 = item.get_meta("drop_velocity", Vector2.ZERO)
	glide(scene.room, item as CharacterRig, ice, v.x)
	return true


## Gleiten: Strecke aus dem Schwung (cm/s), auf der Eisfläche begrenzt. Kein Schwung → Pirouette auf der Stelle.
static func glide(room: Room, rig: CharacterRig, ice: ItemNode, vx: float) -> float:
	var dist: float = 0.0
	if absf(vx) >= 30.0:
		dist = clampf(absf(vx) * 0.4, GLIDE_MIN_CM, GLIDE_MAX_CM) * signf(vx)
	var half: float = ice.def.width_cm * 0.5 - 30.0
	var end_x: float = clampf(rig.position.x + dist, ice.position.x - half, ice.position.x + half)
	rig.set_emotion("laugh")
	AudioBus.play_sfx("drop_soft")
	Secrets.event("pirouette" if dist == 0.0 else "skate")
	_glides += 1
	if _glides >= SCRATCH_AFTER:
		ItemStates.set_state(ice, "scratched", true)
	var sx: float = absf(rig.scale.x)
	if not rig.is_inside_tree() or Settings.reduced_motion:
		rig.position.x = end_x
		return end_x
	var tw: Tween = rig.create_tween().set_parallel(true)
	tw.tween_property(rig, "position:x", end_x, GLIDE_S).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	if dist == 0.0:
		tw.tween_method(func(k: float) -> void: rig.scale.x = sx * cos(k * TAU * 2.0), 0.0, 1.0, GLIDE_S)
		tw.chain().tween_callback(func() -> void: rig.scale.x = sx)
	return end_x


static func tick(scene: AreaScene, dt: float) -> void:
	if not _machines.is_empty() and not _surfaces.is_empty():
		_timer += dt
		if _timer >= RESURF_EVERY_S:
			_timer = 0.0
			resurface(scene.room)
	var on: bool = false
	for d: Variant in _discos:
		if is_instance_valid(d) and (d as ItemNode).state == "on":
			on = true
	if on and scene.light_mod != null:
		_hue = fmod(_hue + dt * 0.25, 1.0)
		scene.light_mod.color = Color.from_hsv(_hue, 0.35, 1.0)
		if not _disco:
			Secrets.event("disco")
	elif _disco and scene.light_mod != null:
		RoomLight.apply(scene.room, scene.light_mod)
	_disco = on


## Eismaschine fährt einmal übers Eis (mit Fahrer/in, falls da) und stellt sich zurück → Eis glänzt.
static func resurface(room: Room) -> bool:
	if _machines.is_empty() or _surfaces.is_empty():
		refresh(room)
	if _machines.is_empty() or _surfaces.is_empty():
		return false
	var m: ItemNode = _machines[0]
	var ice: ItemNode = _surfaces[0]
	if not is_instance_valid(m) or not is_instance_valid(ice):
		return false
	for b: NpcBrain in NpcSpawner.brains(room):
		if String(b.role.get("id", "")) == "ice_driver" and Seats.occupant(m, 0) == null:
			PoolActions.seat_in(b.body, m, 0)
			break
	var home: float = m.position.x
	var shine := func() -> void:
		ItemStates.set_state(ice, "shiny", true)
		_glides = 0
		Secrets.event("shiny")
	AudioBus.play_sfx("rotor")
	if not m.is_inside_tree() or Settings.reduced_motion:
		shine.call()
		return true
	var half: float = ice.def.width_cm * 0.5
	var tw: Tween = m.create_tween()
	tw.tween_property(m, "position:x", ice.position.x + half, DRIVE_S * 0.5).set_trans(Tween.TRANS_SINE)
	tw.tween_callback(shine)
	tw.tween_property(m, "position:x", home, DRIVE_S * 0.5).set_trans(Tween.TRANS_SINE)
	return true
