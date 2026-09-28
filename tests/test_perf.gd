extends GutTest
## Leistung (Tech-Spec §5): 250 Items in einem Raum. Ehrliche Messung – headless/llvmpipe, also Richtwert.
## Ruhe-Items ticken nicht; Greifen (Treffertest über alle Items) bleibt deutlich unter einem Frame.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func test_250_items_spawn_and_pick_fast() -> void:
	var ids: Array = ItemDB.item_ids().filter(func(id: StringName) -> bool: return ItemDB.get_item(id).movable)
	var t0: int = Time.get_ticks_usec()
	for i: int in 250:
		ItemSpawner.on_floor(k.room, ids[i % ids.size()], 20.0 + (i * 37) % 680, float((i * 13) % 70))
	var spawn_ms: float = (Time.get_ticks_usec() - t0) / 1000.0
	assert_eq(Placement.all_items(k.room).size(), 250)
	# Erster Griff je Textur baut einmal die Treffer-Maske (BitMap) – mit 250 VERSCHIEDENEN Katalog-Items
	# gehört das nicht in die Dauer-Messung (wie das Aufwärmen bei find_target). Einmal-Kosten extra melden.
	var tw: int = Time.get_ticks_usec()
	for i: int in 100:
		k.drag.pick_item(Vector2(20.0 + i * 7.0, -20.0))
	var warm_ms: float = (Time.get_ticks_usec() - tw) / 1000.0
	var t1: int = Time.get_ticks_usec()
	var hits: int = 0
	for i: int in 100:
		if k.drag.pick_item(Vector2(20.0 + i * 7.0, -20.0)):
			hits += 1
	var pick_ms: float = (Time.get_ticks_usec() - t1) / 1000.0 / 100.0
	var ball: ItemNode = Placement.all_items(k.room)[0]
	for i: int in 3:      # Aufwärmen (erste Suche lädt noch Texturen/Caches)
		Placement.find_target(k.room, ball, Vector2(100.0, -95.0), Vector2(100.0, -100.0))
	var t2: int = Time.get_ticks_usec()
	for i: int in 20:
		Placement.find_target(k.room, ball, Vector2(100.0 + i * 20.0, -95.0), Vector2(100.0 + i * 20.0, -100.0))
	var place_ms: float = (Time.get_ticks_usec() - t2) / 1000.0 / 20.0
	gut.p("PERF 250 Items: spawn %.1f ms · Masken-Aufbau einmalig %.1f ms · pick %.3f ms · find_target %.3f ms (Treffer %d/100)"
		% [spawn_ms, warm_ms, pick_ms, place_ms, hits])
	assert_lt(pick_ms, 4.0, "Greifen < 4 ms (Ziel auf Gerät < 1 ms)")
	assert_lt(place_ms, 4.0, "Ziel finden < 4 ms")
	for it: ItemNode in Placement.all_items(k.room):
		assert_false(it.is_processing())


## P08-T10: 250 Items + 15 aktive Figuren/Tiere (10 NPCs verschiedener Rollen + 5 Tiere) – Logik je Frame.
func test_15_active_npcs_and_pets_with_250_items() -> void:
	NpcBrain.autonomous = false
	var ids: Array = ItemDB.item_ids().filter(func(id: StringName) -> bool: return ItemDB.get_item(id).movable)
	for i: int in 250:
		ItemSpawner.on_floor(k.room, ids[i % ids.size()], 20.0 + (i * 37) % 680, float((i * 13) % 70))
	ItemSpawner.on_floor(k.room, &"garden_pool_frame_s_sky", 380.0, 30.0)
	var brains: Array = []
	var roles: Array = ["cashier", "lifeguard", "janitor", "teacher", "coach", "passerby", "nurse", "zookeeper",
		"shelf_stocker", "postman"]
	for i: int in roles.size():
		brains.append(NpcSpawner.spawn(k.room, NpcRoles.role(roles[i]),
			{"id": "npc_%d" % i, "role": roles[i], "x_cm": 60.0 + i * 64.0, "y_cm": float((i * 17) % 60)}))
	var pets: Array = []
	for i: int in 5:
		pets.append(ItemSpawner.on_floor(k.room, &"pet_dog_brown", 100.0 + i * 120.0, 40.0))
	var t0: int = Time.get_ticks_usec()
	var frames: int = 120
	for _f: int in frames:
		for b: NpcBrain in brains:
			b.tick(1.0 / 60.0)
		for p: PetNode in pets:
			p.tick(1.0 / 60.0)
	var ms: float = (Time.get_ticks_usec() - t0) / 1000.0 / frames
	gut.p("PERF 15 aktive (10 NPCs + 5 Tiere) + 250 Items: %.3f ms/Frame Logik" % ms)
	assert_lt(ms, 4.0, "KI-Logik < 4 ms je Frame (Budget 16,7 ms)")
	NpcBrain.autonomous = true
