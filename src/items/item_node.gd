class_name ItemNode
extends Node2D
## Ein Item in der Welt (P02-T03). Ursprung = Pivot (meist unten Mitte), Größe exakt aus der Definition.
## Kinder: Sprite · OnTop (Dinge, die auf diesem Item stehen/gestapelt sind) · Contents (Behälter-Inhalt).
## Tickt NICHT im Ruhezustand (kein _process) – Animationen laufen über Tweens.

signal tapped(item: ItemNode)
signal opened_changed(item: ItemNode, open: bool)

const LIFT_CM: float = 6.0            ## Tech-Spec §4.1: Item hebt sich 6 cm
const SHADOW_ALPHA: float = 0.18

static var _next_uid: int = 1
static var _bitmaps: Dictionary = {}  ## Textur-Pfad → BitMap (Alpha-Treffertest)

var def: ItemDefinition
var uid: int = 0
var slot_index: int = -1              ## Platz im Behälter (−1 = nicht in einem Behälter)
var is_open: bool = false
var lifted: float = 0.0:              ## 0 = liegt, 1 = angehoben
	set(v):
		lifted = v
		var n: Node2D = lift_node()
		if n:
			n.position.y = -LIFT_CM * v
		queue_redraw()

var sprite: Sprite2D
var on_top_root: Node2D
var contents_root: Node2D
var _draw_size: Vector2               ## tatsächlich gezeichnete Größe in cm (lokal, unskaliert)
var _lift_tween: Tween


static func create(definition: ItemDefinition) -> ItemNode:
	var n := ItemNode.new()
	n.setup(definition)
	return n


func setup(definition: ItemDefinition) -> void:
	def = definition
	uid = _next_uid
	_next_uid += 1
	name = "%s_%d" % [def.id, uid]
	_build_visual()
	on_top_root = Node2D.new()
	on_top_root.name = "OnTop"
	add_child(on_top_root)
	contents_root = ContentsPanel.new()
	contents_root.name = "Contents"
	contents_root.visible = false
	add_child(contents_root)
	apply_world_size()


## Optik aufbauen (überschreibbar: Figuren bauen hier ihre Ebenen).
func _build_visual() -> void:
	sprite = Sprite2D.new()
	sprite.name = "Sprite"
	sprite.centered = false
	sprite.texture = load(def.sprite_path)
	add_child(sprite)


# ---------------------------------------------------------------- Hooks (Figuren/Tiere überschreiben)

## Knoten, der beim Anheben 6 cm hochgeht (Figuren: der ganze Körper samt Händen und gehaltenem Item).
func lift_node() -> Node2D:
	return sprite


## Knoten, unter denen weitere Items hängen können (für Treffer- und Zielsuche).
func child_roots() -> Array[Node]:
	return [on_top_root, contents_root]


func on_drag_start(_grab_global: Vector2) -> void:
	pass


func on_drag_update(_delta: float, _velocity: Vector2) -> void:
	pass


func on_drag_end() -> void:
	pass


## Nach Abstellen/Rückgängig: neuer Eltern-Knoten steht fest (Figuren wählen hier Stehen/Sitzen/Liegen).
func on_placed() -> void:
	pass


## Tippen mit Ort (Figuren: Kopf → Gesicht wechseln).
func on_tap_at(_world: Vector2) -> void:
	on_tap()


## Maßstab-Bibel §1: Skalierung = Welt-Höhe / Textur-Inhaltshöhe (gleich für x und y).
func apply_world_size() -> void:
	var tex: Vector2 = sprite.texture.get_size()
	var content: Vector2 = tex - Vector2.ONE * 2.0 * def.pad_px
	var s: float = Units.sprite_scale(content.y, def.height_cm)
	sprite.scale = Vector2(s, s)
	sprite.offset = -(Vector2.ONE * def.pad_px + def.pivot * content)
	_draw_size = content * s
	(contents_root as ContentsPanel).rect = interior_rect()
	queue_redraw()


## Rechteck des sichtbaren Inhalts in lokalen cm (ohne Anhebe-Versatz).
func local_rect() -> Rect2:
	return Rect2(-def.pivot * _draw_size, _draw_size)


func draw_size() -> Vector2:
	return _draw_size


func global_rect() -> Rect2:
	var r: Rect2 = local_rect()
	var gs: Vector2 = global_scale
	return Rect2(global_position + r.position * gs + Vector2(0, -LIFT_CM * lifted * gs.y), r.size * gs)


# ---------------------------------------------------------------- Treffertest

## Treffer, wenn der Punkt auf sichtbaren Pixeln liegt – oder innerhalb der Mindest-Tippfläche
## (min_size_world in cm, z. B. 48 dp / Zoom), damit auch ein 6-cm-Ei gut greifbar ist.
func hit_test(global_point: Vector2, min_size_world: float) -> bool:
	var r: Rect2 = global_rect()
	var grown: Rect2 = r
	if r.size.x < min_size_world:
		grown = grown.grow_individual((min_size_world - r.size.x) * 0.5, 0, (min_size_world - r.size.x) * 0.5, 0)
	if r.size.y < min_size_world:
		grown = grown.grow_individual(0, (min_size_world - r.size.y) * 0.5, 0, (min_size_world - r.size.y) * 0.5)
	if not grown.has_point(global_point):
		return false
	if not r.has_point(global_point) or (r.size.x <= min_size_world and r.size.y <= min_size_world):
		return true                     # kleines Item: ganze Tippfläche zählt
	return _alpha_hit(global_point, r)


func _alpha_hit(global_point: Vector2, r: Rect2) -> bool:
	var bm: BitMap = _bitmap_for(sprite.texture)
	if bm == null:
		return true
	var uv: Vector2 = (global_point - r.position) / r.size
	var content: Vector2 = sprite.texture.get_size() - Vector2.ONE * 2.0 * def.pad_px
	var px: Vector2i = Vector2i((Vector2.ONE * def.pad_px + uv * content).floor())
	px = px.clamp(Vector2i.ZERO, bm.get_size() - Vector2i.ONE)
	return bm.get_bitv(px)


static func _bitmap_for(tex: Texture2D) -> BitMap:
	if tex == null:
		return null
	if _bitmaps.has(tex.resource_path):
		return _bitmaps[tex.resource_path]
	var img: Image = tex.get_image()
	var bm: BitMap = null
	if img:
		if img.is_compressed():
			img.decompress()
		bm = BitMap.new()
		bm.create_from_image_alpha(img, 0.15)
	_bitmaps[tex.resource_path] = bm
	return bm


# ---------------------------------------------------------------- Oberfläche & Stapel

## Oberkante der Abstellfläche (global) – nur für Items mit Fläche (Tisch) oder Stapel-Items.
func top_global_y(for_stacking: bool = false) -> float:
	var h: float = _draw_size.y if for_stacking or not def.has_surface() else def.surface_local_h()
	var bottom_local: float = (1.0 - def.pivot.y) * _draw_size.y   # Unterkante (0 bei Pivot unten)
	return global_position.y + (bottom_local - h) * global_scale.y


## x-Bereich der Fläche (global).
func surface_x_range() -> Vector2:
	var r: Rect2 = local_rect()
	var inset: float = r.size.x * def.surface_inset
	return Vector2(global_position.x + (r.position.x + inset) * global_scale.x,
		global_position.x + (r.end.x - inset) * global_scale.x)


func surface_width_global() -> float:
	var xr: Vector2 = surface_x_range()
	return xr.y - xr.x


## Stapel-Höhe unterhalb inkl. diesem Item (nur stapelbare Vorfahren über OnTop).
func stack_depth_below() -> int:
	var n: int = 1
	var p: Node = get_parent()
	while p and p.name == "OnTop" and p.get_parent() is ItemNode and (p.get_parent() as ItemNode).def.is_stackable():
		n += 1
		p = p.get_parent().get_parent()
	return n


## Anzahl stapelbarer Items ab diesem aufwärts (inkl. dieses).
func stack_height_above() -> int:
	var best: int = 0
	for c: Node in on_top_root.get_children():
		if c is ItemNode and (c as ItemNode).def.is_stackable():
			best = maxi(best, (c as ItemNode).stack_height_above())
	return 1 + best


func has_stacked_child() -> bool:
	for c: Node in on_top_root.get_children():
		if c is ItemNode and (c as ItemNode).def.is_stackable():
			return true
	return false


# ---------------------------------------------------------------- Behälter

## Liegt dieses Item (direkt oder indirekt) in einem Behälter?
func container_depth() -> int:
	var n: int = 0
	var p: Node = get_parent()
	while p:
		if p.name == "Contents" and p.get_parent() is ItemNode:
			n += 1
		p = p.get_parent()
	return n


func free_slot() -> int:
	var used: Dictionary = {}
	for c: Node in contents_root.get_children():
		if c is ItemNode:
			used[(c as ItemNode).slot_index] = true
	for i: int in def.container_slots:
		if not used.has(i):
			return i
	return -1


## Innenfläche (lokal) ohne Inhalt.
func interior_rect() -> Rect2:
	return local_rect().grow(-minf(_draw_size.x, _draw_size.y) * 0.08)


## Regal-Layout des Inhalts in ECHTER Größe (Maßstab bleibt gültig): Reihen von links nach rechts,
## unten bündig, sortiert nach Platz. Die Innenfläche wächst bei Bedarf (nach oben, mittig), damit nichts übersteht.
## extra = Item, das gerade hineingelegt wird (für die Zielposition). Gibt {item: lokale Pivot-Position} + "rect" zurück.
func content_layout(extra: ItemNode = null, extra_slot: int = -1) -> Dictionary:
	const GAP: float = 2.0
	var list: Array[ItemNode] = []
	for c: Node in contents_root.get_children():
		if c is ItemNode and c != extra:
			list.append(c)
	if extra:
		list.append(extra)
	var slot_of := func(it: ItemNode) -> int: return extra_slot if it == extra else it.slot_index
	list.sort_custom(func(a: ItemNode, b: ItemNode) -> bool: return slot_of.call(a) < slot_of.call(b))
	var inner: Rect2 = interior_rect()
	var width: float = inner.size.x
	for it: ItemNode in list:
		width = maxf(width, it.draw_size().x + 2.0 * GAP)
	# Reihen bilden
	var rows: Array = []          # [[items], row_w, row_h]
	var row: Array[ItemNode] = []
	var rw: float = GAP
	var rh: float = 0.0
	for it: ItemNode in list:
		var sz: Vector2 = it.draw_size()
		if not row.is_empty() and rw + sz.x + GAP > width:
			rows.append([row, rw, rh])
			row = []
			rw = GAP
			rh = 0.0
		row.append(it)
		rw += sz.x + GAP
		rh = maxf(rh, sz.y)
	if not row.is_empty():
		rows.append([row, rw, rh])
	var height: float = GAP
	for r: Array in rows:
		height += float(r[2]) + GAP
	var size := Vector2(width, maxf(inner.size.y, height))
	var rect := Rect2(Vector2(inner.get_center().x - size.x * 0.5, inner.end.y - size.y), size)
	var out: Dictionary = {"rect": rect}
	var y: float = rect.position.y + GAP
	for r: Array in rows:
		var x: float = rect.position.x + GAP
		for it: ItemNode in r[0]:
			var sz2: Vector2 = it.draw_size()
			out[it] = Vector2(x + it.def.pivot.x * sz2.x, y + float(r[2]) - (1.0 - it.def.pivot.y) * sz2.y)
			x += sz2.x + GAP
		y += float(r[2]) + GAP
	return out


## Ordnet den Inhalt neu an (nach Hineinlegen/Herausnehmen/Rückgängig).
func relayout_contents() -> void:
	if not def.is_container():
		return
	var lay: Dictionary = content_layout()
	(contents_root as ContentsPanel).rect = lay["rect"]
	contents_root.queue_redraw()
	for it: Variant in lay.keys():
		if it is ItemNode:
			(it as ItemNode).position = lay[it]
			(it as ItemNode).scale = Vector2.ONE


## Liegt in einer Hand (HandSlot einer Figur)?
func is_held() -> bool:
	var p: Node = get_parent()
	return p != null and String(p.name).begins_with("HandSlot")


func set_open(open: bool) -> void:
	if not def.is_container() or open == is_open:
		return
	is_open = open
	contents_root.visible = open
	sprite.modulate = Color(0.82, 0.82, 0.86) if open else Color.WHITE
	AudioBus.play_item_sfx(def, "open" if open else "close")
	opened_changed.emit(self, open)


func on_tap() -> void:
	if def.is_container():
		set_open(not is_open)
	else:
		AudioBus.play_sfx("tap")
		_bounce()
	tapped.emit(self)


# ---------------------------------------------------------------- Anheben (Optik)

func set_lifted(on: bool, animate: bool = true) -> void:
	if _lift_tween:
		_lift_tween.kill()
	if not animate or not is_inside_tree():
		lifted = 1.0 if on else 0.0
		return
	_lift_tween = create_tween()
	_lift_tween.tween_property(self, "lifted", 1.0 if on else 0.0, 0.14 if on else 0.1) \
		.set_trans(Tween.TRANS_BACK if on else Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)


func _bounce() -> void:
	if not is_inside_tree():
		return
	var tw: Tween = create_tween()
	tw.tween_property(sprite, "scale", sprite.scale * Vector2(1.08, 0.92), 0.06)
	tw.tween_property(sprite, "scale", sprite.scale, 0.12).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func _draw() -> void:
	if def == null or def.placement == "wall" or is_held():
		return
	# weicher Kontaktschatten, wächst und verblasst beim Anheben
	var w: float = _draw_size.x * (0.82 + 0.25 * lifted)
	var h: float = minf(w * 0.16, 7.0)
	var col := Color(0.15, 0.1, 0.05, SHADOW_ALPHA * (1.0 - 0.45 * lifted))
	var center_x: float = (0.5 - def.pivot.x) * _draw_size.x
	var y: float = (1.0 - def.pivot.y) * _draw_size.y
	draw_set_transform(Vector2(center_x, y), 0.0, Vector2(1.0, h / w))
	draw_circle(Vector2.ZERO, w * 0.5, col)
	draw_circle(Vector2.ZERO, w * 0.36, Color(col, col.a * 0.8))
	draw_set_transform(Vector2.ZERO)


## Innenfläche eines geöffneten Behälters (hinter dem Inhalt).
class ContentsPanel extends Node2D:
	var rect: Rect2 = Rect2()

	func _draw() -> void:
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(0.97, 0.98, 1.0, 0.94)
		sb.border_color = Color(0.55, 0.6, 0.7)
		sb.set_border_width_all(1)
		sb.set_corner_radius_all(4)
		sb.anti_aliasing = true
		draw_style_box(sb, rect)
