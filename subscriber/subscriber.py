# subscriber/subscriber.py
# Thin subscriber: it only listens to MQTT and hands each message to the router.
# All the storing logic lives in core/router.py and the db/ modules.

import json
import sys
import os

import paho.mqtt.client as mqtt

# Allow importing config and core from the project root.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core import router

TOPIC = "sensors/#"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker.")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        summary = router.handle_message(msg.topic, data)
        print(summary)
    except Exception as error:
        print("Error handling message:", error)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.MQTT_BROKER, config.MQTT_PORT)
    print("Waiting for messages...")
    client.loop_forever()


if __name__ == "__main__":
    main()
