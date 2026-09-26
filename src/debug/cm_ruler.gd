class_name CmRuler
extends Node2D
## Senkrechtes cm-Lineal (steht auf der hinteren Bodenlinie). Striche alle 10 cm, Zahlen alle 50 cm.

@export var height_cm: float = 250.0


func _draw() -> void:
	draw_rect(Rect2(-3, -height_cm, 6, height_cm), Color(1, 0.95, 0.7, 0.95))
	draw_rect(Rect2(-3, -height_cm, 6, height_cm), Color(0.45, 0.3, 0.1), false, 0.6)
	var h: int = 0
	while h <= int(height_cm):
		var big: bool = h % 50 == 0
		draw_line(Vector2(-3, -h), Vector2(3 if big else 0, -h), Color(0.3, 0.2, 0.1), 0.8 if big else 0.4)
		if big:
			WorldText.draw(self, Vector2(5, -h + 3), "%d" % h, 8.0, Color(0.3, 0.2, 0.1))
		h += 10
