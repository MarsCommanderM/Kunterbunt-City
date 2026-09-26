extends Node
## SaveSystem – Speichern/Laden von Figuren, Haustieren und Raumzuständen (Tech-Spec §3.5).
## Dateien unter user://, versioniert, mit Migrationen. Alles JSON, kein Netz (Regel T12).

const SAVE_VERSION: int = 1
const CHARACTERS_PATH: String = "user://characters.json"
const PETS_PATH: String = "user://pets.json"

## Migrationen: Schlüssel = alte Version, Wert = Callable(Dictionary) → Dictionary (neue Version).
static var _migrations: Dictionary = {}


static func _write(path: String, payload: Dictionary) -> bool:
	payload["save_version"] = SAVE_VERSION
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		Log.warn("Speichern fehlgeschlagen: %s" % path)
		return false
	f.store_string(JSON.stringify(payload))
	f.close()
	return true


static func _read(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not d is Dictionary:
		return {}
	var data: Dictionary = d
	var v: int = int(data.get("save_version", 1))
	while v < SAVE_VERSION and _migrations.has(v):
		data = (_migrations[v] as Callable).call(data)
		v += 1
	return data


# ---------------------------------------------------------------- Figuren
static func save_characters(list: Array) -> bool:
	var arr: Array = []
	for c: CharacterData in list:
		arr.append(c.to_dict())
	return _write(CHARACTERS_PATH, {"characters": arr})


static func load_characters() -> Array:
	var out: Array = []
	for d: Variant in _read(CHARACTERS_PATH).get("characters", []):
		var c: CharacterData = CharacterData.from_dict(d)
		if c:
			out.append(c)
	return out


static func has_any_character() -> bool:
	for c: CharacterData in load_characters():
		if c.is_complete():
			return true
	return false


# ---------------------------------------------------------------- Haustiere
static func save_pets(list: Array) -> bool:
	var arr: Array = []
	for p: PetData in list:
		arr.append(p.to_dict())
	return _write(PETS_PATH, {"pets": arr})


static func load_pets() -> Array:
	var out: Array = []
	for d: Variant in _read(PETS_PATH).get("pets", []):
		var p: PetData = PetData.from_dict(d)
		if p:
			out.append(p)
	return out


static func wipe() -> void:
	for p: String in [CHARACTERS_PATH, PETS_PATH]:
		if FileAccess.file_exists(p):
			DirAccess.remove_absolute(p)
