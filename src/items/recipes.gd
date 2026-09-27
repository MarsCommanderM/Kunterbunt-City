class_name Recipes
extends RefCounted
## P04b-T10 (Vorgriff auf P07-T06): Kochen ist datengetrieben (data/recipes/*.json, R-06).
## Regel: Zutat liegt IN einem Gerät (Behälter mit „open_top“), das Gerät ist „an“ (oder steht in/auf einem
## Gerät, das an ist – Pfanne im Herd) → nach `time` Sekunden wird die Zutat zum Ergebnis.
## IDs werden über den Anfang verglichen: "food_egg" passt auf food_egg_cream, food_egg_oak …

const DIR: String = "res://data/recipes/"
static var _rules: Array = []
static var instant: bool = false      ## Tests/Beweisbilder: sofort kochen statt warten


static func rules() -> Array:
	if _rules.is_empty():
		for f: String in DirAccess.get_files_at(DIR):
			if not f.ends_with(".json"):
				continue
			var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(DIR + f))
			if d is Dictionary:
				_rules.append_array(Array((d as Dictionary).get("recipes", [])))
	return _rules


## Passende Regel für Gerät + Zutat (oder {}).
static func find(host_id: String, ingredient_id: String) -> Dictionary:
	for r: Dictionary in rules():
		if not host_id.begins_with(String(r["host"])):
			continue
		for pre: Variant in Array(r["in"]):
			if ingredient_id.begins_with(String(pre)):
				return r
	return {}


## Nach Zustandswechsel oder neuer Zutat: alles im Gerät prüfen (auch Geräte im Gerät, z. B. Pfanne im Herd).
static func check(host: ItemNode) -> void:
	if host == null or not host.def.is_container():
		return
	for c: Node in host.contents_root.get_children():
		if c is ItemNode:
			var inner: ItemNode = c
			if inner.def.is_container():
				check(inner)
			if not ItemStates.is_on(host):
				continue
			var r: Dictionary = find(String(host.def.id), String(inner.def.id))
			if r.is_empty() or inner.has_meta("cooking"):
				continue
			inner.set_meta("cooking", true)
			if instant or not host.is_inside_tree():
				_cook(host, inner, r)
			else:
				host.get_tree().create_timer(float(r.get("time", 1.5))).timeout.connect(
					func() -> void: _cook(host, inner, r))


static func _cook(host: ItemNode, inner: ItemNode, r: Dictionary) -> void:
	if not is_instance_valid(host) or not is_instance_valid(inner) or inner.get_parent() != host.contents_root:
		return
	if not ItemStates.is_on(host):
		inner.remove_meta("cooking")
		return
	var slot: int = inner.slot_index
	inner.get_parent().remove_child(inner)
	inner.queue_free()
	var out: ItemNode = ItemSpawner.make(StringName(String(r["out"])))
	if out == null:
		return
	host.contents_root.add_child(out)
	out.slot_index = slot
	host.relayout_contents()
	AudioBus.play_sfx(String(r.get("sfx", "ui_confirm")))
