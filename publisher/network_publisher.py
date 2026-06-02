import paho.mqtt.client as mqtt
import json
import random
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/network"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.connect(BROKER, PORT)

while True:
    network_data = {
        "sensor_id": "S001",
        "location": "Messina_Center",
        "connected_to": "Gateway_A",
        "signal_strength": random.randint(60, 100)
    }

    message = json.dumps(network_data)
    client.publish(TOPIC, message)

    print(f"Published network data: {message}")

    time.sleep(5)