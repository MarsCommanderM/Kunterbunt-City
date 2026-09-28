extends GutTest
## P07-T06 (Akzeptanz: „25 Rezepte funktionieren, GUT je Rezept"): jedes Rezept aus data/recipes/*.json wird
## wirklich gekocht – Gerät hinstellen, Zutat hinein, anschalten (Pfanne/Topf ohne eigenen Schalter: auf den Herd).

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)
	Recipes.instant = true


func after_each() -> void:
	Recipes.instant = false


func _first_item(prefix: String) -> StringName:
	for gid: String in Catalog.group_ids():
		for id: Variant in Catalog.items(gid):
			if String(id).begins_with(prefix):
				return StringName(String(id))
	return &""


func _ingredient(r: Dictionary) -> StringName:
	for pre: Variant in Array(r["in"]):
		var id: StringName = _first_item(String(pre))
		if id != &"":
			return id
	return &""


func test_es_gibt_mindestens_25_rezepte() -> void:
	assert_gte(Recipes.rules().size(), 25)


func test_rezept_kocht(p = use_parameters(Recipes.rules())) -> void:
	var r: Dictionary = p
	var host_id: StringName = _first_item(String(r["host"]))
	var ing_id: StringName = _ingredient(r)
	assert_ne(host_id, &"", "%s: Gerät %s fehlt im Katalog" % [r["id"], r["host"]])
	assert_ne(ing_id, &"", "%s: keine Zutat im Katalog" % r["id"])
	if host_id == &"" or ing_id == &"":
		return
	var host: ItemNode
	var switch: ItemNode
	var hdef: ItemDefinition = ItemDB.get_item(host_id)
	if hdef.states.has("on"):
		host = ItemSpawner.on_floor(k.room, host_id, 300.0, 30.0)
		switch = host
	else:                                                   # Pfanne: auf den Herd
		switch = ItemSpawner.on_floor(k.room, _first_item("app_stove"), 300.0, 10.0)
		host = ItemSpawner.into_container(switch, host_id)
	assert_not_null(host, "%s: Gerät nicht platzierbar" % r["id"])
	var ing: ItemNode = ItemSpawner.into_container(host, ing_id)
	assert_not_null(ing, "%s: Zutat %s passt nicht in %s" % [r["id"], ing_id, host_id])
	ItemStates.set_state(switch, "on", true)
	Recipes.check(switch)
	var got: bool = false
	for c: Node in host.contents_root.get_children():
		if c is ItemNode and String((c as ItemNode).def.id) == String(r["out"]) and not c.is_queued_for_deletion():
			got = true
	assert_true(got, "Rezept %s: %s in %s → %s" % [r["id"], ing_id, host_id, r["out"]])
