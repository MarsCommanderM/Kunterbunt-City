extends GutTest
## P07-T09: Musik im Zuhause, Ambiente je Raum (Garten: Vögel, Bad: Tropfen, sonst Raumklang), Regler wirken.

var area: AreaScene


func before_each() -> void:
	SaveSystem.wipe()
	Game.slot = 0
	Game.load_all()
	CharacterRig.animate_poses = false
	var c: CharacterData = CharacterData.create("kid")
	c.skin = "#f7c9a2"
	Game.add_character(c)
	Game.set_active(c.id)


func after_each() -> void:
	AudioBus.play_music("")
	AudioBus.play_ambience("")
	Settings.set_value("volume_music", 0.7)
	SaveSystem.wipe()
	Game.load_all()


func _enter() -> AreaScene:
	SceneRouter.pending_area = &"home"
	area = load("res://src/world/area_scene.tscn").instantiate()
	add_child_autofree(area)
	await wait_process_frames(6)
	return area


func test_musik_und_ambiente_wechseln_mit_dem_raum() -> void:
	var a: AreaScene = await _enter()
	assert_eq(AudioBus.current_music, "music_home")
	assert_eq(AudioBus.current_ambience, "amb_indoor")
	a.switch_room("garden")
	assert_eq(AudioBus.current_ambience, "amb_garden", "draußen Vögel")
	a.switch_room("bath")
	assert_eq(AudioBus.current_ambience, "amb_bath", "im Bad Tropfen")
	assert_eq(AudioBus.current_music, "music_home", "Musik läuft beim Raumwechsel weiter")


func test_musik_regler_wirkt() -> void:
	AudioBus.play_music("music_home")
	Settings.set_value("volume_music", 1.0)
	var loud: float = AudioBus._music.volume_db
	Settings.set_value("volume_music", 0.2)
	assert_lt(AudioBus._music.volume_db, loud - 10.0, "leiser gestellt = leiser")
