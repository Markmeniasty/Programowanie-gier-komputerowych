import pyray as rl
import math
import config
from utils import ghost_positions

class Ship:
    def __init__(self, x, y):
        self.pos = rl.Vector2(x, y)
        self.vel = rl.Vector2(0, 0)
        self.angle = 0.0
        self.radius = 15
        self.verts = [rl.Vector2(0, -15), rl.Vector2(-10, 10), rl.Vector2(10, 10)]
        self.flame_verts = [rl.Vector2(-5, 10), rl.Vector2(5, 10), rl.Vector2(0, 20)]

    def wrap(self):
        self.pos.x %= config.SCREEN_W
        self.pos.y %= config.SCREEN_H

    def update(self, dt):
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT): self.angle -= config.SHIP_ROT_SPEED * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT): self.angle += config.SHIP_ROT_SPEED * dt

        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            forward = rl.Vector2(math.sin(self.angle), -math.cos(self.angle))
            self.vel.x += forward.x * config.SHIP_THRUST * dt
            self.vel.y += forward.y * config.SHIP_THRUST * dt

        if rl.is_key_down(rl.KeyboardKey.KEY_Z):
            self.vel.x *= config.SHIP_BRAKE_FORCE
            self.vel.y *= config.SHIP_BRAKE_FORCE

        speed = math.hypot(self.vel.x, self.vel.y)
        if speed > 0:
            new_speed = max(0, speed - config.SHIP_FRICTION * dt)
            if new_speed > config.SHIP_MAX_SPEED: new_speed = config.SHIP_MAX_SPEED
            self.vel.x = (self.vel.x / speed) * new_speed
            self.vel.y = (self.vel.y / speed) * new_speed

        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.wrap()

    def draw(self, debug=False):
        for p in ghost_positions(self.pos, self.radius):
            # Rysowanie kadłuba
            s, c = math.sin(self.angle), math.cos(self.angle)
            ship_pts = []
            for v in self.verts:
                ship_pts.append(rl.Vector2(v.x * c - v.y * s + p.x, v.x * s + v.y * c + p.y))
            rl.draw_triangle_lines(ship_pts[0], ship_pts[1], ship_pts[2], rl.RAYWHITE)

            # Rysowanie płomienia
            if rl.is_key_down(rl.KeyboardKey.KEY_UP):
                flame_pts = []
                for v in self.flame_verts:
                    flame_pts.append(rl.Vector2(v.x * c - v.y * s + p.x, v.x * s + v.y * c + p.y))
                rl.draw_triangle_lines(flame_pts[0], flame_pts[1], flame_pts[2], rl.ORANGE)