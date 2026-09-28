class_name Catalog
extends RefCounted
## P04b-T09: Katalog-Reiter aus data/catalog.json (erzeugt von tools/make_items.py).
## Jedes Item ist in JEDEM Raum einsetzbar – die Luftmatratze auch im Wohnzimmer.

const PATH: String = "res://data/catalog.json"

static var _groups: Array = []


static func groups() -> Array:
	if _groups.is_empty() and FileAccess.file_exists(PATH):
		var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(PATH))
		if d is Dictionary:
			for g: Dictionary in Array(d.get("groups", [])):
				var ids: Array = []
				for id: Variant in Array(g.get("items", [])):
					if ItemDB.get_item(StringName(String(id))) != null:
						ids.append(String(id))
				if not ids.is_empty():
					_groups.append({"id": String(g["id"]), "icon": String(g.get("icon", "")), "items": ids})
	return _groups


static func group_ids() -> Array:
	var out: Array = []
	for g: Dictionary in groups():
		out.append(g["id"])
	return out


static func items(group: String) -> Array:
	for g: Dictionary in groups():
		if g["id"] == group:
			return g["items"]
	return []


static func count() -> int:
	var n: int = 0
	for g: Dictionary in groups():
		n += Array(g["items"]).size()
	return n
