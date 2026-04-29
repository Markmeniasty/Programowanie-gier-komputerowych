extends Area3D

@export var speed: float = 40.0
@export var lifetime: float = 3.0

func _process(delta: float):
	# Ruch
	position += -transform.basis.z * speed * delta
	
	# Odliczanie czasu życia
	lifetime -= delta
	if lifetime <= 0:
		print("Pocisk wygasł (lifetime)") # To pokaże Ci w konsoli, czy funkcja działa
		queue_free()
