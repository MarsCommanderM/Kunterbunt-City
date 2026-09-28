extends GutTest
## P10: gilt für JEDEN spielbaren Bereich (auch künftige) – Räume mit Hintergrund, Start-Items im Katalog,
## feste Figuren mit gültiger Rolle im richtigen Raum, Geheimnisse mit Sticker-Bild, Musik vorhanden.


func _ready_areas() -> Array:
	return Areas.ids().filter(func(id: String) -> bool:
		return Areas.is_ready(StringName(id)) and Areas.canonical(StringName(id)) == StringName(id))


func test_every_ready_area_is_complete() -> void:
	var areas: Array = _ready_areas()
	assert_true(areas.size() >= 4, "mind. 4 spielbare Bereiche: %s" % [areas])
	for id: String in areas:
		var d: Dictionary = Room.load_area(Areas.path_of(StringName(id)))
		var rooms: Array = Array(d.get("rooms", []))
		assert_gt(rooms.size(), 0, "%s: Räume" % id)
		assert_true(rooms.map(func(r: Dictionary) -> String: return String(r["id"])).has(Areas.room_of(StringName(id))),
			"%s: Start-Raum existiert" % id)
		for r: Dictionary in rooms:
			assert_true(FileAccess.file_exists(String(r["background"])), "%s/%s: Hintergrund" % [id, r["id"]])
			assert_true(ItemDB.has_item(StringName(String(r.get("icon", "")))), "%s/%s: Raum-Symbol" % [id, r["id"]])
			for e: Dictionary in Array(r.get("default_items", [])):
				assert_true(ItemDB.has_item(StringName(String(e["id"]))), "%s/%s: %s" % [id, r["id"], e["id"]])
		var music: String = String(d.get("music", ""))
		assert_true(music.is_empty() or FileAccess.file_exists("res://assets/audio/music/%s.wav" % music), "%s: Musik" % id)
		for n: Dictionary in NpcRoles.npcs_of(id):
			assert_true(rooms.map(func(r: Dictionary) -> String: return String(r["id"])).has(String(n["room"])),
				"%s: NPC %s steht in einem echten Raum" % [id, n["id"]])
		for s: Dictionary in Secrets.for_area(id):
			assert_not_null(Secrets.sticker_def(s), "%s: Sticker für %s" % [id, s["id"]])


func test_every_npc_role_has_known_work_animations() -> void:
	for r: Dictionary in NpcRoles.all().values():
		for a: Variant in Array(r["work"]):
			assert_true(NpcWork.MOTION.has(String(a)), "%s: Animation %s" % [r["id"], a])
		assert_true(CharacterTemplates.ids().has(String(r["template"])), "%s: Schablone" % r["id"])
