import world, time, threading, curses

class Game:
    def __init__(self, stdscr_local):
        self.world_grid = None
        self.regenerate_world()
        self.stop_program = threading.Event()
        self.stdscr_local = stdscr_local
        self.define_texture_colors()

    def define_texture_colors(self):
        # Define a custom color (if terminal supports it)
        curses.start_color()
        if curses.can_change_color():
            # Define color pairs
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN) # Blue foreground, default background
            curses.init_pair(3, curses.COLOR_WHITE, 137) # Custom orange foreground, black background
            curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
            curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
            curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

    def increment_coin_count(self):
        world.CURRENT_COINS_NUM += 1
        world.UI_GRID[world.coins_number[0]][world.coins_number[1]] = str(world.CURRENT_COINS_NUM)

    def get_coin_count(self):
        return world.CURRENT_COINS_NUM

    def regenerate_world(self):
        """Generates a new world and updates the instance variable."""
        world.CURRENT_WORLD_NUM += 1
        self.world_grid = world.generate_random_world(world_num=world.CURRENT_WORLD_NUM, num_of_objects=10, num_of_connections=2, num_of_coins=5, num_of_monsters=3)

    '''
    Updates map visuals via curses library.
    - interval: tick interval to display
    '''
    def display_map(self, interval):
        self.stdscr_local.clear()
        cell_width = 3
        max_y, max_x = self.stdscr_local.getmaxyx()
        current_y = 0
        # Print out the world map
        for r, row in enumerate(self.world_grid):
            y_pos = r
            for c, element in enumerate(row):
                display_str = f"{element:^{cell_width}}"
                # Check if the position is within screen bounds
                if y_pos < max_y and (c * cell_width) < max_x:
                    self.stdscr_local.addstr(y_pos, c * cell_width, display_str, curses.color_pair(world.TextureToColorPair(element)) | curses.A_DIM)
            # Keep this position update for UI later
            current_y = y_pos
        
        # Print out UI separate from the world map
        for r, row in enumerate(world.UI_GRID):
            for c, element in enumerate(row):
                y_pos = r + current_y
                x_pos = c * 2
                # Check if the position is within screen bounds
                if y_pos < max_y and (c * cell_width) < max_x:
                    self.stdscr_local.addstr(y_pos, x_pos, str(element))
        self.stdscr_local.refresh()
        time.sleep(interval)