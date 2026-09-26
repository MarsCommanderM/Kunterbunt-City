class_name Seats
extends RefCounted
## Sitz- und Liegeplätze (Tech-Spec §4.3, P03-T05). Ein Möbel mit seat_h_cm hat 1…n Plätze nebeneinander.
## Belegt ist ein Platz, wenn unter OnTop ein Item/eine Figur mit slot_index = Platz liegt.

const CHARACTER_SNAP_CM: float = 30.0   ## Becken innerhalb 30 cm → rastet ein


## Lokale Position (im Möbel, unskaliert) von Platz i: auf Sitzhöhe, gleichmäßig über 70 % der Breite verteilt.
static func point_local(host: ItemNode, i: int) -> Vector2:
	var r: Rect2 = host.local_rect()
	var n: int = maxi(1, host.def.seat_slots)
	var usable: float = r.size.x * (0.7 if n > 1 else 0.0)
	var x: float = r.get_center().x + (float(i) + 0.5) / n * usable - usable * 0.5
	var bottom: float = (1.0 - host.def.pivot.y) * host.draw_size().y
	return Vector2(x, bottom - host.def.seat_h_cm)


static func point_global(host: ItemNode, i: int) -> Vector2:
	return host.on_top_root.to_global(point_local(host, i))


static func occupant(host: ItemNode, i: int) -> ItemNode:
	for c: Node in host.on_top_root.get_children():
		if c is ItemNode and (c as ItemNode).slot_index == i:
			return c
	return null


static func free_index_near(host: ItemNode, p: Vector2, radius: float, except: ItemNode = null) -> int:
	var best: int = -1
	var best_d: float = radius
	for i: int in host.def.seat_slots:
		var o: ItemNode = occupant(host, i)
		if o != null and o != except:
			continue
		var d: float = point_global(host, i).distance_to(p)
		if d <= best_d:
			best_d = d
			best = i
	return best


## Breite eines Platzes (global) – Items (Teddy) rasten ein, wenn ihr Pivot darüber liegt.
static func slot_width_global(host: ItemNode) -> float:
	return host.local_rect().size.x * (0.7 / maxi(1, host.def.seat_slots) if host.def.seat_slots > 1 else 0.6) * host.global_scale.x


## Sitzhöhe des Platzes, auf dem das Item sitzt (cm über Boden, unskaliert) – 0 = keiner.
static func seat_height_of(item: ItemNode) -> float:
	var host: ItemNode = seat_host_of(item)
	return host.def.seat_h_cm if host else 0.0


## Sitzt/liegt das Item auf einem Platz? → Möbel, sonst null.
static func seat_host_of(item: ItemNode) -> ItemNode:
	var p: Node = item.get_parent()
	if p and p.name == "OnTop" and p.get_parent() is ItemNode and (p.get_parent() as ItemNode).def.has_seat() and item.slot_index >= 0:
		return p.get_parent()
	return null
