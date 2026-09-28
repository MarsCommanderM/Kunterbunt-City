class_name FairActions
extends RefCounted
## P10d Rummelplatz (AreaActions ruft on_dropped/on_tapped):
##   Fahrgeschäft : Figur hineinsetzen → Klingel, Fahrt startet (Bewegung: PlayMotion), Bediener/in winkt
##   Dosenwerfen  : Dosen antippen → fallen um → Plüsch-Gewinn liegt davor (✋, kann in den Rucksack)
##   Losrad       : drehen → ein Luftballon als Gewinn
##   Hau den Lukas: Glocke oben → alle klatschen · Zauberhut: Hase · Geisterbahn: Gespenst sagt „Huuu“ (lustig)

const PRIZES: Array = ["fair_prize_rose", "fair_prize_sky", "fair_prize_butter", "fair_prize_mint", "fair_prize_lilac"]
const BALLOONS: Array = ["fair_balloon_coral", "fair_balloon_sky", "fair_balloon_butter", "fair_balloon_mint"]

static var _prize_i: int = 0


static func on_dropped(scene: AreaScene, item: ItemNode) -> bool:
	if not (item is CharacterRig):
		return false
	var host: ItemNode = Seats.seat_host_of(item)
	if host == null or not String(host.def.id).begins_with("fair_") or PlayMotion.kind_of(host) == "":
		return false
	AudioBus.play_sfx("fair_bell")
	(item as CharacterRig).set_emotion("laugh")
	Secrets.event("ride")
	if String(host.def.id).begins_with("fair_ferris_wheel"):
		Secrets.event("ferris")
	PlayMotion.refresh(scene.room)
	_crowd(scene.room, "wave", "")
	return false                              # Sitzen erledigt der normale Drop


static func on_tapped(scene: AreaScene, item: ItemNode) -> bool:
	var id: String = String(item.def.id)
	if id.begins_with("fair_cans") and item.state == "fallen":
		prize(scene.room, item, PRIZES[_prize_i % PRIZES.size()])
		_prize_i += 1
		Secrets.event("prize")
		return true
	if id.begins_with("fair_lottery") and item.state == "spin":
		prize(scene.room, item, BALLOONS[_prize_i % BALLOONS.size()])
		_prize_i += 1
		return true
	if id.begins_with("fair_high_striker") and item.state == "ring":
		_crowd(scene.room, "clap", "laugh")
		Secrets.event("strong")
		return true
	if id.begins_with("fair_magic_hat") and item.state == "rabbit":
		_crowd(scene.room, "clap", "surprised")
		Secrets.event("magic")
		return true
	if id.begins_with("fair_ghost_house") and item.state == "boo":
		_crowd(scene.room, "", "laugh")
		return true
	return false


## Gewinn fällt vor die Bude (auf den Boden, frei beweglich).
static func prize(room: Room, at: ItemNode, id: String) -> ItemNode:
	var p: Vector2 = room.ysort_root.to_local(at.global_position)
	var y: float = clampf(p.y + 25.0, room.floor_band.back_y_cm, room.floor_band.front_y_cm)
	var out: ItemNode = ItemSpawner.on_floor(room, StringName(id), p.x + 30.0, y)
	AudioBus.play_sfx("tada")
	return out


## Figuren im Raum reagieren (NPC-Animation und/oder Gesicht).
static func _crowd(room: Room, anim: String, face: String) -> void:
	for b: NpcBrain in NpcSpawner.brains(room):
		if anim != "":
			b.play_work(anim)
		if face != "":
			b.body.set_emotion(face)
	if face != "":
		for it: ItemNode in Placement.all_items(room):
			if it is CharacterRig and not it.has_meta("npc_id"):
				(it as CharacterRig).set_emotion(face)
