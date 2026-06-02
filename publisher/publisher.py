import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

BROKER = "localhost"
PORT = 1883
topic = "sensors/enviroment"

client = mqtt.Client()

client.connect(BROKER, PORT)

while True:
    sensor_data = {
        "sensor_id": "5001",
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "air_quality": round(random.uniform(0, 100), 2),
        "timestamp": datetime.now().isoformat(),
        "location": "Messina_center",
    }
    message = json.dumps(sensor_data)

    client.publish(topic, message)

    print(f"Published: {message}")

    time.sleep(5)
    