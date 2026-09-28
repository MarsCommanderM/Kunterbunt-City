class_name NpcSpawner
extends RefCounted
## P08: NPCs eines Raums aufstellen (data/npcs/<bereich>.json) und Ereignisse an sie weitergeben.
## P08-T05 Tagesplan light: Rollen mit "shop": true sind nur 8–20 Uhr da – außer „Läden immer offen" (Standard).
##   Beim Öffnen läuft die Figur vom Eingang (links) an ihren Platz („schließt auf").
## P08-T09: leichte Figuren (Rolle "light": true, Passanten/Badegäste) – max. MAX_LIGHT je Raum, ohne Arbeit.

const MAX_LIGHT: int = 6
const OPEN_H: int = 8
const CLOSE_H: int = 20

## Test-Uhr (Stunde 0–23); < 0 = echte Uhrzeit.
static var fixed_hour: int = -1


static func hour() -> int:
	return fixed_hour if fixed_hour >= 0 else int(Time.get_datetime_dict_from_system()["hour"])


static func is_open(role: Dictionary) -> bool:
	if not bool(role.get("shop", false)) or Settings.shops_always_open:
		return true
	return hour() >= OPEN_H and hour() < CLOSE_H


## Stellt alle NPCs des Raums auf. Gibt die Gehirne zurück.
static func spawn_for_room(room: Room, area_id: String) -> Array:
	return spawn_list(room, NpcRoles.npcs_in_room(area_id, String(room.room_id)))


static func spawn_list(room: Room, list: Array) -> Array:
	var out: Array = []
	var light: int = 0
	for n: Dictionary in list:
		var role: Dictionary = NpcRoles.role(String(n["role"]))
		if not is_open(role):
			continue                                   # Laden zu: Figur ist nicht da
		if bool(role.get("light", false)):
			if light >= MAX_LIGHT:
				continue
			light += 1
		var b: NpcBrain = spawn(room, role, n)
		if b != null:
			if not Settings.shops_always_open and bool(role.get("shop", false)):
				b.body.position = NpcPath.clamp_to_room(room, Vector2(NpcPath.EDGE_CM, b.post.y))
				b.set_state(NpcBrain.State.RETURN)     # kommt herein und geht an die Arbeit
			out.append(b)
	return out


static func spawn(room: Room, role: Dictionary, n: Dictionary) -> NpcBrain:
	var look: Dictionary = Dictionary(role.get("look", {})).duplicate(true)
	var rig: ItemNode = ItemSpawner.character_on_floor(room, String(role.get("template", "adult")),
		float(n.get("x_cm", 100.0)), float(n.get("y_cm", 10.0)), look)
	if not (rig is CharacterRig):
		return null
	rig.name = String(n.get("id", "Npc"))
	return NpcBrain.attach(rig as CharacterRig, room, role, n)


static func brains(room: Room) -> Array:
	var out: Array = []
	if room == null:
		return out
	for c: Node in room.ysort_root.get_children():
		var b: Node = c.get_node_or_null("NpcBrain")
		if b is NpcBrain:
			out.append(b)
	for it: ItemNode in Placement.all_items(room):          # auch sitzende NPCs (auf einem Sofa)
		var b2: Node = it.get_node_or_null("NpcBrain")
		if b2 is NpcBrain and not out.has(b2):
			out.append(b2)
	return out


## Ding abgelegt → erste Rolle, die darauf reagiert (Kasse), bekommt es.
static func item_dropped(room: Room, item: ItemNode) -> bool:
	for b: NpcBrain in brains(room):
		if b.on_item_dropped(item):
			return true
	return false
