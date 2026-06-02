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
topic = "sensors/#"

#called on connection successful
def on_connect(client, userdata, flags, rc):
    print("connected to MQTT!")
    client.subscribe(topic)

#called when message is received
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    data = json.loads(payload)

    #display recieved message in terminal 
    print("\n New Sensor Data Received:")
    print(f"TOPIC: {topic}")
    print(f"Sensor ID: {data['sensor_id']}")
    print(f"Temperature: {data['temperature']}°C")
    print(f"Humidity: {data['humidity']}%")
    print(f"Air Quality: {data['air_quality']}")
    print(f"Timestamp: {datetime.fromisoformat(data['timestamp'])}")
    print(f"Location: {data['location']}")

    
    if topic == "sensors/enviroment":

        #insertion into mongoDB
        alerts = []

        if data["temperature"] > 35:
            alerts.append({
                "type": "temperature",
                "level": "high",
                "message": "High temperature detected"
            })

        if data["humidity"] > 70:
            alerts.append({
                "type": "humidity",
                "level": "high",
                "message": "High humidity detected"
            })

        if data["air_quality"] > 150:
            alerts.append({
                "type": "air_quality",
                "level": "danger",
                "message": "Poor air quality detected"
            })

        mongo_document = {
            "sensor_id": data["sensor_id"],
            "location": data["location"],
            "readings": {
                "temperature": data["temperature"],
                "humidity": data["humidity"],
                "air_quality": data["air_quality"]
            },
            "alerts": alerts,
            "has_alert": len(alerts) > 0,
            "timestamp": data["timestamp"],
            "source_topic": topic
        }

        collection.insert_one(mongo_document)
        print("Event inserted into MongoDB")
        

        #insertion into MongoDB
        #mongo_result = collection.insert_one(data.copy())
        #print(f"Data inserted into MongoDB with id: {mongo_result.inserted_id}")

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


    elif topic == "sensors/network":
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
        print("Network relationship inserted into Neo4j!")
    
    else:
        print("unknown topic", topic)
    
    

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("waiting for messagges..")

client.loop_forever()
