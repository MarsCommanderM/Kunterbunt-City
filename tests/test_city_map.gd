extends GutTest
## P05-T02/T03/T04: Stadtkarte – ein Knopf pro Bereich, Symbole, Raster-Ansicht,
## Baustelle statt Schloss, große Tippflächen.

var map: CityMap


func before_each() -> void:
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	map = CityMap.new()
	add_child_autofree(map)
	await wait_process_frames(3)


func after_each() -> void:
	SaveSystem.wipe()


func test_alle_bereiche_haben_symbol_und_namen() -> void:
	var areas: Array = Areas.list()
	assert_true(areas.size() >= 11, "mindestens 11 Bereiche, sind %d" % areas.size())
	for a: Variant in areas:
		var d: Dictionary = a
		assert_false(String(d["label"]).is_empty(), "Bereich ohne Namen")
		assert_true(FileAccess.file_exists("res://assets/ui/icons/%s.png" % String(d["icon"])),
			"Symbol fehlt: %s" % String(d["icon"]))
		var x: float = float(d["map_x"])
		var y: float = float(d["map_y"])
		assert_true(x > 120.0 and x < 1800.0, "map_x außerhalb: %s" % String(d["id"]))
		assert_true(y > 120.0 and y < 1040.0, "map_y außerhalb: %s" % String(d["id"]))
		assert_true(Color(String(d["color"])) != Color(1, 1, 1, 1), "Bereich ohne Farbe")


func test_karte_zeigt_einen_knopf_pro_bereich() -> void:
	assert_eq(map._area_buttons.size(), Areas.list().size())
	for id: Variant in map._area_buttons:
		var b: Button = map._area_buttons[id]
		assert_true(b.get_global_rect().size.x >= 120.0 and b.get_global_rect().size.y >= 120.0,
			"Tippfläche zu klein (Ziel ≥ 120×120 px @1080p): %s" % b.get_global_rect().size)


func test_raster_ansicht_zeigt_dieselben_bereiche() -> void:
	map.mode = "grid"
	map._refresh()
	await wait_process_frames(2)
	assert_eq(map._area_buttons.size(), Areas.list().size())
	for id: Variant in map._area_buttons:
		var b: Button = map._area_buttons[id]
		assert_true(b.get_global_rect().size.x >= 120.0, "Raster-Kachel zu klein: %s" % String(id))


func test_fertiger_bereich_wird_betreten() -> void:
	var home := StringName("home")
	assert_true(Areas.is_ready(home), "Zuhause muss spielbar sein")
	assert_eq(Areas.first_ready(), home)
	watch_signals(map)
	map._area_buttons["home"].emit_signal("pressed")
	assert_signal_emitted(map, "entered")


func test_baustelle_statt_schloss() -> void:
	## Kein Bereich ist gesperrt: jeder hat einen Knopf, unfertige zeigen ein Werkzeug.
	var unready: int = 0
	for a: Variant in Areas.list():
		var id: String = String((a as Dictionary)["id"])
		if Areas.is_ready(StringName(id)):
			continue
		unready += 1
		var b: Button = map._area_buttons[id]
		assert_not_null(b, "auch unfertige Bereiche brauchen einen Knopf")
		assert_not_null(b.get_node_or_null("Baustelle"), "%s: Baustellen-Symbol fehlt" % id)
		assert_false(b.disabled, "%s: Knopf darf nicht gesperrt sein" % id)
	if unready == 0:
		pass_test("alle Bereiche fertig – keine Baustelle mehr")


func test_tipp_auf_baustelle_betritt_nichts() -> void:
	var id := StringName("")
	for a: Variant in Areas.list():                  # erste noch unfertige Baustelle (P10: werden nach und nach fertig)
		if not Areas.is_ready(StringName((a as Dictionary)["id"])):
			id = StringName((a as Dictionary)["id"])
			break
	if id == &"":
		pass_test("alle Bereiche fertig – keine Baustelle mehr")
		return
	watch_signals(map)
	AudioBus.history.clear()
	map._area_buttons[String(id)].emit_signal("pressed")
	assert_signal_not_emitted(map, "entered")
	assert_true(AudioBus.history.has("deny"), "kurzes 'geht noch nicht'-Geraeusch")


func test_stadtkarte_hat_die_vier_knoepfe_oben() -> void:
	var buttons: Array = []
	_collect(map, buttons)
	for name: String in ["Figur", "Rucksack", "Album", "Eltern"]:
		var found: bool = false
		for b: Variant in buttons:
			if String(b).contains(name):
				found = true
		assert_true(found, "Knopf '%s' fehlt in der Kopfzeile" % name)


func _collect(n: Node, out: Array) -> void:
	for c: Node in n.get_children():
		if c is Button:
			out.append(String((c as Button).text))
		_collect(c, out)
