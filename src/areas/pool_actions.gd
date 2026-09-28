class_name PoolActions
extends RefCounted
## P10c Freizeitbad (AreaActions ruft on_dropped/on_tapped):
##   Schwimmen    : Figur in ein Becken setzen (Sitzplatz im Wasser) → Platsch, Spritzer; danach tropft sie und trocknet
##   Sprungturm   : Figur neben dem Turm absetzen → klettert hoch, springt in hohem Bogen ins nächste Becken
##   Wasserrutsche: Figur an der Leiter der Rutsche absetzen → rutscht die Röhre hinunter ins Becken
##   Wellen-Anzeige an → alle Becken spritzen, Figuren im Wasser jubeln

const WATER: Array = ["swim_basin", "swim_baby_pool", "swim_whirlpool", "garden_pool"]
const JUMP_S: float = 1.2
const SLIDE_S: float = 1.6
const WET_S: float = 10.0                     ## so lange tropft eine Figur nach dem Baden


static func on_dropped(scene: AreaScene, item: ItemNode) -> bool:
	if not (item is CharacterRig):
		return false
	var rig := item as CharacterRig
	if water_of(rig) != null:
		splash(scene.room, rig)
		return false                          # Sitzen im Wasser erledigt der normale Drop
	var tower: ItemNode = _near_foot(scene.room, rig, "swim_diving_tower", 0.0, 1.0)
	if tower != null:
		return dive(scene, rig, tower)
	var slide: ItemNode = _near_foot(scene.room, rig, "swim_water_slide", 0.0, 0.3)
	if slide != null:
		return water_slide(scene, rig, slide)
	return false


static func on_tapped(scene: AreaScene, item: ItemNode) -> bool:
	if String(item.def.id).begins_with("swim_wave_sign") and item.state == "on":
		for it: ItemNode in Placement.all_items(scene.room):
			if _is_water(it):
				_spray(it)
				for i: int in it.def.seat_slots:
					var o: ItemNode = Seats.occupant(it, i)
					if o is CharacterRig:
						(o as CharacterRig).set_emotion("laugh")
		Secrets.event("waves")
		return true
	return false


static func _is_water(it: ItemNode) -> bool:
	for p: String in WATER:
		if String(it.def.id).begins_with(p):
			return true
	return false


## Becken, in dem die Figur sitzt (oder null).
static func water_of(rig: ItemNode) -> ItemNode:
	var host: ItemNode = Seats.seat_host_of(rig)
	return host if host != null and _is_water(host) else null


## Figur steht auf dem Boden im Bereich [from..to] (Anteil der Breite) des Geräts?
static func _near_foot(room: Room, rig: ItemNode, prefix: String, from: float, to: float) -> ItemNode:
	if rig.get_parent() != room.ysort_root:
		return null
	for o: ItemNode in Placement.all_items(room):
		if String(o.def.id).begins_with(prefix):
			var left: float = o.position.x - o.def.width_cm * 0.5
			if rig.position.x >= left + o.def.width_cm * from - 20.0 and rig.position.x <= left + o.def.width_cm * to + 20.0 \
					and absf(rig.position.y - o.position.y) < 60.0:
				return o
	return null


## Nächstes Becken mit freiem Platz (Sitz-Index) von p aus.
static func nearest_pool(room: Room, p: Vector2) -> Array:
	var best: Array = []
	var best_d: float = INF
	for it: ItemNode in Placement.all_items(room):
		if not String(it.def.id).begins_with("swim_basin") and not String(it.def.id).begins_with("garden_pool"):
			continue
		var i: int = Seats.free_index_near(it, p, INF)
		if i < 0:
			continue
		var d: float = it.position.distance_to(p)
		if d < best_d:
			best_d = d
			best = [it, i]
	return best


## Figur direkt auf Platz i des Beckens setzen (wie ein Drop auf den Sitzplatz).
static func seat_in(rig: CharacterRig, pool: ItemNode, i: int) -> void:
	var gp: Vector2 = Seats.point_global(pool, i) - rig.hip_offset() * pool.global_scale.y
	rig.reparent(pool.on_top_root, false)
	rig.slot_index = i
	rig.position = pool.on_top_root.to_local(gp)
	rig.scale = Vector2.ONE * (pool.global_scale.y / maxf(pool.on_top_root.global_scale.y, 0.0001))
	rig.on_placed()
	rig.refresh_pose(false)


static func dive(scene: AreaScene, rig: CharacterRig, tower: ItemNode) -> bool:
	var target: Array = nearest_pool(scene.room, tower.position)
	if target.is_empty():
		return false
	var pool: ItemNode = target[0]
	var i: int = target[1]
	var top := Vector2(tower.position.x - tower.def.width_cm * 0.3, tower.position.y - tower.def.height_cm * 0.93)
	return _fly(scene, rig, [rig.position, top, top + Vector2(-40, -30)], pool, i, JUMP_S, "dive")


static func water_slide(scene: AreaScene, rig: CharacterRig, s: ItemNode) -> bool:
	var target: Array = nearest_pool(scene.room, s.position + Vector2(s.def.width_cm * 0.5, 0))
	if target.is_empty():
		return false
	var left: float = s.position.x - s.def.width_cm * 0.5
	var h: float = s.def.height_cm
	var path: Array = [rig.position, Vector2(left + s.def.width_cm * 0.22, s.position.y - h * 0.86),
		Vector2(left + s.def.width_cm * 0.6, s.position.y - h * 0.6), Vector2(left + s.def.width_cm * 0.5, s.position.y - h * 0.45),
		Vector2(left + s.def.width_cm * 0.62, s.position.y - h * 0.28), Vector2(left + s.def.width_cm, s.position.y - h * 0.1)]
	return _fly(scene, rig, path, target[0], target[1], SLIDE_S, "water_slide")


## Figur entlang der Punkte bewegen, am Ende ins Becken setzen (Platsch). Ohne Animation sofort.
static func _fly(scene: AreaScene, rig: CharacterRig, path: Array, pool: ItemNode, i: int, secs: float, ev: String) -> bool:
	rig.set_emotion("laugh")
	AudioBus.play_sfx("grow")
	Secrets.event(ev)
	var land := func() -> void:
		rig.z_index = 0
		seat_in(rig, pool, i)
		splash(scene.room, rig)
	if not rig.is_inside_tree() or Settings.reduced_motion:
		land.call()
		return true
	var end: Vector2 = scene.room.ysort_root.to_local(Seats.point_global(pool, i))
	var pts: Array = path.duplicate()
	pts.append(end)
	rig.z_index = 2
	var tw: Tween = rig.create_tween()
	tw.tween_method(func(k: float) -> void:
		var f: float = k * (pts.size() - 1)
		var a: int = mini(int(f), pts.size() - 2)
		rig.position = (pts[a] as Vector2).lerp(pts[a + 1], f - a), 0.0, 1.0, secs)
	tw.tween_callback(land)
	return true


## Platsch: Ton, Spritzer am Becken, die Figur ist danach eine Weile nass (tropft).
static func splash(room: Room, rig: CharacterRig) -> void:
	AudioBus.play_sfx("water_pour")
	rig.set_emotion("laugh")
	rig.set_meta("wet_until", Time.get_ticks_msec() / 1000.0 + WET_S)
	Secrets.event("swim")
	var pool: ItemNode = water_of(rig)
	if pool != null:
		_spray(pool)
	if not rig.is_inside_tree():
		return
	var old: Node = rig.get_node_or_null("Drips")
	if old != null:
		old.queue_free()
	var d := CPUParticles2D.new()
	d.name = "Drips"
	d.amount = 10
	d.lifetime = 0.9
	d.position = Vector2(0, -rig.def.height_cm * 0.6)
	d.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	d.emission_rect_extents = Vector2(rig.def.width_cm * 0.35, rig.def.height_cm * 0.3)
	d.gravity = Vector2(0, 260)
	d.scale_amount_min = 1.5
	d.scale_amount_max = 2.5
	d.color = Color("#7cc6e0")
	rig.add_child(d)
	var tw: Tween = d.create_tween()
	tw.tween_interval(WET_S)
	tw.tween_callback(func() -> void: d.emitting = false)          # getrocknet
	tw.tween_interval(1.0)
	tw.tween_callback(d.queue_free)


static func _spray(pool: ItemNode) -> void:
	if not pool.is_inside_tree():
		return
	var p := CPUParticles2D.new()
	p.amount = 24
	p.one_shot = true
	p.explosiveness = 0.9
	p.lifetime = 0.8
	p.position = Vector2(0, -pool.def.height_cm * 0.8)
	p.direction = Vector2.UP
	p.spread = 50.0
	p.initial_velocity_min = 120.0
	p.initial_velocity_max = 220.0
	p.gravity = Vector2(0, 400)
	p.scale_amount_min = 2.0
	p.scale_amount_max = 4.0
	p.color = Color("#bfe6f3")
	pool.add_child(p)
	p.emitting = true
	p.finished.connect(p.queue_free)
