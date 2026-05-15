extends Node2D
## Player's ship. Moves between ports with simple linear interpolation.
## Speed depends on distance (placeholder for wind/current mechanics).

signal arrived_at_port(port_id: int)

const BASE_SPEED_PX_PER_SEC := 80.0

var target_pos: Vector2 = Vector2.ZERO
var moving: bool = false
var target_port_id: int = -1
var wind_overlay: Node2D = null  # injected by main

@onready var sprite: Sprite2D = $Sprite
@onready var trail: Line2D = $Trail

# Animation between two frames
var anim_timer: float = 0.0
var anim_frame: int = 0
const ANIM_PERIOD := 0.4


func set_ship_sprite(sprite_idx: int) -> void:
	"""Load ship_NN.png as the current sprite."""
	var path := "res://assets/ships/ship_%02d.png" % sprite_idx
	if ResourceLoader.exists(path):
		sprite.texture = load(path)


func get_current_speed() -> float:
	"""Speed is modulated by wind alignment. Tailwind 1.5x, headwind 0.5x, no wind 1.0x."""
	if wind_overlay == null or not moving:
		return BASE_SPEED_PX_PER_SEC
	var sail_dir: Vector2 = (target_pos - global_position).normalized()
	var wind: Dictionary = wind_overlay.get_wind_at(global_position)
	var strength: float = wind.get("strength_0_1", 0.0)
	if strength <= 0.0:
		return BASE_SPEED_PX_PER_SEC
	var wind_dir := Vector2(cos(wind.direction_rad), sin(wind.direction_rad))
	# dot product: +1 = wind same direction as sail (tailwind), -1 = headwind
	var alignment: float = sail_dir.dot(wind_dir)
	# Speed multiplier: 0.5 (headwind) → 1.5 (tailwind), scaled by wind strength
	var mult: float = 1.0 + alignment * strength * 0.5
	return BASE_SPEED_PX_PER_SEC * mult


func _ready() -> void:
	# Draw a simple ship shape (triangle hull + mast)
	pass  # Sprite is defined in scene


func sail_to(pos: Vector2, port_id: int) -> void:
	target_pos = pos
	target_port_id = port_id
	moving = true
	trail.clear_points()
	trail.add_point(global_position)


func _process(delta: float) -> void:
	if not moving:
		return
	var direction := target_pos - global_position
	var dist := direction.length()
	if dist < 2.0:
		global_position = target_pos
		moving = false
		var pid := target_port_id
		target_port_id = -1
		arrived_at_port.emit(pid)
		return
	var step := get_current_speed() * delta
	if step > dist:
		step = dist
	global_position += direction.normalized() * step
	# No rotation on Sprite2D — sprite already shows ship from above-ish.
	# Mirror flip based on horizontal direction.
	if direction.x < 0:
		sprite.flip_h = true
	else:
		sprite.flip_h = false
	# Sail animation: alternate between ship_00.png and ship_01.png
	anim_timer += delta
	if anim_timer >= ANIM_PERIOD:
		anim_timer = 0.0
		anim_frame = 1 - anim_frame
		set_ship_sprite(anim_frame)
	# Trail
	if trail.get_point_count() == 0 or global_position.distance_to(trail.get_point_position(trail.get_point_count() - 1)) > 8.0:
		trail.add_point(global_position)
		if trail.get_point_count() > 40:
			trail.remove_point(0)
