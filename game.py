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
        self.from_player = from_player
        self.to_player = to_player
        self.amount = amount

        if from_player == config.BANK:
            print("Hey bank!")
            amount_of_approves = len(self.players) - 2
        else:
            amount_of_approves = 0

        athread = ApproveThread(self.gameId, amount_of_approves, self.transfer, to_player, amount)
        athread.start()

    # this is a callback for the ApproveThread
    def transfer(self, approved):
        print("Inside callback\nfrom_player is {} to_player is {} and amount is {} approved {}".format(self.from_player, self.to_player, self.amount, approved))

        if approved and self.players[self.from_player].balance - self.amount >= 0:

            self.players[self.from_player].balance -= self.amount
            self.players[self.to_player].balance += self.amount
            success = True
        else:
            success = False

        tx = Tx(self.from_player, self.to_player, self.amount, success)
        self.txs[tx.txId] = tx

        msgs_from = [
            {
                'topic': 'game/{}/balance/{}'.format(self.gameId, self.from_player),
                'payload': str(self.players[self.from_player].balance)
            },
            {
                'topic': 'game/{}/txs/{}'.format(self.gameId, self.from_player),
                'payload': tx.toString()
            }
        ]
        publish_multiple(msgs_from)

        msgs_to = [
            {
                'topic': 'game/{}/balance/{}'.format(self.gameId, self.to_player),
                'payload': str(self.players[self.to_player].balance)
            },
            {
                'topic': 'game/{}/txs/{}'.format(self.gameId, self.to_player),
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
