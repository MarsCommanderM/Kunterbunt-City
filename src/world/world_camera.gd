class_name WorldCamera
extends Camera2D
## Kamera in cm (Regel S-08): zeigt standardmäßig 300 cm Höhe.
## Pinch-Zoom (Touch) und Mausrad, Wisch-Scrollen mit Trägheit, bleibt in den Raumgrenzen.
## Tickt nur, solange sie gleitet (kein Dauer-_process, MASTERPROMPT §7).

signal view_changed(visible_rect: Rect2)

const WHEEL_STEP: float = 1.1          # Zoomfaktor pro Mausrad-Raste
const FRICTION: float = 6.0            # Abbremsen der Trägheit (1/s)
const MIN_FLING_SPEED: float = 20.0    # cm/s – darunter stoppt das Gleiten

@export var visible_h_cm: float = Units.DEFAULT_VIEW_HEIGHT_CM
@export var min_h_cm: float = 220.0
@export var max_h_cm: float = 450.0
## Kamera verarbeitet Eingaben selbst (in Phase 02 übernimmt DragController den Vorrang bei Items).
@export var handle_input: bool = true

var bounds: Rect2 = Rect2(0, -300, 600, 400)
var _velocity: Vector2 = Vector2.ZERO    # cm/s
var _touches: Dictionary = {}            # index -> Position (Screen-px)
var _mouse_dragging: bool = false
var _pinch_start_dist: float = 0.0
var _pinch_start_h: float = 0.0
var _last_move_time: float = 0.0


func _ready() -> void:
	set_process(false)
	_apply_zoom()


## Übernimmt Grenzen + Kamera-Werte eines Raums und springt an den Start (Boden sichtbar, x = focus oder links).
func setup_for_room(room: Room, focus_x_cm: float = -1.0) -> void:
	var cfg: Dictionary = room.camera_cfg
	min_h_cm = float(cfg.get("min_h_cm", 220.0))
	max_h_cm = float(cfg.get("max_h_cm", 450.0))
	bounds = room.camera_bounds()
	set_visible_height(float(cfg.get("default_h_cm", Units.DEFAULT_VIEW_HEIGHT_CM)))
	var vs: Vector2 = view_size()
	var x: float = focus_x_cm if focus_x_cm >= 0.0 else bounds.position.x + vs.x * 0.5
	position = Vector2(x, bounds.end.y - vs.y * 0.5)
	_clamp_position()


func viewport_px() -> Vector2:
	return get_viewport_rect().size


## Sichtbare Größe in cm.
func view_size() -> Vector2:
	return viewport_px() / zoom


func visible_rect() -> Rect2:
	var vs: Vector2 = view_size()
	return Rect2(position - vs * 0.5, vs)


## Setzt die sichtbare Höhe (geklemmt auf min/max). anchor_world bleibt dabei an derselben Bildschirmstelle.
func set_visible_height(h_cm: float, anchor_world: Variant = null) -> void:
	var before: Vector2 = Vector2.ZERO
	if anchor_world is Vector2:
		before = world_to_screen(anchor_world)
	visible_h_cm = clampf(h_cm, min_h_cm, max_h_cm)
	_apply_zoom()
	if anchor_world is Vector2:
		position += (anchor_world as Vector2) - screen_to_world(before)
	_clamp_position()


func zoom_by(factor: float, anchor_world: Variant = null) -> void:
	set_visible_height(visible_h_cm / factor, anchor_world)


## Verschiebt um Bildschirm-Pixel (Finger nach rechts → Welt nach rechts).
func pan_by_screen(delta_px: Vector2) -> void:
	position -= delta_px / zoom
	_clamp_position()


func screen_to_world(p: Vector2) -> Vector2:
	return position + (p - viewport_px() * 0.5) / zoom


func world_to_screen(p: Vector2) -> Vector2:
	return (p - position) * zoom + viewport_px() * 0.5


func fling(velocity_cm_s: Vector2) -> void:
	_velocity = velocity_cm_s
	set_process(_velocity.length() > MIN_FLING_SPEED)


func is_gliding() -> bool:
	return is_processing()


func _apply_zoom() -> void:
	var z: float = Units.zoom_for_visible_height(viewport_px().y, visible_h_cm)
	zoom = Vector2(z, z)


func _clamp_position() -> void:
	var vs: Vector2 = view_size()
	var p: Vector2 = position
	p.x = bounds.get_center().x if vs.x >= bounds.size.x else clampf(p.x, bounds.position.x + vs.x * 0.5, bounds.end.x - vs.x * 0.5)
	p.y = bounds.get_center().y if vs.y >= bounds.size.y else clampf(p.y, bounds.position.y + vs.y * 0.5, bounds.end.y - vs.y * 0.5)
	position = p
	view_changed.emit(visible_rect())


func _process(delta: float) -> void:
	var before: Vector2 = position
	position += _velocity * delta
	_clamp_position()
	if position.is_equal_approx(before):
		_velocity = Vector2.ZERO
	_velocity *= exp(-FRICTION * delta)
	if _velocity.length() < MIN_FLING_SPEED:
		_velocity = Vector2.ZERO
		set_process(false)


func _unhandled_input(event: InputEvent) -> void:
	if not handle_input:
		return
	if event is InputEventMouseButton:
		_on_mouse_button(event as InputEventMouseButton)
	elif event is InputEventMouseMotion and _mouse_dragging:
		_drag_move((event as InputEventMouseMotion).relative)
	elif event is InputEventScreenTouch:
		_on_touch(event as InputEventScreenTouch)
	elif event is InputEventScreenDrag:
		_on_screen_drag(event as InputEventScreenDrag)
	elif event is InputEventMagnifyGesture:
		zoom_by((event as InputEventMagnifyGesture).factor, screen_to_world(event.position))


func _on_mouse_button(e: InputEventMouseButton) -> void:
	match e.button_index:
		MOUSE_BUTTON_WHEEL_UP:
			if e.pressed:
				zoom_by(WHEEL_STEP, screen_to_world(e.position))
		MOUSE_BUTTON_WHEEL_DOWN:
			if e.pressed:
				zoom_by(1.0 / WHEEL_STEP, screen_to_world(e.position))
		MOUSE_BUTTON_LEFT, MOUSE_BUTTON_MIDDLE, MOUSE_BUTTON_RIGHT:
			_mouse_dragging = e.pressed
			if e.pressed:
				fling(Vector2.ZERO)
			else:
				_release_fling()


func _on_touch(e: InputEventScreenTouch) -> void:
	if e.pressed:
		_touches[e.index] = e.position
		fling(Vector2.ZERO)
	else:
		_touches.erase(e.index)
		if _touches.is_empty():
			_release_fling()
	_pinch_start_dist = 0.0   # bei Fingerwechsel Pinch neu beginnen


func _on_screen_drag(e: InputEventScreenDrag) -> void:
	var prev: Vector2 = _touches.get(e.index, e.position)
	_touches[e.index] = e.position
	if _touches.size() == 1:
		_drag_move(e.position - prev)
	elif _touches.size() >= 2:
		var pts: Array = _touches.values()
		var a: Vector2 = pts[0]
		var b: Vector2 = pts[1]
		var dist: float = a.distance_to(b)
		if _pinch_start_dist <= 0.0:
			_pinch_start_dist = dist
			_pinch_start_h = visible_h_cm
		var mid: Vector2 = (a + b) * 0.5
		set_visible_height(_pinch_start_h * _pinch_start_dist / maxf(dist, 1.0), screen_to_world(mid))
		pan_by_screen((e.position - prev) * 0.5)


func _drag_move(delta_px: Vector2) -> void:
	pan_by_screen(delta_px)
	var now: float = Time.get_ticks_msec() / 1000.0
	var dt: float = clampf(now - _last_move_time, 1.0 / 240.0, 0.1)
	_last_move_time = now
	_velocity = _velocity.lerp(-delta_px / zoom / dt, 0.4)


func _release_fling() -> void:
	var idle: float = Time.get_ticks_msec() / 1000.0 - _last_move_time
	fling(_velocity if idle < 0.08 else Vector2.ZERO)
