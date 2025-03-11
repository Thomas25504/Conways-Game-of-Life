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
reverse_colors = False
mouse_held = False
show_grid_lines = False
text_color = DEAD_COLOR

#Create 2D Grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = ALIVE_COLOR if grid[row][col] else DEAD_COLOR
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if show_grid_lines:
                pygame.draw.rect(screen, GRID_LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

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

                    if 0 <= n_row < GRID_SIZE and 0 <= n_col < GRID_SIZE:
                        neighbors += grid[n_row][n_col]
            
            if grid[row][col] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0
            elif neighbors == 3:
                new_grid[row][col] = 1
    
    return new_grid

def handle_click(pos):
    x, y = pos
    col, row = x // CELL_SIZE, y // CELL_SIZE
    if not mouse_held:
        grid[row][col] = 1 if grid[row][col] == 0 else 0

def handle_mouse_hold(pos):
    global FPS
    x, y = pos
    col, row = x // CELL_SIZE, y // CELL_SIZE
    
    if grid[row][col] == 0:
        grid[row][col] = 1

def handle_button_click(pos):
    global simulation_running
    global grid
    global reverse_colors
    global show_grid_lines
    global ALIVE_COLOR, DEAD_COLOR
    global GRID_SIZE, CELL_SIZE

    x, y = pos
    if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
        simulation_running = not simulation_running
    
    if CLEARBUTTON_X <= x <= CLEARBUTTON_X + CLEARBUTTON_WIDTH and CLEARBUTTON_Y <= y <= CLEARBUTTON_Y + CLEARBUTTON_HEIGHT:
        grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        simulation_running = False
    
    if REVERSECOLORS_X <= x <= REVERSECOLORS_X + REVERSECOLORS_WIDTH and REVERSECOLORS_Y <= y <= REVERSECOLORS_Y + REVERSECOLORS_HEIGHT:
        reverse_colors = not reverse_colors
        ALIVE_COLOR, DEAD_COLOR = DEAD_COLOR, ALIVE_COLOR

    if GRIDLINES_X <= x <= GRIDLINES_X + GRIDLINES_WIDTH and GRIDLINES_Y <= y <= GRIDLINES_Y + GRIDLINES_HEIGHT:
        show_grid_lines = not show_grid_lines

    if GRID_SIZE_BUTTON_X <= x <= GRID_SIZE_BUTTON_X + GRID_SIZE_BUTTON_WIDTH and GRID_SIZE_BUTTON_Y <= y <= GRID_SIZE_BUTTON_Y + GRID_SIZE_BUTTON_HEIGHT:
        if GRID_SIZE == GRID_SIZE_SMALL:
            GRID_SIZE = GRID_SIZE_MEDIUM
        elif GRID_SIZE == GRID_SIZE_MEDIUM:
            GRID_SIZE = GRID_SIZE_LARGE
        else:
            GRID_SIZE = GRID_SIZE_SMALL
        CELL_SIZE = WIDTH // GRID_SIZE
        grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_button():
    global text_color

    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_color = DARK_GREEN if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and \
                                 BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT else GREEN
    
    clearbutton_color = DARK_RED if CLEARBUTTON_X <= mouse_x <= CLEARBUTTON_X + CLEARBUTTON_WIDTH and \
                                   CLEARBUTTON_Y <= mouse_y <= CLEARBUTTON_Y + CLEARBUTTON_HEIGHT else RED
    
    reverscolor_button = DEAD_COLOR if REVERSECOLORS_X <= mouse_x <= REVERSECOLORS_X + REVERSECOLORS_WIDTH and \
                                    REVERSECOLORS_Y <= mouse_y <= REVERSECOLORS_Y + REVERSECOLORS_HEIGHT else ALIVE_COLOR
    
    gridlines_button = DARK_BLUE if GRIDLINES_X <= mouse_x <= GRIDLINES_X + GRIDLINES_WIDTH and \
                                  GRIDLINES_Y <= mouse_y <= GRIDLINES_Y + GRIDLINES_HEIGHT else BLUE
    
    grid_size_button_color = GREY if GRID_SIZE_BUTTON_X <= mouse_x <= GRID_SIZE_BUTTON_X + GRID_SIZE_BUTTON_WIDTH and \
                                      GRID_SIZE_BUTTON_Y <= mouse_y <= GRID_SIZE_BUTTON_Y + GRID_SIZE_BUTTON_HEIGHT else DARG_GREY
    
    text_color = ALIVE_COLOR if REVERSECOLORS_X <= mouse_x <= REVERSECOLORS_X + REVERSECOLORS_WIDTH and \
                                    REVERSECOLORS_Y <= mouse_y <= REVERSECOLORS_Y + REVERSECOLORS_HEIGHT else DEAD_COLOR
    
    pygame.draw.rect(screen, button_color, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, clearbutton_color, (CLEARBUTTON_X, CLEARBUTTON_Y, CLEARBUTTON_WIDTH, CLEARBUTTON_HEIGHT))
    pygame.draw.rect(screen, reverscolor_button, (REVERSECOLORS_X, REVERSECOLORS_Y, REVERSECOLORS_WIDTH, REVERSECOLORS_HEIGHT))
    pygame.draw.rect(screen, gridlines_button, (GRIDLINES_X, GRIDLINES_Y, GRIDLINES_WIDTH, GRIDLINES_HEIGHT))
    pygame.draw.rect(screen, grid_size_button_color, (GRID_SIZE_BUTTON_X, GRID_SIZE_BUTTON_Y, GRID_SIZE_BUTTON_WIDTH, GRID_SIZE_BUTTON_HEIGHT))
    
    # Button text
    font = pygame.font.SysFont(None, 30)
    button_text = "Stop Simulation" if simulation_running else "Start Simulation"
    text = font.render(button_text, True, WHITE)
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

    clearbutton_text = "Clear"
    text = font.render(clearbutton_text, True, WHITE)
    text_rect = text.get_rect(center=(CLEARBUTTON_X + BUTTON_WIDTH // 2, CLEARBUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

    reverscolor_text = "Reverse Colors"
    text = font.render(reverscolor_text, True, text_color)
    text_rect = text.get_rect(center=(REVERSECOLORS_X + BUTTON_WIDTH // 2, REVERSECOLORS_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

    gridlines_text = "Show Grid Lines" if not show_grid_lines else "Hide Grid Lines"
    text = font.render(gridlines_text, True, WHITE)
    text_rect = text.get_rect(center=(GRIDLINES_X + BUTTON_WIDTH // 2, GRIDLINES_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

    grid_size_text = "Grid Size: Small" if GRID_SIZE == GRID_SIZE_SMALL else "Grid Size: Medium" if GRID_SIZE == GRID_SIZE_MEDIUM else "Grid Size: Large"
    text = font.render(grid_size_text, True, WHITE)
    text_rect = text.get_rect(center=(GRID_SIZE_BUTTON_X + GRID_SIZE_BUTTON_WIDTH // 2, GRID_SIZE_BUTTON_Y + GRID_SIZE_BUTTON_HEIGHT // 2))
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
            mouse_held = True
            handle_click(event.pos)
            handle_button_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False

    if mouse_held:
        FPS = 60
        handle_mouse_hold(pygame.mouse.get_pos())
    else:
        FPS = 10
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()