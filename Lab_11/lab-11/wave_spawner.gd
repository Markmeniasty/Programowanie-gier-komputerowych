extends Node

@export var enemy_scene: PackedScene
@export var path_follow: PathFollow3D

# Tablica fal - wzorzec danych (Zadanie 3)
var waves: Array[Dictionary] = [
	{ "count": 3, "x_positions": [-3.0, 0.0, 3.0], "z_offset": -30.0, "delay": 2.0 },
	{ "count": 2, "x_positions": [-4.0, 4.0], "z_offset": -40.0, "delay": 5.0 },
	{ "count": 4, "x_positions": [-3.0, -1.0, 1.0, 3.0], "z_offset": -50.0, "delay": 10.0 }
]

var _spawned: Array[bool] = [false, false, false]
var _timer: float = 0.0

func _process(delta: float):
	_timer += delta
	
	for i in range(waves.size()):
		# Sprawdzanie czy czas minął i czy fala nie została już stworzona
		if not _spawned[i] and _timer >= waves[i]["delay"]:
			spawn_wave(waves[i])
			_spawned[i] = true

func spawn_wave(wave_data: Dictionary):
	for i in range(wave_data["count"]):
		var enemy = enemy_scene.instantiate()
		get_tree().root.add_child(enemy)
		
		# Pobranie aktualnej pozycji szyny
		var spawn_pos = path_follow.global_position 
		
		# Modyfikacja pozycji o dane z fali[cite: 1]
		spawn_pos.x += wave_data["x_positions"][i]
		spawn_pos.z += wave_data["z_offset"]
		
		# Przypisanie pozycji do wroga[cite: 1]
		enemy.global_position = spawn_pos
		
		# Łączenie sygnału died z funkcją punktacji w main.gd[cite: 1]
		var main_node = get_tree().current_scene
		if enemy.has_signal("died") and main_node.has_method("add_score"):
			enemy.died.connect(main_node.add_score)
