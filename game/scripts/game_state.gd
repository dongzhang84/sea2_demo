extends Node
## Global game state singleton.
## Loaded as Autoload in project.godot.

var gold: int = 1000
var inventory: Dictionary = {}  # good_name → quantity
var current_port_id: int = -1
var ports_data: Dictionary = {}

signal gold_changed(new_gold: int)
signal inventory_changed()


func _ready() -> void:
	_load_ports()


func _load_ports() -> void:
	var file := FileAccess.open("res://data/ports.json", FileAccess.READ)
	if file == null:
		push_error("Cannot open ports.json")
		return
	var json_text := file.get_as_text()
	file.close()
	var parsed: Variant = JSON.parse_string(json_text)
	if parsed == null:
		push_error("ports.json parse failed")
		return
	ports_data = parsed
	gold = parsed.get("starting_gold", 1000)
	print("Loaded %d ports, %d goods, starting gold %d" % [
		ports_data.ports.size(), ports_data.goods_catalog.size(), gold
	])


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


func get_port(id: int) -> Dictionary:
	for p in ports_data.get("ports", []):
		if p.get("id") == id:
			return p
	return {}
