class_name I18n
extends RefCounted
## P11-T03: Sprachen für die wenigen Eltern-/Menü-Texte. Daten: data/i18n/<sprache>.json (Schlüssel = deutscher Text).
## Godot übersetzt Beschriftungen (Label/Button) dann von selbst; formatierte Texte nutzen tr("…") % werte.
## Kinder spielen ohne Lesen (R-07) – die Sprache ändert nur Eltern-Bereich und Menüs.

const DIR: String = "res://data/i18n/"
const SOURCE: String = "de"

static var _loaded: Dictionary = {}          ## Sprache → Anzeigename


## Alle Sprachen einmal registrieren. Gibt [[code, Name], …] zurück (Deutsch zuerst).
static func languages() -> Array:
	_load_all()
	var out: Array = [[SOURCE, "Deutsch"]]
	var codes: Array = _loaded.keys()
	codes.sort()
	for c: Variant in codes:
		out.append([String(c), String(_loaded[c])])
	return out


static func apply(lang: String) -> void:
	_load_all()
	TranslationServer.set_locale(lang if (lang == SOURCE or _loaded.has(lang)) else SOURCE)


static func _load_all() -> void:
	if not _loaded.is_empty():
		return
	var dir := DirAccess.open(DIR)
	if dir == null:
		return
	for f: String in dir.get_files():
		if not f.ends_with(".json"):
			continue
		var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(DIR + f))
		if not d is Dictionary:
			Log.warn("I18n: %s ist kaputt" % f)
			continue
		var t := Translation.new()
		t.locale = String(d["locale"])
		var msgs: Dictionary = d.get("messages", {})
		for k: String in msgs:
			t.add_message(k, String(msgs[k]))
			t.add_message(" " + k, " " + String(msgs[k]))   # Ui.button setzt ein Leerzeichen vor den Text
		TranslationServer.add_translation(t)
		_loaded[t.locale] = String(d.get("name", t.locale))
		if not TranslationServer.get_loaded_locales().has(SOURCE):
			var de := Translation.new()                # Deutsch ausdrücklich (sonst nimmt Godot „en“ als Ersatz)
			de.locale = SOURCE
			for k: String in msgs:
				de.add_message(k, k)
				de.add_message(" " + k, " " + k)
			TranslationServer.add_translation(de)
