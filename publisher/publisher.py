import paho.mqtt.client as mqtt
import json
import random
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temperatute"

client = mqtt.Client()

client.connect(BROKER, PORT)

while True:
    sensor_data = {
        "sensor_id": "5001",
        "temprature": round(random.uniform(20, 35), 2)
    }
    message = json.dumps(sensor_data)

    client.publish(TOPIC, message)

    print(f"Published: {message}")

    time.sleep(3)