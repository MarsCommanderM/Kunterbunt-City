class_name AreaHud
extends CanvasLayer
## HUD im Bereich (P05-T06): zurück zur Karte (oben links), 📷 Foto (oben rechts),
## ➕ Katalog (oben rechts, klein, P04b), Rucksack (unten rechts), Rückgängig (unten links). Alles Symbole.
## P07: neben der Karte 🏠 Räume (anderer Raum im selben Bereich) und 🖌 Tapete/Boden.

signal leave
signal backpack
signal photo
signal catalog      ## P04b-T09: Katalog aller Items öffnen
signal rooms        ## P07-T01: Raum-Wahl
signal decor        ## P07-T04: Tapete/Boden

const MARGIN: float = 26.0
const BTN: float = 120.0
const SMALL: float = 96.0     ## kleine Symbole oben rechts (Katalog, Foto)

var _flash: ColorRect
var _pack_btn: Button
var _rooms_btn: Button
var _decor_btn: Button


func setup(undo: UndoStack) -> void:
	layer = 40
	var root := Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)
	_flash = ColorRect.new()
	_flash.color = Color(1, 1, 1, 0.0)
	_flash.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_flash)

	var back := _button("map", "accent", Control.PRESET_TOP_LEFT)
	back.pressed.connect(func() -> void: leave.emit())
	root.add_child(back)
	_rooms_btn = _button("home", "teal", Control.PRESET_TOP_LEFT, SMALL)
	_rooms_btn.name = "RoomsButton"
	_rooms_btn.offset_left += BTN + MARGIN * 0.6
	_rooms_btn.offset_right += BTN + MARGIN * 0.6
	_rooms_btn.pressed.connect(func() -> void: rooms.emit())
	root.add_child(_rooms_btn)
	_decor_btn = _button("brush", "lilac", Control.PRESET_TOP_LEFT, SMALL)
	_decor_btn.name = "DecorButton"
	_decor_btn.offset_left += BTN + SMALL + MARGIN * 1.2
	_decor_btn.offset_right += BTN + SMALL + MARGIN * 1.2
	_decor_btn.pressed.connect(func() -> void: decor.emit())
	root.add_child(_decor_btn)
	show_room_buttons(false, false)
	# Oben rechts: kleines Katalog-Symbol (immer da) – daneben 📷 Foto
	var cat := _button("plus", "accent", Control.PRESET_TOP_RIGHT, SMALL)
	cat.name = "CatalogButton"
	cat.pressed.connect(func() -> void: catalog.emit())
	root.add_child(cat)
	var cam := _button("camera", "teal", Control.PRESET_TOP_RIGHT, SMALL)
	cam.offset_left -= SMALL + MARGIN * 0.6
	cam.offset_right -= SMALL + MARGIN * 0.6
	cam.pressed.connect(func() -> void: photo.emit())
	root.add_child(cam)
	_pack_btn = _button("backpack", "lilac", Control.PRESET_BOTTOM_RIGHT)
	_pack_btn.pressed.connect(func() -> void: backpack.emit())
	root.add_child(_pack_btn)

	if undo != null:
		var undo_btn := UndoButton.new()
		undo_btn.undo = undo
		root.add_child(undo_btn)
		_pin(undo_btn, Control.PRESET_BOTTOM_LEFT, undo_btn.get_combined_minimum_size().max(Vector2(BTN, BTN)))


func _button(icon_name: String, kind: String, preset: int, size: float = BTN) -> Button:
	var b := Ui.button("", icon_name, kind, Vector2(size, size))
	b.add_theme_constant_override("icon_max_width", int(size * 0.6))
	_pin(b, preset, Vector2(size, size))
	Ui.wire(b, func() -> void: pass)
	return b


## Ecke + Rand explizit setzen (PRESET_MODE_MINSIZE kannte die Größe noch nicht → Knöpfe rechts/unten ragten
## halb aus dem Bild, gefunden auf den P07-Beweisbildern).
static func _pin(c: Control, preset: int, sz: Vector2) -> void:
	c.set_anchors_preset(preset)
	var right: bool = preset in [Control.PRESET_TOP_RIGHT, Control.PRESET_BOTTOM_RIGHT]
	var bottom: bool = preset in [Control.PRESET_BOTTOM_LEFT, Control.PRESET_BOTTOM_RIGHT]
	c.offset_left = -MARGIN - sz.x if right else MARGIN
	c.offset_right = -MARGIN if right else MARGIN + sz.x
	c.offset_top = -MARGIN - sz.y if bottom else MARGIN
	c.offset_bottom = -MARGIN if bottom else MARGIN + sz.y


## Räume-Knopf nur, wenn der Bereich mehrere Räume hat; Pinsel nur bei wählbarer Tapete/Boden.
func show_room_buttons(rooms_on: bool, decor_on: bool) -> void:
	if _rooms_btn != null:
		_rooms_btn.visible = rooms_on
	if _decor_btn != null:
		_decor_btn.visible = decor_on


## Liegt der Zeiger/Finger auf dem Rucksack-Knopf? (Ding einpacken)
func is_over_backpack() -> bool:
	if _pack_btn == null or not is_instance_valid(_pack_btn):
		return false
	return _pack_btn.get_global_rect().has_point(get_viewport().get_mouse_position())


## Kurzer weißer Blitz beim Fotografieren (wie ein Blitzlicht).
func flash() -> void:
	if _flash == null:
		return
	_flash.color = Color(1, 1, 1, 0.85)
	var tw: Tween = create_tween()
	tw.tween_property(_flash, "color", Color(1, 1, 1, 0.0), 0.35)
