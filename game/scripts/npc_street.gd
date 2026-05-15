extends Control
## Ambient NPC walkers for the port screen — a few Char sprites pacing back
## and forth, purely atmospheric.

const NPC_COUNT := 4
const WALK_SPEED := 22.0
const ANIM_PERIOD := 0.35

var npcs: Array = []   # each: {rect, char_id, frame, anim_t, dir, speed}


func _ready() -> void:
	custom_minimum_size = Vector2(480, 56)
	clip_contents = true
	_add_ground()
	_spawn_npcs()


func _add_ground() -> void:
	# A cobblestone-coloured dock strip so NPCs don't float over the map.
	var ground := ColorRect.new()
	ground.color = Color(0.42, 0.36, 0.28)
	ground.set_anchors_preset(Control.PRESET_FULL_RECT)
	ground.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(ground)
	var quay := ColorRect.new()   # darker quay edge at the top
	quay.color = Color(0.30, 0.26, 0.20)
	quay.set_anchors_preset(Control.PRESET_TOP_WIDE)
	quay.offset_bottom = 8.0
	quay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(quay)


func _spawn_npcs() -> void:
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	var width: float = max(custom_minimum_size.x, size.x, 480.0)
	for i in range(NPC_COUNT):
		var char_id: int = rng.randi_range(0, 6)
		var rect := TextureRect.new()
		rect.custom_minimum_size = Vector2(32, 32)
		rect.size = Vector2(32, 32)
		rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		rect.position = Vector2(rng.randf_range(10, width - 42), 16)
		add_child(rect)
		var npc := {
			"rect": rect, "char_id": char_id, "frame": 0,
			"anim_t": rng.randf() * ANIM_PERIOD,
			"dir": 1 if rng.randf() > 0.5 else -1,
			"speed": WALK_SPEED * rng.randf_range(0.7, 1.3),
		}
		_apply_frame(npc)
		npcs.append(npc)


func _apply_frame(npc: Dictionary) -> void:
	var path := "res://assets/npcs/char%d/frame%02d.png" % [npc.char_id, npc.frame]
	if ResourceLoader.exists(path):
		npc.rect.texture = load(path)
	npc.rect.flip_h = npc.dir < 0


func _process(delta: float) -> void:
	if not visible:
		return
	var width: float = max(custom_minimum_size.x, size.x, 480.0)
	for npc in npcs:
		# Walk
		var r: TextureRect = npc.rect
		r.position.x += npc.dir * npc.speed * delta
		if r.position.x < 4:
			r.position.x = 4
			npc.dir = 1
		elif r.position.x > width - 36:
			r.position.x = width - 36
			npc.dir = -1
		# Animate (alternate frame 0 / 1 for a walk cycle)
		npc.anim_t += delta
		if npc.anim_t >= ANIM_PERIOD:
			npc.anim_t = 0.0
			npc.frame = 1 - npc.frame
			_apply_frame(npc)
