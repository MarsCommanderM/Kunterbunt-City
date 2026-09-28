class_name PlayMotion
extends RefCounted
## P09-T06: Spielgeräte bewegen sich, sobald jemand darauf sitzt: Schaukel schwingt, Karussell (an) dreht,
## Federwippe wippt. Bewegt wird nur `on_top_root` (die Sitzenden und was darauf liegt) – das Gerät selbst bleibt stehen.
## Liste der Geräte wird beim Raumwechsel/nach Änderungen neu gesammelt → kein Suchen in jedem Frame.
## P10d Rummelplatz: Riesenrad (Gondel fährt im Kreis), Karussell, und Fahrzeuge (Autoscooter, Achterbahn-Wagen,
## Geisterbahn-Wagen) – bei Fahrzeugen fährt das Bild mit (`sprite`), die gespeicherte Position bleibt gleich.

const KINDS: Dictionary = {"play_swing": "swing", "play_roundabout": "spin", "play_spring_rider": "rock",
	"garden_swing": "swing", "fair_ferris_wheel": "wheel", "fair_carousel": "carousel", "fair_bumper_car": "drive",
	"fair_coaster_car": "coaster", "fair_ghost_car": "ghost"}
const VEHICLES: Array = ["drive", "coaster", "ghost"]
const COASTER_W: float = 930.0               ## Fahrweg = Schienen-Breite 1100 − Wagen 170 (tools/items/catalog_fair.py)
const COASTER_H: float = 340.0
const WHEEL_R: float = 256.0                 ## Riesenrad-Radius 0,4 × 640 cm (tools/items/funfair.py)
const GHOST_CM: float = 420.0

static var _items: Array = []
static var _t: float = 0.0


static func kind_of(it: ItemNode) -> String:
	var id: String = String(it.def.id)
	for p: String in KINDS:
		if id.begins_with(p):
			return String(KINDS[p])
	return ""


static func refresh(room: Room) -> void:
	_items.clear()
	if room == null:
		return
	for it: ItemNode in Placement.all_items(room):
		if it.def.has_seat() and kind_of(it) != "":
			_items.append(it)


static func occupied(it: ItemNode) -> bool:
	for i: int in it.def.seat_slots:
		if Seats.occupant(it, i) != null:
			return true
	return false


## Einen Schritt bewegen. Gibt die Zahl der Geräte in Bewegung zurück.
static func tick(dt: float) -> int:
	_t += dt
	var n: int = 0
	for it: ItemNode in _items:
		if not is_instance_valid(it) or it.on_top_root == null:
			continue
		var r: Node2D = it.on_top_root
		var kind: String = kind_of(it)
		if not occupied(it) or it.lifted > 0.0:
			r.position = Vector2.ZERO
			r.rotation = 0.0
			if VEHICLES.has(kind):
				_move_sprite(it, Vector2.ZERO, 0.0)
			continue
		if VEHICLES.has(kind):
			var o: Array = vehicle_offset(kind, _t + it.uid * 0.7)
			r.position = o[0]
			r.rotation = o[1]
			_move_sprite(it, o[0], o[1])
			n += 1
			continue
		match kind:
			"swing":
				var a: float = sin(_t * 2.6) * 0.32
				r.rotation = a
				r.position = Vector2(sin(_t * 2.6) * 18.0, -absf(sin(_t * 2.6)) * 6.0)
			"spin":
				if it.state != "on":
					r.position = Vector2.ZERO
					continue
				r.position = Vector2(sin(_t * 3.0) * it.def.width_cm * 0.25, cos(_t * 3.0) * 4.0)
			"rock":
				r.rotation = sin(_t * 5.0) * 0.12
			"wheel":
				var a: float = _t * 0.45
				r.position = Vector2(sin(a) * WHEEL_R, -(1.0 - cos(a)) * WHEEL_R)
			"carousel":
				r.position = Vector2(sin(_t * 1.1) * it.def.width_cm * 0.3, sin(_t * 4.0) * 10.0 - 10.0)
		n += 1
	return n


## Fahrzeug-Versatz zur Zeit t: [Position (cm, y nach oben negativ), Drehung].
static func vehicle_offset(kind: String, t: float) -> Array:
	match kind:
		"drive":
			return [Vector2(sin(t * 1.3) * 150.0 + sin(t * 3.1) * 20.0, 0.0), cos(t * 1.3) * 0.08]
		"coaster":
			var u: float = pingpong(t * 0.12, 1.0)
			var y: float = coaster_y(u) - coaster_y(0.0)
			var y2: float = coaster_y(minf(u + 0.01, 1.0)) - coaster_y(0.0)
			return [Vector2(u * COASTER_W, -y), -atan2(y2 - y, COASTER_W * 0.01)]
		"ghost":
			return [Vector2(pingpong(t * 0.18, 1.0) * GHOST_CM, 0.0), 0.0]
	return [Vector2.ZERO, 0.0]


## Gleiche Formel wie tools/items/funfair.py › coaster_y (Schiene und Fahrt passen zusammen).
static func coaster_y(u: float) -> float:
	return 30.0 + (COASTER_H - 60.0) * (0.75 * pow(sin(PI * u), 2.0) + 0.25 * absf(sin(3.0 * PI * u)))


static func _move_sprite(it: ItemNode, off: Vector2, rot: float) -> void:
	if it.sprite == null:
		return
	if not it.has_meta("sprite_base"):
		it.set_meta("sprite_base", it.sprite.position)
	it.sprite.position = Vector2(it.get_meta("sprite_base")) + off
	it.sprite.rotation = rot
