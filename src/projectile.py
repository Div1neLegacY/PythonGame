from world import CELL_TEXTURE_PROJECTILE
from game_object import GameObject

class Projectile(GameObject):
    def __init__(self, game_instance, x, y):
        super().__init__(x=x, y=y, game_instance=game_instance, obj_texture=CELL_TEXTURE_PROJECTILE)