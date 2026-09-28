class_name NpcRoles
extends RefCounted
## P08-T02: Rollen-Vorlagen (data/npc_roles/*.json) und konkrete NPCs (data/npcs/<bereich>.json).
## Rolle = WAS eine Figur tut (Verhalten, Arbeits-Animationen, Aussehen), NPC = WER WO steht (Raum, x/y in cm, Name).
## Fehler in den Daten werden beim Laden klar gemeldet (Rolle fehlt, Verhalten unbekannt).

const ROLES_DIR: String = "res://data/npc_roles/"
const NPCS_DIR: String = "res://data/npcs/"
const BEHAVIORS: Array = ["station", "patrol", "wander", "deliver"]
const DEFAULTS: Dictionary = {"template": "adult", "speed_cm_s": 70.0, "return_after_s": 8.0, "work_every_s": [3.0, 7.0],
	"behavior": "station", "work": ["look"], "patrol_cm": 150.0, "light": false}

static var _roles: Dictionary = {}


static func all() -> Dictionary:
	if _roles.is_empty():
		for f: String in DirAccess.get_files_at(ROLES_DIR):
			if not f.ends_with(".json"):
				continue
			var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(ROLES_DIR + f))
			if not (d is Dictionary) or not (d as Dictionary).has("id"):
				push_error("NpcRoles: %s ist keine gültige Rolle" % f)
				continue
			var r: Dictionary = DEFAULTS.duplicate(true)
			r.merge(d as Dictionary, true)
			if not BEHAVIORS.has(String(r["behavior"])):
				push_error("NpcRoles: %s – unbekanntes Verhalten '%s'" % [f, r["behavior"]])
				r["behavior"] = "station"
			_roles[String(r["id"])] = r
	return _roles


static func has_role(id: String) -> bool:
	return all().has(id)


static func role(id: String) -> Dictionary:
	return all().get(id, {})


## Alle NPCs eines Bereichs (leer, wenn es keine Datei gibt).
static func npcs_of(area_id: String) -> Array:
	var path: String = NPCS_DIR + area_id + ".json"
	if not FileAccess.file_exists(path):
		return []
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not (d is Dictionary):
		push_error("NpcRoles: %s ist kaputt" % path)
		return []
	var out: Array = []
	for e: Variant in Array((d as Dictionary).get("npcs", [])):
		var n: Dictionary = e
		if not has_role(String(n.get("role", ""))):
			push_error("NpcRoles: NPC '%s' hat die unbekannte Rolle '%s'" % [n.get("id", "?"), n.get("role", "")])
			continue
		out.append(n)
	return out


static func npcs_in_room(area_id: String, room_id: String) -> Array:
	return npcs_of(area_id).filter(func(n: Dictionary) -> bool: return String(n.get("room", "")) == room_id)
