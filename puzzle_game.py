import pygame
import sys
import random
import os
import time

pygame.init()

WINDOW_SIZE = 600
MAX_LEVEL = 6
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# ==== POTONG GAMBAR ====
def slice_image(image_path, grid_size):
    img = pygame.image.load(image_path)
    img = pygame.transform.scale(img, (WINDOW_SIZE, WINDOW_SIZE))
    tiles = []
    for y in range(grid_size):
        for x in range(grid_size):
            rect = pygame.Rect(x*(WINDOW_SIZE//grid_size), y*(WINDOW_SIZE//grid_size),
                               WINDOW_SIZE//grid_size, WINDOW_SIZE//grid_size)
            tile = img.subsurface(rect).copy()
            tiles.append(tile)
    return tiles

# ==== BUAT BOARD ====
def create_board(grid_size):
    order = list(range(grid_size * grid_size))
    random.shuffle(order)
    return [order[i:i+grid_size] for i in range(0, len(order), grid_size)]

# ==== GAMBAR BOARD ====
def draw_board(board, tiles, grid_size, level, selected_pos, time_left):
    screen.fill((255, 255, 255))
    tile_size = WINDOW_SIZE // grid_size
    for y in range(grid_size):
        for x in range(grid_size):
            n = board[y][x]
            pos = (x, y)
            rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
            screen.blit(tiles[n], rect.topleft)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            if selected_pos == pos:
                pygame.draw.rect(screen, (255, 0, 0), rect, 3)

    # Teks level & waktu
    level_text = font.render(f"Level {level}", True, (0, 0, 255))
    screen.blit(level_text, (10, 10))

    time_text = font.render(f"Waktu: {int(time_left)}", True, (255, 0, 0))
    screen.blit(time_text, (WINDOW_SIZE - 160, 10))

# ==== CEK ====
def is_adjacent(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)

def is_solved(board):
    expected = list(range(len(board)**2))
    flat = [n for row in board for n in row]
    return flat == expected

# ==== MULAI LEVEL ====
def start_level(level):
    grid_size = level + 1
    image_path = f"Image/Level{level}.jpg"

    if not os.path.exists(image_path):
        print(f"❌ Gambar untuk level {level} tidak ditemukan: {image_path}")
        pygame.quit()
        sys.exit()

    tiles = slice_image(image_path, grid_size)
    board = create_board(grid_size)
    start_time = time.time()
    duration = level * 10  # misal level 1 = 10 detik, dst
    return grid_size, tiles, board, start_time, duration

# ==== OPENING ====
def show_opening_screen():
    screen.fill((200, 200, 255))
    title = big_font.render("Selamat datang di game puzzle ini", True, (0, 0, 100))
    instr = font.render("Klik untuk mulai", True, (0, 0, 0))
    screen.blit(title, (WINDOW_SIZE//2 - title.get_width()//2, WINDOW_SIZE//2 - 40))
    screen.blit(instr, (WINDOW_SIZE//2 - instr.get_width()//2, WINDOW_SIZE//2 + 10))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# ==== GAME OVER ====
def show_game_over():
    screen.fill((255, 0, 0))
    text = big_font.render("⛔ Waktu Habis! Game Over", True, (255, 255, 255))
    screen.blit(text, (WINDOW_SIZE//2 - text.get_width()//2, WINDOW_SIZE//2 - 30))
    pygame.display.flip()
    pygame.time.wait(3000)

# ==== MAIN ====
show_opening_screen()

level = 1
grid_size, tiles, board, start_time, duration = start_level(level)
running = True
win = False
selected = None

while running:
    current_time = time.time()
    time_left = duration - (current_time - start_time)

    if time_left <= 0 and not win:
        show_game_over()
        break

    draw_board(board, tiles, grid_size, level, selected, time_left)
    pygame.display.flip()

    if is_solved(board):
        if level < MAX_LEVEL:
            pygame.time.wait(1000)
            level += 1
            grid_size, tiles, board, start_time, duration = start_level(level)
            selected = None
        else:
            pygame.display.set_caption("🎉 Semua Level Selesai!")
            win = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not win:
            mx, my = pygame.mouse.get_pos()
            tx, ty = mx // (WINDOW_SIZE // grid_size), my // (WINDOW_SIZE // grid_size)
            if selected is None:
                selected = (tx, ty)
            else:
                if is_adjacent(selected, (tx, ty)):
                    sx, sy = selected
                    board[sy][sx], board[ty][tx] = board[ty][tx], board[sy][sx]
                    selected = None
                else:
                    selected = (tx, ty)

    clock.tick(30)

pygame.quit()
sys.exit()
