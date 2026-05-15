extends Node2D
## Clickable port marker on the world map. Label shows only on hover.

signal clicked(port_data: Dictionary)

@onready var label: Label = $Label
@onready var icon: ColorRect = $Icon
@onready var area: Area2D = $Area2D

var port_data: Dictionary = {}
const COLOR_IDLE := Color(1, 0.85, 0.2)      # yellow dot
const COLOR_HOVER := Color(1, 0.4, 0.1)      # orange when hovered


func _ready() -> void:
	area.input_event.connect(_on_input_event)
	area.mouse_entered.connect(_on_mouse_entered)
	area.mouse_exited.connect(_on_mouse_exited)
	label.text = port_data.get("cn_name", port_data.get("name", "?"))
	label.visible = false
	icon.color = COLOR_IDLE


func set_port_data(data: Dictionary) -> void:
	port_data = data
	if is_node_ready():
		label.text = data.get("cn_name", data.get("name", "?"))


func set_label_visible(v: bool) -> void:
	label.visible = v


func _on_input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		clicked.emit(port_data)


func _on_mouse_entered() -> void:
	icon.color = COLOR_HOVER
	label.visible = true
	# enlarge dot
	icon.offset_left = -5; icon.offset_top = -5
	icon.offset_right = 5; icon.offset_bottom = 5
	z_index = 10


func _on_mouse_exited() -> void:
	icon.color = COLOR_IDLE
	label.visible = false
	icon.offset_left = -3; icon.offset_top = -3
	icon.offset_right = 3; icon.offset_bottom = 3
	z_index = 0
