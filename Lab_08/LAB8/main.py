import pyray as rl
import random
import enum
import config
import math
import os
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion
from utils import clean_dead_objects, draw_text_centered, check_collision_circles


class GameState(enum.Enum):
    MENU = 1
    GAME = 2
    GAME_OVER = 3


class AsteroidsGame:
    def __init__(self):
        self.state = GameState.MENU
        self.score = 0
        self.best = self.load_best_score()
        self.frame_counter = 0

        self.wave_number = 1
        self.wave_cooldown = 0.0

        self.player = None
        self.asteroids = []
        self.bullets = []
        self.explosions = []

        self.sfx_shoot = None
        self.sfx_explode = None
        self.texture_stars = None

    # --- LOGIKA REKORDÓW (ZADANIE **) ---
    def load_best_score(self):
        try:
            if os.path.exists("scores.txt"):
                with open("scores.txt", "r") as f:
                    return int(f.read().strip())
        except:
            pass
        return 0

    def save_best_score(self):
        try:
            with open("scores.txt", "w") as f:
                f.write(str(self.best))
        except Exception as e:
            print(f"Błąd zapisu: {e}")

    # --- ZASOBY ---
    def load_assets(self):
        rl.init_audio_device()
        self.sfx_shoot = rl.load_sound("assets/shoot.wav")
        self.sfx_explode = rl.load_sound("assets/explode.wav")
        self.texture_stars = rl.load_texture("assets/stars.png")
        self._spawn_wave()  # Asteroidy do tła menu

    def _spawn_wave(self):
        base = getattr(config, 'INITIAL_ASTEROIDS', 4)
        count = base + (self.wave_number - 1) * 2
        for _ in range(count):
            x, y = random.randint(0, config.SCREEN_W), random.randint(0, config.SCREEN_H)
            # Bezpieczna odległość od gracza (środek ekranu)
            while rl.vector2_distance(rl.Vector2(x, y), rl.Vector2(config.SCREEN_W // 2, config.SCREEN_H // 2)) < 150:
                x, y = random.randint(0, config.SCREEN_W), random.randint(0, config.SCREEN_H)
            self.asteroids.append(Asteroid(x, y, "LARGE"))

    def start_new_game(self):
        self.player = Ship(config.SCREEN_W // 2, config.SCREEN_H // 2)
        self.score = 0
        self.wave_number = 1
        self.wave_cooldown = 0.0
        self.asteroids, self.bullets, self.explosions = [], [], []
        self._spawn_wave()
        self.state = GameState.GAME

    # --- LOGIKA (UPDATE) ---
    def update(self, dt):
        self.frame_counter += 1

        if self.state == GameState.MENU:
            for a in self.asteroids: a.update(dt)
            if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
                self.start_new_game()

        elif self.state == GameState.GAME:
            self._update_game_logic(dt)

        elif self.state == GameState.GAME_OVER:
            if rl.is_key_pressed(rl.KeyboardKey.KEY_R):
                self.state = GameState.MENU

    def _update_game_logic(self, dt):
        # Input
        if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE) and len(self.bullets) < config.BULLET_LIMIT:
            self.bullets.append(Bullet(self.player.pos.x, self.player.pos.y, self.player.angle))
            rl.play_sound(self.sfx_shoot)

        # Fizyka
        self.player.update(dt)
        for e in self.asteroids + self.bullets + self.explosions: e.update(dt)

        # Kolizje
        new_ast = []
        for b in self.bullets:
            for a in self.asteroids:
                if a.alive and b.alive and check_collision_circles(b.pos, b.radius, a.pos, a.radius):
                    b.alive = a.alive = False
                    rl.play_sound(self.sfx_explode)
                    self.explosions.append(Explosion(a.pos.x, a.pos.y))
                    self.score += config.AST_SIZES[a.size_key]["points"]
                    if self.score > self.best:
                        self.best = self.score
                        self.save_best_score()
                    self._split_asteroid(a, new_ast)
        self.asteroids.extend(new_ast)

        for a in self.asteroids:
            if a.alive and check_collision_circles(self.player.pos, self.player.radius, a.pos, a.radius):
                rl.play_sound(self.sfx_explode)
                self.explosions.append(Explosion(self.player.pos.x, self.player.pos.y))
                self.state = GameState.GAME_OVER

        # Fale i czyszczenie
        self.bullets = clean_dead_objects(self.bullets)
        self.asteroids = clean_dead_objects(self.asteroids)
        self.explosions = clean_dead_objects(self.explosions)

        if len(self.asteroids) == 0 and self.wave_cooldown <= 0:
            self.wave_cooldown = 2.0

        if self.wave_cooldown > 0:
            self.wave_cooldown -= dt
            if self.wave_cooldown <= 0:
                self.wave_number += 1
                self._spawn_wave()

    def _split_asteroid(self, parent, target_list):
        if parent.size_key == "LARGE":
            target_list.extend(
                [Asteroid(parent.pos.x, parent.pos.y, "MEDIUM"), Asteroid(parent.pos.x, parent.pos.y, "MEDIUM")])
        elif parent.size_key == "MEDIUM":
            target_list.extend(
                [Asteroid(parent.pos.x, parent.pos.y, "SMALL"), Asteroid(parent.pos.x, parent.pos.y, "SMALL")])

    # --- RENDEROWANIE ---
    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        # Tło gwiazd
        rl.draw_texture_pro(self.texture_stars,
                            rl.Rectangle(0, 0, self.texture_stars.width, self.texture_stars.height),
                            rl.Rectangle(0, 0, config.SCREEN_W, config.SCREEN_H),
                            rl.Vector2(0, 0), 0, rl.DARKGRAY)

        for e in self.asteroids + self.bullets + self.explosions: e.draw()

        if self.state == GameState.MENU:
            self._draw_menu_ui()
        elif self.state == GameState.GAME:
            self.player.draw()
            self._draw_game_ui()
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over_ui()

        rl.end_drawing()

    def _draw_menu_ui(self):
        rl.draw_rectangle_gradient_v(0, 0, config.SCREEN_W, config.SCREEN_H, rl.color_alpha(rl.BLACK, 0.3),
                                     rl.color_alpha(rl.BLACK, 0.8))
        draw_text_centered("ASTEROIDS", 182, 82, rl.BLACK)
        draw_text_centered("ASTEROIDS", 180, 80, rl.RAYWHITE)

        # Pulsujący napis startowy
        alpha = int(127 + 128 * math.sin(self.frame_counter * 0.1))
        draw_text_centered("PRESS [ENTER] TO START", 340, 25, rl.get_color(0xFFD70000 | alpha))

        rl.draw_rectangle_rounded(rl.Rectangle(config.SCREEN_W // 2 - 110, 490, 220, 40), 0.3, 8,
                                  rl.color_alpha(rl.DARKGRAY, 0.3))
        draw_text_centered(f"HI-SCORE: {self.best:05d}", 500, 20, rl.GOLD)

    def _draw_game_ui(self):
        # Szklany pasek HUD
        rl.draw_rectangle_gradient_v(0, 0, config.SCREEN_W, 50, rl.color_alpha(rl.BLACK, 0.8),
                                     rl.color_alpha(rl.BLACK, 0.0))
        rl.draw_line(0, 50, config.SCREEN_W, 50, rl.color_alpha(rl.RAYWHITE, 0.1))

        rl.draw_text(f"PTS: {self.score:05d}", 25, 15, 22, rl.RAYWHITE)

        wave_txt = f"PHASE {self.wave_number:02d}"
        rl.draw_rectangle_rounded(rl.Rectangle(config.SCREEN_W // 2 - 60, 10, 120, 30), 0.5, 8,
                                  rl.color_alpha(rl.SKYBLUE, 0.2))
        rl.draw_text(wave_txt, config.SCREEN_W // 2 - rl.measure_text(wave_txt, 20) // 2, 15, 20, rl.SKYBLUE)

        rl.draw_text(f"HI-SCORE: {self.best:05d}", config.SCREEN_W - 180, 15, 20, rl.GOLD)

        if self.wave_cooldown > 0:
            draw_text_centered(f"WAVE {self.wave_number + 1} INCOMING", config.SCREEN_H // 2, 30, rl.GOLD)

    def _draw_game_over_ui(self):
        bg_alpha = 0.3 + 0.1 * math.sin(self.frame_counter * 0.05)
        rl.draw_rectangle(0, 0, config.SCREEN_W, config.SCREEN_H, rl.color_alpha(rl.MAROON, bg_alpha))

        draw_text_centered("MISSION FAILED", 198, 62, rl.BLACK)
        draw_text_centered("MISSION FAILED", 200, 60, rl.RED)

        rl.draw_rectangle_rounded(rl.Rectangle(config.SCREEN_W // 2 - 150, 280, 300, 120), 0.1, 8,
                                  rl.color_alpha(rl.BLACK, 0.6))
        draw_text_centered(f"TOTAL SCORE: {self.score:05d}", 310, 25, rl.RAYWHITE)
        draw_text_centered(f"WAVES SURVIVED: {self.wave_number}", 350, 20, rl.GRAY)

        if (self.frame_counter // 30) % 2 == 0:
            draw_text_centered("PRESS [R] TO REINITIALIZE", 450, 18, rl.LIGHTGRAY)

    def cleanup(self):
        rl.unload_texture(self.texture_stars)
        rl.unload_sound(self.sfx_shoot)
        rl.unload_sound(self.sfx_explode)
        rl.close_audio_device()
        rl.close_window()


def main():
    rl.init_window(config.SCREEN_W, config.SCREEN_H, "ASTEROIDS PROFESSIONAL")
    game = AsteroidsGame()
    game.load_assets()
    rl.set_target_fps(getattr(config, 'FPS_LIMIT', 60))

    while not rl.window_should_close():
        game.update(rl.get_frame_time())
        game.draw()

    game.cleanup()


if __name__ == "__main__":
    main()