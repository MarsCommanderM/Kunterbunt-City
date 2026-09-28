extends GutTest
## P08-T07/T08: Haustier-Bedürfnisse (Napf, Spielzeug, Körbchen), Charakterzug-Gewichte, Laute 15–60 s mit Varianten
## und dem globalen Limiter (nie mehr als 1 Tierlaut pro 8 s – auch mit vielen Tieren).

const DT: float = 1.0 / 30.0

var k: KitchenFixture
var _clock: float = 0.0


func before_each() -> void:
	k = KitchenFixture.new(self)
	_clock = 0.0
	AudioBus.clock = func() -> float: return _clock
	AudioBus.reset_animal_limiter()


func after_each() -> void:
	AudioBus.clock = Callable()


func _dog(x: float) -> PetNode:
	return ItemSpawner.on_floor(k.room, &"pet_dog_brown", x, 50.0) as PetNode


func _run(p: PetNode, seconds: float) -> void:
	for _i: int in int(seconds / DT):
		_clock += DT
		p.tick(DT)


func test_needs_rise_slowly_and_stay_between_0_and_1() -> void:
	var b := PetBrain.new(RandomNumberGenerator.new())
	b.tick(10000.0)
	for n: String in PetBrain.NEEDS:
		assert_between(float(b.needs[n]), 0.0, 1.0, n)
	var c := PetBrain.new(RandomNumberGenerator.new())
	c.tick(10.0)
	assert_lt(float(c.needs["hunger"]), 0.3, "steigt langsam (10 s)")


func test_hungry_dog_walks_to_the_full_bowl_and_eats() -> void:
	var bowl: ItemNode = ItemSpawner.on_floor(k.room, &"petgear_bowl_coral", 560.0, 50.0)
	ItemStates.set_state(bowl, "full", true)
	var dog: PetNode = _dog(250.0)
	dog.brain.needs["hunger"] = 1.0
	dog._timer = 0.0
	_run(dog, 12.0)
	assert_eq(bowl.state, "empty", "Napf leer gefressen")
	assert_lt(float(dog.brain.needs["hunger"]), 0.1, "satt")
	assert_lt(absf(dog.position.x - bowl.position.x), 60.0, "steht am Napf")


func test_playful_dog_pushes_the_ball() -> void:
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"petgear_ball_coral", 520.0, 50.0)
	var x0: float = ball.position.x
	var dog: PetNode = _dog(250.0)
	dog.brain.needs["play"] = 1.0
	dog._timer = 0.0
	_run(dog, 10.0)
	assert_gt(absf(ball.position.x - x0), 40.0, "Ball wurde angestupst")
	assert_true(k.room.floor_band.contains(ball.position), "Ball bleibt im Raum")


func test_tired_dog_sleeps_in_the_basket_and_wakes_up_when_tapped() -> void:
	var bed: ItemNode = ItemSpawner.on_floor(k.room, &"petgear_basket_oak", 520.0, 40.0)
	var dog: PetNode = _dog(250.0)
	dog.brain.needs["tired"] = 1.0
	dog._timer = 0.0
	_run(dog, 10.0)
	assert_eq(dog.mode, PetNode.Mode.SLEEP, "schläft")
	assert_lt(absf(dog.position.x - bed.position.x), 5.0, "im Körbchen")
	var x: float = dog.position.x
	_run(dog, 3.0)
	assert_almost_eq(dog.position.x, x, 0.01, "schläft ruhig")
	dog.on_tap()
	assert_ne(dog.mode, PetNode.Mode.SLEEP, "Streicheln weckt")
	assert_eq(float(dog.brain.needs["affection"]), 0.0, "Zuneigung gestillt")


func test_trait_changes_the_weights() -> void:
	var b := PetBrain.new(RandomNumberGenerator.new(), "sleepy")
	b.needs = {"hunger": 0.7, "play": 0.7, "tired": 0.7, "affection": 0.7}
	assert_eq(b.ranked()[0], "tired", "verschlafen → Körbchen zuerst")
	b.pet_trait = "greedy"
	assert_eq(b.ranked()[0], "hunger", "verfressen → Napf zuerst")
	b.pet_trait = "playful"
	assert_eq(b.ranked()[0], "play", "verspielt → Ball zuerst")


func test_without_matching_things_the_pet_just_strolls() -> void:
	var dog: PetNode = _dog(250.0)
	dog.brain.needs = {"hunger": 1.0, "play": 1.0, "tired": 1.0, "affection": 0.0}
	dog._timer = 0.0
	dog.tick(DT)
	assert_ne(dog.mode, PetNode.Mode.SEEK, "kein Napf/Ball/Körbchen → normales Schlendern")


func test_voices_every_15_to_60_s_with_variants() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 5
	var b := PetBrain.new(rng)
	var t: float = 0.0
	var last: float = 0.0
	var gaps: Array = []
	while t < 1200.0:
		t += 0.5
		if b.voice_due(0.5):
			gaps.append(t - last)
			last = t
	assert_gt(gaps.size(), 15)
	for g: Variant in gaps:
		assert_between(float(g), 14.9, 60.6, "Abstand %.1f s" % g)
	var seen: Dictionary = {}
	for i: int in 60:
		seen[b.voice_variant("pet_dog_bark")] = true
	assert_eq(seen.size(), 3, "Hund bellt in 3 Varianten")
	assert_eq(PetBrain.pet_sound("pet_cat_meow"), "pet_cat_purr", "Katze schnurrt beim Streicheln")
	for s: String in ["pet_dog_bark2", "pet_dog_bark3", "pet_cat_meow2", "pet_cat_purr"]:
		assert_true(ResourceLoader.exists("res://assets/audio/sfx/%s.wav" % s), s)


func test_never_more_than_one_animal_sound_per_8_s() -> void:
	var pets: Array = []
	for i: int in 6:
		var p: PetNode = _dog(100.0 + i * 90.0)
		p.brain.voice_in = 0.1 * i
		pets.append(p)
	var plays: Array = []
	var last: float = AudioBus._last_animal_t
	for _i: int in int(180.0 / 0.1):
		_clock += 0.1
		for p: PetNode in pets:
			p.tick(0.1)
		if p_changed(last):
			plays.append(AudioBus._last_animal_t)
			last = AudioBus._last_animal_t
	assert_gt(plays.size(), 3, "Tiere machen Laute")
	for i: int in range(1, plays.size()):
		assert_true(float(plays[i]) - float(plays[i - 1]) >= AudioBus.ANIMAL_SOUND_COOLDOWN_S - 0.001,
			"Abstand %.1f s" % (float(plays[i]) - float(plays[i - 1])))


func p_changed(last: float) -> bool:
	return AudioBus._last_animal_t != last
