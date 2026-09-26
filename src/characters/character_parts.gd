class_name CharacterParts
extends RefCounted
## P04-T01: Katalog der Editor-Teile (data/character_parts/<slot>.json) + Farbpalette.
## Rein statisch, kein Autoload. Jeder Slot hat 5 Varianten (T10); jede Variante nennt das
## Teil (Sprite in assets/characters/parts/<schablone>/) und wie viele Farbzonen es nutzt.

const DIR: String = "res://data/character_parts/"
const PALETTE_FILE: String = DIR + "palette.json"

static var _slots: Dictionary = {}
static var _palette: Dictionary = {}


static func data() -> Dictionary:
	if _slots.is_empty():
		for f: String in DirAccess.get_files_at(DIR):
			if not f.ends_with(".json") or f == "palette.json":
				continue
			var d: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(DIR + f))
			if d is Dictionary and d.has("slot"):
				_slots[String(d["slot"])] = d
	return _slots


static func palette() -> Dictionary:
	if _palette.is_empty():
		_palette = JSON.parse_string(FileAccess.get_file_as_string(PALETTE_FILE))
	return _palette


static func slot_ids() -> Array:
	return data().keys()


static func variants(slot: String) -> Array:
	return data().get(slot, {}).get("variants", [])


static func ids(slot: String) -> Array:
	var out: Array = []
	for v: Dictionary in variants(slot):
		out.append(String(v["id"]))
	return out


static func variant(slot: String, id: String) -> Dictionary:
	for v: Dictionary in variants(slot):
		if String(v["id"]) == id:
			return v
	return {}


static func label(slot: String) -> String:
	return String(data().get(slot, {}).get("label", slot))


static func icon(slot: String) -> String:
	return String(data().get(slot, {}).get("icon", "•"))


## Erste Variante, die kein „none"/„bald" ist – Startwert im Editor.
static func default_id(slot: String) -> String:
	for v: Dictionary in variants(slot):
		if not Array(v.get("tags", [])).has("none"):
			return String(v["id"])
	return String(variants(slot)[0]["id"]) if not variants(slot).is_empty() else ""


static func is_empty_variant(slot: String, id: String) -> bool:
	return Array(variant(slot, id).get("tags", [])).has("none")


## Gibt es das Sprite für diese Schablone? (Schützt vor Katalog ohne Teile.)
static func part_exists(tid: String, slot: String, id: String) -> bool:
	var v: Dictionary = variant(slot, id)
	if v.is_empty():
		return false
	return CharacterTemplates.has_part(tid, String(v["part"]))


## Zonen-Anzahl der Variante (1…3).
static func zones(slot: String, id: String) -> int:
	return int(variant(slot, id).get("zones", 1))


## Farben einer Gruppe aus der Palette (Hex-Strings).
static func palette_colors(group: String) -> Array:
	return palette().get(group, {}).get("colors", [])


static func palette_groups() -> Array:
	var out: Array = []
	for k: String in palette():
		if k != "note":
			out.append(k)
	return out


static func random_colors(group: String, rng: RandomNumberGenerator) -> Array:
	var c: Array = palette_colors(group)
	return [c[rng.randi() % c.size()]] if not c.is_empty() else ["#ffffff"]


## Stimmige Zufalls-Kombination (🎲): je Slot eine Variante + passende Farben.
static func random_set(tid: String, rng: RandomNumberGenerator) -> Dictionary:
	var parts: Dictionary = {}
	var colors: Dictionary = {}
	for slot: String in slot_ids():
		var ids: Array = ids(slot)
		if ids.is_empty():
			continue
		var pick: String = String(ids[rng.randi() % ids.size()])
		parts[slot] = pick
		var group: String = _group_for(slot)
		var pal: Array = palette_colors(group)
		var n: int = clampi(zones(slot, pick), 1, 3)
		var cols: Array = []
		for i: int in n:
			cols.append(pal[rng.randi() % pal.size()])
		colors[slot] = cols
	return {"parts": parts, "colors": colors}


static func default_set(tid: String) -> Dictionary:
	var parts: Dictionary = {}
	var colors: Dictionary = {}
	for slot: String in slot_ids():
		var id: String = default_id(slot)
		if id.is_empty():
			continue
		parts[slot] = id
		var pal: Array = palette_colors(_group_for(slot))
		var n: int = clampi(zones(slot, id), 1, 3)
		var cols: Array = []
		for i: int in n:
			cols.append(pal[i * 3 % maxi(1, pal.size())] if not pal.is_empty() else "#ffffff")
		colors[slot] = cols
	return {"parts": parts, "colors": colors}


## Welche Palette passt zu welchem Slot?
static func _group_for(slot: String) -> String:
	match slot:
		"top":
			return "cloth"
		"bottom":
			return "cloth"
		"shoes":
			return "shoes"
		"hair":
			return "hair"
		"accessory", "aid":
			return "cloth"
		_:
			return "skin"
