import pygame
import random
import math

#Initializing all modules in pygame
pygame.init()

#Defining constants used in the program
FPS = 60
#Window sizing
WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4
#Grid sizing and positioning
GRID_WIDTH, GRID_HEIGHT = 600, 600  # Size of the grid area
GRID_X = (WIDTH - GRID_WIDTH) // 2  # Center horizontally
GRID_Y = HEIGHT - GRID_HEIGHT - 60  # 60px margin from bottom

RECT_WIDTH = GRID_WIDTH // COLS
RECT_HEIGHT = GRID_HEIGHT // ROWS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

#Window size and name
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

FONT = pygame.font.SysFont("ClearSansBold", 60, bold=True)
MOVE_VELOCITY = 20

#High score is saved locally in a text file and if the score is higher than the high score, it is updated
def draw_score(window, high_score):
    pass

class Tile:
    #Colors for each tile value, starting from values 2 to 1024
    COLORS = [
    (237, 229, 218),
    (238, 225, 201),
    (243, 178, 122),
    (246, 150, 101),
    (247, 124, 95),
    (247, 95, 59),
    (237, 208, 115),
    (237, 204, 99),
    (236, 202, 80),
    (237, 197, 63),
    ]

    #Each tile contains its value and its position in the grid
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        #position to draw the tile
        self.x = GRID_X + col * RECT_WIDTH
        self.y = GRID_Y + row * RECT_HEIGHT
    
    #Returns the color of the tile based on its value
    def get_color(self):
        color_index = int(math.log2(self.value)) -1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit()

    def set_position(self, row, col):
        self.row = row
        self.col = col
        self.x = GRID_X + col * RECT_WIDTH
        self.y = GRID_Y + row * RECT_HEIGHT

    def move(self,delta):
        pass

#Drawing the grid and background
def draw_grid(window):
    #Drawing the inner horizontal outlines for the grid
    for row in range(1, ROWS):
        #Offsetting the y position of the lines to match the grid and make it lower
         y = GRID_Y + row * RECT_HEIGHT
         pygame.draw.line(window, OUTLINE_COLOR, (GRID_X, y), (GRID_X + GRID_WIDTH, y), OUTLINE_THICKNESS)
    
    #Drawing the inner vertical outlines for the grid
    for col in range (1, COLS):
        x = GRID_X + col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, GRID_Y), (x, GRID_Y + GRID_HEIGHT), OUTLINE_THICKNESS)
    
    # Outer outline
    pygame.draw.rect(window, OUTLINE_COLOR, (GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT), OUTLINE_THICKNESS)


def draw(window):
    window.fill(BACKGROUND_COLOR)
    draw_grid(window)

    pygame.display.update()




#Main game loop
def main(window):
    #Clock object ensures a consistent frame rate
    clock = pygame.time.Clock()
    run = True

    while run:
        #Loop is limited to 60 FPS or updates per second
        clock.tick(FPS)
        #Event loop to check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        draw(window)
    #Quits the game if the user closes the window
    pygame.quit()

#Only runs if this file is run directly, not imported
if __name__ == "__main__":
    main(WINDOW)
    #Quitting pygame
    pygame.quit()