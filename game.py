import random
import paho.mqtt.publish as publish
from player import Player
from tx import Tx

HOSTNAME = "mqtt.corp.aira.life"
TRANSPORT = "websockets"
PORT = 80

class Game:
    def __init__(self):
        self.players = {}
        self.txs = {}
        self.gameId = random.randint(0, 2**32)
        self.players[0] = Player(True)  # add bank player

    def addPlayer(self):
        p = Player()
        self.players[p.playerId] = p
        print("I'm going to publish")
        publish.single('game/player/joined', str(p.playerId), hostname=HOSTNAME, transport=TRANSPORT, port=PORT)
        print("Done {}".format(p.playerId))
        return p.playerId

    def send(self, from_player, to_player, amount):
        tx = Tx(from_player, to_player, amount)
        print("Transfering from {} to {} amount {}".format(from_player, to_player, amount))
        self.txs[tx.txId] = tx
        self.players[from_player].balance -= amount
        self.players[to_player].balance += amount

        from_balance = self.players[from_player].balance
        to_balance = self.players[to_player].balance
        publish.single('game/player/updatebalance/' + from_player, str(from_balance), hostname=HOSTNAME, transport=TRANSPORT, port=PORT)

        publish.single('game/player/updatebalance/' + to_player, str(to_balance), hostname=HOSTNAME, transport=TRANSPORT, port=PORT)

    def leaveTheGame(self, who):
        del self.players[who]

    def __str__(self):
        return ', '.join("{!s}={!r}".format(key,val) for (key,val) in self.players.items())

    def __repr__(self):
        return ', '.join("{!s}={!r}".format(key,val) for (key,val) in self.players.items())
