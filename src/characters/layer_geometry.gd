class_name LayerGeometry
extends RefCounted
## Geometrie für Figuren aus mehreren Sprite-Ebenen (Rig, später NPCs): Hülle und Pixel-genauer Treffer.


## Hülle aller sichtbaren Ebenen in lokalen Koordinaten von root (funktioniert auch außerhalb des Baums).
static func bounds(root: Node2D, layers: Array) -> Rect2:
	var r := Rect2()
	var first: bool = true
	for sp: Sprite2D in layers:
		if not _visible_under(sp, root):
			continue
		var sr: Rect2 = local_xf(root, sp) * sp.get_rect()
		r = sr if first else r.merge(sr)
		first = false
	return r


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
