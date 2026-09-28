extends GutTest
## R-11: umbenannte Items (data/item_aliases.json) – alte IDs aus Speicherständen werden weiter gefunden,
## gespeichert wird die neue ID. (Anlass: 7 Varianten hießen nach ihrem Farbcode, z. B. „…_#b8b2a7".)


func test_old_ids_resolve_to_the_new_items() -> void:
	assert_true(ItemDB.has_item(&"garden_bird_bath_#b8b2a7"), "alte ID bekannt")
	var d: ItemDefinition = ItemDB.get_item(&"garden_bird_bath_#b8b2a7")
	assert_not_null(d)
	assert_eq(String(d.id), "garden_bird_bath_stone", "liefert das umbenannte Item")
	assert_false(ItemDB.item_ids().has(&"garden_bird_bath_#b8b2a7"), "alte ID taucht im Katalog nicht auf")


func test_room_state_with_old_id_loads_and_saves_the_new_id() -> void:
	var k := KitchenFixture.new(self)
	var n: int = RoomSnapshot.apply(k.room, [{"id": "furn_fireplace_#c0664f", "x": 300.0, "y": 20.0}])
	assert_eq(n, 1, "Ding aus altem Speicherstand ist wieder da")
	var ids: Array = RoomSnapshot.capture(k.room).map(func(e: Dictionary) -> String: return String(e["id"]))
	assert_true(ids.has("furn_fireplace_brick"), "neu gespeichert unter der neuen ID: %s" % [ids])
