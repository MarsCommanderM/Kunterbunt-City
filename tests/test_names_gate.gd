extends GutTest
## P04-T06: Namen (200 Kacheln, Würfel, freie Eingabe nur hinter dem Eltern-Tor) und
## das Eltern-Tor selbst (Rechenaufgabe + Halten).

func before_each() -> void:
	SaveSystem.wipe()


func after_each() -> void:
	SaveSystem.wipe()


# ------------------------------------------------------------------ Namenliste
func test_namenliste_hat_200_eindeutige_namen() -> void:
	var names: Array = NamePicker.names()
	assert_true(names.size() >= 200, "mindestens 200 Namen, sind %d" % names.size())
	var seen: Dictionary = {}
	for n: Variant in names:
		var s: String = String(n)
		assert_false(seen.has(s), "doppelt: %s" % s)
		seen[s] = true
		assert_true(s.length() <= 16, "zu lang für eine Kachel: %s" % s)
		assert_false(s.strip_edges().is_empty())


# ------------------------------------------------------------------ Wortfilter
func test_filter_laesst_gute_namen_durch() -> void:
	for n: String in ["Mia", "Ben", "Li-La", "Ana Sofia", "Bo"]:
		assert_eq(NameFilter.check(n), "", "%s muss erlaubt sein" % n)


func test_filter_sperrt_schlimme_woerter() -> void:
	for n: String in ["Arsch", "kacke", "FICK", "Shit", "Porn"]:
		assert_ne(NameFilter.check(n), "", "%s muss gesperrt sein" % n)


func test_filter_sperrt_zu_lange_namen() -> void:
	assert_ne(NameFilter.check("A".repeat(40)), "", "zu lange Namen sind gesperrt")


func test_pretty_und_clean() -> void:
	assert_eq(NameFilter.pretty("mIA"), "Mia")
	assert_eq(NameFilter.pretty("  anna   maria "), "Anna Maria")
	assert_eq(NameFilter.clean("  Lea  "), "Lea")


# ------------------------------------------------------------------ Namens-Auswahl
func test_namenswahl_zeigt_kacheln_und_wuerfelt() -> void:
	var host: Control = add_child_autofree(Control.new())
	var box: Dictionary = {"name": ""}
	var np: NamePicker = NamePicker.open(host, "", 1, func(n: String) -> void: box["name"] = n)
	await wait_process_frames(3)
	var tiles: int = 0
	for c: Node in np._grid.get_children():
		if c is Button:
			tiles += 1
	assert_eq(tiles, NamePicker.names().size(), "jeder Name bekommt eine Kachel")
	np._roll()
	await wait_process_frames(2)
	assert_ne(np._current, "", "🎲 wählt einen Namen")
	assert_true(NamePicker.names().has(np._current))
	np._pick(np._current)
	assert_eq(box["name"], np._current, "der getippte Name wird übernommen")


func test_freie_eingabe_nur_hinter_dem_tor() -> void:
	var host: Control = add_child_autofree(Control.new())
	var np: NamePicker = NamePicker.open(host, "", 1, func(_n: String) -> void: pass)
	await wait_process_frames(3)
	var pencil: Button = np.find_child("PencilButton", true, false) as Button
	assert_not_null(pencil, "der Bleistift-Knopf fehlt")
	pencil.pressed.emit()
	await wait_process_frames(2)
	var gate: ParentGate = null
	for c: Node in np.get_children():
		if c is ParentGate:
			gate = c
	assert_not_null(gate, "freie Eingabe öffnet ZUERST das Eltern-Tor")
	gate.passed.emit()
	await wait_process_frames(2)
	var edit: LineEdit = null
	for b: Node in np.find_children("*", "LineEdit", true, false):
		edit = b
	assert_not_null(edit, "erst nach dem Tor kommt das Eingabefeld")


# ------------------------------------------------------------------ Eltern-Tor
func test_tor_rechnen_hat_genau_eine_richtige_antwort() -> void:
	var host: Control = add_child_autofree(Control.new())
	var box: Dictionary = {"ok": false}
	var gate: ParentGate = ParentGate.ask(host, func() -> void: box["ok"] = true)
	await wait_process_frames(3)
	assert_eq(gate._mode, 0, "Standard ist die Rechenaufgabe")
	var opts: Array = gate._options()
	assert_eq(opts.size(), 4, "vier Auswahl-Kacheln")
	assert_true(opts.has(gate._a + gate._b), "eine davon ist richtig")
	gate._answer(gate._a + gate._b)
	assert_true(box["ok"], "richtige Antwort öffnet das Tor")


func test_tor_falsche_antwort_laesst_dich_nicht_durch() -> void:
	var host: Control = add_child_autofree(Control.new())
	var box: Dictionary = {"ok": false}
	var gate: ParentGate = ParentGate.ask(host, func() -> void: box["ok"] = true)
	await wait_process_frames(3)
	var wrong: int = gate._a + gate._b + 1
	gate._answer(wrong)
	assert_false(box["ok"], "falsche Antwort darf nicht durchlassen")


func test_tor_halten_braucht_drei_sekunden() -> void:
	var host: Control = add_child_autofree(Control.new())
	var box: Dictionary = {"ok": false}
	var gate: ParentGate = ParentGate.ask(host, func() -> void: box["ok"] = true)
	await wait_process_frames(3)
	gate._mode = 1
	gate._build()
	await wait_process_frames(2)
	assert_not_null(gate._ring, "Halte-Kreis fehlt")
	gate._holding = true
	gate._process(ParentGate.HOLD_S * 0.5)
	assert_false(box["ok"], "nach der halben Zeit ist noch zu")
	gate._process(ParentGate.HOLD_S * 0.6)
	assert_true(box["ok"], "nach 3 Sekunden geht das Tor auf")
