extends Node3D

@export var control_speed: float = 10.0
@export var limit_x: float = 4.0
@export var limit_y: float = 2.0

func _process(delta: float) -> void:
	var input_dir = Input.get_vector("ui_left", "ui_right", "ui_down", "ui_up")
	
	# Obliczanie nowej pozycji
	var new_pos_x = position.x + input_dir.x * control_speed * delta
	var new_pos_y = position.y + input_dir.y * control_speed * delta
	
	# Zastosowanie ograniczeń (clamp)
	position.x = clamp(new_pos_x, -limit_x, limit_x)
	position.y = clamp(new_pos_y, -limit_y, limit_y)
