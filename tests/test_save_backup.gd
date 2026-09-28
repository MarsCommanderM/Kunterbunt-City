extends GutTest
## P11-T04: Speicherstand-Robustheit – 2 rotierende Sicherungen, kaputte Datei → Sicherung wird geladen.

const SLOT: int = 2


func before_each() -> void:
	SaveSystem.wipe_world(SLOT)


func after_all() -> void:
	SaveSystem.wipe_world(SLOT)


func _save(n: int) -> void:
	var w: Dictionary = SaveSystem.empty_world(SLOT)
	w["secrets"] = ["marker_%d" % n]
	assert_true(SaveSystem.save_world(SLOT, w))


func test_two_rotating_backups_are_kept() -> void:
	for n: int in [1, 2, 3, 4]:
		_save(n)
	var p: String = SaveSystem.world_path(SLOT)
	assert_true(FileAccess.file_exists(SaveSystem.backup_path(p, 1)))
	assert_true(FileAccess.file_exists(SaveSystem.backup_path(p, 2)))
	assert_false(FileAccess.file_exists(SaveSystem.backup_path(p, 3)), "nie mehr als 2")
	assert_false(FileAccess.file_exists(p + ".tmp"), "keine Reste")
	assert_eq(SaveSystem.load_world(SLOT)["secrets"], ["marker_4"])


func test_broken_file_loads_the_last_good_backup() -> void:
	_save(1)
	_save(2)
	var f := FileAccess.open(SaveSystem.world_path(SLOT), FileAccess.WRITE)
	f.store_string("{ kaputt …")                     # z. B. Strom weg mitten im Schreiben
	f.close()
	assert_eq(SaveSystem.load_world(SLOT)["secrets"], ["marker_1"], "Sicherung 1 gerettet")


func test_missing_main_file_uses_backup_and_wipe_removes_all() -> void:
	_save(1)
	_save(2)
	DirAccess.remove_absolute(SaveSystem.world_path(SLOT))
	assert_eq(SaveSystem.load_world(SLOT)["secrets"], ["marker_1"])
	SaveSystem.wipe_world(SLOT)
	assert_false(FileAccess.file_exists(SaveSystem.backup_path(SaveSystem.world_path(SLOT), 1)))
	assert_eq(Array(SaveSystem.load_world(SLOT)["secrets"]).size(), 0, "nach Löschen wirklich leer")
