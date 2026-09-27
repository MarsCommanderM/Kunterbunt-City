class_name CharacterLook
extends RefCounted
## P04-T04: Aussehen einer Figur → Teilname + Zonenfarben je Ebene.
## Der Rig kennt nur Ebenen-Namen; WELCHES Teil (Variante) und WELCHE Farben (Zonen) sie tragen,
## entscheidet diese Klasse. Dadurch bleibt character_rig.gd schlank und der Editor tauscht nur
## `look` aus (Schablone + Hautton + Teile + Farben).

const SHADER: Shader = preload("res://assets/shaders/zone_tint.gdshader")

## P04b: Konturfarbe der Figuren (dunkles Braun statt Schwarz – Stil „großer Kopf“).
const INK: Color = Color("#3b2a2a")
## Wangenrot = Haut, zu diesem Rosa hin gemischt.
const BLUSH: Color = Color("#ff8c8c")
const HAIR_ACCENT: String = "#ef6f9c"   ## Haargummi/Spange, falls nicht gewählt

## Farben, die der Spieler nicht wählt (Mund ist fertig koloriert, Augen: Standard-Augenfarbe).
const FIXED: Dictionary = {
	"Eyes": ["#3a2620", "#ffffff"],      # Zone 1 = Augenfarbe (wählbar über colors.eyes), Zone 2 = Glanz
	"Mouth": ["#b0424f", "#ff8fa3"],     # Zone 1 = Mund, Zone 2 = Zunge
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
	if not variant.is_empty():
		variant = CharacterParts.resolve(slot, variant)      # alte IDs aus Speicherständen
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


## Zonenfarben einer Ebene (Shader-Zonen 1…3), als Color-Array.
## Die Zuordnung Editor-Farbe → Shader-Zone hängt von der Ebene ab (P04b):
##   Haut-Ebenen: [Haut, Wangenrot] · Augen: [Augenfarbe, Weiß, Haarfarbe (Brauen)]
##   Haare: [Haar, Glanz, Haargummi] · Kleidung/Beine/Schuhe: [Farbe 1, Farbe 2, Haut]
static func colors_for(look: Dictionary, layer: String) -> Array:
	var skin: Color = Color(String(look.get("skin", "#ffd6bf")))
	if layer == "Mouth":
		return _to_colors(FIXED["Mouth"])
	if layer == "Eyes":
		var eye: Array = Array(look.get("colors", {}).get("eyes", []))
		return [Color(String(eye[0])) if not eye.is_empty() else Color(String(FIXED["Eyes"][0])),
			Color(String(FIXED["Eyes"][1])), hair_color(look)]
	if layer == "Head" or layer.ends_with("Skin") or layer.ends_with("Palm") \
			or layer.ends_with("Fingers") or layer.begins_with("Fingers"):
		return [skin, skin.lerp(BLUSH, 0.38)]
	var slot: String = String(SLOT.get(layer, ""))
	var cols: Array = _to_colors(Array(look.get("colors", {}).get(slot, [])))
	if cols.is_empty():
		# alte look-Schlüssel (Phase 03) weiterhin unterstützen
		var single: String = String(look.get({"top": "shirt", "bottom": "pants", "shoes": "shoes",
			"hair": "hair"}.get(slot, ""), ""))
		cols = [Color(single)] if single else [Color.WHITE]
	if slot == "hair":
		var h: Color = cols[0]
		return [h, h.lerp(Color(0.97, 0.93, 0.86), 0.42),
			cols[1] if cols.size() > 1 else Color(HAIR_ACCENT)]
	if slot in ["top", "bottom", "shoes", "aid"]:
		return [cols[0], cols[1] if cols.size() > 1 else cols[0], skin]
	return cols


## Haarfarbe der Figur (Editor-Farbe oder alter Schlüssel „hair“).
static func hair_color(look: Dictionary) -> Color:
	var cols: Array = Array(look.get("colors", {}).get("hair", []))
	if not cols.is_empty():
		return Color(String(cols[0]))
	return Color(String(look.get("hair", "#6b4a36")))


static func _to_colors(hexes: Array) -> Array:
	var out: Array = []
	for h: Variant in hexes:
		out.append(Color(String(h)))
	return out


## Material mit den Zonenfarben setzen (Shader: Farbe = R·c1 + G·c2 + B·c3 + Rest·Tinte).
static func apply(item: CanvasItem, cols: Array, ink: Color = INK) -> void:
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
	mat.set_shader_parameter("ink", ink)
	item.material = mat
	item.modulate = Color.WHITE


## Farbe einer Zone ändern (Editor: Palette klicken) – ohne das Material neu zu bauen.
static func set_zone(sprite: Sprite2D, index: int, col: Color) -> void:
	var mat: ShaderMaterial = sprite.material as ShaderMaterial
	if mat == null:
		return
	mat.set_shader_parameter("zone%d" % (index + 1), col)
