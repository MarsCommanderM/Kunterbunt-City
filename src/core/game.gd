extends Node
## Game – globaler Spielzustand: Figuren, Haustiere, aktive Figur, aktueller Bereich, Rucksack.
## Alles liegt im SaveSystem (user://), nichts geht ins Netz (Regel T12).
## Regel: Ohne vollständige Figur (Schablone + Hautton) ist KEIN Bereich betretbar (P04-T07).

signal characters_changed
signal pets_changed
signal active_character_changed

var current_area: StringName = &""
var current_room: StringName = &""
var characters: Array = []            ## [CharacterData]
var pets: Array = []                  ## [PetData]
var active_id: StringName = &""
var active_pets: Array = []           ## [StringName] – maximal 2 Tiere begleiten die Figur
var backpack: Array = []              ## [{id, …, }] – Phase 05 füllt ihn
const MAX_PETS: int = 2


func _ready() -> void:
	load_all()


# ------------------------------------------------------------------ Laden / Speichern
func load_all() -> void:
	characters = SaveSystem.load_characters()
	pets = SaveSystem.load_pets()
	if active_id.is_empty() and not characters.is_empty():
		active_id = (characters[0] as CharacterData).id
	Log.info("Game: %d Figuren, %d Haustiere geladen" % [characters.size(), pets.size()])


func save_all() -> void:
	SaveSystem.save_characters(characters)
	SaveSystem.save_pets(pets)


## Nur speichern, wenn sich wirklich etwas geändert hat (wird entprellt aufgerufen).
func save_characters() -> void:
	SaveSystem.save_characters(characters)
	characters_changed.emit()


func save_pets() -> void:
	SaveSystem.save_pets(pets)
	pets_changed.emit()


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
	active_character_changed.emit()


func add_character(c: CharacterData) -> void:
	characters.append(c)
	if active_id.is_empty():
		active_id = c.id
	save_characters()


func remove_character(id: StringName) -> void:
	for i: int in range(characters.size() - 1, -1, -1):
		if (characters[i] as CharacterData).id == id:
			characters.remove_at(i)
	if active_id == id:
		active_id = characters[0].id if not characters.is_empty() else &""
	save_characters()


func duplicate_character(id: StringName) -> CharacterData:
	var src: CharacterData = character_by_id(id)
	if src == null:
		return null
	var copy: CharacterData = CharacterData.from_dict(src.to_dict())
	copy.id = StringName("c_%d_%d" % [Time.get_unix_time_from_system(), randi() % 100000])
	if not copy.character_name.is_empty():
		copy.character_name = copy.character_name + " 2"
	# Kopien hängen nie im selben Outfit fest: Outfits werden mitkopiert, das aktive bleibt.
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
	save_pets()


func remove_pet(id: StringName) -> void:
	for i: int in range(pets.size() - 1, -1, -1):
		if (pets[i] as PetData).id == id:
			pets.remove_at(i)
	active_pets.erase(id)
	save_pets()


func toggle_active_pet(id: StringName) -> void:
	if active_pets.has(id):
		active_pets.erase(id)
	elif active_pets.size() < MAX_PETS:
		active_pets.append(id)


## Alle Daten löschen (Eltern-Tor → „Bereich zurücksetzen“).
func wipe() -> void:
	characters.clear()
	pets.clear()
	active_id = &""
	active_pets.clear()
	backpack.clear()
	SaveSystem.wipe()
	characters_changed.emit()
	pets_changed.emit()
