import world
from pynput import keyboard
from game_object import GameObject
from projectile import Projectile

'''
Input Action / Game Mappings
'''
MOVEMENTS = {"up": (1, 0), "down": (-1, 0), "left": (0, 1), "right": (0, -1)}
MOVEMENTS_MAP = {'w': MOVEMENTS["up"], 's': MOVEMENTS["down"], 'a': MOVEMENTS["left"], 'd': MOVEMENTS["right"]}

class Player(GameObject):

    ATTACK_DIRECTIONS = [[],
                         [(1, 0), (0, 1), (-1, 0), (0, -1)],
                         [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]]
    CURRENT_ATTACK_LVL = 0

    def __init__(self, game_instance, locX, locY):
        super().__init__(x=locX, y=locY, game_instance=game_instance, obj_texture=world.CELL_TEXTURE_PLAYER)
        self.game_instance = game_instance

    def upgrade_attack(self):
        self.CURRENT_ATTACK_LVL += 1
        self.CURRENT_ATTACK_LVL = min(self.CURRENT_ATTACK_LVL, len(self.ATTACK_DIRECTIONS) - 1)

    def on_press(self, key):
        # Quit game
        if key == keyboard.Key.esc:
            print("GAME SHUTTING DOWN...")
            self.game_instance.stop_program.set()
            return False
        # Attack
        elif key == keyboard.Key.space:
            self.player_attack()
        # Ranged Attack
        elif key.char == 'c':
            self.ranged_attack()
        # Move player
        elif key.char in MOVEMENTS_MAP:
            self.player_move(MOVEMENTS_MAP[key.char][0], MOVEMENTS_MAP[key.char][1])

        self.game_instance.display_map(0)
        # Stop the listener after the first key press
        return False

    def player_move(self, move_x, move_y):
        x, y = self.get_location()
        if self.game_instance.world_grid[x][y] == world.CELL_TEXTURE_PLAYER and 0 <= (x - move_x) < world.CONSTANT_WORLD_SIZE[0] and 0 <= (y - move_y) < world.CONSTANT_WORLD_SIZE[1]:
                    
            # If player is moving over coins, pick up and increment current count
            if self.game_instance.world_grid[x - move_x][y - move_y] == world.CELL_TEXTURE_COIN:
                self.game_instance.increment_coin_count()

                # :: WEAPON UPGRADE GOAL ::
                if (self.game_instance.get_coin_count() % 5 == 0):
                    self.upgrade_attack()
            
            # Prevent movement onto obstacles
            if self.game_instance.world_grid[x - move_x][y - move_y] == world.CELL_TEXTURE_OBSTACLE:
                return
            else:
                # Move player
                self.move(x - move_x, y - move_y)

                # If player is moving out of bounds, assume world transition
                if (x - move_x == 0) or \
                    (x - move_x == world.CONSTANT_WORLD_SIZE[0] - 1) or \
                    (y - move_y == 0) or \
                    (y - move_y == world.CONSTANT_WORLD_SIZE[1] - 1):
                    self.game_instance.regenerate_world()

                    # @TODO Hardcoded for now
                    self.move(2, 2)
                return
            
    def player_attack(self):
        attack_locations = []

        x, y = self.get_location()
        # Is the player moving within the board bounds
        if self.game_instance.world_grid[x][y] == world.CELL_TEXTURE_PLAYER:
            for dir in self.ATTACK_DIRECTIONS[self.CURRENT_ATTACK_LVL]:
                if 0 <= (x - dir[0]) < world.CONSTANT_WORLD_SIZE[0] and 0 <= (y - dir[1]) < world.CONSTANT_WORLD_SIZE[1]:
                    # Add attack texture near player
                    self.game_instance.world_grid[x - dir[0]][y - dir[1]] = world.CELL_TEXTURE_ATTACK
                    attack_locations.append((x - dir[0], y - dir[1]))
        
        # Hacked animation sequence for attacks
        # Doing this here, prevents player from moving during attack.
        self.game_instance.display_map(0.15)

        for attack in attack_locations:
            self.game_instance.world_grid[attack[0]][attack[1]] = world.CELL_TEXTURE_ATTACK_AFTERMATH

        self.game_instance.display_map(0.15)

        for attack in attack_locations:
            self.game_instance.world_grid[attack[0]][attack[1]] = world.CELL_TEXTURE_NOTHING

    def ranged_attack(self):
        x, y = self.get_location()
        dirX, dirY = self.get_direction()

        projectile = Projectile(self.game_instance, x + dirX, y + dirY)

        projectile_time = 5
        for i in range(1, projectile_time):
            try:
                projectile.move(x + (dirX * i), y + (dirY * i))
            except:
                # @TODO Need better way to do this, as this messes with the UI
                # Projectile went off screen
               continue

            # Hacked animation sequence for attacks
            # Doing this here, prevents player from moving during attack.
            self.game_instance.display_map(0.05)

        # Erase final projectile
        x, y = projectile.get_location()
        self.game_instance.world_grid[x][y] = world.CELL_TEXTURE_NOTHING