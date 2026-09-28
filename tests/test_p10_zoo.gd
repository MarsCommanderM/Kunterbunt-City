extends GutTest
## P10g Zoo: Daten, echte Größen, richtiges/falsches Futter, Fütterungsrunde der Pflegerin, Affe „leiht“ sich ein Ding,
## Streichelzoo-Tiere tragbar, Zoo-Tiere bleiben im Gehege.

var k: KitchenFixture
var fake: AreaScene


func before_each() -> void:
	NpcBrain.autonomous = false
	PetNode.autonomous = false
	Settings.reduced_motion = true
	k = KitchenFixture.new(self)
	fake = AreaScene.new()
	fake.room = k.room


func after_each() -> void:
	Settings.reduced_motion = false
	fake.free()


func after_all() -> void:
	NpcBrain.autonomous = true


func test_zoo_area_has_nine_rooms_npcs_and_secrets() -> void:
	var d: Dictionary = Room.load_area(Areas.path_of(&"zoo"))
	assert_eq(Array(d["rooms"]).size(), 9)
	assert_eq(NpcRoles.npcs_of("zoo").size(), 6)
	assert_eq(Secrets.for_area("zoo").size(), 7)
	assert_true(Areas.is_ready(&"zoo"))


func test_animals_have_real_sizes() -> void:
	var kid: float = ItemDB.height_cm(&"char_child")
	var gir: ItemDefinition = ItemDB.get_item(&"zoo_giraffe_butter")
	assert_gt(gir.height_cm, 400.0, "Giraffe über 4 m")
	assert_gt(gir.height_cm, kid * 3.0)
	assert_gt(ItemDB.get_item(&"zoo_elephant_grey").height_cm, ItemDB.get_item(&"zoo_zebra_white").height_cm)
	assert_lt(ItemDB.get_item(&"zoo_penguin_navy").height_cm, ItemDB.height_cm(&"char_toddler"), "Pinguin < Kleinkind")
	assert_lt(ItemDB.get_item(&"zoo_chick_butter").height_cm, 20.0)
	assert_true(ItemSpawner.on_floor(k.room, &"zoo_zebra_white", 400.0, 40.0) is PetNode, "Zoo-Tiere leben (PetNode)")


func test_right_food_makes_the_animal_happy_wrong_food_stays() -> void:
	var lion: ItemNode = ItemSpawner.on_floor(k.room, &"zoo_lion_oak", 400.0, 40.0)
	var banana: ItemNode = ItemSpawner.on_floor(k.room, &"food_banana_butter", 530.0, 45.0)
	assert_false(ZooActions.on_dropped(fake, banana), "Löwe mag keine Banane")
	assert_true(is_instance_valid(banana) and banana.get_parent() != null, "Banane bleibt liegen")
	var meat: ItemNode = ItemSpawner.on_floor(k.room, &"zoo_food_meat_coral", 530.0, 45.0)
	assert_true(AreaActions.on_dropped(fake, meat), "Fleisch!")
	assert_true(lion.get_meta("fed", false), "satt und froh")
	assert_null(meat.get_parent(), "gefressen")


func test_zookeeper_feeding_round_and_animals_eat() -> void:
	var peng: ItemNode = ItemSpawner.on_floor(k.room, &"zoo_penguin_navy", 400.0, 40.0)
	NpcSpawner.spawn(k.room, NpcRoles.role("zookeeper"), {"id": "z", "role": "zookeeper", "x_cm": 200, "y_cm": 60})
	ZooActions.refresh(k.room)
	assert_eq(ZooActions.feeding_round(k.room), 1, "eine Portion Fisch")
	ZooActions.tick(fake, 1.0)
	assert_true(peng.get_meta("fed", false), "Pinguin hat den Fisch gefressen")


func test_monkey_borrows_a_small_thing() -> void:
	var monkey: ItemNode = ItemSpawner.on_floor(k.room, &"zoo_monkey_walnut", 400.0, 40.0)
	var apple: ItemNode = ItemSpawner.on_floor(k.room, &"food_apple_red", 300.0, 50.0)
	var x0: float = apple.position.x
	assert_eq(ZooActions.steal(k.room, monkey), apple)
	assert_gt(absf(apple.position.x - x0), 100.0, "liegt jetzt woanders")
	assert_true(k.room.floor_band.contains(apple.position), "bleibt im Raum")


func test_petting_zoo_animals_can_be_carried() -> void:
	for id: StringName in [&"zoo_goat_white", &"zoo_lamb_cream", &"zoo_rabbit_linen", &"zoo_pig_rose"]:
		var d: ItemDefinition = ItemDB.get_item(id)
		assert_eq(d.hold, "two_hands", String(id))
		assert_true(d.tags.has("pettable"))
	assert_eq(ItemDB.get_item(&"zoo_giraffe_butter").hold, "none", "Giraffe trägt man nicht")


func test_zoo_animal_stays_in_its_enclosure_and_does_not_flee() -> void:
	var z: PetNode = ItemSpawner.on_floor(k.room, &"zoo_zebra_white", 500.0, 40.0) as PetNode
	ItemSpawner.character_on_floor(k.room, "kid", 530.0, 40.0)
	var home: Rect2 = z.home_area(k.room)
	for i: int in 600:
		z.tick(1.0 / 30.0)
	assert_true(home.grow(1.0).has_point(z.position), "im Gehege")
	assert_lt(absf(z.position.x - 500.0), z.def.width_cm + 1.0)
