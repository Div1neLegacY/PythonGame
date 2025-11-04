import world

class Game:
    def __init__(self):
        self.world_grid = None
        self.regenerate_world()

    def increment_coin_count(self):
        world.CURRENT_COINS_NUM += 1
        world.UI_GRID[world.coins_number[0]][world.coins_number[1]] = str(world.CURRENT_COINS_NUM)

    def regenerate_world(self):
        """Generates a new world and updates the instance variable."""
        world.CURRENT_WORLD_NUM += 1
        self.world_grid = world.generate_random_world(world_num=world.CURRENT_WORLD_NUM, num_of_objects=10, num_of_connections=2, num_of_coins=5, num_of_monsters=3)