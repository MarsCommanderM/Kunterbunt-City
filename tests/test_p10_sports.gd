extends GutTest
## P10e Sportzentrum: Daten, Ball schießen (rollt weg von der Figur), Tor-Erkennung + Anzeigetafel + Trainer,
## Ball ins Tor legen, Kletterwand, Tutu anziehen.

var k: KitchenFixture
var fake: AreaScene


func before_each() -> void:
	NpcBrain.autonomous = false
	Settings.reduced_motion = true
	k = KitchenFixture.new(self)
	fake = AreaScene.new()
	fake.room = k.room


func after_each() -> void:
	Settings.reduced_motion = false
	fake.free()


func after_all() -> void:
	NpcBrain.autonomous = true


func _kid(x: float, y: float = 40.0) -> CharacterRig:
	return ItemSpawner.character_on_floor(k.room, "kid", x, y) as CharacterRig


func test_sports_area_has_seven_rooms_npcs_and_secrets() -> void:
	var d: Dictionary = Room.load_area(Areas.path_of(&"sports"))
	assert_eq(Array(d["rooms"]).size(), 7)
	assert_eq(NpcRoles.npcs_of("sports").size(), 6)
	assert_eq(Secrets.for_area("sports").size(), 6)
	assert_true(Areas.is_ready(&"sports"))


func test_kick_rolls_the_ball_away_from_the_figure() -> void:
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"spc_football_white", 300.0, 40.0)
	_kid(240.0)
	assert_true(AreaActions.on_tapped(fake, ball))
	assert_almost_eq(ball.position.x, 300.0 + SportActions.KICK_CM, 0.5, "nach rechts, weg von der Figur")


func test_goal_is_detected_scoreboard_counts_and_coach_claps() -> void:
	var goal: ItemNode = ItemSpawner.on_floor(k.room, &"spc_goal_white", 560.0, 40.0)
	var board: ItemNode = ItemSpawner.on_wall(k.room, &"spc_scoreboard_navy", 300.0, -230.0)
	var coach: NpcBrain = NpcSpawner.spawn(k.room, NpcRoles.role("coach"), {"id": "c", "role": "coach", "x_cm": 150, "y_cm": 60})
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"spc_football_white", 400.0, 45.0)
	_kid(340.0)
	assert_eq(board.state, "s0")
	assert_true(SportActions.kick(k.room, ball), "Tor!")
	assert_almost_eq(ball.position.x, goal.position.x, 0.5, "Ball liegt im Netz")
	assert_eq(board.state, "s1", "Anzeigetafel zählt")
	assert_eq(coach.anim, "clap", "Trainer klatscht")


func test_kick_away_from_the_goal_is_no_goal() -> void:
	ItemSpawner.on_floor(k.room, &"spc_goal_white", 560.0, 40.0)
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"spc_football_white", 300.0, 45.0)
	_kid(360.0)
	assert_false(SportActions.kick(k.room, ball), "Schuss nach links")
	assert_lt(ball.position.x, 300.0)


func test_ball_dropped_into_the_goal_counts() -> void:
	ItemSpawner.on_floor(k.room, &"spc_goal_white", 560.0, 40.0)
	var board: ItemNode = ItemSpawner.on_wall(k.room, &"spc_scoreboard_navy", 300.0, -230.0)
	var ball: ItemNode = ItemSpawner.on_floor(k.room, &"spc_football_white", 540.0, 45.0)
	AreaActions.on_dropped(fake, ball)
	assert_eq(board.state, "s1")


func test_tutu_in_hand_is_worn() -> void:
	var kid: CharacterRig = _kid(300.0)
	var tutu: ItemNode = ItemSpawner.on_floor(k.room, &"spc_tutu_rose", 420.0, 40.0)
	var grip: Vector2 = PlacementCharacter.grip_global(tutu, Vector2.ZERO)
	var t: Placement.Target = k.drag_pivot_to(tutu, (kid.hand_slots()[0]["global"] as Vector2) - grip, 3)
	assert_eq(t.kind, &"hand")
	assert_true(AreaActions.on_dropped(fake, tutu))
	assert_eq(String(Dictionary(kid.look["parts"])["bottom"]), "tutu")
