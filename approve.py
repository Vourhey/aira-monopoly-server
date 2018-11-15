import threading
from mqtt_utils import publish_single #, subscribe_callback
import config
import time
import json

import paho.mqtt.client as mqtt
import ssl
import config

class ApproveThread(threading.Thread):
    def __init__(self, gameId, amount_of_players, cb, playerId=None, amountXRT=0):
        super(ApproveThread, self).__init__()
        print("Game is {} and amount of players is {}".format(gameId, amount_of_players))

        self.callback = cb
        self.playerId = playerId
        self.amountXRT = amountXRT

        self.topicSend = 'game/{}/player/getfrombank'.format(gameId)
        self.topicRecieve = 'game/{}/player/approved'.format(gameId)
        self.count = amount_of_players
        self.rejected = 0
        self.approved = True

        self.mqttc = mqtt.Client(transport=config.TRANSPORT)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.tls_set(ca_certs='/etc/nginx/ssl/mqtt.corp.aira.life/ca.cer', cert_reqs=ssl.CERT_NONE)
        self.mqttc.connect(config.HOSTNAME, port=config.PORT)
        self.mqttc.loop_start()

        print("Finish initialization")

    def run(self):
        print("Started thread with {} players".format(self.count))

        if self.count != 0:
            payload = {
                'playerId': self.playerId,
                'amountXRT': self.amountXRT
            }
            publish_single(self.topicSend, json.dumps(payload))

            while self.count > 0:
                if self.rejected > 0:
                    self.approved = False
                    break
                time.sleep(1)

        print("And done with Thread")

        self.mqttc.loop_stop()
        self.mqttc.disconnect()
        print(self.approved)
        self.callback(self.approved)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code {}".format(rc))
        client.subscribe(self.topicRecieve)

    def on_message(self, client, userdata, message):
        print(client)
        print(message.payload)

        answer = message.payload

        if message.payload == '1':
            print("Approved")
            self.count -= 1
        else:
            print("Rejected")
            self.rejected += 1
