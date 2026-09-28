extends GutTest
## P07-T04 (Regel R-11): Speicherstand Version 3 – Tapete/Boden je Raum und zuletzt besuchter Raum.
## Fixture tests/fixtures/world_v2.json ist ein echter v2-Stand (ohne decor/last_room) und muss verlustfrei wandern.

const FIXTURE: String = "res://tests/fixtures/world_v2.json"


func before_each() -> void:
	SaveSystem.wipe()


func after_each() -> void:
	SaveSystem.wipe()
	Game.load_all()


func _write_raw(slot: int, d: Dictionary) -> void:
	var f := FileAccess.open(SaveSystem.world_path(slot), FileAccess.WRITE)
	f.store_string(JSON.stringify(d))
	f.close()


func test_fixture_ist_version_2() -> void:
	var d: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(FIXTURE))
	assert_eq(int(d["save_version"]), 2)
	assert_false(d.has("decor"), "v2 kennt keine Raum-Einrichtung")
	assert_true(Dictionary(d["areas"]).has("home"))


func test_v2_wandert_nach_v3_ohne_verlust() -> void:
	var old: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(FIXTURE))
	_write_raw(1, old)                                  # roh schreiben – so liegt ein alter Stand auf dem Gerät
	var w: Dictionary = SaveSystem.load_world(1)
	assert_eq(int(w["save_version"]), SaveSystem.SAVE_VERSION, "v2 wandert bis zur aktuellen Version")
	assert_eq(w["decor"], {}, "Einrichtung startet leer (= Standard je Raum)")
	assert_eq(w["last_room"], {})
	var kitchen: Array = Dictionary(Dictionary(w["areas"])["home"])["kitchen"]
	assert_eq(kitchen.size(), 2, "Küchen-Zustand bleibt erhalten (gleiche Raum-ID)")
	assert_eq(Array(w["characters"]).size(), Array(old["characters"]).size())
	assert_eq(Array(w["backpack"]).size(), 1)


func test_einrichtung_und_letzter_raum_werden_gespeichert() -> void:
	Game.load_all()
	var d: Dictionary = {"wall": ["#a9c3dd", "#ffffff", "#f0b6c2"], "pattern": "stars", "pattern_col": "#f6d98a",
		"floor": "carpet", "floor_cols": ["#f0b6c2", "#e8a4b3", "#c1547a"]}
	Game.set_room_decor(&"home", &"kids1", d)
	Game.set_last_room(&"home", &"kids1")
	Game.save_now()
	Game.decor = {}
	Game.last_rooms = {}
	Game.load_all()
	assert_eq(Game.room_decor(&"home", &"kids1"), d)
	assert_eq(Game.last_room(&"home"), "kids1")
	assert_eq(Game.room_decor(&"home", &"bath"), {}, "nicht gewählte Räume behalten den Standard")
