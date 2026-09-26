class_name SpriteCharacter
extends ItemNode
## Fertig gemalte Figur (Referenz-Mädchen char_girl_01, Stil C) – nur Stehen, eine Hand (Bild rechts).
## Hand-Trick (P03-T04): HandSlot am Griffpunkt der Faust, darüber ein Overlay mit NUR der Faust
## (gleiche Leinwand) → Finger liegen über dem Item: Körper < Item < Finger.

const SPRITE_DIR: String = "res://assets/characters/sprite/"

var meta: Dictionary
var body: Node2D                     ## Körper + HandSlot + Faust – gehen zusammen hoch
var slot_front: Node2D
var hand_overlay: Sprite2D


static func create_sprite_character(sprite_id: String) -> SpriteCharacter:
	var c := SpriteCharacter.new()
	c.meta = JSON.parse_string(FileAccess.get_file_as_string(SPRITE_DIR + sprite_id + ".json"))
	var def := ItemDefinition.new()
	def.id = StringName(sprite_id)
	def.scale_ref = String(c.meta["scale_ref"])
	def.height_cm = ItemDB.height_cm(def.scale_ref)
	def.width_cm = ItemDB.width_cm(def.scale_ref)
	def.category = "character"
	def.placement = "floor"
	def.sprite_path = SPRITE_DIR + sprite_id + ".png"
	c.setup(def)
	return c


func _build_visual() -> void:
	body = Node2D.new()
	body.name = "Body"
	add_child(body)
	sprite = Sprite2D.new()
	sprite.name = "Sprite"
	sprite.centered = false
	sprite.texture = load(def.sprite_path)
	body.add_child(sprite)
	slot_front = Node2D.new()
	slot_front.name = "HandSlotFront"
	body.add_child(slot_front)
	hand_overlay = Sprite2D.new()
	hand_overlay.name = "HandOverlay"
	hand_overlay.centered = false
	hand_overlay.texture = load(String(def.sprite_path).replace(".png", "_hand.png"))
	hand_overlay.visible = false
	body.add_child(hand_overlay)


func lift_node() -> Node2D:
	return body


func apply_world_size() -> void:
	super.apply_world_size()
	hand_overlay.scale = sprite.scale
	hand_overlay.offset = sprite.offset
	var g: Array = meta["grip_px"]
	slot_front.position = (Vector2(float(g[0]), float(g[1])) + sprite.offset) * sprite.scale


func child_roots() -> Array[Node]:
	return [on_top_root, contents_root, slot_front]


func hand_slots() -> Array[Dictionary]:
	if held_item() != null:
		return []
	return [{"slot": slot_front, "index": 0, "global": slot_front.global_position}]


func held_item(_index: int = 0) -> ItemNode:
	for c: Node in slot_front.get_children():
		if c is ItemNode:
			return c
	return null


func hold_rotation_for(_index: int, item: ItemNode) -> float:
	return global_rotation + deg_to_rad(item.def.hold_angle)


func refresh_pose(_animate: bool = true) -> void:
	var it: ItemNode = held_item()
	slot_front.rotation = deg_to_rad(it.def.hold_angle) if it else 0.0
	hand_overlay.visible = it != null


func on_placed() -> void:
	refresh_pose(false)
