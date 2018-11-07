import threading
from mqtt_utils import publish_single #, subscribe_callback
import config
import time

import paho.mqtt.client as mqtt
import ssl
import config

class ApproveThread(threading.Thread):
    def __init__(self, gameId, amount_of_players, cb):
        super(ApproveThread, self).__init__()
        print("Game is {} and amount of players is {}".format(gameId, amount_of_players))

        self.callback = cb

        self.topicSend = 'game/{}/player/getfrombank'.format(gameId)
        self.topicRecieve = 'game/{}/player/approved'.format(gameId)
        self.count = amount_of_players

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
            publish_single(self.topicSend, "")

            while self.count > 0:
                time.sleep(1)

        print("And done with Thread")

        self.mqttc.loop_stop()
        self.callback()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code {}".format(rc))
        client.subscribe(self.topicRecieve)

    def on_message(self, client, userdata, message):
        print(client)
        print(message.payload)

        self.count -= 1
        print(self.count)
        if self.count == 0:
            client.disconnect()
