import pyray as rl
import math

# STAŁE FIZYCZNE
ROT_SPEED = 4.5  # Radiany/s
THRUST = 450.0  # Przyspieszenie px/s^2
FRICTION = 180.0  # Stałe hamowanie px/s^2
MAX_SPEED = 500.0  # Limit prędkości px/s
BRAKE_FORCE = 0.95  # Mnożnik hamulca (zmniejsza prędkość o 5% co klatkę)


class Ship:
    def __init__(self, x, y):
        self.pos = rl.Vector2(x, y)
        self.vel = rl.Vector2(0, 0)
        self.angle = 0.0
        self.radius = 15  # Promień do detekcji kolizji ze ścianami

        self.verts = [rl.Vector2(0, -15), rl.Vector2(-10, 10), rl.Vector2(10, 10)]
        self.flame_verts = [rl.Vector2(-5, 10), rl.Vector2(5, 10), rl.Vector2(0, 20)]

    def rotate_point(self, p, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        return rl.Vector2(p.x * c - p.y * s, p.x * s + p.y * c)

    def update(self, dt, screen_w, screen_h):
        # 1. Obrót
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT): self.angle -= ROT_SPEED * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT): self.angle += ROT_SPEED * dt

        # 2. Ciąg (Thrust)
        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            forward = rl.Vector2(math.sin(self.angle), -math.cos(self.angle))
            self.vel.x += forward.x * THRUST * dt
            self.vel.y += forward.y * THRUST * dt

        # 3. Hamulec Awaryjny (Zadanie *)
        if rl.is_key_down(rl.KeyboardKey.KEY_Z):
            # Gwałtowne wygaszanie prędkości
            self.vel.x *= BRAKE_FORCE
            self.vel.y *= BRAKE_FORCE

        # 4. Tarcie (Friction)
        speed = math.hypot(self.vel.x, self.vel.y)
        if speed > 0:
            drop = FRICTION * dt
            new_speed = max(0, speed - drop)
            self.vel.x = (self.vel.x / speed) * new_speed
            self.vel.y = (self.vel.y / speed) * new_speed

        # 5. Limit prędkości
        speed = math.hypot(self.vel.x, self.vel.y)
        if speed > MAX_SPEED:
            self.vel.x = (self.vel.x / speed) * MAX_SPEED
            self.vel.y = (self.vel.y / speed) * MAX_SPEED

        # 6. Ruch
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        # 7. Odbijanie od krawędzi (Zadanie **)
        # Sprawdzamy X
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.vel.x *= -0.7  # Odbicie z utratą energii
        elif self.pos.x + self.radius > screen_w:
            self.pos.x = screen_w - self.radius
            self.vel.x *= -0.7

        # Sprawdzamy Y
        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -0.7
        elif self.pos.y + self.radius > screen_h:
            self.pos.y = screen_h - self.radius
            self.vel.y *= -0.7

    def draw(self, debug=False):
        # Kadłub
        transformed = []
        for v in self.verts:
            rot = self.rotate_point(v, self.angle)
            transformed.append(rl.Vector2(rot.x + self.pos.x, rot.y + self.pos.y))
        rl.draw_triangle_lines(transformed[0], transformed[1], transformed[2], rl.RAYWHITE)

        # Płomień
        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            f_trans = []
            for v in self.flame_verts:
                rot = self.rotate_point(v, self.angle)
                f_trans.append(rl.Vector2(rot.x + self.pos.x, rot.y + self.pos.y))
            rl.draw_triangle_lines(f_trans[0], f_trans[1], f_trans[2], rl.ORANGE)

        if debug:
            end_v = rl.Vector2(self.pos.x + self.vel.x * 0.2, self.pos.y + self.vel.y * 0.2)
            rl.draw_line_v(self.pos, end_v, rl.GREEN)
            rl.draw_circle_lines(int(self.pos.x), int(self.pos.y), self.radius, rl.DARKGRAY)