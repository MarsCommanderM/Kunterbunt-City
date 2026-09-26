extends Node
## Game – globaler Spielzustand (P05-T07): aktive Figur, Haustiere, Rucksack, Album,
## Raumzustände je Bereich, Welt-Slot. Alles liegt lokal in user:// (SaveSystem), kein Netz.
## Regel: Ohne vollständige Figur (Schablone + Hautton) ist KEIN Bereich betretbar (P04-T07).

signal characters_changed
signal pets_changed
signal active_character_changed
signal world_changed

const MAX_PETS: int = 2
const AUTOSAVE_S: float = 2.0            ## entprellt: erst 2 s nach der letzten Änderung

var slot: int = 0
var current_area: StringName = &""
var current_room: StringName = &""
var characters: Array = []               ## [CharacterData]
var pets: Array = []                     ## [PetData]
var active_id: StringName = &""
var active_pets: Array = []              ## [StringName] – maximal 2 Tiere begleiten
var backpack: Array = []                 ## [{id, …}] – max. 20 Plätze
var areas: Dictionary = {}               ## area_id → {room_id → [Item-Zustand]}
var _timer: Timer
var _dirty: Dictionary = {}              ## "area/room" → true


func _ready() -> void:
	_timer = Timer.new()
	_timer.one_shot = true
	_timer.wait_time = AUTOSAVE_S
	_timer.timeout.connect(_flush)
	add_child(_timer)
	load_all()


# ------------------------------------------------------------------ Laden / Speichern
func load_all() -> void:
	var w: Dictionary = SaveSystem.load_world(slot)
	characters = _chars(w.get("characters", []))
	pets = _pets(w.get("pets", []))
	backpack = Array(w.get("backpack", [])).duplicate(true)
	areas = Dictionary(w.get("areas", {})).duplicate(true)
	active_id = StringName(String(w.get("active_id", "")))
	active_pets = []
	for p: Variant in Array(w.get("active_pets", [])):
		active_pets.append(StringName(String(p)))
	if active_id.is_empty() and not characters.is_empty():
		active_id = (characters[0] as CharacterData).id
	Log.info("Game: Welt %d · %d Figuren, %d Haustiere, %d im Rucksack" % [
		slot, characters.size(), pets.size(), backpack.size()])


func _chars(list: Array) -> Array:
	var out: Array = []
	for d: Variant in list:
		var c: CharacterData = CharacterData.from_dict(d)
		if c:
			out.append(c)
	# Rückwärtsgang: alte Einzeldateien (Phase 04) sind sonst weg
	if out.is_empty():
		out = SaveSystem.load_characters()
	return out


func _pets(list: Array) -> Array:
	var out: Array = []
	for d: Variant in list:
		var p: PetData = PetData.from_dict(d)
		if p:
			out.append(p)
	if out.is_empty():
		out = SaveSystem.load_pets()
	return out


func save_all() -> void:
	SaveSystem.save_world(slot, _world_dict())


func _world_dict() -> Dictionary:
	var chars: Array = []
	for c: Variant in characters:
		chars.append((c as CharacterData).to_dict())
	var ps: Array = []
	for p: Variant in pets:
		ps.append((p as PetData).to_dict())
	var ap: Array = []
	for i: Variant in active_pets:
		ap.append(String(i))
	return {
		"characters": chars, "pets": ps, "active_id": String(active_id), "active_pets": ap,
		"backpack": backpack, "album": [], "areas": areas, "slot": slot,
	}


## Sofort speichern (beim Verlassen eines Bereichs, beim Beenden).
func save_now() -> void:
	_flush()


## Änderung merken – gespeichert wird entprellt (2 s), damit es nie ruckelt.
func mark_dirty(area_id: StringName = &"", room_id: StringName = &"") -> void:
	if area_id != &"":
		current_area = area_id
		current_room = room_id
		_dirty["%s/%s" % [String(area_id), String(room_id)]] = true
	_timer.start(AUTOSAVE_S)


func _flush() -> void:
	save_all()
	world_changed.emit()


# ------------------------------------------------------------------ Raumzustände
func room_state(area_id: StringName, room_id: StringName) -> Array:
	return Array(Dictionary(areas.get(String(area_id), {})).get(String(room_id), []))


func set_room_state(area_id: StringName, room_id: StringName, snapshot: Array) -> void:
	var a: Dictionary = Dictionary(areas.get(String(area_id), {}))
	a[String(room_id)] = snapshot
	areas[String(area_id)] = a
	mark_dirty()


func reset_areas() -> void:
	areas.clear()
	mark_dirty()
	save_now()


# ------------------------------------------------------------------ Welt-Slots
func switch_slot(i: int) -> void:
	save_now()
	slot = clampi(i, 0, SaveSystem.SLOTS - 1)
	active_id = &""
	active_pets.clear()
	backpack.clear()
	load_all()
	world_changed.emit()


# ------------------------------------------------------------------ Figuren
func has_complete_character() -> bool:
	for c: Variant in characters:
		if (c as CharacterData).is_complete():
			return true
	return false


func character_by_id(id: StringName) -> CharacterData:
	for c: Variant in characters:
		if (c as CharacterData).id == id:
			return c
	return null


func active_character() -> CharacterData:
	var c: CharacterData = character_by_id(active_id)
	if c == null and not characters.is_empty():
		c = characters[0]
		active_id = c.id
	return c


func set_active(id: StringName) -> void:
	if character_by_id(id) == null:
		return
	active_id = id
	mark_dirty()
	active_character_changed.emit()


func add_character(c: CharacterData) -> void:
	characters.append(c)
	if active_id.is_empty():
		active_id = c.id
	mark_dirty()


func remove_character(id: StringName) -> void:
	for i: int in range(characters.size() - 1, -1, -1):
		if (characters[i] as CharacterData).id == id:
			characters.remove_at(i)
	if active_id == id:
		active_id = characters[0].id if not characters.is_empty() else &""
	mark_dirty()


func duplicate_character(id: StringName) -> CharacterData:
	var src: CharacterData = character_by_id(id)
	if src == null:
		return null
	var copy: CharacterData = CharacterData.from_dict(src.to_dict())
	copy.id = StringName("c_%d_%d" % [Time.get_unix_time_from_system(), randi() % 100000])
	if not copy.character_name.is_empty():
		copy.character_name = copy.character_name + " 2"
	add_character(copy)
	return copy


# ------------------------------------------------------------------ Haustiere
func pet_by_id(id: StringName) -> PetData:
	for p: Variant in pets:
		if (p as PetData).id == id:
			return p
	return null


func add_pet(p: PetData) -> void:
	pets.append(p)
	if active_pets.size() < MAX_PETS:
		active_pets.append(p.id)
	mark_dirty()


func remove_pet(id: StringName) -> void:
	for i: int in range(pets.size() - 1, -1, -1):
		if (pets[i] as PetData).id == id:
			pets.remove_at(i)
	active_pets.erase(id)
	mark_dirty()


func toggle_active_pet(id: StringName) -> void:
	if active_pets.has(id):
		active_pets.erase(id)
	elif active_pets.size() < MAX_PETS:
		active_pets.append(id)
	mark_dirty()


# ------------------------------------------------------------------ Komfort (alt, Tests)
func save_characters() -> void:
	mark_dirty()
	SaveSystem.save_characters(characters)
	characters_changed.emit()


func save_pets() -> void:
	mark_dirty()
	SaveSystem.save_pets(pets)
	pets_changed.emit()


## Alles löschen (Eltern-Tor → „Alles löschen").
func wipe() -> void:
	characters.clear()
	pets.clear()
	active_id = &""
	active_pets.clear()
	backpack.clear()
	areas.clear()
	SaveSystem.wipe()
	characters_changed.emit()
	pets_changed.emit()
