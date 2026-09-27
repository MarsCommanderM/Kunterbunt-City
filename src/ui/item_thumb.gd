class_name ItemThumb
extends RefCounted
## Vorschaubild eines Items für Menüs (Katalog, Rucksack) – mit Farbzonen wie im Spiel.


static func make(def: ItemDefinition, size: float) -> TextureRect:
	var pic := TextureRect.new()
	pic.texture = load(def.sprite_path)
	pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	pic.custom_minimum_size = Vector2(size, size)
	pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if not def.colors.is_empty():
		CharacterLook.apply(pic, Array(def.colors))
	return pic
