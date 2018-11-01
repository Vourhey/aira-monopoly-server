import key_gen as KG
import json

class Tx:
    def __init__(self, from_player, to_player, amount, success):
        self.txId = KG.new_tx()
        self.from_player = from_player
        self.to_player = to_player
        self.amount = amount
        self.success = success

    def toString(self):
        body = {
            'txhash': self.txId,
            'from':   self.from_player,
            'to':     self.to_player,
            'value':  self.amount,
            'status': self.success
        }

        return json.dumps(body)

    def __str__(self):
        return 'Tx {}: {{ from: {}, to: {}, amount: {} }}'.format(self.txId, self.from_player, self.to_player, self.amount)
