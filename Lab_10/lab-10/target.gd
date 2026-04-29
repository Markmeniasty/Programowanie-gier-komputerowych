extends Area3D

func _ready():
	# Podłączenie sygnału. Upewnij się, że ten skrypt jest na węźle Area3D!
	area_entered.connect(_on_hit)
	print(name, " jest gotowy i czeka na kolizję...")

func _on_hit(area: Area3D):
	# Ten print MUSI się pojawić w konsoli, jeśli cokolwiek wejdzie w cel
	print("!!! KOLIZJA WYKRYTA z: ", area.name, " !!!")
	
	# Usunięcie na siłę, żeby sprawdzić, czy chociaż to działa
	print("Próbuję usunąć cel: ", name)
	queue_free()
	
	if area.has_method("queue_free"):
		print("Próbuję usunąć pocisk: ", area.name)
		area.queue_free()
