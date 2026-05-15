extends Node
## Global game state singleton (Autoload).

var gold: int = 1000
var inventory: Dictionary = {}
var current_port_id: int = -1
var ports_data: Dictionary = {}
var ships_data: Dictionary = {}
var events_data: Dictionary = {}

# Ship state
var ship_sprite_id: int = 0       # which sprite from assets/ships/ (0-31)
var ship_type_id: int = 1          # which ship type from ships.json (1-25)
var ship_durability: int = 100     # 0-100 hull condition
var ship_max_durability: int = 100
var ship_capacity: int = 50        # cargo capacity in tons
var ship_max_guns: int = 10

# Calendar — game starts 1 Jan 1502
var year: int = 1502
var month: int = 1                 # 1-12
var day: int = 1                   # 1-30 (simplified 30-day months)

signal gold_changed(new_gold: int)
signal inventory_changed()
signal date_changed()
signal ship_changed()
signal loaded()

const SAVE_PATH := "user://save.json"


func _ready() -> void:
	_load_json('res://data/ports.json', 'ports_data')
	_load_json('res://data/ships.json', 'ships_data')
	_load_json('res://data/events.json', 'events_data')
	if ports_data.has('starting_gold'):
		gold = ports_data.starting_gold
	print("Loaded: %d ports, %d ships, %d event templates, gold=%d" % [
		ports_data.get('ports', []).size(),
		ships_data.get('ships', []).size(),
		events_data.get('events', []).size(),
		gold,
	])


func _load_json(path: String, var_name: String) -> void:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Cannot open " + path)
		return
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if parsed != null:
		set(var_name, parsed)


func buy(good: String, qty: int, price: int) -> bool:
	var total: int = price * qty
	if gold < total:
		return false
	gold -= total
	inventory[good] = inventory.get(good, 0) + qty
	gold_changed.emit(gold)
	inventory_changed.emit()
	return true


func sell(good: String, qty: int, price: int) -> bool:
	if inventory.get(good, 0) < qty:
		return false
	gold += price * qty
	inventory[good] -= qty
	if inventory[good] == 0:
		inventory.erase(good)
	gold_changed.emit(gold)
	inventory_changed.emit()
	return true


func apply_event_outcome(opt: Dictionary) -> void:
	if opt.has("cost_gold"):
		gold = max(0, gold - int(opt.cost_gold))
		gold_changed.emit(gold)
	if opt.has("gain_gold"):
		gold += int(opt.gain_gold)
		gold_changed.emit(gold)
	if opt.has("damage"):
		ship_durability = max(0, ship_durability - int(opt.damage))
		ship_changed.emit()
	if opt.has("gain_item"):
		var item: String = opt.gain_item
		inventory[item] = inventory.get(item, 0) + 1
		inventory_changed.emit()


func advance_days(n: int) -> void:
	"""Advance the calendar by n days. 30-day months."""
	day += n
	while day > 30:
		day -= 30
		month += 1
		if month > 12:
			month = 1
			year += 1
	date_changed.emit()


func date_string() -> String:
	return "%d年%d月%d日" % [year, month, day]


func season_price_factor(good: String) -> float:
	"""Seasonal price modulation. Some goods cheaper/dearer by month.
	Returns a multiplier ~0.85-1.15."""
	# Simple sinusoid keyed to month, phase-shifted per good name hash.
	var phase: float = float(good.hash() % 12)
	var t: float = (float(month) + phase) / 12.0 * TAU
	return 1.0 + sin(t) * 0.15


func get_port(id: int) -> Dictionary:
	for p in ports_data.get("ports", []):
		if p.get("id") == id:
			return p
	return {}


func get_ship(id: int) -> Dictionary:
	for s in ships_data.get("ships", []):
		if s.get("id") == id:
			return s
	return {}


func buy_ship(ship_id: int) -> bool:
	"""Buy a new ship, swapping the current one. Trade-in worth 30% of new price."""
	var ship := get_ship(ship_id)
	if ship.is_empty():
		return false
	var price: int = int(ship.get("base_price", 0))
	if price == 0:
		return false
	# Trade-in value of current ship (30% of its price)
	var current := get_ship(ship_type_id)
	var trade_in: int = int(current.get("base_price", 0) * 0.3) if not current.is_empty() else 0
	var net_cost: int = max(0, price - trade_in)
	if gold < net_cost:
		return false
	gold -= net_cost
	ship_type_id = ship_id
	ship_durability = int(ship.get("durability", 100))
	ship_max_durability = ship_durability
	ship_capacity = int(ship.get("capacity_tons", 50))
	ship_max_guns = int(ship.get("maximum_guns", 10))
	# Sprite mapping: 25 ships → 16 sprite pairs (each pair = 2 frames)
	ship_sprite_id = ((ship_id - 1) % 16) * 2
	gold_changed.emit(gold)
	ship_changed.emit()
	return true


func save_game() -> bool:
	var data := {
		"gold": gold,
		"inventory": inventory,
		"current_port_id": current_port_id,
		"ship_sprite_id": ship_sprite_id,
		"ship_type_id": ship_type_id,
		"ship_durability": ship_durability,
		"ship_max_durability": ship_max_durability,
		"ship_capacity": ship_capacity,
		"ship_max_guns": ship_max_guns,
		"year": year, "month": month, "day": day,
		"timestamp": Time.get_datetime_string_from_system(),
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		push_error("Cannot open save file for writing")
		return false
	file.store_string(JSON.stringify(data, "  "))
	file.close()
	print("Saved game to ", SAVE_PATH)
	return true


func load_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return false
	var text := file.get_as_text()
	file.close()
	var parsed: Variant = JSON.parse_string(text)
	if parsed == null or typeof(parsed) != TYPE_DICTIONARY:
		return false
	gold = int(parsed.get("gold", 1000))
	inventory = parsed.get("inventory", {}).duplicate()
	current_port_id = int(parsed.get("current_port_id", 0))
	ship_sprite_id = int(parsed.get("ship_sprite_id", 0))
	ship_type_id = int(parsed.get("ship_type_id", 1))
	ship_durability = int(parsed.get("ship_durability", 30))
	ship_max_durability = int(parsed.get("ship_max_durability", 30))
	ship_capacity = int(parsed.get("ship_capacity", 50))
	ship_max_guns = int(parsed.get("ship_max_guns", 10))
	year = int(parsed.get("year", 1502))
	month = int(parsed.get("month", 1))
	day = int(parsed.get("day", 1))
	gold_changed.emit(gold)
	inventory_changed.emit()
	ship_changed.emit()
	date_changed.emit()
	loaded.emit()
	print("Loaded save from ", SAVE_PATH)
	return true


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)


func delete_save() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(SAVE_PATH))


func pick_random_event() -> Dictionary:
	var events: Array = events_data.get("events", [])
	if events.is_empty():
		return {}
	var total_weight: int = 0
	for e in events:
		total_weight += int(e.get("weight", 1))
	var roll: int = randi() % total_weight
	var cum: int = 0
	for e in events:
		cum += int(e.get("weight", 1))
		if roll < cum:
			return e
	return events[0]
