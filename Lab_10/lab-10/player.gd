extends Node3D

@export var control_speed: float = 10.0
@export var limit_x: float = 5.0
@export var limit_y: float = 3.0

@export var bullet_scene: PackedScene # Tu przeciągnij bullet.tscn
@export var shoot_delay: float = 0.3
var _shoot_cooldown: float = 0.0

func _process(delta: float):
	# Ruch
	var input_dir = Input.get_vector("ui_left", "ui_right", "ui_down", "ui_up")
	position.x = clamp(position.x + input_dir.x * control_speed * delta, -limit_x, limit_x)
	position.y = clamp(position.y + input_dir.y * control_speed * delta, -limit_y, limit_y)
	
	# Cooldown i strzelanie
	if _shoot_cooldown > 0:
		_shoot_cooldown -= delta
		
	if Input.is_action_pressed("ui_accept") and _shoot_cooldown <= 0:
		shoot()

func shoot():
	if bullet_scene == null: return
	
	var bullet = bullet_scene.instantiate()
	# Dodajemy do root, żeby pocisk leciał niezależnie
	get_tree().root.add_child(bullet)
	
	bullet.global_position = global_position
	bullet.global_rotation = global_rotation
	_shoot_cooldown = shoot_delay
