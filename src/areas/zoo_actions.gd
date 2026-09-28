class_name ZooActions
extends RefCounted
## P10g Zoo (AreaActions ruft on_dropped/on_tapped, AreaScene ruft tick/refresh):
##   Füttern   : Futter neben ein Tier legen → richtiges Futter (Tag „eats:<ID-Präfix>“) = frisst, freut sich (Herzen),
##               falsches Futter = dreht sich weg, das Futter bleibt liegen
##   Pfleger/in: alle 90 s eine Fütterungsrunde (legt jedem Tier im Raum sein Futter hin, das Tier frisst es)
##   Affen     : („steals“) nehmen alle 45 s ein kleines Ding vom Boden und legen es woanders hin
##   Streicheln: Streichelzoo-Tiere („pettable“) antippen → Herzen

const FEED_CM: float = 140.0
const FEED_EVERY_S: float = 90.0
const STEAL_EVERY_S: float = 45.0
const STEAL_CM: float = 400.0
const CHECK_S: float = 0.5

static var _animals: Array = []
static var _feed_t: float = 0.0
static var _steal_t: float = 0.0
static var _check_t: float = 0.0


static func refresh(room: Room) -> void:
	_animals.clear()
	if room == null:
		return
	for it: ItemNode in Placement.all_items(room):
		if it is PetNode and it.def.tags.has("zoo"):
			_animals.append(it)


static func diet(animal: ItemNode) -> Array:
	var out: Array = []
	for t: Variant in animal.def.tags:
		if String(t).begins_with("eats:"):
			out.append(String(t).substr(5))
	return out


static func likes(animal: ItemNode, food: ItemNode) -> bool:
	for p: String in diet(animal):
		if String(food.def.id).begins_with(p):
			return true
	return false


static func is_food(it: ItemNode) -> bool:
	var id: String = String(it.def.id)
	return it.def.tags.has("zoo_food") or it.def.category == "food" or id.begins_with("food_")


## Nächstes Zoo-Tier neben p (gleiche Tiefe), sonst null.
static func animal_near(room: Room, p: Vector2) -> ItemNode:
	var best: ItemNode = null
	var best_d: float = INF
	for it: ItemNode in Placement.all_items(room):
		if not (it is PetNode) or not it.def.tags.has("zoo"):
			continue
		var dx: float = absf(it.position.x - p.x) - it.def.width_cm * 0.5
		if dx < FEED_CM and absf(it.position.y - p.y) < 80.0 and dx < best_d:
			best_d = dx
			best = it
	return best


static func on_dropped(scene: AreaScene, item: ItemNode) -> bool:
	if not is_food(item) or item.get_parent() != scene.room.ysort_root:
		return false
	var a: ItemNode = animal_near(scene.room, item.position)
	if a == null:
		return false
	if likes(a, item):
		feed(a, item)
		return true
	refuse(a)
	return false


static func on_tapped(_scene: AreaScene, item: ItemNode) -> bool:
	if item is PetNode and item.def.tags.has("pettable"):
		_hearts(item)
		Secrets.event("petting")
	return false                                     # Laut + Hüpfer macht das Tier selbst


static func feed(animal: ItemNode, food: ItemNode) -> void:
	if food.get_parent() != null:
		food.get_parent().remove_child(food)
	food.queue_free()
	AudioBus.play_sfx("yum")
	AudioBus.play_animal(String(animal.def.sfx.get("voice", "tap")))
	if animal.has_method("_bounce"):
		animal.call("_bounce")
	_hearts(animal)
	animal.set_meta("fed", true)
	Secrets.event("feed")
	if String(animal.def.id).begins_with("zoo_elephant"):
		Secrets.event("feed_elephant")


static func refuse(animal: ItemNode) -> void:
	AudioBus.play_sfx("deny")
	if animal is PetNode:
		(animal as PetNode).sprite.flip_h = not (animal as PetNode).sprite.flip_h     # dreht sich weg


static func tick(scene: AreaScene, dt: float) -> void:
	if _animals.is_empty():
		return
	_check_t += dt
	if _check_t < CHECK_S:
		return
	var step: float = _check_t
	_check_t = 0.0
	_feed_t += step
	_steal_t += step
	if _feed_t >= FEED_EVERY_S:
		_feed_t = 0.0
		feeding_round(scene.room)
	if _steal_t >= STEAL_EVERY_S:
		_steal_t = 0.0
		for a: Variant in _animals:
			if is_instance_valid(a) and (a as ItemNode).def.tags.has("steals"):
				steal(scene.room, a)
				break
	_eat_lying_food(scene.room)


## Tiere fressen passendes Futter, das nah genug auf dem Boden liegt (z. B. von der Pflegerin hingelegt).
static func _eat_lying_food(room: Room) -> void:
	for f: Node in room.ysort_root.get_children():
		if not (f is ItemNode) or not is_food(f as ItemNode) or (f as ItemNode).lifted > 0.0:
			continue
		var a: ItemNode = animal_near(room, (f as ItemNode).position)
		if a != null and likes(a, f as ItemNode):
			feed(a, f as ItemNode)


## Pfleger/in im Raum: jedem Tier sein erstes Futter hinlegen. Gibt die Zahl der Portionen zurück.
static func feeding_round(room: Room) -> int:
	var keeper: NpcBrain = null
	for b: NpcBrain in NpcSpawner.brains(room):
		if String(b.role.get("id", "")) == "zookeeper":
			keeper = b
	if keeper == null:
		return 0
	keeper.play_work("feed")
	var n: int = 0
	for a: Variant in _animals:
		if not is_instance_valid(a) or diet(a).is_empty():
			continue
		var an: ItemNode = a
		var fid: StringName = _food_item(String(diet(an)[0]))
		if fid == &"":
			continue
		var x: float = clampf(an.position.x + an.def.width_cm * 0.5 + 20.0, 20.0, room.width_cm - 20.0)
		ItemSpawner.on_floor(room, fid, x, an.position.y)
		n += 1
	Secrets.event("feeding_time")
	return n


## Konkretes Item zu einem Futter-Präfix (erste Variante im Katalog).
static func _food_item(prefix: String) -> StringName:
	for id: Variant in ItemDB.item_ids():
		if String(id).begins_with(prefix):
			return StringName(id)
	return &""


## Affe nimmt ein kleines Ding vom Boden und legt es woanders hin.
static func steal(room: Room, monkey: ItemNode) -> ItemNode:
	var loot: ItemNode = null
	for it: Node in room.ysort_root.get_children():
		if it is ItemNode and not (it is PetNode) and not (it is CharacterRig) and (it as ItemNode).def.hold == "one_hand" \
				and (it as ItemNode).def.height_cm <= 30.0 and absf((it as ItemNode).position.x - monkey.position.x) < STEAL_CM:
			loot = it
			break
	if loot == null:
		return null
	var dest := Vector2(clampf(monkey.position.x + (260.0 if loot.position.x < monkey.position.x else -260.0), 30.0,
		room.width_cm - 30.0), clampf(loot.position.y + 10.0, room.floor_band.back_y_cm, room.floor_band.front_y_cm))
	AudioBus.play_animal(String(monkey.def.sfx.get("voice", "monkey")))
	Secrets.event("monkey_steal")
	if not loot.is_inside_tree() or Settings.reduced_motion:
		loot.position = dest
	else:
		var tw: Tween = loot.create_tween()
		tw.tween_property(loot, "position", monkey.position + Vector2(0, -monkey.def.height_cm * 0.5), 0.6)
		tw.tween_property(loot, "position", dest, 0.9).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	return loot


static func _hearts(it: ItemNode) -> void:
	if not it.is_inside_tree():
		return
	var p := CPUParticles2D.new()
	p.amount = 6
	p.one_shot = true
	p.explosiveness = 0.6
	p.lifetime = 1.2
	p.position = Vector2(0, -it.def.height_cm)
	p.direction = Vector2.UP
	p.spread = 35.0
	p.initial_velocity_min = 40.0
	p.initial_velocity_max = 80.0
	p.gravity = Vector2(0, -20)
	p.scale_amount_min = 4.0
	p.scale_amount_max = 6.0
	p.color = Color("#f0708a")
	it.add_child(p)
	p.emitting = true
	p.finished.connect(p.queue_free)
