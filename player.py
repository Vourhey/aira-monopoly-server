import random

class Player:
    def __init__(self, bank=False):
        if bank:
            self.playerId = 0
            self.balance = 999999
        else: 
            self.playerId = random.randint(1, 2**32)
            self.balance = 150

    def __repr__(self):
        return "balance: {}".format(self.balance)
