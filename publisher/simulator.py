# publisher/simulator.py
# One publisher that simulates several sensors.
# Each loop it sends an environment reading AND a network message,
# so MongoDB, MySQL and Neo4j all get fed.

import json
import random
import time
import sys
import os
from datetime import datetime

import paho.mqtt.client as mqtt

# Allow importing config from the project root.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

ENV_TOPIC = "sensors/environment"
NETWORK_TOPIC = "sensors/network"

# Five fixed sensors, each tied to a zone / location / room / gateway.
# This gives Neo4j a varied 5-level graph.
SENSORS = [
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
        "signal_strength": random.randint(60, 100),
    }


def main():
    client = mqtt.Client()
    client.connect(config.MQTT_BROKER, config.MQTT_PORT)
    print("Publisher connected. Sending data every 5 seconds (Ctrl-C to stop).")

    while True:
        sensor = random.choice(SENSORS)

        env_message = json.dumps(make_environment(sensor))
        client.publish(ENV_TOPIC, env_message)
        print("env     ->", env_message)

        net_message = json.dumps(make_network(sensor))
        client.publish(NETWORK_TOPIC, net_message)
        print("network ->", net_message)

        time.sleep(5)


if __name__ == "__main__":
    main()
