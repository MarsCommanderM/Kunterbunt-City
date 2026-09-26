extends GutTest
## Units: Kamera-Zoom, Bildschirm-y, Sprite-Skalierung.


func test_zoom_for_300cm_on_1080p() -> void:
	assert_almost_eq(Units.zoom_for_visible_height(1080.0, 300.0), 3.6, 0.0001)


func test_zoom_roundtrip() -> void:
	var z: float = Units.zoom_for_visible_height(1080.0, 300.0)
	assert_almost_eq(Units.visible_height_for_zoom(1080.0, z), 300.0, 0.0001)


func test_screen_y_back_line() -> void:
	assert_almost_eq(Units.screen_y(0.0, 90.0, 0.0, 80.0), -90.0, 0.0001)


func test_screen_y_front_scaled() -> void:
	assert_almost_eq(Units.screen_y(80.0, 100.0, 0.0, 80.0), 80.0 - 112.0, 0.0001)


func test_sprite_scale_carrot() -> void:
	# Maßstab-Bibel §1: Karotte 20 cm, Textur 160 px → 0,125
	assert_almost_eq(Units.sprite_scale(160.0, 20.0), 0.125, 0.0001)
