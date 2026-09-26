class_name FigureStage
extends SubViewportContainer
## Große Vorschau einer Figur im Editor (P04-T03). Eigene Mini-Welt mit Kamera, damit die Figur
## immer genau ins Bild passt – die cm-Größe kommt dabei nur aus der Schablone.
## Tippen auf die Figur → nächstes Gefühl (kein Lesen nötig).

signal tapped

var _vp: SubViewport
var _world: Node2D
var _cam: Camera2D
var rig: CharacterRig
var template_id: String = "kid"
var look: Dictionary = {}
var emotion: String = "happy"
var show_deco: bool = true

const DECO_COLOR: Color = Color("#efe3d6")


func _ready() -> void:
	stretch = false
	mouse_filter = Control.MOUSE_FILTER_PASS
	_vp = SubViewport.new()
	_vp.size = Vector2i(maxi(64, int(size.x)), maxi(64, int(size.y)))
	_vp.transparent_bg = true
	_vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	_vp.disable_3d = true
	add_child(_vp)
	_world = Node2D.new()
	_vp.add_child(_world)
	_cam = Camera2D.new()
	_world.add_child(_cam)
	_cam.make_current()
	resized.connect(_on_resized)


func _on_resized() -> void:
	if _vp != null:
		_vp.size = Vector2i(maxi(64, int(size.x)), maxi(64, int(size.y)))
		_frame_camera()


## Figur (neu) aufbauen. `keep_emotion` lässt das Gefühl stehen (Editor: Farben umschalten).
func show_look(tid: String, lk: Dictionary, keep_emotion: bool = true) -> void:
	if rig != null and tid == template_id and is_instance_valid(rig):
		look = lk
		rig.apply_look(lk)
		if not keep_emotion:
			set_emotion(emotion)
		_frame_camera()
		return
	template_id = tid
	look = lk
	if rig != null and is_instance_valid(rig):
		rig.queue_free()
	rig = CharacterRig.create_character(tid, lk)
	_world.add_child(rig)
	rig.position = Vector2.ZERO
	set_emotion(emotion if keep_emotion else "happy")
	_deco()
	_frame_camera()


func set_emotion(e: String) -> void:
	emotion = e
	if rig != null:
		rig.set_emotion(e)


func next_emotion() -> void:
	if rig != null:
		rig.next_emotion()
		emotion = rig.emotion


## Bühne: weicher Boden-Schatten und ein heller Kreis hinter der Figur.
func _deco() -> void:
	for c: Node in _world.get_children():
		if c is Polygon2D:
			c.queue_free()
	if not show_deco:
		return
	var h: float = _height_cm()
	var disc := Polygon2D.new()
	disc.polygon = _circle_points(64, h * 0.42)
	disc.color = DECO_COLOR
	disc.position = Vector2(0, -h * 0.02)
	disc.scale = Vector2(1.0, 0.24)
	disc.z_index = -20
	_world.add_child(disc)
	var halo := Polygon2D.new()
	halo.polygon = _circle_points(64, h * 0.46)
	halo.color = Color(1, 1, 1, 0.55)
	halo.position = Vector2(0, -h * 0.58)
	halo.z_index = -21
	_world.add_child(halo)


static func _circle_points(n: int, r: float) -> PackedVector2Array:
	var p := PackedVector2Array()
	for i: int in n:
		var a: float = TAU * float(i) / float(n)
		p.append(Vector2(cos(a), sin(a)) * r)
	return p


func _height_cm() -> float:
	var t: Dictionary = CharacterTemplates.get_template(template_id)
	return float(ItemDB.height_cm(String(t.get("scale_ref", "char_child")))) \
		* float(CharacterTemplates.get_template(template_id).get("scale_mul", 1.0))


## Kamera so setzen, dass die Figur mit etwas Luft drin genau hineinpasst.
func _frame_camera() -> void:
	if _cam == null:
		return
	var h: float = maxf(_height_cm(), 10.0)
	var vh: float = h * 1.18                        # 9 % Luft oben und unten
	var zoom: float = _vp.size.y / vh
	_cam.zoom = Vector2(zoom, zoom)
	_cam.position = Vector2(0.0, -h * 0.5)


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch and event.pressed:
		tapped.emit()
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		tapped.emit()
