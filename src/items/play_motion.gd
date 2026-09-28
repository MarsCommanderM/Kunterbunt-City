class_name PlayMotion
extends RefCounted
## P09-T06: Spielgeräte bewegen sich, sobald jemand darauf sitzt: Schaukel schwingt, Karussell (an) dreht,
## Federwippe wippt. Bewegt wird nur `on_top_root` (die Sitzenden und was darauf liegt) – das Gerät selbst bleibt stehen.
## Liste der Geräte wird beim Raumwechsel/nach Änderungen neu gesammelt → kein Suchen in jedem Frame.

const KINDS: Dictionary = {"play_swing": "swing", "play_roundabout": "spin", "play_spring_rider": "rock",
	"garden_swing": "swing"}

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
		if not occupied(it) or it.lifted > 0.0:
			r.position = Vector2.ZERO
			r.rotation = 0.0
			continue
		match kind_of(it):
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
		n += 1
	return n
