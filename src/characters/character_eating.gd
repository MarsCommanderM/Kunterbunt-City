class_name CharacterEating
extends RefCounted
## Essen (P03-T07): Essen an den Mund → 3 Bisse (Mampf-Gesicht + Geräusch, Essen wird kleiner) → weg → verliebt.


static func eat(rig: CharacterRig, food: ItemNode, animate: bool = true) -> void:
	rig.set_emotion("laugh")
	var fid: StringName = food.def.id
	if not animate:
		food.queue_free()
		rig.set_emotion("love")
		rig.ate.emit(fid)
		return
	var tw: Tween = rig.create_tween()
	for bite: int in 3:
		tw.tween_callback(func() -> void:
			rig._set_part(rig._layers["Mouth"], "mouth_eat_open")
			AudioBus.play_sfx("eat_chomp"))
		tw.tween_interval(0.18)
		tw.tween_callback(func() -> void:
			rig._set_part(rig._layers["Mouth"], "mouth_eat_closed")
			if is_instance_valid(food):
				food.scale *= 0.72)
		tw.tween_interval(0.22)
	tw.tween_callback(func() -> void:
		if is_instance_valid(food):
			food.queue_free()
		rig.set_emotion("love")
		rig.ate.emit(fid))
	tw.tween_interval(1.4)
	tw.tween_callback(func() -> void: rig.set_emotion("happy"))
