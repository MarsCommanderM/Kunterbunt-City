extends GutTest
## P08-T06: Garantien der NPC-Zustandsmaschine + Abnahme (Kasse scannt, Bademeister rettet, Post kommt).
##   blockiert keinen Drop · verlässt nie den Raum · kehrt nach return_after_s zurück · reagiert beim Tragen

const DT: float = 0.1

var k: KitchenFixture


func before_each() -> void:
	NpcBrain.autonomous = false
	k = KitchenFixture.new(self)
	AudioBus.reset_animal_limiter()


func after_all() -> void:
	NpcBrain.autonomous = true
	NpcSpawner.fixed_hour = -1
	Settings.shops_always_open = true


func _npc(role_id: String, x: float, y: float = 40.0, extra: Dictionary = {}) -> NpcBrain:
	var role: Dictionary = NpcRoles.role(role_id).duplicate(true)
	role.merge(extra, true)
	return NpcSpawner.spawn(k.room, role, {"id": "npc_" + role_id, "role": role_id, "x_cm": x, "y_cm": y})


func _run(b: NpcBrain, seconds: float) -> void:
	for _i: int in int(seconds / DT):
		b.tick(DT)


func test_all_roles_load_with_valid_behavior_and_look() -> void:
	var roles: Dictionary = NpcRoles.all()
	assert_true(roles.size() >= 15, "mind. 15 Rollen (P08-T04): %d" % roles.size())
	for id: String in ["cashier", "shelf_stocker", "lifeguard", "teacher", "janitor", "doctor", "nurse", "coach",
			"supervisor", "mechanic", "florist", "zookeeper", "ride_operator", "vendor", "receptionist"]:
		assert_true(roles.has(id), "Rolle %s fehlt" % id)
	for r: Dictionary in roles.values():
		assert_true(NpcRoles.BEHAVIORS.has(String(r["behavior"])), "%s: Verhalten" % r["id"])
		assert_true(Array(r["work"]).size() >= 1, "%s: Arbeits-Animationen" % r["id"])
		for a: Variant in Array(r["work"]):
			assert_true(NpcWork.MOTION.has(String(a)), "%s: Animation '%s' ist bekannt" % [r["id"], a])
		assert_true(CharacterTemplates.ids().has(String(r["template"])), "%s: Schablone" % r["id"])


func test_home_npcs_are_neighbor_and_postman_in_the_garden() -> void:
	var list: Array = NpcRoles.npcs_in_room("home", "garden")
	var roles: Array = list.map(func(n: Dictionary) -> String: return String(n["role"]))
	assert_true(roles.has("neighbor") and roles.has("postman"), "Nachbarin + Briefträger im Garten: %s" % [roles])


func test_npc_is_a_real_figure_with_the_template_height() -> void:
	var b: NpcBrain = _npc("cashier", 300.0)
	assert_true(b.body is CharacterRig)
	assert_true(b.body.has_meta("npc_id"))
	assert_eq(b.state, NpcBrain.State.IDLE)
	assert_almost_eq(b.body.def.height_cm, ItemDB.height_cm(&"char_adult"), 0.5, "Größe aus der Tabelle (Erwachsene)")


func test_npc_does_not_block_a_drop() -> void:
	var b: NpcBrain = _npc("cashier", 300.0, 40.0)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_coral", 500.0, 40.0)
	var t: Placement.Target = k.drag_pivot_to(apple, k.room.ysort_root.to_global(b.body.position + Vector2(8.0, 2.0)), 4)
	assert_not_null(t, "Drop an der Stelle der Figur klappt")
	assert_eq(t.rejected_reason, "", "nicht abgelehnt")
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"home_chair_mint", 600.0, 40.0)
	var t2: Placement.Target = k.drag_pivot_to(chair, k.room.ysort_root.to_global(b.body.position), 5)
	assert_not_null(t2, "auch ein Stuhl lässt sich genau dort abstellen")
	assert_eq(t2.kind, &"floor")


func test_npc_never_leaves_the_room() -> void:
	var b: NpcBrain = _npc("passerby", 200.0, 40.0, {"patrol_cm": 5000.0, "work_every_s": [0.2, 0.5]})
	for _i: int in 1500:
		b.tick(DT)
		assert_true(k.room.floor_band.contains(b.body.position), "im Bodenband: %s" % b.body.position)
		assert_between(b.body.position.x, 0.0, k.room.width_cm, "im Raum (x)")
	var r: Array = NpcPath.route(k.room, Vector2(100, 40), Vector2(-900, 900))
	var last: Vector2 = r[r.size() - 1]
	assert_true(k.room.floor_band.contains(last) and last.x >= 0.0, "Ziel außerhalb → in den Raum geklemmt")


func test_reacts_when_carried_and_returns_after_return_after_s() -> void:
	var b: NpcBrain = _npc("cashier", 300.0, 40.0)
	var post: Vector2 = b.post
	var grab: Vector2 = k.grab_point(b.body)
	k.drag.press(7, grab)
	k.drag.move(7, grab + Vector2(0, -20))
	b.tick(DT)
	assert_eq(b.state, NpcBrain.State.CARRIED, "getragen")
	assert_eq(b.body.emotion, "surprised", "staunt beim Tragen")
	k.drag.move(7, grab + Vector2(260.0, 0.0))
	k.drag.release(7, grab + Vector2(260.0, 0.0))
	b.tick(DT)
	assert_eq(b.state, NpcBrain.State.REACT, "freut sich nach dem Absetzen")
	assert_gt(b.body.position.distance_to(post), 150.0, "steht jetzt woanders")
	_run(b, float(b.role["return_after_s"]))
	assert_eq(b.state, NpcBrain.State.RETURN, "spätestens nach return_after_s zurück an den Platz")
	_run(b, 260.0 / b.speed() + 2.0)
	assert_true(b.at_post(), "wieder am Platz (%.0f cm entfernt)" % b.body.position.distance_to(post))
	assert_eq(b.state, NpcBrain.State.IDLE)


func test_seated_npc_stands_up_and_walks_back() -> void:
	var b: NpcBrain = _npc("teacher", 200.0, 40.0)
	var sofa: ItemNode = ItemSpawner.on_floor(k.room, &"home_sofa", 480.0, 30.0)
	var p: Vector2 = Seats.point_global(sofa, 0) - b.body.hip_offset() * b.body.global_scale.y
	k.drag_pivot_to(b.body, p, 8)
	b.tick(DT)
	assert_true(b.is_seated(), "sitzt auf dem Sofa")
	_run(b, float(b.role["return_after_s"]) + 0.2)
	assert_false(b.is_seated(), "steht auf")
	_run(b, 12.0)
	assert_true(b.at_post(), "läuft zurück an den Platz")


func test_path_goes_around_big_furniture() -> void:
	var shelf: ItemNode = ItemSpawner.on_floor(k.room, &"home_sofa", 350.0, 50.0)
	var r: Array = NpcPath.route(k.room, Vector2(150, 10), Vector2(550, 10))
	assert_eq(r.size(), 3, "Umweg über die vordere Laufspur")
	assert_gt(float((r[0] as Vector2).y), shelf.position.y, "Laufspur liegt vor dem Sofa")
	assert_eq(NpcPath.route(k.room, Vector2(150, 70), Vector2(550, 70)).size(), 1, "vor dem Sofa: gerader Weg")


func test_cashier_scans_an_item_beep_and_bag() -> void:
	var register: ItemNode = ItemSpawner.on_floor(k.room, &"shop_cash_register_cream", 300.0, 30.0)
	var b: NpcBrain = _npc("cashier", 230.0, 25.0)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_coral", 330.0, 34.0)
	assert_true(NpcSpawner.item_dropped(k.room, apple), "Kasse reagiert auf das Ding daneben")
	assert_eq(b.work.scanned, 1, "gescannt (Piep)")
	assert_eq(b.anim, "scan")
	assert_eq(register.state, "open", "Kasse springt auf")
	var bag: ItemNode = apple.get_parent().get_parent() as ItemNode
	assert_not_null(bag, "Apfel liegt in einer Tüte")
	assert_true(String(bag.def.id).begins_with("shop_bag"), "Tüte erscheint: %s" % bag.def.id)
	var far: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_coral", 650.0, 34.0)
	assert_false(NpcSpawner.item_dropped(k.room, far), "weit weg von der Kasse: kein Scan")


func test_lifeguard_patrols_whistles_at_runners_and_rescues_after_10_s() -> void:
	var pool: ItemNode = ItemSpawner.on_floor(k.room, &"garden_pool_frame_s_sky", 380.0, 30.0)
	var b: NpcBrain = _npc("lifeguard", 150.0, 50.0, {"work_every_s": [0.3, 0.5]})
	var xs: Array = []
	for _i: int in 80:
		b.tick(DT)
		xs.append(b.body.position.x)
	assert_gt(float(xs.max()) - float(xs.min()), 150.0, "läuft den Rand ab (Patrouille)")
	var kid: CharacterRig = ItemSpawner.character_on_floor(k.room, "kid", 80.0, 60.0)
	for _i: int in 30:                                    # rennt am Becken vorbei
		kid.position.x += 30.0
		b.tick(DT)
	assert_gt(b.work.whistles, 0, "pfeift bei rennender Figur")
	var p: Vector2 = Seats.point_global(pool, 1) - kid.hip_offset() * kid.global_scale.y
	k.drag_pivot_to(kid, p, 9)
	assert_true(b.work.in_water(kid), "Figur ist im Becken")
	_run(b, 9.5)
	assert_eq(b.work.rescued, 0, "vor 10 s keine Rettung")
	_run(b, 12.0)
	assert_eq(b.work.rescued, 1, "rettet nach 10 s unter Wasser")
	assert_false(b.work.in_water(kid), "Figur ist wieder draußen")
	assert_eq(kid.get_parent(), k.room.ysort_root)


func test_postman_brings_mail_to_the_mailbox_and_walks_back() -> void:
	var box: ItemNode = ItemSpawner.on_floor(k.room, &"garden_mailbox_coral", 520.0, 20.0)
	var b: NpcBrain = _npc("postman", 150.0, 30.0)
	b.work._mail_t = 999.0
	_run(b, 30.0)
	assert_eq(b.work.delivered, 1, "Post liegt beim Briefkasten")
	var mag: ItemNode = null
	for it: ItemNode in Placement.all_items(k.room):
		if String(it.def.id).begins_with("deco_magazines"):
			mag = it
	assert_not_null(mag)
	assert_lt(absf(mag.position.x - box.position.x), 120.0, "direkt am Briefkasten")
	assert_true(b.at_post(), "zurück an seinem Platz")


func test_day_plan_shops_closed_at_night_unless_always_open() -> void:
	var entry: Array = [{"id": "npc_c", "role": "cashier", "x_cm": 300, "y_cm": 30}]
	Settings.shops_always_open = false
	NpcSpawner.fixed_hour = 22
	assert_eq(NpcSpawner.spawn_list(k.room, entry).size(), 0, "22 Uhr: Laden zu, Kassiererin nicht da")
	NpcSpawner.fixed_hour = 10
	var got: Array = NpcSpawner.spawn_list(k.room, entry)
	assert_eq(got.size(), 1, "10 Uhr: offen")
	var b: NpcBrain = got[0]
	assert_eq(b.state, NpcBrain.State.RETURN, "kommt herein und schließt auf")
	assert_lt(b.body.position.x, 60.0, "startet am Eingang")
	Settings.shops_always_open = true
	NpcSpawner.fixed_hour = 22
	assert_eq(NpcSpawner.spawn_list(k.room, entry).size(), 1, "Standard: immer offen")
	NpcSpawner.fixed_hour = -1


func test_at_most_six_light_background_npcs() -> void:
	var list: Array = []
	for i: int in 9:
		list.append({"id": "npc_p%d" % i, "role": "passerby", "x_cm": 60 + i * 60, "y_cm": 30})
	assert_eq(NpcSpawner.spawn_list(k.room, list).size(), NpcSpawner.MAX_LIGHT, "max. 6 leichte Figuren")


func test_tap_makes_the_npc_wave() -> void:
	var b: NpcBrain = _npc("florist", 300.0)
	var got: Array = []
	b.worked.connect(func(a: String) -> void: got.append(a))
	b.body.on_tap_at(b.body.global_position + Vector2(0, -20))
	assert_true(got.has("wave"), "winkt zurück")
	assert_eq(b.state, NpcBrain.State.REACT)
