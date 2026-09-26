extends GutTest
## P03-T09: Haustier – Maße aus der Tabelle, in JEDER Tiefe kleiner als der Tisch,
## folgt der nächsten Figur (deterministisch per tick()), Tipp → Laut über den AudioBus-Limiter.

var k: KitchenFixture
var _clock: float = 0.0


func before_each() -> void:
	k = KitchenFixture.new(self)
	_clock = 0.0
	AudioBus.clock = func() -> float: return _clock
	AudioBus.reset_animal_limiter()


func after_each() -> void:
	AudioBus.clock = Callable()


func test_pet_sizes_come_from_the_scale_table() -> void:
	var dog: ItemNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 200.0, 40.0)
	var cat: ItemNode = ItemSpawner.on_floor(k.room, &"pet_cat", 260.0, 40.0)
	assert_almost_eq(dog.global_rect().size.y / dog.global_scale.y, 45.0, 1.0, "Hund mittel 45 cm")
	assert_almost_eq(cat.global_rect().size.y / cat.global_scale.y, 28.0, 1.0, "Katze 28 cm")
	assert_eq(dog.def.category, "pet")


func test_dog_is_smaller_than_the_table_at_every_depth() -> void:
	for depth: float in [0.0, 18.0, 36.0, 55.0, 73.0]:
		var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 300.0, depth)
		var dog: ItemNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 420.0, depth)
		var th: float = table.global_rect().size.y / table.global_scale.y
		var dh: float = dog.global_rect().size.y / dog.global_scale.y
		assert_lt(dh, th, "Tiefe %.0f: Hund (%.0f cm) kleiner als Tisch (%.0f cm)" % [depth, dh, th])
		assert_lt(dh / th, 0.75, "deutlich kleiner (Verhältnis %.2f)" % (dh / th))
		assert_almost_eq(dog.global_scale.y, table.global_scale.y, 0.0001, "gleicher Tiefen-Faktor")


func test_dog_in_front_of_table_stays_smaller() -> void:
	## Gemeiner Fall: Hund ganz vorne (Faktor 1,12), Tisch ganz hinten (Faktor 1,0).
	var table: ItemNode = ItemSpawner.on_floor(k.room, &"home_table_wood", 300.0, 0.0)
	var dog: ItemNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 420.0, 73.0)
	assert_lt(dog.global_rect().size.y, table.global_rect().size.y, "auch mit Tiefen-Vorteil kleiner")


func test_follows_the_nearest_character_and_keeps_distance() -> void:
	var girl: ItemNode = ItemSpawner.character_on_floor(k.room, "char_girl_01", 200.0, 50.0)
	var dog: PetNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 500.0, 60.0)
	dog._rng.seed = 4242                     # reproduzierbar: gleicher Seed → gleicher Weg
	assert_eq(dog.mode, PetNode.Mode.IDLE)
	var d0: float = dog.position.distance_to(girl.position)
	assert_true(d0 > PetNode.FOLLOW_START_CM, "Startabstand %.0f cm > 110 cm" % d0)
	var min_d: float = INF
	var late: float = 0.0                    # Abstand am Ende (300 Frames) → Ø
	for i: int in 900:
		dog.tick(1.0 / 60.0)
		var d: float = dog.position.distance_to(girl.position)
		min_d = minf(min_d, d)
		if i >= 600:
			late += d
	assert_lt(min_d, d0 - 50.0, "Hund läuft hinterher: %.0f → %.0f cm" % [d0, min_d])
	assert_true(min_d >= PetNode.MIN_FRIEND_CM - 2.0,
		"Hund läuft nie in die Figur hinein (kleinster Abstand %.1f cm)" % min_d)
	var mean: float = late / 300.0
	assert_true(mean < PetNode.FOLLOW_START_CM,
		"bleibt in Freundesnähe (Ø %.0f cm)" % mean)


func test_dog_does_not_leave_the_floor_band() -> void:
	var girl: ItemNode = ItemSpawner.character_on_floor(k.room, "char_girl_01", 200.0, 50.0)
	var dog: PetNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 600.0, 70.0)
	for _i: int in 900:
		dog.tick(1.0 / 60.0)
	assert_true(k.room.floor_band.contains(dog.position), "Hund bleibt im Bodenband: %s" % dog.position)


func test_tick_is_deterministic() -> void:
	var a: PetNode = _walked_pet()
	var b: PetNode = _walked_pet()
	assert_almost_eq(a.position.x, b.position.x, 0.001, "gleicher Start → gleicher Weg (Seed)")
	assert_almost_eq(a.position.y, b.position.y, 0.001)


func test_tap_plays_one_bark_per_8_seconds() -> void:
	var dog: PetNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 300.0, 60.0)
	assert_eq(dog.voice(), "pet_dog_bark")
	assert_true(AudioBus.play_animal("pet_dog_bark"), "erster Laut")
	assert_false(AudioBus.play_animal("pet_dog_bark"), "zweiter Laut in derselben Sekunde: stumm")
	_clock = 8.5
	assert_true(AudioBus.play_animal("pet_dog_bark"), "nach 8,5 s wieder erlaubt")


func test_cat_voice_is_meow() -> void:
	var cat: PetNode = ItemSpawner.on_floor(k.room, &"pet_cat", 300.0, 60.0)
	assert_eq(cat.voice(), "pet_cat_meow")
	assert_true(AudioBus.play_animal(cat.voice()))
	assert_false(AudioBus.play_animal(cat.voice()))


func _walked_pet() -> PetNode:
	ItemSpawner.character_on_floor(k.room, "char_girl_01", 150.0, 40.0)
	var dog: PetNode = ItemSpawner.on_floor(k.room, &"pet_dog_brown", 520.0, 65.0)
	for _i: int in 240:
		dog.tick(1.0 / 60.0)
	return dog
