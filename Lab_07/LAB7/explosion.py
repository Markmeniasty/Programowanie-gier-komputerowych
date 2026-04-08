import pyray as rl
import config


class Explosion:
    def __init__(self, x, y):
        self.pos = rl.Vector2(x, y)
        self.timer = 0.0
        self.alive = True

    def update(self, dt):
        self.timer += dt
        if self.timer >= config.EXPLOSION_DURATION:
            self.alive = False

    def draw(self):
        # Promień rośnie wraz z czasem
        progress = self.timer / config.EXPLOSION_DURATION
        radius = progress * config.EXPLOSION_MAX_RADIUS
        # Kolor zanika (alfa)
        alpha = int(255 * (1.0 - progress))
        color = rl.color_alpha(rl.ORANGE, alpha / 255.0)

        rl.draw_circle_lines(int(self.pos.x), int(self.pos.y), radius, color)