extends Area3D

# Przeciągnij tutaj scenę death_particles.tscn w Inspektorze
@export var death_effect: PackedScene 

func _ready():
	# Łączymy sygnał kolizji
	area_entered.connect(_on_hit)

func _on_hit(area: Area3D):
	# Sprawdzamy, czy to pocisk gracza (warstwa 3, maska 4)
	# Jeśli pociski po prostu znikają, upewnij się, że warstwy są zgodne
	
	spawn_death_effect()
	
	# Dodawanie punktów do main.gd
	var main_node = get_tree().current_scene
	if main_node.has_method("add_score"):
		main_node.add_score(10) # Cele dają np. 10 punktów
	
	# Usuwanie pocisku i celu
	if area.has_method("queue_free"):
		area.queue_free()
	queue_free()

func spawn_death_effect():
	if death_effect != null:
		var effect = death_effect.instantiate()
		# Dodajemy do root, aby efekt nie zniknął natychmiast z celem
		get_tree().root.add_child(effect)
		effect.global_position = global_position
