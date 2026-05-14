extends Node2D
## Player's ship. Moves between ports with simple linear interpolation.
## Speed depends on distance (placeholder for wind/current mechanics).

signal arrived_at_port(port_id: int)

const BASE_SPEED_PX_PER_SEC := 80.0

var target_pos: Vector2 = Vector2.ZERO
var moving: bool = false
var target_port_id: int = -1
var wind_overlay: Node2D = null  # injected by main

@onready var sprite: Polygon2D = $Sprite
@onready var trail: Line2D = $Trail


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
		var pid := target_port_id  # capture before reset
		target_port_id = -1
		arrived_at_port.emit(pid)
		return
	var step := get_current_speed() * delta
	if step > dist:
		step = dist
	global_position += direction.normalized() * step
	# Update ship rotation to face direction
	if direction.length() > 0:
		sprite.rotation = direction.angle() + PI / 2
	# Update trail (every ~10px)
	if trail.get_point_count() == 0 or global_position.distance_to(trail.get_point_position(trail.get_point_count() - 1)) > 8.0:
		trail.add_point(global_position)
		# Cap trail length
		if trail.get_point_count() > 40:
			trail.remove_point(0)
