extends Node2D
## Main scene: world map + ports + ship + events + UI.

@onready var port_layer: Node2D = $PortLayer
@onready var ship_layer: Node2D = $ShipLayer
@onready var wind_overlay: Node2D = $WindOverlay
@onready var gold_label: Label = $UI/GoldLabel
@onready var dura_label: Label = $UI/DuraLabel
@onready var date_label: Label = $UI/DateLabel
@onready var info_label: Label = $UI/InfoLabel
@onready var port_screen_panel: PanelContainer = $UI/PortScreenPanel
@onready var port_screen_title: Label = $UI/PortScreenPanel/V/Title
@onready var port_screen_image: TextureRect = $UI/PortScreenPanel/V/Image
@onready var governor_portrait: TextureRect = $UI/PortScreenPanel/V/GovernorRow/Portrait
@onready var governor_label: Label = $UI/PortScreenPanel/V/GovernorRow/Label
@onready var trade_list: VBoxContainer = $UI/PortScreenPanel/V/Tabs/贸易/List
@onready var shipyard_list: VBoxContainer = $UI/PortScreenPanel/V/Tabs/船坞/List
@onready var tavern_list: VBoxContainer = $UI/PortScreenPanel/V/Tabs/酒馆/List
@onready var event_dialog: PanelContainer = $UI/EventDialog
@onready var combat_panel: PanelContainer = $UI/Combat

var ship: Node2D = null
var current_port_id: int = -1
var pending_sail_days: int = 0

const EVENT_CHANCE_PER_SEC := 0.04
const MIN_TIME_BETWEEN_EVENTS := 5.0
var time_since_event: float = MIN_TIME_BETWEEN_EVENTS


func _pn(port: Dictionary) -> String:
	return port.get("cn_name", port.get("name", "?"))


func _ready() -> void:
	randomize()
	AudioManager.play("port")
	GameState.gold_changed.connect(_on_gold_changed)
	GameState.ship_changed.connect(_on_ship_changed)
	GameState.date_changed.connect(_on_date_changed)
	_on_gold_changed(GameState.gold)
	_on_ship_changed()
	_on_date_changed()
	port_screen_panel.visible = false
	event_dialog.visible = false
	combat_panel.visible = false
	event_dialog.option_chosen.connect(_on_event_option_chosen)
	combat_panel.combat_ended.connect(_on_combat_ended)
	_spawn_ports()
	_spawn_ship()
	# Initialize starter ship before any potential load
	var starter := GameState.get_ship(1)
	if not starter.is_empty():
		GameState.ship_durability = int(starter.get("durability", 30))
		GameState.ship_max_durability = GameState.ship_durability
		GameState.ship_capacity = int(starter.get("capacity_tons", 50))
		GameState.ship_max_guns = int(starter.get("maximum_guns", 10))
	# Try to auto-load save
	if GameState.has_save() and GameState.load_game():
		current_port_id = GameState.current_port_id
		var loaded_port := GameState.get_port(current_port_id)
		if not loaded_port.is_empty():
			ship.global_position = Vector2(loaded_port.world_x, loaded_port.world_y)
			info_label.text = "读取存档。停靠在 %s。" % _pn(loaded_port)
			ship.refresh_from_game_state()
			_open_port_screen(loaded_port)
		return
	# Otherwise fresh start
	current_port_id = 0
	GameState.ship_changed.emit()
	var start_port := GameState.get_port(0)
	if not start_port.is_empty():
		ship.global_position = Vector2(start_port.world_x, start_port.world_y)
		info_label.text = "停靠在 %s。点击港口起航。" % _pn(start_port)
		_open_port_screen(start_port)


func _on_save_pressed() -> void:
	if ship != null and ship.moving:
		info_label.text = "航行中无法存档"
		return
	if GameState.save_game():
		info_label.text = "游戏已保存。"


func _on_load_pressed() -> void:
	if not GameState.has_save():
		info_label.text = "没有存档。"
		return
	if GameState.load_game():
		current_port_id = GameState.current_port_id
		var p := GameState.get_port(current_port_id)
		if not p.is_empty():
			ship.global_position = Vector2(p.world_x, p.world_y)
			ship.refresh_from_game_state()
			ship.moving = false
			_open_port_screen(p)
			info_label.text = "存档已读取。"


func _on_new_pressed() -> void:
	GameState.delete_save()
	get_tree().reload_current_scene()


func _spawn_ports() -> void:
	for port in GameState.ports_data.get("ports", []):
		var marker := preload("res://scenes/port_marker.tscn").instantiate()
		marker.position = Vector2(port.world_x, port.world_y)
		marker.set_port_data(port)
		marker.clicked.connect(_on_port_clicked)
		port_layer.add_child(marker)


func _spawn_ship() -> void:
	ship = preload("res://scenes/ship.tscn").instantiate()
	ship.wind_overlay = wind_overlay
	ship_layer.add_child(ship)
	ship.arrived_at_port.connect(_on_ship_arrived)


func _process(delta: float) -> void:
	if ship == null or not ship.moving:
		return
	if event_dialog.visible:
		return
	time_since_event += delta
	if time_since_event < MIN_TIME_BETWEEN_EVENTS:
		return
	if randf() < EVENT_CHANCE_PER_SEC * delta * 60.0:
		_trigger_random_event()


func _trigger_random_event() -> void:
	var event := GameState.pick_random_event()
	if event.is_empty():
		return
	time_since_event = 0.0
	event_dialog.show_event(event)
	info_label.text = "事件: %s" % event.get("title", "...")


func _on_event_option_chosen(opt: Dictionary) -> void:
	GameState.apply_event_outcome(opt)
	if opt.has("info"):
		info_label.text = opt.info
	# If option label mentions "Fight" — launch combat
	if str(opt.get("label", "")).to_lower().contains("fight"):
		combat_panel.start_combat("海盗", 1)


func _on_combat_ended(outcome: String, rewards: Dictionary) -> void:
	if outcome == "victory":
		GameState.gold += int(rewards.get("gold", 0))
		GameState.gold_changed.emit(GameState.gold)
		if rewards.has("damage"):
			GameState.ship_durability = max(0, GameState.ship_durability - int(rewards.damage))
			GameState.ship_changed.emit()
		info_label.text = "胜利! +%d 金币" % rewards.get("gold", 0)
	elif outcome == "defeat":
		GameState.gold = max(0, GameState.gold - int(rewards.get("gold_loss", 0)))
		GameState.gold_changed.emit(GameState.gold)
		GameState.ship_durability = max(1, GameState.ship_durability / 2)
		GameState.ship_changed.emit()
		info_label.text = "战败! -%d 金币,船体受损" % rewards.get("gold_loss", 0)
	else:
		info_label.text = "你逃离了战斗。"


func _on_port_clicked(port: Dictionary) -> void:
	if ship == null or ship.moving:
		info_label.text = "航行中,请等待抵达"
		return
	if port.id == current_port_id:
		_open_port_screen(port)
	else:
		var dist := ship.global_position.distance_to(Vector2(port.world_x, port.world_y))
		pending_sail_days = max(1, int(dist / 25.0))
		info_label.text = "起航前往 %s (约 %d 天)..." % [_pn(port), pending_sail_days]
		ship.sail_to(Vector2(port.world_x, port.world_y), port.id)
		port_screen_panel.visible = false
		AudioManager.play("sea")


func _on_ship_arrived(port_id: int) -> void:
	current_port_id = port_id
	if pending_sail_days > 0:
		GameState.advance_days(pending_sail_days)
		pending_sail_days = 0
	var port := GameState.get_port(port_id)
	info_label.text = "抵达 %s。" % _pn(port)
	AudioManager.play("port")
	if not port.is_empty():
		_open_port_screen(port)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_M:
		var muted: bool = AudioManager.toggle_mute()
		info_label.text = "音乐：" + ("静音" if muted else "开")


func _open_port_screen(port: Dictionary) -> void:
	GameState.current_port_id = port.id
	port_screen_title.text = "%s · %s" % [_pn(port), port.get("region","")]
	var port_img_path := "res://assets/ports/" + str(port.get("port_screen", ""))
	if ResourceLoader.exists(port_img_path):
		port_screen_image.texture = load(port_img_path)
	var gov_id: int = port.get("governor_portrait", 0)
	var gov_path := "res://assets/portraits/%03d.png" % gov_id
	if ResourceLoader.exists(gov_path):
		governor_portrait.texture = load(gov_path)
	governor_label.text = "%s 总督" % _pn(port)
	_populate_trade_list(port)
	_populate_shipyard(port)
	_populate_tavern(port)
	port_screen_panel.visible = true


func _populate_shipyard(port: Dictionary) -> void:
	for child in shipyard_list.get_children():
		child.queue_free()
	var offered: Array = port.get("shipyard", [])
	if offered.is_empty():
		var lbl := Label.new()
		lbl.text = "此处没有船坞。"
		shipyard_list.add_child(lbl)
		return
	# Header
	var header := Label.new()
	header.text = "当前船: %d 号 (船体 %d/%d, 容量 %d, 火炮 %d)" % [
		GameState.ship_type_id, GameState.ship_durability,
		GameState.ship_max_durability, GameState.ship_capacity, GameState.ship_max_guns]
	header.add_theme_font_size_override("font_size", 13)
	shipyard_list.add_child(header)
	for ship_id in offered:
		var ship := GameState.get_ship(int(ship_id))
		if ship.is_empty():
			continue
		var row := HBoxContainer.new()
		row.custom_minimum_size = Vector2(0, 56)
		# Ship sprite
		var sprite_idx: int = ((int(ship_id) - 1) % 16) * 2
		var icon_rect := TextureRect.new()
		icon_rect.custom_minimum_size = Vector2(48, 48)
		icon_rect.expand_mode = TextureRect.EXPAND_FIT_WIDTH_PROPORTIONAL
		icon_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		var path := "res://assets/ships/ship_%02d.png" % sprite_idx
		if ResourceLoader.exists(path):
			icon_rect.texture = load(path)
		row.add_child(icon_rect)
		# Stats column
		var stats := VBoxContainer.new()
		stats.custom_minimum_size = Vector2(260, 0)
		var name_lbl := Label.new()
		name_lbl.text = "%d 号船 (帆型 %d)" % [ship_id, int(ship.get("sail_type", 0))]
		name_lbl.add_theme_font_size_override("font_size", 14)
		stats.add_child(name_lbl)
		var detail_lbl := Label.new()
		detail_lbl.text = "容量 %d · 火炮 %d · 耐久 %d · 速度 %d" % [
			int(ship.get("capacity_tons", 0)), int(ship.get("maximum_guns", 0)),
			int(ship.get("durability", 0)), int(ship.get("power", 0))]
		detail_lbl.add_theme_font_size_override("font_size", 12)
		stats.add_child(detail_lbl)
		row.add_child(stats)
		# Price
		var trade_in: int = 0
		var cur := GameState.get_ship(GameState.ship_type_id)
		if not cur.is_empty():
			trade_in = int(cur.get("base_price", 0) * 0.3)
		var net: int = max(0, int(ship.get("base_price", 0)) - trade_in)
		var price_lbl := Label.new()
		price_lbl.text = "%dg" % net
		price_lbl.custom_minimum_size = Vector2(80, 0)
		price_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(price_lbl)
		# Buy button
		var buy_btn := Button.new()
		buy_btn.text = "买"
		buy_btn.pressed.connect(_on_buy_ship.bind(int(ship_id)))
		row.add_child(buy_btn)
		shipyard_list.add_child(row)


func _on_buy_ship(ship_id: int) -> void:
	if GameState.buy_ship(ship_id):
		# Refresh ship sprite + repopulate
		if ship != null and ship.has_method("refresh_from_game_state"):
			ship.refresh_from_game_state()
		info_label.text = "已购入 %d 号船。" % ship_id
		var port := GameState.get_port(current_port_id)
		if not port.is_empty():
			_populate_shipyard(port)
	else:
		info_label.text = "金币不足以购买此船。"


func _populate_trade_list(port: Dictionary) -> void:
	for child in trade_list.get_children():
		child.queue_free()
	var icons_map: Dictionary = GameState.ports_data.get("goods_icons", {})
	for good_name in port.goods.keys():
		# Seasonal price: base × month factor
		var price: int = int(port.goods[good_name] * GameState.season_price_factor(good_name))
		var row := HBoxContainer.new()
		row.custom_minimum_size = Vector2(0, 40)
		var icon_rect := TextureRect.new()
		icon_rect.custom_minimum_size = Vector2(36, 36)
		icon_rect.expand_mode = TextureRect.EXPAND_FIT_WIDTH_PROPORTIONAL
		icon_rect.stretch_mode = TextureRect.STRETCH_SCALE
		var icon_idx: int = icons_map.get(good_name, 0)
		var icon_path := "res://assets/items/%03d.png" % icon_idx
		if ResourceLoader.exists(icon_path):
			icon_rect.texture = load(icon_path)
		row.add_child(icon_rect)
		var name_lbl := Label.new()
		name_lbl.text = good_name
		name_lbl.custom_minimum_size = Vector2(90, 0)
		name_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(name_lbl)
		var price_lbl := Label.new()
		price_lbl.text = "%dg" % price
		price_lbl.custom_minimum_size = Vector2(60, 0)
		price_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(price_lbl)
		var inv_qty: int = GameState.inventory.get(good_name, 0)
		var inv_lbl := Label.new()
		inv_lbl.text = "x%d" % inv_qty
		inv_lbl.custom_minimum_size = Vector2(40, 0)
		inv_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(inv_lbl)
		for qty in [1, 10]:
			var b := Button.new()
			b.text = "买" if qty == 1 else "买%d" % qty
			b.custom_minimum_size = Vector2(38, 0)
			b.pressed.connect(_on_buy.bind(good_name, price, qty))
			row.add_child(b)
		for qty in [1, 10]:
			var s := Button.new()
			s.text = "卖" if qty == 1 else "卖%d" % qty
			s.custom_minimum_size = Vector2(38, 0)
			s.pressed.connect(_on_sell.bind(good_name, price, qty))
			row.add_child(s)
		trade_list.add_child(row)


const TAVERN_GREETINGS := [
	"风浪可不饶人，喝一杯再走吧。",
	"听说最近海上不太平，当心海盗。",
	"远方来的客人？这儿的酒可烈着呢。",
	"想发财就去东边的香料群岛闯闯。",
	"老水手都说，南风起时是出航的好日子。",
]


func _populate_tavern(port: Dictionary) -> void:
	for child in tavern_list.get_children():
		child.queue_free()
	# Barkeep — a Kao portrait keyed to the port so it's stable per visit.
	var pid: int = int(port.get("id", 0))
	var npc_id: int = pid % 128
	var row := HBoxContainer.new()
	row.custom_minimum_size = Vector2(0, 72)
	var portrait := TextureRect.new()
	portrait.custom_minimum_size = Vector2(80, 64)
	portrait.expand_mode = TextureRect.EXPAND_FIT_WIDTH_PROPORTIONAL
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	var p_path := "res://assets/portraits/%03d.png" % npc_id
	if ResourceLoader.exists(p_path):
		portrait.texture = load(p_path)
	row.add_child(portrait)
	var greet := Label.new()
	greet.text = "酒保：" + TAVERN_GREETINGS[pid % TAVERN_GREETINGS.size()]
	greet.custom_minimum_size = Vector2(300, 0)
	greet.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	greet.add_theme_font_size_override("font_size", 13)
	row.add_child(greet)
	tavern_list.add_child(row)
	# Intel button
	var intel_btn := Button.new()
	intel_btn.text = "打听商情（消耗 1 天）"
	intel_btn.pressed.connect(_on_tavern_intel.bind(port))
	tavern_list.add_child(intel_btn)
	var intel_lbl := Label.new()
	intel_lbl.name = "IntelLabel"
	intel_lbl.text = "——"
	intel_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	intel_lbl.custom_minimum_size = Vector2(440, 0)
	intel_lbl.add_theme_font_size_override("font_size", 13)
	tavern_list.add_child(intel_lbl)


func _on_tavern_intel(port: Dictionary) -> void:
	# Pick a random good sold here, find where it fetches the best price.
	var goods: Array = port.get("goods", {}).keys()
	if goods.is_empty():
		return
	var good: String = goods[randi() % goods.size()]
	var best_port: Dictionary = {}
	var best_price: int = 0
	for p in GameState.ports_data.get("ports", []):
		var g: Dictionary = p.get("goods", {})
		if not g.has(good):
			continue
		var price: int = int(g[good])
		if price > best_price:
			best_price = price
			best_port = p
	GameState.advance_days(1)
	var intel_lbl: Label = tavern_list.get_node_or_null("IntelLabel")
	if intel_lbl == null:
		return
	if best_port.is_empty():
		intel_lbl.text = "酒保摇摇头，没打听到什么。"
	else:
		intel_lbl.text = "酒保压低声音：听说 %s 那边，%s 能卖到 %d 金币。" % [
			_pn(best_port), good, best_price]


func _on_buy(good: String, price: int, qty: int = 1) -> void:
	var bought := 0
	while bought < qty and GameState.buy(good, 1, price):
		bought += 1
	if bought > 0:
		info_label.text = "买入 %s ×%d" % [good, bought]
		_populate_trade_list(GameState.get_port(current_port_id))
	else:
		info_label.text = "金币不足"


func _on_sell(good: String, price: int, qty: int = 1) -> void:
	var sold := 0
	while sold < qty and GameState.sell(good, 1, price):
		sold += 1
	if sold > 0:
		info_label.text = "卖出 %s ×%d" % [good, sold]
		_populate_trade_list(GameState.get_port(current_port_id))
	else:
		info_label.text = "没有货物可卖"


func _on_gold_changed(new_gold: int) -> void:
	gold_label.text = "金币: %d" % new_gold


func _on_date_changed() -> void:
	date_label.text = GameState.date_string()


func _on_ship_changed() -> void:
	dura_label.text = "船体: %d/%d" % [GameState.ship_durability, GameState.ship_max_durability]


func _on_close_pressed() -> void:
	port_screen_panel.visible = false
	var port := GameState.get_port(current_port_id)
	if not port.is_empty():
		info_label.text = "停靠在 %s。点击港口起航。" % _pn(port)
