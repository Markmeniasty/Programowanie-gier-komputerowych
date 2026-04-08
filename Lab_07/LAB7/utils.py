import pyray as rl
import math
import config


def ghost_positions(pos, size):
    """
    Oblicza listę pozycji (oryginał + widma), na których należy narysować obiekt,
    aby uzyskać płynne przejście przez krawędzie ekranu (torus).
    """
    positions = [pos]
    w, h = config.SCREEN_W, config.SCREEN_H

    # 1. Sprawdzamy przesunięcia poziome (Lewo/Prawo)
    if pos.x < size:
        positions.append(rl.Vector2(pos.x + w, pos.y))
    elif pos.x > w - size:
        positions.append(rl.Vector2(pos.x - w, pos.y))

    # 2. Sprawdzamy przesunięcia pionowe (Góra/Dół) dla wszystkich punktów
    # (oryginału i widm bocznych), aby obsłużyć narożniki ekranu.
    extra_y = []
    for p in positions:
        if p.y < size:
            extra_y.append(rl.Vector2(p.x, p.y + h))
        elif p.y > h - size:
            extra_y.append(rl.Vector2(p.x, p.y - h))

    return positions + extra_y


def check_collision_circles(p1, r1, p2, r2):
    """
    Sprawdza kolizję dwóch okręgów na podstawie odległości euklidesowej.
    Zadanie 5 (Lab 07).

    p1, p2: rl.Vector2 (środki okręgów)
    r1, r2: float (promienie okręgów)
    """
    # math.hypot(dx, dy) oblicza sqrt(dx*dx + dy*dy)
    distance = math.hypot(p1.x - p2.x, p1.y - p2.y)

    # Kolizja zachodzi, gdy dystans między środkami jest mniejszy niż suma promieni
    return distance < (r1 + r2)