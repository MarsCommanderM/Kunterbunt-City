extends Node
## SaveSystem – Speichern/Laden von Figuren, Haustieren, Rucksack, Album und Raumzuständen
## (Tech-Spec §3.5, P05-T07/T08). Dateien unter user://, versioniert, MIT Migrationen.
## Alles JSON, kein Netz (Regel T12). Drei Welt-Slots.

const SAVE_VERSION: int = 4
const SLOTS: int = 3
const WORLD_PATH: String = "user://world_%d.json"
const LEGACY_CHARACTERS: String = "user://characters.json"
const LEGACY_PETS: String = "user://pets.json"
const EXPORT_DIR: String = "user://export/"

## Migrationen: Schlüssel = alte Version, Wert = Callable(Dictionary) → Dictionary (neue Version).
static var _migrations: Dictionary = {}


static func _static_init() -> void:
	_migrations[1] = _migrate_v1_to_v2
	_migrations[2] = _migrate_v2_to_v3
	_migrations[3] = _migrate_v3_to_v4


## Version 1 (Phase 04) kannte nur Figuren und Tiere. Version 2 ergänzt Bereiche, Rucksack,
## Album und die begleitenden Tiere. Alte Stände bleiben dabei erhalten.
static func _migrate_v1_to_v2(old: Dictionary) -> Dictionary:
	var d: Dictionary = old.duplicate(true)
	d["areas"] = d.get("areas", {})
	d["backpack"] = Array(d.get("backpack", [])).duplicate(true)
	d["album"] = Array(d.get("album", [])).duplicate(true)
	d["active_pets"] = Array(d.get("active_pets", [])).duplicate(true)
	d["slot"] = int(d.get("slot", 0))
	d["save_version"] = 2
	Log.info("SaveSystem: Speicherstand v1 → v2 gewandert (%d Figuren)" % [
		Array(d.get("characters", [])).size()])
	return d


## Version 3 (P07): Zuhause hat mehrere Räume – je Raum Tapete/Boden (`decor`) und der zuletzt besuchte Raum
## (`last_room`). Bestehende Raumzustände bleiben unverändert (die Küche heißt weiter `kitchen`).
static func _migrate_v2_to_v3(old: Dictionary) -> Dictionary:
	var d: Dictionary = old.duplicate(true)
	d["decor"] = Dictionary(d.get("decor", {})).duplicate(true)
	d["last_room"] = Dictionary(d.get("last_room", {})).duplicate(true)
	d["save_version"] = 3
	Log.info("SaveSystem: Speicherstand v2 → v3 gewandert (%d Bereiche mit Zustand)" % [
		Dictionary(d.get("areas", {})).size()])
	return d


## Version 4 (P07-T10): gefundene Geheimnisse (Sticker im Album). Alles andere bleibt.
static func _migrate_v3_to_v4(old: Dictionary) -> Dictionary:
	var d: Dictionary = old.duplicate(true)
	d["secrets"] = Array(d.get("secrets", [])).duplicate(true)
	d["save_version"] = 4
	Log.info("SaveSystem: Speicherstand v3 → v4 gewandert")
	return d


## P11-T04: Erst in eine .tmp-Datei schreiben, dann rotieren: .bak2 ← .bak1 ← aktuelle Datei ← .tmp.
## Ein Absturz mitten im Schreiben zerstört so nie den letzten guten Stand.
const BACKUPS: int = 2


static func _write(path: String, payload: Dictionary) -> bool:
	payload["save_version"] = SAVE_VERSION
	var tmp: String = path + ".tmp"
	var f := FileAccess.open(tmp, FileAccess.WRITE)
	if f == null:
		Log.warn("Speichern fehlgeschlagen: %s" % path)
		return false
	f.store_string(JSON.stringify(payload))
	f.close()
	for i: int in range(BACKUPS, 0, -1):
		var older: String = backup_path(path, i)
		var newer: String = path if i == 1 else backup_path(path, i - 1)
		if FileAccess.file_exists(newer):
			if FileAccess.file_exists(older):
				DirAccess.remove_absolute(older)
			DirAccess.rename_absolute(newer, older)
	return DirAccess.rename_absolute(tmp, path) == OK


static func backup_path(path: String, i: int) -> String:
	return "%s.bak%d" % [path, i]


## Lesen mit Rettung: kaputte oder fehlende Datei → erste lesbare Sicherung (.bak1, dann .bak2).
static func _read(path: String) -> Dictionary:
	for i: int in BACKUPS + 1:
		var p: String = path if i == 0 else backup_path(path, i)
		var d: Dictionary = _read_one(p)
		if not d.is_empty():
			if i > 0:
				Log.warn("SaveSystem: %s war kaputt – Sicherung %d geladen" % [path, i])
			return d
	return {}


static func _read_one(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var j := JSON.new()                               # still: kaputte Datei ist ein erwarteter Fall (Sicherung)
	if j.parse(FileAccess.get_file_as_string(path)) != OK or not j.data is Dictionary:
		return {}
	var data: Dictionary = j.data
	var v: int = int(data.get("save_version", 1))
	while v < SAVE_VERSION and _migrations.has(v):
		data = (_migrations[v] as Callable).call(data)
		v = int(data.get("save_version", v + 1))
	return data


# ------------------------------------------------------------------ Welt (Slots)
static func world_path(slot: int) -> String:
	return WORLD_PATH % clampi(slot, 0, SLOTS - 1)


static func empty_world(slot: int = 0) -> Dictionary:
	return {
		"save_version": SAVE_VERSION, "slot": slot,
		"characters": [], "pets": [], "active_id": "", "active_pets": [],
		"backpack": [], "album": [], "areas": {}, "decor": {}, "last_room": {}, "secrets": [], "updated_ms": 0,
	}


static func save_world(slot: int, payload: Dictionary) -> bool:
	var w: Dictionary = payload.duplicate(true)
	w["slot"] = clampi(slot, 0, SLOTS - 1)
	w["updated_ms"] = Time.get_unix_time_from_system()
	return _write(world_path(slot), w)


static func load_world(slot: int) -> Dictionary:
	var p: String = world_path(slot)
	var w: Dictionary = _read(p)
	if w.is_empty():
		# Erststart mit alten Einzeldateien (Phase 04) → automatisch übernehmen.
		var legacy: Dictionary = import_legacy()
		if not legacy.is_empty():
			save_world(slot, legacy)
			return legacy
		return empty_world(slot)
	return _complete(w)


static func _complete(w: Dictionary) -> Dictionary:
	var out: Dictionary = empty_world(int(w.get("slot", 0)))
	for k: String in out:
		if w.has(k):
			out[k] = w[k]
	return out


static func world_exists(slot: int) -> bool:
	return FileAccess.file_exists(world_path(slot))


static func world_info(slot: int) -> Dictionary:
	var w: Dictionary = load_world(slot)
	return {
		"slot": slot, "exists": world_exists(slot),
		"characters": Array(w.get("characters", [])).size(),
		"pets": Array(w.get("pets", [])).size(),
		"updated_ms": int(w.get("updated_ms", 0)),
		"version": int(w.get("save_version", 1)),
	}


static func wipe_world(slot: int) -> void:
	for p: String in [world_path(slot), backup_path(world_path(slot), 1), backup_path(world_path(slot), 2)]:
		if FileAccess.file_exists(p):
			DirAccess.remove_absolute(p)


static func wipe() -> void:
	for i: int in SLOTS:
		wipe_world(i)
	for p: String in [LEGACY_CHARACTERS, LEGACY_PETS]:
		if FileAccess.file_exists(p):
			DirAccess.remove_absolute(p)


## Alte Phase-04-Dateien (characters.json / pets.json) in eine Welt übernehmen.
static func import_legacy() -> Dictionary:
	var chars: Array = []
	var pets: Array = []
	if FileAccess.file_exists(LEGACY_CHARACTERS):
		var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(LEGACY_CHARACTERS))
		if d is Dictionary:
			chars = Array((d as Dictionary).get("characters", []))
	if FileAccess.file_exists(LEGACY_PETS):
		var p: Variant = JSON.parse_string(FileAccess.get_file_as_string(LEGACY_PETS))
		if p is Dictionary:
			pets = Array((p as Dictionary).get("pets", []))
	if chars.is_empty() and pets.is_empty():
		return {}
	var w: Dictionary = empty_world(0)
	w["characters"] = chars
	w["pets"] = pets
	if not chars.is_empty():
		w["active_id"] = String((chars[0] as Dictionary).get("id", ""))
	Log.info("SaveSystem: alte Figuren-/Tier-Dateien übernommen (%d/%d)" % [chars.size(), pets.size()])
	return w


# ------------------------------------------------------------------ Export / Import (ohne Netz)
static func export_world(slot: int, path: String = "") -> String:
	DirAccess.make_dir_recursive_absolute(EXPORT_DIR)
	var out: String = path if not path.is_empty() else \
		EXPORT_DIR + "kunterbunt-city-welt-%d.json" % clampi(slot, 0, SLOTS - 1)
	var w: Dictionary = load_world(slot)
	var f := FileAccess.open(out, FileAccess.WRITE)
	if f == null:
		return ""
	f.store_string(JSON.stringify(w, "\t"))
	f.close()
	return ProjectSettings.globalize_path(out)


static func import_world(path: String, slot: int = 0) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not d is Dictionary:
		return false
	var w: Dictionary = _complete(d)
	w["save_version"] = SAVE_VERSION      # migrieren passiert beim nächsten Laden
	return save_world(slot, w)


# ------------------------------------------------------------------ Figuren / Tiere (Komfort)
static func save_characters(list: Array) -> bool:
	var arr: Array = []
	for c: CharacterData in list:
		arr.append(c.to_dict())
	return _write(LEGACY_CHARACTERS, {"characters": arr})


static func load_characters() -> Array:
	var out: Array = []
	for d: Variant in _read(LEGACY_CHARACTERS).get("characters", []):
		var c: CharacterData = CharacterData.from_dict(d)
		if c:
			out.append(c)
	return out


static func has_any_character() -> bool:
	for c: CharacterData in load_characters():
		if c.is_complete():
			return true
	return false


static func save_pets(list: Array) -> bool:
	var arr: Array = []
	for p: PetData in list:
		arr.append(p.to_dict())
	return _write(LEGACY_PETS, {"pets": arr})


static func load_pets() -> Array:
	var out: Array = []
	for d: Variant in _read(LEGACY_PETS).get("pets", []):
		var p: PetData = PetData.from_dict(d)
		if p:
			out.append(p)
	return out


# ------------------------------------------------------------------ Album (Fotos)
static func album_dir() -> String:
	return "user://album/"


static func album_photos() -> Array:
	DirAccess.make_dir_recursive_absolute(album_dir())
	var out: Array = []
	for f: String in DirAccess.get_files_at(album_dir()):
		if f.ends_with(".jpg"):
			out.append(album_dir() + f)
	out.sort()
	out.reverse()
	return out


static func album_add(img: Image) -> String:
	DirAccess.make_dir_recursive_absolute(album_dir())
	var name: String = "foto_%d.jpg" % Time.get_unix_time_from_system()
	if img.save_jpg(album_dir() + name, 0.85) != OK:
		return ""
	return album_dir() + name


static func album_remove(path: String) -> void:
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(path)
