extends GutTest
## ItemDB: Maßstab-Tabelle geladen, Größen nur aus der Tabelle.


func test_table_loaded() -> void:
	assert_true(ItemDB.is_loaded)
	assert_gt(ItemDB.entry_count(), 150)


func test_reference_heights() -> void:
	assert_eq(ItemDB.height_cm("char_child"), 125.0)
	assert_eq(ItemDB.height_cm("pet_dog_medium"), 45.0)
	assert_eq(ItemDB.height_cm("home_table_dining"), 75.0)
	assert_eq(ItemDB.height_cm("food_apple"), 8.0)
	assert_eq(ItemDB.height_cm("food_carrot"), 20.0)


func test_scale_mul_applies() -> void:
	assert_almost_eq(ItemDB.height_cm("food_apple", 1.25), 10.0, 0.0001)


func test_scale_mul_out_of_range_is_clamped() -> void:
	var errors_before: int = Log.error_count
	assert_almost_eq(ItemDB.height_cm("food_apple", 3.0), 8.0 * 1.3, 0.0001)
	assert_gt(Log.error_count, errors_before, "muss als Fehler gemeldet werden")
	assert_push_error("außerhalb 0,7–1,3")


func test_unknown_ref_is_error_not_guess() -> void:
	var errors_before: int = Log.error_count
	assert_true(ItemDB.get_scale("gibt_es_nicht").is_empty())
	assert_eq(ItemDB.height_cm("gibt_es_nicht"), 0.0)
	assert_gt(Log.error_count, errors_before)
	assert_push_error("unbekannte scale_ref")
	assert_push_error("unbekannte scale_ref")


func test_every_dog_smaller_than_table() -> void:
	for dog: String in ["pet_dog_small", "pet_dog_medium", "pet_dog_large"]:
		assert_lt(ItemDB.height_cm(dog), ItemDB.height_cm("home_table_dining"), dog)
