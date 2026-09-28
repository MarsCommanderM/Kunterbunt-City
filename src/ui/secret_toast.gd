class_name SecretToast
extends RefCounted
## P07-T10: Geheimnis gefunden → großer Sticker mit Stern springt kurz auf (kein Text), Ton, dann ins Album.


static func show_for(ui: CanvasLayer, id: String) -> void:
	var def: ItemDefinition = Secrets.sticker_def(Secrets.by_id(id))
	var card := Ui.card(Ui.RADIUS, Ui.CARD)
	card.name = "SecretToast"
	card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	card.set_anchors_preset(Control.PRESET_CENTER_TOP)
	card.offset_left = -150
	card.offset_right = 150
	card.offset_top = 150
	card.offset_bottom = 450
	ui.add_child(card)
	var star := Ui.icon("star", 90)
	star.position = Vector2(-20, -30)
	card.add_child(star)
	if def != null:
		var pic: TextureRect = ItemThumb.make(def, 240)
		pic.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 30)
		pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
		card.add_child(pic)
	AudioBus.play_sfx("harvest")
	card.pivot_offset = Vector2(150, 150)
	card.scale = Vector2(0.4, 0.4)
	var tw: Tween = card.create_tween()
	tw.tween_property(card, "scale", Vector2.ONE, 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_interval(2.2)
	tw.tween_property(card, "modulate:a", 0.0, 0.4)
	tw.tween_callback(card.queue_free)
