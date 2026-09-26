class_name PetNode
extends ItemNode
## Haustier (P03-T08): läuft selbstständig im Bodenband – Pause (2–5 s) → Spaziergang → folgt der nächsten
## Figur und bleibt ~50 cm neben ihr stehen. Tippen = Tierlaut (globaler Limiter 1×/8 s im AudioBus).
## Getragen, in der Hand oder auf dem Sofa: macht nichts. Zufall pro Tier fest (Seed = uid) → reproduzierbar.

enum Mode { IDLE, WALK, FOLLOW }

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


static func create_pet(definition: ItemDefinition) -> PetNode:
	var p := PetNode.new()
	p.setup(definition)
	p._rng.seed = 7919 * p.uid + 17
	p._timer = p._rng.randf_range(0.5, 2.0)
	return p


func _ready() -> void:
	set_process(autonomous)          ## Tests/Screenshots: Tiere laufen nur per tick()


func voice() -> String:
	return String(def.sfx.get("voice", "pet_dog_bark"))


func on_tap() -> void:
	if not AudioBus.play_animal(voice()):
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
				position += dir * step
				# Harte Grenze (zusätzlich zum Ausweichen): nie näher als MIN_FRIEND_CM.
				if friend != null:
					var gap: Vector2 = position - friend.position
					var gd: float = gap.length()
					if gd < MIN_FRIEND_CM:
						var out: Vector2 = (gap / maxf(gd, 0.001)) if gd > 0.001 \
							else Vector2(1.0, 0.0)
						position = friend.position + out * MIN_FRIEND_CM
				if absf(to.x) > 1.0:
					sprite.flip_h = to.x > 0.0
				_walk_t += dt
				_set_bob(absf(sin(_walk_t * 11.0)) * 1.6)
			scale = Vector2.ONE * r.floor_band.depth_factor(position.y)


func _set_bob(h: float) -> void:
	var base: Vector2 = -(Vector2.ONE * def.pad_px + def.pivot * (sprite.texture.get_size() - Vector2.ONE * 2.0 * def.pad_px))
	sprite.offset = base - Vector2(0, h / maxf(sprite.scale.y, 0.0001))


func _nearest_character(r: Room) -> ItemNode:
	var best: ItemNode = null
	var best_d: float = INF
	for c: Node in r.ysort_root.get_children():
		if c is ItemNode and (c as ItemNode).def.category == "character":
			var d: float = (c as ItemNode).position.distance_to(position)
			if d < best_d:
				best_d = d
				best = c
	return best
