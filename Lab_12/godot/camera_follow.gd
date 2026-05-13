extends Camera3D

@export var camera_target: Node3D 
@export var lag_speed: float = 6.0

func _process(delta: float):
	if camera_target == null: return
	# Płynne podążanie (Lerp)
	global_position = global_position.lerp(camera_target.global_position, lag_speed * delta)
