extends Node3D

@export var hp: int = 2
@export var score_value: int = 100
@export var death_effect: PackedScene # Tu wrzuć death_particles.tscn
@export var enemy_bullet_scene: PackedScene # Tu wrzuć enemy_bullet.tscn
@export var shoot_interval: float = 2.5

var _shoot_timer: float = 0.0

func _ready():
	# Łączymy sygnał Area3D, aby wykrywać pociski gracza
	if has_node("Area3D"):
		$Area3D.area_entered.connect(_on_hit)

func _process(delta: float):
	# Obsługa strzelania
	_shoot_timer += delta
	if _shoot_timer >= shoot_interval:
		shoot_at_player()
		_shoot_timer = 0.0

func shoot_at_player():
	var players = get_tree().get_nodes_in_group("player")
	if players.size() > 0 and enemy_bullet_scene != null:
		var target_player = players[0]
		var bullet = enemy_bullet_scene.instantiate()
		get_tree().root.add_child(bullet)
		bullet.global_position = global_position
		
		var dir = (target_player.global_position - global_position).normalized()
		bullet.direction = dir

# TA FUNKCJA JEST KLUCZOWA DO ZABIJANIA WROGA
func _on_hit(area: Area3D):
	# Zakładamy, że pocisk gracza jest na warstwie 3 (wartość 4)
	if area.collision_layer == 4:
		hp -= 1
		print("Wróg oberwał! HP: ", hp)
		
		if hp <= 0:
			spawn_death_effect()
			
			# Dodawanie punktów do main.gd
			var main_node = get_tree().current_scene
			if main_node.has_method("add_score"):
				main_node.add_score(score_value)
			
			area.queue_free() # Usuwamy pocisk gracza
			queue_free()      # Usuwamy wroga

func spawn_death_effect():
	if death_effect != null:
		var effect = death_effect.instantiate()
		get_tree().root.add_child(effect)
		effect.global_position = global_position
