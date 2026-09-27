extends GutTest
## P04-T03/T05/T07: Der Editor ist bedienbar und hält die Regeln ein – gemessen, nicht geschätzt.
## Wichtigste Regel: Die GRÖSSE der Figur kommt NUR aus der Schablone (nie aus Teilen/Farben).

const HEIGHT: Dictionary = {"toddler": 90.0, "kid": 125.0, "adult": 172.0}

var ed: CharacterEditor


func before_each() -> void:
	SaveSystem.wipe()
	CharacterRig.animate_poses = false
	ed = CharacterEditor.new()
	ed.data = CharacterData.create("kid")
	add_child_autofree(ed)
	await wait_process_frames(3)


func after_each() -> void:
	SaveSystem.wipe()


# ------------------------------------------------------------------ Pflicht-Ablauf (T07)
func test_fertig_erst_mit_hautton() -> void:
	assert_false(ed.data.is_complete(), "frische Figur darf nicht fertig sein")
	assert_false(ed.is_done_enabled(), "✓ muss gesperrt sein, solange kein Hautton gewählt ist")
	ed.select_category("skin")
	ed.select_color("#e8a877")
	assert_true(ed.data.is_complete())
	assert_true(ed.is_done_enabled(), "✓ muss frei sein, sobald Schablone + Hautton stehen")


func test_pflicht_editor_hat_keinen_zurueck_knopf() -> void:
	var host: Control = add_child_autofree(Control.new())
	var forced: CharacterEditor = CharacterEditor.open(host, CharacterData.create("kid"), true,
		func(_x) -> void: pass)
	await wait_process_frames(2)
	var back: bool = false
	for c: Node in forced.get_children():
		if c is Button and (c as Button).icon == Ui.tex("back"):
			back = true
	assert_false(back, "im Pflicht-Ablauf darf es kein Zurück geben")
	forced.queue_free()


func test_ohne_hautton_trotzdem_sichtbar() -> void:
	## Ohne Hautton wird ein heller Standard gezeigt (keine schwarze Figur).
	var lk: Dictionary = ed.data.look()
	assert_true(String(lk["skin"]).begins_with("#"), "Standard-Hautton fehlt: %s" % str(lk["skin"]))
	assert_ne(Color(String(lk["skin"])), Color.BLACK)


# ------------------------------------------------------------------ Teile & Farben (T03/T04)
func test_teil_waehlen_aendert_vorschau_und_daten() -> void:
	ed.select_category("top")
	ed.select_variant("dress")
	assert_eq(ed.data.parts["top"], "dress")
	var part: String = String(ed._stage.rig._layers["Top"].get_meta("part"))
	assert_eq(part, "top_dress", "die Vorschau muss das gewählte Teil zeigen")


func test_farbe_waehlen_setzt_shader_zone() -> void:
	ed.select_category("top")
	ed.select_variant("shirt")
	ed.select_zone(0)
	ed.select_color("#ff0000")
	var mat: ShaderMaterial = ed._stage.rig._layers["Top"].material as ShaderMaterial
	assert_not_null(mat)
	assert_eq(mat.get_shader_parameter("zone1"), Color("#ff0000"))
	ed.select_zone(1)
	ed.select_color("#00ff00")
	mat = ed._stage.rig._layers["Top"].material as ShaderMaterial
	assert_eq(mat.get_shader_parameter("zone2"), Color("#00ff00"))
	assert_eq(mat.get_shader_parameter("zone1"), Color("#ff0000"), "Zone 1 darf Zone 2 nicht überschreiben")


func test_hautton_faerbt_alle_haut_ebenen() -> void:
	ed.select_category("skin")
	ed.select_color("#6f3f22")
	var want: Color = Color("#6f3f22")
	for layer: String in ["Head", "ArmFrontSkin", "ArmFrontPalm", "Fingers0"]:
		var mat: ShaderMaterial = ed._stage.rig._layers[layer].material as ShaderMaterial
		assert_eq(mat.get_shader_parameter("zone1"), want, "Ebene %s ist nicht hautfarben" % layer)


func test_wuerfel_liefert_stimmigen_look() -> void:
	ed.select_category("skin")
	ed.select_color("#f7c9a2")
	var before: Dictionary = ed.data.parts.duplicate(true)
	ed.roll_dice()
	assert_ne(before.hash(), ed.data.parts.hash(), "🎲 muss etwas ändern")
	for slot: String in CharacterParts.slot_ids():
		assert_true(CharacterParts.ids(slot).has(String(ed.data.parts[slot])),
			"🎲 hat für %s eine unbekannte Variante gesetzt" % slot)
	assert_eq(ed.data.template_id, "kid", "🎲 darf die Schablone nicht ändern")


# ------------------------------------------------------------------ Größe nur aus der Schablone
func test_groesse_kommt_nur_aus_der_schablone() -> void:
	for tid: String in HEIGHT:
		ed.select_template(tid)
		await wait_process_frames(2)
		var h: float = -ed._stage.rig.local_rect().position.y
		assert_almost_eq(h, HEIGHT[tid], 1.5,
			"%s muss %d cm hoch sein, ist aber %.1f" % [tid, int(HEIGHT[tid]), h])


func test_kein_teil_aendert_die_koerpergroesse() -> void:
	ed.select_category("skin")
	ed.select_color("#f7c9a2")
	ed.select_template("kid")
	await wait_process_frames(2)
	var base: float = -ed._stage.rig.local_rect().position.y
	for slot: String in CharacterParts.slot_ids():
		for id: Variant in CharacterParts.ids(slot):
			ed.select_variant(String(id))
			await wait_process_frames(1)
			var h: float = -ed._stage.rig.local_rect().position.y
			assert_almost_eq(h, base, 1.0, "%s/%s ändert die Größe (%.1f cm)" % [slot, id, h])
	for i: int in CharacterParts.palette_colors("cloth").size():
		ed.select_category("top")
		ed.select_color(String(CharacterParts.palette_colors("cloth")[i]))
		await wait_process_frames(1)
		assert_almost_eq(-ed._stage.rig.local_rect().position.y, base, 1.0)


# ------------------------------------------------------------------ Outfits (T05)
func test_outfit_platz_speichern_anziehen_leeren() -> void:
	ed.select_category("top")
	ed.select_variant("dress")
	ed.store_outfit(0)
	assert_false(Dictionary(ed.data.outfits[0]).is_empty())
	ed.select_variant("shirt")
	ed.wear_outfit(0)
	assert_eq(ed.data.outfit, 0)
	assert_eq(String(ed.data.look()["parts"]["top"]), "dress", "angezogenes Outfit muss wirken")
	ed.clear_outfit(0)
	assert_true(Dictionary(ed.data.outfits[0]).is_empty())
	assert_eq(ed.data.outfit, -1)


# ------------------------------------------------------------------ Katalog-Anbindung
## P04b: Der Katalog wächst – mindestens 5 Varianten je Kategorie, jede mit Symbol.
func test_jede_kategorie_hat_mindestens_fuenf_varianten_und_ein_symbol() -> void:
	for slot: String in CharacterParts.slot_ids():
		assert_gte(CharacterParts.ids(slot).size(), 5, "Slot %s" % slot)
		assert_true(FileAccess.file_exists("res://assets/ui/icons/%s.png" % _icon_for(slot)),
			"Symbol für %s fehlt" % slot)


func _icon_for(slot: String) -> String:
	for c: Variant in CharacterEditor.CATS:
		if String((c as Dictionary)["id"]) == slot:
			return String((c as Dictionary)["icon"])
	return "star"


func test_alle_teile_aller_schablonen_existieren() -> void:
	for tid: String in CharacterTemplates.ids():
		for slot: String in CharacterParts.slot_ids():
			for id: Variant in CharacterParts.ids(slot):
				var v: Dictionary = CharacterParts.variant(slot, String(id))
				assert_true(CharacterTemplates.has_part(tid, String(v["part"])),
					"%s/%s: Teil %s fehlt" % [tid, slot, v["part"]])
