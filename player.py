import key_gen as KG
import config

class Player:
    def __init__(self, bank=False):
        if bank:
            self.playerId = config.BANK
            self.balance = 999999
        else: 
            self.playerId = KG.new_address()
            self.balance = 150

    def __repr__(self):
        return "balance: {}".format(self.balance)
