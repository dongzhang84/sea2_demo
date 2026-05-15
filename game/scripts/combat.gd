extends PanelContainer
## Simple turn-based naval combat: player ship vs enemy ship.

signal combat_ended(outcome: String, rewards: Dictionary)

@onready var player_sprite: TextureRect = $V/Battle/PlayerCol/Sprite
@onready var player_hp: ProgressBar = $V/Battle/PlayerCol/HP
@onready var player_hp_label: Label = $V/Battle/PlayerCol/HPLabel
@onready var enemy_sprite: TextureRect = $V/Battle/EnemyCol/Sprite
@onready var enemy_hp: ProgressBar = $V/Battle/EnemyCol/HP
@onready var enemy_hp_label: Label = $V/Battle/EnemyCol/HPLabel
@onready var log_label: RichTextLabel = $V/Log
@onready var actions_box: HBoxContainer = $V/Actions
@onready var title_label: Label = $V/Title

var player_max_hp: int = 100
var player_cur_hp: int = 100
var enemy_max_hp: int = 60
var enemy_cur_hp: int = 60
var enemy_name: String = "Pirate"
var rng := RandomNumberGenerator.new()


func _ready() -> void:
	rng.randomize()


func start_combat(opponent_name: String, opponent_strength: int = 1) -> void:
	enemy_name = opponent_name
	title_label.text = "Naval Combat — vs %s" % opponent_name
	player_max_hp = max(50, GameState.ship_durability)
	player_cur_hp = player_max_hp
	enemy_max_hp = 40 + opponent_strength * 20
	enemy_cur_hp = enemy_max_hp
	# Load player ship sprite + enemy pirate sprite (different ship)
	player_sprite.texture = load("res://assets/ships/ship_00.png")
	enemy_sprite.texture = load("res://assets/ships/ship_10.png")  # different style
	log_label.text = "[color=cyan]A %s ship engages you in battle![/color]" % opponent_name
	_setup_actions()
	_refresh_hp()
	visible = true


func _setup_actions() -> void:
	for child in actions_box.get_children():
		child.queue_free()
	for action in [
		{"name": "Cannon Volley", "kind": "attack", "tag": "cannon"},
		{"name": "Aimed Shot", "kind": "attack", "tag": "aimed"},
		{"name": "Try to Flee", "kind": "flee", "tag": "flee"},
	]:
		var btn := Button.new()
		btn.text = action.name
		btn.custom_minimum_size = Vector2(140, 40)
		btn.pressed.connect(_on_action.bind(action))
		actions_box.add_child(btn)


func _on_action(action: Dictionary) -> void:
	if action.kind == "attack":
		_resolve_attack(action.tag)
	elif action.kind == "flee":
		_try_flee()


func _resolve_attack(tag: String) -> void:
	# Player attack
	var p_dmg: int
	if tag == "cannon":
		p_dmg = rng.randi_range(8, 18)
	else:  # aimed
		p_dmg = rng.randi_range(4, 25)
	enemy_cur_hp = max(0, enemy_cur_hp - p_dmg)
	var log_text := "[color=yellow]Your %s hits for %d damage.[/color]" % [tag, p_dmg]
	# Enemy counter-attack
	if enemy_cur_hp > 0:
		var e_dmg: int = rng.randi_range(6, 14)
		player_cur_hp = max(0, player_cur_hp - e_dmg)
		log_text += "\n[color=red]%s returns fire for %d damage.[/color]" % [enemy_name, e_dmg]
	log_label.append_text("\n" + log_text)
	_refresh_hp()
	# Check end
	if enemy_cur_hp <= 0:
		_victory()
	elif player_cur_hp <= 0:
		_defeat()


func _try_flee() -> void:
	# 50% chance to flee
	if rng.randf() < 0.5:
		log_label.append_text("\n[color=cyan]You break off and escape![/color]")
		await get_tree().create_timer(1.5).timeout
		visible = false
		combat_ended.emit("flee", {})
	else:
		var e_dmg: int = rng.randi_range(10, 20)
		player_cur_hp = max(0, player_cur_hp - e_dmg)
		log_label.append_text("\n[color=red]The enemy catches up! You take %d damage.[/color]" % e_dmg)
		_refresh_hp()
		if player_cur_hp <= 0:
			_defeat()


func _victory() -> void:
	var gold_reward: int = rng.randi_range(80, 250)
	log_label.append_text("\n[color=lime]Victory! You loot %d gold from the wreck.[/color]" % gold_reward)
	await get_tree().create_timer(2.5).timeout
	visible = false
	combat_ended.emit("victory", {"gold": gold_reward, "damage": player_max_hp - player_cur_hp})


func _defeat() -> void:
	var gold_loss: int = min(GameState.gold, rng.randi_range(100, 300))
	log_label.append_text("\n[color=red]Your ship is overrun! You lose %d gold and barely escape.[/color]" % gold_loss)
	await get_tree().create_timer(2.5).timeout
	visible = false
	combat_ended.emit("defeat", {"gold_loss": gold_loss, "damage": player_max_hp})


func _refresh_hp() -> void:
	player_hp.max_value = player_max_hp
	player_hp.value = player_cur_hp
	player_hp_label.text = "%d / %d" % [player_cur_hp, player_max_hp]
	enemy_hp.max_value = enemy_max_hp
	enemy_hp.value = enemy_cur_hp
	enemy_hp_label.text = "%d / %d" % [enemy_cur_hp, enemy_max_hp]
