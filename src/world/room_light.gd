class_name RoomLight
extends RefCounted
## P07-T05: Licht im Raum. Ein Licht-Schalter (home_light_switch) auf „aus" → der Raum wird dunkel (Nacht-Stimmung);
## eingeschaltete Lampen, Wandleuchten, Nachtlichter, Kamin, Feuer, Lichterketten leuchten dann als echte Lichter
## (PointLight2D, weicher Kreis). Kein Schalter im Raum = immer hell.

const DARK: Color = Color(0.3, 0.32, 0.48)
const SWITCH: String = "home_light_switch"
const SOURCES: Array = ["deco_lamp", "wall_sconce", "deco_nightlight", "garden_lights", "garden_torch", "garden_fire_bowl",
	"camp_lantern", "camp_campfire", "furn_fireplace", "elec_tv"]
const RADIUS_CM: float = 260.0


static func is_dark(room: Room) -> bool:
	for it: ItemNode in Placement.all_items(room):
		if String(it.def.id).begins_with(SWITCH) and it.state == "off":
			return true
	return false


static func is_source(it: ItemNode) -> bool:
	var id: String = String(it.def.id)
	for p: Variant in SOURCES:
		if id.begins_with(String(p)):
			return true
	return false


## Dunkelheit + Lichtquellen aktualisieren (nach Tippen, Ablegen, Raumwechsel).
static func apply(room: Room, cm: CanvasModulate) -> bool:
	var dark: bool = is_dark(room)
	if cm != null:
		cm.color = DARK if dark else Color.WHITE
	for it: ItemNode in Placement.all_items(room):
		if is_source(it):
			_glow(it, dark and it.state == "on")
	return dark


static func _glow(it: ItemNode, on: bool) -> void:
	var l: PointLight2D = it.get_node_or_null("Glow")
	if not on:
		if l != null:
			l.queue_free()
		return
	if l != null:
		return
	l = PointLight2D.new()
	l.name = "Glow"
	l.texture = _texture()
	l.texture_scale = RADIUS_CM * 2.0 / 256.0
	l.color = Color(1.0, 0.86, 0.6)
	l.energy = 1.1
	l.position = Vector2(0.0, -it.def.height_cm * 0.75)
	it.add_child(l)


## Weicher Licht-Kreis (je Licht neu – keine statische Ressource, die das Beenden stört).
static func _texture() -> Texture2D:
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 1))
	g.set_color(1, Color(1, 1, 1, 0))
	var t := GradientTexture2D.new()
	t.gradient = g
	t.fill = GradientTexture2D.FILL_RADIAL
	t.fill_from = Vector2(0.5, 0.5)
	t.fill_to = Vector2(1.0, 0.5)
	t.width = 256
	t.height = 256
	return t
