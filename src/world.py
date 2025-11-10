import random
from enum import Enum

# World details
CONSTANT_WORLD_SIZE = (15, 15)
CURRENT_WORLD_NUM = 0
CURRENT_COINS_NUM = 0

class Cardinals(Enum):
    North = (-1, 0)
    East  = (0, 1)
    South = (1, 0)
    West  = (0, -1)

CELL_TEXTURE_NOTHING = '.'
CELL_TEXTURE_OBSTACLE = '#'
CELL_TEXTURE_COIN = '@'
CELL_TEXTURE_PLAYER = 'P'
CELL_TEXTURE_MONSTER = 'M'
CELL_TEXTURE_ATTACK = 'X'
CELL_TEXTURE_ATTACK_AFTERMATH = 'x'
CELL_TEXTURE_PROJECTILE = '*'

# Default initialization, blank UI
UI_GRID = [['' for _ in range(CONSTANT_WORLD_SIZE[0])]]
UI_GRID.append(['*' for _ in range(CONSTANT_WORLD_SIZE[0])])
UI_GRID.append(['' for _ in range(CONSTANT_WORLD_SIZE[0])])
UI_GRID[2][0] = '*'
UI_GRID[2][1] = "WORLD"
world_number = (2, 4)
UI_GRID[2][5] = '|'
UI_GRID[2][6] = 'COINS'
coins_number = (2, 9)
UI_GRID[2][CONSTANT_WORLD_SIZE[0] - 1] = '*'
UI_GRID.append(['*' for _ in range(CONSTANT_WORLD_SIZE[0])])

def generate_random_pair(min_x, max_x, min_y, max_y, pairs_to_avoid):
    """
    Generates two random floating-point numbers (x, y) in a specified range
    avoiding specified pairs
    """
    x = random.randint(min_x, max_x)
    y = random.randint(min_y, max_y)
    while {x, y} in pairs_to_avoid:
        y = random.randint(min_y, max_y)
    return x, y

def generate_items_in_world(map_grid, num_of_items=0, cell_texture='', unavailable_locs=[]):
    for m in range(num_of_items):
        random_x, random_y = generate_random_pair(min_x=1,
                                                  max_x=CONSTANT_WORLD_SIZE[0]-2,
                                                  min_y=1,
                                                  max_y=CONSTANT_WORLD_SIZE[1]-2,
                                                  pairs_to_avoid=unavailable_locs)
        unavailable_locs.append({random_x, random_y})
        map_grid[random_x][random_y] = cell_texture

def generate_random_world(world_num=CURRENT_WORLD_NUM, num_of_monsters=0, num_of_coins=0, num_of_objects=0, num_of_connections=0):
    # Parameter validity checks
    if not (0 <= num_of_connections <= 4):
        raise ValueError("num_of_connections must be between 0 and 4 (inclusive).")

    # Generate a completely blank world
    map_grid = [[CELL_TEXTURE_NOTHING for _ in range(CONSTANT_WORLD_SIZE[0])] for _ in range(CONSTANT_WORLD_SIZE[1])] + UI_GRID

    # Set the world number
    UI_GRID[world_number[0]][world_number[1]] = str(world_num)

    # Set the number of currently collected coins
    UI_GRID[coins_number[0]][coins_number[1]] = str(CURRENT_COINS_NUM)

    # @TODO hardcoded player location
    map_grid[2][2] = CELL_TEXTURE_PLAYER

    # Generate the world borders
    map_grid[0][0:CONSTANT_WORLD_SIZE[0]]                          = [CELL_TEXTURE_OBSTACLE] * CONSTANT_WORLD_SIZE[0]
    map_grid[CONSTANT_WORLD_SIZE[0] - 1][0:CONSTANT_WORLD_SIZE[0]] = [CELL_TEXTURE_OBSTACLE] * CONSTANT_WORLD_SIZE[0]
    # Loop through rows 0 to 14 (range(15) is exclusive of 15)
    for row in map_grid[0:15]:
        row[0] = CELL_TEXTURE_OBSTACLE
        row[CONSTANT_WORLD_SIZE[0] - 1] = CELL_TEXTURE_OBSTACLE

    # Generate all border connections (if needed)
    # Get 'n' randomly unique connections 
    random_connections = random.sample(list(Cardinals), num_of_connections)
    for conn in random_connections:
        match conn:
            case Cardinals.West:
                map_grid[int(CONSTANT_WORLD_SIZE[0] / 2)][0] = CELL_TEXTURE_NOTHING
            case Cardinals.South:
                map_grid[int(CONSTANT_WORLD_SIZE[0] - 1)][int(CONSTANT_WORLD_SIZE[1] / 2)] = CELL_TEXTURE_NOTHING
            case Cardinals.East:
                map_grid[int(CONSTANT_WORLD_SIZE[0] / 2)][int(CONSTANT_WORLD_SIZE[1] - 1)] = CELL_TEXTURE_NOTHING
            case Cardinals.North:
                map_grid[0][int(CONSTANT_WORLD_SIZE[1] / 2)] = CELL_TEXTURE_NOTHING

    # Generate all random objects on map.
    # Avoid replacing player spawn
    already_generated = []
    already_generated.append({2, 2})
    generate_items_in_world(map_grid, num_of_objects, CELL_TEXTURE_OBSTACLE, already_generated)
    
    # Generate all coins randomly on map
    generate_items_in_world(map_grid, num_of_coins, CELL_TEXTURE_COIN, already_generated)

    # Generate all monsters randomly on map
    generate_items_in_world(map_grid, num_of_monsters, CELL_TEXTURE_MONSTER, already_generated)

    return map_grid