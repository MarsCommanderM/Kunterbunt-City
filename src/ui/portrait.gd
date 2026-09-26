class_name Portrait
extends RefCounted
## Kleines Figuren-Bild für Galerie, Figuren-Knopf und Haustier-Editor (P04-T08).
## Eine einzige versteckte Mini-Welt rendert alle Porträts nacheinander; Ergebnisse werden
## zwischengespeichert (Schlüssel = Schablone + Aussehen), damit die Galerie nicht ruckelt.

static var _vp: SubViewport
static var _world: Node2D
static var _cam: Camera2D
static var _cache: Dictionary = {}


static func _ensure(size: Vector2i) -> void:
	if _vp == null:
		_vp = SubViewport.new()
		_vp.name = "PortraitCam"
		_vp.transparent_bg = true
		_vp.disable_3d = true
		_vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		var tree: SceneTree = Engine.get_main_loop() as SceneTree
		tree.root.add_child(_vp)
		_world = Node2D.new()
		_vp.add_child(_world)
		_cam = Camera2D.new()
		_world.add_child(_cam)
		_cam.make_current()
	_vp.size = size


static func key(tid: String, look: Dictionary) -> String:
	return "%s#%s" % [tid, JSON.stringify(look)]


## Porträt rendern (async: braucht 2 Frames). Gibt ein Texture2D zurück (nie null, falls Welt fehlt).
static func capture(tid: String, look: Dictionary, w: int = 240, h: int = 280) -> Texture2D:
	var k: String = key(tid, look) + "#%dx%d" % [w, h]
	if _cache.has(k):
		return _cache[k]
	var tree: SceneTree = Engine.get_main_loop() as SceneTree
	if tree == null:
		return null
	if not can_render():
		return null
	_ensure(Vector2i(w, h))
	var rig := CharacterRig.create_character(tid, look)
	_world.add_child(rig)
	var t: Dictionary = CharacterTemplates.get_template(tid)
	var hcm: float = maxf(float(ItemDB.height_cm(String(t.get("scale_ref", "char_child")))), 10.0)
	var zoom: float = float(h) / (hcm * 1.12)
	_cam.zoom = Vector2(zoom, zoom)
	_cam.position = Vector2(0.0, -hcm * 0.5)
	# Zwei Prozess-Frames reichen und funktionieren auch OHNE Bildschirm (--headless).
	await tree.process_frame
	await tree.process_frame
	var vpt: Texture2D = _vp.get_texture()
	var img: Image = vpt.get_image() if vpt != null else null
	var out: Texture2D = null
	if img != null and not img.is_empty():
		out = ImageTexture.create_from_image(img)
	rig.queue_free()
	await tree.process_frame
	if out != null:
		_cache[k] = out
	return out


## Porträts brauchen echtes Rendern. Ohne Bildschirm (--headless, Dummy-Renderer) gibt es
## kein Bild – dann liefert capture() null und die Galerie zeigt nur den Namen.
static func can_render() -> bool:
	return DisplayServer.get_name() != "headless"


static func clear_cache() -> void:
	_cache.clear()
