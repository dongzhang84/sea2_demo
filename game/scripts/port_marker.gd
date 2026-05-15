extends Node2D
## Clickable port marker on the world map.

signal clicked(port_data: Dictionary)

@onready var label: Label = $Label
@onready var icon: ColorRect = $Icon
@onready var area: Area2D = $Area2D

var port_data: Dictionary = {}


func _ready() -> void:
	area.input_event.connect(_on_input_event)
	area.mouse_entered.connect(_on_mouse_entered)
	area.mouse_exited.connect(_on_mouse_exited)
	# Apply any data set before _ready
	if not port_data.is_empty():
		label.text = port_data.get("cn_name", port_data.get("name", "?"))


func set_port_data(data: Dictionary) -> void:
	port_data = data
	# Only update label if node is ready (otherwise _ready() will apply it)
	if is_node_ready():
		label.text = data.get("cn_name", data.get("name", "?"))


func _on_input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		clicked.emit(port_data)


func _on_mouse_entered() -> void:
	icon.color = Color(1, 1, 0.4)


func _on_mouse_exited() -> void:
	icon.color = Color(1, 0.4, 0.2)
