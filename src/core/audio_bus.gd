extends Node
## AudioBus – Effekte (mit kleinem Player-Pool), später Musik/Ambiente und der globale
## Tierlaut-Limiter (max. 1 Tierlaut pro 8 s, Tech-Spec §2).

const ANIMAL_SOUND_COOLDOWN_S: float = 8.0
const SFX_DIR: String = "res://assets/audio/sfx/"
const POOL_SIZE: int = 8
## Material je Kategorie – bestimmt den Abstell-Sound, falls das Item keinen eigenen hat.
const CATEGORY_MATERIAL: Dictionary = {
	"food": "soft", "kitchen": "clink", "toy": "plastic", "furniture": "wood", "fixture": "wood",
	"item": "soft", "school": "wood", "sport": "plastic", "garage": "metal", "shop": "plastic",
}

var _pool: Array[AudioStreamPlayer] = []
var _cache: Dictionary = {}
var _next: int = 0
## Zuletzt gespielte Effekte (für Tests, max. 20).
var history: Array[String] = []
var muted: bool = false
## Zeitquelle für den Tierlaut-Limiter (Tests setzen eine feste Uhr).
var clock: Callable = func() -> float: return Time.get_ticks_msec() / 1000.0
var _last_animal_t: float = -1.0e9


func _ready() -> void:
	for i: int in POOL_SIZE:
		var p := AudioStreamPlayer.new()
		p.bus = &"Master"
		add_child(p)
		_pool.append(p)


func play_sfx(sfx_name: String, pitch_jitter: float = 0.06) -> void:
	history.append(sfx_name)
	if history.size() > 20:
		history.pop_front()
	if muted:
		return
	var stream: AudioStream = _get_stream(sfx_name)
	if stream == null:
		return
	var p: AudioStreamPlayer = _pool[_next]
	_next = (_next + 1) % POOL_SIZE
	p.stream = stream
	p.pitch_scale = 1.0 + randf_range(-pitch_jitter, pitch_jitter)
	p.volume_db = linear_to_db(maxf(0.001, float(Settings.get_value("volume_sfx"))))
	p.play()


## Tierlaut mit globalem Limiter: höchstens einer pro 8 s (egal wie viele Tiere). true = gespielt.
func play_animal(sfx_name: String) -> bool:
	var now: float = clock.call()
	if now - _last_animal_t < ANIMAL_SOUND_COOLDOWN_S:
		return false
	_last_animal_t = now
	play_sfx(sfx_name, 0.1)
	return true


func reset_animal_limiter() -> void:
	_last_animal_t = -1.0e9


## Sound für eine Item-Aktion (pickup/drop/open/close/tap).
func play_item_sfx(def: ItemDefinition, kind: String) -> void:
	if def and def.sfx.has(kind):
		play_sfx(String(def.sfx[kind]))
	elif kind == "drop":
		play_sfx("drop_" + String(CATEGORY_MATERIAL.get(def.category if def else "", "soft")))
	else:
		play_sfx(kind)


func _get_stream(sfx_name: String) -> AudioStream:
	if _cache.has(sfx_name):
		return _cache[sfx_name]
	var path: String = SFX_DIR + sfx_name + ".wav"
	var s: AudioStream = load(path) if ResourceLoader.exists(path) else null
	if s == null:
		Log.debug("AudioBus: Sound fehlt: " + path)
	_cache[sfx_name] = s
	return s
