extends GutTest
## P04-T08/T09: Galerie (Figuren + Tiere, Ordner, duplizieren, löschen) und Haustier-Editor.

var gal: Gallery


func before_each() -> void:
	SaveSystem.wipe()
	Game.characters.clear()
	Game.pets.clear()
	Game.active_id = &""
	Game.active_pets.clear()
	CharacterRig.animate_poses = false
	Portrait.clear_cache()


func after_each() -> void:
	SaveSystem.wipe()


func _gallery() -> Gallery:
	var g := Gallery.new()
	add_child_autofree(g)
	await wait_process_frames(3)
	return g


func _add_char(name: String, folder: String = "Familie") -> CharacterData:
	var c: CharacterData = CharacterData.create("kid")
	c.character_name = name
	c.skin = "#f7c9a2"
	c.folder = folder
	Game.add_character(c)
	return c


# ------------------------------------------------------------------ Galerie: Figuren
func test_galerie_zeigt_eine_karte_pro_figur() -> void:
	var g: Gallery = await _gallery()
	assert_eq(g.card_count(), 0, "ohne Figuren ist die Galerie leer (außer der Neu-Kachel)")
	_add_char("Mia")
	_add_char("Ben", "Freunde")
	await g._refresh()
	assert_eq(g.card_count(), 2, "jede Figur bekommt eine Karte")
	assert_eq(g.card_count(), Game.characters.size())


func test_galerie_ordner_filtern() -> void:
	var g: Gallery = await _gallery()
	_add_char("Mia", "Familie")
	_add_char("Ben", "Freunde")
	g.folder = "Freunde"
	await g._refresh()
	assert_eq(g.card_count(), 1, "nur Figuren aus dem Ordner")
	g.folder = "Alle"
	await g._refresh()
	assert_eq(g.card_count(), 2, "„Alle“ zeigt alles")


func test_duplizieren_und_loeschen() -> void:
	var g: Gallery = await _gallery()
	var c: CharacterData = _add_char("Mia")
	await g._refresh()
	g.duplicate_card(c.id)
	await wait_process_frames(3)
	assert_eq(Game.characters.size(), 2)
	var copy: CharacterData = Game.characters[1]
	assert_ne(copy.id, c.id, "die Kopie braucht eine eigene ID")
	assert_eq(copy.character_name, "Mia 2")
	assert_eq(copy.template_id, c.template_id)
	assert_eq(copy.parts.hash(), c.parts.hash(), "die Kopie sieht gleich aus")
	g.delete_card(copy.id)
	await wait_process_frames(3)
	assert_eq(Game.characters.size(), 1)


func test_aktive_figur_waehlen() -> void:
	var g: Gallery = await _gallery()
	var a: CharacterData = _add_char("Mia")
	var b: CharacterData = _add_char("Ben")
	await g._refresh()
	Game.set_active(b.id)
	assert_eq(Game.active_id, b.id)
	assert_eq(Game.active_character().character_name, "Ben")
	assert_true(Game.has_complete_character())


func test_spielen_ohne_figur_gesperrt() -> void:
	Game.characters.clear()
	Game.active_id = &""
	assert_false(Game.has_complete_character())
	var g: Gallery = await _gallery()
	assert_false(Flow.can_play(), "ohne vollständige Figur ist kein Bereich betretbar")


# ------------------------------------------------------------------ Galerie: Tiere
func test_tier_reiter_zeigt_haustiere() -> void:
	var g: Gallery = await _gallery()
	Game.add_pet(PetData.create("pet_cat"))
	Game.add_pet(PetData.create("pet_rabbit"))
	g.mode = "pets"
	await g._refresh()
	assert_eq(g.card_count(), 2)
	assert_eq(Game.pets.size(), 2)


func test_maximal_zwei_tiere_begleiten() -> void:
	Game.add_pet(PetData.create("pet_cat"))
	Game.add_pet(PetData.create("pet_dog_small"))
	Game.add_pet(PetData.create("pet_bird"))
	var ids: Array = []
	for p: Variant in Game.pets:
		ids.append((p as PetData).id)
	Game.active_pets.clear()
	Game.toggle_active_pet(ids[0])
	Game.toggle_active_pet(ids[1])
	Game.toggle_active_pet(ids[2])
	assert_eq(Game.active_pets.size(), Game.MAX_PETS, "höchstens zwei Tiere gleichzeitig")
	Game.toggle_active_pet(ids[0])
	assert_eq(Game.active_pets.size(), 1, "nochmal tippen nimmt das Tier wieder mit raus")


# ------------------------------------------------------------------ Haustier-Editor
func test_haustier_editor_setzt_art_und_farben() -> void:
	var pe := PetEditor.new()
	pe.pet = PetData.create("pet_dog_medium")
	add_child_autofree(pe)
	await wait_process_frames(2)
	assert_eq(pe.pet.species_id, "pet_dog_medium")
	pe.set_species("pet_cat")
	assert_eq(pe.pet.species_id, "pet_cat")
	pe.select_category("fur")
	pe.select_color("#3b2f2a")
	assert_eq(pe.pet.fur, "#3b2f2a")
	pe.set_trait("sleepy")
	assert_eq(pe.pet.pet_trait, "sleepy")
	pe.set_pattern("stripes")
	assert_eq(pe.pet.pattern, "stripes")
	pe.roll_dice()
	assert_true(PetSpecies.ids().has(pe.pet.species_id))
	assert_true(PetSpecies.trait_ids(pe.pet.species_id).has(pe.pet.pet_trait),
		"🎲 darf nur Züge wählen, die zur Art passen")
	assert_true(PetSpecies.pattern_ids().has(pe.pet.pattern))


func test_haustier_groesse_kommt_aus_der_tabelle() -> void:
	for sid: Variant in PetSpecies.ids():
		var def: ItemDefinition = ItemDB.get_item(StringName(String(sid)))
		assert_not_null(def, "%s ist kein Item" % String(sid))
		var entry: Dictionary = ItemDB.get_scale(def.scale_ref)
		assert_almost_eq(def.height_cm, float(entry["h_cm"]), 0.01,
			"%s: Höhe aus der Tabelle" % String(sid))
		assert_true(def.height_cm > 0.0)


func test_haustier_speichern_und_laden() -> void:
	var p: PetData = PetData.create("pet_rabbit")
	p.pet_name = "Hopsi"
	p.fur = "#ffffff"
	p.fur2 = "#f0f0f0"
	p.collar = "#e2574c"
	p.pet_trait = "curious"
	Game.add_pet(p)
	Game.save_now()               # ab P05 lebt alles in der Welt-Datei (user://world_0.json)
	Game.pets.clear()
	Game.load_all()
	var back: PetData = Game.pet_by_id(p.id)
	assert_not_null(back, "Haustier muss nach dem Neustart da sein")
	assert_eq(back.species_id, "pet_rabbit")
	assert_eq(back.pet_name, "Hopsi")
	assert_eq(back.fur, "#ffffff")
	assert_eq(back.collar, "#e2574c")
	assert_eq(back.pet_trait, "curious")
	assert_eq(back.display_name(), "Hopsi")
