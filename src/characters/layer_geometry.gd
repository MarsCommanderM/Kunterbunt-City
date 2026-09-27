class_name LayerGeometry
extends RefCounted
## Geometrie für Figuren aus mehreren Sprite-Ebenen (Rig, später NPCs): Hülle und Pixel-genauer Treffer.


## Hülle aller sichtbaren Ebenen in lokalen Koordinaten von root (funktioniert auch außerhalb des Baums).
## extra: zusätzliche Drehung/Verschiebung vor dem Messen (z. B. „wie läge die Figur geneigt?“).
static func bounds(root: Node2D, layers: Array, extra: Transform2D = Transform2D.IDENTITY) -> Rect2:
	var r := Rect2()
	var first: bool = true
	for sp: Sprite2D in layers:
		if not _visible_under(sp, root):
			continue
		var sr: Rect2 = extra * local_xf(root, sp) * sp.get_rect()
		r = sr if first else r.merge(sr)
		first = false
	return r


static var _outline: Dictionary = {}   ## Textur → Umriss-Punkte der gemalten Fläche (Textur-Pixel)


## Umriss der gemalten Fläche einer Ebene in ihren lokalen Koordinaten (für gedrehte Messungen genau).
static func content_points(sp: Sprite2D) -> PackedVector2Array:
	var out := PackedVector2Array()
	if sp.texture == null:
		return out
	var key: String = sp.texture.resource_path
	if not _outline.has(key):
		var pts := PackedVector2Array()
		var bm: BitMap = ItemNode._bitmap_for(sp.texture)
		if bm != null:
			for poly: PackedVector2Array in bm.opaque_to_polygons(Rect2i(Vector2i.ZERO, bm.get_size()), 1.5):
				pts.append_array(poly)
		_outline[key] = pts
	var full: Rect2 = sp.get_rect()
	var k: Vector2 = full.size / sp.texture.get_size()
	for q: Vector2 in _outline[key]:
		out.append(full.position + q * k)
	return out


## Tiefster gemalter Punkt (größtes y) aller sichtbaren Ebenen in root-Koordinaten, optional gedreht (extra).
static func lowest(root: Node2D, layers: Array, extra: Transform2D = Transform2D.IDENTITY) -> float:
	var y: float = -INF
	for sp: Sprite2D in layers:
		if not _visible_under(sp, root):
			continue
		var xf: Transform2D = extra * local_xf(root, sp)
		for q: Vector2 in content_points(sp):
			y = maxf(y, (xf * q).y)
	return y


## Transform von n relativ zu root (Kette der Eltern bis root).
static func local_xf(root: Node, n: Node2D) -> Transform2D:
	var xf: Transform2D = n.transform
	var p: Node = n.get_parent()
	while p and p != root:
		xf = (p as Node2D).transform * xf
		p = p.get_parent()
	return xf


## Trifft der Punkt ein nicht-transparentes Pixel irgendeiner sichtbaren Ebene?
static func alpha_hit(layers: Array, global_point: Vector2) -> bool:
	for sp: Sprite2D in layers:
		if not sp.is_visible_in_tree():
			continue
		var lp: Vector2 = sp.to_local(global_point)
		var rr: Rect2 = sp.get_rect()
		if not rr.has_point(lp):
			continue
		var bm: BitMap = ItemNode._bitmap_for(sp.texture)
		if bm == null:
			return true
		var px: Vector2i = Vector2i((lp - rr.position).floor()).clamp(Vector2i.ZERO, bm.get_size() - Vector2i.ONE)
		if bm.get_bitv(px):
			return true
	return false


static func _visible_under(n: CanvasItem, root: Node) -> bool:
	var c: Node = n
	while c and c != root:
		if c is CanvasItem and not (c as CanvasItem).visible:
			return false
		c = c.get_parent()
	return true
