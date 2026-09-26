class_name CharacterTemplates
extends RefCounted
## Figuren-Schablonen aus data/characters/templates.json + Teile-Index assets/characters/parts/parts.json.
## Gesamthöhe kommt IMMER aus der Maßstab-Tabelle (scale_ref) – nie aus den Teilen.

const TEMPLATES_PATH: String = "res://data/characters/templates.json"
const PARTS_DIR: String = "res://assets/characters/parts/"

static var _data: Dictionary = {}
static var _parts: Dictionary = {}


static func data() -> Dictionary:
	if _data.is_empty():
		_data = JSON.parse_string(FileAccess.get_file_as_string(TEMPLATES_PATH))
		_parts = JSON.parse_string(FileAccess.get_file_as_string(PARTS_DIR + "parts.json"))
	return _data


static func ids() -> Array:
	return data()["templates"].keys()


static func get_template(tid: String) -> Dictionary:
	return data()["templates"].get(tid, {})


static func part_info(tid: String, part: String) -> Dictionary:
	data()
	return _parts.get(tid, {}).get(part, {})


## Sitz-Geometrie der Schablone (sit_drop_cm, shoe_h_cm, sit_thigh_cm).
static func geometry(tid: String) -> Dictionary:
	data()
	return _parts.get(tid, {}).get("_geometry", {})


static func part_texture(tid: String, part: String) -> Texture2D:
	return load(PARTS_DIR + tid + "/" + part + ".png")


static func default_look(tid: String) -> Dictionary:
	return data()["default_look"].get(tid, {}).duplicate()


static func emotions() -> Array:
	return data()["emotions"]


## Synthetische Item-Definition für eine Figur (Kategorie character, Größe aus der Tabelle).
static func make_definition(tid: String) -> ItemDefinition:
	var t: Dictionary = get_template(tid)
	var def := ItemDefinition.new()
	def.id = StringName("char_" + tid)
	def.scale_ref = String(t["scale_ref"])
	def.height_cm = ItemDB.height_cm(def.scale_ref)
	def.width_cm = ItemDB.width_cm(def.scale_ref)
	def.category = "character"
	def.hold = "none"
	def.placement = "floor"
	def.movable = true
	def.pivot = Vector2(0.5, 1.0)
	return def
