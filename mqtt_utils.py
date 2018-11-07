import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import ssl
import config

def publish_single(topic, data):
    publish.single(topic, data, hostname=config.HOSTNAME, transport=config.TRANSPORT, port=config.PORT, tls={'ca_certs': '/etc/nginx/ssl/mqtt.corp.aira.life/ca.cer', 'cert_reqs':ssl.CERT_NONE})

def publish_multiple(msgs):
    publish.multiple(msgs, hostname=config.HOSTNAME, transport=config.TRANSPORT, port=config.PORT, tls={'ca_certs': '/etc/nginx/ssl/mqtt.corp.aira.life/ca.cer', 'cert_reqs':ssl.CERT_NONE})

def subscribe_callback(cb, topic):
    subscribe.callback(cb, topic, hostname=config.HOSTNAME, transport=config.TRANSPORT, port=config.PORT, tls={'ca_certs': '/etc/nginx/ssl/mqtt.corp.aira.life/ca.cer', 'cert_reqs':ssl.CERT_NONE})
