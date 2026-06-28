import json
import random
import time
import sys
import os
from datetime import datetime

import paho.mqtt.client as mqtt

# Allow importing config and db from the project root.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from db import mongo_store

ENV_TOPIC = "sensors/environment"
NETWORK_TOPIC = "sensors/network"

# Default sensors used to seed the registry the first time only.
DEFAULT_SENSORS = [
    {"sensor_id": "S001", "zone": "North_Zone",   "location": "Messina_Center",     "room": "Room_101",    "gateway": "Gateway_A"},
    {"sensor_id": "S002", "zone": "South_Zone",   "location": "Messina_Port",       "room": "Room_102",    "gateway": "Gateway_B"},
    {"sensor_id": "S003", "zone": "East_Zone",    "location": "Messina_University",  "room": "Lab_A",       "gateway": "Gateway_C"},
    {"sensor_id": "S004", "zone": "West_Zone",    "location": "Messina_Hospital",   "room": "Lab_B",       "gateway": "Gateway_D"},
    {"sensor_id": "S005", "zone": "Central_Zone", "location": "Messina_Station",    "room": "Server_Room", "gateway": "Gateway_E"},
]


def make_environment(sensor):
    return {
        "sensor_id": sensor["sensor_id"],
        "location": sensor["location"],
        "temperature": round(random.uniform(20, 45), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "air_quality": round(random.uniform(0, 200), 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def make_network(sensor):
    return {
        "sensor_id": sensor["sensor_id"],
        "zone": sensor["zone"],
        "location": sensor["location"],
        "room": sensor["room"],
        "connected_to": sensor["gateway"],
        "signal_strength": random.randint(50, 100),
    }


def main():
    # Make sure the registry has the default sensors the first time.
    mongo_store.seed_sensors(DEFAULT_SENSORS)

    client = mqtt.Client()
    client.connect(config.MQTT_BROKER, config.MQTT_PORT)
    print("Publisher connected. Sending data every 5 seconds (Ctrl-C to stop).")

    while True:
        # Reload the registry each loop so newly added sensors are included.
        sensors = mongo_store.list_sensors()
        if not sensors:
            sensors = DEFAULT_SENSORS
        sensor = random.choice(sensors)

        env_message = json.dumps(make_environment(sensor))
        client.publish(ENV_TOPIC, env_message)
        print("env     ->", env_message)

        net_message = json.dumps(make_network(sensor))
        client.publish(NETWORK_TOPIC, net_message)
        print("network ->", net_message)

        time.sleep(5)


if __name__ == "__main__":
    main()
