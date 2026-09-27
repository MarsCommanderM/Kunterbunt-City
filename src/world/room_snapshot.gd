class_name RoomSnapshot
extends RefCounted
## Raumzustand (P05-T07): Was steht wo? Wird beim Verlassen gespeichert und beim Betreten
## wieder aufgebaut. Figuren (die eigene + NPCs) und getragene Items gehören NICHT dazu.

const VERSION: int = 1


## Alle losen Items und Haustiere eines Raums einfrieren.
static func capture(room: Room) -> Array:
	var out: Array = []
	for it: ItemNode in Placement.all_items(room):
		if it is CharacterRig:
			continue                                   # Figuren werden frisch gespawnt
		if it is PetNode and it.has_meta("pet_id"):
			continue                                   # eigene Tiere laufen mit der Figur mit (P07: Raumwechsel)
		var e: Dictionary = {
			"id": String(it.def.id),
			"x": round(it.position.x * 10.0) / 10.0,
			"y": round(it.position.y * 10.0) / 10.0,
		}
		var host: Node = it.get_parent()
		while host != null and not (host is ItemNode) and host != room.ysort_root:
			host = host.get_parent()
		if host is ItemNode and host != it:             # liegt auf einem Tisch/Stuhl/Behälter
			e["on"] = String((host as ItemNode).def.id)
			e["x_rel"] = round(_rel_x(host as ItemNode, it) * 1000.0) / 1000.0
		if it.def.has_states() and it.state != String(it.def.states[0]):
			e["state"] = it.state                       # P04b-T10: Schrank offen, Lampe an …
		for k: String in ["water_t", "grow_t"]:         # P07-T07: Garten (Unix-Zeit → wächst weiter)
			if it.has_meta(k):
				e[k] = float(it.get_meta(k))
		out.append(e)
	out.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return String(a["id"]) < String(b["id"]))
	return out


## Zustand in einen (leeren) Raum setzen.
static func apply(room: Room, list: Array) -> int:
	var n: int = 0
	for e: Variant in list:
		var d: Dictionary = e
		var id := StringName(String(d.get("id", "")))
		if id == &"" or not ItemDB.has_item(id):
			continue
		if String(d.get("pet_id", "")) != "":
			continue                                   # alte Stände: eigene Tiere werden frisch gespawnt
		var it: ItemNode
		if d.has("on") and String(d["on"]) != "":
			var host: ItemNode = _find_by_id(room, StringName(String(d["on"])))
			it = ItemSpawner.on_item(host, id, float(d.get("x_rel", 0.0))) if host else null
		else:
			var def: ItemDefinition = ItemDB.get_item(id)
			if def != null and def.is_wall():
				it = ItemSpawner.on_wall(room, id, float(d.get("x", 0.0)), float(d.get("y", 0.0)))
			else:
				it = ItemSpawner.on_floor(room, id, float(d.get("x", 0.0)), float(d.get("y", 0.0)))
		if it == null:
			continue
		if d.has("state"):
			ItemStates.set_state(it, String(d["state"]), true)
		for k: String in ["water_t", "grow_t"]:
			if d.has(k):
				it.set_meta(k, float(d[k]))
		n += 1
	return n


## x_rel des Gastes relativ zur Fläche des Wirts (−0,5 … 0,5).
static func _rel_x(host: ItemNode, it: ItemNode) -> float:
	var r: Rect2 = host.local_rect()
	var w: float = r.size.x * (1.0 - 2.0 * host.def.surface_inset)
	if w <= 0.01:
		return 0.0
	return clampf((it.position.x - r.get_center().x) / w, -0.5, 0.5)


static func _find_by_id(room: Room, id: StringName) -> ItemNode:
	for it: ItemNode in Placement.all_items(room):
		if it.def.id == id:
			return it
	return null


## Alles im Raum löschen (für „Bereich zurücksetzen" 🪄).
static func clear(room: Room) -> void:
	for it: ItemNode in Placement.all_items(room):
		if it is CharacterRig:
			continue
		it.queue_free()
