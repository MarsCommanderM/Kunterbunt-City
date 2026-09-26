extends GutTest
## ItemDefinition.from_dict: Größen aus der Tabelle, robuste Daten, Platzhalter-Fallback.

const APPLE: Dictionary = {"id": "food_apple", "category": "food", "h_cm": 8, "w_cm": 8, "hold": "one_hand", "placement": "table"}


func _make(d: Dictionary, entry: Dictionary = APPLE) -> Array:
	var errors: Array[String] = []
	var def: ItemDefinition = ItemDefinition.from_dict(d, entry, "test.json", errors)
	return [def, errors]


func test_size_comes_from_table_not_json() -> void:
	var r: Array = _make({"id": "a", "scale_ref": "food_apple", "size_cm": [99, 99], "grip": [0.5, 0.5]})
	assert_eq((r[0] as ItemDefinition).height_cm, 8.0)
	assert_eq((r[1] as Array).size(), 0, str(r[1]))


func test_scale_mul_is_clamped() -> void:
	var r: Array = _make({"id": "a", "scale_ref": "food_apple", "scale_mul": 5.0, "grip": [0.5, 0.5]})
	assert_almost_eq((r[0] as ItemDefinition).height_cm, 8.0 * 1.3, 0.0001)


func test_null_grip_and_pivot_do_not_crash() -> void:
	var r: Array = _make({"id": "a", "scale_ref": "food_apple", "grip": null, "pivot": null, "hold": "none", "sfx": null})
	var def: ItemDefinition = r[0]
	assert_eq(def.pivot, Vector2(0.5, 1.0))
	assert_eq(def.sfx, {})


func test_missing_grip_for_holdable_is_error() -> void:
	var r: Array = _make({"id": "a", "scale_ref": "food_apple"})
	assert_string_contains("\n".join(r[1]), "grip fehlt")


func test_unknown_hold_and_placement_are_errors() -> void:
	var r: Array = _make({"id": "a", "scale_ref": "food_apple", "hold": "tentacle", "placement": "ceiling"})
	assert_string_contains("\n".join(r[1]), "hold 'tentacle'")
	assert_string_contains("\n".join(r[1]), "placement 'ceiling'")


func test_missing_sprite_falls_back_to_placeholder() -> void:
	var r: Array = _make({"id": "a", "scale_ref": "food_apple", "grip": [0.5, 0.5], "sprite": "res://gibts/nicht.png"})
	var def: ItemDefinition = r[0]
	assert_true(def.uses_placeholder)
	assert_eq(def.sprite_path, "res://assets/placeholders/food_apple.png")
	assert_true(ResourceLoader.exists(def.sprite_path))


func test_surface_from_measured_fraction() -> void:
	var table: Dictionary = {"id": "home_table_dining", "category": "furniture", "h_cm": 75, "w_cm": 160, "hold": "none", "placement": "floor", "surface_h_cm": 75}
	var r: Array = _make({"id": "t", "scale_ref": "home_table_dining", "surface_frac_y": 0.12}, table)
	assert_almost_eq((r[0] as ItemDefinition).surface_local_h(), 66.0, 0.001)
	r = _make({"id": "t", "scale_ref": "home_table_dining"}, table)
	assert_almost_eq((r[0] as ItemDefinition).surface_local_h(), 75.0, 0.001, "ohne Anteil: Tabellenhöhe")


func test_container_and_tags() -> void:
	var r: Array = _make({"id": "a", "scale_ref": "food_apple", "grip": [0.5, 0.5], "tags": ["stackable"], "container": {"slots": 3, "max_item_h_cm": 5}})
	var def: ItemDefinition = r[0]
	assert_true(def.is_stackable())
	assert_true(def.is_container())
	assert_eq(def.container_max_item_h_cm, 5.0)


func test_fixture_is_not_movable_by_default() -> void:
	var fix: Dictionary = {"id": "fix_x", "category": "fixture", "h_cm": 100, "hold": "none", "placement": "floor"}
	var r: Array = _make({"id": "f", "scale_ref": "fix_x"}, fix)
	assert_false((r[0] as ItemDefinition).movable)
