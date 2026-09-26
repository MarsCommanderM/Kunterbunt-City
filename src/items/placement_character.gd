class_name PlacementCharacter
extends RefCounted
## Ziele mit Figuren (Tech-Spec §4.1-4.3, P03-T04/T05/T07). Kommen VOR Behälter/Fläche/Boden:
##   Mund (Essen ≤ 15 cm am Mund) → Hand (Griffpunkt ≤ 25 cm an einer freien Hand) → Sitz-/Liegeplatz.
## Figuren werden per Duck-Typing erkannt (hand_slots(), mouth_global(), eat()) – auch das Mädchen-Sprite.

const HAND_SNAP_CM: float = 25.0
const MOUTH_SNAP_CM: float = 15.0
const SEAT_ITEM_SNAP_CM: float = 12.0
## Nur Figuren, Tiere und Spielzeug setzen sich hin – Geschirr & Co. nutzen die Abstellfläche (Hocker).
const SEAT_CATEGORIES: Array[String] = ["character", "pet", "toy"]


static func find(room: Room, item: ItemNode, pivot: Vector2, _pointer: Vector2) -> Placement.Target:
	var items: Array[ItemNode] = Placement.all_items(room)
	var t: Placement.Target = _mouth_target(items, item, pivot)
	if t == null:
		t = _hand_target(items, item, pivot)
	if t == null:
		t = _seat_target(items, item, pivot)
	return t


## Griffpunkt des Items (global), wenn sein Pivot bei pivot läge.
static func grip_global(item: ItemNode, pivot: Vector2) -> Vector2:
	var g: Vector2 = item.def.grip if item.def.grip.x >= 0.0 else Vector2(0.5, 0.5)
	return pivot + (g - item.def.pivot) * item.draw_size() * item.global_scale


static func _is_free_rig(c: ItemNode, item: ItemNode) -> bool:
	return c != item and not item.is_ancestor_of(c) and c.has_method("hand_slots") and c.is_visible_in_tree()


static func _mouth_target(items: Array[ItemNode], item: ItemNode, pivot: Vector2) -> Placement.Target:
	if item.def.category != "food":
		return null
	var center: Vector2 = pivot + (Vector2(0.5, 0.5) - item.def.pivot) * item.draw_size() * item.global_scale
	for c: ItemNode in items:
		if not _is_free_rig(c, item) or not c.has_method("mouth_global"):
			continue
		var m: Vector2 = c.mouth_global()
		if center.distance_to(m) <= MOUTH_SNAP_CM * c.global_scale.y:
			var t := Placement.Target.new()
			t.kind = &"mouth"
			t.node = c
			t.parent = c
			t.global_pos = m - (center - pivot)
			t.global_scale = c.global_scale.y
			return t
	return null


static func _hand_target(items: Array[ItemNode], item: ItemNode, pivot: Vector2) -> Placement.Target:
	if item.def.hold == "none" or item.def.category == "character":
		return null
	var grip: Vector2 = grip_global(item, pivot)
	var best: Dictionary = {}
	var best_d: float = INF
	var best_rig: ItemNode = null
	for c: ItemNode in items:
		if not _is_free_rig(c, item):
			continue
		for s: Dictionary in c.hand_slots():
			var two: bool = int(s["index"]) == 2
			if two != (item.def.hold == "two_hands"):
				continue
			var d: float = (s["global"] as Vector2).distance_to(grip) - (0.5 if int(s["index"]) == 0 else 0.0)
			if d <= HAND_SNAP_CM * c.global_scale.y and d < best_d:
				best_d = d
				best = s
				best_rig = c
	if best_rig == null:
		return null
	var slot: Node2D = best["slot"]
	var t := Placement.Target.new()
	t.kind = &"hand"
	t.node = best_rig
	t.parent = slot
	t.slot = int(best["index"])
	t.global_scale = slot.global_scale.y
	# Position mit der späteren Slot-Drehung (Item aufrecht + Haltewinkel) → Griff genau in der Hand
	var rot: float = slot.global_rotation
	if best_rig.has_method("hold_rotation_for"):
		rot = best_rig.hold_rotation_for(int(best["index"]), item)
	t.global_pos = slot.global_position + (CharacterRig.grip_local(item) * t.global_scale).rotated(rot)
	return t


static func _seat_target(items: Array[ItemNode], item: ItemNode, pivot: Vector2) -> Placement.Target:
	if not SEAT_CATEGORIES.has(item.def.category) or item.def.has_seat() or item.def.has_surface():
		return null
	var is_char: bool = item.def.category == "character"
	if is_char and not item.has_method("hip_offset"):
		return null                          # fertig gemalte Figur kann (noch) nicht sitzen
	# Figur: Becken zählt (stehend beim Tragen); Item: Pivot (Unterkante)
	var probe: Vector2 = pivot
	if is_char and item.has_method("hip_offset"):
		probe = pivot + item.hip_offset() * item.global_scale.y
	var best_host: ItemNode = null
	var best_i: int = -1
	var best_d: float = INF
	for host: ItemNode in items:
		if host == item or item.is_ancestor_of(host) or not host.def.has_seat() or not host.is_visible_in_tree():
			continue
		var radius: float = Seats.CHARACTER_SNAP_CM if is_char else Seats.slot_width_global(host) * 0.5
		var i: int = Seats.free_index_near(host, probe, maxf(radius, SEAT_ITEM_SNAP_CM) * host.global_scale.y, item)
		if i < 0:
			continue
		var d: float = Seats.point_global(host, i).distance_to(probe)
		if d < best_d:
			best_d = d
			best_host = host
			best_i = i
	if best_host == null:
		return null
	var t := Placement.Target.new()
	t.kind = &"seat"
	t.node = best_host
	t.parent = best_host.on_top_root
	t.slot = best_i
	t.global_pos = Seats.point_global(best_host, best_i)
	t.global_scale = best_host.global_scale.y
	if is_char and item.has_method("hip_offset"):
		# Der Knoten-Ursprung einer Figur sind die Füße: versetzt ablegen, damit die HÜFTE auf dem
		# Sitzpunkt sitzt (sonst steht die Figur mit den Füßen auf der Sitzfläche).
		t.global_pos -= item.hip_offset() * t.global_scale
	return t
