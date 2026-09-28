extends Node
## ItemDB – lädt die Maßstab-Tabelle (und ab Phase 02 Items/Rezepte) aus data/.
## Einzige Quelle für Größen im Spiel (MASTERPROMPT S-01). Unbekannte Referenz = klarer Fehler.

signal loaded

const SCALE_TABLE_PATH: String = "res://data/scale_table.json"
const ITEMS_DIR: String = "res://data/items/"
const ALIASES_PATH: String = "res://data/item_aliases.json"
const SCALE_MUL_MIN: float = 0.7
const SCALE_MUL_MAX: float = 1.3

var _scale: Dictionary = {}   # id -> Dictionary (Eintrag aus scale_table.json)
var _items: Dictionary = {}   # id -> ItemDefinition
var _aliases: Dictionary = {} # alte id -> neue id (data/item_aliases.json)
## Fehler der letzten Validierung (leer = alles gut). Tests prüfen, dass dies leer ist.
var validation_errors: Array[String] = []
var is_loaded: bool = false


func _ready() -> void:
	load_all()


func load_all() -> void:
	_scale.clear()
	var text: String = FileAccess.get_file_as_string(SCALE_TABLE_PATH)
	var parsed: Variant = JSON.parse_string(text)
	if not (parsed is Dictionary) or not (parsed as Dictionary).has("entries"):
		Log.error("ItemDB: %s fehlt oder ist kaputt" % SCALE_TABLE_PATH)
		return
	for e: Dictionary in parsed["entries"]:
		_scale[e["id"]] = e
	_load_items()
	is_loaded = true
	Log.info("ItemDB: %d Maßstab-Einträge, %d Items geladen" % [_scale.size(), _items.size()])
	for e: String in validation_errors:
		Log.error("ItemDB: " + e)
	loaded.emit()


func has_scale(ref: String) -> bool:
	return _scale.has(ref)


## Eintrag der Maßstab-Tabelle. Unbekannt → Fehler + leeres Dictionary.
func get_scale(ref: String) -> Dictionary:
	if not _scale.has(ref):
		Log.error("ItemDB: unbekannte scale_ref '%s' – Eintrag in data/scale_table.json anlegen" % ref)
		return {}
	return _scale[ref]


## Welt-Höhe in cm = Tabelle × scale_mul (0,7–1,3, Regel S-02).
func height_cm(ref: String, scale_mul: float = 1.0) -> float:
	var e: Dictionary = get_scale(ref)
	if e.is_empty():
		return 0.0
	if scale_mul < SCALE_MUL_MIN or scale_mul > SCALE_MUL_MAX:
		Log.error("ItemDB: scale_mul %.2f für '%s' außerhalb 0,7–1,3" % [scale_mul, ref])
		scale_mul = clampf(scale_mul, SCALE_MUL_MIN, SCALE_MUL_MAX)
	return float(e["h_cm"]) * scale_mul


func width_cm(ref: String, scale_mul: float = 1.0) -> float:
	var e: Dictionary = get_scale(ref)
	return 0.0 if e.is_empty() else float(e.get("w_cm", e["h_cm"])) * scale_mul


func entry_count() -> int:
	return _scale.size()


# ---------------------------------------------------------------- Items (Phase 02)

func _load_items() -> void:
	_items.clear()
	validation_errors.clear()
	var dir: DirAccess = DirAccess.open(ITEMS_DIR)
	if dir == null:
		return
	var files: PackedStringArray = dir.get_files()
	files.sort()
	for f: String in files:
		if not f.ends_with(".json"):
			continue
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(ITEMS_DIR + f))
		if not (parsed is Dictionary):
			validation_errors.append("%s: kein gültiges JSON" % f)
			continue
		for d: Dictionary in parsed.get("items", []):
			var def: ItemDefinition = ItemDefinition.from_dict(d, _scale.get(d.get("scale_ref", ""), {}), f, validation_errors)
			if def == null:
				continue
			if _items.has(def.id):
				validation_errors.append("%s: doppelte Item-ID '%s'" % [f, def.id])
				continue
			_items[def.id] = def
	_load_aliases()


## Umbenannte Items (R-11): alte ID → neue ID. Alte Speicherstände finden ihr Ding weiter, gespeichert wird die neue ID.
func _load_aliases() -> void:
	_aliases.clear()
	if not FileAccess.file_exists(ALIASES_PATH):
		return
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(ALIASES_PATH))
	for old: Variant in Dictionary(d.get("aliases", {}) if d is Dictionary else {}):
		var new_id := StringName(String(d["aliases"][old]))
		if _items.has(new_id) and not _items.has(StringName(String(old))):
			_aliases[StringName(String(old))] = new_id
		else:
			validation_errors.append("item_aliases.json: '%s' → '%s' passt nicht" % [old, new_id])


func has_item(id: StringName) -> bool:
	return _items.has(id) or _aliases.has(id)


## Item-Definition per ID (auch alte, umbenannte IDs). Unbekannt → Fehler + null.
func get_item(id: StringName) -> ItemDefinition:
	if not _items.has(id) and _aliases.has(id):
		id = _aliases[id]
	if not _items.has(id):
		Log.error("ItemDB: unbekanntes Item '%s'" % id)
		return null
	return _items[id]


func item_ids() -> Array:
	var ids: Array = _items.keys()
	ids.sort()
	return ids


func item_count() -> int:
	return _items.size()
