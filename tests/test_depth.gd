extends GutTest
## Pflicht-Test (Tech-Spec §6): Tiefen-Faktor 1,00 hinten, 1,12 vorne, NIE größer (Regel S-07).


func test_back_is_one() -> void:
	assert_almost_eq(Units.depth_factor(0.0, 0.0, 80.0), 1.0, 0.0001)


func test_front_is_1_12() -> void:
	assert_almost_eq(Units.depth_factor(80.0, 0.0, 80.0), 1.12, 0.0001)


func test_middle_is_linear() -> void:
	assert_almost_eq(Units.depth_factor(40.0, 0.0, 80.0), 1.06, 0.0001)


func test_never_above_limit_even_if_data_says_so() -> void:
	assert_almost_eq(Units.depth_factor(80.0, 0.0, 80.0, 1.54), 1.12, 0.0001, "1,54 aus v1 darf nie wieder durchkommen")
	assert_almost_eq(Units.depth_factor(500.0, 0.0, 80.0), 1.12, 0.0001, "hinter der Vorderkante geklemmt")


func test_never_below_one() -> void:
	assert_almost_eq(Units.depth_factor(-100.0, 0.0, 80.0), 1.0, 0.0001)


func test_floor_band_clamps_bad_data() -> void:
	var band := FloorBand.new()
	band.setup({"back_y_cm": 0.0, "front_y_cm": 70.0, "depth_scale_max": 2.0}, 500.0)
	assert_almost_eq(band.depth_factor(70.0), 1.12, 0.0001)
	band.free()


func test_zero_height_band_is_safe() -> void:
	assert_almost_eq(Units.depth_factor(10.0, 5.0, 5.0), 1.0, 0.0001)


func test_ratio_is_kept_in_depth() -> void:
	# Hund vorne und Tisch vorne behalten ihr Verhältnis (beide ×1,12).
	var f: float = Units.depth_factor(80.0, 0.0, 80.0)
	assert_lt(45.0 * f, 75.0 * f)
	assert_almost_eq((45.0 * f) / (75.0 * f), 45.0 / 75.0, 0.0001)
