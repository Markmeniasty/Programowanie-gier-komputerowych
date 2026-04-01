# Ustawienia Ekranu
SCREEN_W = 800
SCREEN_H = 600

# Fizyka Statku
SHIP_ROT_SPEED = 4.5
SHIP_THRUST = 450.0
SHIP_FRICTION = 180.0
SHIP_MAX_SPEED = 500.0
SHIP_BRAKE_FORCE = 0.95

# Parametry Asteroid (skalowanie trudności)
ASTEROID_SPEED_MULT = 50.0  # Mnożnik ogólnej prędkości
ASTEROID_ROT_MIN = -2.0
ASTEROID_ROT_MAX = 2.0

# Definicje Rozmiarów Asteroid (Promień, Punkty, Prędkość)
AST_SIZES = {
    "LARGE":  {"radius": 50, "points": 12, "speed": 1.0},
    "MEDIUM": {"radius": 25, "points": 9,  "speed": 1.5},
    "SMALL":  {"radius": 12, "points": 6,  "speed": 2.5}
}