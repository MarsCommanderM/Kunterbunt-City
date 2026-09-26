class_name PetStage
extends Control
## Vorschau eines Haustiers (P04-T09): Sprite aus assets/sprites/pets, eingefärbt über die drei
## Zonen des Shaders (Fell, Bauch/Muster, Halsband). Größe = Maßstab-Tabelle, nie das Sprite.

var _spr: Sprite2D
var species_id: String = ""
var colors: Array = ["#d9a066", "#f7e6c8", "#e2574c"]


func _ready() -> void:
	clip_contents = true
	_ensure()


func _ensure() -> void:
	if _spr != null:
		return
	_spr = Sprite2D.new()
	_spr.centered = false
	add_child(_spr)


func show_pet(sid: String, cols: Array = []) -> void:
	species_id = sid
	_ensure()
	if not cols.is_empty():
		colors = cols
	var def: ItemDefinition = ItemDB.get_item(sid)
	if def == null:
		return
	_spr.texture = load(def.sprite_path)
	_layout()
	_recolor()


func _layout() -> void:
	if _spr == null or _spr.texture == null:
		return
	var def: ItemDefinition = ItemDB.get_item(species_id)
	if def == null:
		return
	var tex: Vector2 = _spr.texture.get_size()
	# Skalierung aus der TEXTUR (px) – die cm-Größe steckt schon im Item, nicht im Bild.
	var sc: float = minf(size.y * 0.94 / maxf(tex.y, 1.0), size.x * 0.98 / maxf(tex.x, 1.0))
	_spr.scale = Vector2(sc, sc)
	_spr.position = Vector2(size.x * 0.5 - tex.x * sc * 0.5, size.y - tex.y * sc - size.y * 0.02)


func _recolor() -> void:
	var cols: Array = []
	for c: Variant in colors:
		cols.append(Color(String(c)))
	CharacterLook.apply(_spr, cols)


func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED:
		_layout()
	elif what == NOTIFICATION_READY:
		_layout()
