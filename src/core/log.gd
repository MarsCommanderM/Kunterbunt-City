extends Node
## Log – einfache, rein lokale Protokollierung (Konsole). Sendet NIEMALS Daten nach außen.

enum Level { DEBUG, INFO, WARN, ERROR }

## Mindest-Level, das ausgegeben wird (in Release-Builds INFO).
var min_level: Level = Level.DEBUG if OS.is_debug_build() else Level.INFO

## Zählt Warnungen/Fehler – nützlich für Tests.
var warn_count: int = 0
var error_count: int = 0


func debug(msg: String) -> void:
	_write(Level.DEBUG, msg)


func info(msg: String) -> void:
	_write(Level.INFO, msg)


func warn(msg: String) -> void:
	warn_count += 1
	_write(Level.WARN, msg)


func error(msg: String) -> void:
	error_count += 1
	_write(Level.ERROR, msg)


func _write(level: Level, msg: String) -> void:
	if level < min_level:
		return
	var line: String = "[%s] %s" % [Level.keys()[level], msg]
	match level:
		Level.WARN:
			push_warning(line)
		Level.ERROR:
			push_error(line)
		_:
			print(line)
