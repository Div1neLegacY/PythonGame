from world import Cardinals, CELL_TEXTURE_PROJECTILE
from game_object import GameObject

class Projectile(GameObject):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)