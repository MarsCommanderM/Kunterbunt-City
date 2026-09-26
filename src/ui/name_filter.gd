class_name NameFilter
extends RefCounted
## Lokaler Wortfilter für die freie Namenseingabe (P04-T06). Kein Netz, keine Liste von außen –
## nur eine kurze Sperrliste und einfache Regeln. Liefert zusätzlich den bereinigten Text.

const MAX_LEN: int = 16

## Deutsche/englische Sperrliste (Kurzformen, absichtlich konservativ).
static var BLOCKED: PackedStringArray = PackedStringArray([
	"arsch", "arschloch", "fick", "ficken", "fotze", "hure", "hurеnsohn", "idiot", "kacke",
	"kacka", "mist", "nutte", "penis", "pimmel", "pisse", "scheisse", "scheiße", "schlampe",
	"schwanz", "spast", "verarsche", "wichser", "arschgesicht", "bastard", "bitch", "cock",
	"cunt", "dick", "fuck", "nigger", "porn", "pussy", "sex", "shit", "slut", "tits", "wanker",
])


## Erlaubt? (leer = erlaubt, Grund = gesperrt)
static func check(text: String) -> String:
	var t: String = clean(text)
	if t.length() > MAX_LEN:
		return "zu lang"
	var low: String = t.to_lower()
	for b: String in BLOCKED:
		if low.contains(b):
			return "nicht erlaubt"
	if not t.is_valid_identifier() and not _is_name_like(t):
		return "nur Buchstaben, Zahlen, Leerzeichen und -"
	return ""


static func _is_name_like(t: String) -> bool:
	for c: String in t.split("", false):
		if not (c.is_valid_identifier() or c == " " or c == "-" or c == "."):
			return false
	return true


## Mehrfache Leerzeichen raus, vorne/hinten abschneiden.
static func clean(text: String) -> String:
	var t: String = text.strip_edges()
	while t.contains("  "):
		t = t.replace("  ", " ")
	return t


## Ersten Buchstaben groß, Rest klein („mIA“ → „Mia“).
static func pretty(text: String) -> String:
	var out: String = ""
	for w: String in clean(text).split(" ", false):
		out += (" " if not out.is_empty() else "") + w.substr(0, 1).to_upper() + w.substr(1).to_lower()
	return out
