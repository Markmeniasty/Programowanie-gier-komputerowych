import pyray as pr
from constants import *
from states import GameState
from maze_logic import generate_maze, load_from_grid


def main():
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Neon Labyrinth - Modular Version")
    pr.set_target_fps(60)

    current_state = GameState.MENU
    level_count = 1

    # Pierwsza generacja
    grid = generate_maze(27, 21)
    walls, player_pos, exit_rec = load_from_grid(grid)

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        if current_state == GameState.MENU:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
                current_state = GameState.GAMEPLAY

        elif current_state == GameState.GAMEPLAY:
            old_pos = pr.Vector2(player_pos.x, player_pos.y)

            # Ruch pionowy
            if pr.is_key_down(pr.KeyboardKey.KEY_W): player_pos.y -= PLAYER_SPEED * dt
            if pr.is_key_down(pr.KeyboardKey.KEY_S): player_pos.y += PLAYER_SPEED * dt
            for wall in walls:
                if pr.check_collision_circle_rec(player_pos, PLAYER_RADIUS, wall):
                    player_pos.y = old_pos.y

            # Ruch poziomy
            if pr.is_key_down(pr.KeyboardKey.KEY_A): player_pos.x -= PLAYER_SPEED * dt
            if pr.is_key_down(pr.KeyboardKey.KEY_D): player_pos.x += PLAYER_SPEED * dt
            for wall in walls:
                if pr.check_collision_circle_rec(player_pos, PLAYER_RADIUS, wall):
                    player_pos.x = old_pos.x

            # Następny poziom
            if pr.check_collision_circle_rec(player_pos, PLAYER_RADIUS, exit_rec):
                level_count += 1
                grid = generate_maze(27, 21)
                walls, player_pos, exit_rec = load_from_grid(grid)

        # Rendering
        pr.begin_drawing()
        pr.clear_background(C_BLACK)

        if current_state == GameState.MENU:
            pr.draw_text("NEON MAZE: MODULAR", 180, 280, 40, C_CYAN)
            pr.draw_text("Nacisnij [ENTER] aby startowac", 220, 350, 20, C_WHITE)

        elif current_state == GameState.GAMEPLAY:
            for wall in walls:
                pr.draw_rectangle_rec(wall, C_GRAY)
            pr.draw_rectangle_rec(exit_rec, C_GREEN)
            pr.draw_circle_v(player_pos, PLAYER_RADIUS, C_CYAN)
            pr.draw_text(f"POZIOM: {level_count}", 10, 10, 20, C_WHITE)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()