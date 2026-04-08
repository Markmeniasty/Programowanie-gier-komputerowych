import pyray as rl
import math
import config
from utils import ghost_positions


class Bullet:
    def __init__(self, x, y, angle):
        self.pos = rl.Vector2(x, y)
        self.radius = config.BULLET_RADIUS
        # Obliczamy wektor kierunku na podstawie kąta statku
        self.vel = rl.Vector2(
            math.sin(angle) * config.BULLET_SPEED,
            -math.cos(angle) * config.BULLET_SPEED
        )
        self.life = config.BULLET_LIFE
        self.alive = True

    def update(self, dt):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        # Zawijanie (torus)
        self.pos.x %= config.SCREEN_W
        self.pos.y %= config.SCREEN_H

        # Cykl życia
        self.life -= dt
        if self.life <= 0:
            self.alive = False

    def draw(self):
        for p in ghost_positions(self.pos, self.radius):
            rl.draw_circle_v(p, self.radius, rl.YELLOW)