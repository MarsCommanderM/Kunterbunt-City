extends GutTest
## P05-T07/T08: Speicherstände sind heilig – Version, Migration, Welt-Slots, Rucksack,
## Raumzustände, Export/Import (ohne Netz). Fixture: tests/fixtures/world_v1.json.

const FIXTURE: String = "res://tests/fixtures/world_v1.json"

var _dir: String


func before_each() -> void:
	SaveSystem.wipe()
	_dir = "user://"


func after_each() -> void:
	SaveSystem.wipe()


func _load_fixture(path: String) -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(path))


# ------------------------------------------------------------------ Migration
func test_fixture_ist_ein_alter_speicherstand() -> void:
	var d: Dictionary = _load_fixture(FIXTURE)
	assert_eq(int(d["save_version"]), 1, "Test-Fixture muss Version 1 sein")
	assert_false(d.has("areas"), "v1 kennt keine Bereiche")
	assert_false(d.has("backpack"), "v1 kennt keinen Rucksack")
	assert_eq(Array(d["characters"]).size(), 2)


func test_v1_wird_beim_laden_zu_v2() -> void:
	var old: Dictionary = _load_fixture(FIXTURE)
	# Fixture in Slot 1 legen (als wäre es ein alter Stand) …
	assert_true(SaveSystem.save_world(1, old), "Schreiben muss klappen")
	var raw: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(SaveSystem.world_path(1)))
	assert_eq(int(raw["save_version"]), SaveSystem.SAVE_VERSION, "beim Schreiben wird versioniert")
	var loaded: Dictionary = SaveSystem.load_world(1)
	assert_eq(int(loaded.get("save_version", 0)), SaveSystem.SAVE_VERSION)
	assert_true(loaded.has("areas"), "Migration ergänzt die Bereiche")
	assert_true(loaded.has("backpack"), "Migration ergänzt den Rucksack")
	assert_true(loaded.has("album"), "Migration ergänzt das Album")
	assert_true(loaded.has("active_pets"), "Migration ergänzt die Begleittiere")


func test_figuren_und_tiere_ueberleben_die_migration() -> void:
	var old: Dictionary = _load_fixture(FIXTURE)
	SaveSystem.save_world(1, old)
	var before: Array = Array(old["characters"])
	var after: Array = Array(SaveSystem.load_world(1).get("characters", []))
	assert_eq(after.size(), before.size(), "keine Figur darf verloren gehen")
	assert_eq(String((after[0] as Dictionary)["name"]), "Mia")
	assert_eq(String((after[0] as Dictionary)["skin"]), "#f7c9a2")
	assert_eq(String((after[1] as Dictionary)["template"]), "adult")
	var pets: Array = Array(SaveSystem.load_world(1).get("pets", []))
	assert_eq(pets.size(), 1)
	assert_eq(String((pets[0] as Dictionary)["species"]), "pet_cat")


func test_migration_hinterlaesst_spielbare_daten() -> void:
	SaveSystem.save_world(1, _load_fixture(FIXTURE))
	Game.slot = 1
	Game.load_all()
	assert_eq(Game.characters.size(), 2)
	assert_eq(Game.pets.size(), 1)
	assert_true(Game.has_complete_character(), "die vollständige Figur muss spielbar bleiben")
	var mia: CharacterData = Game.character_by_id(&"c_1")
	assert_not_null(mia)
	assert_eq(mia.display_name(), "Mia")
	assert_true(mia.is_complete())
	var incomplete: CharacterData = Game.character_by_id(&"c_2")
	assert_false(incomplete.is_complete(), "Figur ohne Hautton bleibt unfertig")
	Game.slot = 0
	Game.load_all()


# ------------------------------------------------------------------ Welt-Slots & Zustand
func test_drei_welt_slots_sind_getrennt() -> void:
	var w0: Dictionary = SaveSystem.empty_world(0)
	w0["characters"] = [{"id": "a", "name": "A"}]
	SaveSystem.save_world(0, w0)
	var w1: Dictionary = SaveSystem.empty_world(1)
	w1["characters"] = [{"id": "b", "name": "B"}]
	SaveSystem.save_world(1, w1)
	assert_eq(Array(SaveSystem.load_world(0)["characters"]).size(), 1)
	assert_eq(String((Array(SaveSystem.load_world(0)["characters"])[0] as Dictionary)["name"]), "A")
	assert_eq(String((Array(SaveSystem.load_world(1)["characters"])[0] as Dictionary)["name"]), "B")
	SaveSystem.wipe_world(1)
	assert_false(SaveSystem.world_exists(1))
	assert_true(SaveSystem.world_exists(0))


func test_raumzustand_round_trip() -> void:
	Game.slot = 0
	Game.load_all()
	var snap: Array = [
		{"id": "toy_beachball", "x": 690.0, "y": 72.0},
		{"id": "food_carrot", "x": 0.0, "y": 0.0, "on": "home_table_wood", "x_rel": -0.3},
	]
	Game.set_room_state(&"home", &"kitchen", snap)
	Game.save_now()
	Game.areas.clear()
	Game.load_all()
	var back: Array = Game.room_state(&"home", &"kitchen")
	assert_eq(back.size(), 2)
	assert_eq(String((back[0] as Dictionary)["id"]), "toy_beachball")
	assert_almost_eq(float((back[0] as Dictionary)["x"]), 690.0, 0.05,
		"Positionen auf 0,1 cm genau (Akzeptanzkriterium)")
	assert_eq(String((back[1] as Dictionary)["on"]), "home_table_wood")
	assert_almost_eq(float((back[1] as Dictionary)["x_rel"]), -0.3, 0.001)


func test_rucksack_wird_mitgespeichert() -> void:
	Game.slot = 0
	Game.load_all()
	Game.backpack = [{"id": "toy_teddy_brown"}, {"id": "food_apple_red"}]
	Game.save_now()
	Game.backpack.clear()
	Game.load_all()
	assert_eq(Game.backpack.size(), 2)
	assert_eq(String((Game.backpack[0] as Dictionary)["id"]), "toy_teddy_brown")
	Game.backpack.clear()


func test_export_und_import_ohne_netz() -> void:
	Game.slot = 0
	Game.load_all()
	var c: CharacterData = CharacterData.create("kid")
	c.character_name = "Export-Kind"
	c.skin = "#f7c9a2"
	Game.add_character(c)
	Game.save_now()
	var path: String = SaveSystem.export_world(0)
	assert_ne(path, "", "Export muss eine Datei schreiben")
	assert_true(FileAccess.file_exists("user://export/kunterbunt-city-welt-0.json"))
	Game.wipe()
	assert_eq(Game.characters.size(), 0)
	assert_true(SaveSystem.import_world("user://export/kunterbunt-city-welt-0.json", 0))
	Game.load_all()
	assert_eq(Game.characters.size(), 1)
	assert_eq(Game.active_character().character_name, "Export-Kind")


func test_autosave_ist_entprellt() -> void:
	Game.slot = 0
	Game.load_all()
	var files_before: int = _world_size()
	for i: int in 20:
		Game.mark_dirty(&"home", &"kitchen")     # 20 Änderungen hintereinander
	assert_true(Game._timer.time_left > 0.0, "der Speicher-Timer läuft (2 s entprellt)")
	Game.save_now()
	assert_true(_world_size() > files_before, "nach save_now() steht alles in der Datei")


func _world_size() -> int:
	return FileAccess.get_file_as_string(SaveSystem.world_path(0)).length()
