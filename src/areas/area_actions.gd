class_name AreaActions
extends RefCounted
## P09: Spiel-Aktionen der Einkaufsstraße und des Spielplatzes (AreaScene ruft nur on_dropped/on_tapped).
##   Modeladen  : Kleidungsstück in die Hand einer Figur → sie zieht es an (Editor-Teile, Farbe vom Item)
##   Friseur    : Figur sitzt im Friseurstuhl, Stuhl antippen → neue Frisur (Friseur/in schneidet)
##   Rutsche    : Figur am Turm der Rutsche absetzen → rutscht die Bahn hinunter und landet davor
##   Sandkasten : Förmchen auf den Sandkasten → Sandfigur (Stern/Fisch/Burg wie das Förmchen)
##   Seifenblasen / Bushaltestelle (Bus kommt, zurück zur Stadtkarte)
##   Arztpraxis (P10b): Pflaster, Armschlinge, Augenklappe in die Hand → Figur wird verarztet (Slot „aid“)

const WEAR: Dictionary = {                    ## Item-Präfix → [Slot, Teil]
	"cloth_shirt": ["top", "shirt"], "cloth_dress": ["top", "dress"], "cloth_jacket": ["top", "jacket"],
	"cloth_raincoat": ["top", "raincoat"], "cloth_pants": ["bottom", "trousers"], "cloth_shoes": ["shoes", "sneaker"],
	"cloth_boots": ["shoes", "boot"], "cloth_slippers": ["shoes", "slipper"], "cloth_hat": ["accessory", "sunhat"],
	"cloth_cap": ["accessory", "cap"], "cloth_beanie": ["accessory", "beanie"], "cloth_sunglasses": ["accessory", "sunglasses"],
	"cloth_scarf": ["top", "sweater"],
	"spc_tutu": ["bottom", "tutu"], "sport_skates": ["shoes", "boot"], "spc_ballet_shoes": ["shoes", "ballet"],
	"health_bandage": ["aid", "plaster"], "med_sling": ["aid", "arm_sling"], "med_eye_patch": ["aid", "eye_patch"],
}
const SLIDE_S: float = 1.1
const INSTRUMENTS: Array = ["drum_hit", "piano_note", "xylophone", "guitar", "violin", "flute", "triangle", "tambourine"]
const BAND_S: float = 6.0                      ## 3 verschiedene Instrumente in 6 s = Band spielt

static var _band: Dictionary = {}              ## Instrument-Ton → Zeitpunkt (s)
const BUS_ID: StringName = &"street_bus_butter"


## Ding losgelassen. true = hier erledigt (AreaScene speichert dann nur noch).
static func on_dropped(scene: AreaScene, item: ItemNode) -> bool:
	if PoolActions.on_dropped(scene, item) or FairActions.on_dropped(scene, item) or SportActions.on_dropped(scene, item) \
			or IceActions.on_dropped(scene, item):
		return true
	var id: String = String(item.def.id)
	for p: String in WEAR:
		if id.begins_with(p):
			var rig: CharacterRig = _holder(item)
			if rig != null:
				wear(scene, rig, item)
				return true
	if item is CharacterRig:
		var tower: ItemNode = slide_at(scene.room, item)
		if tower != null:
			slide(scene, item as CharacterRig, tower)
			return true
	if id.begins_with("play_sand_mold") and _host_or_near(scene.room, item, "garden_sandbox") != null:
		mold(scene.room, item)
		return true
	return false


static func on_tapped(scene: AreaScene, item: ItemNode) -> bool:
	if PoolActions.on_tapped(scene, item) or FairActions.on_tapped(scene, item) or SportActions.on_tapped(scene, item):
		return true
	var id: String = String(item.def.id)
	if id.begins_with("edu_bell") and item.state == "ring":
		school_bell(scene.room)
		return true
	if id.begins_with("edu_skeleton"):
		AudioBus.play_sfx("dice_roll")
		Secrets.event("skeleton")
		return true
	if item.def.sfx.has("tap") and INSTRUMENTS.has(String(item.def.sfx["tap"])):
		return band(scene.room, String(item.def.sfx["tap"]))
	if id.begins_with("shop_barber_chair"):
		return new_hair(scene, item)
	if id.begins_with("play_bubble_wand"):
		bubbles(item)
		return true
	if id.begins_with("street_bus_stop"):
		bus(scene, item)
		return true
	return false


# ---------------------------------------------------------------- Modeladen

static func wear(scene: AreaScene, rig: CharacterRig, item: ItemNode) -> void:
	var id: String = String(item.def.id)
	var what: Array = []
	for p: String in WEAR:
		if id.begins_with(p):
			what = WEAR[p]
	var slot: String = String(what[0])
	var cols: Array = []
	for c: Color in item.def.colors:
		cols.append("#" + c.to_html(false))
	while cols.size() < 3:
		cols.append(String(rig.look.get("skin", "#f2c9a8")))
	if slot != "accessory":
		cols[2] = String(rig.look.get("skin", cols[2]))        # Zone 3 = Haut (Arme/Beine) wie im Editor
	var look: Dictionary = rig.look.duplicate(true)
	var parts: Dictionary = Dictionary(look.get("parts", {}))
	var colors: Dictionary = Dictionary(look.get("colors", {}))
	parts[slot] = String(what[1])
	colors[slot] = cols
	look["parts"] = parts
	look["colors"] = colors
	rig.apply_look(look)
	if rig == scene.me:                                        # eigene Figur: bleibt so (Speicherstand)
		var cd: CharacterData = Game.active_character()
		if cd != null:
			if cd.outfit >= 0 and cd.outfit < cd.outfits.size() and not Dictionary(cd.outfits[cd.outfit]).is_empty():
				cd.outfits[cd.outfit] = {"parts": parts.duplicate(true), "colors": colors.duplicate(true)}
			else:
				cd.parts = parts.duplicate(true)
				cd.colors = colors.duplicate(true)
			Game.mark_dirty()
	if item.get_parent() != null:
		item.get_parent().remove_child(item)
	item.queue_free()
	rig.refresh_pose(false)
	rig.set_emotion("laugh")
	AudioBus.play_sfx("harvest")
	Secrets.event("patched" if slot == "aid" else "tutu" if String(what[1]) == "tutu" else "wear")


# ---------------------------------------------------------------- Friseur

static func new_hair(scene: AreaScene, chair: ItemNode) -> bool:
	var rig: CharacterRig = null
	for i: int in chair.def.seat_slots:
		if Seats.occupant(chair, i) is CharacterRig:
			rig = Seats.occupant(chair, i)
	if rig == null:
		return false
	var styles: Array = CharacterParts.ids("hair")
	var look: Dictionary = rig.look.duplicate(true)
	var parts: Dictionary = Dictionary(look.get("parts", {}))
	var cur: int = styles.find(String(parts.get("hair", "")))
	parts["hair"] = String(styles[(cur + 1) % styles.size()])
	look["parts"] = parts
	rig.apply_look(look)
	rig.set_emotion("surprised")
	if rig == scene.me and Game.active_character() != null:
		Game.active_character().parts["hair"] = parts["hair"]
		Game.mark_dirty()
	for b: NpcBrain in NpcSpawner.brains(scene.room):
		if String(b.role.get("id", "")) == "hairdresser":
			b.play_work("cut")
	AudioBus.play_sfx("dice_roll")
	Secrets.event("haircut")
	return true


# ---------------------------------------------------------------- Schule (P10a)

## Schulglocke: Pause! Die Schulkinder jubeln und winken, die Lehrer klatschen.
static func school_bell(room: Room) -> int:
	var n: int = 0
	for b: NpcBrain in NpcSpawner.brains(room):
		var rid: String = String(b.role.get("id", ""))
		if rid.begins_with("pupil"):
			b.play_work("wave")
			b.body.set_emotion("laugh")
			n += 1
		elif rid.ends_with("teacher") or rid == "principal":
			b.play_work("clap")
	return n


## Instrument angetippt: 3 verschiedene in kurzer Zeit → „Band": alle klatschen, Sticker.
static func band(room: Room, sound: String) -> bool:
	var now: float = Time.get_ticks_msec() / 1000.0
	_band[sound] = now
	var recent: int = 0
	for k: String in _band:
		if now - float(_band[k]) <= BAND_S:
			recent += 1
	if recent < 3:
		return false
	_band.clear()
	for b: NpcBrain in NpcSpawner.brains(room):
		b.play_work("clap")
	Secrets.event("band")
	return true


# ---------------------------------------------------------------- Spielplatz

## Figur am Turm der Rutsche abgesetzt? (Figuren stehen nie auf Flächen – der Turm-Bereich zählt.)
static func slide_at(room: Room, rig: ItemNode) -> ItemNode:
	if rig.get_parent() != room.ysort_root:
		return null
	for o: ItemNode in Placement.all_items(room):
		if String(o.def.id).begins_with("play_tower_slide"):
			var left: float = o.position.x - o.def.width_cm * 0.5
			if rig.position.x >= left - 10.0 and rig.position.x <= left + o.def.width_cm * 0.22 \
					and absf(rig.position.y - o.position.y) < 40.0:
				return o
	return null


## Figur rutscht vom Turm die Bahn hinunter und steht danach vor dem Ende der Rutsche.
static func slide(scene: AreaScene, rig: CharacterRig, s: ItemNode) -> void:
	var room: Room = scene.room
	var top := Vector2(s.position.x - s.def.width_cm * 0.38, s.position.y - s.def.height_cm * 0.52)
	var end: Vector2 = NpcPath.clamp_to_room(room, Vector2(s.position.x + s.def.width_cm * 0.5 + 30.0, s.position.y + 6.0))
	AudioBus.play_sfx("grow")
	rig.set_emotion("laugh")
	Secrets.event("slide")
	if not rig.is_inside_tree() or Settings.reduced_motion:
		rig.position = end
		return
	rig.z_index = 1                                            # während der Fahrt vor der Bahn
	var tw: Tween = rig.create_tween()
	tw.tween_method(func(k: float) -> void:
		var x: float = lerpf(top.x, end.x, k)
		var y: float = lerpf(top.y, end.y, 1.0 - pow(1.0 - k, 2.2))   # erst steil, dann flach (Kurve der Bahn)
		rig.position = Vector2(x, y), 0.0, 1.0, SLIDE_S).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_callback(func() -> void:
		rig.z_index = 0
		rig.position = end
		rig.scale = Vector2.ONE * room.floor_band.depth_factor(end.y))


## Förmchen auf dem Sandkasten → Sandfigur in der Form des Förmchens daneben.
static func mold(room: Room, m: ItemNode) -> ItemNode:
	var shape: String = m.state if m.state in ["star", "fish", "castle"] else "star"
	var p: Vector2 = room.ysort_root.to_local(m.global_position)
	var out: ItemNode = ItemSpawner.on_floor(room, StringName("play_sand_shape_%s_sand" % shape), p.x + 24.0, minf(p.y + 4.0,
		room.floor_band.front_y_cm))
	AudioBus.play_sfx("drop_soft")
	if shape == "castle":
		Secrets.event("sand_castle")
	return out


static func bubbles(wand: ItemNode) -> void:
	AudioBus.play_sfx("grow")
	Secrets.event("bubbles")
	if not wand.is_inside_tree():
		return
	var p := CPUParticles2D.new()
	p.name = "Bubbles"
	p.amount = 18
	p.lifetime = 3.0
	p.one_shot = true
	p.explosiveness = 0.2
	p.direction = Vector2(0.4, -1.0)
	p.spread = 35.0
	p.gravity = Vector2(0.0, -12.0)
	p.initial_velocity_min = 20.0
	p.initial_velocity_max = 45.0
	p.color = Color(0.85, 0.95, 1.0, 0.7)
	p.position = Vector2(0.0, -wand.def.height_cm)
	p.texture = _bubble_texture()
	p.scale_amount_min = 0.03
	p.scale_amount_max = 0.08
	wand.add_child(p)
	p.emitting = true
	p.finished.connect(p.queue_free)


static func _bubble_texture() -> Texture2D:
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 0.15))
	g.add_point(0.8, Color(1, 1, 1, 0.9))
	g.set_color(1, Color(1, 1, 1, 0))
	var t := GradientTexture2D.new()
	t.gradient = g
	t.fill = GradientTexture2D.FILL_RADIAL
	t.fill_from = Vector2(0.5, 0.5)
	t.fill_to = Vector2(1.0, 0.5)
	t.width = 128
	t.height = 128
	return t


## Bushaltestelle antippen: Bus fährt vor, hupt, danach geht es zurück zur Stadtkarte.
static func bus(scene: AreaScene, stop: ItemNode) -> ItemNode:
	var room: Room = scene.room
	var b: ItemNode = ItemSpawner.on_floor(room, BUS_ID, room.width_cm + 300.0, minf(stop.position.y + 30.0, room.floor_band.front_y_cm))
	if b == null:
		return null
	b.set_meta("transient", true)                              # nicht speichern
	AudioBus.play_sfx("bus_horn")
	Secrets.event("bus")
	if not scene.is_inside_tree() or Settings.reduced_motion:
		b.position.x = stop.position.x
		return b
	var tw: Tween = b.create_tween()
	tw.tween_property(b, "position:x", stop.position.x, 1.6).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
	tw.tween_interval(0.9)
	tw.tween_callback(scene.leave)
	return b


# ---------------------------------------------------------------- Hilfen

static func _holder(item: ItemNode) -> CharacterRig:
	var n: Node = item.get_parent()
	while n != null and not (n is Room):
		if n is CharacterRig:
			return n
		n = n.get_parent()
	return null


static func _host_id(item: ItemNode) -> String:
	var n: Node = item.get_parent()
	while n != null and not (n is Room):
		if n is ItemNode:
			return String((n as ItemNode).def.id)
		n = n.get_parent()
	return ""


static func _host_or_near(room: Room, item: ItemNode, prefix: String) -> ItemNode:
	if _host_id(item).begins_with(prefix):
		return item.get_parent().get_parent() as ItemNode
	for o: ItemNode in Placement.all_items(room):
		if String(o.def.id).begins_with(prefix) and absf(o.global_position.x - item.global_position.x) < o.def.width_cm * 0.5 \
				and absf(o.global_position.y - item.global_position.y) < 60.0:
			return o
	return null
