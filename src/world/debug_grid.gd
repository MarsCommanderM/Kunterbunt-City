class_name DebugGrid
extends Node2D
## 10-cm-Raster für den Debug-Modus (F3). Kräftige Linien alle 50 cm, beschriftet alle 100 cm.

var _w: float = 600.0
var _h: float = 260.0
var _front: float = 80.0


func setup(width_cm: float, height_cm: float, front_y_cm: float) -> void:
	_w = width_cm
	_h = height_cm
	_front = front_y_cm
	queue_redraw()


func _draw() -> void:
	var x: float = 0.0
	while x <= _w:
		var strong: bool = int(roundf(x)) % 50 == 0
		draw_line(Vector2(x, -_h), Vector2(x, _front), Color(0, 0, 0, 0.35 if strong else 0.12), 1.0 if strong else 0.5)
		if int(roundf(x)) % 100 == 0:
			WorldText.draw(self, Vector2(x + 1.5, _front - 2.0), "%d" % int(x), 6.0, Color.BLACK)
		x += 10.0
	var y: float = 0.0
	while y >= -_h:
		var strong_y: bool = int(roundf(-y)) % 50 == 0
		draw_line(Vector2(0, y), Vector2(_w, y), Color(0, 0, 0, 0.35 if strong_y else 0.12), 1.0 if strong_y else 0.5)
		if int(roundf(-y)) % 50 == 0:
			WorldText.draw(self, Vector2(2.0, y - 1.5), "%d cm" % int(-y), 6.0, Color.BLACK)
		y -= 10.0
