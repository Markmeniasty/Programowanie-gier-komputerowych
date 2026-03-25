import pyray as rl
from ship import Ship


def main():
    W, H = 800, 600
    rl.init_window(W, H, "Lab 05: Asteroids - Ship Physics")
    rl.set_target_fps(60)

    player = Ship(W // 2, H // 2)
    debug_mode = False

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        # Update - przekazujemy wymiary okna do obsługi odbić
        player.update(dt, W, H)

        if rl.is_key_pressed(rl.KeyboardKey.KEY_D):
            debug_mode = not debug_mode

        # Render
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        player.draw(debug=debug_mode)

        rl.draw_text("ARROWS: Move | Z: Brake | D: Debug", 10, 10, 20, rl.GRAY)
        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()