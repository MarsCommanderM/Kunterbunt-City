class_name Areas
extends RefCounted
## Bereichs-Katalog (P05-T02): data/areas/index.json.
## `ready` = der Bereich hat Inhalt. Nicht fertige Bereiche sind SICHTBAR (Baustelle), nie gesperrt.

const FILE: String = "res://data/areas/index.json"

static var _data: Dictionary = {}


static func data() -> Dictionary:
	if _data.is_empty():
		var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(FILE))
		_data = d if d is Dictionary else {}
	return _data


static func list() -> Array:
	return data().get("areas", [])


static func ids() -> Array:
	var out: Array = []
	for a: Variant in list():
		out.append(String((a as Dictionary)["id"]))
	return out


static func get_area(id: StringName) -> Dictionary:
	for a: Variant in list():
		if String((a as Dictionary)["id"]) == String(id):
			return a
	return {}


static func label(id: StringName) -> String:
	return String(get_area(id).get("label", String(id)))


static func icon(id: StringName) -> String:
	return String(get_area(id).get("icon", "map"))


static func color(id: StringName) -> Color:
	return Color(String(get_area(id).get("color", "#f2a65a")))


static func sound(id: StringName) -> String:
	return String(get_area(id).get("sound", "ui_confirm"))


## Hat der Bereich Inhalt? (Fehlende oder unlesbare Datei → Baustelle.)
static func is_ready(id: StringName) -> bool:
	var a: Dictionary = get_area(id)
	if a.is_empty() or not bool(a.get("ready", false)):
		return false
	var p: String = String(a.get("path", ""))
	return not p.is_empty() and FileAccess.file_exists(p)


## Erster spielbarer Bereich (Start-Ziel der Stadtkarte).
static func first_ready() -> StringName:
	for a: Variant in list():
		if is_ready(StringName(String((a as Dictionary)["id"]))):
			return StringName(String((a as Dictionary)["id"]))
	return &""


## Spawn-Punkt eines Bereichs (cm, y = Tiefe im Bodenband).
static func spawn_of(id: StringName) -> Vector2:
	var a: Dictionary = get_area(id)
	return Vector2(float(a.get("spawn_x_cm", 400.0)), float(a.get("spawn_y_cm", 40.0)))


static func room_of(id: StringName) -> String:
	return String(get_area(id).get("room", ""))


static func path_of(id: StringName) -> String:
	return String(get_area(id).get("path", ""))


## P09: Ein Knopf kann in einen anderen Bereich führen (Blumenladen → Einkaufsstraße, Raum „florist").
## Spielstand und Räume gehören dann dem Ziel-Bereich – nichts wird doppelt gespeichert.
static func canonical(id: StringName) -> StringName:
	var s: String = String(get_area(id).get("same_as", ""))
	return StringName(s) if not s.is_empty() else id
