import random
import paho.mqtt.publish as publish
from player import Player
from tx import Tx

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
        publish.single('game/player/joined', str(p.playerId), hostname="mqtt.corp.aira.life", transport="websockets", port=80)
        print("Done {}".format(p.playerId))
        return p.playerId

    def send(self, from_player, to_player, amount):
        tx = Tx(from_player, to_player, amount)
        print("Transfering from {} to {} amount {}".format(from_player, to_player, amount))
        # TODO publish 
        self.txs[tx.txId] = tx
        self.players[from_player].balance -= amount
        self.players[to_player].balance += amount

    def leaveTheGame(self, who):
        del self.players[who]

    def __str__(self):
        return ', '.join("{!s}={!r}".format(key,val) for (key,val) in self.players.items())

    def __repr__(self):
        return ', '.join("{!s}={!r}".format(key,val) for (key,val) in self.players.items())
