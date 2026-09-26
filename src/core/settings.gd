extends Node
## Settings – Lautstärken, Sprache, Barrierefreiheit. Gespeichert lokal in user://settings.json.

signal changed(key: String, value: Variant)

const PATH: String = "user://settings.json"
const DEFAULTS: Dictionary = {
	"volume_music": 0.7,
	"volume_sfx": 0.9,
	"volume_animals": 0.8,
	"language": "de",
	"reduced_motion": false,
	"large_ui": false,
}

var _values: Dictionary = DEFAULTS.duplicate(true)


func _ready() -> void:
	load_settings()


func get_value(key: String) -> Variant:
	assert(DEFAULTS.has(key), "Unbekannte Einstellung: %s" % key)
	return _values.get(key, DEFAULTS[key])


func set_value(key: String, value: Variant) -> void:
	assert(DEFAULTS.has(key), "Unbekannte Einstellung: %s" % key)
	_values[key] = value
	changed.emit(key, value)
	save_settings()


func reset() -> void:
	_values = DEFAULTS.duplicate(true)
	save_settings()


func load_settings() -> void:
	if not FileAccess.file_exists(PATH):
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(PATH))
	if parsed is Dictionary:
		for key: String in DEFAULTS:
			if (parsed as Dictionary).has(key):
				_values[key] = parsed[key]


func save_settings() -> void:
	var f: FileAccess = FileAccess.open(PATH, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(_values, "\t"))
