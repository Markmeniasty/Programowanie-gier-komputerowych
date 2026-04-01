import pyray as rl
import random
import math
import config
from utils import ghost_positions


class Asteroid:
    def __init__(self, x, y, size_key="LARGE"):
        self.pos = rl.Vector2(x, y)
        self.angle = 0.0

        # Pobieranie danych z konfiguracji na podstawie klucza
        cfg = config.AST_SIZES.get(size_key, config.AST_SIZES["LARGE"])
        self.radius = cfg["radius"]
        num_points = cfg["points"]
        base_speed = cfg["speed"]

        # Logika ruchu oparta na konfiguracji
        speed_val = base_speed * config.ASTEROID_SPEED_MULT
        self.vel = rl.Vector2(
            random.uniform(-1, 1) * speed_val,
            random.uniform(-1, 1) * speed_val
        )
        self.rot_speed = random.uniform(config.ASTEROID_ROT_MIN, config.ASTEROID_ROT_MAX)

        # Generowanie kształtu
        self.verts = []
        for i in range(num_points):
            a = (math.tau / num_points) * i
            dist = self.radius * random.uniform(0.7, 1.2)
            self.verts.append(rl.Vector2(math.cos(a) * dist, math.sin(a) * dist))

    def wrap(self):
        self.pos.x %= config.SCREEN_W
        self.pos.y %= config.SCREEN_H

    def update(self, dt):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.angle += self.rot_speed * dt
        self.wrap()

    def draw(self):
        for p in ghost_positions(self.pos, self.radius):
            transformed = []
            s, c = math.sin(self.angle), math.cos(self.angle)
            for v in self.verts:
                rx = v.x * c - v.y * s
                ry = v.x * s + v.y * c
                transformed.append(rl.Vector2(rx + p.x, ry + p.y))

            for i in range(len(transformed)):
                rl.draw_line_v(transformed[i], transformed[(i + 1) % len(transformed)], rl.LIGHTGRAY)