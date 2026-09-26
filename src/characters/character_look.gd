class_name CharacterLook
extends RefCounted
## P04-T04: Aussehen einer Figur → Teilname + Zonenfarben je Ebene.
## Der Rig kennt nur Ebenen-Namen; WELCHES Teil (Variante) und WELCHE Farben (Zonen) sie tragen,
## entscheidet diese Klasse. Dadurch bleibt character_rig.gd schlank und der Editor tauscht nur
## `look` aus (Schablone + Hautton + Teile + Farben).

const SHADER: Shader = preload("res://assets/shaders/zone_tint.gdshader")

## Farben, die der Spieler nicht wählt (Augen/Mund sind fertig koloriert).
const FIXED: Dictionary = {
	"Eyes": ["#3a2620", "#ffffff"],      # Zone 1 = Iris (später wählbar), Zone 2 = Glanz
	"Mouth": ["#a85050", "#ff9aa8"],     # Zone 1 = Mund, Zone 2 = Zunge
}

## Ebene → Slot im Editor-Katalog.
const SLOT: Dictionary = {
	"HairBack": "hair", "HairFront": "hair", "Top": "top", "ArmBackSleeve": "top",
	"ArmFrontSleeve": "top", "Legs": "bottom", "Shoes": "shoes", "Eyes": "eyes",
	"Mouth": "mouth", "Accessory": "accessory", "Aid": "aid",
}

## Teil je Ebene. Ohne Editor-Auswahl (look.parts) bleiben die P03-Namen – so bleibt alles abwärtskompatibel.
static func part_for(tid: String, look: Dictionary, layer: String, suffix: String = "") -> String:
	var slot: String = String(SLOT.get(layer, ""))
	var variant: String = String(look.get("parts", {}).get(slot, "")) if not slot.is_empty() else ""
	if variant.is_empty() and not slot.is_empty():
		variant = "none" if layer in ["Accessory", "Aid"] else CharacterParts.default_id(slot)
	if not variant.is_empty():
		var name: String = _name_for(layer, variant, suffix)
		if not name.is_empty() and CharacterTemplates.has_part(tid, name):
			return name
	return _fallback(layer, look, suffix)


## Teilname aus Ebene + Variante (+ „sit" für das sitzende Unterteil).
static func _name_for(layer: String, variant: String, suffix: String) -> String:
	match layer:
		"HairBack":
			return "hair_back_" + variant
		"HairFront":
			return "hair_front_" + variant
		"Top":
			return "top_" + variant
		"ArmBackSleeve", "ArmFrontSleeve":
			return "sleeve_" + variant
		"Legs":
			return ("bottom_sit_" if suffix == "sit" else "bottom_") + variant
		"Shoes":
			return "shoes_" + variant
		"Eyes":
			return "eyes_" + variant
		"Mouth":
			return "mouth_" + variant
		"Accessory":
			return "acc_" + variant
		"Aid":
			return "aid_" + variant
	return ""


static func _fallback(layer: String, look: Dictionary, suffix: String) -> String:
	match layer:
		"HairBack":
			return "hair_back_" + String(look.get("hair_style", "short"))
		"HairFront":
			return "hair_front_" + String(look.get("hair_style", "short"))
		"Legs":
			return "legs_sit" if suffix == "sit" else "legs_stand"
		"Top":
			return "torso"
		"ArmBackSleeve", "ArmFrontSleeve":
			return "arm_sleeve"
		"Shoes":
			return "shoes_stand"
		"Mouth":
			return "mouth_" + String(look.get("emotion", "happy"))
		_:
			return ""


## Zonenfarben einer Ebene (1…3), als Color-Array.
static func colors_for(look: Dictionary, layer: String) -> Array:
	if FIXED.has(layer):
		return _to_colors(FIXED[layer])
	if layer == "Head" or layer.ends_with("Skin") or layer.ends_with("Palm") \
			or layer.ends_with("Fingers") or layer.begins_with("Fingers"):
		return [Color(String(look.get("skin", "#ffd6bf")))]
	var slot: String = String(SLOT.get(layer, ""))
	var cols: Array = Array(look.get("colors", {}).get(slot, []))
	if cols.is_empty():
		# alte look-Schlüssel (Phase 03) weiterhin unterstützen
		var single: String = String(look.get({"top": "shirt", "bottom": "pants", "shoes": "shoes",
			"hair": "hair"}.get(slot, ""), ""))
		return [Color(single)] if single else [Color.WHITE]
	return _to_colors(cols)


static func _to_colors(hexes: Array) -> Array:
	var out: Array = []
	for h: Variant in hexes:
		out.append(Color(String(h)))
	return out


## Material mit den Zonenfarben setzen (Shader: Farbe = R·c1 + G·c2 + B·c3).
static func apply(item: CanvasItem, cols: Array) -> void:
	# Material wiederverwenden: der Editor färbt oft hintereinander um, da wäre ein neues
	# Material pro Klick Müll.
	var mat: ShaderMaterial = item.material as ShaderMaterial
	if mat == null or mat.shader != SHADER:
		mat = ShaderMaterial.new()
		mat.shader = SHADER
	for i: int in mini(3, cols.size()):
		mat.set_shader_parameter("zone%d" % (i + 1), cols[i])
	for i: int in range(cols.size(), 3):
		mat.set_shader_parameter("zone%d" % (i + 1), cols[0] if cols.size() > 0 else Color.WHITE)
	item.material = mat
	item.modulate = Color.WHITE


## Farbe einer Zone ändern (Editor: Palette klicken) – ohne das Material neu zu bauen.
static func set_zone(sprite: Sprite2D, index: int, col: Color) -> void:
	var mat: ShaderMaterial = sprite.material as ShaderMaterial
	if mat == null:
		return
	mat.set_shader_parameter("zone%d" % (index + 1), col)
