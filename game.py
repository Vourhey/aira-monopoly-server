import random
from player import Player
from tx import Tx
import config
from approve import ApproveThread
from mqtt_utils import publish_single, publish_multiple


class Game:
    def __init__(self):
        self.players = {}
        self.txs = {}
        self.gameId = random.randint(0, 2**32)

        bankPlayer = Player(True)
        self.players[bankPlayer.playerId] = bankPlayer  # add bank player

    def addPlayer(self):
        p = Player()
        self.players[p.playerId] = p

        topic = 'game/{}/player/joined'.format(self.gameId)
        publish_single(topic, str(p.playerId))
        return p.playerId

    def send(self, from_player, to_player, amount):
        print("Transfering from {} to {} amount {}".format(from_player, to_player, amount))

        if from_player == config.BANK: 
            print("Hey bank!")
            athread = ApproveThread(self.gameId, len(self.players))
            athread.start()
            return

        if self.players[from_player].balance - amount >= 0:
            self.players[from_player].balance -= amount
            self.players[to_player].balance += amount    
            success = True
        else:
            success = False

        tx = Tx(from_player, to_player, amount, success)
        self.txs[tx.txId] = tx

        msgs_from = [
            {
                'topic': 'game/{}/player/{}'.format(self.gameId, from_player),
                'payload': str(self.players[from_player].balance)
            },
            {
                'topic': 'game/{}/txs/{}'.format(self.gameId, from_player),
                'payload': tx.toString()
            }
        ]
        publish_multiple(msgs_from)
        
        msgs_to = [
            {
                'topic': 'game/{}/player/{}'.format(self.gameId, to_player),
                'payload': str(self.players[to_player].balance)
            },
            {
                'topic': 'game/{}/txs/{}'.format(self.gameId, to_player),
                'payload': tx.toString()
            }
        ]
        publish_multiple(msgs_to)

    def leaveTheGame(self, who):
        del self.players[who]

    def __str__(self):
        return ', '.join("{!s}={!r}".format(key,val) for (key,val) in self.players.items())

    def __repr__(self):
        return ', '.join("{!s}={!r}".format(key,val) for (key,val) in self.players.items())
