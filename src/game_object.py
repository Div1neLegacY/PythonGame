from world import Cardinals

"""
Base class for all game objects.
Handles all general properties and mechanics for each in-game object.
This includes players, obstacles, enemies, etc.
"""

class GameObject:
    def __init__(self, x, y):
        self.direction = Cardinals.North
        self.x = x
        self.y = y

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
        # When moving object, update the direction based on placement changes
        for cardinal in Cardinals:
            card_x, card_y = cardinal.value
            if ((card_x == (x - self.x)) and (card_y == (y - self.y))):
                self.direction = cardinal
        # Move object in specified directional x, y movement
        self.x = x
        self.y = y