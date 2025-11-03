import os, world
from pynput import keyboard
from enum import Enum

import time, threading, curses

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
    for x in range(world.CONSTANT_WORLD_SIZE[0]):
        for y in range(world.CONSTANT_WORLD_SIZE[1]):
            # Is the player moving within the board bounds?
            if world.GRID[x][y] == world.CELL_TEXTURE_PLAYER and 0 <= (x - move_x) < world.CONSTANT_WORLD_SIZE[0] and 0 <= (y - move_y) < world.CONSTANT_WORLD_SIZE[1]:
                # Prevent movement onto obstacles
                if world.GRID[x - move_x][y - move_y] == world.CELL_TEXTURE_OBSTACLE:
                    continue
                else:
                    # Move player
                    world.GRID[x - move_x][y - move_y] = world.CELL_TEXTURE_PLAYER
                    world.GRID[x][y] = world.CELL_TEXTURE_NOTHING
                    
                    # If player is moving out of bounds, assume world transition
                    if ((x - move_x) == (0 or world.CONSTANT_WORLD_SIZE[0] - 1)) or ((y - move_y) == (0 or world.CONSTANT_WORLD_SIZE[1] - 1)):
                        world.generate_next_world()
                    return

def player_attack():
    attack_locations = []

    for x in range(world.CONSTANT_WORLD_SIZE[0]):
        for y in range(world.CONSTANT_WORLD_SIZE[1]):
            # Is the player moving within the board bounds
            if world.GRID[x][y] == world.CELL_TEXTURE_PLAYER:
                for dir in ATTACK_DIRECTIONS:
                    if 0 <= (x - dir[0]) < world.CONSTANT_WORLD_SIZE[0] and 0 <= (y - dir[1]) < world.CONSTANT_WORLD_SIZE[1]:
                        # Add attack texture near player
                        world.GRID[x - dir[0]][y - dir[1]] = world.CELL_TEXTURE_ATTACK
                        attack_locations.append((x - dir[0], y - dir[1]))
    
    # Hacked animation sequence for attacks
    # Doing this here, prevents player from moving during attack.
    display_map(stdscr, 0.15)

    for attack in attack_locations:
        world.GRID[attack[0]][attack[1]] = world.CELL_TEXTURE_ATTACK_AFTERMATH

    display_map(stdscr, 0.15)

    for attack in attack_locations:
        world.GRID[attack[0]][attack[1]] = world.CELL_TEXTURE_NOTHING

def random_move_monster():
    random_x, random_y = world.generate_random_pair(min_x=-1, max_x=1, min_y=-1, max_y=1, pairs_to_avoid=[{0, 0}])

    indexes_to_ignore = []

    for x in range(world.CONSTANT_WORLD_SIZE[0]):
        for y in range(world.CONSTANT_WORLD_SIZE[1]):
            # Check if we have not already moved this monster
            if {x, y} not in indexes_to_ignore:
                if world.GRID[x][y] == world.CELL_TEXTURE_MONSTER and 0 <= (x - random_x) < world.CONSTANT_WORLD_SIZE[0] and 0 <= (y - random_y) < world.CONSTANT_WORLD_SIZE[1]:
                    # Prevent monster from moving onto obstacles & other monsters
                    if world.GRID[x - random_x][y - random_y] == (world.CELL_TEXTURE_OBSTACLE or world.CELL_TEXTURE_MONSTER):
                        indexes_to_ignore.append({x, y})
                        continue

                    # Move monster
                    world.GRID[x - random_x][y - random_y] = world.CELL_TEXTURE_MONSTER
                    indexes_to_ignore.append({x - random_x, y - random_y})
                    world.GRID[x][y] = world.CELL_TEXTURE_NOTHING

'''
Updates map visuals via curses library.
- stdscr: curses istance
- interval: tick interval to display
'''
def display_map(stdscr, interval):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    # Print out all display items: includes world and UI
    for r_idx, row in enumerate(world.GRID):
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
    input_thread = threading.Thread(target=tick_input, args=[])
    
    # Main game tick every 1s
    tick_thread = threading.Thread(target=tick, args=[stdscr, 1])

    input_thread.start()
    tick_thread.start()
    input_thread.join()
    tick_thread.join()

if __name__ == '__main__':

    world.generate_random_world(num_of_objects=10, num_of_connections=2, num_of_coins=5, num_of_monsters=3)

    curses.wrapper(main)
    
    print("Game successfully shutdown.")
        