import world

class Game:
    def __init__(self):
        self.world_grid = None
        self.regenerate_world()

    # TODO: Add tick and have this class generate new world when player goes out of bounds

    def regenerate_world(self):
        """Generates a new world and updates the instance variable."""
        self.world_grid = world.generate_random_world(num_of_objects=10, num_of_connections=2, num_of_coins=5, num_of_monsters=3)