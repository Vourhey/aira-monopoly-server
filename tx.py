import random

class Tx:
    def __init__(self, from_player, to_player, amount):
        self.txId = random.randint(0, 2**32)
        self.from_player = from_player
        self.to_player = to_player
        self.amount = amount

    def __str__(self):
        return 'Tx {}: {{ from: {}, to: {}, amount: {} }}'.format(self.txId, self.from_player, self.to_player, self.amount)
