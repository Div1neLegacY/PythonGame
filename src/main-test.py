import os, world
from game import Game
from player import Player
from pynput import keyboard
#from sprite import SpriteApp

import time, threading, curses

'''
Miscellaneous Game Functions
'''
def clear_terminal():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')

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
                        game_instance.stop_program.set()

                    # Move monster
                    game_instance.world_grid[x - random_x][y - random_y] = world.CELL_TEXTURE_MONSTER
                    indexes_to_ignore.append({x - random_x, y - random_y})
                    game_instance.world_grid[x][y] = world.CELL_TEXTURE_NOTHING

def tick(interval):
    while not game_instance.stop_program.is_set():
        '''
        Main Game Logic Code
        '''
        clear_terminal()
        game_instance.display_map(interval)

        random_move_monster()
    print("Tick thread stopped.")

def tick_input():
    while not game_instance.stop_program.is_set():
        # Blocking but runs in separate thread
        with keyboard.Listener(on_press=player_instance.on_press) as listener:
            listener.join()
        time.sleep(0.01) # Small delay to prevent busy-waiting
    print("Input thread stopped.")

def main(stdscr_local):
    global stdscr
    stdscr = stdscr_local
    clear_terminal()
    
    # Initialize Game Instance
    global game_instance
    game_instance = Game(stdscr_local)

    global player_instance
    player_instance = Player(game_instance, 2, 2)

    # Create and run a blocking thread for player input
    input_thread = threading.Thread(target=tick_input, args=[])
    
    # Main game tick
    tick_thread = threading.Thread(target=tick, args=[1])

    input_thread.start()
    tick_thread.start()
    input_thread.join()
    tick_thread.join()

if __name__ == '__main__':
    # Experimental sprite with textual
    #app = SpriteApp()
    #app.run()

    curses.wrapper(main)
    
    print("Game successfully shutdown.")
        