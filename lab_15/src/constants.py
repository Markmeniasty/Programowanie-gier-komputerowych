import pyray as pr

SCREEN_WIDTH = 810
SCREEN_HEIGHT = 630
TILE_SIZE = 30
PLAYER_RADIUS = 8
PLAYER_SPEED = 220.0
FOG_RADIUS = 150.0

# Kolory zdefiniowane bezpiecznie
C_CYAN = pr.Color(0, 255, 255, 255)
C_GRAY = pr.Color(30, 30, 30, 255)
C_WHITE = pr.Color(255, 255, 255, 255)
C_GREEN = pr.Color(0, 255, 0, 255)
C_BLACK = pr.Color(0, 0, 0, 255)

ENEMY_RADIUS = 7
ENEMY_SPEED = 120.0
C_RED = pr.Color(230, 41, 55, 255)
BULLET_RADIUS = 3
BULLET_SPEED = 500.0
C_YELLOW = pr.Color(255, 255, 0, 255)
DETECTION_RADIUS = 100.0  # Odległość, przy której wróg zaczyna gonić
SCORE_FILE = "highscore.txt"
# Kolory do efektów menu
C_DARK_CYAN = pr.Color(0, 150, 150, 255)
C_NEON_PINK = pr.Color(255, 0, 255, 255)