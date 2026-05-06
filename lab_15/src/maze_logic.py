import pyray as pr
import random
from constants import TILE_SIZE


def generate_maze(width, height):
    grid = [["#" for _ in range(width)] for _ in range(height)]
    stack = [(1, 1)]
    grid[1][1] = "P"
    visited = {(1, 1)}
    last_pos = (1, 1)

    while stack:
        cx, cy = stack[-1]
        neighbors = []
        for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and (nx, ny) not in visited:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            grid[cy + (ny - cy) // 2][cx + (nx - cx) // 2] = " "
            grid[ny][nx] = " "
            visited.add((nx, ny))
            stack.append((nx, ny))
            last_pos = (nx, ny)
        else:
            stack.pop()

    ex, ey = last_pos
    grid[ey][ex] = "E"
    return grid


def load_from_grid(grid):
    walls = []
    player_start = pr.Vector2(0, 0)
    exit_rec = pr.Rectangle(0, 0, 0, 0)

    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            rect = pr.Rectangle(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if char == "#":
                walls.append(rect)
            elif char == "P":
                player_start = pr.Vector2(rect.x + TILE_SIZE / 2, rect.y + TILE_SIZE / 2)
            elif char == "E":
                exit_rec = rect
    return walls, player_start, exit_rec