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

FONT = pygame.font.SysFont("comicsans", 50, bold=True)
MOVE_VELOCITY = 20

class Tile:
    #Colors for each tile value, starting from values 2 to 2048
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
    (237, 197, 63)
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
        #Text is drawn on the rectangle and centered
        window.blit(text, (self.x + (RECT_WIDTH / 2 - text.get_width() / 2), self.y + (RECT_HEIGHT / 2 - text.get_height() / 2)))


    #Sets the position of the tile in the grid based on its x and y coordinates
    def set_position(self, ceil=False):
        if ceil:
            #Rounds up the value 
            self.row = math.ceil((self.y - GRID_Y) / RECT_HEIGHT)
            self.col = math.ceil((self.x - GRID_X) / RECT_WIDTH)
        else:
            #Rounds down the value
            self.row = math.floor((self.y - GRID_Y) / RECT_HEIGHT)
            self.col = math.floor((self.x - GRID_X) / RECT_WIDTH)

    def move(self,delta):
        self.x += delta[0]
        self.y += delta[1]
        #Clamp to grid boundaries
        self.x = max(GRID_X, min(self.x, GRID_X + (COLS - 1) * RECT_WIDTH))
        self.y = max(GRID_Y, min(self.y, GRID_Y + (ROWS - 1) * RECT_HEIGHT))

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

#Displays the UI
def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)
    for tile in tiles.values():
        tile.draw(window)
    
    draw_grid(window)
    pygame.display.update()

#used in the generate_tiles function to generate random available positions for the tiles
def gen_random_position(tiles):
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)
        #Checking if the tile already exists in the dictionary 
        #fString is used to convert the ints into strings
        if f"{row}{col}" not in tiles:
            break

    return row, col

def generate_tiles():
    #Dictionary to hold the tiles in the grid
    #The first digit in the key is the row and the second digit represents the column
    #Dictionary is used for instant access to tiles based on their position, rather than looping a 2D array or list
    tiles = {}
    #Underscore is used to indicate that the value is not used
    #simply loops twice to create two tiles
    for _ in range(2):
        row, col = gen_random_position(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


#This function will handle the movement of the tiles in the grid
#The direction parameter will be used to determine the direction of the movement
#The clock parameter is used to ensure that the movement is smooth and consistent
def mov_tiles(window, tiles, clock, direction):
    updated = True
    #Tells which tiles have already merged
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VELOCITY,0)
        #If col is 0, then it can't move left
        boundary_check = lambda tile: tile.col == 0 and tile.x <= GRID_X
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        #The move velocity will start at 20 and then go to 0, which will allow for the tile to merge when both tiles overlap
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VELOCITY
        #Used to check if the tile can keep on moving to the left, and since the tile on the left has a different value,
        #this lambda function will return False as soon as the border of the tile is reached
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VELOCITY
        ceil = True

    #Essentially the same as the left movement, but signs and inequalities are reversed as needed to make the movement to the right
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        #Moving in positive x direction since we are moving right
        delta = (MOVE_VELOCITY,0)
        #If at the last col, then it can't move right, 
        #and the x position of the tile to the right can't be beyond the boundary of the grid
        boundary_check = lambda tile: tile.col == COLS - 1 and tile.x >= GRID_X + (COLS - 1) * RECT_WIDTH
        #col + 1 because the next tile will be on the right
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VELOCITY
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VELOCITY < next_tile.x 
        ceil = False
        
    #Code is pretty much the same as the left movement, but anything done to col is changed to row and tile.y is utilized
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0,-MOVE_VELOCITY)
        boundary_check = lambda tile: tile.row == 0 and tile.y <= GRID_Y
        get_next_tile = lambda tile: tiles.get(f"{tile.row-1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VELOCITY
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VELOCITY
        ceil = True

    #Code is pretty much the same as the right movement, but anything done to col is changed to row and tile.y is utilized
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0,MOVE_VELOCITY)
        boundary_check = lambda tile: tile.row == ROWS - 1 and tile.y >= GRID_Y + (ROWS - 1) * RECT_HEIGHT
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VELOCITY
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VELOCITY < next_tile.y 
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        #Tiles need to be sorted based on their position in the grid
        #This is done so that the tiles can be moved in the correct order
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)
        #Getting index and each Tile object in the sorted tiles
        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue
            
            #Gets the tile next to the current tile in the specified direction
            next_tile = get_next_tile(tile)
            #Continues to move the tile if it's not at the boundary and there isn't a next tile
            if not next_tile:
                tile.move(delta)

            #Ensures the tiles are the same value to merge and makes sure the tiles are not already merged with another tile
            elif (tile.value == next_tile.value) and (tile not in blocks) and (next_tile not in blocks):
                #Tile keeps on moving until it overlaps the next tile of the same value
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    #Simulates adding the two tiles together as they're always powers of 2
                    next_tile.value *= 2
                    #The current tile is removed and the next tile is added to the blocks set
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            #We know there is a next tile, but the values are different
            #So the tile will keep on moving unyil it reaches the border of the next tile
            elif move_check(tile, next_tile):
                tile.move(delta)
            #No possible move is possible so there wil be no update
            else:
                continue
            #As long as no continue statement is reached, the window will be updated
            tile.set_position(ceil)
            updated = True
        
        update_tiles(window, tiles, sorted_tiles)
    end_move(tiles)

#This function is called at the end of each move to check if the game is over
def end_move(tiles):
    if len(tiles) == 16:
        return "Lost"
    else:
        row, col = gen_random_position(tiles)
        tiles[f"{row}{col}"] = Tile(random.choice([2,4]), row, col)
        return "continue"


#Tiles dictionary is updated so that the tiles that actually exist in the grid are in the dictionary and drawn to show the tiles moving
def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)       
                

#Main game loop
def main(window):
    #Clock object ensures a consistent frame rate
    clock = pygame.time.Clock()
    run = True

    #Generating the tiles at the start of the game
    tiles = generate_tiles()
    while run:
        #Loop is limited to 60 FPS or updates per second
        clock.tick(FPS)
        #Event loop to check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            #Checking if a key is pressed down and if it's one of the arrow keys then the tiles will move if possible
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mov_tiles(window, tiles, clock, "left")
                elif event.key == pygame.K_RIGHT:
                    mov_tiles(window, tiles, clock, "right")
                elif event.key == pygame.K_UP:
                    mov_tiles(window, tiles, clock, "up")
                elif event.key == pygame.K_DOWN:
                    mov_tiles(window, tiles, clock, "down")

        draw(window, tiles)
    #Quits the game if the user closes the window
    pygame.quit()

#Only runs if this file is run directly, not imported
if __name__ == "__main__":
    main(WINDOW)
    #Quitting pygame
    pygame.quit()