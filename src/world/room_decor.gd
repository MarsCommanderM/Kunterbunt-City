class_name RoomDecor
extends RefCounted
## P07-T04: Tapete (Farbe + Muster) und Boden (Art + Farben) eines Raums – frei wählbar, ohne neue Bilder.
## Wand und Boden sind Zonen-Ebenen aus tools/make_rooms.py (Wand: 1 Tapete, 2 Leisten, 3 Paneel;
## Boden: 1 Grundton, 2 zweiter Ton, 3 Fugen). Der Shader zone_tint färbt sie wie Items ein.
## Ein Decor-Eintrag: {wall: [3 Hex], pattern: "", pattern_col: Hex, floor: "planks", floor_cols: [3 Hex]}.

const SHADER: Shader = preload("res://assets/shaders/zone_tint.gdshader")
const INK: Color = Color("3b2a2a")
const PATTERN_DIR: String = "res://assets/shaders/wallpapers/"
## Musterlänge in cm: 2048 px Kachel / (4 px/cm · 10) → jede Kachel endet auf einer ganzen Wiederholung (keine Naht).
const REPEAT_CM: float = 51.2

const PATTERNS: Array = ["", "stripes", "pinstripes", "dots", "checks", "flowers", "stars", "waves", "bricks", "tiles"]
const WALL_COLORS: Array = ["#f3e6d0", "#fbfaf7", "#f6d98a", "#f0b6c2", "#a9c3dd", "#dbe8d9", "#9fc3a0", "#b9a6d6",
	"#f09a55", "#e07a7a", "#6f8fb8", "#d8cfc2"]
const PATTERN_COLORS: Array = ["#ffffff", "#f6d98a", "#e07a7a", "#6f8fb8", "#5f8f6a", "#7a5ea8"]
const PANEL_COLORS: Array = ["#b9d7c0", "#fbfaf7", "#a9c3dd", "#f0b6c2", "#d4a86e", "#6d6f78"]
const FLOOR_PRESETS: Dictionary = {
	"planks": [["#d9a066", "#c98a4b", "#8a5a3c"], ["#e3c79a", "#d4b07c", "#8a6a4a"], ["#8a5e3f", "#74492f", "#4a3024"],
		["#e8e2d8", "#d8cfc2", "#a1887f"]],
	"tiles": [["#f5f3ee", "#dfe6ea", "#a9b3bd"], ["#f6d98a", "#f5f3ee", "#b89a55"], ["#a9c3dd", "#f5f3ee", "#6f8fb8"],
		["#c96a4a", "#b85c45", "#7a3a2a"], ["#2e3140", "#f5f3ee", "#6d6f78"]],
	"carpet": [["#a9c3dd", "#9ab5d0", "#6f8fb8"], ["#f0b6c2", "#e8a4b3", "#c1547a"], ["#9fc3a0", "#8fb592", "#5f8f6a"],
		["#d8cfc2", "#cabfb0", "#a1887f"], ["#b9a6d6", "#a893c9", "#7a5ea8"]],
	"concrete": [["#b8b8b8", "#a8a8a8", "#7a7a7a"], ["#c9c0b0", "#b8ae9c", "#8a8070"]],
	"grass": [["#8cc47a", "#7fb36e", "#5f8f4a"], ["#a6cf7c", "#94c06c", "#6f9a4a"]],
	"sand": [["#f1dca6", "#e6cc90", "#c9a86a"]],
}


## Standard-Einrichtung eines Raums (aus der Hintergrund-Datei), überschrieben mit dem, was das Kind gewählt hat.
static func merged(meta: Dictionary, chosen: Dictionary) -> Dictionary:
	var d: Dictionary = {"wall": ["#f3e6d0", "#ffffff", "#b9d7c0"], "pattern": "", "pattern_col": "#ffffff",
		"floor": "planks", "floor_cols": ["#d9a066", "#c98a4b", "#8a5a3c"]}
	d.merge(Dictionary(meta.get("decor", {})), true)
	d.merge(chosen, true)
	var kinds: Array = floor_kinds(meta)
	if not kinds.is_empty() and not kinds.has(String(d["floor"])):
		d["floor"] = kinds[0]
	return d


## Welche Bodenarten gibt es für diesen Raum (für jede Breite erzeugt)?
static func floor_kinds(meta: Dictionary) -> Array:
	var out: Array = []
	for k: String in FLOOR_PRESETS:
		if Dictionary(meta.get("floors", {})).has(k):
			out.append(k)
	return out


static func has_decor(meta: Dictionary) -> bool:
	return meta.has("layers") or meta.has("floors")


## Wand- und Boden-Ebene unter `parent` bauen (vorher Leeren). Koordinaten: Pixel des Hintergrunds.
static func build(parent: Node2D, meta: Dictionary, decor: Dictionary) -> void:
	for c: Node in parent.get_children():
		parent.remove_child(c)
		c.queue_free()
	var ppc: float = float(meta.get("px_per_cm", 4.0))
	for layer: Dictionary in Array(meta.get("layers", [])):
		if String(layer.get("kind", "")) != "wall":
			continue
		for t: Dictionary in Array(layer["tiles"]):
			parent.add_child(_sprite(t, float(layer.get("y_px", 0)), Array(decor["wall"]), String(decor.get("pattern", "")),
				String(decor.get("pattern_col", "#ffffff")), ppc))
	var floors: Dictionary = meta.get("floors", {})
	var fl: Dictionary = floors.get(String(decor.get("floor", "")), {})
	for t: Dictionary in Array(fl.get("tiles", [])):
		parent.add_child(_sprite(t, float(fl.get("y_px", 0)), Array(decor["floor_cols"]), "", "#ffffff", ppc))


static func _sprite(t: Dictionary, y_off: float, cols: Array, pattern: String, pattern_col: String, ppc: float) -> Sprite2D:
	var spr := Sprite2D.new()
	spr.texture = load(String(t["file"]))
	spr.centered = false
	spr.position = Vector2(float(t["x_px"]), float(t["y_px"]) + y_off)
	var m := ShaderMaterial.new()
	m.shader = SHADER
	m.set_shader_parameter("zone1", Color(String(cols[0])))
	m.set_shader_parameter("zone2", Color(String(cols[1])))
	m.set_shader_parameter("zone3", Color(String(cols[2])))
	m.set_shader_parameter("ink", INK)
	var tex: Texture2D = pattern_texture(pattern)
	m.set_shader_parameter("has_pattern", tex != null)
	if tex != null:
		m.set_shader_parameter("pattern_tex", tex)
		m.set_shader_parameter("pattern_col", Color(pattern_col))
		var w_px: float = float(t.get("w_px", spr.texture.get_width()))
		var h_px: float = float(t.get("h_px", spr.texture.get_height()))
		m.set_shader_parameter("pattern_scale", Vector2(w_px, h_px) / (REPEAT_CM * ppc))
	spr.material = m
	return spr


static func pattern_texture(pattern: String) -> Texture2D:
	if pattern.is_empty():
		return null
	var p: String = PATTERN_DIR + pattern + ".png"
	return load(p) if ResourceLoader.exists(p) else null
