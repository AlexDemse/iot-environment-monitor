import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pymongo import MongoClient
import mysql.connector
from neo4j import GraphDatabase

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

#connection to Neo4j
NEO4J_URL = "bolt://localhost:7687" 
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "root12345"

neo4j_driver = GraphDatabase.driver(
    NEO4J_URL,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


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

    #insertion into neo4j
    with neo4j_driver.session() as session:
        session.run(
            """
            MERGE (s:Sensor {sensor_id: $sensor_id})
        SET s.last_temperature = $temperature,
            s.last_humidity = $humidity,
            s.last_air_quality = $air_quality,
            s.last_seen = $timestamp

        MERGE (l:Location {name: $location})
        MERGE (s)-[:LOCATED_IN]->(l)
        """,
        sensor_id=data["sensor_id"],
        location=data["location"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        air_quality=data["air_quality"],
        timestamp=data["timestamp"]
    )

    print("Data inserted into Neo4j!")


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
