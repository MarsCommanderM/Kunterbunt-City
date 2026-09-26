class_name UndoStack
extends RefCounted
## Rückgängig für Item-Bewegungen (P02-T08): max. 30 Schritte pro Raum.
## Ein Eintrag speichert, wo das Item VORHER war (Eltern-Node, lokale Position, Skalierung, Behälter-Platz).

signal changed(count: int)

const MAX_STEPS: int = 30

var _steps: Array[Dictionary] = []


func push(item: ItemNode, from_parent: Node, from_pos: Vector2, from_scale: Vector2, from_slot: int) -> void:
	_steps.append({"item": item, "parent": from_parent, "pos": from_pos, "scale": from_scale, "slot": from_slot})
	while _steps.size() > MAX_STEPS:
		_steps.pop_front()
	changed.emit(_steps.size())


func size() -> int:
	return _steps.size()


func can_undo() -> bool:
	return not _steps.is_empty()


func clear() -> void:
	_steps.clear()
	changed.emit(0)


## Macht den letzten Schritt rückgängig. false, wenn nichts (Gültiges) mehr da ist.
func undo() -> bool:
	while not _steps.is_empty():
		var s: Dictionary = _steps.pop_back()
		var item: ItemNode = s["item"] if is_instance_valid(s["item"]) else null
		var parent: Node = s["parent"] if is_instance_valid(s["parent"]) else null
		if item == null or parent == null:
			continue
		var old_parent: Node = item.get_parent()
		if old_parent != parent:
			item.reparent(parent, false)
			DragController._relayout_owner(old_parent)
		item.position = s["pos"]
		item.scale = s["scale"]
		item.slot_index = s["slot"]
		item.set_lifted(false, false)
		item.rotation = 0.0
		item.on_placed()
		DragController._relayout_owner(parent)
		changed.emit(_steps.size())
		return true
	changed.emit(0)
	return false
