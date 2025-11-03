import world

class Game:
    def __init__(self):
        self.world_grid = None
        self.regenerate_world()

    def regenerate_world(self):
        """Generates a new world and updates the instance variable."""
        world.CURRENT_WORLD_NUM += 1
        self.world_grid = world.generate_random_world(world_num=world.CURRENT_WORLD_NUM, num_of_objects=10, num_of_connections=2, num_of_coins=5, num_of_monsters=3)