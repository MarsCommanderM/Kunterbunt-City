extends Control
## Einstieg: Splash → (Pflicht-Editor) → Galerie → Bereich (src/ui/flow.gd).

func _ready() -> void:
	Log.info("Kunterbunt City %s gestartet" % ProjectSettings.get_setting("application/config/version"))
	Flow.start(self)
