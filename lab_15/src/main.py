import pyray as pr
import random
import math
import os
from constants import *
from states import GameState
from maze_logic import generate_maze, load_from_grid, get_random_spawn_points

# --- DYNAMICZNE ŚCIEŻKI ---
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, "..")

# Ścieżka do muzyki
music_path = os.path.join(base_dir, "music", "muzykamenu.wav")

# Ścieżka do folderu ze skorem
score_dir = os.path.join(base_dir, "score")
score_file_path = os.path.join(score_dir, "highscore.txt")


def save_highscore(lvl):
    # Jeśli folder 'score' nie istnieje, stwórz go
    if not os.path.exists(score_dir):
        os.makedirs(score_dir)

    with open(score_file_path, "w") as f:
        f.write(str(lvl))


def load_highscore():
    if os.path.exists(score_file_path):
        with open(score_file_path, "r") as f:
            try:
                return int(f.read())
            except:
                return 1
    return 1

# --- FUNKCJE POMOCNICZE DLA EFEKTÓW ---
def draw_glitch_text(text, x, y, size, color, timer):
    # Główny tekst
    pr.draw_text(text, x, y, size, color)
    # Przesunięte warstwy glitch (pojawiające się co jakiś czas)
    if int(timer * 10) % 5 == 0:
        offset = random.randint(-4, 4)
        pr.draw_text(text, x + offset, y, size, pr.Color(255, 0, 100, 150))
        pr.draw_text(text, x - offset, y, size, pr.Color(0, 255, 255, 150))


def draw_neon_grid(timer):
    # Rysowanie siatki retro-future przesuwającej się w dół
    grid_speed = 60
    offset_y = int(timer * grid_speed) % 40
    color = pr.Color(20, 20, 40, 255)

    for i in range(0, SCREEN_WIDTH + 40, 40):
        pr.draw_line(i, 0, i, SCREEN_HEIGHT, color)
    for j in range(0, SCREEN_HEIGHT + 40, 40):
        pr.draw_line(0, j + offset_y, SCREEN_WIDTH, j + offset_y, color)


def main():
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "NEON LABYRINTH - CYBERPUNK EDITION")
    pr.init_audio_device()
    pr.set_target_fps(60)

    # Audio
    menu_music = None
    if os.path.exists(music_path):
        menu_music = pr.load_music_stream(music_path)
        pr.play_music_stream(menu_music)
        pr.set_music_volume(menu_music, 0.4)

    # Zmienne gry
    current_state = GameState.MENU
    level_count = 1
    highscore = load_highscore()
    timer = 0.0

    # Inicjalizacja poziomu
    grid = generate_maze(27, 21)
    walls, player_pos, exit_rec = load_from_grid(grid)

    # Przeciwnicy i Walka
    num_enemies = 5
    enemy_positions = get_random_spawn_points(grid, num_enemies)
    enemy_dirs = [pr.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(num_enemies)]
    bullets = []
    last_move_dir = pr.Vector2(1, 0)

    # Cząsteczki tła (Menu)
    particles = [{"pos": pr.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                  "speed": random.uniform(10, 30)} for _ in range(30)]

    while not pr.window_should_close():
        if menu_music: pr.update_music_stream(menu_music)
        dt = pr.get_frame_time()
        timer += dt

        if current_state == GameState.MENU:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
                current_state = GameState.GAMEPLAY
                level_count = 1
                grid = generate_maze(27, 21)
                walls, player_pos, exit_rec = load_from_grid(grid)
                enemy_positions = get_random_spawn_points(grid, 5)
                enemy_dirs = [pr.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(5)]
                bullets = []

        elif current_state == GameState.GAMEPLAY:
            # --- LOGIKA RUCHU (Standardowa) ---
            move_input = pr.Vector2(0, 0)
            if pr.is_key_down(pr.KeyboardKey.KEY_W): move_input.y = -1
            if pr.is_key_down(pr.KeyboardKey.KEY_S): move_input.y = 1
            if pr.is_key_down(pr.KeyboardKey.KEY_A): move_input.x = -1
            if pr.is_key_down(pr.KeyboardKey.KEY_D): move_input.x = 1
            if move_input.x != 0 or move_input.y != 0: last_move_dir = pr.Vector2(move_input.x, move_input.y)

            old_p_pos = pr.Vector2(player_pos.x, player_pos.y)
            player_pos.y += move_input.y * PLAYER_SPEED * dt
            for wall in walls:
                if pr.check_collision_circle_rec(player_pos, PLAYER_RADIUS, wall): player_pos.y = old_p_pos.y
            player_pos.x += move_input.x * PLAYER_SPEED * dt
            for wall in walls:
                if pr.check_collision_circle_rec(player_pos, PLAYER_RADIUS, wall): player_pos.x = old_p_pos.x

            # --- STRZELANIE I WROGOWIE ---
            if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
                bullets.append({"pos": pr.Vector2(player_pos.x, player_pos.y),
                                "dir": pr.Vector2(last_move_dir.x, last_move_dir.y)})

            for b in bullets[:]:
                b["pos"].x += b["dir"].x * BULLET_SPEED * dt
                b["pos"].y += b["dir"].y * BULLET_SPEED * dt
                for wall in walls:
                    if pr.check_collision_circle_rec(b["pos"], BULLET_RADIUS, wall):
                        if b in bullets: bullets.remove(b)
                        break
                for i in range(len(enemy_positions) - 1, -1, -1):
                    edx, edy = b["pos"].x - enemy_positions[i].x, b["pos"].y - enemy_positions[i].y
                    if (edx * edx + edy * edy) ** 0.5 < (BULLET_RADIUS + ENEMY_RADIUS):
                        enemy_positions.pop(i);
                        enemy_dirs.pop(i)
                        if b in bullets: bullets.remove(b)
                        break

            for i in range(len(enemy_positions)):
                e_pos = enemy_positions[i]
                pdx, pdy = player_pos.x - e_pos.x, player_pos.y - e_pos.y
                dist = (pdx * pdx + pdy * pdy) ** 0.5
                if dist < DETECTION_RADIUS:
                    enemy_dirs[i] = pr.Vector2(pdx / dist, pdy / dist) if dist != 0 else enemy_dirs[i]
                    speed = ENEMY_SPEED * 1.2
                else:
                    speed = ENEMY_SPEED
                old_e_pos = pr.Vector2(e_pos.x, e_pos.y)
                e_pos.x += enemy_dirs[i].x * speed * dt
                e_pos.y += enemy_dirs[i].y * speed * dt
                for wall in walls:
                    if pr.check_collision_circle_rec(e_pos, ENEMY_RADIUS, wall):
                        if dist >= DETECTION_RADIUS: enemy_dirs[i].x *= -1; enemy_dirs[i].y *= -1
                        e_pos.x, e_pos.y = old_e_pos.x, old_e_pos.y;
                        break
                if dist < (PLAYER_RADIUS + ENEMY_RADIUS):
                    if level_count > highscore: highscore = level_count; save_highscore(highscore)
                    current_state = GameState.MENU

            if pr.check_collision_circle_rec(player_pos, PLAYER_RADIUS, exit_rec):
                level_count += 1
                grid = generate_maze(27, 21);
                walls, player_pos, exit_rec = load_from_grid(grid)
                enemy_positions = get_random_spawn_points(grid, 4 + level_count)
                enemy_dirs = [pr.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) for _ in
                              range(len(enemy_positions))]
                bullets = []

        # --- RENDERING ---
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        if current_state == GameState.MENU:
            draw_neon_grid(timer)

            # Cząsteczki
            for p in particles:
                p["pos"].y += p["speed"] * dt
                if p["pos"].y > SCREEN_HEIGHT: p["pos"].y = -10
                pr.draw_circle_v(p["pos"], 1, pr.Color(0, 255, 255, 100))

            # Tytuł z efektem Glitch
            draw_glitch_text("NEON LABYRINTH", SCREEN_WIDTH // 2 - 250, 150, 60, pr.SKYBLUE, timer)

            # Highscore w neonowej ramce
            pr.draw_rectangle_lines_ex(pr.Rectangle(SCREEN_WIDTH // 2 - 120, 230, 240, 40), 2, pr.MAGENTA)
            pr.draw_text(f"HIGH SCORE: LVL {highscore}", SCREEN_WIDTH // 2 - 105, 240, 20, pr.MAGENTA)

            # Przyciski / Instrukcja
            pulse = (math.sin(timer * 5) + 1) / 2
            pr.draw_text("PRESS [ENTER] TO BOOT SYSTEM", SCREEN_WIDTH // 2 - 180, 400, 22,
                         pr.Color(255, 255, 255, int(150 + 105 * pulse)))
            pr.draw_text("WSAD - NAVIGATE | SPACE - PURGE ENEMIES", SCREEN_WIDTH // 2 - 190, 450, 16, pr.GRAY)

        elif current_state == GameState.GAMEPLAY:
            # (Render Gameplay bez zmian, by utrzymać wydajność)
            for wall in walls:
                dx, dy = player_pos.x - (wall.x + TILE_SIZE / 2), player_pos.y - (wall.y + TILE_SIZE / 2)
                d = (dx * dx + dy * dy) ** 0.5
                if d < FOG_RADIUS:
                    alpha = int(255 * (1.0 - (d / FOG_RADIUS)))
                    pr.draw_rectangle_rec(wall, pr.Color(30, 30, 50, alpha))
                    pr.draw_rectangle_lines_ex(wall, 1, pr.Color(0, 255, 255, alpha // 4))

            for b in bullets: pr.draw_circle_v(b["pos"], BULLET_RADIUS, pr.YELLOW)
            for e_pos in enemy_positions:
                dx, dy = player_pos.x - e_pos.x, player_pos.y - e_pos.y
                if (dx * dx + dy * dy) ** 0.5 < FOG_RADIUS:
                    pr.draw_circle_v(e_pos, ENEMY_RADIUS, pr.RED)

            pr.draw_rectangle_rec(exit_rec, pr.GREEN)
            pr.draw_circle_v(player_pos, PLAYER_RADIUS, pr.SKYBLUE)
            pr.draw_text(f"LVL: {level_count}", 20, 20, 20, pr.WHITE)

        pr.end_drawing()

    if menu_music: pr.unload_music_stream(menu_music)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()