import os, world, player
from game import Game
from player import Player
from pynput import keyboard

import time, threading, curses

'''
Input Action / Game Mappings
'''
MOVEMENTS = {"up": (1, 0), "down": (-1, 0), "left": (0, 1), "right": (0, -1)}
MOVEMENTS_MAP = {'w': MOVEMENTS["up"], 's': MOVEMENTS["down"], 'a': MOVEMENTS["left"], 'd': MOVEMENTS["right"]}

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
# @TODO Move into player.py
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

    game_instance.display_map(stdscr, 0)
    # Stop the listener after the first key press
    return False

# @TODO Move into player.py
def player_move(move_x, move_y):
    x, y = player_instance.get_player_loc()
    if game_instance.world_grid[x][y] == world.CELL_TEXTURE_PLAYER and 0 <= (x - move_x) < world.CONSTANT_WORLD_SIZE[0] and 0 <= (y - move_y) < world.CONSTANT_WORLD_SIZE[1]:
                
        # If player is moving over coins, pick up and increment current count
        if game_instance.world_grid[x - move_x][y - move_y] == world.CELL_TEXTURE_COIN:
            game_instance.increment_coin_count()
            # @TODO Why is this broken?
            #if (game_instance.get_coin_count() == 5):
                #player_instance.upgrade_attack()

        
        # Prevent movement onto obstacles
        if game_instance.world_grid[x - move_x][y - move_y] == world.CELL_TEXTURE_OBSTACLE:
            return
        else:
            # Move player
            player_instance.locX = x - move_x
            player_instance.locY = y - move_y
            game_instance.world_grid[x - move_x][y - move_y] = world.CELL_TEXTURE_PLAYER
            game_instance.world_grid[x][y] = world.CELL_TEXTURE_NOTHING

            # If player is moving out of bounds, assume world transition
            if (x - move_x == 0) or \
                (x - move_x == world.CONSTANT_WORLD_SIZE[0] - 1) or \
                (y - move_y == 0) or \
                (y - move_y == world.CONSTANT_WORLD_SIZE[1] - 1):
                game_instance.regenerate_world()

                # @TODO Hardcoded for now
                player_instance.locX = 2
                player_instance.locY = 2
            return
                
# @TODO Move into player.py
def player_attack():
    attack_locations = []

    x, y = player_instance.get_player_loc()
    # Is the player moving within the board bounds
    if game_instance.world_grid[x][y] == world.CELL_TEXTURE_PLAYER:
        for dir in player_instance.ATTACK_DIRECTIONS[2]:
            if 0 <= (x - dir[0]) < world.CONSTANT_WORLD_SIZE[0] and 0 <= (y - dir[1]) < world.CONSTANT_WORLD_SIZE[1]:
                # Add attack texture near player
                game_instance.world_grid[x - dir[0]][y - dir[1]] = world.CELL_TEXTURE_ATTACK
                attack_locations.append((x - dir[0], y - dir[1]))
    
    # Hacked animation sequence for attacks
    # Doing this here, prevents player from moving during attack.
    game_instance.display_map(stdscr, 0.15)

    for attack in attack_locations:
        game_instance.world_grid[attack[0]][attack[1]] = world.CELL_TEXTURE_ATTACK_AFTERMATH

    game_instance.display_map(stdscr, 0.15)

    for attack in attack_locations:
        game_instance.world_grid[attack[0]][attack[1]] = world.CELL_TEXTURE_NOTHING

def random_move_monster():
    random_x, random_y = world.generate_random_pair(min_x=-1, max_x=1, min_y=-1, max_y=1, pairs_to_avoid=[{0, 0}])

    indexes_to_ignore = []

    for x in range(world.CONSTANT_WORLD_SIZE[0]):
        for y in range(world.CONSTANT_WORLD_SIZE[1]):
            # Check if we have not already moved this monster
            if {x, y} not in indexes_to_ignore:
                if game_instance.world_grid[x][y] == world.CELL_TEXTURE_MONSTER and 0 <= (x - random_x) < world.CONSTANT_WORLD_SIZE[0] and 0 <= (y - random_y) < world.CONSTANT_WORLD_SIZE[1]:
                    # Prevent monster from moving onto obstacles & other monsters
                    if game_instance.world_grid[x - random_x][y - random_y] == (world.CELL_TEXTURE_OBSTACLE or world.CELL_TEXTURE_MONSTER):
                        indexes_to_ignore.append({x, y})
                        continue

                    # If monster if moving onto player, initial GAME OVER status
                    if game_instance.world_grid[x - random_x][y - random_y] == world.CELL_TEXTURE_PLAYER:
                        print("GAME OVER")
                        stop_program.set()

                    # Move monster
                    game_instance.world_grid[x - random_x][y - random_y] = world.CELL_TEXTURE_MONSTER
                    indexes_to_ignore.append({x - random_x, y - random_y})
                    game_instance.world_grid[x][y] = world.CELL_TEXTURE_NOTHING

def tick(stdscr, interval):
    while not stop_program.is_set():
        '''
        Main Game Logic Code
        '''
        clear_terminal()
        game_instance.display_map(stdscr, interval)

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
    
    # Main game tick
    tick_thread = threading.Thread(target=tick, args=[stdscr, 1])

    input_thread.start()
    tick_thread.start()
    input_thread.join()
    tick_thread.join()

if __name__ == '__main__':
    global game_instance
    game_instance = Game()

    global player_instance
    player_instance = Player(game_instance, 2, 2)

    curses.wrapper(main)
    
    print("Game successfully shutdown.")
        