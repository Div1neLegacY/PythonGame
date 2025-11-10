class Player:

    ATTACK_DIRECTIONS = [[],
                         [(1, 0), (0, 1), (-1, 0), (0, -1)],
                         [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]]
    CURRENT_ATTACK_LVL = 0

    def __init__(self, game_instance, locX, locY):
        self.game_instance = game_instance
        self.locX = locX
        self.locY = locY

    def get_player_loc(self):
        return (self.locX, self.locY)

    def upgrade_attack(self):
        self.CURRENT_ATTACK_LVL += 1
        self.CURRENT_ATTACK_LVL = min(self.CURRENT_ATTACK_LVL, len(self.ATTACK_DIRECTIONS) - 1)
