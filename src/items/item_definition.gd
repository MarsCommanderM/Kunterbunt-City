class_name ItemDefinition
extends Resource
## Definition eines Items aus data/items/*.json (docs/06_TECH_SPEC.md §3.1).
## Größen kommen aus der Maßstab-Tabelle (scale_ref × scale_mul) – nie aus dem Sprite.

const PLACEHOLDER_DIR: String = "res://assets/placeholders/"
const HOLD_TYPES: Array[String] = ["one_hand", "two_hands", "none"]
const PLACEMENTS: Array[String] = ["floor", "table", "shelf", "wall", "seat"]

@export var id: StringName
@export var scale_ref: String
@export var scale_mul: float = 1.0
@export var height_cm: float          ## Welt-Höhe = Tabelle × scale_mul
@export var width_cm: float
@export var category: String
@export var pivot: Vector2 = Vector2(0.5, 1.0)
@export var grip: Vector2 = Vector2(-1, -1)
@export var hold: String = "none"
@export var hold_angle: float = 0.0
@export var placement: String = "floor"
@export var movable: bool = true
@export var tags: PackedStringArray = []
@export var states: PackedStringArray = []
@export var sprite_path: String
@export var pad_px: int = 0           ## transparenter Rand im Sprite (wird bei der Größe abgezogen)
@export var surface_h_cm: float = 0.0 ## > 0: hat eine Abstellfläche (Tisch, Kommode)
@export var surface_inset: float = 0.08  ## seitlicher Rand der Fläche (Anteil der Breite)
@export var surface_frac_y: float = -1.0 ## ≥ 0: Abstellhöhe als Anteil von oben im Sprite (perspektivische Tischplatte)
@export var seat_frac_y: float = -1.0    ## ≥ 0: Sitzhöhe als Anteil von oben (Phase 03)
@export var seat_h_cm: float = 0.0    ## > 0: Sitz-/Liegeplatz (Stuhl 45, Sofa 42, Bett 45) – aus der Tabelle
@export var seat_pose: String = "sit" ## sit | lie
@export var seat_slots: int = 1
@export var container_slots: int = 0
@export var container_max_item_h_cm: float = 0.0
@export var sfx: Dictionary = {}
@export var source_file: String
@export var uses_placeholder: bool = false
@export var colors: PackedColorArray = []   ## P04b: Farbzonen (Sprite speichert Zonen-Gewichte) – leer = Sprite fertig bunt
@export var catalog: String = ""            ## P04b: Katalog-Reiter (sofas, plants …) – leer = nicht im Katalog
@export var state_sprites: Dictionary = {}  ## P04b-T10: Zustand → Sprite (auf, an …); Grundzustand = states[0] = sprite_path
@export var anim: Dictionary = {}           ## P04b-T10: Zustand → Animation (shake, pulse, bounce)


func is_stackable() -> bool:
	return tags.has("stackable")


## Hat umschaltbare Zustände (Schrank auf/zu, Gerät an/aus)?
func has_states() -> bool:
	return states.size() >= 2


## Inhalt ist immer sichtbar (Topf, Toaster, Waschmaschine) – nicht nur bei geöffnetem Deckel.
func open_top() -> bool:
	return tags.has("open_top")


func is_container() -> bool:
	return container_slots > 0


func has_seat() -> bool:
	return seat_h_cm > 0.0


func has_surface() -> bool:
	return surface_h_cm > 0.0


## Abstellhöhe in cm über dem Pivot (lokal, unskaliert).
func surface_local_h() -> float:
	if surface_frac_y >= 0.0:
		return height_cm * (1.0 - surface_frac_y)
	return surface_h_cm


## Baut eine Definition aus JSON + Maßstab-Eintrag. Gibt Fehlertexte über errors zurück.
static func from_dict(d: Dictionary, scale_entry: Dictionary, file: String, errors: Array[String]) -> ItemDefinition:
	var def := ItemDefinition.new()
	def.id = StringName(d.get("id", ""))
	def.source_file = file
	def.scale_ref = String(d.get("scale_ref", ""))
	if String(def.id).is_empty():
		errors.append("%s: Item ohne id" % file)
	if scale_entry.is_empty():
		errors.append("%s/%s: unbekannte scale_ref '%s'" % [file, def.id, def.scale_ref])
		return null
	def.scale_mul = float(d.get("scale_mul", 1.0))
	if def.scale_mul < 0.7 or def.scale_mul > 1.3:
		errors.append("%s/%s: scale_mul %.2f außerhalb 0,7–1,3" % [file, def.id, def.scale_mul])
		def.scale_mul = clampf(def.scale_mul, 0.7, 1.3)
	def.height_cm = float(scale_entry["h_cm"]) * def.scale_mul
	def.width_cm = float(scale_entry.get("w_cm", scale_entry["h_cm"])) * def.scale_mul
	def.category = String(scale_entry.get("category", ""))
	def.hold = String(d.get("hold", scale_entry.get("hold", "none")))
	if not HOLD_TYPES.has(def.hold):
		errors.append("%s/%s: hold '%s' unbekannt" % [file, def.id, def.hold])
	def.placement = String(d.get("placement", scale_entry.get("placement", "floor")))
	if not PLACEMENTS.has(def.placement):
		errors.append("%s/%s: placement '%s' unbekannt" % [file, def.id, def.placement])
	if d.get("pivot") is Array:
		def.pivot = Vector2(d["pivot"][0], d["pivot"][1])
	elif def.placement == "wall":
		def.pivot = Vector2(0.5, 0.0)
	if d.get("grip") is Array:
		def.grip = Vector2(d["grip"][0], d["grip"][1])
	if def.hold != "none" and def.grip.x < 0.0:
		errors.append("%s/%s: grip fehlt (hold = %s)" % [file, def.id, def.hold])
	def.hold_angle = float(d.get("hold_angle", 0.0))
	def.movable = bool(d.get("movable", def.category != "fixture"))
	def.tags = PackedStringArray(d.get("tags", []))
	def.states = PackedStringArray(d.get("states", []))
	def.sfx = d.get("sfx", {}) if d.get("sfx") is Dictionary else {}
	def.pad_px = int(d.get("pad_px", 0))
	def.surface_h_cm = float(d.get("surface_h_cm", scale_entry.get("surface_h_cm", 0.0))) * def.scale_mul
	def.surface_inset = float(d.get("surface_inset", 0.08))
	def.surface_frac_y = float(d.get("surface_frac_y", -1.0))
	def.seat_frac_y = float(d.get("seat_frac_y", -1.0))
	var seat: Dictionary = d.get("seat", {}) if d.get("seat") is Dictionary else {}
	def.seat_h_cm = float(seat.get("h_cm", scale_entry.get("seat_h_cm", 0.0))) * def.scale_mul
	def.seat_pose = String(seat.get("pose", "lie" if def.scale_ref.contains("bed") else "sit"))
	def.seat_slots = int(seat.get("slots", 1))
	var cont: Dictionary = d.get("container", {})
	def.container_slots = int(cont.get("slots", 0))
	def.container_max_item_h_cm = float(cont.get("max_item_h_cm", def.height_cm * 0.3))
	for h: Variant in Array(d.get("colors", [])):
		def.colors.append(Color(String(h)))
	def.catalog = String(d.get("catalog", ""))
	def.state_sprites = d.get("state_sprites", {}) if d.get("state_sprites") is Dictionary else {}
	def.anim = d.get("anim", {}) if d.get("anim") is Dictionary else {}
	def.sprite_path = String(d.get("sprite", ""))
	if def.sprite_path.is_empty() or not ResourceLoader.exists(def.sprite_path):
		def.uses_placeholder = true
		def.sprite_path = PLACEHOLDER_DIR + def.scale_ref + ".png"
		if not ResourceLoader.exists(def.sprite_path):
			errors.append("%s/%s: weder Sprite noch Platzhalter (%s) – tools/make_placeholders.py ausführen" % [file, def.id, def.sprite_path])
	return def
