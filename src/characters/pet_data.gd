class_name PetData
extends RefCounted
## P04-T09: Datenmodell eines Haustiers (Art aus der Tabelle, Fell, Muster, Halsband, Charakterzug).

const TRAITS: Array[String] = ["playful", "sleepy", "curious", "greedy", "shy"]
const PATTERNS: Array[String] = ["plain", "patches", "stripes", "spots", "tips"]

var id: StringName
var species_id: String = "pet_dog_medium"     ## Item-Id (Kategorie pet, Größe aus der Tabelle)
var pet_name: String = ""
var fur: String = ""
var fur2: String = ""
var pattern: String = "plain"
var collar: String = ""
var pet_trait: String = "playful"


static func create(sid: String = "pet_dog_medium") -> PetData:
	var d := PetData.new()
	d.id = StringName("p_%d_%d" % [Time.get_unix_time_from_system(), randi() % 100000])
	d.species_id = sid if PetSpecies.ids().has(sid) else "pet_dog_medium"
	var cols: Array = PetSpecies.default_fur(d.species_id)
	d.fur = String(cols[0])
	d.fur2 = String(cols[1])
	d.collar = String(cols[2])
	d.pet_trait = String(PetSpecies.trait_ids(d.species_id)[0])
	return d


func to_dict() -> Dictionary:
	return {"id": String(id), "species": species_id, "name": pet_name, "fur": fur, "fur2": fur2,
		"pattern": pattern, "collar": collar, "trait": pet_trait,
		"created_ms": Time.get_ticks_msec()}


static func from_dict(d: Dictionary) -> PetData:
	if not d is Dictionary or d.is_empty():
		return null
	var p := PetData.new()
	p.id = StringName(String(d.get("id", "p_0")))
	p.species_id = String(d.get("species", "pet_dog_medium"))
	p.pet_name = String(d.get("name", ""))
	p.fur = String(d.get("fur", ""))
	p.fur2 = String(d.get("fur2", ""))
	p.pattern = String(d.get("pattern", "plain"))
	p.collar = String(d.get("collar", ""))
	p.pet_trait = String(d.get("trait", "playful"))
	if not TRAITS.has(p.pet_trait):
		p.pet_trait = "playful"
	return p


func is_complete() -> bool:
	return not species_id.is_empty() and ItemDB.get_item(StringName(species_id)) != null


func display_name() -> String:
	if not pet_name.is_empty():
		return pet_name
	var sid: String = species_id if PetSpecies.ids().has(species_id) else "pet_dog_medium"
	return PetSpecies.label(sid)
