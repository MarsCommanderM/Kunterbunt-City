class_name PetBrain
extends RefCounted
## P08-T07: Bedürfnisse eines Haustiers (Tech-Spec §4.6, „Utility light"). Werte 0–1 steigen langsam.
## Das stärkste (mal Charakterzug-Gewicht) gewinnt, sobald es über NEED_MIN liegt UND es ein passendes Ding im Raum gibt:
##   hunger    → voller Napf (tag pet_bowl, Zustand "full")      → frisst, Napf wird leer
##   play      → Spielzeug (tag pet_toy oder toy_ball…)          → stupst es ein Stück weiter
##   tired     → Körbchen/Kissen (tag pet_bed)                    → schläft eine Weile
##   affection → folgt der Figur (macht PetNode ohnehin)          → wird beim Streicheln (Tippen) gestillt
## Rein kosmetisch: nie krank, nie traurig, kein Druck. Laute: zufällig alle 15–60 s über den AudioBus-Limiter.

const NEEDS: Array = ["hunger", "play", "tired", "affection"]
const RISE_PER_S: Dictionary = {"hunger": 1.0 / 240.0, "play": 1.0 / 150.0, "tired": 1.0 / 300.0, "affection": 1.0 / 120.0}
const NEED_MIN: float = 0.5
const SLEEP_S: float = 12.0
const PUSH_CM: float = 70.0
const VOICE_MIN_S: float = 15.0
const VOICE_MAX_S: float = 60.0
## Charakterzug → Gewichte (verspielt spielt öfter, verschlafen schläft öfter …)
const TRAIT_WEIGHTS: Dictionary = {
	"playful": {"play": 1.5}, "sleepy": {"tired": 1.6}, "greedy": {"hunger": 1.6},
	"curious": {"play": 1.2, "affection": 0.8}, "shy": {"affection": 0.6, "tired": 1.2},
}
## Tier-Laute mit Varianten (P08-T08: Hund 3×, Katze 2×). Katze schnurrt beim Streicheln.
const VOICES: Dictionary = {"pet_dog_bark": ["pet_dog_bark", "pet_dog_bark2", "pet_dog_bark3"],
	"pet_cat_meow": ["pet_cat_meow", "pet_cat_meow2"]}
const PET_SOUND: Dictionary = {"pet_cat_meow": "pet_cat_purr"}

var needs: Dictionary = {"hunger": 0.2, "play": 0.3, "tired": 0.1, "affection": 0.2}
var pet_trait: String = "playful"
var voice_in: float = 30.0
var sleep_left: float = 0.0
var _rng: RandomNumberGenerator


func _init(rng: RandomNumberGenerator, trait_id: String = "playful") -> void:
	_rng = rng
	pet_trait = trait_id
	voice_in = _rng.randf_range(VOICE_MIN_S, VOICE_MAX_S)


func weight(need: String) -> float:
	return float(Dictionary(TRAIT_WEIGHTS.get(pet_trait, {})).get(need, 1.0))


func tick(dt: float) -> void:
	for n: String in NEEDS:
		if n == "tired" and sleep_left > 0.0:
			continue
		needs[n] = minf(1.0, float(needs[n]) + float(RISE_PER_S[n]) * weight(n) * dt)
	if sleep_left > 0.0:
		sleep_left = maxf(0.0, sleep_left - dt)
		needs["tired"] = maxf(0.0, float(needs["tired"]) - dt / SLEEP_S)


## Soll das Tier gerade von sich aus einen Laut machen? (Intervall 15–60 s; der AudioBus begrenzt global 1/8 s)
func voice_due(dt: float) -> bool:
	if sleep_left > 0.0:
		return false
	voice_in -= dt
	if voice_in > 0.0:
		return false
	voice_in = _rng.randf_range(VOICE_MIN_S, VOICE_MAX_S)
	return true


func voice_variant(base: String) -> String:
	var list: Array = VOICES.get(base, [base])
	return String(list[_rng.randi() % list.size()])


static func pet_sound(base: String) -> String:
	return String(PET_SOUND.get(base, base))


## Bedürfnisse nach Stärke (gewichtet), nur die über NEED_MIN.
func ranked() -> Array:
	var out: Array = []
	for n: String in NEEDS:
		if float(needs[n]) >= NEED_MIN:
			out.append(n)
	out.sort_custom(func(a: String, b: String) -> bool: return float(needs[a]) * weight(a) > float(needs[b]) * weight(b))
	return out


## Wohin? → {need, item} oder {} (dann schlendert/folgt das Tier wie gewohnt).
func choose(items: Array) -> Dictionary:
	for n: String in ranked():
		var it: ItemNode = find_for(n, items)
		if it != null:
			return {"need": n, "item": it}
	return {}


static func find_for(need: String, items: Array) -> ItemNode:
	for it: ItemNode in items:
		if it.get_parent() == null or it.get_parent().name != "YSortRoot":
			continue                                        # nur Dinge auf dem Boden (nicht im Schrank/Rucksack)
		match need:
			"hunger":
				if it.def.tags.has("pet_bowl") and it.state == "full":
					return it
			"play":
				if it.def.tags.has("pet_toy") or (String(it.def.id).begins_with("toy_ball_") \
						and not String(it.def.id).begins_with("toy_ball_pit")):
					return it
			"tired":
				if it.def.tags.has("pet_bed"):
					return it
	return null


## Am Ziel angekommen: Bedürfnis stillen und das Ding verändern. Gibt den Ton zurück ("" = keiner).
func satisfy(need: String, item: ItemNode, from: Vector2) -> String:
	needs[need] = 0.0
	match need:
		"hunger":
			ItemStates.set_state(item, "empty", true)
			return "eat_chomp"
		"play":
			var dir: float = signf(item.position.x - from.x) if item.position.x != from.x else 1.0
			item.position.x += dir * PUSH_CM
			return "drop_soft"
		"tired":
			sleep_left = SLEEP_S
			return ""
	return ""


## Streicheln (Tippen) stillt die Zuneigung.
func petted() -> void:
	needs["affection"] = 0.0
