import pyray as pr


# --- LAB 12: Maszyna Stanów (FSM) ---
class GameState:
    MENU = 0
    GAMEPLAY = 1
    GAME_OVER = 2


def main():
    # Inicjalizacja (Lab 10/11)
    screen_width, screen_height = 800, 600
    pr.init_window(screen_width, screen_height, "Neon Labyrinth - Lab 12 FSM")
    pr.set_target_fps(60)

    # --- DEFINICJA BEZPIECZNYCH KOLORÓW ---
    COLOR_CYAN = pr.Color(0, 255, 255, 255)
    COLOR_WHITE = pr.Color(255, 255, 255, 255)
    COLOR_RED = pr.Color(230, 41, 55, 255)
    COLOR_GREEN = pr.Color(0, 228, 48, 255)
    COLOR_DARK_GRAY = pr.Color(80, 80, 80, 255)

    # --- Stan początkowy ---
    current_state = GameState.MENU

    # Dane gracza
    player_pos = pr.Vector2(100.0, 100.0)
    player_radius = 12.0
    player_speed = 250.0

    # Przeszkody (Lab 11)
    walls = [
        pr.Rectangle(200, 150, 400, 40),
        pr.Rectangle(400, 300, 50, 200),
        pr.Rectangle(0, 0, 800, 10),
        pr.Rectangle(0, 590, 800, 10),
        pr.Rectangle(0, 0, 10, 600),
        pr.Rectangle(790, 0, 10, 600)
    ]

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        # --- LOGIKA MASZYNY STANÓW ---
        if current_state == GameState.MENU:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
                current_state = GameState.GAMEPLAY
                player_pos = pr.Vector2(100, 100)

        elif current_state == GameState.GAMEPLAY:
            old_pos = pr.Vector2(player_pos.x, player_pos.y)

            # Ruch w Y
            if pr.is_key_down(pr.KeyboardKey.KEY_W): player_pos.y -= player_speed * dt
            if pr.is_key_down(pr.KeyboardKey.KEY_S): player_pos.y += player_speed * dt
            for wall in walls:
                if pr.check_collision_circle_rec(player_pos, player_radius, wall):
                    # Sprawdzamy czy to ściana wewnętrzna (śmierć) czy zewnętrzna (blokada)
                    if walls.index(wall) < 2:
                        current_state = GameState.GAME_OVER
                    player_pos.y = old_pos.y

            # Ruch w X
            if pr.is_key_down(pr.KeyboardKey.KEY_A): player_pos.x -= player_speed * dt
            if pr.is_key_down(pr.KeyboardKey.KEY_D): player_pos.x += player_speed * dt
            for wall in walls:
                if pr.check_collision_circle_rec(player_pos, player_radius, wall):
                    if walls.index(wall) < 2:
                        current_state = GameState.GAME_OVER
                    player_pos.x = old_pos.x

        elif current_state == GameState.GAME_OVER:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_R):
                current_state = GameState.MENU

        # --- RYSOWANIE ---
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        if current_state == GameState.MENU:
            pr.draw_text("NEON LABYRINTH", 180, 220, 50, COLOR_CYAN)
            pr.draw_text("Nacisnij [ENTER], aby zaczac", 240, 310, 20, COLOR_WHITE)

        elif current_state == GameState.GAMEPLAY:
            for wall in walls:
                pr.draw_rectangle_rec(wall, COLOR_DARK_GRAY)
            pr.draw_circle_v(player_pos, player_radius, COLOR_CYAN)
            pr.draw_text("Grasz! Unikaj srodkowych scian.", 20, 20, 20, COLOR_GREEN)

        elif current_state == GameState.GAME_OVER:
            pr.draw_text("KONIEC GRY", 240, 220, 50, COLOR_RED)
            pr.draw_text("Nacisnij [R], aby sprobowac ponownie", 210, 310, 20, COLOR_WHITE)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()