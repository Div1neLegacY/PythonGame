import world, time

class Game:
    def __init__(self):
        self.world_grid = None
        self.regenerate_world()

    def increment_coin_count(self):
        world.CURRENT_COINS_NUM += 1
        world.UI_GRID[world.coins_number[0]][world.coins_number[1]] = str(world.CURRENT_COINS_NUM)

    def get_coin_count():
        return world.CURRENT_COINS_NUM

    def regenerate_world(self):
        """Generates a new world and updates the instance variable."""
        world.CURRENT_WORLD_NUM += 1
        self.world_grid = world.generate_random_world(world_num=world.CURRENT_WORLD_NUM, num_of_objects=10, num_of_connections=2, num_of_coins=5, num_of_monsters=3)

    '''
    Updates map visuals via curses library.
    - stdscr: curses istance
    - interval: tick interval to display
    '''
    def display_map(self, stdscr, interval):
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        # Print out all display items: includes world and UI
        for r, row in enumerate(self.world_grid):
            for c, element in enumerate(row):
                # Calculate position for each element
                y_pos = r
                x_pos = c * 2  # Multiply by a factor for spacing between elements

                # Check if the position is within screen bounds
                if y_pos < max_y and x_pos < max_x:
                    stdscr.addstr(y_pos, x_pos, str(element))

        stdscr.refresh()
        time.sleep(interval)