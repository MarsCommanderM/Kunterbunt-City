extends GutTest
## P03-T01/T02/T03/T07/T08: Schablonen, Maße aus der Tabelle, Posen, Gefühle, Tiefen-Faktor.

var k: KitchenFixture


func before_each() -> void:
	k = KitchenFixture.new(self)


func _rig(tid: String, x: float = 300.0, depth: float = 60.0) -> CharacterRig:
	return ItemSpawner.character_on_floor(k.room, tid, x, depth)


func _height_of(it: ItemNode) -> float:
	return it.global_rect().size.y / it.global_scale.y


## Körperbreite OHNE Frisur (die darf breiter sein als die Tabellenbreite).
func _body_width(c: CharacterRig) -> float:
	var r := Rect2()
	for lname: String in c._layers:
		if lname.begins_with("Hair"):
			continue
		var sp: Sprite2D = c._layers[lname]
		if not sp.is_visible_in_tree():
			continue
		var lr: Rect2 = LayerGeometry.local_xf(c, sp) * sp.get_rect()
		r = lr if not r.has_area() else r.merge(lr)
	return r.size.x


func test_template_heights_come_from_scale_table() -> void:
	for tid: String in ["toddler", "kid", "adult"]:
		var c: CharacterRig = _rig(tid)
		var want: float = ItemDB.height_cm(String(CharacterTemplates.get_template(tid)["scale_ref"]))
		assert_almost_eq(_height_of(c), want, 1.5, "%s ist %d cm hoch (Tabelle)" % [tid, int(want)])
		var ref_w: float = ItemDB.width_cm(String(CharacterTemplates.get_template(tid)["scale_ref"]))
		assert_between(_body_width(c), ref_w * 0.6, ref_w * 1.4,
			"%s: Körperbreite passt zur Tabelle (%d cm)" % [tid, int(ref_w)])
		assert_lt(c.global_rect().size.x / c.global_scale.x, ref_w * 1.7,
			"auch mit Frisur nicht breiter als 1,7 × Tabellenbreite")


func test_sprite_character_keeps_reference_height() -> void:
	var girl: SpriteCharacter = ItemSpawner.character_on_floor(k.room, "char_girl_01", 400.0, 60.0)
	assert_almost_eq(_height_of(girl), 125.0, 2.0, "fertiges Mädchen-Sprite: 125 cm")
	assert_eq(girl.def.category, "character")


func test_depth_factor_applies_to_characters() -> void:
	var back: CharacterRig = _rig("kid", 200.0, 5.0)
	var front: CharacterRig = _rig("kid", 300.0, 70.0)
	assert_almost_eq(front.global_scale.y / back.global_scale.y,
		k.room.floor_band.depth_factor(70.0) / k.room.floor_band.depth_factor(5.0), 0.0001,
		"Figur vorne ist genau so viel größer wie der Tiefen-Faktor es sagt")
	assert_true(front.global_scale.y / back.global_scale.y <= Units.DEPTH_SCALE_LIMIT + 0.0001)


func test_sit_pose_shortens_legs_and_keeps_feet_above_floor() -> void:
	var chair: ItemNode = ItemSpawner.on_floor(k.room, &"home_chair_mint", 300.0, 50.0)
	var kid: CharacterRig = _rig("kid", 300.0, 50.0)
	_kid_sits_on(kid, chair)
	assert_eq(kid.body_pose, "sit")
	var hip: float = float(kid.t["hip"]["y"])
	assert_almost_eq(_h_over(chair, kid.parts.to_global(Vector2(0, -hip)).y), 45.0, 1.0,
		"Hüfte sitzt auf 45 cm")
	var sole: float = _sole_over(chair, kid)
	assert_true(sole > 5.0, "Füße baumeln über dem Boden (%s cm)" % sole)
	# Oberkörper sitzt unverändert auf der Hüfte: Scheitel = Sitz + (Schablonen-Höhe − Hüfte)
	var head_top: float = 45.0 + float(kid.t["hair_top"]) - hip
	assert_almost_eq(_h_over(chair, kid.global_rect().position.y), head_top, 3.0,
		"Kopf bei ~%d cm" % int(head_top))


func test_adult_on_low_sofa_reaches_the_floor() -> void:
	var sofa: ItemNode = ItemSpawner.on_floor(k.room, &"home_sofa", 300.0, 30.0)
	var adult: CharacterRig = _rig("adult", 300.0, 30.0)
	_kid_sits_on(adult, sofa)
	assert_eq(adult.body_pose, "sit")
	assert_almost_eq(_h_over(sofa, adult.parts.to_global(Vector2(0, -float(adult.t["hip"]["y"]))).y), 42.0, 1.0,
		"Sofa: 42 cm")
	assert_almost_eq(_sole_over(sofa, adult), 0.0, 3.0, "Füße stehen auf dem Boden (nicht darunter)")


## P04b: Mit dem großen Kopf liegt die GANZE Figur (Kopf auf dem Kissen) – ein aufrechter Kopf ließ
## lange Haare durch das Bett hängen. Waagerecht läge nur der dicke Kopf auf und der Körper schwebte
## (Blick-Check Luftmatratze) → leicht geneigt: Kopf UND Füße liegen auf, nichts sinkt ein, nichts schwebt.
func test_lie_pose_rests_head_and_feet_on_the_mattress() -> void:
	var bed: ItemNode = ItemSpawner.on_floor(k.room, &"home_bed_kid", 300.0, 30.0)
	var toddler: CharacterRig = _rig("toddler", 300.0, 30.0)
	_kid_sits_on(toddler, bed)
	assert_eq(toddler.body_pose, "lie")
	var rot: float = toddler.parts.global_rotation
	assert_between(rot, -PI * 0.5, -PI * 0.5 + CharacterRig.LIE_TILT_MAX + 0.001, "liegt, höchstens 26° geneigt")
	assert_almost_eq(toddler.head_pivot.global_rotation, rot, 0.001, "Kopf liegt mit auf dem Kissen")
	var feet: Vector2 = toddler.parts.to_global(Vector2.ZERO)
	var hip_g: Vector2 = toddler.parts.to_global(Vector2(0, -float(toddler.t["hip"]["y"])))
	assert_gt(feet.x - hip_g.x, float(toddler.t["hip"]["y"]) * toddler.global_scale.x * cos(CharacterRig.LIE_TILT_MAX) * 0.98,
		"Beine in voller Länge")
	var solid: Array = toddler._layers.values().filter(func(sp: Sprite2D) -> bool: return not String(sp.name).begins_with("Hair"))
	assert_almost_eq(_h_over(bed, _low(toddler, solid)), 45.0, 2.0, "Kopf/Körper liegen auf der Matratze (45 cm)")
	assert_gt(_h_over(bed, _low(toddler, toddler._layers.values())), 45.0 - 12.0, "Haare fallen aufs Kissen, hängen aber nicht durch")
	var legs_bottom: float = _low(toddler, [toddler._layers["Legs"], toddler._layers["Shoes"]])
	assert_almost_eq(_h_over(bed, legs_bottom), 45.0, 4.0, "auch die Beine liegen auf (kein Schweben)")
	assert_lt(_h_over(bed, hip_g.y) - 45.0, 25.0, "Hüfte nah an der Matratze (früher schwebte der Körper)")


func test_six_emotions_cycle_on_head_tap() -> void:
	var kid: CharacterRig = _rig("kid")
	var head: Vector2 = kid.parts.to_global(Vector2(0, -float(kid.t["head"]["cy"])))
	var seen: Array = [kid.emotion]
	for _i: int in 6:
		kid.on_tap_at(head)
		seen.append(kid.emotion)
	assert_eq(CharacterTemplates.emotions().size(), 6)
	assert_eq(seen, ["happy", "laugh", "surprised", "sad", "tired", "love", "happy"],
		"Tipp auf den Kopf schaltet eins weiter und läuft um")


func test_tap_on_body_makes_the_character_laugh() -> void:
	var kid: CharacterRig = _rig("kid")
	kid.set_emotion("sad")
	kid.on_tap_at(kid.global_position + Vector2(0, -10.0))   # Bauch
	assert_eq(kid.emotion, "laugh", "am Körper gekitzelt → lachen")
	var head: Vector2 = kid.parts.to_global(Vector2(0, -float(kid.t["head"]["cy"])))
	kid.on_tap_at(head)                                      # Kopf → eins weiter
	assert_eq(kid.emotion, "surprised")


# ---------------------------------------------------------------- Hilfen
func _kid_sits_on(who: ItemNode, host: ItemNode) -> void:
	var p: Vector2 = Seats.point_global(host, 0)
	if who.has_method("hip_offset"):
		p -= who.hip_offset() * who.global_scale.y
	k.drag_pivot_to(who, p, 7)


## Tiefster gemalter Punkt der Ebenen (Umriss statt Rechteck – bei gedrehten Ebenen genau), global.
func _low(rig: CharacterRig, layers: Array) -> float:
	return rig.to_global(Vector2(0, LayerGeometry.lowest(rig, layers))).y


func _h_over(ref: ItemNode, world_y: float) -> float:
	return (ref.global_position.y - world_y) / ref.global_scale.y


func _sole_over(ref: ItemNode, ch: CharacterRig) -> float:
	var sp: Sprite2D = ch._layers["Shoes"]
	return _h_over(ref, (sp.global_transform * sp.get_rect()).end.y)


## P04b: „Alles geht überall“ – die Schwimmbad-Luftmatratze taugt zu Hause als Bett, die Figur liegt AUF ihr.
func test_kid_lies_on_the_pool_air_mattress() -> void:
	var mat: ItemNode = ItemSpawner.on_floor(k.room, &"pool_air_mattress_coral", 300.0, 30.0)
	var kid: CharacterRig = _rig("kid", 300.0, 30.0)
	_kid_sits_on(kid, mat)
	assert_eq(kid.body_pose, "lie", "Luftmatratze → liegen")
	var solid: Array = kid._layers.values().filter(func(sp: Sprite2D) -> bool: return not String(sp.name).begins_with("Hair"))
	assert_almost_eq(_h_over(mat, _low(kid, solid)), mat.def.seat_h_cm, 2.0, "liegt auf der Matratze, schwebt nicht")
	var legs_bottom: float = _low(kid, [kid._layers["Legs"], kid._layers["Shoes"]])
	assert_almost_eq(_h_over(mat, legs_bottom), mat.def.seat_h_cm, 3.0, "Kopf UND Beine liegen auf")
