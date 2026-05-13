extends Area3D # Działa z fizycznymi sygnałami kolizji

@export var control_speed: float = 10.0
@export var limit_x: float = 5.0
@export var limit_y: float = 3.0

@export var bullet_scene: PackedScene # Tu przeciągnij bullet.tscn
@export var shoot_delay: float = 0.3
var _shoot_cooldown: float = 0.0

# Zmienne systemu zdrowia (Zadanie 2)
@export var max_hp: int = 5
var current_hp: int = max_hp

# --- ZADANIE 4: Flaga niezniszczalności ---
var is_invincible: bool = false

func _ready():
	# Zadanie 4B: Dodajemy gracza do grupy, aby wróg mógł go namierzyć
	add_to_group("player") 
	
	# Podłączenie sygnału wykrywania ścian (Zadanie 2)
	body_entered.connect(_on_body_entered)

func _process(delta: float):
	# Ruch gracza
	var input_dir = Input.get_vector("ui_left", "ui_right", "ui_down", "ui_up")
	position.x = clamp(position.x + input_dir.x * control_speed * delta, -limit_x, limit_x)
	position.y = clamp(position.y + input_dir.y * control_speed * delta, -limit_y, limit_y)
	
	# Obsługa strzelania
	if _shoot_cooldown > 0:
		_shoot_cooldown -= delta
		
	if Input.is_action_pressed("ui_accept") and _shoot_cooldown <= 0:
		shoot()
		
	# --- ZADANIE 4: Wykrywanie wciśnięcia klawisza Barrel Roll ---
	# ui_select to domyślnie klawisz SPACJA. Jeśli strzelasz spacją (ui_accept), 
	# możesz zmienić to np. na "ui_focus_next" (Tab) lub przypisać własną akcję.
	if Input.is_action_just_pressed("ui_select"):
		execute_barrel_roll()

func shoot():
	if bullet_scene == null: return
	
	var bullet = bullet_scene.instantiate()
	get_tree().root.add_child(bullet)
	
	bullet.global_position = global_position
	bullet.global_rotation = global_rotation
	bullet.direction = Vector3(0, 0, -1)
	
	_shoot_cooldown = shoot_delay

# --- ZADANIE 4: Logika wykonania uniku ---
func execute_barrel_roll():
	# Jeśli już kręcimy beczkę, ignorujemy kolejne wciśnięcie klawisza
	if is_invincible: 
		return
		
	is_invincible = true
	print("BARREL ROLL! Gracz jest niezniszczalny.")
	
	# Szukamy odtwarzacza animacji wewnątrz MeshInstance3D
	if has_node("MeshInstance3D/AnimationPlayer"):
		$MeshInstance3D/AnimationPlayer.play("barrel_roll")
		# Słowo kluczowe 'await' zatrzymuje wykonanie dalszego kodu tej funkcji,
		# dopóki AnimationPlayer nie wyemituje sygnału 'animation_finished'
		await $MeshInstance3D/AnimationPlayer.animation_finished
		
	is_invincible = false
	print("Koniec uniku. Gracz ponownie wrażliwy na ciosy.")

# Funkcja odbierająca sygnał zderzenia ze ścianą (Zadanie 2)
func _on_body_entered(body: Node3D):
	if body is StaticBody3D:
		print("Uderzenie w ścianę: ", body.name)
		_take_damage(1)

# Prywatna metoda zadawania obrażeń (Zadanie 2 i 4)
func _take_damage(amount: int):
	# --- ZADANIE 4: Jeśli aktywna jest niezniszczalność, ignoruj obrażenia ---
	if is_invincible:
		print("Uniknięto obrażeń dzięki Barrel Roll!")
		return
		
	current_hp -= amount
	print("Gracz otrzymał obrażenia! Aktualne HP: ", current_hp)
	
	if current_hp <= 0:
		print("Statek zniszczony! Game Over.")
		set_process(false)
