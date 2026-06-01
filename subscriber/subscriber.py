import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temperatute"

#called on connection successful
def on_connect(client, userdata, flags, rc):
    print("connected to MQTT broker!")
    client.subscribe(TOPIC)

#called when message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("waiting for messagges..")

client.loop_forever()
