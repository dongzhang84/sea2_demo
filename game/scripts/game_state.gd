extends Node
## Global game state singleton (Autoload).

var gold: int = 1000
var inventory: Dictionary = {}
var current_port_id: int = -1
var ports_data: Dictionary = {}
var ships_data: Dictionary = {}
var events_data: Dictionary = {}
var story_quests_data: Dictionary = {}

# Ship state
var ship_sprite_id: int = 0       # which sprite from assets/ships/ (0-31)
var ship_type_id: int = 1          # which ship type from ships.json (1-25)
var ship_durability: int = 100     # 0-100 hull condition
var ship_max_durability: int = 100
var ship_capacity: int = 50        # cargo capacity in tons
var ship_max_guns: int = 10
var ship_capacity_bonus: int = 0
var ship_max_durability_bonus: int = 0

# Story quest state
var story_quest_state: Dictionary = {
	"active_id": "",
	"stage": 0,
	"completed": [],
	"flags": {},
}

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
	_load_json('res://data/story_quests.json', 'story_quests_data')
	if ports_data.has('starting_gold'):
		gold = ports_data.starting_gold
	_sync_ship_stats(true)
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


func reset_game() -> void:
	gold = int(ports_data.get("starting_gold", 1000))
	inventory = {}
	current_port_id = -1
	ship_sprite_id = 0
	ship_type_id = 1
	ship_capacity_bonus = 0
	ship_max_durability_bonus = 0
	story_quest_state = {
		"active_id": "",
		"stage": 0,
		"completed": [],
		"flags": {},
	}
	year = 1502
	month = 1
	day = 1
	_sync_ship_stats(true)
	gold_changed.emit(gold)
	inventory_changed.emit()
	ship_changed.emit()
	date_changed.emit()


func _sync_ship_stats(repair_to_max: bool = false) -> void:
	var ship := get_ship(ship_type_id)
	if ship.is_empty():
		return
	var base_dura := int(ship.get("durability", 100))
	var base_capacity := int(ship.get("capacity_tons", 50))
	ship_max_durability = base_dura + ship_max_durability_bonus
	ship_capacity = base_capacity + ship_capacity_bonus
	ship_max_guns = int(ship.get("maximum_guns", 10))
	if repair_to_max or ship_durability <= 0:
		ship_durability = ship_max_durability
	else:
		ship_durability = min(ship_durability, ship_max_durability)


func _quest_list() -> Array:
	return story_quests_data.get("quests", [])


func _completed_story_quests() -> Array:
	return story_quest_state.get("completed", [])


func _is_flag_set(flag_name: String) -> bool:
	var flags: Dictionary = story_quest_state.get("flags", {})
	return bool(flags.get(flag_name, false))


func _set_flag(flag_name: String, value: bool = true) -> void:
	var flags: Dictionary = story_quest_state.get("flags", {})
	flags[flag_name] = value
	story_quest_state["flags"] = flags


func _port_name(port_id: int) -> String:
	var port := get_port(port_id)
	if port.is_empty():
		return "未知港口"
	return str(port.get("cn_name", port.get("name", "未知港口")))


func get_story_quest(quest_id: String) -> Dictionary:
	for q in _quest_list():
		if str(q.get("id", "")) == quest_id:
			return q
	return {}


func get_active_story_quest() -> Dictionary:
	var active_id := str(story_quest_state.get("active_id", ""))
	if active_id == "":
		return {}
	return get_story_quest(active_id)


func quest_completed(quest_id: String) -> bool:
	return _completed_story_quests().has(quest_id)


func quest_available(quest: Dictionary, port_id: int) -> bool:
	if quest.is_empty():
		return false
	var quest_id := str(quest.get("id", ""))
	if quest_id == "" or quest_completed(quest_id):
		return false
	if str(story_quest_state.get("active_id", "")) != "":
		return false
	if int(quest.get("origin_port_id", -1)) != port_id:
		return false
	for flag_name in quest.get("required_flags", []):
		if not _is_flag_set(str(flag_name)):
			return false
	return true


func get_available_story_quests(port_id: int) -> Array:
	var result: Array = []
	for quest in _quest_list():
		if quest_available(quest, port_id):
			result.append(quest)
	return result


func start_story_quest(quest_id: String) -> bool:
	if str(story_quest_state.get("active_id", "")) != "":
		return false
	var quest := get_story_quest(quest_id)
	if quest.is_empty():
		return false
	story_quest_state["active_id"] = quest_id
	story_quest_state["stage"] = 1
	return true


func quest_progress_text() -> String:
	var quest := get_active_story_quest()
	if quest.is_empty():
		return "暂无进行中的主线委托。"
	var stage := int(story_quest_state.get("stage", 0))
	var waypoints: Array = quest.get("waypoints", [])
	var return_port_id: int = int(quest.get("return_port_id", -1))
	if stage <= 0:
		return "任务状态异常。"
	if stage <= waypoints.size():
		var target_port_id := int(waypoints[stage - 1])
		return "进行中：%s -> 第 %d / %d 站 [%s]" % [
			str(quest.get("title", quest.get("id", ""))),
			stage, waypoints.size(), _port_name(target_port_id)]
	return "进行中：%s -> 返回 [%s]" % [
		str(quest.get("title", quest.get("id", ""))),
		_port_name(return_port_id)]


func quest_offer_text(quest: Dictionary) -> String:
	if quest.is_empty():
		return ""
	return "%s：%s" % [str(quest.get("title", "任务")), str(quest.get("summary", ""))]


func progress_story_quests_on_port_arrival(port_id: int) -> Array:
	var notes: Array = []
	var quest := get_active_story_quest()
	if quest.is_empty():
		return notes
	var stage := int(story_quest_state.get("stage", 0))
	var waypoints: Array = quest.get("waypoints", [])
	var return_port_id: int = int(quest.get("return_port_id", -1))
	if stage >= 1 and stage <= waypoints.size():
		var target_port_id := int(waypoints[stage - 1])
		if port_id == target_port_id:
			story_quest_state["stage"] = stage + 1
			stage += 1
			var waypoint_texts: Dictionary = quest.get("waypoint_texts", {})
			var text := str(waypoint_texts.get(str(target_port_id), ""))
			if text == "":
				text = "%s 的这一站已完成。" % _port_name(target_port_id)
			notes.append(text)
	if stage == waypoints.size() + 1 and port_id == return_port_id:
		var reward_gold := int(quest.get("reward_gold", 0))
		var reward_capacity_bonus := int(quest.get("reward_capacity_bonus", 0))
		var reward_durability_bonus := int(quest.get("reward_durability_bonus", 0))
		gold += reward_gold
		if reward_gold != 0:
			gold_changed.emit(gold)
		if reward_capacity_bonus != 0:
			ship_capacity_bonus += reward_capacity_bonus
		if reward_durability_bonus != 0:
			ship_max_durability_bonus += reward_durability_bonus
		if reward_capacity_bonus != 0 or reward_durability_bonus != 0:
			_sync_ship_stats(true)
			ship_changed.emit()
		for flag_name in quest.get("reward_flags", []):
			_set_flag(str(flag_name))
		var completed: Array = _completed_story_quests()
		completed.append(str(quest.get("id", "")))
		story_quest_state["completed"] = completed
		story_quest_state["active_id"] = ""
		story_quest_state["stage"] = 0
		notes.append(str(quest.get("complete_text", "任务完成。")))
	return notes


func reward_ship_bonus(capacity_bonus: int = 0, durability_bonus: int = 0) -> void:
	ship_capacity_bonus += capacity_bonus
	ship_max_durability_bonus += durability_bonus
	_sync_ship_stats(true)
	ship_changed.emit()


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
	_sync_ship_stats(true)
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
		"ship_capacity_bonus": ship_capacity_bonus,
		"ship_max_durability_bonus": ship_max_durability_bonus,
		"story_quest_state": story_quest_state,
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
	ship_capacity_bonus = int(parsed.get("ship_capacity_bonus", 0))
	ship_max_durability_bonus = int(parsed.get("ship_max_durability_bonus", 0))
	var loaded_story_state: Variant = parsed.get("story_quest_state", story_quest_state)
	if typeof(loaded_story_state) == TYPE_DICTIONARY:
		story_quest_state = loaded_story_state
	year = int(parsed.get("year", 1502))
	month = int(parsed.get("month", 1))
	day = int(parsed.get("day", 1))
	_sync_ship_stats(false)
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
