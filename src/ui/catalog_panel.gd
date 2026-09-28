class_name CatalogPanel
extends Control
## P04b-T09: Katalog als Seitenleiste rechts (max. ein Drittel des Bildschirms) – die Welt bleibt sichtbar.
## Oben die Kategorien (kleine Bilder statt Text), darunter alle Items der Kategorie in kleiner Ansicht.
## Antippen → das Ding erscheint sofort im freien Teil des Bildes und ist frei verschiebbar; die Leiste bleibt
## offen, damit man nacheinander Sofa, Schrank, Pflanze … aussuchen kann. Jedes Item geht in JEDEM Raum.

signal placed(id: String)

const WIDTH_FRAC: float = 1.0 / 3.0   ## höchstens ein Drittel des Bildschirms
const TAB: float = 92.0
const TILE: float = 128.0

var _grid: GridContainer
var _tabs: GridContainer
var _place_cb: Callable
var _group: String = ""
var _count: int = 0                   ## wie viele Dinge in dieser Sitzung schon gestellt wurden


static func open(host: Node, place_cb: Callable) -> CatalogPanel:
	var p := CatalogPanel.new()
	p._place_cb = place_cb
	host.add_child(p)
	return p


## Breite der Leiste in Pixeln (für AreaScene: Items erscheinen links davon).
static func panel_width(viewport_w: float) -> float:
	return viewport_w * WIDTH_FRAC


func _ready() -> void:
	var vp: Vector2 = get_viewport_rect().size
	var w: float = panel_width(vp.x)
	anchor_left = 1.0
	anchor_right = 1.0
	anchor_top = 0.0
	anchor_bottom = 1.0
	offset_left = -w
	offset_right = 0.0
	offset_top = 0.0
	offset_bottom = 0.0
	mouse_filter = Control.MOUSE_FILTER_STOP
	var panel := Ui.card(Ui.RADIUS, Ui.CARD)
	panel.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 12)
	add_child(panel)
	var v := Ui.vbox(10)
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 14)
	panel.add_child(v)
	var head := Ui.hbox(8)
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(sp)
	var x := Ui.button("", "close", "ghost", Vector2(80, 80))
	Ui.wire(x, func() -> void: queue_free(), "ui_back")
	head.add_child(x)
	v.add_child(head)
	var inner_w: float = w - 24.0 - 28.0
	# Kategorien: Raster aus kleinen Bildern (erstes Item der Gruppe)
	var tab_cols: int = maxi(3, int(inner_w / (TAB + 8.0)))
	_tabs = Ui.grid(tab_cols, 8)
	v.add_child(_tabs)
	for g: Dictionary in Catalog.groups():
		var b := Ui.tile(TAB)
		b.custom_minimum_size = Vector2(TAB, TAB)
		var def: ItemDefinition = ItemDB.get_item(StringName(String(Array(g["items"])[0])))
		if def != null:
			var pic: TextureRect = ItemThumb.make(def, TAB - 20)
			pic.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 10)
			b.add_child(pic)
		var gid: String = String(g["id"])
		b.set_meta("group", gid)
		Ui.wire(b, func() -> void: show_group(gid))
		_tabs.add_child(b)
	# Items
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(scroll)
	_grid = Ui.grid(maxi(2, int(inner_w / (TILE + 10.0))), 10)
	scroll.add_child(_grid)
	if not Catalog.group_ids().is_empty():
		show_group(String(Catalog.group_ids()[0]))


## Kategorie wechseln (auch für Tests).
func show_group(gid: String) -> void:
	_group = gid
	for b: Node in _tabs.get_children():
		Ui.mark_selected(b as Button, String(b.get_meta("group", "")) == gid)
	for c: Node in _grid.get_children():
		c.queue_free()
	for id: Variant in Catalog.items(gid):
		var def: ItemDefinition = ItemDB.get_item(StringName(String(id)))
		if def == null:
			continue
		var b := Ui.tile(TILE)
		b.custom_minimum_size = Vector2(TILE, TILE)
		Ui.mark_selected(b, false)
		var pic: TextureRect = ItemThumb.make(def, TILE - 22)
		pic.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 11)
		b.add_child(pic)
		var sid: String = String(id)
		b.set_meta("item", sid)
		Ui.wire(b, func() -> void: pick(sid))
		_grid.add_child(b)


func current_group() -> String:
	return _group


## Item gewählt → erscheint im Raum; die Leiste bleibt offen für das nächste Ding.
func pick(id: String) -> void:
	if _place_cb.is_valid() and bool(_place_cb.call(id, _count)):
		_count += 1
		placed.emit(id)
	else:
		AudioBus.play_sfx("deny")
