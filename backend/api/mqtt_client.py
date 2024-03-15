import paho.mqtt.client as mqtt
from config import *

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f"{TOPIC}/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    print(f"MQTT: {topic} {msg.payload}")
    if topic == f"{TOPIC}/in":
        # TODO: Save to database
        pass
    elif topic == f"{TOPIC}/out":
        # TODO: Save to database
        pass


def init_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    # Keepalive 60 seconds
    client.connect(HOSTNAME, MQTT_PORT, 60)
    client.loop_forever()
