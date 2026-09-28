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
		if it.has_meta("transient"):
			continue                                   # P09: nur kurz da (der Bus an der Haltestelle)
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
			e["on_x"] = round(room.ysort_root.to_local((host as ItemNode).global_position).x * 10.0) / 10.0
			e["x_rel"] = round(_rel_x(host as ItemNode, it) * 1000.0) / 1000.0
		if it.def.has_states() and it.state != String(it.def.states[0]):
			e["state"] = it.state                       # P04b-T10: Schrank offen, Lampe an …
		for k: String in ["water_t", "grow_t"]:         # P07-T07: Garten (Unix-Zeit → wächst weiter)
			if it.has_meta(k):
				e[k] = float(it.get_meta(k))
		out.append(e)
	out.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return String(a["id"]) < String(b["id"]))
	return out


## Zustand in einen (leeren) Raum setzen. Erst alles auf Boden/Wand, dann in Durchgängen die Dinge AUF anderen
## (Kasse auf der Theke, Apfel auf dem Teller auf dem Tisch) – vorher gingen Gäste verloren, deren ID alphabetisch
## vor der ihres Wirts lag (P09: Kasse „shop_cash_register" < Theke „shop_checkout").
static func apply(room: Room, list: Array) -> int:
	var n: int = 0
	var pending: Array = []
	for e: Variant in list:
		var d: Dictionary = e
		var id := StringName(String(d.get("id", "")))
		if id == &"" or not ItemDB.has_item(id) or String(d.get("pet_id", "")) != "":
			continue                                   # unbekannt / alte Stände: eigene Tiere werden frisch gespawnt
		if d.has("on") and String(d["on"]) != "":
			pending.append(d)
			continue
		var def: ItemDefinition = ItemDB.get_item(id)
		var it: ItemNode
		if def != null and def.is_wall():
			it = ItemSpawner.on_wall(room, id, float(d.get("x", 0.0)), float(d.get("y", 0.0)))
		else:
			it = ItemSpawner.on_floor(room, id, float(d.get("x", 0.0)), float(d.get("y", 0.0)))
		n += _restore(it, d)
	for _pass: int in 4:                               # Stapel: Teller auf Tisch, Apfel auf Teller …
		var left: Array = []
		for d: Dictionary in pending:
			var host: ItemNode = _find_host(room, StringName(String(d["on"])), d)
			if host == null:
				left.append(d)
				continue
			n += _restore(ItemSpawner.on_item(host, StringName(String(d["id"])), float(d.get("x_rel", 0.0))), d)
		if left.size() == pending.size():
			break
		pending = left
	return n


static func _restore(it: ItemNode, d: Dictionary) -> int:
	if it == null:
		return 0
	if d.has("state"):
		ItemStates.set_state(it, String(d["state"]), true)
	for k: String in ["water_t", "grow_t"]:
		if d.has(k):
			it.set_meta(k, float(d[k]))
	return 1


## Wirt mit dieser ID – bei mehreren gleichen (zwei Theken) der an der gespeicherten Stelle (on_x).
static func _find_host(room: Room, id: StringName, d: Dictionary) -> ItemNode:
	var best: ItemNode = null
	var bd: float = INF
	for it: ItemNode in Placement.all_items(room):
		if it.def.id != id:
			continue
		var dd: float = absf(room.ysort_root.to_local(it.global_position).x - float(d.get("on_x", 0.0))) if d.has("on_x") else 0.0
		if dd < bd:
			bd = dd
			best = it
	return best


## x_rel des Gastes relativ zur Fläche des Wirts (−0,5 … 0,5).
static func _rel_x(host: ItemNode, it: ItemNode) -> float:
	var r: Rect2 = host.local_rect()
	var w: float = r.size.x * (1.0 - 2.0 * host.def.surface_inset)
	if w <= 0.01:
		return 0.0
	return clampf((it.position.x - r.get_center().x) / w, -0.5, 0.5)


## Alles im Raum löschen (für „Bereich zurücksetzen" 🪄).
static func clear(room: Room) -> void:
	for it: ItemNode in Placement.all_items(room):
		if it is CharacterRig:
			continue
		it.queue_free()
