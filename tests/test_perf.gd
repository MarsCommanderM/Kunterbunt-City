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
