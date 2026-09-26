class_name CharacterData
extends RefCounted
## P04-T02: Datenmodell einer Figur (Schablone, Hautton, Teile + Farben, Name, Stimme, Outfits).
## ↔ JSON über to_dict()/from_dict(), gespeichert wird über SaveSystem.
## Regel: Die GRÖSSE kommt nur aus der Schablone (Maßstab-Tabelle) – nie aus Teilen oder Farben.

const OUTFITS: int = 5          ## 5 Outfit-Plätze pro Figur (T05)
const VOICES: int = 8           ## Stimmen 1…8

var id: StringName
var template_id: String = "kid"
var character_name: String = ""
var voice: int = 1
var skin: String = ""                 ## leer = noch nicht gewählt (Pflicht-Ablauf T07)
var parts: Dictionary = {}            ## slot → Varianten-Id
var colors: Dictionary = {}           ## slot → [Farbe Zone 1, Zone 2, Zone 3]
var outfits: Array = []               ## 5 Plätze: {} oder {"parts": …, "colors": …}
var outfit: int = -1                  ## aktives Outfit, −1 = Basis-Look
var folder: String = "Familie"
var created_ms: int = 0


static func create(tid: String = "kid") -> CharacterData:
	var d := CharacterData.new()
	d.id = StringName("c_%d_%d" % [Time.get_unix_time_from_system(), randi() % 100000])
	d.template_id = tid
	d.created_ms = Time.get_ticks_msec()
	var set: Dictionary = CharacterParts.default_set(tid)
	d.parts = set["parts"]
	d.colors = set["colors"]
	d.outfits = []
	for _i: int in OUTFITS:
		d.outfits.append({})
	return d


func to_dict() -> Dictionary:
	return {
		"id": String(id), "template": template_id, "name": character_name, "voice": voice,
		"skin": skin, "parts": parts, "colors": colors, "outfits": outfits, "outfit": outfit,
		"folder": folder, "created_ms": created_ms,
	}


static func from_dict(d: Dictionary) -> CharacterData:
	if not d is Dictionary or d.is_empty():
		return null
	var c := CharacterData.new()
	c.id = StringName(String(d.get("id", "c_0")))
	c.template_id = String(d.get("template", "kid"))
	c.character_name = String(d.get("name", ""))
	c.voice = clampi(int(d.get("voice", 1)), 1, VOICES)
	c.skin = String(d.get("skin", ""))
	c.parts = d.get("parts", {})
	c.colors = d.get("colors", {})
	c.outfits = d.get("outfits", [])
	while c.outfits.size() < OUTFITS:
		c.outfits.append({})
	c.outfit = clampi(int(d.get("outfit", -1)), -1, OUTFITS - 1)
	c.folder = String(d.get("folder", "Familie"))
	c.created_ms = int(d.get("created_ms", 0))
	return c


## Pflicht-Ablauf (T07): erst mit Schablone UND Hautton ist die Figur fertig.
func is_complete() -> bool:
	return CharacterTemplates.get_template(template_id).has("hip") and not skin.is_empty()


func display_name() -> String:
	return character_name if not character_name.is_empty() else "?"


## Alles, was der CharacterRig zum Bauen braucht.
func look(out: Dictionary = {}) -> Dictionary:
	var l: Dictionary = {"skin": skin, "parts": parts.duplicate(true),
		"colors": colors.duplicate(true)}
	if outfit >= 0 and outfit < outfits.size():
		var o: Dictionary = outfits[outfit]
		if not o.is_empty():
			l["parts"] = Dictionary(o.get("parts", {})).duplicate(true)
			l["colors"] = Dictionary(o.get("colors", {})).duplicate(true)
	l.merge(out, true)
	return l


func set_color(slot: String, zone: int, hex: String) -> void:
	var cols: Array = colors.get(slot, [])
	while cols.size() <= zone:
		cols.append(hex)
	cols[zone] = hex
	colors[slot] = cols


func randomize_look(rng: RandomNumberGenerator) -> void:
	var set: Dictionary = CharacterParts.random_set(template_id, rng)
	parts = set["parts"]
	colors = set["colors"]
	var skins: Array = CharacterParts.palette_colors("skin")
	if not skins.is_empty():
		skin = String(skins[rng.randi() % skins.size()])


## Aktuellen Look auf Outfit-Platz i legen / anziehen / löschen.
func store_outfit(i: int) -> void:
	if i < 0 or i >= OUTFITS:
		return
	outfits[i] = {"parts": parts.duplicate(true), "colors": colors.duplicate(true)}


func wear_outfit(i: int) -> void:
	if i < 0 or i >= OUTFITS:
		return
	var o: Dictionary = outfits[i]
	if o.is_empty():
		return
	outfit = i


func clear_outfit(i: int) -> void:
	if i < 0 or i >= OUTFITS:
		return
	outfits[i] = {}
	if outfit == i:
		outfit = -1
