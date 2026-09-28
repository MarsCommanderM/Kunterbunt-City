class_name SportActions
extends RefCounted
## P10e Sportzentrum (AreaActions ruft on_dropped/on_tapped):
##   Ball antippen = schießen: rollt weg von der nächsten eigenen Figur (sonst zur Raummitte), bremst ab, dreht sich
##   Tor-Erkennung: kreuzt der Ball ein Tor (auf gleicher Tiefe), bleibt er im Netz → TOR: Pfiff, Trainer klatscht,
##   alle jubeln, Anzeigetafel zählt einen Ball weiter (Punkte statt Ziffern, R-07). Ball ins Tor legen zählt auch.
##   Kletterwand: Figur an der Wand einhängen → Aufsicht sichert (schaut, Hebel), Geheimnis

const BALLS: Array = ["spc_football", "toy_ball", "spc_tennis_ball"]
const GOALS: Array = ["spc_goal", "sport_goal"]
const KICK_CM: float = 340.0
const KICK_S: float = 0.9
const DEPTH_CM: float = 80.0                  ## so nah (Tiefe) muss der Ball am Tor sein


static func on_dropped(scene: AreaScene, item: ItemNode) -> bool:
	if _is(item, BALLS) and item.get_parent() == scene.room.ysort_root and goal_at(scene.room, item.position.x, item.position.y) != null:
		goal(scene.room)
		return false
	if item is CharacterRig:
		var host: ItemNode = Seats.seat_host_of(item)
		if host != null and String(host.def.id).begins_with("spc_climbing_wall"):
			for b: NpcBrain in NpcSpawner.brains(scene.room):
				if String(b.role.get("id", "")) == "supervisor":
					b.play_work("look")
			(item as CharacterRig).set_emotion("laugh")
			Secrets.event("climb")
	return false


static func on_tapped(scene: AreaScene, item: ItemNode) -> bool:
	if _is(item, BALLS) and item.get_parent() == scene.room.ysort_root:
		kick(scene.room, item)
		return true
	return false


static func _is(item: ItemNode, prefixes: Array) -> bool:
	for p: String in prefixes:
		if String(item.def.id).begins_with(p):
			return true
	return false


## Tor, in dessen Rahmen x liegt (gleiche Tiefe), oder null.
static func goal_at(room: Room, x: float, y: float) -> ItemNode:
	for g: ItemNode in Placement.all_items(room):
		if _is(g, GOALS) and g.get_parent() == room.ysort_root and absf(g.position.y - y) < DEPTH_CM:
			var half: float = g.def.width_cm * 0.5 - 10.0
			if x >= g.position.x - half and x <= g.position.x + half:
				return g
	return null


## Schuss. Gibt true zurück, wenn der Ball im Tor landet.
static func kick(room: Room, ball: ItemNode) -> bool:
	var dir: float = 1.0 if ball.position.x < room.width_cm * 0.5 else -1.0
	var near: float = 200.0
	for it: ItemNode in Placement.all_items(room):
		if it is CharacterRig and not it.has_meta("npc_id") and it.get_parent() == room.ysort_root:
			var d: float = ball.position.x - it.position.x
			if absf(d) < near:
				near = absf(d)
				dir = signf(d) if d != 0.0 else dir
	var dist: float = KICK_CM * (1.6 if String(ball.def.id).begins_with("spc_tennis_ball") else 1.0)
	var end_x: float = clampf(ball.position.x + dir * dist, 30.0, room.width_cm - 30.0)
	var scored: ItemNode = null
	for g: ItemNode in Placement.all_items(room):          # kreuzt der Weg ein Tor? → Ball bleibt im Netz
		if not _is(g, GOALS) or g.get_parent() != room.ysort_root or absf(g.position.y - ball.position.y) >= DEPTH_CM:
			continue
		if (g.position.x - ball.position.x) * dir > 0.0 and absf(g.position.x - ball.position.x) <= dist + g.def.width_cm * 0.3:
			if scored == null or absf(g.position.x - ball.position.x) < absf(scored.position.x - ball.position.x):
				scored = g
	if scored != null:
		end_x = scored.position.x
	AudioBus.play_sfx("drop_soft")
	var end := Vector2(end_x, ball.position.y)
	var done := func() -> void:
		ball.position = end
		ball.rotation = 0.0
		if scored != null:
			goal(room)
		Game.mark_dirty()
	if not ball.is_inside_tree() or Settings.reduced_motion:
		done.call()
	else:
		var tw: Tween = ball.create_tween().set_parallel(true)
		tw.tween_property(ball, "position", end, KICK_S).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(ball, "rotation", dir * TAU * 2.0, KICK_S).set_ease(Tween.EASE_OUT)
		tw.chain().tween_callback(done)
	return scored != null


## TOR! Pfiff, Jubel, Anzeigetafel zählt weiter (nach 5 wieder von vorne).
static func goal(room: Room) -> void:
	AudioBus.play_sfx("whistle")
	Secrets.event("goal")
	for it: ItemNode in Placement.all_items(room):
		if String(it.def.id).begins_with("spc_scoreboard"):
			var n: int = int(it.state.substr(1)) if it.state.begins_with("s") else 0
			ItemStates.set_state(it, "s%d" % ((n + 1) % 6))
		elif it is CharacterRig:
			(it as CharacterRig).set_emotion("laugh")
	for b: NpcBrain in NpcSpawner.brains(room):
		b.play_work("clap" if String(b.role.get("id", "")) == "coach" else "wave")
