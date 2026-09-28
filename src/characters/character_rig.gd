class_name CharacterRig
extends ItemNode
## Figur aus Ebenen (Tech-Spec §4.2, P03-T01…T08). Ursprung = zwischen den Füßen (stehend) bzw. Sitzpunkt.
## Ebenen hinten → vorne: Haare hinten · Arm hinten · Beine · Schuhe · Shirt · Kopf · Gesicht · Haare vorne ·
## Arm vorne [Haut, Ärmel, Handfläche, HandSlot (Item), Finger] · Zwei-Hand-Slot · Finger (zwei Hände).
## → Zeichenreihenfolge Arm < Item < Hand. Posen: stand, sit, lie × Arme idle/hold_one/hold_two.

signal emotion_changed(emotion: String)
signal ate(item_id: StringName)

const ARM_IDLE: float = 0.12
const ARM_HOLD: float = 0.55
const ARM_TWO: float = 0.58
static var animate_poses: bool = true   ## false: Posen springen (Tests, Screenshots, Messungen)

const ARM_CARRIED: float = 1.05     ## Arme hoch, wenn die Figur getragen wird („Wiii!“)
const LIE_TILT_MAX: float = 0.45    ## max. Neigung beim Liegen (≈ 26°, Kopf wie auf einem dicken Kissen)

var template_id: String
var t: Dictionary
var look: Dictionary
var body_pose: String = "stand"     ## stand | sit | lie
var emotion: String = "happy"

var lift_root: Node2D
var swing: Node2D
var parts: Node2D
var arm_front: Node2D
var arm_back: Node2D
var slot_front: Node2D
var slot_back: Node2D
var slot_two: Node2D
var head_pivot: Node2D
var head_back: Node2D               ## P04b: Haare hinten liegen HINTER dem Körper, folgen aber dem Kopf
var hands_top: Node2D
var _layers: Dictionary = {}        ## Name → Sprite2D
var _pose_offset: Vector2 = Vector2.ZERO
var _carried: bool = false
var _swing_vel: float = 0.0
var _rect_cache: Rect2 = Rect2()
var _pose_tween: Tween


static func create_character(tid: String, appearance: Dictionary = {}) -> CharacterRig:
	var r := CharacterRig.new()
	r.template_id = tid
	r.t = CharacterTemplates.get_template(tid)
	r.look = CharacterTemplates.default_look(tid)
	r.look.merge(appearance, true)
	r.setup(CharacterTemplates.make_definition(tid))
	return r


func _build_visual() -> void:
	lift_root = Node2D.new()
	lift_root.name = "Lift"
	add_child(lift_root)
	swing = Node2D.new()
	swing.name = "Swing"
	lift_root.add_child(swing)
	parts = Node2D.new()
	parts.name = "Parts"
	swing.add_child(parts)
	var top: float = float(t["hair_top"])
	head_back = Node2D.new()
	head_back.name = "HeadBack"
	parts.add_child(head_back)
	arm_back = _arm("ArmBack", -1.0)
	parts.add_child(arm_back)
	_layer(parts, "Legs", CharacterLook.part_for(template_id, look, "Legs"), Vector2.ZERO)
	_layer(parts, "Shoes", CharacterLook.part_for(template_id, look, "Shoes"), Vector2.ZERO)
	_layer(parts, "Top", CharacterLook.part_for(template_id, look, "Top"),
		Vector2(0, -float(t["torso"]["bot"])))
	head_pivot = Node2D.new()
	head_pivot.name = "HeadPivot"
	parts.add_child(head_pivot)
	var cy: float = -float(t["head"]["cy"])
	head_pivot.position = Vector2(0, cy)
	var hy: float = -top - cy                  ## Haar sitzt oben, Kopf in der Mitte
	head_back.position = head_pivot.position
	_layer(head_back, "HairBack", CharacterLook.part_for(template_id, look, "HairBack"), Vector2(0, hy))
	_layer(head_pivot, "Head", "head", Vector2.ZERO)
	_layer(head_pivot, "Eyes", CharacterLook.part_for(template_id, look, "Eyes"), Vector2.ZERO)
	_layer(head_pivot, "Mouth", CharacterLook.part_for(template_id, look, "Mouth"), Vector2.ZERO)
	_layer(head_pivot, "HairFront", CharacterLook.part_for(template_id, look, "HairFront"), Vector2(0, hy))
	_layer(head_pivot, "Accessory", CharacterLook.part_for(template_id, look, "Accessory"), Vector2.ZERO)
	_layer(head_pivot, "Aid", CharacterLook.part_for(template_id, look, "Aid"), Vector2.ZERO)
	arm_front = _arm("ArmFront", 1.0)
	parts.add_child(arm_front)
	slot_two = Node2D.new()
	slot_two.name = "HandSlotTwo"
	parts.add_child(slot_two)
	hands_top = Node2D.new()
	hands_top.name = "HandsTop"
	hands_top.visible = false
	parts.add_child(hands_top)
	for i: int in 2:
		_layer(hands_top, "Fingers%d" % i, "hand_front", Vector2.ZERO)
	sprite = _layers["Top"]          # Basis-Klasse erwartet ein Sprite
	_apply_arms(ARM_IDLE, ARM_IDLE)


## Ebene mit Anker aus parts.json (cm, y von unten) an Position pos.
func _layer(parent: Node, lname: String, part: String, pos: Vector2, tint: bool = true) -> Sprite2D:
	var sp := Sprite2D.new()
	sp.name = lname
	sp.centered = false
	_set_part(sp, part)
	sp.position = pos
	if tint:
		CharacterLook.apply(sp, CharacterLook.colors_for(look, lname), CharacterLook.ink_for(look, lname))
	parent.add_child(sp)
	_layers[lname] = sp
	return sp


func _set_part(sp: Sprite2D, part: String) -> void:
	var info: Dictionary = CharacterTemplates.part_info(template_id, part)
	sp.texture = CharacterTemplates.part_texture(template_id, part)
	var s: float = float(info["w_cm"]) / sp.texture.get_size().x
	sp.scale = Vector2(s, s)
	# Anker (cm, y von unten) → Offset in px (y von oben)
	var a: Array = info["anchor_cm"]
	sp.offset = -Vector2(float(a[0]), float(info["h_cm"]) - float(a[1])) / s
	sp.set_meta("part", part)


func _arm(aname: String, side: float) -> Node2D:
	var arm := Node2D.new()
	arm.name = aname
	arm.position = Vector2(side * float(t["shoulder"]["x"]), -float(t["shoulder"]["y"]))
	var hand_pos := Vector2(0, float(t["arm"]["len"]))
	_layer(arm, aname + "Skin", "arm_skin", Vector2.ZERO)
	_layer(arm, aname + "Sleeve", CharacterLook.part_for(template_id, look, aname + "Sleeve"), Vector2.ZERO)
	_layer(arm, aname + "Palm", "hand", hand_pos)
	var slot := Node2D.new()
	slot.name = "HandSlot" + ("Front" if side > 0 else "Back")
	slot.position = hand_pos
	arm.add_child(slot)
	var fingers: Sprite2D = _layer(arm, aname + "Fingers", "hand_front", hand_pos)
	if side < 0:
		fingers.scale.x *= -1.0     # Finger zeigen zur Körpermitte
	if side > 0:
		slot_front = slot
	else:
		slot_back = slot
	return arm


# ---------------------------------------------------------------- Hände (P03-T04)

func lift_node() -> Node2D:
	return lift_root


func child_roots() -> Array[Node]:
	return [on_top_root, contents_root, slot_front, slot_back, slot_two]


## Freie Hände als [{slot, index, global}] – index 0 = vorne (rechts im Bild), 1 = hinten, 2 = beide.
func hand_slots() -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	var two_busy: bool = _held_in(slot_two) != null
	if not two_busy:
		if _held_in(slot_front) == null:
			out.append({"slot": slot_front, "index": 0, "global": slot_front.global_position})
		if _held_in(slot_back) == null:
			out.append({"slot": slot_back, "index": 1, "global": slot_back.global_position})
		if out.size() == 2:
			out.append({"slot": slot_two, "index": 2, "global": (slot_front.global_position + slot_back.global_position) * 0.5})
	return out


func held_item(index: int = 0) -> ItemNode:
	return _held_in([slot_front, slot_back, slot_two][index])


func _held_in(slot: Node) -> ItemNode:
	for c: Node in slot.get_children():
		if c is ItemNode:
			return c
	return null


## Lokale Position eines Items im HandSlot: Griffpunkt genau auf den Slot-Ursprung.
static func grip_local(item: ItemNode) -> Vector2:
	var g: Vector2 = item.def.grip if item.def.grip.x >= 0.0 else Vector2(0.5, 0.5)
	return -(g - item.def.pivot) * item.draw_size()


## Becken relativ zum Ursprung (stehend, unskaliert) – rastet auf Sitzplätzen ein.
func hip_offset() -> Vector2:
	return Vector2(0, -float(t["hip"]["y"]))


func hold_rotation_for(_index: int, item: ItemNode) -> float:
	return parts.global_rotation + deg_to_rad(item.def.hold_angle)


## Mund in globalen cm (für „Essen geben“).
func mouth_global() -> Vector2:
	var head: Dictionary = t["head"]
	return parts.to_global(Vector2(0, -float(head["cy"]) + float(head["h"]) * 0.26))


func eat(food: ItemNode, animate: bool = true) -> void:
	CharacterEating.eat(self, food, animate)


# ---------------------------------------------------------------- Posen (P03-T03)

## Pose aus der Umgebung: auf Sitzplatz → sit/lie, sonst stehen; Arme aus den gehaltenen Items.
func refresh_pose(animate: bool = true) -> void:
	var host: ItemNode = Seats.seat_host_of(self)
	var bp: String = "stand"
	if host != null:
		bp = host.def.seat_pose
	_set_body_pose(bp)
	var f: float = ARM_IDLE
	var b: float = ARM_IDLE
	var two_item: ItemNode = _held_in(slot_two)
	if two_item != null:
		f = two_hand_angle(two_item)
		b = f
	else:
		if _held_in(slot_front) != null:
			f = ARM_HOLD
		if _held_in(slot_back) != null:
			b = ARM_HOLD
		if _carried:
			f = maxf(f, ARM_CARRIED) if _held_in(slot_front) == null else f
			b = maxf(b, ARM_CARRIED) if _held_in(slot_back) == null else b
	if animate and animate_poses and is_inside_tree():
		if _pose_tween:
			_pose_tween.kill()
		var f0: float = -arm_front.rotation
		var b0: float = arm_back.rotation
		_pose_tween = create_tween()
		_pose_tween.tween_method(func(k: float) -> void: _apply_arms(lerpf(f0, f, k), lerpf(b0, b, k)), 0.0, 1.0, 0.16) \
			.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	else:
		_apply_arms(f, b)
	_rect_cache = Rect2()
	queue_redraw()


## Arm-Winkel für ein Item in BEIDEN Händen: aus der Item-Breite gerechnet, damit die Hände links und
## rechts am Item sitzen (Wasserball) – und nicht über Kreuz vor dem Bauch hängen.
func two_hand_angle(item: ItemNode) -> float:
	var shoulder_x: float = float(t["shoulder"]["x"])
	var arm_len: float = float(t["arm"]["len"])
	var half: float = item.def.width_cm * item.global_scale.x / maxf(global_scale.x, 0.001) * 0.5
	return asin(clampf((half - shoulder_x) / arm_len, -0.9, 0.9))


## Arm-Winkel: positiv = nach außen gespreizt, negativ = zur Körpermitte (vor dem Bauch).
func _apply_arms(front_out: float, back_out: float) -> void:
	arm_front.rotation = -front_out
	arm_back.rotation = back_out
	var two: bool = _held_in(slot_two) != null
	# Arm hinten kommt beim Tragen mit zwei Händen vor den Körper
	parts.move_child(arm_back, parts.get_children().find(head_pivot) if two else 1)
	for s: Node2D in [slot_front, slot_back]:
		s.rotation = -s.get_parent().rotation            # Item bleibt aufrecht …
		var it: ItemNode = _held_in(s)
		if it:
			s.rotation += deg_to_rad(it.def.hold_angle)  # … plus eigener Haltewinkel
	var pf: Vector2 = arm_front.transform * slot_front.position   # Hand vorne in Parts-Koordinaten
	var pb: Vector2 = arm_back.transform * slot_back.position
	slot_two.position = (pf + pb) * 0.5
	var held_two: ItemNode = _held_in(slot_two)
	slot_two.rotation = deg_to_rad(held_two.def.hold_angle) if held_two else 0.0
	hands_top.visible = two
	for a: Node2D in [arm_front, arm_back]:
		_layers[String(a.name) + "Fingers"].visible = not two
	if two:
		(_layers["Fingers0"] as Sprite2D).position = pf
		(_layers["Fingers1"] as Sprite2D).position = pb
		(_layers["Fingers1"] as Sprite2D).scale.x = -absf((_layers["Fingers1"] as Sprite2D).scale.x)
	_rect_cache = Rect2()


func _set_body_pose(bp: String) -> void:
	body_pose = bp
	var hip: float = float(t["hip"]["y"])
	var sit: bool = bp == "sit"
	_set_part(_layers["Legs"], CharacterLook.part_for(template_id, look, "Legs", "sit" if sit else ""))
	_layers["Legs"].scale.y = absf(_layers["Legs"].scale.y)
	_layers["Shoes"].position = Vector2.ZERO
	_layers["Legs"].position = Vector2.ZERO
	var drop: float = 0.0
	var thick: float = 0.0
	if sit:
		# Beine hängen ab der Hüfte (Anker des Teils) herab; reicht der Platz nicht bis zum Boden
		# (Erwachsene auf dem 42-cm-Sofa), verkürzt sich der Unterschenkel perspektivisch.
		var natural: float = float(CharacterTemplates.geometry(template_id)["sit_drop_cm"])
		drop = natural
		var seat_h: float = Seats.seat_height_of(self)
		if seat_h > 0.0:
			drop = minf(drop, seat_h)       ## Sitz zu niedrig → Unterschenkel perspektivisch kürzen
		_layers["Legs"].position = Vector2(0, -hip)
		_layers["Legs"].scale.y *= clampf(drop / natural, 0.55, 1.0)
		_layers["Shoes"].position = Vector2(0, -hip + drop - 0.8)
	match bp:
		"lie":
			# P04b: Die ganze Figur liegt – auch der große Kopf (auf dem Kissen, Gesicht zur Seite).
			# Aufrecht bleibende Köpfe ließen lange Haare durch das Bett hängen.
			head_pivot.rotation = 0.0
			head_pivot.position.x = 0.0
			head_back.rotation = 0.0
			head_back.position = head_pivot.position
			# Beide Arme liegen OBEN auf dem Körper (sonst hängt einer unterm Rücken)
			arm_back.position.x = float(t["shoulder"]["x"])
			arm_front.position.x = float(t["shoulder"]["x"]) * 0.55
			# Der große Kopf ist dicker als Rumpf und Beine: waagerecht läge nur der Kopf auf und der Körper
			# schwebte. Darum leicht geneigt wie auf einem Kissen – Kopf UND Füße liegen auf (max. 26°).
			parts.rotation = 0.0
			var legs: Array = [_layers["Legs"], _layers["Shoes"]]
			var solid: Array = _layers.values().filter(func(sp: Sprite2D) -> bool: return not String(sp.name).begins_with("Hair"))
			var rot := Transform2D(-PI * 0.5, Vector2.ZERO)
			var tilt: float = 0.0
			while tilt < LIE_TILT_MAX:      # kleinste Neigung, bei der die Beine so tief liegen wie der Kopf
				rot = Transform2D(-PI * 0.5 + tilt, Vector2.ZERO)
				if LayerGeometry.lowest(parts, legs, rot) >= LayerGeometry.lowest(parts, solid, rot) - 1.0:
					break
				tilt = minf(tilt + 0.02, LIE_TILT_MAX)
			rot = Transform2D(-PI * 0.5 + tilt, Vector2.ZERO)
			thick = LayerGeometry.lowest(parts, solid, rot)     # Haare sind weich: sie liegen aufs Kissen
			parts.rotation = -PI * 0.5 + tilt
			_pose_offset = Vector2(-(rot * Vector2(0, -hip)).x, -hip - thick)
		_:
			parts.rotation = 0.0
			_pose_offset = Vector2.ZERO
			head_pivot.rotation = 0.0
			head_pivot.position.x = 0.0
			arm_back.position.x = -float(t["shoulder"]["x"])
			arm_front.position.x = float(t["shoulder"]["x"])
	head_back.position = head_pivot.position
	head_back.rotation = head_pivot.rotation
	parts.position = _pose_offset - swing.position


func on_placed() -> void:
	refresh_pose(false)


# ---------------------------------------------------------------- Getragen werden (P03-T06)

func on_drag_start(grab_global: Vector2) -> void:
	_carried = true
	_set_body_pose("stand")
	var g: Vector2 = to_local(grab_global)
	swing.position = g
	parts.position = _pose_offset - g
	refresh_pose()


func on_drag_update(delta: float, velocity: Vector2) -> void:
	# Pendeln am Griffpunkt: Feder zum Ziel-Winkel (Gegenrichtung der Bewegung), gedämpft
	var target: float = clampf(-velocity.x * 0.0022, -0.55, 0.55)
	_swing_vel += (target - swing.rotation) * 90.0 * delta
	_swing_vel *= exp(-9.0 * delta)
	swing.rotation += _swing_vel * delta


func on_drag_end() -> void:
	_carried = false
	_swing_vel = 0.0
	swing.rotation = 0.0
	swing.position = Vector2.ZERO
	parts.position = _pose_offset
	refresh_pose(false)


# ---------------------------------------------------------------- Aussehen tauschen (P04-T03)

## Neues Aussehen (Teile + Farben + Hautton) auf die bestehende Figur anwenden – ohne sie neu zu
## bauen. Die GRÖSSE bleibt immer die der Schablone (Regel: nie aus Teilen oder Farben).
func apply_look(new_look: Dictionary) -> void:
	look = new_look
	var e: String = emotion
	for name: String in ["Legs", "Shoes", "Top", "HairBack", "Head", "Eyes", "Mouth",
			"HairFront", "Accessory", "Aid"]:
		var sp: Sprite2D = _layers.get(name)
		if sp == null:
			continue
		_set_part(sp, _part_name(name))
		CharacterLook.apply(sp, CharacterLook.colors_for(look, name), CharacterLook.ink_for(look, name))
	for arm: Node2D in [arm_back, arm_front]:
		for c: Node in arm.get_children():
			if not (c is Sprite2D):
				continue
			var sp2: Sprite2D = c
			if not String(sp2.name).ends_with("Skin") and not String(sp2.name).ends_with("Palm") \
					and not String(sp2.name).ends_with("Fingers"):
				_set_part(sp2, _part_name(String(sp2.name)))
			CharacterLook.apply(sp2, CharacterLook.colors_for(look, String(sp2.name)))
	for i: int in 2:
		var f: Sprite2D = _layers.get("Fingers%d" % i)
		if f != null:
			CharacterLook.apply(f, CharacterLook.colors_for(look, "Fingers%d" % i))
	set_emotion(e)
	_rect_cache = Rect2()
	refresh_pose(false)
	queue_redraw()


func _part_name(layer: String) -> String:
	if layer == "Head":
		return "head"
	if layer == "Legs":
		return CharacterLook.part_for(template_id, look, "Legs",
			"sit" if body_pose == "sit" else "")
	return CharacterLook.part_for(template_id, look, layer)


# ---------------------------------------------------------------- Gesicht (P03-T07)

func set_emotion(e: String) -> void:
	if not CharacterTemplates.emotions().has(e):
		return
	emotion = e
	# „fröhlich“ ist der Normalzustand → der im Editor gewählte Mund bleibt (P04b)
	_set_part(_layers["Mouth"], CharacterLook.part_for(template_id, look, "Mouth") if e == "happy" \
		else "mouth_" + e)
	# Augen: für jedes Gefühl ein eigenes Teil, sonst die im Editor gewählte Form
	var eyes: String = "eyes_" + e
	if not CharacterTemplates.has_part(template_id, eyes):
		eyes = CharacterLook.part_for(template_id, look, "Eyes")
	_set_part(_layers["Eyes"], eyes)
	_rect_cache = Rect2()
	emotion_changed.emit(e)


func next_emotion() -> void:
	var list: Array = CharacterTemplates.emotions()
	set_emotion(list[(list.find(emotion) + 1) % list.size()])


func on_tap_at(world: Vector2) -> void:
	var head_c: Vector2 = parts.to_global(Vector2(0, -float(t["head"]["cy"])))
	if world.distance_to(head_c) <= float(t["head"]["w"]) * 0.55 * global_scale.x:
		next_emotion()
	else:
		on_tap()
	tapped.emit(self)


func on_tap() -> void:
	AudioBus.play_sfx("tap")
	set_emotion("laugh")
	_bounce()


func _bounce() -> void:
	if not is_inside_tree():
		return
	var tw: Tween = create_tween()
	tw.tween_property(parts, "scale", Vector2(1.05, 0.95), 0.07)
	tw.tween_property(parts, "scale", Vector2.ONE, 0.16).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


# ---------------------------------------------------------------- Maße, Treffer, Schatten

func apply_world_size() -> void:
	_draw_size = Vector2(def.width_cm, def.height_cm)
	queue_redraw()


## Rechteck = Hülle aller sichtbaren Ebenen (hängt von der Pose ab).
func local_rect() -> Rect2:
	if not _rect_cache.has_area():
		_rect_cache = LayerGeometry.bounds(self, _layers.values())
	return _rect_cache


func global_rect() -> Rect2:
	var r: Rect2 = local_rect()
	return Rect2(to_global(r.position), r.size * global_scale.abs())


func hit_test(global_point: Vector2, min_size_world: float) -> bool:
	return global_rect().grow(min_size_world * 0.25).has_point(global_point) \
		and LayerGeometry.alpha_hit(_layers.values(), global_point)


func _draw() -> void:
	if body_pose != "stand" or Seats.seat_host_of(self) != null:
		return
	var w: float = float(t["torso"]["w_bot"]) * (1.3 + 0.3 * lifted)
	var col := Color(0.15, 0.1, 0.05, 0.2 * (1.0 - 0.5 * lifted))
	draw_set_transform(Vector2(0, 0), 0.0, Vector2(1.0, 0.16))
	draw_circle(Vector2.ZERO, w * 0.5, col)
	draw_set_transform(Vector2.ZERO)
