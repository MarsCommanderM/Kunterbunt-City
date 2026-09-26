extends Control
## Einstiegsszene (vorläufig). Wird in Phase 05 durch Splash → Editor/Stadtkarte ersetzt.


func _ready() -> void:
	Log.info("Kunterbunt City %s gestartet" % ProjectSettings.get_setting("application/config/version"))
