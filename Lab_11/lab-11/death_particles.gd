extends GPUParticles3D

func _ready():
	emitting = true # Rozpocznij efekt
	# Czekaj na zakończenie lifetime i usuń węzeł
	await get_tree().create_timer(lifetime).timeout
	queue_free()
