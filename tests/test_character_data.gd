extends GutTest
## P04-T02: Figuren- und Haustier-Daten (JSON-Rundlauf, 100 Figuren, Outfits, Pflicht-Felder).

const N: int = 100


func before_each() -> void:
	SaveSystem.wipe()


func after_each() -> void:
	SaveSystem.wipe()


func test_round_trip_keeps_everything() -> void:
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#f7c9a2"
	c.character_name = "Mila"
	c.voice = 5
	c.folder = "Freunde"
	c.set_color("top", 1, "#ff0000")
	var back: CharacterData = CharacterData.from_dict(c.to_dict())
	assert_eq(back.template_id, "kid")
	assert_eq(back.character_name, "Mila")
	assert_eq(back.voice, 5)
	assert_eq(back.folder, "Freunde")
	assert_eq(back.colors["top"][1], "#ff0000")
	assert_eq(back.to_dict().hash(), c.to_dict().hash())


func test_complete_requires_skin_tone() -> void:
	var c: CharacterData = CharacterData.create("kid")
	assert_false(c.is_complete(), "ohne Hautton nicht fertig (T07)")
	c.skin = "#f7c9a2"
	assert_true(c.is_complete())
	c.template_id = "gibt_es_nicht"
	assert_false(c.is_complete(), "unbekannte Schablone zählt nicht")


func test_100_characters_save_and_load_fast() -> void:
	var list: Array = []
	for i: int in N:
		var c: CharacterData = CharacterData.create(["toddler", "kid", "adult"][i % 3])
		c.skin = "#f7c9a2"
		c.character_name = "Figur %d" % i
		list.append(c)
	var t0: int = Time.get_ticks_usec()
	assert_true(SaveSystem.save_characters(list), "speichern")
	var back: Array = SaveSystem.load_characters()
	var ms: float = (Time.get_ticks_usec() - t0) / 1000.0
	gut.p("100 Figuren speichern+laden: %.1f ms (%.2f MB)" % [
		ms, FileAccess.open("user://characters.json", FileAccess.READ).get_length() / 1048576.0])
	var first := back[0] as CharacterData
	var last := back[N - 1] as CharacterData
	assert_eq(back.size(), N)
	assert_lt(ms, 400.0, "kein Ruckeln beim Laden")
	assert_eq(first.character_name, "Figur 0")
	assert_true(last.is_complete())


func test_no_character_no_entry() -> void:
	assert_false(SaveSystem.has_any_character(), "ohne Figur kein Bereich (T07)")
	var c: CharacterData = CharacterData.create("kid")
	assert_false(SaveSystem.has_any_character(), "unfertige Figur zählt nicht")
	c.skin = "#f7c9a2"
	SaveSystem.save_characters([c])
	assert_true(SaveSystem.has_any_character())


func test_five_outfit_slots() -> void:
	var c: CharacterData = CharacterData.create("kid")
	assert_eq(c.outfits.size(), CharacterData.OUTFITS)
	c.parts["top"] = "dress"
	c.store_outfit(2)
	c.parts["top"] = "shirt"
	c.wear_outfit(2)
	assert_eq(c.outfit, 2)
	assert_eq(c.look()["parts"]["top"], "dress", "Outfit 2 angezogen")
	c.wear_outfit(0)
	assert_eq(c.look()["parts"]["top"], "dress", "leerer Platz ändert nichts")
	c.clear_outfit(2)
	assert_eq(c.outfit, -1)
	assert_eq(c.look()["parts"]["top"], "shirt", "Basis-Look wieder da")


func test_random_look_is_reproducible_and_valid() -> void:
	var c: CharacterData = CharacterData.create("kid")
	var rng := RandomNumberGenerator.new()
	rng.seed = 4711
	c.randomize_look(rng)
	var first: Dictionary = c.to_dict()
	rng.seed = 4711
	c.randomize_look(rng)
	assert_eq(c.to_dict(), first, "🎲 mit gleichem Seed = gleiche Figur")
	assert_true(CharacterParts.ids("top").has(String(c.parts["top"])))
	assert_true(CharacterParts.palette_colors("skin").has(c.skin))


func test_pet_round_trip() -> void:
	var p: PetData = PetData.create("pet_dog_brown")
	p.pet_name = "Bello"
	p.pet_trait = "hungry"
	p.pattern = "spots"
	SaveSystem.save_pets([p])
	var back: Array = SaveSystem.load_pets()
	assert_eq(back.size(), 1)
	var p0 := back[0] as PetData
	assert_eq(p0.pet_trait, "hungry")
	assert_true(p0.is_complete())
