import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pymongo import MongoClient
import mysql.connector

#connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iot_database"]
collection = db["sensor_data"]

#connection to MySQL
mysql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="iot_database"
)
mysql_cursor = mysql_connection.cursor()

#connection to MQTT broker
BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/temperature"

#called on connection successful
def on_connect(client, userdata, flags, rc):
    print("connected to MQTT!")
    client.subscribe(TOPIC)

#called when message is received
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    data = json.loads(payload)
    #insertion into MongoDB
    mongo_result = collection.insert_one(data.copy())
    print(f"Data inserted into MongoDB with id: {mongo_result.inserted_id}")

    #insertion into MySQL
    sql = """
    INSERT INTO sensor_readings
    (sensor_id, location, temperature, humidity, air_quality, timestamp)
    VALUES(%s,%s,%s,%s,%s,%s)
    """
    values = (
        data["sensor_id"],
        data["location"],
        data["temperature"],
        data["humidity"],
        data["air_quality"],
        data["timestamp"]
    )
    mysql_cursor.execute(sql, values)
    mysql_connection.commit()

    print("Data inserted into MySQL")

    #display recieved message in terminal 
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
