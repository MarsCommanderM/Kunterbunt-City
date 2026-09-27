class_name Garden
extends RefCounted
## P07-T07: Garten zum Spielen – säen, gießen, wachsen, ernten; Blumen welken ohne Wasser.
##   Samentüte aufs leere Beet ziehen   → Beet keimt ("sprout"), die Tüte ist verbraucht.
##   Gießkanne aufs Beet ziehen         → Beet/Blumen/Kübel sind nass (dunklere Erde). Rasensprenger (an) gießt im Umkreis.
##   Nasses Beet wächst alle GROW_S eine Stufe: sprout → grown → ripe. Trockenes Beet wartet (wächst nicht).
##   Reifes Beet antippen               → Ernte fällt davor auf den Boden, Beet ist wieder leer.
##   Blumenbeet ohne Wasser nach DRY_S  → welk ("dry"); gießen macht es wieder frisch.
## Zeit = echte Uhrzeit (Unix) → der Garten wächst auch, während das Kind woanders spielt (Zeitstempel im Raumzustand).

const GROW_S: float = 45.0            ## Sekunden je Wachstums-Stufe (kindgerecht schnell)
const WET_S: float = 150.0            ## so lange hält einmal Gießen
const DRY_S: float = 240.0            ## Blumen welken nach 4 min ohne Wasser
const SPRINKLER_CM: float = 260.0     ## Reichweite des Rasensprengers
const REACH_CM: float = 40.0          ## Gießkanne/Samen: so nah muss es am Beet landen (zusätzlich zur Beet-Breite)
const WET_TINT: Color = Color(0.86, 0.9, 1.0)
const CROPS: Dictionary = {           ## Beet-Sorte → Ernte (Item-ID, Anzahl)
	"carrot": ["food_carrot_orange", 3], "tomato": ["food_tomato_rust", 4], "lettuce": ["food_lettuce_green", 2],
	"strawberry": ["food_strawberry_red", 5], "pumpkin": ["food_pumpkin_orange", 1],
	"sunflower": ["plant_sunflower_terracotta_terracotta", 1],
}

## Test-Uhr: ≥ 0 = feste Zeit (Tests/Beweisbilder). Bewusst KEINE Lambda in einer statischen Variable –
## die überlebt ihr Skript und ließ Godot beim Beenden abstürzen („corrupted size vs. prev_size").
static var fixed_now: float = -1.0


static func now() -> float:
	return fixed_now if fixed_now >= 0.0 else Time.get_unix_time_from_system()


static func is_bed(it: ItemNode) -> bool:
	return it.def.tags.has("bed") and it.def.states.has("ripe")


static func is_flowers(it: ItemNode) -> bool:
	return it.def.tags.has("bed") and it.def.states.has("dry")


static func needs_water(it: ItemNode) -> bool:
	return it.def.tags.has("needs_water")


static func crop_of(it: ItemNode) -> String:
	var id: String = String(it.def.id)
	for c: String in CROPS:
		if id.contains("_" + c):
			return c
	return "carrot"


static func is_wet(it: ItemNode, at: float = -1.0) -> bool:
	var t: float = now() if at < 0.0 else at
	return it.has_meta("water_t") and t - float(it.get_meta("water_t")) < WET_S


## Tippen: reifes Beet → ernten (true = erledigt, sonst normales Weiterschalten verhindern).
static func handles_tap(it: ItemNode) -> bool:
	return is_bed(it) or is_flowers(it)


static func on_tap(it: ItemNode) -> void:
	if is_bed(it) and it.state == "ripe":
		harvest(it)
		return
	AudioBus.play_sfx("tap")
	if it.is_inside_tree() and not Settings.reduced_motion:
		var tw: Tween = it.create_tween()
		tw.tween_property(it.sprite, "rotation", 0.03, 0.06)
		tw.tween_property(it.sprite, "rotation", -0.03, 0.12)
		tw.tween_property(it.sprite, "rotation", 0.0, 0.06)


## Ein Ding wurde losgelassen: Samen säen oder gießen. true = Garten hat es verarbeitet.
static func on_drop(room: Room, item: ItemNode) -> bool:
	if item.def.tags.has("seeds"):
		var bed: ItemNode = _nearest(room, item, func(o: ItemNode) -> bool: return is_bed(o) and o.state == "empty")
		if bed == null:
			return false
		sow(bed)
		if item.get_parent() != null:                      # Tüte ist verbraucht (sofort raus → nicht im Raumzustand)
			item.get_parent().remove_child(item)
		item.queue_free()
		return true
	if String(item.def.id).begins_with("garden_watering_can"):
		var n: int = 0
		for o: ItemNode in Placement.all_items(room):
			if o != item and needs_water(o) and _close(o, item):
				water(o)
				n += 1
		return n > 0
	return false


static func sow(bed: ItemNode) -> void:
	bed.set_meta("grow_t", now())
	ItemStates.set_state(bed, "sprout", true)
	AudioBus.play_sfx("grow")
	_refresh_tint(bed)


static func water(it: ItemNode) -> void:
	var t: float = now()
	it.set_meta("water_t", t)
	if is_bed(it) and it.state in ["sprout", "grown"] and not it.has_meta("grow_t"):
		it.set_meta("grow_t", t)
	if is_flowers(it) and it.state == "dry":
		ItemStates.set_state(it, String(it.def.states[0]), true)
	AudioBus.play_sfx("water_pour")
	_refresh_tint(it)


static func harvest(bed: ItemNode) -> Array:
	var out: Array = []
	var crop: Array = CROPS.get(crop_of(bed), CROPS["carrot"])
	var room: Room = _room_of(bed)
	if room != null:
		var n: int = int(crop[1])
		for k: int in n:
			var x: float = bed.position.x + (float(k) - (n - 1) * 0.5) * 22.0
			var it: ItemNode = ItemSpawner.on_floor(room, StringName(String(crop[0])), x, bed.position.y + 14.0)
			if it != null:
				out.append(it)
	if bed.has_meta("grow_t"):
		bed.remove_meta("grow_t")
	ItemStates.set_state(bed, "empty", true)
	AudioBus.play_sfx("harvest")
	Secrets.event("harvest")                             # P07-T10: erste Ernte = Sticker
	return out


## Zeit vergeht: Beete wachsen (wenn nass), Blumen welken (wenn lange trocken), Sprenger gießen.
## Gibt die Zahl der Änderungen zurück. Mehrere Stufen auf einmal (nach langer Abwesenheit) → catch_up.
static func tick(room: Room, at: float = -1.0) -> int:
	var t: float = now() if at < 0.0 else at
	var items: Array = Placement.all_items(room)
	var changed: int = 0
	for s: ItemNode in items:                               # Rasensprenger zuerst
		if String(s.def.id).begins_with("garden_sprinkler") and s.state == "on":
			for o: ItemNode in items:
				if needs_water(o) and absf(o.position.x - s.position.x) < SPRINKLER_CM and not is_wet(o, t):
					o.set_meta("water_t", t)
					if is_flowers(o) and o.state == "dry":
						ItemStates.set_state(o, String(o.def.states[0]), true)
					changed += 1
	for o: ItemNode in items:
		if is_bed(o) and o.state in ["sprout", "grown"]:
			var g: float = float(o.get_meta("grow_t", t))
			if not o.has_meta("grow_t"):
				o.set_meta("grow_t", t)
			if is_wet(o, t) and t - g >= GROW_S:
				ItemStates.set_state(o, "grown" if o.state == "sprout" else "ripe", true)
				o.set_meta("grow_t", g + GROW_S)
				AudioBus.play_sfx("grow")
				changed += 1
		elif is_flowers(o) and o.state != "dry":
			var w: float = float(o.get_meta("water_t", -1.0))
			if w < 0.0:
				o.set_meta("water_t", t)                   # frisch gepflanzt = frisch gegossen
			elif t - w > DRY_S:
				ItemStates.set_state(o, "dry", true)
				changed += 1
		if needs_water(o):
			_refresh_tint(o, t)
	return changed


static func catch_up(room: Room, at: float = -1.0) -> int:
	var total: int = 0
	for i: int in 4:
		var n: int = tick(room, at)
		total += n
		if n == 0:
			break
	return total


static func _refresh_tint(it: ItemNode, at: float = -1.0) -> void:
	it.sprite.self_modulate = WET_TINT if is_wet(it, at) else Color.WHITE


static func _close(o: ItemNode, item: ItemNode) -> bool:
	var half: float = o.global_rect().size.x / maxf(o.global_scale.x, 0.001) * 0.5
	return absf(item.position.x - o.position.x) <= half + REACH_CM and absf(item.position.y - o.position.y) <= 80.0


static func _nearest(room: Room, item: ItemNode, ok: Callable) -> ItemNode:
	var best: ItemNode = null
	var bd: float = INF
	for o: ItemNode in Placement.all_items(room):
		if o == item or not bool(ok.call(o)) or not _close(o, item):
			continue
		var d: float = absf(item.position.x - o.position.x)
		if d < bd:
			bd = d
			best = o
	return best


static func _room_of(n: Node) -> Room:
	while n != null and not (n is Room):
		n = n.get_parent()
	return n as Room
