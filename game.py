import random
import paho.mqtt.publish as publish
from player import Player
from tx import Tx
import ssl

HOSTNAME = "mqtt.corp.aira.life"
TRANSPORT = "websockets"
PORT = 80

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
        publish.single(topic, str(p.playerId), hostname=HOSTNAME, transport=TRANSPORT, port=PORT, tls={'ca_certs': '/etc/nginx/ssl/mqtt.corp.aira.life/ca.cer', 'cert_reqs':ssl.CERT_NONE})
        return p.playerId

    def send(self, from_player, to_player, amount):
        print("Transfering from {} to {} amount {}".format(from_player, to_player, amount))

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
        publish.multiple(msgs_from, hostname=HOSTNAME, transport=TRANSPORT, port=PORT, tls={'ca_certs': '/etc/nginx/ssl/mqtt.corp.aira.life/ca.cer', 'cert_reqs':ssl.CERT_NONE})
        
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
        publish.multiple(msgs_to, hostname=HOSTNAME, transport=TRANSPORT, port=PORT, tls={'ca_certs': '/etc/nginx/ssl/mqtt.corp.aira.life/ca.cer', 'cert_reqs':ssl.CERT_NONE})

    def leaveTheGame(self, who):
        del self.players[who]

    def __str__(self):
        return ', '.join("{!s}={!r}".format(key,val) for (key,val) in self.players.items())

    def __repr__(self):
        return ', '.join("{!s}={!r}".format(key,val) for (key,val) in self.players.items())
