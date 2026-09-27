class_name Secrets
extends RefCounted
## P07-T10: Geheimnisse (data/secrets/<bereich>.json) → Sticker im Album. Ohne Text, ohne Druck: man findet sie
## beim Spielen (Truhe öffnen, Licht aus, ernten, kochen …). Gefundene IDs liegen in Game.secrets (Speicherstand v4).
##   when "state": ein Item mit Präfix `item` hat den Zustand `state` (optional nur, wenn der Raum dunkel ist)
##   when "dark":  der Raum ist dunkel (Licht-Schalter aus)
##   when "event": etwas ist passiert – Secrets.event("harvest"/"cook") aus Garten/Rezepten

const DIR: String = "res://data/secrets/"
static var _all: Array = []


static func all() -> Array:
	if _all.is_empty():
		for f: String in DirAccess.get_files_at(DIR):
			if f.ends_with(".json"):
				var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(DIR + f))
				if d is Dictionary:
					for s: Variant in Array((d as Dictionary).get("secrets", [])):
						var e: Dictionary = s
						e["area"] = String((d as Dictionary).get("area", ""))
						_all.append(e)
	return _all


static func for_area(area_id: String) -> Array:
	return all().filter(func(s: Dictionary) -> bool: return String(s["area"]) == area_id)


## Zustände im Raum prüfen (nach jeder Änderung). Gibt neu gefundene IDs zurück.
static func check(area_id: String, room: Room) -> Array:
	var out: Array = []
	if room == null:
		return out
	var dark: bool = RoomLight.is_dark(room)
	var items: Array = Placement.all_items(room)
	for s: Dictionary in for_area(area_id):
		if Game.has_secret(String(s["id"])) or not _room_ok(s, String(room.room_id)):
			continue
		var hit: bool = false
		match String(s.get("when", "")):
			"dark":
				hit = dark
			"state":
				if not bool(s.get("dark", false)) or dark:
					for it: ItemNode in items:
						if String(it.def.id).begins_with(String(s["item"])) and it.state == String(s["state"]):
							hit = true
		if hit:
			Game.add_secret(String(s["id"]))
			out.append(String(s["id"]))
	return out


## Ereignis (Ernte, Kochen) im aktuellen Raum.
static func event(kind: String) -> Array:
	var out: Array = []
	for s: Dictionary in all():
		if String(s.get("when", "")) != "event" or String(s.get("event", "")) != kind:
			continue
		if String(s["area"]) != String(Game.current_area) or Game.has_secret(String(s["id"])):
			continue
		if not _room_ok(s, String(Game.current_room)):
			continue
		Game.add_secret(String(s["id"]))
		out.append(String(s["id"]))
	return out


static func by_id(id: String) -> Dictionary:
	for s: Dictionary in all():
		if String(s["id"]) == id:
			return s
	return {}


## Sticker-Bild: genaue Item-ID oder das erste Item mit diesem Präfix.
static func sticker_def(s: Dictionary) -> ItemDefinition:
	var id := StringName(String(s.get("sticker", "")))
	var d: ItemDefinition = ItemDB.get_item(id) if ItemDB.has_item(id) else null
	if d != null:
		return d
	for gid: String in Catalog.group_ids():
		for iid: Variant in Catalog.items(gid):
			if String(iid).begins_with(String(id)):
				return ItemDB.get_item(StringName(String(iid)))
	return null


static func _room_ok(s: Dictionary, room_id: String) -> bool:
	var r: String = String(s.get("room", ""))
	return r.is_empty() or r == room_id
