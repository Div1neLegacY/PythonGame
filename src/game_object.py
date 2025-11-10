import world
from world import Cardinals

"""
Base class for all game objects.
Handles all general properties and mechanics for each in-game object.
This includes players, obstacles, enemies, etc.
"""

class GameObject:
    def __init__(self, x, y, game_instance, obj_texture):
        self.direction = Cardinals.North
        self.x = x
        self.y = y
        self.game_instance = game_instance
        self.obj_texture = obj_texture

    # @TODO Fill this in later
    '''
    def update(self, delta_time):
        """
        Update the object's state. To be overridden by subclasses.
        """
        pass # Base class has no specific update logic
    '''

    # @TODO Fill this in later
    '''
    def draw(self, screen):
        """
        Draw the object on the screen. To be overridden by subclasses.
        """
        pass # Base class has no specific draw logic
    '''

    def get_location(self):
        return (self.x, self.y)
    
    def get_direction(self):
        return self.direction.value

    def set_direction(self, direction):
        self.direction = direction

    def move(self, x, y):
        # Empty the now "old" position
        self.game_instance.world_grid[self.x][self.y] = world.CELL_TEXTURE_NOTHING

        # When moving object, update the direction based on placement changes
        for cardinal in Cardinals:
            card_x, card_y = cardinal.value
            if ((card_x == (x - self.x)) and (card_y == (y - self.y))):
                self.direction = cardinal

        # Update object location in specified directional x, y movement
        self.x = x
        self.y = y
        # Update visual location on game map
        self.game_instance.world_grid[x][y] = self.obj_texture