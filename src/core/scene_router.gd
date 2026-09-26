extends Node
## SceneRouter – Bereichswechsel mit Ladebild (Ziel < 2 s), Spawn am `spawn`-Punkt des
## Bereichs, Rückweg in die Stadtkarte. Die Ladezeit wird gemessen (P05-T05).

signal area_requested(id: StringName)

const MAP_SCENE: String = "res://src/main.tscn"
const AREA_SCENE: String = "res://src/world/area_scene.tscn"

var pending_area: StringName = &""
var last_load_ms: float = 0.0


## Bereich betreten (sofort, ohne Editor-Prüfung – die macht Flow).
func goto_area(id: StringName) -> void:
	if not Areas.is_ready(id):
		Log.warn("SceneRouter: Bereich '%s' hat noch keinen Inhalt" % String(id))
		return
	pending_area = id
	area_requested.emit(id)
	get_tree().change_scene_to_file(AREA_SCENE)


## Welcher Bereich soll geladen werden? (AreaScene holt ihn sich in _ready ab.)
func take_pending_area() -> StringName:
	var a: StringName = pending_area
	pending_area = &""
	return a


func goto_map() -> void:
	get_tree().change_scene_to_file(MAP_SCENE)
