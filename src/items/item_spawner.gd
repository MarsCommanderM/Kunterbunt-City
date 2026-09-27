class_name ItemSpawner
extends RefCounted
## Stellt Items in einen Raum – exakt mit denselben Regeln wie ein Drop (Pivot auf der Fläche, Tiefen-Faktor).


static func make(id: StringName) -> ItemNode:
	var def: ItemDefinition = ItemDB.get_item(id)
	if def == null:
		return null
	return PetNode.create_pet(def) if def.category == "pet" else ItemNode.create(def)


## Figur aus Schablone (toddler/kid/adult) oder fertiges Sprite (char_girl_01) auf den Boden.
static func character_on_floor(room: Room, tid: String, x_cm: float, depth_cm: float, look: Dictionary = {}) -> ItemNode:
	var c: ItemNode
	if tid.begins_with("char_"):
		c = SpriteCharacter.create_sprite_character(tid)
	else:
		c = CharacterRig.create_character(tid, look)
	room.ysort_root.add_child(c)
	var p: Vector2 = room.floor_band.clamp_point(Vector2(x_cm, depth_cm))
	c.position = p
	c.scale = Vector2.ONE * room.floor_band.depth_factor(p.y)
	c.on_placed()
	return c


## Auf den Boden an x, Tiefe y (cm).
static func on_floor(room: Room, id: StringName, x_cm: float, depth_cm: float) -> ItemNode:
	var it: ItemNode = make(id)
	if it == null:
		return null
	room.ysort_root.add_child(it)
	var p: Vector2 = room.floor_band.clamp_point(Vector2(x_cm, depth_cm))
	it.position = p
	it.scale = Vector2.ONE * room.floor_band.depth_factor(p.y)
	return it


## Auf eine Raum-Oberfläche (Arbeitsplatte, Regal).
static func on_surface(room: Room, id: StringName, surface_id: StringName, x_cm: float) -> ItemNode:
	var s: Surface = room.get_surface(surface_id)
	var it: ItemNode = make(id)
	if it == null or s == null:
		return it
	room.ysort_root.add_child(it)
	it.position = Vector2(x_cm, s.top_y())
	it.scale = Vector2.ONE * s.depth_factor()
	return it


## Auf ein Item mit Fläche (Tisch) oder als Stapel obendrauf. x_rel: −0,5 … 0,5 der Flächenbreite.
static func on_item(host: ItemNode, id: StringName, x_rel: float = 0.0, stack: bool = false) -> ItemNode:
	var it: ItemNode = make(id)
	if it == null:
		return null
	host.on_top_root.add_child(it)
	var r: Rect2 = host.local_rect()
	var bottom: float = (1.0 - host.def.pivot.y) * host.draw_size().y
	var h: float = host.draw_size().y if stack else host.def.surface_local_h()
	var w: float = r.size.x * (1.0 - 2.0 * host.def.surface_inset)
	it.position = Vector2(r.get_center().x + (0.0 if stack else x_rel * w), bottom - h)
	return it


## In den nächsten freien Behälter-Platz.
static func into_container(container: ItemNode, id: StringName) -> ItemNode:
	var slot: int = container.free_slot()
	if slot < 0:
		return null
	var it: ItemNode = make(id)
	container.contents_root.add_child(it)
	it.slot_index = slot
	container.relayout_contents()
	return it


## P07: An die Wand hängen (top = Oberkante in cm, negativ = über der Bodenlinie).
static func on_wall(room: Room, id: StringName, x_cm: float, top_cm: float) -> ItemNode:
	var it: ItemNode = make(id)
	if it == null:
		return null
	room.ysort_root.add_child(it)
	it.position = Placement.wall_point(room, it, Vector2(x_cm, top_cm))
	it.scale = Vector2.ONE
	return it


## Irgendein Item sinnvoll in den Raum stellen: Wand-Items auf gute Höhe (Fenster-Unterkante 90 cm, Bilder
## mittig auf 150 cm), alles andere auf den Boden in die Tiefe depth_cm.
static func place(room: Room, id: StringName, x_cm: float, depth_cm: float) -> ItemNode:
	var def: ItemDefinition = ItemDB.get_item(id)
	if def != null and def.is_wall():
		var h: float = def.height_cm
		var top: float = -(WALL_SILL_CM + h) if def.catalog in ["windows", "curtains"] else -(WALL_EYE_CM + h * 0.5)
		if def.catalog == "curtains":
			top = -(WALL_SILL_CM + h * 0.5 + 60.0)
		return on_wall(room, id, x_cm, top)
	return on_floor(room, id, x_cm, depth_cm)


const WALL_SILL_CM: float = 90.0     ## Fensterbank-Höhe
const WALL_EYE_CM: float = 150.0     ## Bilder/Poster: Mitte auf Augenhöhe Erwachsener

