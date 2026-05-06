extends PathFollow3D

@export var rail_speed: float = 0.1# Wartość 0.1 oznacza 10% trasy na sekundę

func _process(delta: float) -> void:
	# Zwiększamy postęp o prędkość przemnożoną przez czas ramki
	progress_ratio += rail_speed * delta
