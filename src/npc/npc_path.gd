class_name NpcPath
extends RefCounted
## P08-T03: Wege im Raum – ohne NavMesh. Der Boden ist ein Band (hinten … vorne); gelaufen wird darin.
## Steht ein großes Möbel (Hindernis) zwischen Start und Ziel und würde die Figur HINTER/DURCH ihm laufen,
## geht der Weg über die vordere „Laufspur" (vor allen Möbeln) und erst am Ziel wieder in die Tiefe.
## Ziele außerhalb des Raums werden in den Raum geklemmt → eine Figur verlässt ihn nie.

const OBSTACLE_MIN_H_CM: float = 60.0      ## ab dieser Höhe verdeckt/blockiert ein Möbel den Weg
const EDGE_CM: float = 30.0                ## Abstand zum linken/rechten Raumrand
const LANE_FRAC: float = 0.92              ## Laufspur: 92 % der Bodentiefe (vor fast allem)


static func clamp_to_room(room: Room, p: Vector2) -> Vector2:
	var q: Vector2 = room.floor_band.clamp_point(p)
	q.x = clampf(q.x, EDGE_CM, maxf(EDGE_CM, room.width_cm - EDGE_CM))
	return q


static func is_obstacle(it: ItemNode) -> bool:
	return it.get_parent() != null and it.get_parent().name == "YSortRoot" and it.def.hold == "none" \
		and not (it is CharacterRig) and not (it is PetNode) and it.def.height_cm >= OBSTACLE_MIN_H_CM \
		and not it.def.is_rug() and not it.def.is_wall()


## Hindernisse zwischen a und b, vor denen die Figur (in ihrer Tiefe) nicht vorbeikäme.
static func blockers(room: Room, a: Vector2, b: Vector2) -> Array:
	var out: Array = []
	var x0: float = minf(a.x, b.x)
	var x1: float = maxf(a.x, b.x)
	var depth: float = minf(a.y, b.y)
	for it: ItemNode in Placement.all_items(room):
		if not is_obstacle(it):
			continue
		var half: float = it.def.width_cm * 0.5 * it.scale.x
		if it.position.x + half < x0 or it.position.x - half > x1:
			continue
		if it.position.y >= depth - 4.0:                    # Möbel steht gleich tief oder weiter vorn → im Weg
			out.append(it)
	return out


## Wegpunkte von a nach b (a selbst nicht enthalten, b immer als letzter Punkt, alles im Raum).
static func route(room: Room, a: Vector2, b: Vector2) -> Array:
	var goal: Vector2 = clamp_to_room(room, b)
	var bl: Array = blockers(room, a, goal)
	if bl.is_empty():
		return [goal]
	var lane: float = lerpf(room.floor_band.back_y_cm, room.floor_band.front_y_cm, LANE_FRAC)
	for it: ItemNode in bl:                                 # Spur liegt sicher vor dem vordersten Hindernis
		lane = maxf(lane, minf(it.position.y + 6.0, room.floor_band.front_y_cm))
	return [clamp_to_room(room, Vector2(a.x, lane)), clamp_to_room(room, Vector2(goal.x, lane)), goal]
