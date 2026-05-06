extends Area3D

@export var speed: float = 40.0
@export var lifetime: float = 3.0
# TEJ LINII PRAWDOPODOBNIE BRAKUJE:
@export var direction: Vector3 = Vector3.ZERO 

func _process(delta: float):
	# Ruch musi korzystać ze zmiennej direction
	position += direction * speed * delta
	
	lifetime -= delta
	if lifetime <= 0:
		queue_free()
