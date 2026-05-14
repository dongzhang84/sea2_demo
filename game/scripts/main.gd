extends Node2D
## Main scene: world map + port markers + UI + ship + port screen.

@onready var port_layer: Node2D = $PortLayer
@onready var ship_layer: Node2D = $ShipLayer
@onready var wind_overlay: Node2D = $WindOverlay
@onready var gold_label: Label = $UI/GoldLabel
@onready var info_label: Label = $UI/InfoLabel
@onready var port_screen_panel: PanelContainer = $UI/PortScreenPanel
@onready var port_screen_title: Label = $UI/PortScreenPanel/V/Title
@onready var port_screen_image: TextureRect = $UI/PortScreenPanel/V/Image
@onready var governor_portrait: TextureRect = $UI/PortScreenPanel/V/GovernorRow/Portrait
@onready var governor_label: Label = $UI/PortScreenPanel/V/GovernorRow/Label
@onready var trade_list: VBoxContainer = $UI/PortScreenPanel/V/Scroll/List

var ship: Node2D = null
var current_port_id: int = -1


func _ready() -> void:
	GameState.gold_changed.connect(_on_gold_changed)
	_on_gold_changed(GameState.gold)
	_spawn_ports()
	_spawn_ship()
	current_port_id = 0
	var start_port := GameState.get_port(0)
	if not start_port.is_empty():
		ship.global_position = Vector2(start_port.world_x, start_port.world_y)
		info_label.text = "Docked at %s. Click any port to sail." % start_port.name
		# Auto-open port screen at start so player sees the trade UI immediately
		_open_port_screen(start_port)


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


func _on_port_clicked(port: Dictionary) -> void:
	if ship == null or ship.moving:
		info_label.text = "Sailing — wait until arrival"
		return
	if port.id == current_port_id:
		_open_port_screen(port)
	else:
		info_label.text = "Setting sail to %s..." % port.name
		ship.sail_to(Vector2(port.world_x, port.world_y), port.id)
		port_screen_panel.visible = false


func _on_ship_arrived(port_id: int) -> void:
	current_port_id = port_id
	var port := GameState.get_port(port_id)
	info_label.text = "Arrived at %s. Click again to enter." % port.name


func _open_port_screen(port: Dictionary) -> void:
	GameState.current_port_id = port.id
	port_screen_title.text = "%s — %s" % [port.name, port.region]
	# Load port screen image
	var port_img_path := "res://assets/ports/" + str(port.get("port_screen", ""))
	if ResourceLoader.exists(port_img_path):
		port_screen_image.texture = load(port_img_path)
	# Governor portrait
	var gov_id: int = port.get("governor_portrait", 0)
	var gov_path := "res://assets/portraits/%03d.png" % gov_id
	if ResourceLoader.exists(gov_path):
		governor_portrait.texture = load(gov_path)
	governor_label.text = "Governor of %s" % port.name
	_populate_trade_list(port)
	port_screen_panel.visible = true


func _populate_trade_list(port: Dictionary) -> void:
	for child in trade_list.get_children():
		child.queue_free()
	var icons_map: Dictionary = GameState.ports_data.get("goods_icons", {})
	for good_name in port.goods.keys():
		var price: int = port.goods[good_name]
		var row := HBoxContainer.new()
		row.custom_minimum_size = Vector2(0, 40)
		# Icon
		var icon_rect := TextureRect.new()
		icon_rect.custom_minimum_size = Vector2(36, 36)
		icon_rect.expand_mode = TextureRect.EXPAND_FIT_WIDTH_PROPORTIONAL
		icon_rect.stretch_mode = TextureRect.STRETCH_SCALE
		var icon_idx: int = icons_map.get(good_name, 0)
		var icon_path := "res://assets/items/%03d.png" % icon_idx
		if ResourceLoader.exists(icon_path):
			icon_rect.texture = load(icon_path)
		row.add_child(icon_rect)
		# Name
		var name_lbl := Label.new()
		name_lbl.text = good_name
		name_lbl.custom_minimum_size = Vector2(90, 0)
		name_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(name_lbl)
		# Price
		var price_lbl := Label.new()
		price_lbl.text = "%dg" % price
		price_lbl.custom_minimum_size = Vector2(60, 0)
		price_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(price_lbl)
		# Inventory count
		var inv_qty: int = GameState.inventory.get(good_name, 0)
		var inv_lbl := Label.new()
		inv_lbl.text = "x%d" % inv_qty
		inv_lbl.custom_minimum_size = Vector2(40, 0)
		inv_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(inv_lbl)
		# Buttons
		var buy_btn := Button.new()
		buy_btn.text = "Buy"
		buy_btn.pressed.connect(_on_buy.bind(good_name, price))
		row.add_child(buy_btn)
		var sell_btn := Button.new()
		sell_btn.text = "Sell"
		sell_btn.pressed.connect(_on_sell.bind(good_name, price))
		row.add_child(sell_btn)
		trade_list.add_child(row)


func _on_buy(good: String, price: int) -> void:
	if GameState.buy(good, 1, price):
		var port := GameState.get_port(current_port_id)
		_populate_trade_list(port)
	else:
		info_label.text = "Not enough gold"


func _on_sell(good: String, price: int) -> void:
	if GameState.sell(good, 1, price):
		var port := GameState.get_port(current_port_id)
		_populate_trade_list(port)
	else:
		info_label.text = "Nothing to sell"


func _on_gold_changed(new_gold: int) -> void:
	gold_label.text = "Gold: %d" % new_gold


func _on_close_pressed() -> void:
	port_screen_panel.visible = false
	var port := GameState.get_port(current_port_id)
	if not port.is_empty():
		info_label.text = "Docked at %s. Click any port to sail." % port.name
