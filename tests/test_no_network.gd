extends GutTest
## Qualitäts-Tor „Kein Netzwerk“ (MASTERPROMPT R-Regeln, Tech-Spec §6):
## Kein Code in res://src darf Netzwerk-Klassen verwenden. Das Spiel sammelt keine Daten.

const FORBIDDEN: Array[String] = [
	"HTTPRequest", "HTTPClient", "WebSocketPeer", "WebSocketMultiplayerPeer",
	"StreamPeerTCP", "TCPServer", "PacketPeerUDP", "UDPServer", "ENetConnection",
	"ENetMultiplayerPeer", "WebRTCPeerConnection", "JavaScriptBridge", "OS.shell_open",
]


func test_no_network_classes_in_src() -> void:
	var hits: Array[String] = []
	for path: String in _collect("res://src"):
		var lines: PackedStringArray = FileAccess.get_file_as_string(path).split("\n")
		for i: int in lines.size():
			var code: String = lines[i].split("#")[0]
			for word: String in FORBIDDEN:
				if code.contains(word):
					hits.append("%s:%d → %s" % [path, i + 1, word])
	assert_eq(hits.size(), 0, "Verbotene Netzwerk-Nutzung:\n" + "\n".join(hits))


func test_scanner_finds_scripts() -> void:
	assert_gt(_collect("res://src").size(), 0, "Scanner findet keine Skripte – Test wäre wertlos")


func _collect(dir_path: String) -> Array[String]:
	var out: Array[String] = []
	var dir: DirAccess = DirAccess.open(dir_path)
	if dir == null:
		return out
	for f: String in dir.get_files():
		if f.ends_with(".gd"):
			out.append(dir_path.path_join(f))
	for d: String in dir.get_directories():
		out.append_array(_collect(dir_path.path_join(d)))
	return out
