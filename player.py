import random

class Player:
    def __init__(self, bank=False):
        if bank:
            self.playerId = 0
            self.balance = 999999

        self.playerId = random.randint(1, 2**32)
        self.balance = 150
