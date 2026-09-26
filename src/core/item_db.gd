extends Node
## ItemDB – lädt die Maßstab-Tabelle (und ab Phase 02 Items/Rezepte) aus data/.
## Einzige Quelle für Größen im Spiel (MASTERPROMPT S-01). Unbekannte Referenz = klarer Fehler.

signal loaded

const SCALE_TABLE_PATH: String = "res://data/scale_table.json"
const SCALE_MUL_MIN: float = 0.7
const SCALE_MUL_MAX: float = 1.3

var _scale: Dictionary = {}   # id -> Dictionary (Eintrag aus scale_table.json)
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
	is_loaded = true
	Log.info("ItemDB: %d Maßstab-Einträge geladen" % _scale.size())
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
