import pyray as pr


def main():
    # --- Konfiguracja okna ---
    screen_width = 800
    screen_height = 600
    pr.init_window(screen_width, screen_height, "Neon Labyrinth - Lab 11: Kolizje")
    pr.set_target_fps(60)

    # --- Dane Gracza ---
    # Używamy Vector2 dla precyzyjnych obliczeń pozycji
    player_pos = pr.Vector2(100.0, 100.0)
    player_radius = 12.0
    player_speed = 250.0
    player_color = pr.Color(0, 255, 255, 255)  # Cyan

    # --- Lab 11: Definicja Ścian ---
    # Rectangle(x, y, szerokość, wysokość)
    walls = [
        pr.Rectangle(200, 150, 400, 40),  # Przeszkoda górna
        pr.Rectangle(400, 300, 50, 200),  # Przeszkoda pionowa
        pr.Rectangle(0, 0, 800, 10),  # Granica górna
        pr.Rectangle(0, 590, 800, 10),  # Granica dolna
        pr.Rectangle(0, 0, 10, 600),  # Granica lewa
        pr.Rectangle(790, 0, 10, 600)  # Granica prawa
    ]

    while not pr.window_should_close():
        # Delta time zapewnia taką samą prędkość niezależnie od klatek na sekundę
        dt = pr.get_frame_time()

        # Zapisujemy pozycję przed wykonaniem ruchu (do cofnięcia w razie kolizji)
        old_pos = pr.Vector2(player_pos.x, player_pos.y)

        # 1. Obsługa wejścia i kolizji w osi Y
        if pr.is_key_down(pr.KeyboardKey.KEY_W): player_pos.y -= player_speed * dt
        if pr.is_key_down(pr.KeyboardKey.KEY_S): player_pos.y += player_speed * dt

        for wall in walls:
            if pr.check_collision_circle_rec(player_pos, player_radius, wall):
                player_pos.y = old_pos.y  # Cofnij tylko ruch pionowy

        # 2. Obsługa wejścia i kolizji w osi X
        if pr.is_key_down(pr.KeyboardKey.KEY_A): player_pos.x -= player_speed * dt
        if pr.is_key_down(pr.KeyboardKey.KEY_D): player_pos.x += player_speed * dt

        for wall in walls:
            if pr.check_collision_circle_rec(player_pos, player_radius, wall):
                player_pos.x = old_pos.x  # Cofnij tylko ruch poziomy

        # --- Rysowanie ---
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        # Rysowanie wszystkich ścian
        for wall in walls:
            pr.draw_rectangle_rec(wall, pr.DARKGRAY)
            pr.draw_rectangle_lines_ex(wall, 1, pr.GRAY)

        # Rysowanie gracza
        pr.draw_circle_v(player_pos, player_radius, player_color)

        # Teksty pomocnicze
        pr.draw_text("System kolizji", 20, 20, 20, pr.RAYWHITE)
        pr.draw_text("Testuj ślizganie się po krawędziach ścian", 20, 50, 16, pr.GRAY)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()