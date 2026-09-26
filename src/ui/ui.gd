class_name Kit
extends Node
## UI-Baukasten (P04-T03). Ein Look für das ganze Spiel: warme Karten, dicke runde Knöpfe,
## Symbole statt Text (kein Lese-Zwang). Alle Werte stehen hier – keine Magic Numbers in den
## Bildschirmen. Schrift: Baloo 2 (rund, freundlich, OFL) + Nunito (Fließtext).

const ICON_DIR: String = "res://assets/ui/icons/"
const FONT_DISPLAY: Font = preload("res://assets/fonts/Baloo2.ttf")
const FONT_BODY: Font = preload("res://assets/fonts/Nunito.ttf")

# ------------------------------------------------------------------ Farben (Stil C, kein Schwarz)
const BG_TOP: Color = Color("#fff8ee")
const BG_BOTTOM: Color = Color("#f2e3d4")
const CARD: Color = Color("#ffffff")
const CARD_SOFT: Color = Color("#fbf3ea")
const INK: Color = Color("#2b2440")
const INK_SOFT: Color = Color("#6b6280")
const ACCENT: Color = Color("#ff9f45")     # Orange – Hauptaktion
const ACCENT_DARK: Color = Color("#e8802a")
const TEAL: Color = Color("#48b0a0")
const PINK: Color = Color("#ef6f6c")
const YELLOW: Color = Color("#ffd166")
const LILAC: Color = Color("#8f7ac0")
const DISABLED: Color = Color("#cbc5d6")
const SHADOW: Color = Color(0.35, 0.28, 0.22, 0.16)

# ------------------------------------------------------------------ Größen (Design-Auflösung 1920×1080)
const FONT_TITLE: int = 54
const FONT_BUTTON: int = 36
const FONT_LABEL: int = 30
const FONT_SMALL: int = 24
const RADIUS: int = 34
const RADIUS_SMALL: int = 22
const GAP: int = 18
const MIN_TOUCH: int = 96           # kleinste Tippfläche (Kinderhände)
const BIG_TOUCH: int = 132

static var _theme: Theme
static var _icons: Dictionary = {}


func _ready() -> void:
	# Ein Theme für den ganzen Baum: Schrift + Standardgrößen (wird an die Wurzel gehängt).
	get_tree().root.theme = theme()


# ------------------------------------------------------------------ Theme
static func theme() -> Theme:
	if _theme != null:
		return _theme
	var t := Theme.new()
	t.default_font = FONT_DISPLAY
	t.default_font_size = FONT_LABEL
	t.set_stylebox("panel", "Panel", StyleBoxEmpty.new())
	t.set_color("font_color", "Label", INK)
	t.set_color("font_color", "Button", INK)
	t.set_font_size("font_size", "Button", FONT_BUTTON)
	return t


# ------------------------------------------------------------------ Symbole
static func tex(name: String) -> Texture2D:
	if not _icons.has(name):
		var p: String = ICON_DIR + name + ".png"
		_icons[name] = load(p) if ResourceLoader.exists(p) else null
	return _icons[name]


static func icon(name: String, size: float = 64.0, tint: Color = INK) -> TextureRect:
	var r := TextureRect.new()
	r.texture = tex(name)
	r.custom_minimum_size = Vector2(size, size)
	r.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	r.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	r.modulate = tint
	return r


# ------------------------------------------------------------------ Styles
static func box(fill: Color, radius: int = RADIUS, border: Color = Color(1, 1, 1, 0),
		width: int = 0, shadow: int = 12) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = fill
	s.set_corner_radius_all(radius)
	s.content_margin_left = 18
	s.content_margin_right = 18
	s.content_margin_top = 12
	s.content_margin_bottom = 12
	if width > 0:
		s.set_border_width_all(width)
		s.border_color = border
	if shadow > 0:
		s.shadow_color = SHADOW
		s.shadow_size = shadow
		s.shadow_offset = Vector2(0, 6)
	return s


## Panel (Karte) mit weichem Schatten.
static func card(radius: int = RADIUS, fill: Color = CARD) -> Panel:
	var p := Panel.new()
	p.add_theme_stylebox_override("panel", box(fill, radius))
	return p


static func label(text: String, size: int = FONT_LABEL, color: Color = INK,
		align := HORIZONTAL_ALIGNMENT_CENTER) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	l.horizontal_alignment = align
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	return l


## Großer, runder Knopf. `kind`: "" = weiß, "accent" = Orange, "teal", "pink", "lilac", "ghost".
static func button(text: String, icon_name: String = "", kind: String = "",
		min_size := Vector2(180, MIN_TOUCH)) -> Button:
	var b := Button.new()
	b.custom_minimum_size = min_size
	b.add_theme_font_size_override("font_size", FONT_BUTTON)
	if not icon_name.is_empty() and tex(icon_name) != null:
		b.icon = tex(icon_name)
		b.icon_alignment = HORIZONTAL_ALIGNMENT_LEFT
		b.expand_icon = true
		b.add_theme_constant_override("icon_max_width", int(min_size.y * 0.62))
	if not text.is_empty():
		b.text = " " + text
	var fill: Color = CARD
	var ink: Color = INK
	match kind:
		"accent":
			fill = ACCENT
			ink = Color.WHITE
		"teal":
			fill = TEAL
			ink = Color.WHITE
		"pink":
			fill = PINK
			ink = Color.WHITE
		"lilac":
			fill = LILAC
			ink = Color.WHITE
		"ghost":
			fill = Color(1, 1, 1, 0.0)
			ink = INK_SOFT
		"disabled":
			fill = DISABLED
			ink = Color(0.45, 0.42, 0.52)
	b.add_theme_color_override("font_color", ink)
	b.add_theme_color_override("font_disabled_color", Color(0.4, 0.38, 0.48))
	style_button(b, fill, kind == "ghost")
	return b


static func style_button(b: Button, fill: Color, ghost: bool = false) -> void:
	var r: int = RADIUS_SMALL if b.custom_minimum_size.y <= 84 else RADIUS
	var sh: int = 0 if ghost else 10
	b.add_theme_stylebox_override("normal", box(fill, r, Color(0, 0, 0, 0), 0, sh))
	b.add_theme_stylebox_override("hover", box(fill.lightened(0.06), r, Color(0, 0, 0, 0), 0, sh + 4))
	b.add_theme_stylebox_override("pressed", box(fill.darkened(0.14), r, Color(0, 0, 0, 0), 0, 2))
	b.add_theme_stylebox_override("disabled", box(DISABLED, r, Color(0, 0, 0, 0), 0, 0))
	b.add_theme_stylebox_override("focus", box(fill, r, ACCENT, 5, sh))


## Vierreckige Kachel (Für Auswahl-Listen: Teile, Namen, Tiere …).
static func tile(size: float = 150.0) -> Button:
	var b := Button.new()
	b.custom_minimum_size = Vector2(size, size)
	b.add_theme_font_size_override("font_size", FONT_SMALL)
	b.add_theme_color_override("font_color", INK)
	return b


## Kachel als „ausgewählt“ markieren (dicker Rahmen in Akzentfarbe).
static func mark_selected(b: Button, on: bool) -> void:
	var fill: Color = Color(1, 1, 1, 0.92)
	if on:
		b.add_theme_stylebox_override("normal", box(fill, RADIUS_SMALL, ACCENT, 6, 6))
		b.add_theme_stylebox_override("hover", box(fill, RADIUS_SMALL, ACCENT, 6, 8))
		b.add_theme_stylebox_override("pressed", box(fill, RADIUS_SMALL, ACCENT_DARK, 6, 2))
		b.add_theme_stylebox_override("disabled", box(fill, RADIUS_SMALL, ACCENT, 6, 6))
	else:
		style_button(b, fill)


## Hintergrund des Spiels: warmer Verlauf.
static func background(node: Control) -> Control:
	var tex := GradientTexture2D.new()
	var g := Gradient.new()
	g.set_color(0, BG_TOP)
	g.set_color(1, BG_BOTTOM)
	tex.gradient = g
	tex.fill_from = Vector2(0, 0)
	tex.fill_to = Vector2(0, 1)
	tex.width = 128
	tex.height = 128
	var r := TextureRect.new()
	r.texture = tex
	r.stretch_mode = TextureRect.STRETCH_SCALE
	r.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	node.add_child(r)
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return r


static func vbox(gap: int = GAP) -> VBoxContainer:
	var b := VBoxContainer.new()
	b.add_theme_constant_override("separation", gap)
	return b


static func hbox(gap: int = GAP) -> HBoxContainer:
	var b := HBoxContainer.new()
	b.add_theme_constant_override("separation", gap)
	return b


static func grid(cols: int, gap: int = GAP) -> GridContainer:
	var g := GridContainer.new()
	g.columns = cols
	g.add_theme_constant_override("h_separation", gap)
	g.add_theme_constant_override("v_separation", gap)
	return g


static func row_scroll() -> ScrollContainer:
	var s := ScrollContainer.new()
	s.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	s.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	return s


## Weiches „Plopp“-Feedback + Sound.
static func tap_feedback(b: Button) -> void:
	if not b.is_inside_tree():
		return
	var tw: Tween = b.create_tween()
	tw.tween_property(b, "scale", Vector2(0.94, 0.94), 0.05)
	tw.tween_property(b, "scale", Vector2.ONE, 0.14).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	AudioBus.play_sfx("ui_tap")


## Ein Knopf → Tap-Sound + kleines Stampfen, Callback.
static func wire(b: Button, cb: Callable, sound: String = "ui_tap") -> void:
	b.pressed.connect(func() -> void:
		AudioBus.play_sfx(sound)
		Ui.tap_feedback(b)
		cb.call())
