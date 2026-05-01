import pyray as pr

def main():
    pr.init_window(800, 600, "Neon Labyrinth - Lab 10")
    pr.set_target_fps(60)

    player_pos = pr.Vector2(100, 100)
    player_speed = 250.0

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        # Prosty ruch bez kolizji
        if pr.is_key_down(pr.KeyboardKey.KEY_W): player_pos.y -= player_speed * dt
        if pr.is_key_down(pr.KeyboardKey.KEY_S): player_pos.y += player_speed * dt
        if pr.is_key_down(pr.KeyboardKey.KEY_A): player_pos.x -= player_speed * dt
        if pr.is_key_down(pr.KeyboardKey.KEY_D): player_pos.x += player_speed * dt

        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pr.draw_circle_v(player_pos, 12, pr.Color(0, 255, 255, 255))
        pr.draw_text("Lab 10: Podstawowy ruch", 20, 20, 20, pr.WHITE)
        pr.end_drawing()

    pr.close_window()

if __name__ == "__main__":
    main()