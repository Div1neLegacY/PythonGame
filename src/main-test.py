import os, random
from pynput import keyboard

import time, threading, curses

CONSTANT_WORLD_SIZE = (15, 15)
CELL_TEXTURE_NOTHING = '_'
CELL_TEXTURE_OBSTACLE = '#'
CELL_TEXTURE_COIN = '@'
CELL_TEXTURE_PLAYER = 'P'
CELL_TEXTURE_MONSTER = 'M'
CELL_TEXTURE_ATTACK = 'X'
CELL_TEXTURE_ATTACK_AFTERMATH = 'x'
WORLD_GRID = [[CELL_TEXTURE_NOTHING for _ in range(CONSTANT_WORLD_SIZE[0])] for _ in range(CONSTANT_WORLD_SIZE[1])]
WORLD_GRID[2][2] = CELL_TEXTURE_PLAYER
WORLD_GRID[2][4] = CELL_TEXTURE_OBSTACLE
WORLD_GRID[1][4] = CELL_TEXTURE_COIN
WORLD_GRID[5][4] = CELL_TEXTURE_COIN

# Spawn 4 monsters in each corner of map
WORLD_GRID[1][1] = CELL_TEXTURE_MONSTER
WORLD_GRID[CONSTANT_WORLD_SIZE[0] - 2][1] = CELL_TEXTURE_MONSTER
WORLD_GRID[1][CONSTANT_WORLD_SIZE[1] - 2] = CELL_TEXTURE_MONSTER
WORLD_GRID[CONSTANT_WORLD_SIZE[0] - 2][CONSTANT_WORLD_SIZE[1] - 2] = CELL_TEXTURE_MONSTER

'''
Initialize the world grid borders to prevent player and monsters
from going offscreen.
'''
# Borders
WORLD_GRID[0][0:CONSTANT_WORLD_SIZE[0]]                          = [CELL_TEXTURE_OBSTACLE] * CONSTANT_WORLD_SIZE[0]
WORLD_GRID[CONSTANT_WORLD_SIZE[0] - 1][0:CONSTANT_WORLD_SIZE[0]] = [CELL_TEXTURE_OBSTACLE] * CONSTANT_WORLD_SIZE[0]
# Loop through rows 0 to 14 (range(15) is exclusive of 15)
for row in WORLD_GRID[0:15]:
    row[0] = CELL_TEXTURE_OBSTACLE
    row[CONSTANT_WORLD_SIZE[0] - 1] = CELL_TEXTURE_OBSTACLE

'''
Input Action / Game Mappings
'''
MOVEMENTS = {"up": (1, 0), "down": (-1, 0), "left": (0, 1), "right": (0, -1)}
MOVEMENTS_MAP = {'w': MOVEMENTS["up"], 's': MOVEMENTS["down"], 'a': MOVEMENTS["left"], 'd': MOVEMENTS["right"]}
ATTACK_DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]

stop_program = threading.Event()

'''
Miscellaneous Game Functions
'''
def clear_terminal():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')

def generate_unequal_random_pair():
    """
    Generates two random floating-point numbers (x, y) in the range [-1, 1]
    such that x is not equal to y.
    """
    x = random.randint(-1, 1)
    y = random.randint(-1, 1)
    while (x == 0) and (y == 0):  # Ensure x and y are a unique combination that is not itself
        y = random.randint(-1, 1)
    return x, y

#def generate_random_world(num_of_monsters, num_of_coins, num_of_exits):


'''
Player Functions
'''
def on_press(key):
    # Quit game
    if key == keyboard.Key.esc:
        print("GAME SHUTTING DOWN...")
        stop_program.set()
        return False
    # Attack
    elif key == keyboard.Key.space:
        player_attack()

    # Move player
    elif key.char in MOVEMENTS_MAP:
        player_move(MOVEMENTS_MAP[key.char][0], MOVEMENTS_MAP[key.char][1])

    display_map(stdscr, 0)
    # Stop the listener after the first key press
    return False

def player_move(move_x, move_y):
    for x in range(CONSTANT_WORLD_SIZE[0]):
        for y in range(CONSTANT_WORLD_SIZE[1]):
            # Is the player moving within the board bounds?
            if WORLD_GRID[x][y] == CELL_TEXTURE_PLAYER and 0 <= (x - move_x) < CONSTANT_WORLD_SIZE[0] and 0 <= (y - move_y) < CONSTANT_WORLD_SIZE[1]:
                # Prevent movement onto obstacles
                if WORLD_GRID[x - move_x][y - move_y] == CELL_TEXTURE_OBSTACLE:
                    continue
                else:
                    # Move player
                    WORLD_GRID[x - move_x][y - move_y] = CELL_TEXTURE_PLAYER
                    WORLD_GRID[x][y] = CELL_TEXTURE_NOTHING
                    return
        
def player_attack():
    attack_locations = []

    for x in range(CONSTANT_WORLD_SIZE[0]):
        for y in range(CONSTANT_WORLD_SIZE[1]):
            # Is the player moving within the board bounds
            if WORLD_GRID[x][y] == CELL_TEXTURE_PLAYER:
                for dir in ATTACK_DIRECTIONS:
                    if 0 <= (x - dir[0]) < CONSTANT_WORLD_SIZE[0] and 0 <= (y - dir[1]) < CONSTANT_WORLD_SIZE[1]:
                        # Add attack texture near player
                        WORLD_GRID[x - dir[0]][y - dir[1]] = CELL_TEXTURE_ATTACK
                        attack_locations.append((x - dir[0], y - dir[1]))
    
    # @TODO Needs to be separate tick, but also modified to not
    # remove player from map
    #
    # Hacked animation sequence for attacks
    display_map(stdscr, 0.15)

    for attack in attack_locations:
        WORLD_GRID[attack[0]][attack[1]] = CELL_TEXTURE_ATTACK_AFTERMATH

    display_map(stdscr, 0.15)

    for attack in attack_locations:
        WORLD_GRID[attack[0]][attack[1]] = CELL_TEXTURE_NOTHING

def random_move_monster():
    random_x, random_y = generate_unequal_random_pair()

    indexes_to_ignore = []

    for x in range(CONSTANT_WORLD_SIZE[0]):
        for y in range(CONSTANT_WORLD_SIZE[1]):
            # Check if we have not already moved this monster
            if {x, y} not in indexes_to_ignore:
                if WORLD_GRID[x][y] == CELL_TEXTURE_MONSTER and 0 <= (x - random_x) < CONSTANT_WORLD_SIZE[0] and 0 <= (y - random_y) < CONSTANT_WORLD_SIZE[1]:
                    # Prevent monster from moving onto obstacles & other monsters
                    if WORLD_GRID[x - random_x][y - random_y] == (CELL_TEXTURE_OBSTACLE or CELL_TEXTURE_MONSTER):
                        indexes_to_ignore.append({x, y})
                        continue

                    # Move monster
                    WORLD_GRID[x - random_x][y - random_y] = CELL_TEXTURE_MONSTER
                    indexes_to_ignore.append({x - random_x, y - random_y})
                    WORLD_GRID[x][y] = CELL_TEXTURE_NOTHING

'''
Updates visual display via curses library.
- stdscr: curses istance
- interval: tick interval to display
'''
def display_map(stdscr, interval):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    # Print the 2D array
    for r_idx, row in enumerate(WORLD_GRID):
        for c_idx, element in enumerate(row):
            # Calculate position for each element
            y_pos = r_idx
            x_pos = c_idx * 2  # Multiply by a factor for spacing between elements

            # Check if the position is within screen bounds
            if y_pos < max_y and x_pos < max_x:
                stdscr.addstr(y_pos, x_pos, str(element))
    
    stdscr.refresh()
    time.sleep(interval)

def tick(stdscr, interval):
    while not stop_program.is_set():
        '''
        Main Game Logic Code
        '''
        clear_terminal()
        display_map(stdscr, interval)

        random_move_monster()
    print("Tick thread stopped.")

def tick_input():
    while not stop_program.is_set():
        # Blocking but runs in separate thread
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        time.sleep(0.01) # Small delay to prevent busy-waiting
    print("Input thread stopped.")

def main(stdscr_local):
    global stdscr
    stdscr = stdscr_local
    clear_terminal()
    
    # Create and run a blocking thread for player input
    input_lock = threading.Lock()
    input_thread = threading.Thread(target=tick_input, args=[])
    
    # Main game tick every 1s
    tick_thread = threading.Thread(target=tick, args=[stdscr, 1])

    input_thread.start()
    tick_thread.start()
    input_thread.join()
    tick_thread.join()

if __name__ == '__main__':
    curses.wrapper(main)
    
    print("Game successfully shutdown.")
        