import paho.mqtt.client as mqtt
import json
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temperatute"

#called on connection successful
def on_connect(client, userdata, flags, rc):
    print("connected to MQTT broker!")
    client.subscribe(TOPIC)

#called when message is received
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    data = json.loads(payload)

    print("\n New Sensor Data Received:")
    print(f"Sensor ID: {data['sensor_id']}")
    print(f"Temperature: {data['temperature']}°C")
    print(f"Humidity: {data['humidity']}%")
    print(f"Air Quality: {data['air_quality']}")
    print(f"Timestamp: {datetime.fromisoformat(data['timestamp'])}")
    print(f"Location: {data['location']}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("waiting for messagges..")

client.loop_forever()
