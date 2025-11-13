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
            #curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN) # CELL_TEXTURE_NOTHING
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN) # Blue foreground, default background
            curses.init_pair(3, curses.COLOR_WHITE, 137) # Custom orange foreground, black background

    '''
    Mapping function to easily get the curses color pairs for each texture in game
    '''
    def TextureToColorPair(self, texture_constant):
        if texture_constant == world.CELL_TEXTURE_NOTHING:
            return 2
        elif texture_constant == world.CELL_TEXTURE_OBSTACLE:
            return 3
        else:
            return 1 # Default color

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
        # Print out all display items: includes world and UI
        for r, row in enumerate(self.world_grid):
            for c, element in enumerate(row):
                # Calculate position for each element
                y_pos = r
                display_str = f"{element:^{cell_width}}"

                # Check if the position is within screen bounds
                if y_pos < max_y and (c * cell_width) < max_x:
                    self.stdscr_local.addstr(y_pos, c * cell_width, display_str, curses.color_pair(self.TextureToColorPair(element)) | curses.A_BOLD)
        # @TODO: Separate UI section needed because the 3 spacing breaks UI
        
        self.stdscr_local.refresh()
        time.sleep(interval)