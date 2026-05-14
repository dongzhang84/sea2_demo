extends Node2D
## Wind/current overlay. Renders arrows on a 30×45 grid over the worldmap.
## Toggle visibility with 'W' key.

const COLS := 30
const ROWS := 45

var grid: Array = []     # 45 rows × 30 cols of byte values
var block_w: float = 42.667
var block_h: float = 16.0


func _ready() -> void:
	var file := FileAccess.open("res://data/wind_grid.json", FileAccess.READ)
	if file == null:
		push_error("Cannot open wind_grid.json")
		return
	var json_text := file.get_as_text()
	file.close()
	var parsed: Variant = JSON.parse_string(json_text)
	if parsed == null: return
	grid = parsed.get("grid", [])
	block_w = parsed.get("game_block_w", 42.667)
	block_h = parsed.get("game_block_h", 16.0)
	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_W:
		visible = not visible


func _draw() -> void:
	# Draw subtle arrows in each non-zero cell. Skip dense rendering for clarity.
	# Show only every 2nd cell for readability.
	for row_idx in range(ROWS):
		if row_idx % 2 != 0: continue
		var row: Array = grid[row_idx]
		for col_idx in range(COLS):
			var v: int = row[col_idx]
			if v == 0: continue
			var hi: int = (v >> 4) & 0x0F
			var lo: int = v & 0x0F
			# Center of block
			var cx: float = col_idx * block_w + block_w * 0.5
			var cy: float = row_idx * block_h + block_h * 0.5
			# Direction angle (0=N, 90=E in our convention)
			var angle_deg: float = (hi / 16.0) * 360.0 - 90.0  # Godot 0° = right
			var angle_rad: float = deg_to_rad(angle_deg)
			# Arrow length proportional to strength
			var length: float = 6.0 + (lo / 15.0) * 8.0  # 6-14 px
			var dx: float = cos(angle_rad) * length
			var dy: float = sin(angle_rad) * length
			# Color by strength (blue→yellow→red)
			var strength_norm: float = lo / 15.0
			var color := Color(0.4 + strength_norm * 0.6, 0.7 + strength_norm * 0.3, 1.0 - strength_norm * 0.5, 0.55)
			# Arrow tail to head
			var tail := Vector2(cx - dx * 0.5, cy - dy * 0.5)
			var head := Vector2(cx + dx * 0.5, cy + dy * 0.5)
			draw_line(tail, head, color, 1.5, true)
			# Arrowhead
			var ah_angle1 := angle_rad + 2.5
			var ah_angle2 := angle_rad - 2.5
			var ah_size := 3.0
			draw_line(head, head + Vector2(cos(ah_angle1), sin(ah_angle1)) * ah_size, color, 1.2, true)
			draw_line(head, head + Vector2(cos(ah_angle2), sin(ah_angle2)) * ah_size, color, 1.2, true)


func get_wind_at(world_pos: Vector2) -> Dictionary:
	"""Returns {direction_rad, strength_0_1} for the block at the given world position."""
	var col: int = int(world_pos.x / block_w)
	var row: int = int(world_pos.y / block_h)
	if col < 0 or col >= COLS or row < 0 or row >= ROWS:
		return {"direction_rad": 0.0, "strength_0_1": 0.0}
	var v: int = grid[row][col]
	if v == 0:
		return {"direction_rad": 0.0, "strength_0_1": 0.0}
	var hi: int = (v >> 4) & 0x0F
	var lo: int = v & 0x0F
	return {
		"direction_rad": deg_to_rad((hi / 16.0) * 360.0 - 90.0),
		"strength_0_1": lo / 15.0,
	}
