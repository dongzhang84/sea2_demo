extends PanelContainer
## Modal event dialog: portrait + title + description + 1-3 option buttons.

signal option_chosen(option: Dictionary)

@onready var title_lbl: Label = $V/Title
@onready var portrait_rect: TextureRect = $V/Row/Portrait
@onready var description_lbl: Label = $V/Row/Description
@onready var options_box: VBoxContainer = $V/Options


func show_event(event: Dictionary) -> void:
	title_lbl.text = event.get("title", "Event")
	description_lbl.text = event.get("description", "")
	# Portrait or icon
	var port_id = event.get("portrait_id")
	var icon_id = event.get("icon_id")
	if port_id != null:
		var path := "res://assets/portraits/%03d.png" % port_id
		if ResourceLoader.exists(path):
			portrait_rect.texture = load(path)
	elif icon_id != null:
		var path := "res://assets/items/%03d.png" % icon_id
		if ResourceLoader.exists(path):
			portrait_rect.texture = load(path)
	else:
		portrait_rect.texture = null
	# Clear old options
	for child in options_box.get_children():
		child.queue_free()
	# Add option buttons
	for opt in event.get("options", []):
		var btn := Button.new()
		btn.text = opt.get("label", "...")
		btn.custom_minimum_size = Vector2(0, 36)
		btn.pressed.connect(_on_option_pressed.bind(opt))
		options_box.add_child(btn)
	visible = true


func _on_option_pressed(opt: Dictionary) -> void:
	option_chosen.emit(opt)
	visible = false
