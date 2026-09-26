class_name PetSpecies
extends RefCounted
## Katalog der Haustier-Arten (P04-T09): data/pets/species.json.
## Die GRÖSSE kommt nie von hier – immer aus der Maßstab-Tabelle über das Item (ItemDB).

const FILE: String = "res://data/pets/species.json"

static var _data: Dictionary = {}


static func data() -> Dictionary:
	if _data.is_empty():
		var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(FILE))
		_data = d if d is Dictionary else {}
	return _data


static func species() -> Array:
	return data().get("species", [])


static func ids() -> Array:
	var out: Array = []
	for s: Variant in species():
		out.append(String((s as Dictionary)["id"]))
	return out


static func entry(sid: String) -> Dictionary:
	for s: Variant in species():
		if String((s as Dictionary)["id"]) == sid:
			return s
	return {}


static func label(sid: String) -> String:
	return String(entry(sid).get("label", sid))


static func icon(sid: String) -> String:
	return String(entry(sid).get("icon", "paw"))


static func voice(sid: String) -> String:
	return String(entry(sid).get("voice", "pet_dog_bark"))


static func traits(sid: String = "") -> Array:
	var all: Array = data().get("traits", [])
	var e: Dictionary = entry(sid)
	if e.is_empty():
		return all
	var allowed: Array = e.get("traits", [])
	var out: Array = []
	for t: Variant in all:
		if allowed.has(String((t as Dictionary)["id"])):
			out.append(t)
	return out


static func trait_ids(sid: String = "") -> Array:
	var out: Array = []
	for t: Variant in traits(sid):
		out.append(String((t as Dictionary)["id"]))
	return out


static func trait_icon(tid: String) -> String:
	for t: Variant in data().get("traits", []):
		if String((t as Dictionary)["id"]) == tid:
			return String((t as Dictionary)["icon"])
	return "paw"


static func trait_label(tid: String) -> String:
	for t: Variant in data().get("traits", []):
		if String((t as Dictionary)["id"]) == tid:
			return String((t as Dictionary)["label"])
	return tid


## Wie nah folgt das Tier der Figur? (Phase 08 nutzt das für die KI.)
static func trait_follow(tid: String) -> float:
	for t: Variant in data().get("traits", []):
		if String((t as Dictionary)["id"]) == tid:
			return float((t as Dictionary).get("follow_dist_cm", 80.0))
	return 80.0


static func patterns() -> Array:
	return data().get("patterns", [])


static func pattern_ids() -> Array:
	var out: Array = []
	for p: Variant in patterns():
		out.append(String((p as Dictionary)["id"]))
	return out


static func collars() -> Array:
	return data().get("collars", [])


static func collar_color(cid: String) -> String:
	for c: Variant in collars():
		if String((c as Dictionary)["id"]) == cid:
			return String((c as Dictionary)["color"])
	return "#ffffff"


## Standard-Fellfarben einer Art (aus dem Sprite-Index, Fallback: Palette).
static func default_fur(sid: String) -> Array:
	var p: String = "res://assets/sprites/pets/index.json"
	if FileAccess.file_exists(p):
		var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(p))
		if d is Dictionary and (d as Dictionary).has(sid):
			return (d as Dictionary)[sid]["colors"]
	var furs: Array = CharacterParts.palette_colors("fur")
	return [furs[1], furs[0], "#e2574c"] if furs.size() > 1 else ["#d9a066", "#f7e6c8", "#e2574c"]
