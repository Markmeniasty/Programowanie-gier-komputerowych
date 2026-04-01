import pyray as rl
import random
from ship import Ship
from asteroid import Asteroid
import config
from config import SCREEN_W, SCREEN_H

def main():
    rl.init_window(SCREEN_W, SCREEN_H, "Lab 06: Toroidal Space")
    rl.set_target_fps(60)

    player = Ship(SCREEN_W // 2, SCREEN_H // 2)

    # Inicjalizacja asteroid
    asteroids = []
    types = ["LARGE", "MEDIUM", "SMALL"]
    for _ in range(6):
        asteroids.append(Asteroid(
            random.randint(0, config.SCREEN_W),
            random.randint(0, config.SCREEN_H),
            random.choice(types)
        ))

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        # Update
        player.update(dt)
        for a in asteroids:
            a.update(dt)

        # Render
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        player.draw()
        for a in asteroids:
            a.draw()

        rl.draw_text("TOPOLOGY: TORUS (MODULO)  BRAKE (Z)"   , 10, 10, 20, rl.DARKGRAY)
        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()