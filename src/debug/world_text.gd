class_name WorldText
extends RefCounted
## Scharfer Text in Welt-cm: rendert mit n-facher Schriftgröße und verkleinert per Transform.


static func draw(canvas: CanvasItem, pos: Vector2, text: String, size_cm: float, color: Color,
		centered: bool = false, outline: Color = Color(1, 1, 1, 0.85)) -> void:
	var k: float = UiConstants.WORLD_TEXT_OVERSAMPLE
	var fs: int = roundi(size_cm * k)
	var font: Font = ThemeDB.fallback_font
	var w: float = font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
	var p: Vector2 = pos * k - (Vector2(w * 0.5, 0.0) if centered else Vector2.ZERO)
	canvas.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE / k)
	canvas.draw_string_outline(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, roundi(fs * 0.25), outline)
	canvas.draw_string(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, color)
	canvas.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
