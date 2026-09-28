class_name PetNode
extends ItemNode
## Haustier (P03-T08): läuft selbstständig im Bodenband – Pause (2–5 s) → Spaziergang → folgt der nächsten
## Figur und bleibt ~50 cm neben ihr stehen. Tippen = Tierlaut (globaler Limiter 1×/8 s im AudioBus).
## Getragen, in der Hand oder auf dem Sofa: macht nichts. Zufall pro Tier fest (Seed = uid) → reproduzierbar.
## P08-T07: PetBrain (Bedürfnisse) wählt statt Schlendern ein Ziel: Napf, Spielzeug, Körbchen (Modus SEEK),
## am Körbchen schläft das Tier (SLEEP). P08-T08: von selbst alle 15–60 s ein Laut (Varianten, globaler Limiter).

enum Mode { IDLE, WALK, FOLLOW, SEEK, SLEEP }

const SPEED_CM_S: float = 60.0
const FOLLOW_START_CM: float = 110.0
const FOLLOW_STOP_CM: float = 50.0
const WANDER_CM: float = 120.0
const MIN_FRIEND_CM: float = 40.0      # beim Schlendern nie näher als 40 cm an die Figur

## Global aus in Tests/Beweis-Runnern (sonst laufen Tiere zwischen zwei Screenshots weiter).
static var autonomous: bool = true

var mode: int = Mode.IDLE
var auto_walk: bool = true           ## Tests schalten die Eigenbewegung ab und rufen tick() selbst
var target: Vector2
var _timer: float = 1.0
var _walk_t: float = 0.0
var _rng := RandomNumberGenerator.new()
var brain: PetBrain
var goal: Dictionary = {}            ## {need, item} während SEEK


static func create_pet(definition: ItemDefinition) -> PetNode:
	var p := PetNode.new()
	p.setup(definition)
	p._rng.seed = 7919 * p.uid + 17
	p._timer = p._rng.randf_range(0.5, 2.0)
	var brng := RandomNumberGenerator.new()          # eigener Zufall: das Schlendern bleibt wie vor P08
	brng.seed = 104729 * p.uid + 3
	p.brain = PetBrain.new(brng)
	return p


## Charakterzug aus dem Tier-Editor (verspielt, verschlafen …) → Gewichte der Bedürfnisse.
func set_trait(trait_id: String) -> void:
	brain.pet_trait = trait_id


func _ready() -> void:
	set_process(autonomous)          ## Tests/Screenshots: Tiere laufen nur per tick()


func voice() -> String:
	return String(def.sfx.get("voice", "pet_dog_bark"))


func on_tap() -> void:
	brain.petted()                                   # Streicheln: Zuneigung gestillt, Katze schnurrt
	if mode == Mode.SLEEP:
		mode = Mode.IDLE
		brain.sleep_left = 0.0
	if not AudioBus.play_animal(PetBrain.pet_sound(voice())):
		AudioBus.play_sfx("tap")
	_bounce()
	tapped.emit(self)


func room() -> Room:
	var p: Node = get_parent()
	return p.get_parent() as Room if p and p.name == "YSortRoot" else null


## Läuft nur, wenn es frei auf dem Boden steht.
func can_walk() -> bool:
	return room() != null and lifted <= 0.0 and slot_index < 0


func _process(delta: float) -> void:
	if not autonomous:
		set_process(false)
		return
	if auto_walk and autonomous:
		tick(delta)


func tick(dt: float) -> void:
	var r: Room = room()
	if r == null or not can_walk():
		_set_bob(0.0)
		if mode == Mode.SLEEP or mode == Mode.SEEK:
			mode = Mode.IDLE
		return
	if def.tags.has("wild"):
		_wild_tick(r, dt)                            # P09-T07: Enten, Tauben, Eichhörnchen
		return
	brain.tick(dt)
	if brain.voice_due(dt):
		AudioBus.play_animal(brain.voice_variant(voice()))
	if mode == Mode.SLEEP:
		if brain.sleep_left <= 0.0:
			mode = Mode.IDLE
			sprite.rotation = 0.0
		return
	if mode == Mode.SEEK and _seek(r, dt):
		return
	var friend: ItemNode = _nearest_character(r)
	if friend and friend.position.distance_to(position) > FOLLOW_START_CM:
		mode = Mode.FOLLOW
	if mode == Mode.FOLLOW:
		if friend == null:
			mode = Mode.IDLE
		else:
			var side: float = signf(position.x - friend.position.x) if position.x != friend.position.x else 1.0
			target = r.floor_band.clamp_point(friend.position + Vector2(side * FOLLOW_STOP_CM, 6.0))
	match mode:
		Mode.IDLE:
			_set_bob(0.0)
			_timer -= dt
			if _timer <= 0.0 and _start_seek(r):
				return
			if _timer <= 0.0:
				var base: Vector2 = friend.position if friend else position
				var wander: Vector2 = base + Vector2(_rng.randf_range(-WANDER_CM, WANDER_CM),
					_rng.randf_range(-25.0, 25.0))
				# Nie IN die Figur hinein laufen: beim Schlendern mindestens MIN_FRIEND_CM Abstand.
				if friend != null:
					var off: Vector2 = wander - friend.position
					if off.length() < MIN_FRIEND_CM:
						var dir: Vector2 = off.normalized() if off.length_squared() > 0.01 \
							else Vector2(signf(position.x - friend.position.x), 1.0).normalized()
						wander = friend.position + dir * MIN_FRIEND_CM
				target = r.floor_band.clamp_point(wander)
				mode = Mode.WALK
		_:
			var to: Vector2 = target - position
			var step: float = SPEED_CM_S * dt
			if to.length() <= maxf(step, 2.0):
				position = target
				mode = Mode.IDLE
				_timer = _rng.randf_range(2.0, 5.0)
			else:
				var dir: Vector2 = to.normalized()
				# Persönlicher Abstand: kommt die Figur auf dem Weg zu nah, weicht der Hund im
				# Bogen aus – er läuft NIE durch sie hindurch.
				if friend != null:
					var away: Vector2 = position - friend.position
					var ad: float = away.length()
					if ad < MIN_FRIEND_CM:
						var push: Vector2 = (away / maxf(ad, 0.001)) if ad > 0.001 \
							else Vector2(1.0, 0.0)
						dir = (dir + push * 2.0 * clampf(
							(MIN_FRIEND_CM - ad) / MIN_FRIEND_CM, 0.0, 1.0)).normalized()
				position = r.floor_band.clamp_point(position + dir * step)
				# Harte Grenze (zusätzlich zum Ausweichen): nie näher als MIN_FRIEND_CM – und dabei nie aus dem
				# Bodenband geschoben (vorher landete der Hund je nach Zufall vor der vorderen Bodenlinie).
				if friend != null:
					var gap: Vector2 = position - friend.position
					var gd: float = gap.length()
					if gd < MIN_FRIEND_CM:
						var out: Vector2 = (gap / maxf(gd, 0.001)) if gd > 0.001 \
							else Vector2(1.0, 0.0)
						var p2: Vector2 = friend.position + out * MIN_FRIEND_CM
						if not r.floor_band.contains(p2):
							out = Vector2(signf(gap.x) if absf(gap.x) > 0.001 else 1.0, 0.0)
							p2 = friend.position + out * MIN_FRIEND_CM
						position = r.floor_band.clamp_point(p2)
				if absf(to.x) > 1.0:
					sprite.flip_h = to.x > 0.0
				_walk_t += dt
				_set_bob(absf(sin(_walk_t * 11.0)) * 1.6)
			scale = Vector2.ONE * r.floor_band.depth_factor(position.y)


## P09-T07: Wildtier – bleibt in seinem Revier (Ente: auf dem Teich, auf dem es steht), schlendert, meldet sich
## ab und zu und flüchtet vor Figuren (schneller, weg von ihnen). Folgt nie jemandem.
const FLEE_CM: float = 80.0
var _home: Rect2 = Rect2()


func home_area(r: Room) -> Rect2:
	if _home.size != Vector2.ZERO:
		return _home
	_home = Rect2(position.x - 160.0, r.floor_band.back_y_cm, 320.0, r.floor_band.front_y_cm - r.floor_band.back_y_cm)
	for o: ItemNode in Placement.all_items(r):
		if String(o.def.id).begins_with("garden_pond") and absf(o.position.x - position.x) < o.def.width_cm * 0.5:
			_home = Rect2(o.position.x - o.def.width_cm * 0.38, o.position.y - 12.0, o.def.width_cm * 0.76, 20.0)
	return _home


func _wild_tick(r: Room, dt: float) -> void:
	var home: Rect2 = home_area(r)
	var fear: ItemNode = null
	for c: Node in r.ysort_root.get_children():
		if c is CharacterRig and not c.has_meta("npc_id") and (c as Node2D).position.distance_to(position) < FLEE_CM:
			fear = c
	var speed: float = SPEED_CM_S
	if fear != null:
		var away: float = signf(position.x - fear.position.x) if position.x != fear.position.x else 1.0
		target = Vector2(position.x + away * 150.0, position.y)
		mode = Mode.WALK
		speed *= 2.2
		if brain.voice_due(8.0):
			AudioBus.play_animal(voice())
			Secrets.event("duck_flee")
	elif mode == Mode.IDLE:
		_set_bob(0.0)
		_timer -= dt
		if brain.voice_due(dt):
			AudioBus.play_animal(voice())
		if _timer > 0.0:
			return
		target = home.position + Vector2(_rng.randf() * home.size.x, _rng.randf() * home.size.y)
		mode = Mode.WALK
	target = Vector2(clampf(target.x, home.position.x, home.end.x), clampf(target.y, home.position.y, home.end.y))
	target = r.floor_band.clamp_point(target)
	var to: Vector2 = target - position
	if to.length() <= maxf(speed * dt, 2.0):
		position = target
		mode = Mode.IDLE
		_timer = _rng.randf_range(1.5, 4.0)
		_set_bob(0.0)
		return
	position = r.floor_band.clamp_point(position + to.normalized() * speed * dt)
	if absf(to.x) > 1.0:
		sprite.flip_h = to.x < 0.0                    # Wildtiere schauen im Bild nach rechts
	_walk_t += dt
	_set_bob(absf(sin(_walk_t * 9.0)) * 1.0)
	scale = Vector2.ONE * r.floor_band.depth_factor(position.y)


## Bedürfnis mit passendem Ding im Raum? → hinlaufen (SEEK).
func _start_seek(r: Room) -> bool:
	var g: Dictionary = brain.choose(Placement.all_items(r))
	if g.is_empty():
		return false
	goal = g
	mode = Mode.SEEK
	return true


## Zum Ziel laufen; angekommen → fressen / anstupsen / schlafen. true = SEEK hat den Schritt übernommen.
func _seek(r: Room, dt: float) -> bool:
	var it: ItemNode = goal.get("item")
	if not is_instance_valid(it) or it.get_parent() == null or it.get_parent().name != "YSortRoot":
		mode = Mode.IDLE
		_timer = 1.0
		return true
	var side: float = -1.0 if it.position.x > position.x else 1.0
	var spot: Vector2 = it.position if goal["need"] == "tired" else it.position + Vector2(side * (it.def.width_cm * 0.5 + 12.0), 2.0)
	target = r.floor_band.clamp_point(spot)
	var to: Vector2 = target - position
	var step: float = SPEED_CM_S * dt
	if to.length() > maxf(step, 2.0):
		position = r.floor_band.clamp_point(position + to.normalized() * step)
		if absf(to.x) > 1.0:
			sprite.flip_h = to.x > 0.0
		_walk_t += dt
		_set_bob(absf(sin(_walk_t * 11.0)) * 1.6)
		scale = Vector2.ONE * r.floor_band.depth_factor(position.y)
		return true
	position = target
	_set_bob(0.0)
	var need: String = String(goal["need"])
	var snd: String = brain.satisfy(need, it, position)
	it.position = r.floor_band.clamp_point(it.position)
	it.position.x = clampf(it.position.x, 20.0, r.width_cm - 20.0)
	if snd != "":
		AudioBus.play_sfx(snd)
	goal = {}
	if need == "tired":
		mode = Mode.SLEEP
		position.y = it.position.y + 1.0             # vor dem Körbchen-Rand einsortiert
	else:
		mode = Mode.IDLE
		_timer = _rng.randf_range(2.0, 5.0)
	return true


func _set_bob(h: float) -> void:
	var base: Vector2 = -(Vector2.ONE * def.pad_px + def.pivot * (sprite.texture.get_size() - Vector2.ONE * 2.0 * def.pad_px))
	sprite.offset = base - Vector2(0, h / maxf(sprite.scale.y, 0.0001))


func _nearest_character(r: Room) -> ItemNode:
	var best: ItemNode = null
	var best_d: float = INF
	for c: Node in r.ysort_root.get_children():
		if c is ItemNode and (c as ItemNode).def.category == "character" and not c.has_meta("npc_id"):
			var d: float = (c as ItemNode).position.distance_to(position)
			if d < best_d:
				best_d = d
				best = c
	return best
