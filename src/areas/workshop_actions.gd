class_name WorkshopActions
extends RefCounted
## P10h Werkstatt (AreaActions ruft on_dropped/on_tapped):
##   Hupe        : Auto antippen → hupt (überall, das Auto gibt es im Katalog für jeden Bereich)
##   Hebebühne   : Hebebühne antippen → steht ein Auto darauf, fährt es mit hoch (Bild), Mechaniker/in repariert
##   Reifenwechsel: Reifen an ein Auto legen → Reifen weg, Auto hüpft („neue Reifen“)
##   Lackieren   : Sprühpistole an ein Auto → Auto bekommt die Farbe der Pistole (gleiches Modell, andere Farbvariante)
##   Waschanlage : Auto in die Waschanlage stellen → Bürsten laufen, Schaum, Auto glänzt
##   Tanken      : Zapfsäule antippen, wenn ein Auto daneben steht → Schlauch am Auto, Geräusch
##   Schrottplatz: Schrotthaufen antippen → goldene Radkappe liegt davor (Geheimnis)

const CARS: Array = ["veh_car_", "garage_scrap_car"]
const NEAR_CM: float = 60.0
const LIFT_UP_CM: float = 140.0


static func is_car(it: ItemNode) -> bool:
	for p: String in CARS:
		if String(it.def.id).begins_with(p):
			return true
	return false


## Auto, das (Mitte) im Bereich des Geräts steht (gleiche Tiefe), sonst null.
static func car_at(room: Room, host: ItemNode, extra_cm: float = 0.0) -> ItemNode:
	for it: ItemNode in Placement.all_items(room):
		if is_car(it) and it.get_parent() == room.ysort_root and absf(it.position.y - host.position.y) < 80.0 \
				and absf(it.position.x - host.position.x) < host.def.width_cm * 0.5 + extra_cm:
			return it
	return null


static func on_tapped(scene: AreaScene, item: ItemNode) -> bool:
	var id: String = String(item.def.id)
	if is_car(item):
		AudioBus.play_sfx("bus_horn")
		Secrets.event("honk")
		return true
	if id.begins_with("garage_car_lift"):
		lift(scene.room, item)
		return true
	if id.begins_with("garage_gas_pump") and item.state == "fuel":
		if car_at(scene.room, item, 250.0) != null:
			Secrets.event("fuel")
		return true
	if id.begins_with("garage_wash_tunnel") and item.state == "on":
		var car: ItemNode = car_at(scene.room, item)
		if car != null:
			wash(car)
		return true
	if id.begins_with("garage_scrap_pile") and item.state == "found":
		var p: Vector2 = scene.room.ysort_root.to_local(item.global_position)
		ItemSpawner.on_floor(scene.room, &"garage_hubcap_gold", p.x + item.def.width_cm * 0.3,
			clampf(p.y + 20.0, scene.room.floor_band.back_y_cm, scene.room.floor_band.front_y_cm))
		Secrets.event("treasure")
		return true
	return false


static func on_dropped(scene: AreaScene, item: ItemNode) -> bool:
	var id: String = String(item.def.id)
	if is_car(item) and item.get_parent() == scene.room.ysort_root:
		for it: ItemNode in Placement.all_items(scene.room):
			if String(it.def.id).begins_with("garage_wash_tunnel") and car_at(scene.room, it) == item:
				ItemStates.set_state(it, "on")
				wash(item)
		return false
	if id.begins_with("garage_spray_gun") or id.begins_with("work_tire"):
		var car: ItemNode = _car_near(scene.room, item)
		if car == null:
			return false
		if id.begins_with("garage_spray_gun"):
			return paint(scene.room, car, item) != null
		_consume(item)
		_hop(car)
		AudioBus.play_sfx("drop_metal")
		Secrets.event("tires")
		return true
	return false


static func _car_near(room: Room, item: ItemNode) -> ItemNode:
	var p: Vector2 = room.ysort_root.to_local(item.global_position)
	for it: ItemNode in Placement.all_items(room):
		if is_car(it) and absf(it.position.x - p.x) < it.def.width_cm * 0.5 + NEAR_CM and absf(it.position.y - p.y) < 80.0:
			return it
	return null


## Hebebühne hoch/runter; ein Auto darauf fährt mit (nur das Bild, gespeichert bleibt der Standplatz).
static func lift(room: Room, l: ItemNode) -> void:
	var car: ItemNode = car_at(room, l)
	var up: bool = l.state == "up"
	if car != null:
		var off := Vector2(0.0, -LIFT_UP_CM if up else 0.0)
		if car.sprite != null:
			if not car.has_meta("sprite_base"):
				car.set_meta("sprite_base", car.sprite.position)
			car.sprite.position = Vector2(car.get_meta("sprite_base")) + off
		car.on_top_root.position = off
		if up:
			for b: NpcBrain in NpcSpawner.brains(room):
				if String(b.role.get("id", "")) == "mechanic":
					b.play_work("repair")
			Secrets.event("lift")


## Gleiches Automodell in der Farbe der Sprühpistole (Variante), an derselben Stelle. Null = Farbe gibt es nicht.
static func paint(room: Room, car: ItemNode, gun: ItemNode) -> ItemNode:
	var colour: String = String(gun.def.id).trim_prefix("garage_spray_gun_")
	var model: String = String(car.def.id).substr(0, String(car.def.id).rfind("_"))
	var new_id := StringName("%s_%s" % [model, colour])
	if not ItemDB.has_item(new_id) or new_id == car.def.id:
		AudioBus.play_sfx("deny")
		return null
	var p: Vector2 = car.position
	car.get_parent().remove_child(car)
	car.queue_free()
	var out: ItemNode = ItemSpawner.on_floor(room, new_id, p.x, p.y)
	AudioBus.play_sfx("fizz")
	Secrets.event("paint")
	return out


static func wash(car: ItemNode) -> void:
	AudioBus.play_sfx("water_pour")
	Secrets.event("wash")
	_hop(car)
	if not car.is_inside_tree():
		return
	var p := CPUParticles2D.new()
	p.amount = 30
	p.one_shot = true
	p.explosiveness = 0.7
	p.lifetime = 1.6
	p.position = Vector2(0, -car.def.height_cm * 0.6)
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	p.emission_rect_extents = Vector2(car.def.width_cm * 0.45, car.def.height_cm * 0.3)
	p.gravity = Vector2(0, -30)
	p.scale_amount_min = 4.0
	p.scale_amount_max = 9.0
	p.color = Color(1, 1, 1, 0.85)
	car.add_child(p)
	p.emitting = true
	p.finished.connect(p.queue_free)


static func _consume(item: ItemNode) -> void:
	if item.get_parent() != null:
		item.get_parent().remove_child(item)
	item.queue_free()


static func _hop(car: ItemNode) -> void:
	if car.has_method("_bounce"):
		car.call("_bounce")
