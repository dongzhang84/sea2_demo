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

signal gold_changed(new_gold: int)
signal inventory_changed()
signal ship_changed()


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
