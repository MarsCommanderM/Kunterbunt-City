class_name PetLook
extends RefCounted
## P04b-T07: Haustier einfärben – drei Farbzonen (Fell, Bauch, Halsband) + Fellmuster (Flecken, Streifen,
## Punkte, Spitzen). Das Muster liegt nur auf dem Fell (Zone 1) und skaliert mit dem Tier.

const DIR: String = "res://assets/shaders/patterns/"
const REPEAT: Dictionary = {"patches": 2.2, "stripes": 3.0, "spots": 2.4, "tips": 1.0}
const DARKEN: Dictionary = {"stripes": 0.32, "spots": 0.42, "tips": 0.45}


## cols: Farben als String oder Color (Fell, Bauch, Halsband); pattern: Muster-ID aus data/pets/species.json.
static func apply(item: CanvasItem, cols: Array, pattern: String = "plain") -> void:
	var c: Array = []
	for x: Variant in cols:
		c.append(x if x is Color else Color(String(x)))
	CharacterLook.apply(item, c)
	var mat: ShaderMaterial = item.material as ShaderMaterial
	var path: String = DIR + pattern + ".png"
	var on: bool = pattern != "plain" and not pattern.is_empty() and ResourceLoader.exists(path) and not c.is_empty()
	mat.set_shader_parameter("has_pattern", on)
	if not on:
		return
	var fur: Color = c[0]
	var col: Color = (c[1] if c.size() > 1 else fur.lightened(0.5)) if pattern == "patches" \
		else fur.darkened(float(DARKEN.get(pattern, 0.35)))
	mat.set_shader_parameter("pattern_tex", load(path))
	mat.set_shader_parameter("pattern_col", col)
	var rep: float = float(REPEAT.get(pattern, 2.0))
	var aspect: float = 1.0
	if item is Sprite2D and (item as Sprite2D).texture != null:
		var sz: Vector2 = (item as Sprite2D).texture.get_size()
		aspect = sz.y / maxf(sz.x, 1.0)
	mat.set_shader_parameter("pattern_scale", Vector2(rep, rep * aspect) if pattern != "tips" else Vector2.ONE)
