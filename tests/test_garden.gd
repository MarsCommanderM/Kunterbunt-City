extends GutTest
## P07-T07: Säen → Gießen → Wachsen → Ernten; Blumen welken ohne Wasser; Rasensprenger gießt; Zeit läuft weiter,
## auch wenn das Kind woanders ist (Zeitstempel im Raumzustand). Uhr ist im Test fest (Garden.fixed_now).

var k: KitchenFixture
var now: float = 1000000.0


func before_each() -> void:
	k = KitchenFixture.new(self)
	now = 1000000.0
	Garden.fixed_now = now


func after_each() -> void:
	Garden.fixed_now = -1.0


func _bed() -> ItemNode:
	return ItemSpawner.on_floor(k.room, &"garden_raised_bed_m_carrot_oak", 300.0, 30.0)


func _drop_on(item_id: StringName, target: ItemNode) -> ItemNode:
	var it: ItemNode = ItemSpawner.on_floor(k.room, item_id, target.position.x + 5.0, target.position.y + 5.0)
	assert_not_null(it, String(item_id))
	return it


func test_beet_startet_leer_und_tippen_schaltet_nicht_um() -> void:
	var bed: ItemNode = _bed()
	assert_eq(bed.state, "empty")
	bed.on_tap()
	assert_eq(bed.state, "empty", "leeres Beet wird nicht durch Tippen „reif“")


func test_saeen_giessen_wachsen_ernten() -> void:
	var bed: ItemNode = _bed()
	var seeds: ItemNode = _drop_on(&"garden_seeds_carrot_pack", bed)
	assert_true(Garden.on_drop(k.room, seeds), "Samen landen im Beet")
	assert_eq(bed.state, "sprout", "gesät → Keimling")
	assert_false(seeds.is_inside_tree(), "Samentüte ist verbraucht")
	now += Garden.GROW_S + 1.0
	Garden.fixed_now = now
	assert_eq(Garden.tick(k.room), 0, "ohne Wasser wächst nichts")
	assert_eq(bed.state, "sprout")
	var can: ItemNode = _drop_on(&"garden_watering_can_mint", bed)
	assert_true(Garden.on_drop(k.room, can), "Gießkanne gießt das Beet")
	assert_true(Garden.is_wet(bed))
	assert_eq(bed.sprite.self_modulate, Garden.WET_TINT, "nasse Erde ist dunkler")
	now += Garden.GROW_S + 1.0
	Garden.fixed_now = now
	Garden.tick(k.room)
	assert_eq(bed.state, "grown")
	now += Garden.GROW_S + 1.0
	Garden.fixed_now = now
	Garden.tick(k.room)
	assert_eq(bed.state, "ripe")
	var before: int = Placement.all_items(k.room).size()
	bed.on_tap()                                          # reif antippen = ernten
	assert_eq(bed.state, "empty", "nach der Ernte ist das Beet leer")
	var carrots: int = 0
	for it: ItemNode in Placement.all_items(k.room):
		if String(it.def.id) == "food_carrot_orange":
			carrots += 1
	assert_eq(carrots, 3, "drei Möhren geerntet")
	assert_eq(Placement.all_items(k.room).size(), before + 3)


func test_blumen_welken_ohne_wasser_und_erholen_sich() -> void:
	var fl: ItemNode = ItemSpawner.on_floor(k.room, &"garden_flower_bed_m_rose", 200.0, 30.0)
	Garden.tick(k.room)
	assert_eq(fl.state, "fresh")
	now += Garden.DRY_S + 1.0
	Garden.fixed_now = now
	Garden.tick(k.room)
	assert_eq(fl.state, "dry", "vergessen zu gießen → welk")
	Garden.water(fl)
	assert_eq(fl.state, "fresh", "gießen → wieder frisch")


func test_rasensprenger_giesst_im_umkreis() -> void:
	var bed: ItemNode = _bed()
	Garden.sow(bed)
	var far: ItemNode = ItemSpawner.on_floor(k.room, &"garden_raised_bed_m_tomato_oak", 690.0, 30.0)
	Garden.sow(far)
	var sp: ItemNode = ItemSpawner.on_floor(k.room, &"garden_sprinkler_green", 330.0, 40.0)
	ItemStates.set_state(sp, "on", true)
	Garden.tick(k.room)
	assert_true(Garden.is_wet(bed), "Beet in Reichweite ist nass")
	assert_false(Garden.is_wet(far), "Beet weit weg bleibt trocken")


func test_garten_waechst_weiter_waehrend_man_weg_ist() -> void:
	var bed: ItemNode = _bed()
	Garden.sow(bed)
	Garden.water(bed)
	var snap: Array = RoomSnapshot.capture(k.room)
	RoomSnapshot.clear(k.room)
	await wait_process_frames(2)
	now += Garden.GROW_S * 2.0 + 5.0                      # 2 Stufen später zurück (noch nass)
	Garden.fixed_now = now
	RoomSnapshot.apply(k.room, snap)
	await wait_process_frames(1)
	Garden.catch_up(k.room)
	var back: ItemNode = null
	for it: ItemNode in Placement.all_items(k.room):
		if Garden.is_bed(it):
			back = it
	assert_not_null(back)
	assert_eq(back.state, "ripe", "zwei Stufen gewachsen, während das Kind im Haus war")
