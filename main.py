import pygame
from pygame.locals import *

from settings import * 

#Pygame Initialization
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

simulation_running = False

#Create 2D Grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = ALIVE_COLOR if grid[row][col] else DEAD_COLOR
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE -1))


def update_grid():
    new_grid = [[grid[row][col] for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            neighbors = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    n_row, n_col = row + i, col + j

                    if 0 <= n_row < GRID_SIZE and 0 < n_col < GRID_SIZE:
                        neighbors += grid[n_row][n_col]
            
            if grid[row][col] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0
            elif neighbors == 3:
                new_grid[row][col] = 1
    
    return new_grid

def handle_click(pos):
    global simulation_running
    x,y = pos

    col, row = x // CELL_SIZE, y // CELL_SIZE
    grid[row][col] = 1 if grid[row][col] == 0 else 0

    if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
        simulation_running = not simulation_running


def draw_button():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_color = DARK_GREEN if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and \
                                 BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT else GREEN
    pygame.draw.rect(screen, button_color, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    
    # Button text
    font = pygame.font.SysFont(None, 30)
    text = font.render("Start Simulation", True, WHITE)
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

#Game Loop
running = True


while running:
    screen.fill((0,0,0))
    draw_grid()
    draw_button()
    
    if simulation_running:
        grid = update_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)
    
    

    pygame.display.flip()
    clock.tick(5)


pygame.quit()



