extends GutTest
## ItemNode: gezeichnete Größe exakt wie in der Tabelle (Maßstab-Bibel), Pivot unten, keine _process-Last.


func _node(id: StringName) -> ItemNode:
	var n: ItemNode = ItemSpawner.make(id)
	add_child_autofree(n)
	return n


func test_drawn_heights_are_exact() -> void:
	for pair: Array in [[&"food_egg", 6.0], [&"food_apple_red", 8.0], [&"food_carrot", 20.0], [&"toy_teddy_brown", 30.0],
			[&"pet_dog_brown", 45.0], [&"home_table_wood", 75.0], [&"home_chair_mint", 90.0], [&"fix_fridge", 180.0]]:
		var n: ItemNode = _node(pair[0])
		assert_almost_eq(n.draw_size().y, pair[1], 0.01, String(pair[0]))
		assert_almost_eq(n.global_rect().size.y, pair[1], 0.01)


func test_aspect_ratio_is_kept() -> void:
	var n: ItemNode = _node(&"home_table_wood")
	var tex: Vector2 = n.sprite.texture.get_size()
	# draw_size ist die INHALTS-Box (tex minus Padding) – Seitenverhältnis muss exakt bleiben.
	var content: Vector2 = tex - Vector2.ONE * 2.0 * n.def.pad_px
	assert_almost_eq(n.draw_size().x / n.draw_size().y, content.x / content.y, 0.001)
	assert_eq(n.def.pad_px, 4, "Pipeline-Sprites melden 4 px Padding")


func test_placeholder_sizes_match_table_too() -> void:
	var n: ItemNode = _node(&"kitchen_microwave")
	assert_almost_eq(n.draw_size().y, 30.0, 0.01)
	assert_almost_eq(n.draw_size().x, 50.0, 1.0, "Platzhalter hat echte Breite")


func test_pivot_is_bottom_center() -> void:
	var n: ItemNode = _node(&"toy_beachball")
	n.position = Vector2(100, 20)
	var r: Rect2 = n.global_rect()
	assert_almost_eq(r.end.y, 20.0, 0.01)
	assert_almost_eq(r.get_center().x, 100.0, 0.01)


func test_lift_raises_sprite_6cm() -> void:
	var n: ItemNode = _node(&"food_apple_red")
	n.set_lifted(true, false)
	assert_almost_eq(n.sprite.position.y, -ItemNode.LIFT_CM, 0.001)
	assert_almost_eq(n.global_rect().end.y, -6.0, 0.01)
	n.set_lifted(false, false)
	assert_eq(n.sprite.position.y, 0.0)


func test_idle_items_do_not_tick() -> void:
	var n: ItemNode = _node(&"food_apple_red")
	assert_false(n.is_processing(), "Ruhe-Items kosten keine Rechenzeit")
	assert_false(n.is_physics_processing())


func test_unique_ids() -> void:
	assert_ne(_node(&"food_egg").uid, _node(&"food_egg").uid)


func test_wall_items_have_no_shadow_and_containers_toggle() -> void:
	var bag: ItemNode = _node(&"item_backpack")
	watch_signals(bag)
	bag.on_tap()
	assert_signal_emitted(bag, "opened_changed")
	assert_true(bag.is_open)
	var apple: ItemNode = _node(&"food_apple_red")
	apple.set_open(true)
	assert_false(apple.is_open, "kein Behälter → lässt sich nicht öffnen")


## P11-Bot-Fund: Ding in der Hand einer nach links gespiegelten Figur – Rechteck nie negativ, trotzdem greifbar.
func test_mirrored_item_has_a_positive_rect_and_can_be_hit() -> void:
	var holder := Node2D.new()
	holder.scale = Vector2(-1.0, 1.0)
	add_child_autofree(holder)
	var it: ItemNode = ItemNode.create(ItemDB.get_item(&"toy_ball_coral"))
	holder.add_child(it)
	var r: Rect2 = it.global_rect()
	assert_gt(r.size.x, 0.0, "Breite positiv")
	assert_true(it.hit_test(r.get_center(), 1.0), "Mitte trifft")
	assert_false(it.hit_test(r.position + r.size * 3.0, 1.0), "weit daneben trifft nicht")
