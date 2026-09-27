class_name Placement
extends RefCounted
## Wohin fällt ein losgelassenes Item? (Tech-Spec §4.1, P02-T05/T06/T07)
## Priorität: Mund → Hand → Sitzplatz (PlacementCharacter, Phase 03) → Behälter (offen, unter dem Finger)
## → Oberfläche/Stapel unter dem Item → Bodenband.

const SNAP_CM: float = 10.0           ## Pivot darf so weit UNTER einer Fläche sein und rastet trotzdem ein
const TABLE_MAX_H_CM: float = 60.0    ## Regel S-11: auf Tische/Regale nur Dinge ≤ 60 cm
const STACK_MAX: int = 8
const FRONT_OF_SURFACE_CM: float = 15.0
const MAX_FALL_S: float = 0.4
const NOT_ON_SURFACES: Array[String] = ["furniture", "fixture", "character", "zoo_animal"]


class Target:
	var kind: StringName = &"floor"   ## floor | surface | item_surface | stack | container | hand | seat | mouth
	var parent: Node                  ## neuer Eltern-Node
	var global_pos: Vector2           ## Ziel-Pivot (global, cm)
	var global_scale: float = 1.0     ## Ziel-Skalierung (global)
	var node: Object                  ## Surface / ItemNode (Ziel)
	var slot: int = -1
	var rejected_reason: String = ""  ## gesetzt, wenn das Wunschziel abgelehnt wurde


## pivot = gewünschte Pivot-Position (global), pointer = Finger/Maus (global).
static func find_target(room: Room, item: ItemNode, pivot: Vector2, pointer: Vector2) -> Target:
	if item.def.is_wall():
		return _wall_target(room, item, pivot)          # P07: hängt, wo man es loslässt
	if item.def.is_rug():
		return _floor_target(room, pivot)               # P07: Teppich nie auf Tisch/Stuhl
	var items: Array[ItemNode] = all_items(room)      # einmal sammeln (vorher 3× je Suche)
	var ch: Target = PlacementCharacter.find(room, item, pivot, pointer, items)
	if ch:
		return ch
	var c: Target = _container_target(room, item, pointer, items)
	if c:
		return c
	var best_y: float = INF
	var best: Target = null
	var floor_t: Target = _floor_target(room, pivot)
	var min_y: float = pivot.y - SNAP_CM
	# Raum-Oberflächen
	for s: Surface in room.get_surfaces():
		var y: float = s.top_y()
		if s.contains_x(pivot.x) and y >= min_y and y < best_y:
			var t := Target.new()
			t.kind = &"surface"
			t.node = s
			t.parent = room.ysort_root
			t.global_pos = Vector2(pivot.x, y)
			t.global_scale = s.depth_factor()
			best_y = y
			best = t
	# Items mit Fläche (Tisch) und Stapel-Spitzen
	var stackable: bool = item.def.is_stackable()
	for other: ItemNode in items:
		var surf: bool = other.def.has_surface()
		var stack: bool = stackable and other.def.is_stackable()
		if not (surf or stack):              # billige Prüfung zuerst: die meisten Items sind weder Tisch noch Stapel
			continue
		if other == item or item.is_ancestor_of(other) or not other.is_visible_in_tree():
			continue
		var kinds: Array[StringName] = []
		if surf:
			kinds.append(&"item_surface")
		if stack and not other.has_stacked_child():
			kinds.append(&"stack")
		for k: StringName in kinds:
			var y2: float = other.top_global_y(k == &"stack")
			var xr: Vector2 = other.surface_x_range() if k == &"item_surface" else \
				Vector2(other.global_rect().position.x, other.global_rect().end.x)
			if pivot.x >= xr.x and pivot.x <= xr.y and y2 >= min_y and y2 < best_y:
				var t2 := Target.new()
				t2.kind = k
				t2.node = other
				t2.parent = other.on_top_root
				t2.global_pos = Vector2(pivot.x if k == &"item_surface" else other.global_position.x, y2)
				t2.global_scale = other.global_scale.y
				best_y = y2
				best = t2
	# Im Bodenband steht das Item schon auf dem Boden: ein Ziel knapp darunter (≤ SNAP) gewinnt trotzdem,
	# weiter vorne liegende Dinge nicht. Darüber (in der Luft) fällt es auf das Höchste darunter.
	var in_band: bool = pivot.y >= room.floor_band.back_y_cm
	if best == null or floor_t.global_pos.y + (SNAP_CM if in_band else 0.0) < best_y:
		return floor_t
	var reason: String = rejection_reason(room, item, best)
	if reason.is_empty():
		return best
	# passt nicht → federt auf den Boden vor der Fläche
	var depth: float = room.floor_band.back_y_cm + FRONT_OF_SURFACE_CM
	if best.node is Surface:
		depth = (best.node as Surface).depth_y_cm + FRONT_OF_SURFACE_CM
	elif best.node is ItemNode:
		depth = _floor_depth_of(room, best.node as ItemNode) + FRONT_OF_SURFACE_CM
	var f: Target = _floor_target(room, Vector2(pivot.x, depth))
	f.rejected_reason = reason
	return f


## Leer = passt. Sonst Grund (für Tests, Debug und das „Nein“-Geräusch).
static func rejection_reason(room: Room, item: ItemNode, t: Target) -> String:
	var d: ItemDefinition = item.def
	if t.kind == &"floor":
		return ""
	if NOT_ON_SURFACES.has(d.category) or d.has_surface():
		return "%s gehört auf den Boden" % d.id
	if t.kind == &"stack":
		var other: ItemNode = t.node
		if other.stack_depth_below() + item.stack_height_above() > STACK_MAX:
			return "Stapel wäre höher als %d" % STACK_MAX
		return ""
	if d.height_cm > TABLE_MAX_H_CM:
		return "%s ist %.0f cm hoch (max. %.0f auf Flächen)" % [d.id, d.height_cm, TABLE_MAX_H_CM]
	var width_avail: float
	if t.kind == &"surface":
		var s: Surface = t.node
		width_avail = s.width_cm()
		var clearance: float = _clearance_above(room, s)
		if d.height_cm * s.depth_factor() > clearance:
			return "%s passt nicht unter die Fläche darüber (%.0f cm Platz)" % [d.id, clearance]
	else:
		width_avail = (t.node as ItemNode).surface_width_global()
	if item.draw_size().x * t.global_scale > width_avail + 0.01:
		return "%s ist breiter als die Fläche" % d.id
	return ""


static func _container_target(room: Room, item: ItemNode, pointer: Vector2, items: Array[ItemNode] = []) -> Target:
	# innerster offener Behälter unter dem Finger gewinnt (Box im Kühlschrank vor dem Kühlschrank)
	var other: ItemNode = null
	for c: ItemNode in (items if not items.is_empty() else all_items(room)):
		if not c.def.is_container() or not c.is_open or c == item or item.is_ancestor_of(c):
			continue
		if not c.is_visible_in_tree() or not c.global_rect().has_point(pointer):
			continue
		if other == null or c.container_depth() > other.container_depth():
			other = c
	if other != null:
		var t := Target.new()
		t.kind = &"container"
		t.node = other
		t.parent = other.contents_root
		t.slot = other.free_slot()
		if item.def.height_cm > other.def.container_max_item_h_cm:
			t.rejected_reason = "%s ist zu groß für %s" % [item.def.id, other.def.id]
		elif t.slot < 0:
			t.rejected_reason = "%s ist voll" % other.def.id
		elif item.def.is_container() and other.container_depth() >= 1:
			t.rejected_reason = "Behälter höchstens 2 Ebenen tief"
		if not t.rejected_reason.is_empty():
			var f: Target = _floor_target(room, Vector2(pointer.x, _floor_depth_of(room, other) + FRONT_OF_SURFACE_CM))
			f.rejected_reason = t.rejected_reason
			return f
		var lay: Dictionary = other.content_layout(item, t.slot)
		t.global_pos = other.contents_root.to_global(lay[item])
		t.global_scale = other.global_scale.y
		return t
	return null


static func _floor_target(room: Room, pivot: Vector2) -> Target:
	var band: FloorBand = room.floor_band
	var p: Vector2 = band.clamp_point(pivot)
	var t := Target.new()
	t.kind = &"floor"
	t.parent = room.ysort_root
	t.global_pos = p
	t.global_scale = band.depth_factor(p.y)
	return t


## Tiefe (y im Bodenband) des obersten Boden-Vorfahren eines Items.
static func _floor_depth_of(room: Room, item: ItemNode) -> float:
	var n: Node = item
	while n.get_parent() and n.get_parent() != room.ysort_root:
		n = n.get_parent()
	return clampf((n as Node2D).position.y if n is Node2D else 0.0, room.floor_band.back_y_cm, room.floor_band.front_y_cm)


## Freier Platz über einer Raum-Oberfläche bis zur nächsten darüber (gleiche x-Überlappung).
static func _clearance_above(room: Room, s: Surface) -> float:
	var best: float = INF
	for o: Surface in room.get_surfaces():
		if o == s or o.x_to_cm < s.x_from_cm or o.x_from_cm > s.x_to_cm:
			continue
		var gap: float = s.top_y() - o.top_y()
		if gap > 0.0 and gap < best:
			best = gap
	return best


## Fallzeit (s) für eine Strecke in cm – natürlich wirkend, aber nie länger als 0,4 s.
static func fall_time(distance_cm: float) -> float:
	return clampf(sqrt(maxf(distance_cm, 0.0) / 490.0), 0.08, MAX_FALL_S)


## Alle Items im Raum (auch auf Tischen, in Stapeln und Behältern), ohne das Drag-Layer.
static func all_items(room: Room) -> Array[ItemNode]:
	var out: Array[ItemNode] = []
	_collect(room.ysort_root, out)
	return out


static func _collect(n: Node, out: Array[ItemNode]) -> void:
	for c: Node in n.get_children():
		if c is ItemNode:
			out.append(c)
			for r: Node in (c as ItemNode).child_roots():
				_collect(r, out)


# ---------------------------------------------------------------- P07: Wand
const WALL_TOP_GAP_CM: float = 6.0     ## Abstand zur Decke


static func _wall_target(room: Room, item: ItemNode, top_center: Vector2) -> Target:
	var t := Target.new()
	t.kind = &"wall"
	t.parent = room.ysort_root
	t.global_pos = wall_point(room, item, top_center)
	t.global_scale = 1.0                    # an der Rückwand: Tiefen-Faktor 1,0
	return t


## Aufhängepunkt (oben Mitte) an der Wand: nie unter die Bodenlinie, nie über die Decke, nie seitlich hinaus.
## Türen und bodentiefe Fenster (tag "to_floor") stehen immer genau auf der Bodenlinie.
static func wall_point(room: Room, item: ItemNode, top_center: Vector2) -> Vector2:
	var sz: Vector2 = item.draw_size()
	var x: float = clampf(top_center.x, sz.x * 0.5, maxf(sz.x * 0.5, room.width_cm - sz.x * 0.5))
	var y_min: float = -room.height_cm + WALL_TOP_GAP_CM
	var y_max: float = maxf(y_min, -sz.y)
	var y: float = y_max if item.def.tags.has("to_floor") else clampf(top_center.y, y_min, y_max)
	return Vector2(x, y)

