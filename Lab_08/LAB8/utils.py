import pyray as rl
import math
import config


def clean_dead_objects(entities):
    """Filtruje listę, zostawiając tylko aktywne obiekty."""
    return [e for e in entities if e.alive]


def draw_text_centered(text, y, font_size, color):
    """Rysuje tekst wycentrowany w osi X."""
    text_width = rl.measure_text(text, font_size)
    x = (config.SCREEN_W // 2) - (text_width // 2)
    rl.draw_text(text, x, y, font_size, color)


def check_collision_circles(p1, r1, p2, r2):
    """Matematyka kolizji kołowej."""
    distance = math.hypot(p1.x - p2.x, p1.y - p2.y)
    return distance < (r1 + r2)


def ghost_positions(pos, size):
    """Obsługa rysowania obiektów na krawędziach (torus)."""
    positions = [pos]
    w, h = config.SCREEN_W, config.SCREEN_H
    if pos.x < size:
        positions.append(rl.Vector2(pos.x + w, pos.y))
    elif pos.x > w - size:
        positions.append(rl.Vector2(pos.x - w, pos.y))

    extra_y = []
    for p in positions:
        if p.y < size:
            extra_y.append(rl.Vector2(p.x, p.y + h))
        elif p.y > h - size:
            extra_y.append(rl.Vector2(p.x, p.y - h))
    return positions + extra_y