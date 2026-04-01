import pyray as rl
import config  # Importujemy cały plik config


def ghost_positions(pos, size):
    positions = [pos]
    # Korzystam z config.SCREEN_W zamiast zmiennej lokalnej
    w, h = config.SCREEN_W, config.SCREEN_H

    # Logika sprawdzania krawędzi X
    if pos.x < size:
        positions.append(rl.Vector2(pos.x + w, pos.y))
    elif pos.x > w - size:
        positions.append(rl.Vector2(pos.x - w, pos.y))

    # Logika sprawdzania krawędzi Y
    extra_y = []
    for p in positions:
        if p.y < size:
            extra_y.append(rl.Vector2(p.x, p.y + h))
        elif p.y > h - size:
            extra_y.append(rl.Vector2(p.x, p.y - h))

    return positions + extra_y